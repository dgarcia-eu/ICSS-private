#!/usr/bin/env python3
"""Generate the diagrams of ICSS session 5 (Algorithms) as SVG."""
import os

OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/05-Algorithms/figures"
FONT = 'font-family="Arial, Helvetica, sans-serif"'
DEFS = '''  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#111"/></marker>
    <marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#4a4a4a"/></marker>
    <marker id="agS" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.2" markerHeight="3.2"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#4a4a4a"/></marker>
  </defs>
'''


def svg(w, h, body, defs=True):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" {FONT}>\n' + (DEFS if defs else "") + body + '</svg>\n')


def txt(x, y, t, fs=13, anchor="middle", fill="#111", weight="normal", style="normal"):
    return (f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{fill}" '
            f'font-weight="{weight}" font-style="{style}">{t}</text>\n')


def write(name, content):
    open(os.path.join(OUT, name), "w").write(content)
    print("  ", name)


# ============================================================ flowchart symbols
GREEN, TAN, GREY, RED = "#3fd28a", "#b3a07a", "#c8c8c8", "#f0645f"


def terminal(cx, cy, w, h, label, fs=12):
    return (f'  <rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{h/2}" '
            f'fill="{GREEN}" stroke="#111" stroke-width="1.1"/>\n'
            + txt(cx, cy + 4, label, fs, weight="bold"))


def parallelo(cx, cy, w, h, label, fs=11, dy=0):
    sk = 12
    return (f'  <polygon points="{cx-w/2+sk},{cy-h/2} {cx+w/2},{cy-h/2} {cx+w/2-sk},{cy+h/2} '
            f'{cx-w/2},{cy+h/2}" fill="{TAN}" stroke="#111" stroke-width="1.1"/>\n'
            + label_lines(cx, cy, label, fs))


def rectbox(cx, cy, w, h, label, fs=11, fill=GREY):
    return (f'  <rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" fill="{fill}" '
            f'stroke="#111" stroke-width="1.1"/>\n' + label_lines(cx, cy, label, fs))


def diamond(cx, cy, w, h, label, fs=11):
    return (f'  <polygon points="{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}" '
            f'fill="{RED}" stroke="#111" stroke-width="1.1"/>\n' + label_lines(cx, cy, label, fs))


def label_lines(cx, cy, label, fs):
    lines = label.split("|")
    y0 = cy + 4 - (len(lines) - 1) * fs * 0.6
    return "".join(txt(cx, y0 + i * fs * 1.2, l, fs, weight="bold") for i, l in enumerate(lines))


def arrow(x1, y1, x2, y2, color="#111"):
    return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.4" '
            f'marker-end="url(#a)"/>\n')


body = ""
body += terminal(80, 22, 116, 26, "start/stop")
body += parallelo(80, 86, 128, 34, "input &amp;|output")
body += rectbox(80, 152, 122, 30, "operation")
body += diamond(80, 226, 116, 44, "split")
body += arrow(138, 226, 176, 226)
body += txt(180, 220, "no", 11, anchor="start")
body += arrow(80, 248, 80, 282)
body += txt(70, 272, "yes", 11, anchor="end")
write("05-flowchart-symbols.svg", svg(210, 292, body))

