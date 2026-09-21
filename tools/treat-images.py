"""
LEAP website image pipeline.

Run once locally (python tools/treat-images.py) whenever a source photograph
changes. It is NOT part of the site build: the treated files in assets/img/
are committed to the repository.

What it does
  1. Archival photographs -> greyscale -> two-colour LUT (shadow -> highlight,
     one pair per LEAP letter) -> film grain -> slight vignette.
     Exported as WebP and JPEG at 1800px and 900px wide.
  2. Headshots -> square crop around the face -> 600px JPEG.
  3. Social card (1200x630) and PNG favicon.

Requires Python 3 with Pillow. Source folders are on Johan's Dropbox; edit
SRC and HEADSHOT_SRC if they move.
"""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter, ImageChops

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(r"C:\Users\johanf\Dropbox\5 LEAP")
HEADSHOT_SRC = ROOT / "_sources" / "headshots"      # photos found for members without a studio portrait
OUT = ROOT / "assets" / "img"
FONTS = ROOT / "assets" / "fonts"

# ---- Duotone pairs: (shadow, highlight). One per letter, plus a neutral maroon.
TONES = {
    "sage":   ("#16241a", "#c3d9b0"),   # L  contour map
    "earth":  ("#2a1c0e", "#e4d5b5"),   # E  archival paper
    "blue":   ("#0d2636", "#b4d9ee"),   # A  manuscript ink
    "plum":   ("#2e0f25", "#d6a9bf"),   # P  weave (plum -> rose)
    "maroon": ("#1a0b12", "#e9dcc6"),   # neutral: project images, quote band
}

# ---- Archival images: name -> (source, tone, crop box as fractions l,t,r,b, rotate)
ARCHIVE = {
    # Hero letters
    "hero-l":   (r"Photos\Website photos\IMG_4202.JPG",            "sage",  (0.05, 0.00, 0.75, 1.00), 0),
    "hero-e":   (r"Photos\Website photos\Barberton.JPG",           "earth", (0.10, 0.12, 0.95, 0.92), 0),
    "hero-a":   (r"Photos\Website photos\Archive.jpg",             "blue",  (0.04, 0.05, 0.86, 0.95), 0),
    "hero-p":   (r"Photos\Projects\Living standards.JPG",          "plum",  (0.08, 0.14, 0.92, 0.95), 0),
    # Section motifs
    "motif-e":  (r"Photos\Limited Liability\Swaziland Concession.jpeg", "earth", (0.10, 0.22, 0.92, 0.80), 0),
    "motif-a":  (r"Photos\Website photos\Archive.jpg",             "blue",  (0.04, 0.10, 0.86, 0.70), 0),
    # Quote band
    "quote":    (r"Photos\Lab\high-res\LEAP lab 03.jpg",           "maroon", (0.00, 0.05, 1.00, 0.95), 0),
}

PROJECTS = {
    "project-1834":        (r"Photos\Exhibit\Runaway2.jpg",                       "maroon", (0.00, 0.22, 1.00, 0.78), 0),
    "cape-panel":          (r"Photos\Faces\Projects\Cape of Good Hope.tif",       "maroon", (0.00, 0.04, 1.00, 0.96), 0),
    "time-traveller":      (r"Photos\Limited Liability\Swaziland Concession.jpeg", "earth", (0.08, 0.10, 0.95, 0.55), 0),
    "frontiers-of-finance":(r"Photos\Limited Liability\IMG_6028.JPG",             "maroon", (0.10, 0.08, 0.95, 0.85), 0),
    "indigenous-economies":(r"Photos\Faces\Projects\Black living standards.tif",  "maroon", (0.00, 0.00, 1.00, 0.90), 0),
    "chair":               (r"Photos\Website photos\Barberton.JPG",               "maroon", (0.10, 0.20, 0.95, 0.85), 0),
}

# ---- Headshots: key -> (source, face centre x, face centre y, square side as fraction of width)
TEAM = {
    "johan-fourie":      (SRC / r"Photos\Faces\Johan.jpg",     0.49, 0.150, 0.78),
    "dieter-von-fintel": (SRC / r"Photos\Faces\Dieter.jpg",    0.50, 0.170, 0.78),
    "calumet-links":     (SRC / r"Photos\Faces\Cal.jpg",       0.49, 0.160, 0.80),
    "edward-kerby":      (SRC / r"Photos\Faces\Edward.jpg",    0.50, 0.150, 0.78),
    # Found online or in the old site's backup: see _sources/headshots/PROVENANCE.md
    "kate-ekama":           (HEADSHOT_SRC / "kate-ekama.jpg",            0.50, 0.42, 1.00),
    "karl-bergemann":       (HEADSHOT_SRC / "karl-bergemann.jpg",        0.50, 0.42, 1.00),
    "munashe-chideya":      (HEADSHOT_SRC / "munashe-chideya.jpg",       0.50, 0.27, 0.90),
    "noah-macdonald":       (HEADSHOT_SRC / "noah-macdonald.jpg",        0.53, 0.42, 0.62),
    "etienne-le-rossignol": (HEADSHOT_SRC / "etienne-le-rossignol.jpg",  0.50, 0.42, 1.00),
    "jan-hendrik-pretorius":(HEADSHOT_SRC / "jan-hendrik-pretorius.webp", 0.50, 0.42, 1.00),
}
BOARD = {
    "ada-jansen":          (HEADSHOT_SRC / "ada-jansen.jpg",      0.47, 0.24, 1.00),
    "sophia-du-plessis":   (SRC / r"Photos\Faces\Sophia.jpg",     0.50, 0.180, 0.78),
    "janine-myburgh":      (SRC / r"Governing Board\Janine.jpg",  0.50, 0.340, 0.95),
    "kanshukan-rajaratnam":(SRC / r"Governing Board\Kanshu.png",  0.47, 0.300, 0.95),
    "mohamed-saleh":       (SRC / r"Governing Board\Mohamed.jpg", 0.52, 0.420, 0.46),
    "kris-inwood":         (SRC / r"Governing Board\Kris.jpg",    0.50, 0.500, 1.00),
}


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def load(path, box=None, rotate=0):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    if rotate:
        im = im.rotate(rotate, expand=True)
    if box:
        w, h = im.size
        l, t, r, b = box
        im = im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))
    return im


