#!/usr/bin/env python3
"""Figures of ICSS session 6 (Recursion) added on 2026-11-22.

Writes SVG files into Slides/06-Recursion/figures. The call-stack slides hold their
SVG inline (the code is text on the slide): it is written to figures/_callstack-N.html
and pasted into the deck between the <!-- CALLSTACK:N:BEGIN/END --> markers."""
import os

OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/06-Recursion/figures"
FONT = 'font-family="Arial, Helvetica, sans-serif"'
SEE, SEE1, SEE2, KARP = "#00a9e0", "#cceef9", "#a6e1f4", "#3e5496"
ORG, HL, RED, GREEN = "#e07b00", "#fde3a7", "#cc2222", "#2e9e4f"


def marker(mid, color, size=6):
    return (f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{size}" '
            f'markerHeight="{size}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
            f'fill="{color}"/></marker>')


DEFS = ("  <defs>" + marker("a", "#111") + marker("ar", "#b03a2e", 5) + marker("ao", ORG, 5)
        + marker("ak", KARP, 5) + marker("ag", "#888", 5) + "</defs>\n")


def svg(w, h, body, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" {FONT}{extra}>\n' + DEFS + body + '</svg>\n')


def txt(x, y, t, fs=14, anchor="middle", fill="#111", weight="normal", style="normal", extra=""):
    return (f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{fill}" '
            f'font-weight="{weight}" font-style="{style}"{extra}>{t}</text>\n')


def rect(x, y, w, h, fill="#fff", stroke="#111", sw=1.4, rx=0, extra=""):
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{extra}/>\n')


def line(x1, y1, x2, y2, stroke="#111", sw=1.4, extra=""):
    return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}"{extra}/>\n')


def path(d, stroke="#111", sw=1.6, fill="none", extra=""):
    return f'  <path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{extra}/>\n'


def write(name, content):
    open(os.path.join(OUT, name), "w").write(content)
    print("  ", name)


# ===================================================================== persons
SKIN = ["#f6d3b3", "#e9b98f", "#c98d63", "#f2c9a5", "#a8704a", "#f6d3b3", "#dba77c"]


def person(cx, top, shirt, hair, style="short", skin="#f6d3b3", s=1.0, label=None):
    """A simple figure, 70*s tall: shoulders, head and hair. (cx, top) is the top center."""
    def X(v):
        return round(cx + v * s, 1)

    def Y(v):
        return round(top + v * s, 1)
    o = path(f"M {X(-25)} {Y(70)} Q {X(-25)} {Y(40)} {X(0)} {Y(40)} Q {X(25)} {Y(40)} {X(25)} {Y(70)} Z",
             stroke="#333", sw=1.3, fill=shirt)
    if style == "long":
        o += path(f"M {X(-17)} {Y(18)} Q {X(-22)} {Y(40)} {X(-15)} {Y(46)} L {X(15)} {Y(46)} "
                  f"Q {X(22)} {Y(40)} {X(17)} {Y(18)} Z", stroke="none", fill=hair)
    o += (f'  <circle cx="{X(0)}" cy="{Y(20)}" r="{round(15*s,1)}" fill="{skin}" stroke="#333" '
          f'stroke-width="1.3"/>\n')
    if style != "bald":
        o += path(f"M {X(-15.5)} {Y(19)} A {round(15.5*s,1)} {round(15.5*s,1)} 0 0 1 {X(15.5)} {Y(19)} "
                  f"Q {X(8)} {Y(11)} {X(0)} {Y(12)} Q {X(-8)} {Y(11)} {X(-15.5)} {Y(19)} Z",
                  stroke="none", fill=hair)
    else:
        o += path(f"M {X(-15)} {Y(22)} Q {X(-17)} {Y(14)} {X(-12)} {Y(11)}", stroke=hair, sw=3)
        o += path(f"M {X(15)} {Y(22)} Q {X(17)} {Y(14)} {X(12)} {Y(11)}", stroke=hair, sw=3)
    if style == "bun":
        o += f'  <circle cx="{X(0)}" cy="{Y(3)}" r="{round(6*s,1)}" fill="{hair}"/>\n'
    if style == "pigtails":
        o += f'  <circle cx="{X(-17)}" cy="{Y(12)}" r="{round(5.5*s,1)}" fill="{hair}"/>\n'
        o += f'  <circle cx="{X(17)}" cy="{Y(12)}" r="{round(5.5*s,1)}" fill="{hair}"/>\n'
    if label:
        o += txt(X(0), Y(62), label, round(17 * s), weight="bold", fill="#fff")
    return o