# ============================================================ profit flowchart
body = ""
body += terminal(110, 20, 78, 24, "start", 12)
body += parallelo(110, 74, 176, 38, "Read Selling Price|(SP)", 11)
body += parallelo(110, 140, 176, 38, "Read Cost Price|(CP)", 11)
body += diamond(110, 208, 172, 48, "SP &gt;= CP", 12)
body += rectbox(340, 208, 168, 32, "Profit = SP - CP", 12)
body += rectbox(110, 278, 168, 32, "Loss = CP - SP", 12)
body += parallelo(110, 344, 176, 36, "Output Loss", 12)
body += parallelo(340, 344, 176, 36, "Output Profit", 12)
body += terminal(110, 404, 78, 24, "stop", 12)
body += arrow(110, 32, 110, 53)
body += arrow(110, 93, 110, 119)
body += arrow(110, 159, 110, 182)
body += arrow(196, 208, 254, 208)
body += txt(226, 200, "&#10004;", 15, fill="#2e8b3a")
body += arrow(110, 232, 110, 260)
body += txt(122, 250, "&#10008;", 14, fill="#cc2222", anchor="start")
body += arrow(110, 294, 110, 324)
body += arrow(340, 224, 340, 324)
body += arrow(110, 362, 110, 390)
body += (f'  <path d="M 340 362 L 340 404 L 152 404" fill="none" stroke="#111" stroke-width="1.4" '
         f'marker-end="url(#a)"/>\n')
write("05-flowchart-profit.svg", svg(440, 424, body))

# ==================================================================== queue
LB = "#cceef9"


def cells(x, y, n, w, h):
    s = ""
    for i in range(n):
        s += (f'  <rect x="{x}" y="{y+i*h}" width="{w}" height="{h}" fill="{LB}" stroke="#8a8a8a" '
              f'stroke-width="1"/>\n')
    return s


body = ""
body += cells(96, 60, 6, 140, 38)
body += (f'  <rect x="8" y="16" width="120" height="34" fill="{LB}" stroke="#8a8a8a" stroke-width="1"/>\n')
body += txt(68, 10, "Enqueue", 14)
body += (f'  <path d="M 128 33 L 150 33 Q 162 33 162 45 L 162 54" fill="none" stroke="#4a4a4a" '
         f'stroke-width="4" marker-end="url(#agS)"/>\n')
body += txt(90, 78, "Rear &#10132;", 14, anchor="end")
body += txt(90, 282, "Front &#10132;", 14, anchor="end")
body += (f'  <rect x="214" y="278" width="120" height="34" fill="{LB}" stroke="#8a8a8a" stroke-width="1"/>\n')
body += txt(274, 268, "Dequeue", 14)
body += (f'  <path d="M 178 268 L 178 292 Q 178 296 190 296 L 208 296" fill="none" stroke="#4a4a4a" '
         f'stroke-width="4" marker-end="url(#agS)"/>\n')
write("05-queue.svg", svg(344, 322, body))

# ==================================================================== stack
body = ""
body += cells(96, 74, 6, 140, 38)
body += (f'  <rect x="8" y="24" width="120" height="34" fill="{LB}" stroke="#8a8a8a" stroke-width="1"/>\n')
body += txt(68, 16, "Push item", 14)
body += (f'  <rect x="222" y="24" width="120" height="34" fill="{LB}" stroke="#8a8a8a" stroke-width="1"/>\n')
body += txt(282, 16, "Pop item", 14)
body += (f'  <path d="M 128 41 L 148 41 Q 160 41 160 53 L 160 68" fill="none" stroke="#4a4a4a" '
         f'stroke-width="4" marker-end="url(#agS)"/>\n')
body += (f'  <path d="M 186 68 L 186 53 Q 186 41 198 41 L 216 41" fill="none" stroke="#4a4a4a" '
         f'stroke-width="4" marker-end="url(#agS)"/>\n')
body += txt(90, 92, "Top &#10132;", 14, anchor="end")
write("05-stack.svg", svg(350, 312, body))

# ============================================================ v1..v8 graph
VP = {"v1": (46, 78), "v2": (140, 44), "v3": (222, 52), "v4": (330, 40),
      "v5": (44, 148), "v6": (186, 110), "v7": (254, 122), "v8": (334, 152)}
VE = [("v1", "v2"), ("v3", "v4"), ("v3", "v5"), ("v4", "v6"), ("v4", "v7"),
      ("v5", "v6"), ("v5", "v8"), ("v6", "v7"), ("v7", "v8")]
body = ""
for a, b in VE:
    (x1, y1), (x2, y2) = VP[a], VP[b]
    body += f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="1"/>\n'
