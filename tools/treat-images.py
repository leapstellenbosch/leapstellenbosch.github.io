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
GALLERY_SRC = ROOT / "_sources" / "gallery"         # LEAP's own photographs, supplied by Johan (originals not in git)
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
}

# ---- Quote band: one Elliott Collection photograph behind each quotation in _data/quotes.yml.
# stem -> (file in DATA\Archive photos\Elliot Collection, crop box l,t,r,b). Crops are about 2:1
# and leave out the archive stamps and card edges.
ELLIOTT = Path(r"C:\Users\johanf\Dropbox\3 Data\Archive photos\Elliot Collection")
QUOTES = {
    "quote-e1207": ("E1207 Old house, Dorp Street, Stellenbosch.tif",                         (0.00, 0.08, 1.00, 0.78)),
    "quote-e5321": ("E5321 Front Toneel in Zululand.tif",                                     (0.00, 0.15, 1.00, 0.82)),
    "quote-e7841": ("E7841 Front Convicts Picking grapes - Groot Constantia..tif",            (0.00, 0.28, 0.98, 0.97)),
    "quote-e7894": ("E7894 Front Dr Jameson Addressing Railway Workers - Salt River (1905)..tif", (0.00, 0.30, 1.00, 1.00)),
    "quote-e8110": ("E8110 Front Transporting Wool at Wolseley.tif",                          (0.02, 0.22, 0.99, 0.92)),
    "quote-e8308": ("E8308 Front Parade Sales - Cape Town..tif",                              (0.00, 0.26, 1.00, 0.93)),
    "quote-e8615": ("E8615 Front Sifting Diamonds - Kimberley.tif",                           (0.00, 0.12, 1.00, 0.82)),
}

# ---- Home page letters: several sources per letter, one drawn at random on each visit.
# stem -> (source, crop box as fractions l,t,r,b, rotation in degrees, clockwise negative).
# The tone follows the letter. Captions live in _data/hero.yml; origins in _sources/hero/SOURCES.md.
# L maps · E photographs and pictures · A handwriting · P printed records
DATA = Path(r"C:\Users\johanf\Dropbox\3 Data")
AP = DATA / "Archive photos"
CP = Path(r"C:\Users\johanf\Dropbox\3 Cape Panel")
HERO_SRC = ROOT / "_sources" / "hero"           # pages rendered from PDFs: see _sources/hero/SOURCES.md

def ap(folder, ref):
    """An archive photograph by its reference number: the file names are long descriptions."""
    hits = sorted((AP / folder).glob(ref + "*.tif"))
    if not hits:
        raise FileNotFoundError(f"{folder}/{ref}*.tif")
    return hits[0]

