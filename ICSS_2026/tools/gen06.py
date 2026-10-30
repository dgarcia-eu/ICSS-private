#!/usr/bin/env python3
"""Generate the diagrams of ICSS session 6 (Recursion) as SVG."""
import os

OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/06-Recursion/figures"
FONT = 'font-family="Arial, Helvetica, sans-serif"'
DEFS = '''  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#111"/></marker>
  </defs>
'''


def svg(w, h, body, defs=True):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" {FONT}>\n' + (DEFS if defs else "") + body + '</svg>\n')


def txt(x, y, t, fs=14, anchor="middle", fill="#111", weight="normal", style="normal"):
    return (f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{fill}" '
            f'font-weight="{weight}" font-style="{style}">{t}</text>\n')


def write(name, content):
    open(os.path.join(OUT, name), "w").write(content)
    print("  ", name)


# ===================================================== factorial execution tree
# Each state: (number of "*" nodes, label of deepest-left child, deepest-right,
#              result under the deepest node or None)
FSTATES = [
    (1, "fac(3)", None, None),
    (2, "fac(2)", None, None),
    (3, "fac(1)", None, None),
    (4, "1", "1", "1"),
    (3, "1", "2", "2"),
    (2, "2", "3", "6"),
    (1, "6", "4", "24"),
]
DX, DY = 46, 44


def factorial_tree(stars, left_label, right_override, result):
    """Root '*' top-right, chain of '*' going down-left, numbers hanging right.
    Every state uses the canvas of the largest tree (MAXSTARS), so the root stays at
    the same place and the tree grows in place from slide to slide."""
    MAXSTARS = max(st for st, *_ in FSTATES)
    w = DX * (MAXSTARS + 1) + 110
    h = DY * (MAXSTARS + 1) + 60
    x0, y0 = w - 70, 24
    body = ""
    pts = [(x0 - i * DX, y0 + i * DY) for i in range(stars)]
    # right children are n, n-1, ... counting down from 4
    rights = [str(4 - i) for i in range(stars)]
    if right_override is not None:
        rights[-1] = right_override
    for i, (x, y) in enumerate(pts):
        rx, ry = x + DX * 0.8, y + DY
        body += f'  <line x1="{x}" y1="{y+8}" x2="{rx-6}" y2="{ry-12}" stroke="#111" stroke-width="1.8"/>\n'
        body += txt(rx, ry, rights[i], 21)
        if i < stars - 1:
            nx, ny = pts[i + 1]
            body += (f'  <line x1="{x}" y1="{y+8}" x2="{nx+6}" y2="{ny-12}" stroke="#111" '
                     f'stroke-width="1.8"/>\n')
        else:
            lx, ly = x - DX * 0.8, y + DY
            body += (f'  <line x1="{x}" y1="{y+8}" x2="{lx+6}" y2="{ly-12}" stroke="#111" '
                     f'stroke-width="1.8"/>\n')
            body += txt(lx, ly, left_label, 21)
        body += txt(x, y + 9, "*", 30, weight="bold")
    if result is not None:
        lx, ly = pts[-1][0] - DX * 0.8, pts[-1][1] + DY
        body += txt(pts[-1][0], ly + 36, result, 22, weight="bold")
    return svg(w, h, body, defs=False)


for i, (stars, ll, ro, res) in enumerate(FSTATES, start=1):
    write(f"06-factorial-tree-{i}.svg", factorial_tree(stars, ll, ro, res))

# ============================================================ DFS trace figures
# directed graph:  c->b, c->f, c->g, b->e, e->a, e->f, g->d
GP = {"a": (36, 96), "b": (128, 56), "c": (222, 56), "d": (316, 56),
      "e": (128, 140), "f": (222, 140), "g": (316, 140)}
GE = [("c", "b"), ("c", "f"), ("c", "g"), ("b", "e"), ("e", "a"), ("e", "f"), ("g", "d")]
TOP = {"a", "b", "c", "d"}
NW, NH = 42, 30

# (times dict, parents dict, current node or None)
def st(times, parents, cur=None):
    t = {n: "/" for n in GP}
    t.update(times)
    p = {n: "NIL" for n in GP}
    p.update(parents)
    return (t, p, cur)