for k, (x, y) in VP.items():
    body += (f'  <circle cx="{x}" cy="{y}" r="18" fill="#b8b8b8" stroke="#111" stroke-width="1.1"/>\n')
    body += (f'  <text x="{x-1}" y="{y+4}" text-anchor="middle" font-size="16">v<tspan font-size="14" '
             f'dy="4">{k[1]}</tspan></text>\n')
write("05-graph-v1v8.svg", svg(380, 196, body, defs=False))

# ============================================================ BFS trace figures
# wide canvas so the figure fills its column; node fill follows the BFS colors
# (WHITE not seen yet, GRAY seen and waiting in the queue, BLACK processed)
GP = {"a": (40, 112), "b": (148, 74), "c": (256, 74), "d": (364, 74),
      "e": (148, 154), "f": (256, 154), "g": (364, 154)}
GE = [("a", "e"), ("e", "b"), ("b", "c"), ("c", "f"), ("c", "g"), ("d", "g"), ("e", "f")]
TOP = {"a", "b", "c", "d"}
INF = "&#8734;"
BW, BH = 400, 300

# state = (dict node -> (distance, parent), current node or None, queue list)
STATES = {
    "init": ({n: (INF, "NIL") for n in GP} | {"c": ("0", "NIL")}, None, None),
    "q0":   ({n: (INF, "NIL") for n in GP} | {"c": ("0", "NIL")}, None, [("c", "0")]),
    "c":    ({"a": (INF, "NIL"), "b": ("1", "C"), "c": ("0", "NIL"), "d": (INF, "NIL"),
              "e": (INF, "NIL"), "f": ("1", "C"), "g": ("1", "C")}, "c",
             [("c", "0", True), ("b", "1"), ("f", "1"), ("g", "1")]),
    "b":    ({"a": (INF, "NIL"), "b": ("1", "C"), "c": ("0", "NIL"), "d": (INF, "NIL"),
              "e": ("2", "B"), "f": ("1", "C"), "g": ("1", "C")}, "b",
             [("b", "1", True), ("f", "1"), ("g", "1"), ("e", "2")]),
    "f":    ({"a": (INF, "NIL"), "b": ("1", "C"), "c": ("0", "NIL"), "d": (INF, "NIL"),
              "e": ("2", "B"), "f": ("1", "C"), "g": ("1", "C")}, "f",
             [("f", "1", True), ("g", "1"), ("e", "2")]),
    "g":    ({"a": (INF, "NIL"), "b": ("1", "C"), "c": ("0", "NIL"), "d": ("2", "G"),
              "e": ("2", "B"), "f": ("1", "C"), "g": ("1", "C")}, "g",
             [("g", "1", True), ("e", "2"), ("d", "2")]),
    "e":    ({"a": ("3", "E"), "b": ("1", "C"), "c": ("0", "NIL"), "d": ("2", "G"),
              "e": ("2", "B"), "f": ("1", "C"), "g": ("1", "C")}, "e",
             [("e", "2", True), ("d", "2"), ("a", "3")]),
    "e2":   ({"a": ("3", "E"), "b": ("1", "C"), "c": ("0", "NIL"), "d": ("2", "G"),
              "e": ("2", "B"), "f": ("1", "C"), "g": ("1", "C")}, None,
             [("d", "2"), ("a", "3")]),
    "d":    ({"a": ("3", "E"), "b": ("1", "C"), "c": ("0", "NIL"), "d": ("2", "G"),
              "e": ("2", "B"), "f": ("1", "C"), "g": ("1", "C")}, "d", [("a", "3")]),
    "done": ({"a": ("3", "E"), "b": ("1", "C"), "c": ("0", "NIL"), "d": ("2", "G"),
              "e": ("2", "B"), "f": ("1", "C"), "g": ("1", "C")}, None, []),
}
# the processed (BLACK) nodes after each step, in the order BFS dequeues them
# (on the "e" slide the line color[u] <- BLACK is not shaded yet, so e is still GRAY)
ORDER = ["c", "b", "f", "g", "e", "d", "a"]
DONE = {"init": 0, "q0": 0, "c": 1, "b": 2, "f": 3, "g": 4, "e": 4, "e2": 5, "d": 6, "done": 7}