HERO = {
    "sage": {
        "l-free-state-map":    (SRC / r"Photos\Website photos\IMG_4202.JPG",                          (0.05, 0.00, 0.75, 1.00), 0),
        "l-africa-de-wit":     (DATA / r"Maps\JN12021 - KHC AF - 1660 DE WIT.tif",                    (0.22, 0.10, 0.78, 0.88), 0),
        "l-africa-1578":       (ap("Elliot Collection", "E4430"),                                     (0.04, 0.04, 0.96, 0.66), 0),
        "l-cape-town-1897":    (DATA / r"Maps\CapeTown1897.jpg",                                      (0.15, 0.08, 0.85, 0.80), 0),
        "l-cadastral-albert":  (DATA / r"Robert Ross maps\Cape Colony Cadastral Maps c.1890 M3 Series\1588\Cadastral Maps For Professor Ross 063.jpg", (0.08, 0.10, 0.80, 0.95), 0),
    },
    "earth": {
        "e-barberton":         (SRC / r"Photos\Website photos\Barberton.JPG",                         (0.10, 0.12, 0.95, 0.92), 0),
        "e-rogge-bay":         (ap("2020", "AG983"),                                                  (0.03, 0.10, 0.97, 0.95), 0),
        "e-wine-farm":         (ap("2020", "AG1044"),                                                 (0.00, 0.22, 1.00, 0.95), 0),
        "e-east-london":       (ap("2020", "AG1101"),                                                 (0.00, 0.25, 1.00, 0.92), 0),
        "e-sifting-diamonds":  (ap("Elliot Collection", "E8615"),                                     (0.25, 0.15, 1.00, 1.00), 0),
        "e-wool-wolseley":     (ap("Elliot Collection", "E8110"),                                     (0.00, 0.15, 0.92, 0.93), 0),
        "e-brandes-cape-town": (CP / "Brandes.jpg",                                                   (0.40, 0.05, 0.80, 1.00), 0),
    },
    "blue": {
        "a-estate-inventory":  (SRC / r"Photos\Website photos\Archive.jpg",                           (0.04, 0.05, 0.86, 0.95), 0),
        "a-opgaafrol":         (CP / "FirstOpgaafrol.jpg",                                            (0.04, 0.06, 0.94, 0.42), 0),
        "a-estate-letter-1926":(DATA / r"Black inventories\KBN_3-1-1\32-2-36\IMG_0992.JPG",           (0.08, 0.14, 0.96, 0.80), 0),
        "a-cape-police":       (DATA / r"Attestations\Cape Mounted Police\20140107_105717.jpg",       (0.05, 0.18, 0.95, 0.82), -90),
        "a-zar-certificate":   (SRC / r"Photos\Limited Liability\IMG_3344.JPG",                       (0.05, 0.12, 0.98, 0.80), 0),
        "a-register":          (SRC / r"Photos\Limited Liability\IMG_6647.JPG",                       (0.02, 0.05, 0.62, 0.95), 0),
    },
    "plum": {
        "p-attestation-paper": (SRC / r"Photos\Projects\Living standards.JPG",                        (0.08, 0.14, 0.92, 0.95), 0),
        "p-slave-return-1834": (DATA / r"Valuation rolls\T71.8 Valuation Roll Swellendam\IMG_0629.JPG", (0.04, 0.04, 0.96, 0.72), -90),
        "p-gazette-1830":      (DATA / r"Gazettes\1830 Jan-Dec\IMG_6876.JPG",                         (0.03, 0.05, 0.97, 0.68), 0),
        "p-census-1865":       (HERO_SRC / "census-1865-produce.png",                                 (0.10, 0.06, 0.97, 0.56), 0),
        "p-bantu-world":      (DATA / r"Bantu World\nf-s-000015-n1\nf-s-000015-n1 (Page 11).png",    (0.02, 0.03, 0.50, 0.72), 0),
        "p-voters-roll":       (DATA / r"Voters Rolls\1870-1909\27\10. Wodehouse\IMG_7306.JPG",       (0.22, 0.10, 0.51, 0.90), 0),
        "p-wages-1909":        (DATA / r"Occupations and wages\Agri data wages 1909\wages198.jpg",    (0.05, 0.05, 0.95, 0.72), 0),
    },
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
    "lauren-stevens-harris":(HEADSHOT_SRC / "lauren-stevens-harris.webp", 0.50, 0.42, 1.00),
}
# ---- LEAP photographs for the About band on the home page (_data/gallery.yml).
# stem -> (source file, crop box). Every crop is 3:2; the output is black and white.
GALLERY = {
    "graduation-2018":  ("Abel Gwaindepi graduates with Johan Fourie and Krige Siebrits.jpg",               (0.00, 0.12, 1.00, 0.62)),
    "biography-2019":   ("Biography first meeting 2019.jpg",                                                (0.00, 0.08, 1.00, 0.92)),
    "aehn-2017":        ("Bokang Mpeta thanks Trudi Makhaya at AEHN 2017.jpg",                              (0.00, 0.00, 1.00, 1.00)),
    "class-2017":       ("Classof2017.jpg",                                                                 (0.00, 0.10, 1.00, 0.99)),
    "fugitives-2021":   ("Fugitives art installation (httpswww.youtube.comwatchv=wKyt0xyT3Qo).jpg",          (0.08, 0.00, 0.92, 1.00)),
    "new-york-2018":    ("Johan Fourie presents a LEAP talk in New York.jpg",                               (0.00, 0.00, 1.00, 1.00)),
    "colloquium-2023":  ("Munashe Chideya at a LEAP Colloquium 2023.jpeg",                                  (0.00, 0.03, 1.00, 0.92)),
    "launch-2015":      ("The launch function of LEAP (2015).jpg",                                          (0.16, 0.00, 0.84, 1.00)),
    "early-lab-2017":   ("The very early LEAP lab (with Michiel de Haas and David Bijsterbosch).jpg",       (0.00, 0.00, 1.00, 1.00)),
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


def monochrome(im, grain=0.035):
    """Black and white with a little film grain, for LEAP's own photographs."""
    g = ImageOps.autocontrast(im.convert("L"), cutoff=0.5)
    if grain:
        g = Image.blend(g, ImageChops.overlay(g, Image.effect_noise(g.size, 40)), grain * 4)
    return g.convert("RGB")


def halftone(im, width=900, cell=7, ink="#120a0e", dot="#d4bf8a"):
    """A newspaper halftone: one gold dot per cell, its size set by the brightness beneath."""
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    g = g.resize((width, round(g.height * width / g.width)), Image.LANCZOS)
    k = 4                                                     # draw large, then shrink, for smooth dots
    out = Image.new("RGB", (g.width * k, g.height * k), hex2rgb(ink))
    d = ImageDraw.Draw(out)
    small = g.resize((g.width // cell + 1, g.height // cell + 1), Image.BOX)
    for y in range(small.height):
        for x in range(small.width):
            v = small.getpixel((x, y)) / 255
            r = cell * k * 0.64 * v ** 1.15
            if r > 0.4 * k:
                cx, cy = (x + 0.5) * cell * k, (y + 0.5) * cell * k
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=hex2rgb(dot))
    return out.resize(g.size, Image.LANCZOS)


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
    if want("hero"):
        (OUT / "hero").mkdir(parents=True, exist_ok=True)
        for tone, items in HERO.items():
            for stem, (src, box, rot) in items.items():
                im = duotone(load(src, box, rot), tone)
                im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
                im.save(OUT / "hero" / f"{stem}.webp", quality=78, method=6)
                print("hero", stem)
    if want("projects"):
        for stem, (src, tone, box, rot) in PROJECTS.items():
            export(duotone(load(SRC / src, box, rot), tone, vignette=0.25), stem, OUT / "projects", widths=(1400, 700))
            print("project", stem)
    if want("faces"):
        for key, (src, cx, cy, s) in TEAM.items():
            headshot(src, cx, cy, s, OUT / "team" / f"{key}.jpg"); print("team", key)
        for key, (src, cx, cy, s) in BOARD.items():
            headshot(src, cx, cy, s, OUT / "board" / f"{key}.jpg"); print("board", key)
    if want("quotes"):
        for stem, (src, box) in QUOTES.items():
            export(duotone(load(ELLIOTT / src, box), "maroon", vignette=0.2), stem, OUT / "archive")
            print("quote", stem)
    if want("lectures"):
        # Stills from LEAP's own lecture videos (YouTube thumbnails, 1280x720), toned like the archive
        src_dir, out = ROOT / "_sources" / "lectures", OUT / "lectures"
        out.mkdir(parents=True, exist_ok=True)
        for f in sorted(src_dir.glob("*.jpg")):
            im = duotone(load(f), "maroon", grain=0.03, vignette=0.2).resize((960, 540), Image.LANCZOS)
            im.save(out / f"{f.stem}.webp", quality=80, method=6)
            print("lecture", f.stem)
    if want("terreblanche"):
        # Sampie Terreblanche, a portrait: see _sources/terreblanche/PROVENANCE.md
        im = load(ROOT / "_sources" / "terreblanche" / "sampie-terreblanche-portrait.jpg", (0.18, 0.00, 0.92, 1.00))
        halftone(im).save(OUT / "archive" / "terreblanche.webp", quality=82, method=6)
        print("terreblanche")
    if want("gallery"):
        (OUT / "gallery").mkdir(parents=True, exist_ok=True)
        for stem, (src, box) in GALLERY.items():
            im = monochrome(load(GALLERY_SRC / src, box).resize((1200, 800), Image.LANCZOS))
            for w in (1200, 700):
                r = im if w == 1200 else im.resize((w, round(w * 2 / 3)), Image.LANCZOS)
                r.save(OUT / "gallery" / f"{stem}-{w}.webp", quality=80, method=6)
            print("gallery", stem)
    if want("card"):
        social_card(); favicon_png(); print("card + favicon")
