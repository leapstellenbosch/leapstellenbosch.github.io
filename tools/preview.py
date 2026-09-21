"""
Rough local preview of the LEAP site WITHOUT Ruby or Jekyll.

    python tools/preview.py            build into the temp folder and serve http://localhost:4000
    python tools/preview.py --build    build only

This is a small re-implementation of the subset of Liquid that this site's
templates use. It exists so the design can be checked on a machine that has
Python but no Ruby. It is NOT Jekyll: the real build runs on GitHub Actions
(or `bundle exec jekyll serve`), and that build is the one that counts. If a
template starts using a Liquid feature this script does not know, it says so.

Requires Python 3 with PyYAML and markdown-it-py.
"""
import datetime as dt
import html
import http.server
import re
import shutil
import socketserver
import sys
import tempfile
from functools import partial
from pathlib import Path

import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(tempfile.gettempdir()) / "leap-preview"    # outside Dropbox, so builds do not churn the sync
MD = MarkdownIt("commonmark", {"html": True, "typographer": True}).enable(["replacements", "smartquotes", "table"])
TOKEN = re.compile(r"(\{\{-?.*?-?\}\}|\{%-?.*?-?%\})", re.S)


# ----------------------------------------------------------------- expressions
def split_outside_quotes(s, sep):
    parts, buf, q = [], "", None
    i = 0
    while i < len(s):
        c = s[i]
        if q:
            buf += c
            if c == q:
                q = None
        elif c in "\"'":
            q = c; buf += c
        elif s.startswith(sep, i):
            parts.append(buf); buf = ""; i += len(sep); continue
        else:
            buf += c
        i += 1
    parts.append(buf)
    return parts


def lookup(path, ctx):
    cur = ctx
    for key in path.split("."):
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        elif key == "size" and hasattr(cur, "__len__"):
            cur = len(cur)
        elif key == "first" and isinstance(cur, list):
            cur = cur[0] if cur else None
        elif key == "last" and isinstance(cur, list):
            cur = cur[-1] if cur else None
        else:
            return None
    return cur


def atom(tok, ctx):
    tok = tok.strip()
    if not tok:
        return None
    if tok[0] in "\"'" and tok[-1] == tok[0]:
        return tok[1:-1]
    if re.fullmatch(r"-?\d+", tok):
        return int(tok)
    if re.fullmatch(r"-?\d*\.\d+", tok):
        return float(tok)
    if tok in ("true", "false"):
        return tok == "true"
    if tok in ("nil", "null", "empty", "blank"):
        return None
    return lookup(tok, ctx)


def to_date(v, ctx):
    if isinstance(v, dt.datetime):
        return v
    if isinstance(v, dt.date):
        return dt.datetime(v.year, v.month, v.day)
    if v in ("now", "today"):
        return dt.datetime.now()
    return dt.datetime.fromisoformat(str(v)[:10])


def f_date(v, fmt, ctx):
    d = to_date(v, ctx)
    fmt = fmt.replace("%-d", str(d.day)).replace("%-m", str(d.month))
    return d.strftime(fmt)


def f_where(v, key, val, ctx):
    return [x for x in (v or []) if isinstance(x, dict) and x.get(key) == val]


def f_group_by(v, key, ctx):
    groups = {}
    for x in v or []:
        groups.setdefault(str(x.get(key)), []).append(x)
    return [{"name": k, "items": it, "size": len(it)} for k, it in groups.items()]


def f_group_by_exp(v, var, exp, ctx):
    groups = {}
    for x in v or []:
        groups.setdefault(str(evaluate(exp, {**ctx, var: x})), []).append(x)
    return [{"name": k, "items": it, "size": len(it)} for k, it in groups.items()]


def f_truncatewords(v, n, ctx):
    words = str(v or "").split()
    return " ".join(words[:n]) + ("..." if len(words) > n else "")


def num(v):
    return v if isinstance(v, (int, float)) else float(v)