for key, (vals, cur, queue) in STATES.items():
    black = set(ORDER[:DONE[key]])
    body = ""
    for a, b in GE:
        (x1, y1), (x2, y2) = GP[a], GP[b]
        body += f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="1.4"/>\n'
    for n, (x, y) in GP.items():
        d, par = vals[n]
        if n in black:
            fill, tc = "#222", "#fff"
        elif d != INF:
            fill, tc = "#b8b8b8", "#111"
        else:
            fill, tc = "#fff", "#111"
        if n == cur:
            body += (f'  <circle cx="{x}" cy="{y}" r="28" fill="none" stroke="#e07b00" '
                     f'stroke-width="5"/>\n')
        body += (f'  <circle cx="{x}" cy="{y}" r="22" fill="{fill}" stroke="#111" stroke-width="1.4"/>\n')
        body += txt(x, y + 7, d, 20, fill=tc, weight="bold")
        if n in TOP:
            body += txt(x, y - 32, n, 18, style="italic")
            body += txt(x, y - 52, par, 15, fill="#8a8a8a", style="italic")
        else:
            body += txt(x, y + 46, n, 18, style="italic")
            body += txt(x, y + 66, par, 15, fill="#8a8a8a", style="italic")
    if queue is not None:
        qy = 238
        body += txt(6, qy + 26, "Q:", 22, anchor="start", weight="bold", style="italic")
        x = 50
        if not queue:
            body += txt(60, qy + 28, "&#8709;", 26, anchor="start")
        for item in queue:
            n, d = item[0], item[1]
            crossed = len(item) > 2
            body += (f'  <rect x="{x}" y="{qy}" width="50" height="38" fill="#fff" stroke="#111" '
                     f'stroke-width="1.4"/>\n')
            body += txt(x + 25, qy + 26, n, 21)
            body += txt(x + 25, qy + 58, d, 17)
            if crossed:
                body += (f'  <line x1="{x+3}" y1="{qy+3}" x2="{x+47}" y2="{qy+35}" stroke="#cc2222" '
                         f'stroke-width="2"/>\n')
                body += (f'  <line x1="{x+47}" y1="{qy+3}" x2="{x+3}" y2="{qy+35}" stroke="#cc2222" '
                         f'stroke-width="2"/>\n')
                body += (f'  <rect x="{x}" y="{qy}" width="50" height="38" fill="none" '
                         f'stroke="#cc2222" stroke-width="2"/>\n')
            x += 58
    # every trace figure has the same canvas, so the graph stays in place from slide to slide
    write(f"05-bfs-{key}.svg", svg(BW, BH, body, defs=False))
    if key == "init":
        write("05-bfs-init-full.svg", svg(BW, BH, body, defs=False))

# ============================================================ what an algorithm is: schema and three examples
SEE, SEE1, SEE2, KARP = "#00a9e0", "#cceef9", "#a6e1f4", "#3e5496"


def ubox(x, y, w, h, fill=SEE1, stroke=SEE, sw=2.2, rx=10):
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>\n')


def uarrow(x1, y1, x2, y2):
    return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{KARP}" stroke-width="2.6" '
            f'marker-end="url(#ak)"/>\n')