# ========================================================= Simpleland (slides 6-17)
def land(cx, cy, r, label=True, fs=20):
    o = f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{SEE2}" stroke="{KARP}" stroke-width="{max(2, r/22):.1f}"/>\n'
    k = r / 60.0

    def P(pts):
        return " ".join(f"{cx + x*k:.1f} {cy + y*k:.1f}" for x, y in pts)
    # an island with a bay: an original shape, not a real country
    o += (f'  <path d="M {P([(-34, -18)])} C {P([(-30, -44), (6, -46), (14, -30)])} '
          f'C {P([(24, -36), (44, -22), (38, -4)])} C {P([(48, 10), (36, 34), (16, 32)])} '
          f'C {P([(4, 46), (-22, 42), (-24, 22)])} C {P([(-44, 20), (-46, -6), (-34, -18)])} Z" '
          f'fill="#9bd48a" stroke="#3d7d3a" stroke-width="{max(1.2, r/40):.1f}"/>\n')
    o += (f'  <path d="M {P([(-8, 30)])} C {P([(-2, 14), (10, 16), (12, 30)])}" fill="{SEE2}" '
          f'stroke="#3d7d3a" stroke-width="{max(1.2, r/40):.1f}"/>\n')
    # pin
    o += (f'  <path d="M {P([(2, -4)])} C {P([(-12, -22), (-8, -34), (2, -34)])} '
          f'C {P([(12, -34), (16, -22), (2, -4)])} Z" fill="#e0503a" stroke="#8c2a1c" '
          f'stroke-width="{max(1, r/50):.1f}"/>\n')
    o += f'  <circle cx="{cx + 2*k:.1f}" cy="{cy - 23*k:.1f}" r="{4*k:.1f}" fill="#fff"/>\n'
    if label:
        o += txt(cx, cy + r + fs + 4, "Simpleland", fs, weight="bold")
    return o


SW, SH = 1160, 314
ROW = {"unknown": 16, "grand": 42, "parents": 138, "p": 234}
PS = 1.05     # size of the persons
PX = 520
FAM = {
    "p": (PX, "p", "#d16ba5", "#2b2b2b", "pigtails", "#f2c9a5", "P"),
    "m": (PX - 130, "parents", "#d9534f", "#7a4a2a", "long", "#f6d3b3", None),
    "f": (PX + 130, "parents", "#e8a13a", "#3a3a3a", "short", "#dba77c", None),
    "gm1": (PX - 205, "grand", "#e6c84a", "#b9b9b9", "bun", "#f6d3b3", None),
    "gf1": (PX - 75, "grand", "#6f9fd8", "#b9b9b9", "bald", "#f2c9a5", None),
    "gm2": (PX + 75, "grand", "#7fb7e6", "#d0d0d0", "bun", "#dba77c", None),
    "gf2": (PX + 205, "grand", "#a8704a", "#c4c4c4", "bald", "#c98d63", None),
}
PARENTS = {"p": ("m", "f"), "m": ("gm1", "gf1"), "f": ("gm2", "gf2")}


def simpleland(level):
    """level 0: only the country; 1: P; 2: + parents; 3: + grandparents; 4: + unknown ancestors."""
    show = {0: [], 1: ["p"], 2: ["p", "m", "f"], 3: list(FAM), 4: list(FAM)}[level]
    body = ""
    # generation captions on the left, always at the same place
    caps = [("p", "P", 1), ("parents", "parents of P", 2), ("grand", "grandparents of P", 3)]
    for row, cap, lv in caps:
        if level >= lv:
            body += txt(20, ROW[row] + 46, cap, 20, anchor="start", fill="#666", style="italic")
    if level >= 4:
        body += txt(20, ROW["unknown"] + 9, "unknown ancestors", 20, anchor="start", fill=RED,
                    style="italic")
    for child, (a, b) in PARENTS.items():
        if child in show and a in show:
            cx, crow = FAM[child][0], ROW[FAM[child][1]]
            for q in (a, b):
                qx, qrow = FAM[q][0], ROW[FAM[q][1]]
                body += line(qx, qrow + 70 * PS + 2, cx, crow - 3, stroke="#777", sw=1.6)
    if level >= 4:
        for g in ("gm1", "gf1", "gm2", "gf2"):
            gx = FAM[g][0]
            for dx in (-26, 26):
                body += line(gx + dx, ROW["unknown"] + 16, gx, ROW["grand"] - 2, stroke=RED, sw=1.3,
                             extra=' stroke-dasharray="4 3"')
                body += (f'  <circle cx="{gx+dx}" cy="{ROW["unknown"]+3}" r="13" fill="#fff" '
                         f'stroke="{RED}" stroke-width="1.5" stroke-dasharray="4 3"/>\n')
                body += txt(gx + dx, ROW["unknown"] + 9, "?", 17, fill=RED, weight="bold")
    for k in show:
        x, row, shirt, hair, style, skin, lab = FAM[k]
        body += person(x, ROW[row], shirt, hair, style, skin, s=PS, label=lab)
    body += land(1040, 206, 62)
    return svg(SW, SH, body)