def duotone(im, tone, grain=0.05, vignette=0.35):
    shadow, highlight = (hex2rgb(c) for c in TONES[tone])
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    out = ImageOps.colorize(g, black=shadow, white=highlight)
    if grain:
        noise = Image.effect_noise(out.size, 40).convert("RGB")
        out = Image.blend(out, ImageChops.overlay(out, noise), grain * 4)
    if vignette:
        w, h = out.size
        mask = Image.new("L", (256, 256), 0)
        ImageDraw.Draw(mask).ellipse((-40, -40, 296, 296), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(50)).resize((w, h))
        dark = Image.new("RGB", (w, h), shadow)
        out = Image.composite(out, Image.blend(out, dark, vignette), mask)
    return out


def export(im, stem, folder, widths=(1800, 900)):
    folder.mkdir(parents=True, exist_ok=True)
    for w in widths:
        r = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(folder / f"{stem}-{w}.webp", quality=78, method=6)
        r.save(folder / f"{stem}-{w}.jpg", quality=80, optimize=True, progressive=True)


def headshot(path, cx, cy, s, out, size=600):
    im = load(path).convert("RGB")
    w, h = im.size
    side = min(int(s * w), w, h)
    l = min(max(int(cx * w - side / 2), 0), w - side)
    t = min(max(int(cy * h - side * 0.42), 0), h - side)
    im = im.crop((l, t, l + side, t + side)).resize((size, size), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=84, optimize=True, progressive=True)


def social_card():
    """1200x630 Open Graph card: LEAP set in Raleway ExtraBold, each letter a window onto its texture."""
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), hex2rgb("#120a0e"))
    glow = Image.new("RGB", (W, H), hex2rgb("#421628"))
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse((500, -400, 1500, 400), fill=160)
    card = Image.composite(glow, card, m.filter(ImageFilter.GaussianBlur(160)))
    big = ImageFont.truetype(str(FONTS / "Raleway-ExtraBold.ttf"), 330)
    d = ImageDraw.Draw(card)
    x = 78
    for ch, stem in zip("LEAP", ("hero-l", "hero-e", "hero-a", "hero-p")):
        tex = Image.open(OUT / "archive" / f"{stem}-900.jpg").convert("RGB")
        bbox = big.getbbox(ch)
        cw, chh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        tex = ImageOps.fit(tex, (cw + 8, chh + 8), Image.LANCZOS)
        mask = Image.new("L", tex.size, 0)
        ImageDraw.Draw(mask).text((-bbox[0] + 4, -bbox[1] + 4), ch, font=big, fill=255)
        card.paste(tex, (x, 110), mask)
        x += cw + 22
    small = ImageFont.truetype(str(FONTS / "Raleway-SemiBold.ttf"), 25)
    d.text((84, 462), "LABORATORY FOR THE ECONOMICS OF AFRICA'S PAST", font=small, fill=hex2rgb("#a78e53"))
    light = ImageFont.truetype(str(FONTS / "Raleway-Light.ttf"), 30)
    d.text((84, 508), "Stellenbosch University", font=light, fill=(244, 239, 230))
    d.line((84, 445, 1116, 445), fill=hex2rgb("#a78e53"), width=1)
    card.save(OUT / "social-card.jpg", quality=88, optimize=True)


def favicon_png():
    """Four letter-colour bars over a gold rule on ink, echoing the letterhead accent strip."""
    S = 256
    im = Image.new("RGB", (S, S), hex2rgb("#120a0e"))
    d = ImageDraw.Draw(im)
    for i, c in enumerate(("#6B8E5E", "#8B6B3D", "#3D8EB9", "#7d3a63")):
        x = 44 + i * 44
        d.rectangle((x, 56 + (i % 2) * 18, x + 30, 178), fill=hex2rgb(c))
    d.rectangle((44, 192, 206, 198), fill=hex2rgb("#a78e53"))
    im.resize((64, 64), Image.LANCZOS).save(ROOT / "assets" / "favicon.png")


if __name__ == "__main__":
    import sys
    only = set(sys.argv[1:])
    def want(k): return not only or k in only

    if want("archive"):
        for stem, (src, tone, box, rot) in ARCHIVE.items():
            export(duotone(load(SRC / src, box, rot), tone), stem, OUT / "archive")
            print("archive", stem)
    if want("projects"):
        for stem, (src, tone, box, rot) in PROJECTS.items():
            export(duotone(load(SRC / src, box, rot), tone, vignette=0.25), stem, OUT / "projects", widths=(1400, 700))
            print("project", stem)
    if want("faces"):
        for key, (src, cx, cy, s) in TEAM.items():
            headshot(src, cx, cy, s, OUT / "team" / f"{key}.jpg"); print("team", key)
        for key, (src, cx, cy, s) in BOARD.items():
            headshot(src, cx, cy, s, OUT / "board" / f"{key}.jpg"); print("board", key)
    if want("card"):
        social_card(); favicon_png(); print("card + favicon")
