#!/usr/bin/env python3
"""Figures for the ICSS 2026 exam question pool.

Also prints the worked answer for the Schelling grid item (which agents are
unsatisfied at a given F), so the pool's solution cannot disagree with its
own figure.
"""
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "Exams", "figures")
os.makedirs(OUT, exist_ok=True)

SEEBLAU = "#00a9e0"
FILL = "#eeeeee"


def write(name, body, w, h):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" font-family="Arial, Helvetica, sans-serif">\n'
            '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-end">'
            '<path d="M0,0 L10,5 L0,10 z" fill="#111"/></marker></defs>\n'
            + body + "\n</svg>\n"
        )
    print(path)


# ------------------------------------------------------------------ min-heap
HEAP = [2, 4, 14, 10, 8, 15, 18, 17, 11, 16]


def heap_svg(name, arr, title=None):
    n = len(arr)
    levels = []
    i, lvl = 0, 0
    while i < n:
        levels.append(list(range(i, min(i + 2 ** lvl, n))))
        i += 2 ** lvl
        lvl += 1
    W, H = 900, 60 + 100 * len(levels)
    bw, bh = 54, 40
    pos = {}
    for li, row in enumerate(levels):
        span = 2 ** li
        for k, idx in enumerate(row):
            x = W * (k + 0.5) / span
            y = 40 + 100 * li
            pos[idx] = (x, y)
    b = []
    for idx in range(n):
        p = (idx - 1) // 2
        if p >= 0:
            x1, y1 = pos[p]
            x2, y2 = pos[idx]
            b.append(f'<line x1="{x1:.0f}" y1="{y1+bh/2:.0f}" x2="{x2:.0f}" '
                     f'y2="{y2-bh/2:.0f}" stroke="#111" stroke-width="2"/>')
    for idx, v in enumerate(arr):
        x, y = pos[idx]
        b.append(f'<rect x="{x-bw/2:.0f}" y="{y-bh/2:.0f}" width="{bw}" height="{bh}" '
                 f'fill="#fff" stroke="#111" stroke-width="2"/>')
        b.append(f'<text x="{x:.0f}" y="{y+7:.0f}" text-anchor="middle" '
                 f'font-size="21">{v}</text>')
    write(name, "\n".join(b), W, H)


heap_svg("ex-min-heap.svg", HEAP)
# result of extract-min on HEAP
H2 = HEAP.copy()
H2[0] = H2.pop()                    # move the last element into the root
# sift down (0-based)
i = 0
while True:
    m = i
    for c in (2 * i + 1, 2 * i + 2):
        if c < len(H2) and H2[c] < H2[m]:
            m = c
    if m == i:
        break
    H2[i], H2[m] = H2[m], H2[i]
    i = m
heap_svg("ex-min-heap-after.svg", H2)
print("min-heap after extract-min:", H2)

# ------------------------------------------------------------- Dijkstra graph
NODES = {"a": (90, 330), "b": (390, 90), "c": (760, 90),
         "d": (390, 560), "e": (760, 560)}
R = 34
# (from, to, weight, perpendicular bow, label offset along the bow)
EDGES = [("a", "b", 10, 0, 26), ("a", "d", 5, 0, 26), ("b", "c", 1, 0, -26),
         ("b", "d", 2, -34, -22), ("d", "b", 3, -34, -22),
         ("d", "c", 9, 0, -28), ("d", "e", 2, 0, -26),
         ("c", "e", 6, -34, -22), ("e", "c", 4, -34, -22)]
b = []
for u, v, w, bow, loff in EDGES:
    x1, y1 = NODES[u]
    x2, y2 = NODES[v]
    dx, dy = x2 - x1, y2 - y1
    d = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / d, dy / d
    px, py = -uy, ux                      # unit perpendicular, left of travel
    sx, sy = x1 + ux * R + px * bow * 0.35, y1 + uy * R + py * bow * 0.35
    ex, ey = x2 - ux * R + px * bow * 0.35, y2 - uy * R + py * bow * 0.35
    mx, my = (sx + ex) / 2 + px * bow, (sy + ey) / 2 + py * bow
    b.append(f'<path d="M{sx:.0f},{sy:.0f} Q{mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}" '
             f'fill="none" stroke="#111" stroke-width="2" marker-end="url(#a)"/>')
    lx = (sx + ex) / 2 + px * (bow * 0.6 + loff)
    ly = (sy + ey) / 2 + py * (bow * 0.6 + loff)
    b.append(f'<text x="{lx:.0f}" y="{ly+8:.0f}" text-anchor="middle" '
             f'font-size="24">{w}</text>')
# e -> a : a wide arc under the graph, drawn by hand so it clears d
b.append('<path d="M735,590 C560,690 200,660 100,366" fill="none" stroke="#111" '
         'stroke-width="2" marker-end="url(#a)"/>')
b.append('<text x="330" y="675" text-anchor="middle" font-size="24">7</text>')
for k, (x, y) in NODES.items():
    b.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{FILL}" stroke="#111" stroke-width="3"/>')
    b.append(f'<text x="{x}" y="{y+10}" text-anchor="middle" font-size="28">{k}</text>')
write("ex-dijkstra-graph.svg", "\n".join(b), 880, 700)

# ------------------------------------------------------------- Schelling grid
# B = black agent, W = white agent, '.' = empty cell
GRID = [
    ".B.BWB",
    "BBBW.W",
    ".BW..B",
    ".WBWBW",
    "WWWBWW",
    "B.BBB.",
]
CELL = 70
b, unsat = [], []


def neighbours(r, c):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == dc == 0:
                continue
            rr, cc = r + dr, c + dc
            if 0 <= rr < 6 and 0 <= cc < 6:
                yield GRID[rr][cc]


F = 0.35
for r in range(6):
    for c in range(6):
        v = GRID[r][c]
        if v == ".":
            continue
        occ = [n for n in neighbours(r, c) if n != "."]
        same = sum(1 for n in occ if n == v)
        f = same / len(occ) if occ else 1.0
        if f < F:
            unsat.append((r + 1, c + 1, v, same, len(occ), round(f, 3)))

for r in range(6):
    for c in range(6):
        x, y = 10 + c * CELL, 10 + r * CELL
        b.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                 f'fill="#fff" stroke="#111" stroke-width="2"/>')
        v = GRID[r][c]
        if v == ".":
            continue
        cx, cy = x + CELL / 2, y + CELL / 2
        fillc = "#111" if v == "B" else "#fff"
        b.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="20" fill="{fillc}" '
                 f'stroke="#111" stroke-width="2.5"/>')
        b.append(f'<text x="{x+7}" y="{y+18}" font-size="13" fill="#999">'
                 f'{r+1},{c+1}</text>')
write("ex-schelling-grid.svg", "\n".join(b), 20 + 6 * CELL, 20 + 6 * CELL)

print(f"\nSchelling: unsatisfied agents at F = {F}")
print("  (row, col, kind, same, occupied neighbours, f)")
for u in unsat:
    print("   ", u)