for lv in range(5):
    write(f"06-simpleland-{lv}.svg", simpleland(lv))
write("06-simpleland-map.svg", svg(420, 420, land(210, 190, 170, label=True, fs=34)))

# ====================================================== seating four diners
# Three figures on one canvas, so the slots stay in place from slide to slide.
def seating(kind):
    body = txt(6, 60, "Slots", 22, anchor="start", weight="bold")
    X0 = 150
    for i in range(4):
        x = X0 + i * 118
        body += (f'  <rect x="{x}" y="20" width="96" height="62" fill="#111"/>\n'
                 f'  <rect x="{x+10}" y="30" width="76" height="42" fill="#8fe8d8"/>\n')
        body += txt(x + 48, 62, str(i + 1), 26, weight="bold", fill="#555")
    if kind == "diners":
        body += txt(6, 146, "Diners", 22, anchor="start", weight="bold")
        for i, (shirt, hair, style, skin) in enumerate(DINERS):
            body += person(X0 + 48 + i * 118, 100, shirt, hair, style, skin, s=1.0, label="ABCD"[i])
    if kind == "choices":
        body += txt(6, 146, "Choices", 22, anchor="start", weight="bold")
        for i, (c, sep) in enumerate([("4", "·"), ("3", "·"), ("2", "·"), ("1", "")]):
            x = X0 + i * 118
            body += txt(x + 48, 148, c, 30, weight="bold")
            if sep:
                body += txt(x + 107, 146, sep, 30, weight="bold")
    return svg(640, 176, body)


DINERS = [("#d9534f", "#7a4a2a", "long", "#f6d3b3"), ("#3e5496", "#2b2b2b", "short", "#c98d63"),
          ("#2e9e4f", "#b06a2a", "bun", "#f2c9a5"), ("#e8a13a", "#3a3a3a", "bald", "#dba77c")]
for kind in ("diners", "choices"):
    write(f"06-seating-{kind}.svg", seating(kind))

# ===================================================== comment thread (motivation B)
def thread():
    W = 500
    fills = ["#e9f6fc", "#d4eef9", "#bfe5f5", "#aadcf1"]
    y = [6]
    parts = []

    def comment(x, w, depth, replies, who):
        y0 = y[0]
        start = len(parts)
        parts.append(None)                 # placeholder for the frame, drawn first
        yy = y0 + 9
        inner = rect(x + 10, yy, w - 20, 32, fill="#fff", stroke="#9a9a9a", sw=1, rx=5)
        inner += txt(x + 22, yy + 22, f"post by {who}", 18, anchor="start")
        parts.append(inner)
        yy += 40
        if replies:
            parts.append(txt(x + 12, yy + 14, "list of comments", 16, anchor="start", fill=KARP,
                             style="italic"))
            yy += 22
            y[0] = yy
            for r in replies:
                comment(x + 22, w - 34, depth + 1, r[1], r[0])
                y[0] += 7
            yy = y[0]
        else:
            parts.append(txt(x + 12, yy + 13, "empty list of comments", 16, anchor="start",
                             fill="#888", style="italic"))
            yy += 22
        h = yy - y0 + 4
        parts[start] = rect(x, y0, w, h, fill=fills[min(depth, 3)], stroke=KARP, sw=1.8, rx=8)
        y[0] = y0 + h

    comment(4, W - 8, 0, [("Ben", [("Ana", [])]), ("Cem", [])], "Ana")
    return svg(W, y[0] + 6, "".join(parts))


write("06-thread-recursive.svg", thread())

# ================================================= call stack of recursive_factorial(3)
MONO = 'font-family="DejaVu Sans Mono, Menlo, Consolas, Liberation Mono, monospace"'
KW, FN, NUM, TXT = "#d73a49", "#6f42c1", "#005cc5", "#24292e"
CODE = [
    [("def", KW), (" ", TXT), ("recursive_factorial", FN), ("(n):", TXT)],
    [("    ", TXT), ("if", KW), (" n == ", TXT), ("1", NUM), (":", TXT)],
    [("        ", TXT), ("return", KW), (" ", TXT), ("1", NUM)],
    [("    ", TXT), ("else", KW), (":", TXT)],
    [("        ", TXT), ("return", KW), (" n * recursive_factorial(n-", TXT), ("1", NUM), (")", TXT)],
]
FS, LH, FW, FH = 22, 28, 600, 5 * 28 + 14
CW = FS * 0.602                      # width of one monospace character
FX = [110, 250, 390]
FY = [58, 246, 434]
CSW, CSH = 1160, 596
REDA = "#b03a2e"


