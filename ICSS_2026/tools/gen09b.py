#!/usr/bin/env python3
"""Figures for Exercise09: Sipser's TM M2 and the CLIQUE example graph."""
import math
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "TheoryExercises", "figures")
FILL = "#eeeeee"
BLUE = "#00a9e0"


def write(name, body, w, h):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" font-family="Arial, Helvetica, sans-serif">\n'
            '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-end">'
            '<path d="M0,0 L10,5 L0,10 z" fill="#222"/></marker></defs>\n'
            + body + "\n</svg>\n"
        )
    print(path)


# ---------------------------------------------------------------- TM M2
R = 30
S = {
    "q1": (110, 275),
    "q2": (480, 275),
    "q3": (875, 275),
    "q4": (875, 500),
    "q5": (680, 120),
    "qacc": (480, 505),
    "qrej": (110, 505),
}


def edge(p, q, rp=R, rq=R):
    """Straight segment between two circles, trimmed by their radii."""
    (x1, y1), (x2, y2) = S[p], S[q]
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    return (x1 + ux * rp, y1 + uy * rp, x2 - ux * rq, y2 - uy * rq)


b = []
# nodes
for k, (x, y) in S.items():
    if k in ("qacc", "qrej"):
        b.append(f'<ellipse cx="{x}" cy="{y}" rx="72" ry="30" fill="{FILL}" stroke="#222" stroke-width="2"/>')
        lab = "accept" if k == "qacc" else "reject"
        b.append(f'<text x="{x}" y="{y+8}" text-anchor="middle" font-size="26" '
                 f'font-style="italic">q<tspan font-size="18" dy="6">{lab}</tspan></text>')
    else:
        b.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{FILL}" stroke="#222" stroke-width="2"/>')
        b.append(f'<text x="{x}" y="{y+9}" text-anchor="middle" font-size="26" '
                 f'font-style="italic">q<tspan font-size="18" dy="6">{k[1]}</tspan></text>')

# start arrow
b.append(f'<path d="M110,205 L110,240" stroke="#222" stroke-width="2" fill="none" marker-end="url(#a)"/>')


def arrow(p, q, rq=R):
    x1, y1, x2, y2 = edge(p, q, R, rq)
    b.append(f'<path d="M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}" stroke="#222" '
             f'stroke-width="2" fill="none" marker-end="url(#a)"/>')


def lab(x, y, *lines, anchor="middle", size=19):
    for i, t in enumerate(lines):
        b.append(f'<text x="{x}" y="{y + i*22}" text-anchor="{anchor}" font-size="{size}">{t}</text>')


AR = "&#8594;"   # →
BL = "&#9251;"   # ␣

# q1 -> q2
arrow("q1", "q2")
lab(295, 318, f"0{AR}{BL},R")
# q1 -> qreject
x1, y1, x2, y2 = edge("q1", "qrej", R, 30)
b.append(f'<path d="M110,305 L110,475" stroke="#222" stroke-width="2" fill="none" marker-end="url(#a)"/>')
lab(60, 385, f"{BL}{AR}R", f"x{AR}R", anchor="end")
# q2 -> qaccept
b.append(f'<path d="M480,305 L480,475" stroke="#222" stroke-width="2" fill="none" marker-end="url(#a)"/>')
lab(492, 400, f"{BL}{AR}R", anchor="start")
# q2 -> q3
arrow("q2", "q3")
lab(680, 318, f"0{AR}x,R")
# q2 self loop
b.append('<path d="M462,247 C440,190 520,190 498,247" stroke="#222" stroke-width="2" '
         'fill="none" marker-end="url(#a)"/>')
lab(430, 188, f"x{AR}R", anchor="end")
# q3 self loop
b.append('<path d="M893,249 C950,215 950,300 893,301" stroke="#222" stroke-width="2" '
         'fill="none" marker-end="url(#a)"/>')
lab(950, 245, f"x{AR}R", anchor="start")
# q3 <-> q4 (two curved arcs)
b.append('<path d="M857,304 C820,360 820,415 857,471" stroke="#222" stroke-width="2" '
         'fill="none" marker-end="url(#a)"/>')
lab(805, 395, f"0{AR}R", anchor="end")
b.append('<path d="M896,471 C935,415 935,360 896,304" stroke="#222" stroke-width="2" '
         'fill="none" marker-end="url(#a)"/>')
lab(948, 395, f"0{AR}x,R", anchor="start")
# q4 self loop
b.append('<path d="M903,485 C960,455 968,535 903,518" stroke="#222" stroke-width="2" '
         'fill="none" marker-end="url(#a)"/>')
lab(968, 480, f"x{AR}R", anchor="start")
# q4 -> qreject (big bottom curve)
b.append('<path d="M862,529 C700,650 300,650 150,533" stroke="#222" stroke-width="2" '
         'fill="none" marker-end="url(#a)"/>')
lab(500, 632, f"{BL}{AR}R")
# q3 -> q5
arrow("q3", "q5")
lab(815, 185, f"{BL}{AR}L", anchor="start")
# q5 -> q2
arrow("q5", "q2")
lab(548, 178, f"{BL}{AR}R", anchor="end")
# q5 self loop
b.append('<path d="M663,92 C640,35 720,35 697,92" stroke="#222" stroke-width="2" '
         'fill="none" marker-end="url(#a)"/>')
lab(632, 32, f"0{AR}L", f"x{AR}L", anchor="end")

write("ex09-turing-machine.svg", "\n".join(b), 1060, 680)

# ---------------------------------------------------------------- CLIQUE graph
V = {
    "A": (75, 60),
    "B": (555, 50),
    "C": (1040, 50),
    "D": (320, 315),
    "E": (75, 585),
    "F": (555, 585),
    "G": (1040, 585),
}
THIN = [("A", "B"), ("A", "D"), ("A", "E"), ("E", "D"), ("E", "F")]
CLQ = ["B", "C", "D", "F", "G"]
THICK = [(CLQ[i], CLQ[j]) for i in range(5) for j in range(i + 1, 5)]

g = []
for u, v in THIN:
    (x1, y1), (x2, y2) = V[u], V[v]
    g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="2"/>')
for u, v in THICK:
    (x1, y1), (x2, y2) = V[u], V[v]
    g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="7"/>')
for k, (x, y) in V.items():
    g.append(f'<circle cx="{x}" cy="{y}" r="36" fill="{FILL}" stroke="#111" stroke-width="4"/>')
    g.append(f'<text x="{x}" y="{y+8}" text-anchor="middle" font-size="24">{k}</text>')

write("ex09-clique.svg", "\n".join(g), 1115, 645)