def algorithm_examples():
    body = ('  <defs><marker id="ak" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{KARP}"/></marker></defs>\n')
    # the schema: input -> steps -> output
    body += ubox(6, 8, 170, 70, fill="#ffffff", stroke=KARP)
    body += txt(91, 53, "input", 30, weight="bold", fill=KARP)
    body += uarrow(180, 43, 232, 43)
    body += ubox(238, 8, 624, 70, fill=SEE2, stroke=KARP)
    for k, lab in enumerate(["step 1", "step 2", "step 3", "&#8230;", "step n"]):
        x = 252 + k * 121
        if lab != "&#8230;":
            body += ubox(x, 18, 108, 50, fill="#ffffff", stroke=SEE, sw=1.8, rx=7)
        body += txt(x + 54, 52, lab, 26)
    body += uarrow(866, 43, 918, 43)
    body += ubox(924, 8, 170, 70, fill="#ffffff", stroke=KARP)
    body += txt(1009, 53, "output", 30, weight="bold", fill=KARP)
    # three examples
    ex = [("Youngest respondent", "34, 51, 27, 46", "27"),
          ("Sort names", "Mia, Ana, Leo", "Ana, Leo, Mia"),
          ("Steps from Ana to Ben", "friendship network", "2 steps")]
    body += txt(6, 122, "Examples", 24, anchor="start", weight="bold", fill=KARP)
    body += (f'  <line x1="128" y1="114" x2="1094" y2="114" stroke="{KARP}" stroke-width="1.6" '
             f'stroke-dasharray="6 5"/>\n')
    for k, (prob, inp, out) in enumerate(ex):
        x = 6 + k * 366
        y0 = 136
        body += ubox(x, y0, 354, 190, fill=SEE1, stroke=SEE)
        body += txt(x + 177, y0 + 42, prob, 28, weight="bold")
        body += txt(x + 18, y0 + 96, "input", 24, anchor="start", fill="#555")
        body += txt(x + 112, y0 + 96, inp, 24, anchor="start")
        body += txt(x + 18, y0 + 156, "output", 24, anchor="start", fill="#555")
        body += txt(x + 112, y0 + 156, out, 24, anchor="start", weight="bold")
    write("05-algorithm-examples.svg", svg(1100, 332, body, defs=False))


algorithm_examples()

# ============================================================ flowchart of K-SMALLEST-ELEMENT
def flowchart_kth():
    F = 22
    body = ""
    cx = 290
    def arr(d):
        return f'  <path d="{d}" fill="none" stroke="#111" stroke-width="1.8" marker-end="url(#a)"/>\n'
    def lab(x, y, t):
        return txt(x, y, t, 19, fill="#333", style="italic")
    body += terminal(cx, 26, 140, 38, "start", fs=F)
    body += arr(f"M {cx} 45 V 66")
    body += parallelo(cx, 90, 210, 44, "read M, n, k", fs=F)
    body += arr(f"M {cx} 112 V 130")
    body += rectbox(cx, 152, 130, 40, "i ← 1", fs=F)
    body += arr(f"M {cx} 172 V 190")
    body += diamond(cx, 228, 180, 74, "i ≤ k ?", fs=F)
    # no: output and stop on the left
    body += arr(f"M {cx-90} 228 H 158")
    body += lab(cx - 112, 216, "no")
    body += parallelo(82, 228, 150, 44, "output M[k]", fs=F)
    body += arr("M 82 250 V 282")
    body += terminal(82, 302, 120, 38, "stop", fs=F)
    # yes: the inner loop
    body += arr(f"M {cx} 265 V 288")
    body += lab(cx + 24, 283, "yes")
    body += rectbox(cx, 318, 200, 58, "smallest ← i|j ← i + 1", fs=F)
    body += arr(f"M {cx} 347 V 366")
    body += diamond(cx, 404, 180, 74, "j ≤ n ?", fs=F)
    # no: swap and the next i
    body += arr(f"M {cx+90} 404 H 432")
    body += lab(cx + 108, 394, "no")
    body += rectbox(560, 404, 252, 64, "swap M[i], M[smallest]|i ← i + 1", fs=F)
    body += arr(f"M 560 372 V 228 H {cx+94}")
    # yes: compare
    body += arr(f"M {cx} 441 V 456")
    body += lab(cx + 24, 452, "yes")
    body += diamond(cx, 510, 300, 104, "M[j] &lt;|M[smallest] ?", fs=F)
    body += arr(f"M {cx} 562 V 592")
    body += lab(cx + 24, 584, "yes")
    body += rectbox(cx, 614, 170, 40, "smallest ← j", fs=F)
    body += arr(f"M {cx} 634 V 654")
    body += rectbox(cx, 674, 140, 40, "j ← j + 1", fs=F)
    body += arr(f"M {cx+150} 510 H 478 V 674 H {cx+74}")
    body += lab(cx + 172, 500, "no")
    body += arr(f"M {cx-70} 674 H 150 V 404 H {cx-94}")
    write("05-flowchart-kth.svg", svg(700, 700, body))