def frame(k, n, hl=None, dim=False, note=None):
    x, y = FX[k], FY[k]
    g = f'  <g opacity="{0.45 if dim else 1}">\n'
    g += rect(x, y, FW, FH, fill="#f6f8fa", stroke="#c9d1d9", sw=1.4, rx=6)
    if hl is not None:
        g += rect(x + 4, y + 7 + hl * LH, FW - 8, LH, fill=HL, stroke="none")
    for i, toks in enumerate(CODE):
        spans = "".join(f'<tspan fill="{c}"{" font-weight=\"bold\"" if c == KW else ""}>{t}</tspan>'
                        for t, c in toks)
        g += (f'  <text x="{x+14}" y="{y + 7 + i*LH + 20}" font-size="{FS}" {MONO} '
              f'xml:space="preserve" style="white-space:pre">{spans}</text>\n')
    # the parameter of this call
    g += txt(x + FW + 40, y + 41, "n:", 24, weight="bold", anchor="end")
    g += rect(x + FW + 48, y + 13, 42, 38, fill="#fff", stroke=REDA, sw=2.4)
    g += txt(x + FW + 69, y + 41, str(n), 24, weight="bold")
    if note:
        g += (f'  <text x="{x + FW + 12}" y="{y + 7 + 4*LH + 20}" font-size="{FS}" {MONO} '
              f'fill="{REDA}" font-weight="bold" xml:space="preserve" style="white-space:pre">{note}</text>\n')
    g += "  </g>\n"
    return g


def call_arrow(k):
    """Call from frame k-1 (or from the caller for k = 0) into frame k."""
    if k == 0:
        return (path(f"M 64 37 L {FX[0]+40} {FY[0]-5}", stroke=REDA, sw=3.4,
                     extra=' marker-end="url(#ar)"')
                + txt(FX[0] + 54, FY[0] - 7, "n=3", 24, weight="bold", anchor="start"))
    x1, y1 = FX[k-1] + 14 + 30 * CW, FY[k-1] + FH + 3
    x2, y2 = FX[k] + 310, FY[k] - 5
    return (path(f"M {x1:.0f} {y1} L {x2} {y2}", stroke=REDA, sw=3.4, extra=' marker-end="url(#ar)"')
            + txt(x2 + 16, y2 - 9, f"n={3-k}", 24, weight="bold", anchor="start"))


def return_geom(k):
    ln = 2 if k == 2 else 4
    xs, ys = FX[k] - 3, FY[k] + 7 + ln * LH + LH / 2
    if k == 0:
        xe, ye = 34, 40
        d = f"M {xs} {ys:.0f} C {xs-60} {ys+30:.0f} {xe-12} {ye+140} {xe} {ye}"
        lx, ly = 14, 150
    else:
        xe, ye = FX[k-1] + 56, FY[k-1] + FH + 5
        d = f"M {xs} {ys:.0f} C {xs-90} {ys+14:.0f} {xe-56} {ye+86} {xe} {ye}"
        lx, ly = xe - 40, ye + 70
    return d, lx, ly


def return_arrow(k):
    """Return from frame k to its caller (frame k-1, or the first call for k = 0)."""
    val = {2: "1", 1: "2", 0: "6"}[k]
    d, lx, ly = return_geom(k)
    return (path(d, stroke=REDA, sw=3.4, extra=' marker-end="url(#ar)"')
            + txt(lx, ly, val, 24, weight="bold", fill=REDA))


def tag(x, y, w, label):
    return (rect(x, y, w, 36, fill="#59d8c4", stroke="none", rx=3)
            + txt(x + w / 2, y + 26, label, 24, weight="bold"))


def callstack(step):
    b = txt(20, 28, "recursive_factorial(3)", 24, anchor="start", weight="bold")
    b += call_arrow(0)
    nframes = min(step, 3)
    rets = max(0, min(step - 3, 3))            # number of returns already shown
    if step >= 7:
        rets = 3
    dimmed = {0: [], 1: [2], 2: [2, 1], 3: [2, 1, 0]}[rets] if step <= 6 else []
    hl = {1: (0, 4), 2: (1, 4), 3: (2, 2), 4: (1, 4), 5: (0, 4)}.get(step)
    notes = {}
    if step >= 4:
        notes[1] = "= 2 * 1"
    if step >= 5:
        notes[0] = "= 3 * 2"
    for k in range(nframes):
        if k > 0:
            b += call_arrow(k)
        b += frame(k, 3 - k, hl=hl[1] if hl and hl[0] == k else None, dim=k in dimmed,
                   note=notes.get(k))
    for i in range(rets):
        b += return_arrow(2 - i)
    if step == 7:
        b += tag(930, 60, 200, "Memory costs")
        for k in range(3):
            b += path(f"M {(938, 1010, 1070)[k]} {96 if k else 78} L "
                      f"{FX[k] + FW + (94 if k == 0 else 72)} {FY[k] + (32 if k == 0 else 9)}",
                      stroke="#111", sw=2,
                      extra=' marker-end="url(#a)"')
    if step == 8:
        b += tag(20, 540, 160, "Time costs")
        for k in range(3):
            _, lx, ly = return_geom(k)
            b += path(f"M {60 + k*36} 538 L {lx + (4 if k else 0)} {ly + 12}", stroke="#111", sw=2,
                      extra=' marker-end="url(#a)"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CSW} {CSH}" class="callstack" '
            f'{FONT}>\n' + DEFS + b + '</svg>\n')


