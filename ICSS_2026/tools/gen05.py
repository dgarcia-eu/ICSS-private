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
         f'stroke-width="6" marker-end="url(#ag)"/>\n')
body += txt(90, 78, "Rear &#10132;", 14, anchor="end")
body += txt(90, 282, "Front &#10132;", 14, anchor="end")
body += (f'  <rect x="214" y="278" width="120" height="34" fill="{LB}" stroke="#8a8a8a" stroke-width="1"/>\n')
body += txt(274, 268, "Dequeue", 14)
body += (f'  <path d="M 178 268 L 178 292 Q 178 296 190 296 L 208 296" fill="none" stroke="#4a4a4a" '
         f'stroke-width="6" marker-end="url(#ag)"/>\n')
write("05-queue.svg", svg(344, 322, body))

# ==================================================================== stack
body = ""
body += cells(96, 74, 6, 140, 38)
body += (f'  <rect x="8" y="24" width="120" height="34" fill="{LB}" stroke="#8a8a8a" stroke-width="1"/>\n')
body += txt(68, 16, "Push item", 14)
body += (f'  <rect x="222" y="24" width="120" height="34" fill="{LB}" stroke="#8a8a8a" stroke-width="1"/>\n')
body += txt(282, 16, "Pop item", 14)
body += (f'  <path d="M 128 41 L 148 41 Q 160 41 160 53 L 160 68" fill="none" stroke="#4a4a4a" '
         f'stroke-width="6" marker-end="url(#ag)"/>\n')
body += (f'  <path d="M 186 68 L 186 53 Q 186 41 198 41 L 216 41" fill="none" stroke="#4a4a4a" '
         f'stroke-width="6" marker-end="url(#ag)"/>\n')
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
    body += (f'  <text x="{x}" y="{y+5}" text-anchor="middle" font-size="13">V<tspan font-size="10" '
             f'dy="3">{k[1]}</tspan></text>\n')
write("05-graph-v1v8.svg", svg(380, 196, body, defs=False))

# ============================================================ BFS trace figures
GP = {"a": (34, 92), "b": (112, 58), "c": (192, 58), "d": (272, 58),
      "e": (112, 138), "f": (192, 138), "g": (272, 138)}
GE = [("a", "e"), ("e", "b"), ("b", "c"), ("c", "f"), ("c", "g"), ("d", "g"), ("e", "f")]
TOP = {"a", "b", "c", "d"}
INF = "&#8734;"

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

for key, (vals, cur, queue) in STATES.items():
    body = ""
    for a, b in GE:
        (x1, y1), (x2, y2) = GP[a], GP[b]
        body += f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="1"/>\n'
    for n, (x, y) in GP.items():
        d, par = vals[n]
        ring = ('  <circle cx="%d" cy="%d" r="22" fill="none" stroke="#111" stroke-width="4"/>\n'
                % (x, y)) if n == cur else ""
        body += ring
        body += (f'  <circle cx="{x}" cy="{y}" r="17" fill="#fff" stroke="#111" stroke-width="1.2"/>\n')
        body += txt(x, y + 6, d, 15)
        if n in TOP:
            body += txt(x, y - 24, n, 13, style="italic")
            body += txt(x, y - 40, par, 12, fill="#8a8a8a", style="italic")
        else:
            body += txt(x, y + 32, n, 13, style="italic")
            body += txt(x, y + 48, par, 12, fill="#8a8a8a", style="italic")
    h = 196
    if queue is not None:
        h = 254
        body += txt(14, 216, "Q:", 15, anchor="start", weight="bold", style="italic")
        x = 44
        if not queue:
            body += txt(70, 216, "&#8709;", 16, anchor="start")
        for item in queue:
            n, d = item[0], item[1]
            crossed = len(item) > 2
            body += (f'  <rect x="{x}" y="{198}" width="34" height="26" fill="#fff" stroke="#111" '
                     f'stroke-width="1"/>\n')
            body += txt(x + 17, 216, n, 14)
            body += txt(x + 17, 240, d, 12)
            if crossed:
                body += (f'  <line x1="{x+2}" y1="200" x2="{x+32}" y2="222" stroke="#cc2222" '
                         f'stroke-width="1.6"/>\n')
                body += (f'  <line x1="{x+32}" y1="200" x2="{x+2}" y2="222" stroke="#cc2222" '
                         f'stroke-width="1.6"/>\n')
                body += (f'  <rect x="{x}" y="198" width="34" height="26" fill="none" '
                         f'stroke="#cc2222" stroke-width="1.4"/>\n')
            x += 40
    write(f"05-bfs-{key}.svg", svg(320, h, body, defs=False))
    if key == "init":
        # the same graph on the canvas of the trace figures (room for the queue row),
        # so the INITIALIZE-BFS slide shows it exactly where the trace slides do
        write("05-bfs-init-full.svg", svg(320, 254, body, defs=False))

print("deck 5 figures written")