FILTERS = {
    "relative_url": lambda v, ctx: ctx["site"]["baseurl"] + str(v),
    "absolute_url": lambda v, ctx: ctx["site"]["url"] + ctx["site"]["baseurl"] + str(v),
    "append": lambda v, a, ctx: str(v if v is not None else "") + str(a if a is not None else ""),
    "prepend": lambda v, a, ctx: str(a) + str(v),
    "default": lambda v, a, ctx: a if v in (None, False, "") else v,
    "date": f_date,
    "where": f_where,
    "first": lambda v, ctx: (v[0] if v else None),
    "last": lambda v, ctx: (v[-1] if v else None),
    "size": lambda v, ctx: len(v or []),
    "split": lambda v, sep, ctx: str(v or "").split(sep),
    "slice": lambda v, start, *rest: str(v or "")[start:start + (rest[0] if len(rest) > 1 else 1)],
    "markdownify": lambda v, ctx: MD.render(str(v or "")),
    "group_by": f_group_by,
    "group_by_exp": f_group_by_exp,
    "sort": lambda v, *a: sorted(v or [], key=(lambda x: x.get(a[0])) if len(a) > 1 else None),
    "reverse": lambda v, ctx: list(reversed(v or [])),
    "map": lambda v, key, ctx: [x.get(key) for x in v or []],
    "remove": lambda v, a, ctx: str(v or "").replace(a, ""),
    "replace": lambda v, a, b, ctx: str(v or "").replace(a, b),
    "escape": lambda v, ctx: html.escape(str(v or "")),
    "strip_html": lambda v, ctx: re.sub(r"<[^>]+>", "", str(v or "")),
    "strip": lambda v, ctx: str(v or "").strip(),
    "truncatewords": f_truncatewords,
    "downcase": lambda v, ctx: str(v or "").lower(),
    "upcase": lambda v, ctx: str(v or "").upper(),
    "minus": lambda v, a, ctx: num(v) - num(a),
    "plus": lambda v, a, ctx: num(v) + num(a),
    "times": lambda v, a, ctx: num(v) * num(a),
    "join": lambda v, sep, ctx: sep.join(str(x) for x in v or []),
}


def evaluate(expr, ctx):
    parts = split_outside_quotes(expr, "|")
    val = atom(parts[0], ctx)
    for f in parts[1:]:
        name, _, argstr = f.strip().partition(":")
        name = name.strip()
        if name not in FILTERS:
            raise SystemExit(f"preview.py does not know the Liquid filter '{name}'")
        args = [atom(a, ctx) for a in split_outside_quotes(argstr, ",")] if argstr.strip() else []
        val = FILTERS[name](val, *args, ctx)
    return val


def truthy(v):
    return v is not None and v is not False


def compare(cond, ctx):
    m = re.match(r"^(.*?)\s+(==|!=|<=|>=|<|>|contains)\s+(.*)$", cond.strip())
    if not m:
        return truthy(evaluate(cond, ctx))
    a, op, b = evaluate(m.group(1), ctx), m.group(2), evaluate(m.group(3), ctx)
    if op == "==": return a == b
    if op == "!=": return a != b
    if op == "contains": return a is not None and b in a
    if a is None or b is None: return False
    return {"<": a < b, ">": a > b, "<=": a <= b, ">=": a >= b}[op]


def condition(cond, ctx):
    return any(all(compare(c, ctx) for c in split_outside_quotes(o, " and ")) for o in split_outside_quotes(cond, " or "))


# ---------------------------------------------------------------------- parser
def tokenize(src):
    toks = TOKEN.split(src)
    for i, t in enumerate(toks):                 # whitespace control
        if i % 2 == 1:
            if t[2] == "-" and i > 0:
                toks[i - 1] = toks[i - 1].rstrip()
            if t[-3] == "-" and i + 1 < len(toks):
                toks[i + 1] = toks[i + 1].lstrip()
    out = []
    for i, t in enumerate(toks):
        if i % 2 == 0:
            if t: out.append(("text", t))
        else:
            out.append(("out" if t.startswith("{{") else "tag", t[2:-2].strip("-").strip()))
    return out


def parse(tokens, pos=0, until=()):
    nodes = []
    while pos < len(tokens):
        kind, val = tokens[pos]
        if kind != "tag":
            nodes.append((kind, val)); pos += 1; continue
        word = val.split()[0]
        if word in until:
            return nodes, pos
        rest = val[len(word):].strip()
        if word == "comment":
            while tokens[pos] != ("tag", "endcomment"): pos += 1
            pos += 1
        elif word == "assign":
            name, _, expr = rest.partition("=")
            nodes.append(("assign", name.strip(), expr.strip())); pos += 1
        elif word in ("if", "unless"):
            branches, cond = [], rest
            while True:
                body, pos = parse(tokens, pos + 1, ("elsif", "else", "endif", "endunless"))
                branches.append((cond, body))
                w = tokens[pos][1].split()[0]
                if w == "elsif": cond = tokens[pos][1][5:].strip()
                elif w == "else": cond = None
                else: break
            nodes.append((word, branches)); pos += 1
        elif word == "for":
            m = re.match(r"(\w+)\s+in\s+(.+?)(?:\s+limit:\s*(\d+))?$", rest)
            body, pos = parse(tokens, pos + 1, ("endfor",))
            nodes.append(("for", m.group(1), m.group(2), int(m.group(3)) if m.group(3) else None, body)); pos += 1
        elif word == "include":
            name, _, params = rest.partition(" ")
            nodes.append(("include", name, re.findall(r"(\w+)=(\"[^\"]*\"|'[^']*'|[^\s]+)", params))); pos += 1
        elif word in ("seo", "feed_meta"):
            nodes.append((word,)); pos += 1
        else:
            raise SystemExit(f"preview.py does not know the Liquid tag '{word}'")
    return nodes, pos