DECK = os.path.join(os.path.dirname(OUT), "ICSS-2026-06-Recursion.qmd")
deck = open(DECK).read()
for s in range(1, 9):
    write(f"_callstack-{s}.html", callstack(s))
    a, z = f"<!-- CALLSTACK:{s}:BEGIN -->\n", f"<!-- CALLSTACK:{s}:END -->"
    if a in deck:
        i, j = deck.index(a) + len(a), deck.index(z)
        deck = deck[:i] + "```{=html}\n" + callstack(s) + "```\n" + deck[j:]
open(DECK, "w").write(deck)

# ======================================================== memory of a process
def memory(hl=None):
    """The memory of the system, with the memory of one process inside it:
    code, heap, free space and stack."""
    W, H = 446, 476
    b = rect(3, 3, W - 6, H - 6, fill="#f4f4f4", stroke="#555", sw=2, rx=12)
    b += txt(W / 2, 30, "Memory of the system", 21, weight="bold", fill="#333")
    # the rest of the system memory, on the right
    RX, RW = 318, 114
    for y, h, labs, fill in [(46, 78, ["operating", "system"], "#dcdcdc"),
                             (134, 88, ["another", "process"], "#dcdcdc"),
                             (232, 88, ["another", "process"], "#dcdcdc")]:
        b += rect(RX, y, RW, h, fill=fill, stroke="#777", sw=1.3, rx=6)
        b += txt(RX + RW / 2, y + h / 2 - 3, labs[0], 17, fill="#444")
        b += txt(RX + RW / 2, y + h / 2 + 17, labs[1], 17, fill="#444")
    b += rect(RX, 330, RW, 98, fill="#fff", stroke="#777", sw=1.3, rx=6,
              extra=' stroke-dasharray="5 4"')
    b += txt(RX + RW / 2, 376, "not used", 17, fill="#777", style="italic")
    b += txt(RX + RW / 2, 396, "yet", 17, fill="#777", style="italic")
    # the memory of one process, on the left
    X, PW = 16, 286
    b += rect(X - 5, 41, PW + 10, 418, fill="#fff", stroke=KARP, sw=2.6, rx=8)
    segs = [("cs", 46, 78, "#e2dcc2", ["Code segment (CS)", "the program's instructions"]),
            ("ds", 124, 102, "#bcd6f0", ["Data segment / heap (DS)", "global data and objects"]),
            ("free", 226, 100, "#fff", ["free memory"]),
            ("ss", 326, 102, "#7fb1e8", ["Stack segment (SS)", "one frame per running call"])]
    for key, y, h, fill, labs in segs:
        on = hl in (None, key) or key == "free"
        b += (f'  <g opacity="{1 if on else 0.35}">\n'
              + rect(X, y, PW, h, fill=fill, stroke="#111", sw=1.4,
                     extra=' stroke-dasharray="5 4"' if key == "free" else "")
              + txt(X + PW / 2 if key != "free" else X + 204, y + h / 2 - (5 if len(labs) > 1 else -7),
                    labs[0], 21 if key != "free" else 19,
                    weight="bold" if key != "free" else "normal",
                    fill="#111" if key != "free" else "#777",
                    style="normal" if key != "free" else "italic")
              + (txt(X + PW / 2, y + h / 2 + 21, labs[1], 18, fill="#333") if len(labs) > 1 else "")
              + "  </g>\n")
        if hl == key:
            b += rect(X - 2, y - 2, PW + 4, h + 4, fill="none", stroke=ORG, sw=5, rx=3)
    # growth arrows in the free area
    b += line(X + 22, 232, X + 22, 266, stroke="#111", sw=2.4, extra=' marker-end="url(#a)"')
    b += txt(X + 34, 252, "heap grows", 16, anchor="start", fill="#444")
    b += line(X + 22, 320, X + 22, 286, stroke="#111", sw=2.4, extra=' marker-end="url(#a)"')
    b += txt(X + 34, 312, "stack grows", 16, anchor="start", fill="#444")
    b += txt(X + PW / 2, 451, "Memory of one process", 18, fill=KARP, weight="bold")
    return svg(W, H, b)


write("06-memory.svg", memory())
for k in ("cs", "ss", "ds"):
    write(f"06-memory-{k}.svg", memory(k))