flowchart_kth()


# ============================================================ examples of graph problems on one graph
def graph_problems():
    """Three panels without text: the problems on one graph (shortest path in orange,
    central node in blue, a second connected subgraph in light blue), a spanning tree
    (green) and a coloring with three colors."""
    pos = {"a": (60, 70), "b": (170, 40), "c": (280, 70), "d": (110, 170), "e": (230, 175),
           "f": (340, 180), "g": (190, 270), "h": (500, 60), "i": (570, 140), "j": (500, 230)}
    edges = [("a", "b"), ("b", "c"), ("a", "d"), ("d", "e"), ("b", "e"), ("e", "f"), ("c", "f"),
             ("d", "g"), ("e", "g"), ("h", "i"), ("i", "j"), ("h", "j")]
    main = [e for e in edges if "h" not in e and "i" not in e and "j" not in e]
    path = [("a", "d"), ("d", "e"), ("e", "f")]
    tree = [("a", "b"), ("b", "c"), ("b", "e"), ("d", "e"), ("e", "f"), ("e", "g")]
    col = {"a": 0, "b": 1, "c": 0, "d": 1, "e": 0, "f": 1, "g": 2}
    COLS = ["#f4a3a0", "#9fd8f0", "#ffd966"]
    ORG, TREE = "#e07b00", "#2e9e4f"

    def has(lst, u, v):
        return (u, v) in lst or (v, u) in lst

    def panel(dx, dy, sc, which):
        out = ""
        nodes = pos if which == "top" else {k: v for k, v in pos.items() if k in "abcdefg"}
        es = edges if which == "top" else main
        P = {k: (dx + x * sc, dy + y * sc) for k, (x, y) in nodes.items()}
        if which == "top":
            out += (f'  <ellipse cx="{dx+530*sc}" cy="{dy+146*sc}" rx="{96*sc}" ry="{122*sc}" '
                    f'fill="#eef8fc" stroke="{SEE}" stroke-width="2" stroke-dasharray="7 5"/>\n')
        for u, v in es:
            (x1, y1), (x2, y2) = P[u], P[v]
            if which == "top" and has(path, u, v):
                st = f'stroke="{ORG}" stroke-width="6"'
            elif which == "tree" and has(tree, u, v):
                st = f'stroke="{TREE}" stroke-width="6"'
            elif which == "tree":
                st = 'stroke="#bbb" stroke-width="1.8" stroke-dasharray="5 4"'
            else:
                st = 'stroke="#555" stroke-width="2.2"'
            out += f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {st}/>\n'
        for n, (x, y) in P.items():
            fill, stroke, sw = "#fff", "#111", 1.8
            if which == "top" and n == "e":
                fill, stroke, sw = SEE2, KARP, 4
            if which == "color":
                fill = COLS[col[n]]
            out += (f'  <circle cx="{x}" cy="{y}" r="22" fill="{fill}" stroke="{stroke}" '
                    f'stroke-width="{sw}"/>\n')
            out += txt(x, y + 9, n, 26)
        return out

    body = panel(0, 0, 1.0, "top")
    body += f'  <line x1="10" y1="312" x2="630" y2="312" stroke="#ccc" stroke-width="1.5"/>\n'
    body += panel(-14, 324, 0.86, "tree")
    body += f'  <line x1="320" y1="330" x2="320" y2="580" stroke="#ccc" stroke-width="1.5"/>\n'
    body += panel(300, 324, 0.86, "color")
    write("05-graph-problems.svg", svg(640, 590, body, defs=False))


