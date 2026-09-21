"""
Draws the two hand-made LEAP motifs as SVG files. Run once locally
(python tools/make-motifs.py); the outputs in assets/img/ are committed.

  motif-contour.svg  L: a contour map with two blue watercourses (Data, Contact)
  motif-weave.svg    P: a tile of concentric squares and diagonal line bundles (Team)

The E and A motifs are treated archival photographs: see treat-images.py.
Requires numpy and contourpy (both ship with matplotlib).
"""
from pathlib import Path
import numpy as np
from contourpy import contour_generator

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"
SAGE, BLUE = "#6B8E5E", "#3D8EB9"
PLUM, GOLD, MINT, ROSE = "#8a4a72", "#a78e53", "#97C5B0", "#c98aa6"


def contour_svg(W=1600, H=1000, seed=1834):
    rng = np.random.default_rng(seed)
    nx, ny = 320, 200
    x, y = np.meshgrid(np.linspace(0, W, nx), np.linspace(0, H, ny))
    z = np.zeros_like(x)
    for _ in range(9):                                   # hills
        cx, cy = rng.uniform(0, W), rng.uniform(0, H)
        sx, sy = rng.uniform(160, 420), rng.uniform(140, 360)
        th = rng.uniform(0, np.pi)
        xr = (x - cx) * np.cos(th) + (y - cy) * np.sin(th)
        yr = -(x - cx) * np.sin(th) + (y - cy) * np.cos(th)
        z += rng.uniform(0.5, 1.2) * np.exp(-(xr / sx) ** 2 - (yr / sy) ** 2)
    for k in range(1, 5):                                # gentle irregularity
        z += 0.05 / k * np.sin(x / (170 / k) + rng.uniform(0, 6)) * np.cos(y / (150 / k) + rng.uniform(0, 6))

    def path(pts, step=2):
        pts = pts[::step] if len(pts) > 3 * step else pts
        d = f"M{pts[0][0]:.0f} {pts[0][1]:.0f}"
        for i in range(1, len(pts) - 1):                 # quadratic smoothing through midpoints
            mx, my = (pts[i] + pts[i + 1]) / 2
            d += f"Q{pts[i][0]:.0f} {pts[i][1]:.0f} {mx:.0f} {my:.0f}"
        return d

    gen = contour_generator(x=x, y=y, z=z)
    levels = np.linspace(z.min() + 0.05, z.max() - 0.03, 22)
    thin, index = [], []
    for i, lv in enumerate(levels):
        for line in gen.lines(lv):
            if len(line) > 8:
                (index if i % 5 == 0 else thin).append(path(line))

    # Watercourses: steepest descent from high ground to the sheet edge.
    gy, gx = np.gradient(z, H / (ny - 1), W / (nx - 1))
    rivers = []
    for sx_, sy_ in ((0.30 * W, 0.35 * H), (0.72 * W, 0.62 * H)):
        p, pts = np.array([sx_, sy_]), []
        for _ in range(900):
            i = int(np.clip(p[1] / H * (ny - 1), 0, ny - 1)); j = int(np.clip(p[0] / W * (nx - 1), 0, nx - 1))
            g = np.array([gx[i, j], gy[i, j]])
            n = np.linalg.norm(g)
            if n < 1e-7:
                break
            p = p - 4.0 * g / n
            pts.append(p.copy())
            if not (0 < p[0] < W and 0 < p[1] < H):
                break
        if len(pts) > 20:
            rivers.append(path(np.array(pts), step=6))

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" fill="none" stroke-linecap="round">',
           f'<g stroke="{SAGE}" stroke-width="1">', *[f'<path d="{d}"/>' for d in thin], '</g>',
           f'<g stroke="{SAGE}" stroke-width="2">', *[f'<path d="{d}"/>' for d in index], '</g>',
           f'<g stroke="{BLUE}" stroke-width="2.4">', *[f'<path d="{d}"/>' for d in rivers], '</g>', '</svg>']
    (OUT / "motif-contour.svg").write_text("".join(svg), encoding="utf-8")
    print("contour", len(thin) + len(index), "lines,", len(rivers), "rivers,", (OUT / "motif-contour.svg").stat().st_size // 1024, "KB")


def weave_svg(T=240):
    c = T / 2
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{T}" height="{T}" viewBox="0 0 {T} {T}" fill="none" stroke-width="1.5">']
    # concentric squares, centre of the tile
    for i, col in enumerate((GOLD, PLUM, ROSE, PLUM, MINT, PLUM)):
        r = 14 + i * 11
        parts.append(f'<rect x="{c - r}" y="{c - r}" width="{2 * r}" height="{2 * r}" stroke="{col}"/>')
    parts.append(f'<rect x="{c - 4}" y="{c - 4}" width="8" height="8" fill="{GOLD}"/>')
    # diagonal bundles across each corner: they meet their neighbours to form diamonds when tiled
    for k, col in zip(range(5), (PLUM, ROSE, GOLD, MINT, PLUM)):
        o = 18 + k * 9
        parts.append(f'<path stroke="{col}" d="M0 {o}L{o} 0M{T - o} 0L{T} {o}M0 {T - o}L{o} {T}M{T - o} {T}L{T} {T - o}"/>')
    parts.append('</svg>')
    (OUT / "motif-weave.svg").write_text("".join(parts), encoding="utf-8")
    print("weave ok")


if __name__ == "__main__":
    contour_svg()
    weave_svg()