def stack_fig(overflow=False):
    """The stack segment with the frames of recursive_factorial."""
    W, H = 446, 476
    b = ""
    top, bottom = 76 if overflow else 56, 432
    X, BW = 16, 300
    cx = X + BW / 2
    b += rect(X, top, BW, bottom - top, fill="#fff", stroke="#111", sw=1.6)
    b += line(X - 12, top, X + BW + 22, top, stroke=RED, sw=2.4, extra=' stroke-dasharray="7 4"')
    b += txt(X + BW + 28, top + 6, "limit of", 19, anchor="start", fill=RED, weight="bold")
    b += txt(X + BW + 28, top + 28, "the stack", 19, anchor="start", fill=RED, weight="bold")
    if not overflow:
        frames = [("recursive_factorial(3)", "n = 3"), ("recursive_factorial(2)", "n = 2"),
                  ("recursive_factorial(1)", "n = 1")]
        fh = 76
        b += rect(X, bottom - 40, BW, 40, fill="#dfe6ee", stroke="#111", sw=1.2)
        b += txt(cx, bottom - 14, "the program that made the call", 17, fill="#333")
        for i, (name, n) in enumerate(frames):
            y = bottom - 40 - (i + 1) * fh
            b += rect(X, y, BW, fh, fill=["#7fb1e8", "#9cc4ee", "#bcd6f0"][i], stroke="#111", sw=1.2)
            b += txt(cx, y + 32, name, 19, weight="bold")
            b += txt(cx, y + 57, f"{n}, return address", 17)
        ytop = bottom - 40 - 3 * fh
        b += line(X + 28, ytop - 8, X + 28, ytop - 50, stroke="#111", sw=2.4, extra=' marker-end="url(#a)"')
        b += txt(X + 42, ytop - 22, "each call adds a frame", 17, anchor="start", fill="#444")
        b += txt(cx, top + 34, "free stack memory", 18, fill="#777", style="italic")
        b += txt(W / 2, H - 12, "Stack segment during recursive_factorial(3)", 18, fill="#444",
                 style="italic")
    else:
        n, fh = 11, 31.6
        b += rect(X, bottom - 8, BW, 8, fill="#dfe6ee", stroke="#111", sw=1)
        for i in range(n):
            y = bottom - 8 - (i + 1) * fh
            b += rect(X, y, BW, fh, fill="#9cc4ee" if i % 2 else "#7fb1e8", stroke="#111", sw=1)
            lab = f"f(n = {3 - i})" if i < 5 else ("…" if i < n - 1 else "f(n = …)")
            b += txt(cx, y + 22, lab, 17)
        y = top - 36
        b += rect(X, y, BW, 36, fill="#f6b3ad", stroke=RED, sw=2.4)
        b += txt(cx, y + 25, "next frame: no room", 19, weight="bold", fill="#7a1410")
        b += txt(cx, y - 10, "stack overflow", 21, weight="bold", fill=RED)
        b += txt(W / 2, H - 12, "The base case is never reached", 18, fill="#444", style="italic")
    return svg(W, H, b)


write("06-stack-frames.svg", stack_fig(False))
write("06-stack-overflow.svg", stack_fig(True))

# ============================================== DFS for planning: topological sorting
TN = {"design": (70, 44), "ethics": (255, 44), "collect": (440, 44),
      "prereg.": (70, 170), "analyze": (255, 170), "write": (440, 170)}
TE = [("design", "ethics"), ("ethics", "collect"), ("design", "prereg."), ("collect", "analyze"),
      ("prereg.", "analyze"), ("analyze", "write")]


def dfs_times(nodes, edges):
    adj = {n: sorted(v for u, v in edges if u == n) for n in nodes}
    d, f, t = {}, {}, [0]

    def visit(u):
        t[0] += 1
        d[u] = t[0]
        for v in adj[u]:
            if v not in d:
                visit(v)
        t[0] += 1
        f[u] = t[0]
    for u in nodes:
        if u not in d:
            visit(u)
    return d, f


def boxclip(x1, y1, x2, y2, hw, hh, pad=3):
    import math
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    r = min(hw / (abs(dx) / L) if dx else 1e9, hh / (abs(dy) / L) if dy else 1e9)
    return (x1 + dx / L * (r + pad), y1 + dy / L * (r + pad),
            x2 - dx / L * (r + pad + 5), y2 - dy / L * (r + pad + 5))