DSTATES = {
    "00": st({}, {}, None),
    "01": st({"c": "1/"}, {"b": "C"}, "c"),
    "02": st({"c": "1/", "b": "2/"}, {"b": "C", "e": "B"}, "b"),
    "03": st({"c": "1/", "b": "2/", "e": "3/"}, {"b": "C", "e": "B", "a": "E"}, "e"),
    "04": st({"c": "1/", "b": "2/", "e": "3/", "a": "4/"}, {"b": "C", "e": "B", "a": "E"}, "a"),
    "05": st({"c": "1/", "b": "2/", "e": "3/", "a": "4/5"}, {"b": "C", "e": "B", "a": "E"}, "a"),
    "06": st({"c": "1/", "b": "2/", "e": "3/", "a": "4/5"},
             {"b": "C", "e": "B", "a": "E", "f": "E"}, "e"),
    "07": st({"c": "1/", "b": "2/", "e": "3/", "a": "4/5", "f": "6/"},
             {"b": "C", "e": "B", "a": "E", "f": "E"}, "f"),
    "08": st({"c": "1/", "b": "2/", "e": "3/", "a": "4/5", "f": "6/7"},
             {"b": "C", "e": "B", "a": "E", "f": "E"}, "f"),
    "09": st({"c": "1/", "b": "2/", "e": "3/", "a": "4/5", "f": "6/7"},
             {"b": "C", "e": "B", "a": "E", "f": "E"}, "e"),
    "10": st({"c": "1/", "b": "2/", "e": "3/8", "a": "4/5", "f": "6/7"},
             {"b": "C", "e": "B", "a": "E", "f": "E"}, "e"),
    "11": st({"c": "1/", "b": "2/", "e": "3/8", "a": "4/5", "f": "6/7"},
             {"b": "C", "e": "B", "a": "E", "f": "E"}, "b"),
    "12": st({"c": "1/", "b": "2/9", "e": "3/8", "a": "4/5", "f": "6/7"},
             {"b": "C", "e": "B", "a": "E", "f": "E"}, "b"),
    "13": st({"c": "1/", "b": "2/9", "e": "3/8", "a": "4/5", "f": "6/7"},
             {"b": "C", "e": "B", "a": "E", "f": "E", "g": "C"}, "c"),
    "14": st({"c": "1/", "b": "2/9", "e": "3/8", "a": "4/5", "f": "6/7", "g": "10/"},
             {"b": "C", "e": "B", "a": "E", "f": "E", "g": "C", "d": "G"}, "g"),
    "15": st({"c": "1/", "b": "2/9", "e": "3/8", "a": "4/5", "f": "6/7", "g": "10/", "d": "11/"},
             {"b": "C", "e": "B", "a": "E", "f": "E", "g": "C", "d": "G"}, "d"),
    "16": st({"c": "1/", "b": "2/9", "e": "3/8", "a": "4/5", "f": "6/7", "g": "10/", "d": "11/12"},
             {"b": "C", "e": "B", "a": "E", "f": "E", "g": "C", "d": "G"}, "d"),
    "17": st({"c": "1/", "b": "2/9", "e": "3/8", "a": "4/5", "f": "6/7", "g": "10/", "d": "11/12"},
             {"b": "C", "e": "B", "a": "E", "f": "E", "g": "C", "d": "G"}, "g"),
    "18": st({"c": "1/", "b": "2/9", "e": "3/8", "a": "4/5", "f": "6/7", "g": "10/13", "d": "11/12"},
             {"b": "C", "e": "B", "a": "E", "f": "E", "g": "C", "d": "G"}, "g"),
    "19": st({"c": "1/", "b": "2/9", "e": "3/8", "a": "4/5", "f": "6/7", "g": "10/13", "d": "11/12"},
             {"b": "C", "e": "B", "a": "E", "f": "E", "g": "C", "d": "G"}, "c"),
    "20": st({"c": "1/14", "b": "2/9", "e": "3/8", "a": "4/5", "f": "6/7", "g": "10/13",
              "d": "11/12"},
             {"b": "C", "e": "B", "a": "E", "f": "E", "g": "C", "d": "G"}, "c"),
}


def clip(x1, y1, x2, y2, pad=2):
    """Shorten a segment so the arrow head stops at the node border."""
    import math
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    # approximate the box by its half-diagonal
    r1 = min(NW / 2 / (abs(dx) / L or 1e-6), NH / 2 / (abs(dy) / L or 1e-6))
    r2 = r1
    return (x1 + dx / L * (r1 + pad), y1 + dy / L * (r1 + pad),
            x2 - dx / L * (r2 + pad + 4), y2 - dy / L * (r2 + pad + 4))


for key, (times, parents, cur) in DSTATES.items():
    body = ""
    for a, b in GE:
        (x1, y1), (x2, y2) = GP[a], GP[b]
        cx1, cy1, cx2, cy2 = clip(x1, y1, x2, y2)
        body += (f'  <line x1="{cx1:.1f}" y1="{cy1:.1f}" x2="{cx2:.1f}" y2="{cy2:.1f}" '
                 f'stroke="#111" stroke-width="1.2" marker-end="url(#a)"/>\n')
    for n, (x, y) in GP.items():
        body += (f'  <rect x="{x-NW/2}" y="{y-NH/2}" width="{NW}" height="{NH}" rx="6" fill="#fff" '
                 f'stroke="#111" stroke-width="1.2"/>\n')
        body += txt(x, y + 5, times[n], 13)
        if n in TOP:
            body += txt(x, y - 24, n, 13, style="italic")
            body += txt(x, y - 40, parents[n], 12, fill="#8a8a8a", style="italic")
        else:
            body += txt(x, y + 32, n, 13, style="italic")
            body += txt(x, y + 48, parents[n], 12, fill="#8a8a8a", style="italic")
    if cur:
        x, y = GP[cur]
        body += (f'  <path d="M {x+34} {y-40} L {x+6} {y-NH/2-4}" stroke="#111" stroke-width="2.6" '
                 f'marker-end="url(#a)"/>\n')
    write(f"06-dfs-{key}.svg", svg(370, 200, body))