def render_nodes(nodes, ctx):
    out = []
    for n in nodes:
        k = n[0]
        if k == "text":
            out.append(n[1])
        elif k == "out":
            v = evaluate(n[1], ctx)
            out.append("" if v is None else str(v))
        elif k == "assign":
            ctx[n[1]] = evaluate(n[2], ctx)
        elif k in ("if", "unless"):
            for i, (cond, body) in enumerate(n[1]):
                ok = True if cond is None else condition(cond, ctx)
                if k == "unless" and i == 0: ok = not ok
                if ok:
                    out.append(render_nodes(body, ctx)); break
        elif k == "for":
            items = evaluate(n[2], ctx) or []
            if n[3]: items = items[:n[3]]
            for i, item in enumerate(items):
                ctx[n[1]] = item
                ctx["forloop"] = {"index": i + 1, "index0": i, "rindex": len(items) - i, "first": i == 0, "last": i == len(items) - 1, "length": len(items)}
                out.append(render_nodes(n[4], ctx))
        elif k == "include":
            sub = dict(ctx); sub["include"] = {name: atom(val, ctx) for name, val in n[2]}
            out.append(render((ROOT / "_includes" / n[1]).read_text(encoding="utf-8"), sub))
            for key in ctx:                       # Jekyll includes share the caller's variables
                if key in sub and key != "include": ctx[key] = sub[key]
        elif k == "seo":
            page, site = ctx["page"], ctx["site"]
            title = f"{page['title']} | {site['title']}" if page.get("title") else f"{site['title']} | {site['tagline']}"
            desc = page.get("description") or page.get("summary") or site["description"]
            out.append(f"<title>{html.escape(title)}</title>\n  <meta name=\"description\" content=\"{html.escape(desc)}\">")
        elif k == "feed_meta":
            out.append('<link type="application/atom+xml" rel="alternate" href="/feed.xml" title="LEAP">')
    return "".join(out)


def render(src, ctx):
    nodes, _ = parse(tokenize(src))
    return render_nodes(nodes, ctx)


# ------------------------------------------------------------------------ site
def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    return (yaml.safe_load(m.group(1)) or {}, m.group(2)) if m else (None, text)


def in_layout(page, body, site):
    layout = page.get("layout")
    while layout:
        fm, src = front_matter(ROOT / "_layouts" / f"{layout}.html")
        body = render(src, {"site": site, "page": page, "content": body})
        layout = (fm or {}).get("layout")
    return body


def build():
    cfg = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8"))
    site = {**cfg, "baseurl": "", "time": dt.datetime.now(),
            "data": {p.stem: yaml.safe_load(p.read_text(encoding="utf-8")) for p in (ROOT / "_data").glob("*.yml")}}
    posts = []
    for p in sorted((ROOT / "_posts").glob("*.md"), reverse=True):
        fm, body = front_matter(p)
        y, m, d, slug = re.match(r"(\d+)-(\d+)-(\d+)-(.+)\.md", p.name).groups()
        fm = {"layout": "post", "section": "news", **fm, "date": to_date(fm.get("date") or f"{y}-{m}-{d}", None), "url": f"/news/{y}/{slug}/", "_body": body}
        posts.append(fm)
    posts.sort(key=lambda x: x["date"], reverse=True)
    site["posts"] = posts

    OUT.mkdir(exist_ok=True)
    for child in OUT.iterdir():                  # empty it, but keep the folder: a running server may hold it open
        shutil.rmtree(child, ignore_errors=True) if child.is_dir() else child.unlink()
    shutil.copytree(ROOT / "assets", OUT / "assets", dirs_exist_ok=True)
    for post in posts:
        content = MD.render(render(post["_body"], {"site": site, "page": post}))
        post["content"] = content
        post["excerpt"] = content.split("</p>")[0] + "</p>"
    for post in posts:
        dest = OUT / post["url"].strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(in_layout(post, post["content"], site), encoding="utf-8")
    for src in [ROOT / "index.html", *ROOT.glob("*/index.html")]:
        if src.parent.name.startswith(("_", ".")): continue
        fm, body = front_matter(src)
        if fm is None: continue
        rel = src.parent.relative_to(ROOT)
        page = {"layout": "default", **fm, "url": "/" + (rel.as_posix() + "/" if str(rel) != "." else "")}
        dest = OUT / rel / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(in_layout(page, render(body, {"site": site, "page": page}), site), encoding="utf-8")
        print("built", page["url"])
    print("built", len(posts), "posts ->", OUT)


if __name__ == "__main__":
    build()
    if "--build" not in sys.argv:
        handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        with socketserver.TCPServer(("127.0.0.1", 4000), handler) as srv:
            print("Preview at http://localhost:4000  (Ctrl+C to stop)")
            srv.serve_forever()