def topo():
    d, f = dfs_times(list(TN), TE)
    b = ""
    BW, BH = 124, 58
    for u, v in TE:
        x1, y1, x2, y2 = boxclip(*TN[u], *TN[v], BW / 2, BH / 2)
        b += line(f"{x1:.0f}", f"{y1:.0f}", f"{x2:.0f}", f"{y2:.0f}", sw=1.8,
                  extra=' marker-end="url(#a)"')
    for n, (x, y) in TN.items():
        b += rect(x - BW / 2, y - BH / 2, BW, BH, fill=SEE1, stroke=KARP, sw=1.8, rx=8)
        b += txt(x, y - 3, n, 21, weight="bold")
        b += txt(x, y + 20, f"{d[n]}/{f[n]}", 17, fill="#444")
    # the result: tasks by decreasing finishing time
    order = sorted(TN, key=lambda n: -f[n])
    b += txt(4, 250, "Sorted by decreasing finishing time:", 20, anchor="start", weight="bold",
             fill=KARP)
    ow, gap, oy = 78, 7.4, 330
    pos = {}
    for i, n in enumerate(order):
        x = 4 + i * (ow + gap)
        pos[n] = x + ow / 2
        b += rect(x, oy, ow, 52, fill="#fff", stroke=KARP, sw=1.8, rx=6)
        b += txt(x + ow / 2, oy + 23, n, 18, weight="bold")
        b += txt(x + ow / 2, oy + 44, f"f = {f[n]}", 16, fill="#555")
    for u, v in TE:
        x1, x2 = pos[u] + 8, pos[v] - 8
        hgt = 16 + 10 * round((x2 - x1) / (ow + gap))
        b += path(f"M {x1:.0f} {oy-3} Q {(x1+x2)/2:.0f} {oy-3-hgt*1.6:.0f} {x2:.0f} {oy-4}",
                  stroke="#555", sw=1.5, extra=' marker-end="url(#ag)"')
    return svg(512, 388, b), order, d, f


t_svg, t_order, t_d, t_f = topo()
write("06-dfs-topological.svg", t_svg)
print("     topological order:", " -> ".join(t_order))


def cycle():
    pos = {"Statistics 1": (84, 66), "Statistics 2": (290, 66), "Methods": (496, 66),
           "Seminar": (393, 206)}
    edges = [("Statistics 1", "Statistics 2"), ("Statistics 2", "Methods"), ("Methods", "Seminar"),
             ("Seminar", "Statistics 2")]
    BW, BH = 150, 56
    b = ""
    for u, v in edges:
        back = (u, v) == ("Seminar", "Statistics 2")
        x1, y1, x2, y2 = boxclip(*pos[u], *pos[v], BW / 2, BH / 2)
        b += line(f"{x1:.0f}", f"{y1:.0f}", f"{x2:.0f}", f"{y2:.0f}", stroke=RED if back else "#111",
                  sw=4 if back else 1.8, extra=f' marker-end="url(#{"ar" if back else "a"})"')
    for n, (x, y) in pos.items():
        cur = n == "Seminar"
        b += rect(x - BW / 2, y - BH / 2, BW, BH, fill="#b8b8b8", stroke=ORG if cur else "#111",
                  sw=4 if cur else 1.6, rx=8)
        b += txt(x, y + 7, n, 21, weight="bold")
    b += txt(170, 158, "edge to a GRAY", 20, fill=RED, weight="bold")
    b += txt(170, 184, "vertex: a cycle", 20, fill=RED, weight="bold")
    b += txt(393, 262, "u, being processed", 18, fill=ORG, weight="bold")
    b += txt(290, 22, "v, still GRAY (its call has not returned)", 18, fill="#444", style="italic")
    return svg(580, 272, b)


write("06-dfs-cycle.svg", cycle())

# ===================================================== memoization: Fibonacci
def fibtree():
    nodes, edges, seen = [], [], set()
    nx = [0]

    def build(n, depth):
        i = len(nodes)
        again = n in seen and n > 1
        nodes.append([n, depth, None, again])
        if n < 2:
            nodes[i][2] = nx[0]
            nx[0] += 1
            return i
        kids = [build(n - 1, depth + 1), build(n - 2, depth + 1)]
        seen.add(n)
        for k in kids:
            edges.append((i, k))
        nodes[i][2] = sum(nodes[k][2] for k in kids) / 2
        return i
    build(5, 0)
    W, H = 760, 300
    sx = (W - 80) / (nx[0] - 1)
    b = ""

    def xy(i):
        return 40 + nodes[i][2] * sx, 26 + nodes[i][1] * 62
    for u, v in edges:
        (x1, y1), (x2, y2) = xy(u), xy(v)
        b += line(f"{x1:.0f}", y1 + 14, f"{x2:.0f}", y2 - 15, stroke="#777", sw=1.4)
    for i, (n, depth, _, again) in enumerate(nodes):
        x, y = xy(i)
        base = n < 2
        fill = "#fbd9a5" if again else ("#eeeeee" if base else SEE1)
        stroke = ORG if again else ("#999" if base else KARP)
        b += rect(x - 30, y - 15, 60, 30, fill=fill, stroke=stroke, sw=2 if again else 1.4, rx=7)
        b += txt(x, y + 5, f"FIB({n})", 14, weight="bold" if not base else "normal")
    b += rect(408, 262, 18, 18, fill="#fbd9a5", stroke=ORG, sw=2, rx=4)
    b += txt(434, 277, "computed again, although the result is known", 15, anchor="start")
    return svg(W, H, b), len(nodes)