graph_problems()

# ============================================================ figures of the sheet 5 solutions
SOL = os.path.join(os.path.dirname(OUT), "..", "..", "TheoryExercises", "figures")


def write_sol(name, content):
    open(os.path.join(SOL, name), "w").write(content)
    print("  ", name, "(TheoryExercises/figures)")


def arrow_path(d):
    return f'  <path d="{d}" fill="none" stroke="#111" stroke-width="1.8" marker-end="url(#a)"/>\n'


def sol_ex2_graph():
    pos = {"D": (50, 110), "A": (160, 110), "B": (270, 110), "E": (380, 110), "C": (480, 45), "F": (480, 175)}
    edges = [("A", "B"), ("A", "D"), ("B", "E"), ("C", "E"), ("C", "F"), ("E", "F")]
    body = ""
    for u, v in edges:
        (x1, y1), (x2, y2) = pos[u], pos[v]
        body += f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#333" stroke-width="2.4"/>\n'
    for n, (x, y) in pos.items():
        body += f'  <circle cx="{x}" cy="{y}" r="26" fill="#fff" stroke="#111" stroke-width="2"/>\n'
        body += txt(x, y + 8, n, 24, weight="bold")
    write_sol("sol-05-ex2-graph.svg", svg(530, 220, body, defs=False))


def sol_a1_flowcharts():
    F = 20
    # a) even or odd
    body = terminal(180, 24, 130, 36, "start", fs=F)
    body += arrow_path("M 180 42 V 62") + parallelo(180, 84, 170, 42, "read n", fs=F)
    body += arrow_path("M 180 105 V 126") + diamond(180, 170, 230, 84, "n mod 2 = 0 ?", fs=F)
    body += arrow_path("M 65 170 H 40 V 248") + txt(52, 160, "yes", 18, fill="#333", style="italic")
    body += arrow_path("M 295 170 H 320 V 248") + txt(310, 160, "no", 18, fill="#333", style="italic")
    body += parallelo(60, 270, 120, 42, "print even", fs=F) + parallelo(300, 270, 120, 42, "print odd", fs=F)
    body += arrow_path("M 60 291 V 330 H 112") + arrow_path("M 300 291 V 330 H 248")
    body += terminal(180, 330, 130, 36, "stop", fs=F)
    write_sol("sol-05-a1a-flowchart.svg", svg(372, 352, body))
    # b) MYSTERY
    body = terminal(200, 24, 130, 36, "start", fs=F)
    body += arrow_path("M 200 42 V 62") + parallelo(200, 84, 170, 42, "read n", fs=F)
    body += arrow_path("M 200 105 V 124") + rectbox(200, 150, 150, 52, "r ← 0|i ← 1", fs=F)
    body += arrow_path("M 200 176 V 196") + diamond(200, 236, 170, 76, "i ≤ n ?", fs=F)
    body += arrow_path("M 200 274 V 300") + txt(222, 292, "yes", 18, fill="#333", style="italic")
    body += rectbox(200, 328, 170, 52, "r ← r + i|i ← i + 2", fs=F)
    body += arrow_path("M 115 328 H 60 V 236 H 111")
    body += arrow_path("M 285 236 H 365 V 330") + txt(304, 226, "no", 18, fill="#333", style="italic")
    body += parallelo(365, 352, 130, 42, "return r", fs=F)
    body += arrow_path("M 365 373 V 400")
    body += terminal(365, 420, 120, 36, "stop", fs=F)
    write_sol("sol-05-a1b-flowchart.svg", svg(440, 444, body))


sol_ex2_graph()
sol_a1_flowcharts()

print("deck 5 figures written")