# ============================================================ factorial slots
body = ""
for i in range(4):
    x = 26 + i * 118
    body += (f'  <rect x="{x}" y="20" width="96" height="62" fill="#111"/>\n'
             f'  <rect x="{x+10}" y="30" width="76" height="42" fill="#8fe8d8"/>\n')
    body += txt(x + 48, 62, str(i + 1), 26, weight="bold", fill="#555")
write("06-factorial-slots.svg", svg(500, 100, body, defs=False))

body_c = body
for i, (c, sep) in enumerate([("4", "*"), ("3", "*"), ("2", "*"), ("1", "")]):
    x = 26 + i * 118
    body_c += txt(x + 48, 150, c, 24)
    if sep:
        body_c += txt(x + 108, 150, sep, 22)
write("06-factorial-slots-choices.svg", svg(500, 176, body_c, defs=False))

print("deck 6 figures written")

# ============================================================ process memory
LB2 = "#bcd6f0"
body = ""
body += f'  <rect x="120" y="10" width="150" height="52" fill="#e2dcc2" stroke="#111" stroke-width="1.2"/>\n'
body += txt(195, 32, "Program", 14) + txt(195, 50, "code  (CS)", 14)
body += f'  <rect x="120" y="62" width="150" height="60" fill="#fff" stroke="#111" stroke-width="1.2"/>\n'
body += f'  <rect x="120" y="122" width="150" height="60" fill="{LB2}" stroke="#cc2222" stroke-width="1.6"/>\n'
body += f'  <rect x="120" y="182" width="150" height="58" fill="{LB2}" stroke="#111" stroke-width="1.2"/>\n'
body += f'  <rect x="120" y="240" width="150" height="46" fill="#7fb1e8" stroke="#cc2222" stroke-width="1.6"/>\n'
body += txt(195, 262, "Stack (SP) +", 13) + txt(195, 279, "Variables", 13)
body += (f'  <line x1="195" y1="140" x2="195" y2="176" stroke="#111" stroke-width="2.4" '
         f'marker-end="url(#a)"/>\n')
body += (f'  <line x1="195" y1="176" x2="195" y2="140" stroke="#111" stroke-width="2.4" '
         f'marker-end="url(#a)"/>\n')
body += f'  <rect x="300" y="185" width="112" height="86" rx="10" fill="#fff" stroke="#111" stroke-width="1.2"/>\n'
for i, t in enumerate(["Heap", "Python", "Memory", "manager"]):
    body += txt(356, 206 + i * 18, t, 13)
body += f'  <rect x="316" y="42" width="96" height="60" rx="10" fill="#fff" stroke="#111" stroke-width="1.2"/>\n'
body += txt(364, 68, "System", 13) + txt(364, 86, "memory", 13)
body += (f'  <line x1="272" y1="252" x2="296" y2="238" stroke="#111" stroke-width="1.6" '
         f'marker-end="url(#a)"/>\n')
body += (f'  <line x1="352" y1="182" x2="366" y2="108" stroke="#111" stroke-width="1.6" '
         f'marker-end="url(#a)"/>\n')
body += txt(195, 306, "Memory of", 13) + txt(195, 322, "process", 13)
body += txt(356, 306, "Memory of", 13) + txt(356, 322, "system", 13)
write("06-process-memory.svg", svg(430, 334, body))

# ============================================================ gcd bar figure
def stack(x, y0, n, unit, stroke, groups):
    s = ""
    for i in range(n):
        s += (f'  <rect x="{x}" y="{y0 - (i+1)*unit}" width="62" height="{unit}" fill="#cceef9" '
              f'stroke="#9a9a9a" stroke-width="0.8"/>\n')
    # group frames
    k = 0
    while k < n:
        h = min(groups, n - k)
        s += (f'  <rect x="{x}" y="{y0 - (k+h)*unit}" width="62" height="{h*unit}" fill="none" '
              f'stroke="{stroke}" stroke-width="2"/>\n')
        k += h
    return s

body = ""
BASE, U = 250, 26
cols = [(20, 8, 1, "#9a9a9a", "8/1=8"), (110, 6, 1, "#9a9a9a", "6/1=6"),
        (215, 8, 2, "#111", "8/2=4"), (305, 6, 2, "#111", "6/2=3"),
        (410, 8, 3, "#cc2222", "8/3=2.66…"), (500, 6, 3, "#cc2222", "6/3=2")]
for x, n, g, col, lab in cols:
    body += stack(x, BASE, n, U, col, g)
    body += txt(x + 31, BASE + 22, lab, 13)
write("06-gcd.svg", svg(590, 280, body, defs=False))
print("extra figures written")