f_svg, f_calls = fibtree()
write("06-fib-tree.svg", f_svg)
print("     calls of FIB(5):", f_calls)


def memo_array():
    vals = [0, 1, 1, 2, 3, 5, 8]
    b = txt(8, 78, "memo", 20, anchor="start", weight="bold", style="italic")
    x0, cw = 96, 82
    for i, v in enumerate(vals):
        x = x0 + i * cw
        new = i == 6
        b += rect(x, 50, cw, 46, fill=HL if new else ("#eeeeee" if i < 2 else SEE1), stroke="#111",
                  sw=1.4)
        b += txt(x + cw / 2, 81, str(v), 22, weight="bold")
        b += txt(x + cw / 2, 116, f"[{i}]", 15, fill="#555")
    xa, xb, xc = x0 + 4.5 * cw, x0 + 5.5 * cw, x0 + 6.5 * cw
    b += path(f"M {xb:.0f} 46 Q {(xb+xc)/2:.0f} 12 {xc-6:.0f} 44", stroke=ORG, sw=2.4,
              extra=' marker-end="url(#ao)"')
    b += path(f"M {xa:.0f} 46 Q {(xa+xc)/2:.0f} -14 {xc+6:.0f} 44", stroke=ORG, sw=2.4,
              extra=' marker-end="url(#ao)"')
    b += txt(xc + 50, 24, "3 + 5", 17, anchor="start", fill=ORG, weight="bold")
    return svg(760, 124, b)


write("06-memo-array.svg", memo_array())

# ========================================= types of algorithms (outtake slide)
def type_recursion():
    b = ""
    for i, lab in enumerate(["DFS-VISIT(c)", "DFS-VISIT(b)", "DFS-VISIT(e)"]):
        x, y, w, h = 6 + i * 34, 6 + i * 28, 388 - i * 68, 104 - i * 28 - (i * 6)
        b += rect(x, y, w, h, fill=["#e9f6fc", "#d4eef9", "#bfe5f5"][i], stroke=KARP, sw=1.6, rx=8)
        b += txt(x + 12, y + 20, lab, 15, anchor="start", weight="bold")
    b += txt(260, 86, "… until the base case", 14, fill="#444", style="italic")
    return svg(400, 116, b)


def type_greedy():
    pos = {"s": (60, 62), "a": (150, 24), "b": (150, 100), "c": (245, 24), "d": (245, 100),
           "e": (340, 62)}
    edges = [("s", "a"), ("s", "b"), ("a", "c"), ("b", "d"), ("c", "e"), ("d", "e"), ("a", "b")]
    dist = {"s": 0, "a": 1, "b": 1, "c": 2, "d": 2, "e": 3}
    fill = ["#222", "#7fb1e8", "#bcd6f0", "#fff"]
    b = ""
    for u, v in edges:
        b += line(*pos[u], *pos[v], stroke="#666", sw=1.6)
    for n, (x, y) in pos.items():
        b += f'  <circle cx="{x}" cy="{y}" r="17" fill="{fill[dist[n]]}" stroke="#111" stroke-width="1.5"/>\n'
        b += txt(x, y + 6, str(dist[n]), 16, weight="bold", fill="#fff" if dist[n] == 0 else "#111")
    b += txt(200, 138, "BFS: always the closest unvisited nodes next", 15, fill="#444", style="italic")
    return svg(400, 146, b)


def type_dc():
    b = ""
    rows = [[(20, 360)], [(20, 172), (208, 172)], [(20, 80), (112, 80), (208, 80), (300, 80)]]
    cols = ["#7fb1e8", "#bcd6f0", "#e9f6fc"]
    RH, GAP = 30, 22
    for r, row in enumerate(rows):
        for x, w in row:
            b += rect(x, 6 + r * (RH + GAP), w, RH, fill=cols[r], stroke=KARP, sw=1.5, rx=4)
    for r in range(2):
        for (x, w), kids in zip(rows[r], [rows[r+1][i:i+2] for i in range(0, len(rows[r+1]), 2)]):
            for kx, kw in kids:
                b += line(x + w / 2, 6 + RH + r * (RH + GAP), kx + kw / 2, 6 + (r + 1) * (RH + GAP),
                          stroke="#666", sw=1.3)
    b += txt(200, 27, "problem", 16, weight="bold")
    b += txt(106, 27 + RH + GAP, "half", 15) + txt(294, 27 + RH + GAP, "half", 15)
    for x, w in rows[2]:
        b += txt(x + w / 2, 27 + 2 * (RH + GAP), "quarter", 14)
    return svg(400, 146, b)


write("06-type-recursion.svg", type_recursion())
write("06-type-greedy.svg", type_greedy())
write("06-type-dc.svg", type_dc())
print("session 6 new figures written")
