#!/usr/bin/env python3
"""Figures for the question/answer example decks in Slides/Examples/NN-Examples/figures/.

Every figure is generated, and where a figure shows the result of a
computation (BFS on a maze, a Schelling run, IEEE 754 bit patterns, the
Titanic rule's confusion matrix) it is computed here rather than typed in, so
the picture and the numbers on the slide cannot disagree.

    python3 tools/genexamples_figs.py
"""
import math
import os
import re
import sys
import random
import struct
from datetime import datetime, timezone
from decimal import Decimal

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXDIR = os.path.join(ROOT, "Slides", "Examples")


def outdir(name):
    """Each figure goes to the figures/ folder of its deck, Slides/Examples/NN-Examples/figures/,
    with NN taken from the figure's name prefix."""
    d = os.path.join(EXDIR, f"{name[:2]}-Examples", "figures")
    os.makedirs(d, exist_ok=True)
    return d

SEEBLAU, SEEBLAU1, SEEBLAU2 = "#00a9e0", "#cceef9", "#a6e1f4"
KARPFEN, PETROL, SEEGRUEN, BORDEAUX = "#3e5496", "#00797b", "#0a9086", "#8e2043"
G5, G4, G3, G2, G1 = "#333333", "#666666", "#999999", "#cccccc", "#e5e5e5"
ORANGE = "#f5a623"
FONT = 'font-family="Arial, Helvetica, sans-serif"'

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": G4, "axes.labelcolor": G5,
                     "xtick.color": G4, "ytick.color": G4})


def svg(name, w, h, body, defs=""):
    path = os.path.join(outdir(name), name)
    with open(path, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
                f'width="{w}" height="{h}" {FONT}>\n<defs>'
                '<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                'markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{G5}"/></marker>'
                f'{defs}</defs>\n{body}\n</svg>\n')
    crop(path)
    print(" ", name)


def crop(path, pad=6):
    """Set the SVG canvas to the bounding box of what is drawn (plus pad), so that no text is clipped
    and no empty canvas makes the figure, and its text, smaller on the slide. Uses inkscape."""
    import subprocess
    q = subprocess.run(["inkscape", "--query-all", path], capture_output=True, text=True).stdout.split("\n")[0]
    x, y, w, h = (float(v) for v in q.split(",")[1:5])
    t = open(path).read()
    head = re.search(r"<svg[^>]*>", t).group(0)
    # inkscape reports px from the top-left corner of the current canvas: convert to user units
    vb = [float(v) for v in re.search(r'viewBox="([^"]*)"', head).group(1).replace(",", " ").split()]
    mw = re.search(r'\swidth="([\d.]+)', head)
    k = vb[2] / float(mw.group(1)) if mw else 1.0
    x, y, w, h = vb[0] + x * k, vb[1] + y * k, w * k, h * k
    x, y, w, h = x - pad, y - pad, w + 2 * pad, h + 2 * pad
    new = re.sub(r'viewBox="[^"]*"', f'viewBox="{x:.1f} {y:.1f} {w:.1f} {h:.1f}"', head)
    new = re.sub(r'\swidth="[^"]*"', f' width="{w:.0f}"', new, count=1)
    new = re.sub(r'\sheight="[^"]*"', f' height="{h:.0f}"', new, count=1)
    open(path, "w").write(t.replace(head, new, 1))


def png(name, fig):
    path = os.path.join(outdir(name), name)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(" ", name)


def T(x, y, s, size=16, anchor="start", fill=G5, weight="normal", style="normal", mono=False):
    fam = ' font-family="DejaVu Sans Mono, Menlo, monospace"' if mono else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}" font-weight="{weight}" font-style="{style}"{fam}>{s}</text>')


def R(x, y, w, h, fill="#fff", stroke=G5, sw=1.5, rx=4):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


def L(x1, y1, x2, y2, stroke=G5, sw=2, arrow=False, dash=""):
    a = ' marker-end="url(#ar)"' if arrow else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"{a}{d}/>'


def C(cx, cy, r, fill="#fff", stroke=G5, sw=2):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


# =========================================================================
#  02  Information coding
# =========================================================================
def fig_02():
    # --- Y2038: the 32-bit counter -------------------------------------
    hi = 2 ** 31 - 1
    lo = -(2 ** 31)
    t_hi = datetime.fromtimestamp(hi, timezone.utc)
    t_lo = datetime.fromtimestamp(lo, timezone.utc)
    print("   2^31-1 =", hi, "->", t_hi, "| wraps to", lo, "->", t_lo)

    def bits_row(y, value, label, color):
        b = f"{value & 0xFFFFFFFF:032b}"
        out = [T(20, y - 14, label, 15, fill=G4)]
        for i, ch in enumerate(b):
            x = 20 + i * 26
            fill = color if (i == 0) else "#fff"
            out.append(R(x, y, 24, 30, fill=fill, stroke=G3, sw=1, rx=2))
            out.append(T(x + 12, y + 21, ch, 17, "middle", "#fff" if i == 0 else G5, mono=True))
        return "\n".join(out)

    body = [
        T(20, 30, "signed 32-bit integer: seconds since 1 January 1970, 00:00:00 UTC", 17, fill=G5, weight="bold"),
        bits_row(70, hi, "2 147 483 647  =  19 January 2038, 03:14:07 UTC", SEEGRUEN),
        T(20, 128, "+ 1 second", 16, fill=G4, style="italic"),
        L(430, 118, 430, 148, arrow=True),
        bits_row(175, lo, "−2 147 483 648  =  13 December 1901, 20:45:52 UTC", BORDEAUX),
        T(20, 240, "sign bit", 13, fill=G4),
        L(32, 226, 32, 212, stroke=G4, sw=1.2, arrow=True),
    ]
    svg("02-y2038.svg", 870, 255, "\n".join(body))
    q = [T(20, 30, "signed 32-bit integer: seconds since 1 January 1970, 00:00:00 UTC", 17, fill=G5, weight="bold"),
         bits_row(70, hi, "2 147 483 647  =  19 January 2038, 03:14:07 UTC", SEEGRUEN),
         T(20, 140, "+ 1 second  →  ?", 20, fill=BORDEAUX, weight="bold")]
    svg("02-y2038-q.svg", 870, 160, "\n".join(q))

    # --- 0.1 + 0.2 -----------------------------------------------------
    def dbl(x):
        return struct.unpack(">Q", struct.pack(">d", x))[0]

    rows = [("0.1", 0.1), ("0.2", 0.2), ("0.1 + 0.2", 0.1 + 0.2), ("0.3", 0.3)]
    body = [T(20, 28, "IEEE 754 double: 1 sign · 11 exponent · 52 significand bits", 16, fill=G5, weight="bold")]
    y = 60
    for label, v in rows:
        u = dbl(v)
        hexs = f"0x{u:016X}"
        exact = Decimal(v)
        color = BORDEAUX if label in ("0.1 + 0.2",) else (SEEGRUEN if label == "0.3" else G5)
        body.append(T(20, y, label, 18, fill=color, weight="bold"))
        body.append(T(150, y, hexs, 18, fill=G5, mono=True))
        body.append(T(430, y, f"= {str(exact)[:38]}…", 15, fill=G4, mono=True))
        y += 38
    body.append(L(20, y - 20, 880, y - 20, stroke=G2, sw=1))
    body.append(T(20, y + 8, "last significand bits differ:  …3333333333333334  vs  …3333333333333333", 16, fill=BORDEAUX))
    body.append(T(20, y + 36, f"0.1 + 0.2 − 0.3 = {0.1 + 0.2 - 0.3:.3e}  (one unit in the last place)", 16, fill=G4, mono=True))
    svg("02-float-sum.svg", 900, y + 55, "\n".join(body))

    # --- Machine-readable zone -----------------------------------------
    body = [
        R(20, 20, 860, 300, fill="#f7f3e8", stroke=G3, sw=2, rx=14),
        T(50, 60, "REISEPASS · PASSPORT", 15, fill=G4),
        T(50, 105, "Name / Surname", 12, fill=G4),
        T(50, 132, "MÜLLER", 24, fill=G5, weight="bold"),
        T(50, 165, "Vornamen / Given names", 12, fill=G4),
        T(50, 192, "JÖRG", 24, fill=G5, weight="bold"),
        T(420, 105, "Geburtsort / Place of birth", 12, fill=G4),
        T(420, 132, "KÖLN", 24, fill=G5, weight="bold"),
        R(40, 228, 820, 72, fill="#fff", stroke=G2, sw=1, rx=6),
        T(52, 258, "P&lt;D&lt;&lt;MUELLER&lt;&lt;JOERG&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;", 20, fill=G5, mono=True),
        T(52, 288, "C01X00T478D&lt;&lt;6408125F2702283&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;4", 20, fill=G5, mono=True),
        T(880, 345, "machine-readable zone: 44 characters per line, from a set of 37 (A–Z, 0–9, &lt;)", 14, "end", G4),
    ]
    svg("02-mrz.svg", 900, 360, "\n".join(body))


# =========================================================================
#  03  Data structures
# =========================================================================
def fig_03():
    # --- browser back/forward stacks -----------------------------------
    def stacks(x0, title, back, fwd, current):
        out = [T(x0 + 130, 28, title, 15, "middle", G5, weight="bold")]
        out.append(R(x0 + 80, 40, 100, 34, fill=SEEBLAU2, stroke=SEEBLAU, rx=6))
        out.append(T(x0 + 130, 63, current, 17, "middle", G5, weight="bold"))
        for col, (lab, items) in enumerate([("back", back), ("forward", fwd)]):
            cx = x0 + 20 + col * 140
            out.append(T(cx + 50, 105, lab, 13, "middle", G4))
            for i, it in enumerate(reversed(items)):
                yy = 115 + i * 34
                out.append(R(cx, yy, 100, 30, fill="#fff", stroke=G3, rx=4))
                out.append(T(cx + 50, yy + 21, it, 15, "middle", G5))
            if not items:
                out.append(R(cx, 115, 100, 30, fill="#fff", stroke=G2, rx=4, sw=1))
                out.append(T(cx + 50, 136, "empty", 13, "middle", G3, style="italic"))
        return "\n".join(out)

    body = [
        stacks(0, "visit A, B, C", ["A", "B"], [], "C"),
        stacks(300, "back, back", [], ["C", "B"], "A"),
        stacks(600, "then visit D", ["A"], [], "D"),
        T(750, 250, "the forward stack is thrown away", 14, "middle", BORDEAUX, style="italic"),
    ]
    svg("03-browser-stacks.svg", 900, 265, "\n".join(body))

    # --- word count: list of pairs vs dictionary -----------------------
    words = ["the", "vote", "of", "party", "the", "budget", "vote", "the"]
    body = [T(20, 26, "counting words with a list of (word, count) pairs", 16, fill=G5, weight="bold")]
    for i, (w, c) in enumerate([("the", 3), ("vote", 2), ("of", 1), ("party", 1), ("budget", 1)]):
        y = 45 + i * 34
        body.append(R(20, y, 210, 30, fill="#fff", stroke=G3, rx=4))
        body.append(T(30, y + 21, f'("{w}", {c})', 15, mono=True))
    body.append(T(250, 60, "next word: \"vote\"", 15, fill=G4))
    body.append(T(250, 84, "→ scan pair 1, pair 2 … until found", 14, fill=BORDEAUX))
    body.append(T(250, 108, "cost grows with the number of distinct words", 14, fill=BORDEAUX))
    body.append(T(470, 26, "counting words with a dictionary", 16, fill=G5, weight="bold"))
    for i in range(6):
        y = 45 + i * 34
        body.append(R(470, y, 40, 30, fill=G1, stroke=G3, rx=3))
        body.append(T(490, y + 21, str(i), 13, "middle", G4, mono=True))
        body.append(R(515, y, 170, 30, fill="#fff", stroke=G3, rx=4))
    for slot, txt in [(0, '"of" → 1'), (2, '"the" → 3'), (3, '"vote" → 2'), (5, '"party" → 1')]:
        body.append(T(525, 45 + slot * 34 + 21, txt, 15, mono=True))
    body.append(T(700, 60, 'next word: "vote"', 15, fill=G4))
    body.append(T(700, 84, "→ hash(\"vote\") = 3 → slot 3, directly", 14, fill=SEEGRUEN))
    body.append(T(700, 108, "cost does not depend on table size", 14, fill=SEEGRUEN))
    svg("03-wordcount.svg", 900, 260, "\n".join(body))

    # --- measured timing: list vs dict ---------------------------------
    import time
    ns = [1_000, 3_000, 10_000, 30_000, 100_000]
    t_list, t_dict = [], []
    rnd = random.Random(1)
    for n in ns:
        vocab = [f"w{i}" for i in range(n // 2)]
        stream = [rnd.choice(vocab) for _ in range(n)]
        t0 = time.perf_counter()
        pairs = []
        for w in stream:
            for p in pairs:
                if p[0] == w:
                    p[1] += 1
                    break
            else:
                pairs.append([w, 1])
        t_list.append(time.perf_counter() - t0)
        t0 = time.perf_counter()
        d = {}
        for w in stream:
            d[w] = d.get(w, 0) + 1
        t_dict.append(time.perf_counter() - t0)
    print("   wordcount timings (s):", [f"{n}: list {a:.3f} dict {b:.4f}" for n, a, b in zip(ns, t_list, t_dict)])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ns, t_list, "o-", color=BORDEAUX, lw=2, label="list of (word, count) pairs")
    ax.plot(ns, t_dict, "s-", color=SEEBLAU, lw=2, label="dictionary")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("words counted (n)"); ax.set_ylabel("seconds (measured, this laptop)")
    ax.grid(alpha=.3, which="both")
    ax.legend(frameon=False)
    ax.set_title("Same task, two data structures", loc="left", color=G5)
    png("03-wordcount-timing.png", fig)

    # --- waiting room: shifting an array vs moving a head pointer ------
    body = [T(20, 26, "array: calling the next patient shifts everyone", 16, fill=G5, weight="bold")]
    names = ["Anna", "Ben", "Cem", "Dana", "Eli", "Fay"]
    for i, nm in enumerate(names):
        body.append(R(20 + i * 90, 40, 84, 34, fill=SEEBLAU2 if i == 0 else "#fff", stroke=G3, rx=4))
        body.append(T(62 + i * 90, 63, nm, 15, "middle"))
    body.append(T(580, 63, "← Anna is called", 14, fill=G4))
    for i, nm in enumerate(names[1:]):
        body.append(R(20 + i * 90, 95, 84, 34, fill="#fff", stroke=G3, rx=4))
        body.append(T(62 + i * 90, 118, nm, 15, "middle"))
        body.append(L(62 + (i + 1) * 90, 80, 62 + i * 90 + 8, 92, stroke=BORDEAUX, sw=1.5, arrow=True))
    body.append(T(20, 155, "n − 1 moves for one call; with 1 000 waiting, every call costs 1 000 moves", 14, fill=BORDEAUX))
    body.append(T(20, 200, "queue: the same call moves one pointer", 16, fill=G5, weight="bold"))
    for i, nm in enumerate(names):
        body.append(R(20 + i * 90, 214, 84, 34, fill=G1 if i == 0 else "#fff", stroke=G3, rx=4))
        body.append(T(62 + i * 90, 237, nm, 15, "middle", G3 if i == 0 else G5))
    body.append(T(62, 275, "head", 13, "middle", G4))
    body.append(L(62, 262, 62, 252, stroke=G4, sw=1.5, arrow=True))
    body.append(T(152, 275, "head", 13, "middle", SEEGRUEN, weight="bold"))
    body.append(L(152, 262, 152, 252, stroke=SEEGRUEN, sw=2, arrow=True))
    body.append(T(230, 275, "one step, however many are waiting", 14, fill=SEEGRUEN))
    svg("03-queue-shift.svg", 760, 290, "\n".join(body))
    svg("03-queue-shift-q.svg", 760, 170, "\n".join(body[:1 + 2 * len(names) + 1 + 3 * len(names[1:]) + 1]))


# =========================================================================
#  04  Programming
# =========================================================================
def fig_04():
    # --- string "sum" --------------------------------------------------
    body = [T(20, 26, "the survey column, as read from the file", 15, fill=G4)]
    vals = ["23", "41", "35", "29"]
    for i, v in enumerate(vals):
        body.append(R(20 + i * 70, 38, 60, 34, fill="#fff", stroke=G3, rx=4))
        body.append(T(50 + i * 70, 61, f'"{v}"', 15, "middle", mono=True))
    body.append(T(320, 61, "← each one is a string: quotes", 14, fill=G4))
    body.append(T(20, 120, "total = total + value", 17, fill=G5, mono=True))
    body.append(T(20, 160, 'with strings:   "" + "23" + "41" + "35" + "29"  =  "23413529"', 16, fill=BORDEAUX, mono=True))
    body.append(T(20, 195, "with integers:  0 + 23 + 41 + 35 + 29  =  128", 16, fill=SEEGRUEN, mono=True))
    body.append(T(20, 240, "same operator, same code, different type, different meaning", 15, fill=G4, style="italic"))
    svg("04-string-sum.svg", 760, 255, "\n".join(body))
    q = body[:1 + 2 * len(vals)] + [
        T(20, 120, 'total = ""', 17, fill=G5, mono=True),
        T(20, 150, "for value in ages:  total = total + value", 17, fill=G5, mono=True),
        T(20, 195, "print(total)   →   23413529354119…  (40 000 digits)", 17, fill=BORDEAUX, mono=True)]
    svg("04-string-sum-q.svg", 760, 215, "\n".join(q))

    # --- Ariane 5: 64-bit float into a 16-bit integer -------------------
    body = [
        T(20, 26, "horizontal velocity (BH), as computed", 15, fill=G4),
        R(20, 40, 420, 40, fill="#fff", stroke=G5, rx=6),
        T(230, 67, "64-bit float", 17, "middle"),
        T(450, 67, "e.g. 3.6 × 10⁴, five times what Ariane 4 ever reached", 14, fill=G4),
        L(230, 88, 230, 128, arrow=True),
        T(250, 112, "convert, so the value fits the old alignment code", 14, fill=G4),
        R(150, 135, 160, 40, fill="#fff", stroke=G5, rx=6),
        T(230, 162, "16-bit integer", 17, "middle"),
        T(330, 162, "range −32 768 … 32 767", 14, fill=G4),
        T(20, 215, "36 000 does not fit → operand error → exception not handled → unit shuts down", 15, fill=BORDEAUX),
        T(20, 245, "backup unit runs the same code → same error, 72 ms later → no attitude data → self-destruct at T+37 s", 15, fill=BORDEAUX),
    ]
    svg("04-ariane-overflow.svg", 900, 265, "\n".join(body))

    # --- leap-year flowchart -------------------------------------------
    def diamond(cx, cy, w, h, txt):
        pts = f"{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"
        return (f'<polygon points="{pts}" fill="#fff" stroke="{G5}" stroke-width="2"/>'
                + T(cx, cy + 6, txt, 15, "middle", mono=True))

    body = [
        R(180, 15, 140, 36, fill=SEEBLAU2, stroke=SEEBLAU, rx=18), T(250, 39, "year", 16, "middle"),
        L(250, 51, 250, 78, arrow=True),
        diamond(250, 110, 220, 60, "year mod 4 = 0 ?"),
        T(150, 155, "no", 13, "end", G4), L(250, 140, 250, 168, arrow=True),
        L(140, 110, 60, 110, arrow=True), T(100, 102, "no", 13, "middle", G4),
        R(10, 92, 50, 36, fill="#fde2e2", stroke=BORDEAUX, rx=6), T(35, 116, "no", 14, "middle", BORDEAUX),
        diamond(250, 200, 240, 60, "year mod 100 = 0 ?"),
        L(370, 200, 470, 200, arrow=True), T(420, 192, "no", 13, "middle", G4),
        R(470, 182, 60, 36, fill="#e0f3ec", stroke=SEEGRUEN, rx=6), T(500, 206, "leap", 14, "middle", SEEGRUEN),
        L(250, 230, 250, 258, arrow=True), T(262, 250, "yes", 13, "start", G4),
        diamond(250, 290, 240, 60, "year mod 400 = 0 ?"),
        L(370, 290, 470, 290, arrow=True), T(420, 282, "yes", 13, "middle", G4),
        R(470, 272, 60, 36, fill="#e0f3ec", stroke=SEEGRUEN, rx=6), T(500, 296, "leap", 14, "middle", SEEGRUEN),
        L(130, 290, 60, 290, arrow=True), T(95, 282, "no", 13, "middle", G4),
        R(10, 272, 50, 36, fill="#fde2e2", stroke=BORDEAUX, rx=6), T(35, 296, "no", 14, "middle", BORDEAUX),
        T(262, 160, "yes", 13, "start", G4),
        T(600, 110, "1900: mod 4 ✓, mod 100 ✓, mod 400 ✗ → not a leap year", 14, fill=G4),
        T(600, 135, "2000: mod 4 ✓, mod 100 ✓, mod 400 ✓ → leap year", 14, fill=G4),
        T(600, 160, "2024: mod 4 ✓, mod 100 ✗ → leap year", 14, fill=G4),
    ]
    svg("04-leap-year.svg", 940, 335, "\n".join(body))


# =========================================================================
#  05  Algorithms
# =========================================================================
def fig_05():
    # --- Erdős-number BFS on a small co-authorship graph ---------------
    nodes = {"Erdős": (90, 150), "Graham": (250, 70), "Chung": (250, 230), "Knuth": (410, 70),
             "Lovász": (410, 230), "Garcia": (570, 150), "You": (730, 150)}
    edges = [("Erdős", "Graham"), ("Erdős", "Chung"), ("Graham", "Chung"), ("Graham", "Knuth"),
             ("Chung", "Lovász"), ("Knuth", "Garcia"), ("Lovász", "Garcia"), ("Garcia", "You")]
    # BFS
    adj = {n: [] for n in nodes}
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)
    dist = {"Erdős": 0}
    q = ["Erdős"]
    while q:
        u = q.pop(0)
        for v in sorted(adj[u]):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    print("   Erdős numbers:", dist)
    body = []
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        body.append(L(x1, y1, x2, y2, stroke=G2, sw=2.5))
    layer_col = [SEEBLAU, SEEBLAU2, "#e0f3ec", "#fde9c8", "#fde2e2"]
    for n, (x, y) in nodes.items():
        d = dist[n]
        body.append(C(x, y, 36, fill=layer_col[d], stroke=G5))
        body.append(T(x, y - 4, n, 14, "middle", "#fff" if d == 0 else G5, weight="bold"))
        body.append(T(x, y + 16, str(d), 15, "middle", "#fff" if d == 0 else KARPFEN, weight="bold"))
    for d in range(5):
        body.append(R(20 + d * 130, 290, 24, 20, fill=layer_col[d], stroke=G3, rx=3, sw=1))
        body.append(T(50 + d * 130, 305, f"distance {d}", 13, fill=G4))
    svg("05-erdos-bfs.svg", 820, 320, "\n".join(body))
    q = []
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        q.append(L(x1, y1, x2, y2, stroke=G2, sw=2.5))
    for n, (x, y) in nodes.items():
        q.append(C(x, y, 36, fill=SEEBLAU if n == "Erdős" else "#fff", stroke=G5))
        q.append(T(x, y + 5, n, 14, "middle", "#fff" if n == "Erdős" else G5, weight="bold"))
    q.append(T(730, 215, "?", 26, "middle", BORDEAUX, weight="bold"))
    svg("05-erdos-q.svg", 820, 290, "\n".join(q))

    # --- Königsberg as a multigraph -----------------------------------
    P = {"A": (150, 190), "B": (400, 70), "C": (400, 310), "D": (650, 190)}
    def curve(a, b, bow):
        (x1, y1), (x2, y2) = P[a], P[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy)
        px, py = -dy / n * bow, dx / n * bow
        return f'<path d="M{x1},{y1} Q{mx+px},{my+py} {x2},{y2}" fill="none" stroke="{G4}" stroke-width="3"/>'
    body = [curve("A", "B", 40), curve("A", "B", -40), curve("A", "C", 40), curve("A", "C", -40),
            curve("A", "D", 0), curve("B", "D", 0), curve("C", "D", 0)]
    deg = {"A": 5, "B": 3, "C": 3, "D": 3}
    for k, (x, y) in P.items():
        body.append(C(x, y, 30, fill=SEEBLAU2, stroke=G5))
        body.append(T(x, y + 6, k, 18, "middle", weight="bold"))
        body.append(T(x, y + 52 if k != "B" else y - 40, f"degree {deg[k]}", 14, "middle", BORDEAUX))
    body.append(T(400, 175, "7 bridges = 7 edges", 14, "middle", G4, style="italic"))
    svg("05-konigsberg-graph.svg", 800, 375, "\n".join(body))

    # --- maze + BFS solution -------------------------------------------
    W, H = 21, 13   # odd sizes; cells at odd coordinates
    rnd = random.Random(7)
    grid = [[1] * W for _ in range(H)]

    def carve(x, y):
        grid[y][x] = 0
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        rnd.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 < nx < W - 1 and 0 < ny < H - 1 and grid[ny][nx] == 1:
                grid[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)
    carve(1, 1)
    start, goal = (1, 1), (W - 2, H - 2)
    # BFS
    dist = {start: 0}
    parent = {}
    q = [start]
    while q:
        u = q.pop(0)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            v = (u[0] + dx, u[1] + dy)
            if grid[v[1]][v[0]] == 0 and v not in dist:
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    print(f"   maze: BFS explored {len(dist)} cells, shortest path {dist[goal]} steps")
    cs = 32
    def draw(with_solution):
        out = []
        for y in range(H):
            for x in range(W):
                if grid[y][x] == 1:
                    out.append(f'<rect x="{x*cs}" y="{y*cs}" width="{cs}" height="{cs}" fill="{G5}"/>')
                elif with_solution and (x, y) in dist:
                    d = dist[(x, y)]
                    shade = int(235 - 110 * d / dist[goal])
                    out.append(f'<rect x="{x*cs}" y="{y*cs}" width="{cs}" height="{cs}" fill="rgb({shade - 40},{shade + 10},{min(255, shade + 30)})"/>')
                    out.append(T(x * cs + cs / 2, y * cs + cs / 2 + 4, str(d), 10, "middle", G5))
        if with_solution:
            pts = " ".join(f"{x*cs+cs/2},{y*cs+cs/2}" for x, y in path)
            out.append(f'<polyline points="{pts}" fill="none" stroke="{BORDEAUX}" stroke-width="5" stroke-linejoin="round"/>')
        out.append(C(start[0] * cs + cs / 2, start[1] * cs + cs / 2, 9, fill=SEEGRUEN, stroke="#fff"))
        out.append(C(goal[0] * cs + cs / 2, goal[1] * cs + cs / 2, 9, fill=BORDEAUX, stroke="#fff"))
        return "\n".join(out)
    svg("05-maze.svg", W * cs, H * cs, draw(False))
    svg("05-maze-solved.svg", W * cs, H * cs, draw(True))
    return dist[goal], len(dist)


# =========================================================================
#  06  Recursion
# =========================================================================
def fig_06():
    # --- Hanoi: pegs with 6 disks, and the recursive plan -------------
    def pegs(x0, disks_on, title):
        out = [T(x0 + 240, 22, title, 15, "middle", G5, weight="bold")]
        for p in range(3):
            px = x0 + 80 + p * 160
            out.append(L(px, 40, px, 170, stroke=G4, sw=5))
            out.append(L(px - 70, 170, px + 70, 170, stroke=G4, sw=5))
        for p, disks in enumerate(disks_on):
            px = x0 + 80 + p * 160
            for i, d in enumerate(reversed(disks)):
                w = 20 + d * 18
                y = 158 - i * 16
                out.append(R(px - w / 2, y, w, 13, fill=[SEEBLAU, SEEBLAU2, "#e0f3ec", "#fde9c8", "#fde2e2", G2][d - 1], stroke=G5, sw=1, rx=3))
        return "\n".join(out)
    body = [pegs(0, [[1, 2, 3, 4, 5, 6], [], []], "start: 6 disks on peg A"),
            pegs(500, [[6], [1, 2, 3, 4, 5], []], "after 31 moves: the top 5 on B"),
            T(20, 215, "plan for n disks:  move n−1 to the spare peg,  move the big one,  move n−1 back on top", 15, fill=G4),
            T(20, 242, "moves(n) = 2·moves(n−1) + 1  →  1, 3, 7, 15, 31, 63, …  =  2ⁿ − 1", 16, fill=KARPFEN, weight="bold")]
    svg("06-hanoi.svg", 1000, 260, "\n".join(body))
    secs = 2 ** 64 - 1
    years = secs / 31_557_600
    print(f"   Hanoi 64 disks: {secs} moves = {years:.3e} years")

    # --- fractal tree, four depths -------------------------------------
    def tree(x, y, angle, length, depth, out):
        if depth == 0:
            return
        x2 = x + length * math.cos(math.radians(angle))
        y2 = y - length * math.sin(math.radians(angle))
        col = SEEGRUEN if depth <= 2 else G5
        out.append(L(x, y, x2, y2, stroke=col, sw=max(1, depth * 0.7)))
        tree(x2, y2, angle - 25, length * 0.72, depth - 1, out)
        tree(x2, y2, angle + 25, length * 0.72, depth - 1, out)
    body = []
    for i, d in enumerate([1, 2, 4, 10]):
        x0 = 110 + i * 240
        body.append(T(x0, 25, f"depth {d}", 15, "middle", G4))
        tree(x0, 300, 90, 85, d, body)
    svg("06-fractal-tree.svg", 960, 310, "\n".join(body))

    # --- ancestors: doubling per generation ------------------------------
    body = [T(20, 26, "generation → number of ancestors (if no one appears twice)", 15, fill=G4)]
    rows = [(1, 2, "parents"), (2, 4, "grandparents"), (3, 8, ""), (5, 32, ""), (10, 1024, "~250 years back"),
            (20, 1_048_576, "~500 years back"), (30, 1_073_741_824, "~750 years, c. 1275 AD"),
            (40, 1_099_511_627_776, "~1000 years")]
    for i, (g, n, note) in enumerate(rows):
        y = 55 + i * 30
        body.append(T(20, y, f"{g:>2}", 16, mono=True))
        body.append(T(70, y, f"2^{g}", 16, fill=G4, mono=True))
        body.append(T(160, y, f"{n:,}".replace(",", " "), 16, fill=BORDEAUX if g >= 30 else G5, mono=True, weight="bold" if g >= 30 else "normal"))
        body.append(T(430, y, note, 14, fill=G4, style="italic"))
    body.append(T(20, 305, "world population around 1275 AD: roughly 400 000 000", 15, fill=KARPFEN, weight="bold"))
    svg("06-ancestors.svg", 760, 320, "\n".join(body))


# =========================================================================
#  07  Sorting
# =========================================================================
def fig_07():
    # --- radix sort on postcodes (last digit first) --------------------
    codes = ["78464", "10115", "78462", "80331", "78457", "10117", "50667", "78464"]
    body = [T(20, 24, "arrivals", 15, fill=G4)]
    for i, c in enumerate(codes):
        body.append(R(20, 34 + i * 27, 70, 24, fill="#fff", stroke=G3, rx=3))
        body.append(T(55, 51 + i * 27, c, 14, "middle", mono=True))
    body.append(T(160, 24, "pass 1: bin by the LAST digit", 15, fill=G4))
    bins = {}
    for c in codes:
        bins.setdefault(c[-1], []).append(c)
    x = 160
    for d in sorted(bins):
        body.append(R(x, 34, 74, 24, fill=SEEBLAU2, stroke=SEEBLAU, rx=3))
        body.append(T(x + 37, 51, f"bin {d}", 14, "middle"))
        for j, c in enumerate(bins[d]):
            body.append(R(x, 62 + j * 27, 74, 24, fill="#fff", stroke=G3, rx=3))
            body.append(T(x + 37, 79 + j * 27, c[:-1] + f'<tspan fill="{BORDEAUX}" font-weight="bold">{c[-1]}</tspan>', 14, "middle", mono=True))
        x += 84
    body.append(T(160, 250, "collect the bins in order, repeat for digit 4, 3, 2, 1: five passes, each a single sweep", 14, fill=G4))
    body.append(T(160, 274, "cost: 5 passes × n letters, no comparisons at all", 15, fill=KARPFEN, weight="bold"))
    svg("07-radix-postcodes.svg", 900, 290, "\n".join(body))

    # --- decision tree for sorting 3 elements --------------------------
    body = [T(20, 24, "every comparison sort of a, b, c is a decision tree with 3! = 6 leaves", 15, fill=G4)]
    def node(x, y, txt, leaf=False):
        if leaf:
            return R(x - 38, y - 13, 76, 26, fill="#e0f3ec", stroke=SEEGRUEN, rx=5) + T(x, y + 5, txt, 13, "middle", mono=True)
        return R(x - 32, y - 13, 64, 26, fill="#fff", stroke=G5, rx=13) + T(x, y + 5, txt, 13, "middle", mono=True)
    E = lambda x1, y1, x2, y2: L(x1, y1 + 13, x2, y2 - 13, stroke=G3, sw=1.5)
    body += [E(450, 60, 250, 130), E(450, 60, 650, 130), E(250, 130, 130, 200), E(250, 130, 370, 200),
             E(650, 130, 530, 200), E(650, 130, 770, 200), E(370, 200, 300, 270), E(370, 200, 440, 270),
             E(530, 200, 460, 270), E(530, 200, 600, 270)]
    body += [node(450, 60, "a &lt; b ?"), node(250, 130, "b &lt; c ?"), node(650, 130, "a &lt; c ?"),
             node(130, 200, "a b c", True), node(370, 200, "a &lt; c ?"), node(530, 200, "b &lt; c ?"), node(770, 200, "c b a", True),
             node(300, 270, "a c b", True), node(440, 270, "c a b", True), node(460, 270, "b a c", True), node(600, 270, "b c a", True)]
    body.append(T(20, 312, "6 leaves need depth ≥ log₂ 6 = 2.58 → at least 3 comparisons in the worst case", 15, fill=KARPFEN, weight="bold"))
    body.append(T(20, 336, "n items: n! leaves → depth ≥ log₂(n!) ≈ n log₂ n − 1.44 n", 15, fill=G4))
    svg("07-decision-tree.svg", 900, 350, "\n".join(body))

    # --- quickselect for the median ------------------------------------
    A = [38, 12, 71, 25, 56, 90, 44, 17, 63]
    target = (len(A) + 1) // 2  # 5th smallest
    steps = []
    lo, hi, arr = 0, len(A) - 1, A[:]
    while True:
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        q = i + 1
        steps.append((lo, hi, pivot, q, arr[:]))
        if q == target - 1:
            break
        if q > target - 1:
            hi = q - 1
        else:
            lo = q + 1
    print("   quickselect median:", arr[target - 1], "in", len(steps), "partitions")
    body = [T(20, 24, f"find the median (5th smallest of 9) without sorting everything", 15, fill=G4)]
    y = 40
    for k, (lo, hi, pv, q, snapshot) in enumerate(steps):
        body.append(T(20, y + 18, f"partition [{lo}..{hi}], pivot {pv}", 13, fill=G4))
        for i, v in enumerate(snapshot):
            fill = "#e0f3ec" if i == q else ("#fff" if lo <= i <= hi else G1)
            body.append(R(230 + i * 50, y, 44, 28, fill=fill, stroke=SEEGRUEN if i == q else G3, rx=4))
            body.append(T(252 + i * 50, y + 19, str(v), 14, "middle", mono=True))
        body.append(T(700, y + 18, f"pivot lands at position {q}" + (": done" if q == target - 1 else (" → look left" if q > target - 1 else " → look right")), 13, fill=G4))
        y += 44
    body.append(T(20, y + 14, f"median = {arr[target-1]}.  Only one side is ever recursed into: expected cost O(n), not O(n log n)", 15, fill=KARPFEN, weight="bold"))
    svg("07-quickselect.svg", 960, y + 35, "\n".join(body))


# =========================================================================
#  08  Time complexity
# =========================================================================
def fig_08():
    # --- password brute force ------------------------------------------
    rate = 1e10  # guesses per second, offline attack on a GPU rig
    cases = [("8 lowercase letters", 26 ** 8), ("8 chars, any of 95", 95 ** 8),
             ("4 random common words (2048 list)", 2048 ** 4), ("12 lowercase letters", 26 ** 12),
             ("12 chars, any of 95", 95 ** 12), ("6 random common words", 2048 ** 6)]
    fig, ax = plt.subplots(figsize=(8, 4.2))
    labels = [c[0] for c in cases]
    secs = [c[1] / rate for c in cases]
    ax.barh(labels, secs, color=[SEEBLAU, SEEBLAU, SEEGRUEN, SEEBLAU, SEEBLAU, SEEGRUEN])
    ax.set_xscale("log")
    for y, s in enumerate(secs):
        if s < 60: t = f"{s:.0f} s"
        elif s < 3600: t = f"{s/60:.0f} min"
        elif s < 86400: t = f"{s/3600:.0f} h"
        elif s < 3.16e7: t = f"{s/86400:.0f} days"
        else: t = f"{s/3.156e7:,.0f} years".replace(",", " ")
        ax.text(s * 1.6, y, t, va="center", fontsize=11, color=G5)
    ax.set_xlim(1, 1e17)
    ax.set_xlabel("time to try every possibility at 10¹⁰ guesses per second (log scale)")
    ax.invert_yaxis()
    ax.set_title("Brute force is exponential in the length", loc="left", color=G5)
    png("08-password-bruteforce.png", fig)
    for l, s in zip(labels, secs):
        print(f"   {l}: {s:.3g} s")

    # --- quadratic memory ------------------------------------------------
    ns = [1e3, 3e3, 1e4, 3e4, 1e5, 3e5, 1e6]
    mem = [n * n * 8 for n in ns]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(ns, mem, "o-", color=BORDEAUX, lw=2, label="n × n distance matrix, 8 bytes per cell")
    ax.plot(ns, [n * 8 * 12 for n in ns], "s-", color=SEEBLAU, lw=2, label="the data itself (12 columns)")
    ax.axhline(16e9, color=G3, ls="--"); ax.text(1.1e3, 16e9 * 1.4, "16 GB laptop", color=G4)
    ax.axhline(512e9, color=G3, ls="--"); ax.text(1.1e3, 512e9 * 1.4, "512 GB cluster node", color=G4)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("respondents (n)"); ax.set_ylabel("bytes")
    ax.grid(alpha=.3, which="both"); ax.legend(frameon=False, loc="upper left")
    ax.set_title("Memory of a pairwise-distance matrix", loc="left", color=G5)
    png("08-quadratic-memory.png", fig)

    # --- algorithms vs hardware (Grötschel, in PCAST 2010) --------------
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.bar(["faster hardware\n(1988 → 2003)", "better algorithms\n(1988 → 2003)", "both together"],
           [1_000, 43_000, 43_000_000], color=[G3, SEEBLAU, KARPFEN])
    ax.set_yscale("log")
    for i, v in enumerate([1_000, 43_000, 43_000_000]):
        ax.text(i, v * 1.4, f"{v:,}×".replace(",", " "), ha="center", color=G5, fontsize=13, fontweight="bold")
    ax.set_ylim(1, 5e8); ax.set_ylabel("speed-up of a benchmark linear-programming solve")
    ax.set_title("Where the speed came from", loc="left", color=G5)
    png("08-algorithms-vs-hardware.png", fig)


# =========================================================================
#  09  Theoretical CS
# =========================================================================
def fig_09():
    # --- vending machine DFA: 10c / 20c coins, accept at 50c ------------
    states = [0, 10, 20, 30, 40, 50]
    xs = {s: 70 + i * 150 for i, s in enumerate(states)}
    y = 120
    body = [T(20, 24, "coins: 10 or 20 cents · accept when exactly 50 cents have been inserted", 15, fill=G4)]
    for s in states:
        body.append(C(xs[s], y, 30, fill="#e0f3ec" if s == 50 else "#fff", stroke=G5))
        if s == 50:
            body.append(C(xs[s], y, 24, fill="none", stroke=G5))
        body.append(T(xs[s], y + 6, f"{s}c", 15, "middle", weight="bold"))
    body.append(L(10, y, 38, y, arrow=True))
    for s in states[:-1]:
        body.append(L(xs[s] + 30, y, xs[s + 10] - 32, y, arrow=True))
        body.append(T((xs[s] + xs[s + 10]) / 2, y - 8, "10", 13, "middle", G4))
    for s in states[:-2]:
        x1, x2 = xs[s], xs[s + 20]
        body.append(f'<path d="M{x1+14},{y+27} Q{(x1+x2)/2},{y+95} {x2-16},{y+27}" fill="none" stroke="{G5}" stroke-width="2" marker-end="url(#ar)"/>')
        body.append(T((x1 + x2) / 2, y + 74, "20", 13, "middle", G4))
    body.append(f'<path d="M{xs[40]+14},{y+27} Q{xs[40]+90},{y+120} {xs[40]+160},{y+60}" fill="none" stroke="{BORDEAUX}" stroke-width="2" marker-end="url(#ar)"/>')
    body.append(R(xs[40] + 140, y + 60, 90, 30, fill="#fde2e2", stroke=BORDEAUX, rx=6))
    body.append(T(xs[40] + 185, y + 80, "reject", 14, "middle", BORDEAUX))
    body.append(T(xs[40] + 60, y + 100, "20 (would be 60)", 12, "middle", BORDEAUX))
    body.append(T(20, y + 130, "6 states: the machine only needs to remember how much has been paid so far", 15, fill=KARPFEN, weight="bold"))
    svg("09-vending-dfa.svg", 960, 275, "\n".join(body))

    # --- bracket checking with a stack ---------------------------------
    s = "(()(()))"
    body = [T(20, 24, f"input:  {s}     (one symbol at a time, with a stack)", 15, fill=G4)]
    stack = []
    for i, ch in enumerate(s):
        x = 20 + i * 108
        body.append(R(x, 40, 100, 30, fill=SEEBLAU2 if ch == "(" else "#fde9c8", stroke=G3, rx=4))
        body.append(T(x + 50, 61, f"read {ch}", 14, "middle", mono=True))
        if ch == "(":
            stack.append("(")
        else:
            stack.pop()
        for j, _ in enumerate(stack):
            body.append(R(x + 25, 200 - j * 26, 50, 22, fill="#fff", stroke=G5, rx=3))
            body.append(T(x + 50, 216 - j * 26, "(", 14, "middle", mono=True))
        body.append(L(x + 15, 224, x + 85, 224, stroke=G4, sw=2))
        body.append(T(x + 50, 245, f"depth {len(stack)}", 12, "middle", G4))
    body.append(T(20, 280, "accept ⇔ never pop an empty stack, and the stack is empty at the end", 15, fill=KARPFEN, weight="bold"))
    body.append(T(20, 304, "a finite automaton cannot do this: it has no unbounded counter, and depth is unbounded", 14, fill=BORDEAUX))
    svg("09-brackets-pda.svg", 900, 320, "\n".join(body))


# =========================================================================
#  10  Machine learning
# =========================================================================
def fig_10():
    # --- husky vs wolf: what the model looked at ------------------------
    def panel(x, label, snow, verdict, ok):
        out = [R(x, 30, 200, 150, fill="#eaf4fb" if snow else "#dfe8d3", stroke=G3, rx=8)]
        if snow:
            for k in range(14):
                out.append(C(x + 15 + (k * 37) % 190, 45 + (k * 53) % 120, 3, fill="#fff", stroke="#fff"))
        # a very schematic canine: body + head + ears
        out.append(f'<ellipse cx="{x+100}" cy="{125}" rx="48" ry="22" fill="{G4}"/>')
        out.append(C(x + 140, 105, 18, fill=G4, stroke=G4))
        out.append(f'<polygon points="{x+130},{92} {x+136},{72} {x+146},{92}" fill="{G4}"/>')
        out.append(f'<polygon points="{x+146},{92} {x+154},{72} {x+160},{92}" fill="{G4}"/>')
        out.append(T(x + 100, 200, label, 14, "middle", G5))
        out.append(T(x + 100, 222, f"model says: {verdict}", 14, "middle", SEEGRUEN if ok else BORDEAUX, weight="bold"))
        return "\n".join(out)
    body = [panel(20, "wolf, in snow (training)", True, "wolf", True),
            panel(250, "husky, on grass (training)", False, "husky", True),
            panel(480, "husky, in snow (new photo)", True, "wolf", False),
            panel(710, "wolf, on grass (new photo)", False, "husky", False)]
    svg("10-husky-wolf-q.svg", 940, 235, "\n".join(body))
    body.append(f'<rect x="480" y="30" width="200" height="150" rx="8" fill="none" stroke="{BORDEAUX}" stroke-width="3" stroke-dasharray="6,4"/>')
    body.append(T(580, 262, "what the explanation highlights: the background, not the animal", 14, "middle", BORDEAUX, style="italic"))
    svg("10-husky-wolf.svg", 940, 275, "\n".join(body))

    # --- Titanic: the one-rule model -------------------------------------
    # Kaggle training set, 891 passengers
    female_s, female_d, male_s, male_d = 233, 81, 109, 468
    tp, fp, fn, tn = female_s, female_d, male_s, male_d
    acc = (tp + tn) / (tp + fp + fn + tn)
    prec = tp / (tp + fp); rec = tp / (tp + fn)
    print(f"   Titanic rule 'survived iff female': acc {acc:.3f} prec {prec:.3f} rec {rec:.3f}")
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.8))
    ax = axs[0]
    ax.bar(["women", "men"], [female_s / (female_s + female_d), male_s / (male_s + male_d)], color=[SEEBLAU, G3])
    ax.set_ylim(0, 1); ax.set_ylabel("share who survived")
    for i, v in enumerate([female_s / (female_s + female_d), male_s / (male_s + male_d)]):
        ax.text(i, v + .03, f"{v:.0%}", ha="center", color=G5, fontsize=13)
    ax.set_title("Survival by sex (n = 891)", loc="left", color=G5)
    ax = axs[1]
    cls = {1: (136, 80), 2: (87, 97), 3: (119, 372)}
    ax.bar(["1st", "2nd", "3rd"], [s / (s + d) for s, d in cls.values()], color=[SEEBLAU, SEEBLAU2, G3])
    for i, (s, d) in enumerate(cls.values()):
        ax.text(i, s / (s + d) + .03, f"{s/(s+d):.0%}", ha="center", color=G5, fontsize=13)
    ax.set_ylim(0, 1); ax.set_title("Survival by ticket class", loc="left", color=G5)
    png("10-titanic-rates.png", fig)
    body = [T(20, 26, "rule: predict 'survived' if and only if the passenger is a woman", 15, fill=G5, weight="bold"),
            R(180, 45, 130, 30, fill=G1, stroke=G3, rx=4), T(245, 66, "predicted: yes", 13, "middle", G4),
            R(320, 45, 130, 30, fill=G1, stroke=G3, rx=4), T(385, 66, "predicted: no", 13, "middle", G4),
            R(40, 85, 130, 40, fill=G1, stroke=G3, rx=4), T(105, 110, "survived", 13, "middle", G4),
            R(40, 135, 130, 40, fill=G1, stroke=G3, rx=4), T(105, 160, "died", 13, "middle", G4),
            R(180, 85, 130, 40, fill="#e0f3ec", stroke=SEEGRUEN, rx=4), T(245, 110, f"TP = {tp}", 15, "middle"),
            R(320, 85, 130, 40, fill="#fde2e2", stroke=BORDEAUX, rx=4), T(385, 110, f"FN = {fn}", 15, "middle"),
            R(180, 135, 130, 40, fill="#fde2e2", stroke=BORDEAUX, rx=4), T(245, 160, f"FP = {fp}", 15, "middle"),
            R(320, 135, 130, 40, fill="#e0f3ec", stroke=SEEGRUEN, rx=4), T(385, 160, f"TN = {tn}", 15, "middle"),
            T(490, 100, f"accuracy  = ({tp} + {tn}) / 891 = {acc:.1%}", 15, mono=True),
            T(490, 128, f"precision = {tp} / ({tp} + {fp}) = {prec:.2f}", 15, mono=True),
            T(490, 156, f"recall    = {tp} / ({tp} + {fn}) = {rec:.2f}", 15, mono=True),
            T(20, 205, "a one-feature rule that a human could state in five words gets 79%: the baseline every model must beat", 14, fill=KARPFEN, weight="bold")]
    svg("10-titanic-confusion.svg", 900, 220, "\n".join(body))

    # --- k-means: blobs, elbow, rings ------------------------------------
    rnd = random.Random(3)
    centers = [(2, 2), (7, 7), (8, 1.5)]
    pts = []
    for cx, cy in centers:
        for _ in range(80):
            pts.append((rnd.gauss(cx, 0.8), rnd.gauss(cy, 0.8)))

    def kmeans(P, k, iters=30, seed=0):
        r = random.Random(seed)
        means = r.sample(P, k)
        for _ in range(iters):
            groups = [[] for _ in range(k)]
            for p in P:
                j = min(range(k), key=lambda j: (p[0] - means[j][0]) ** 2 + (p[1] - means[j][1]) ** 2)
                groups[j].append(p)
            means = [(sum(a for a, _ in g) / len(g), sum(b for _, b in g) / len(g)) if g else means[j] for j, g in enumerate(groups)]
        wss = sum(min((p[0] - m[0]) ** 2 + (p[1] - m[1]) ** 2 for m in means) for p in P)
        return means, groups, wss

    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=18, color=G4, alpha=.7)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title("240 respondents, two attitude scores", loc="left", color=G5)
    png("10-kmeans-data.png", fig)

    means, groups, _ = kmeans(pts, 3, seed=1)
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    for g, col in zip(groups, [SEEBLAU, SEEGRUEN, ORANGE]):
        ax.scatter([p[0] for p in g], [p[1] for p in g], s=18, color=col, alpha=.8)
    ax.scatter([m[0] for m in means], [m[1] for m in means], marker="X", s=160, color=G5)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title("K-means with K = 3", loc="left", color=G5)
    png("10-kmeans-k3.png", fig)

    ks = list(range(1, 9))
    wss = [min(kmeans(pts, k, seed=s)[2] for s in range(5)) for k in ks]
    print("   k-means WSS:", [f"{w:.0f}" for w in wss])
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    ax.plot(ks, wss, "o-", color=KARPFEN, lw=2)
    ax.axvline(3, color=SEEGRUEN, ls="--"); ax.text(3.15, wss[0] * .8, "elbow at K = 3", color=SEEGRUEN)
    ax.set_xlabel("K"); ax.set_ylabel("within-cluster sum of squares")
    ax.set_title("Choosing K", loc="left", color=G5)
    png("10-kmeans-elbow.png", fig)

    rings = []
    for r0, n in [(1.0, 80), (4.0, 160)]:
        for i in range(n):
            a = 2 * math.pi * i / n
            rings.append((r0 * math.cos(a) + rnd.gauss(0, .15), r0 * math.sin(a) + rnd.gauss(0, .15)))
    _, groups, _ = kmeans(rings, 2, seed=2)
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    for g, col in zip(groups, [SEEBLAU, ORANGE]):
        ax.scatter([p[0] for p in g], [p[1] for p in g], s=18, color=col, alpha=.8)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("K = 2 on two rings: K-means finds the wrong groups", loc="left", color=BORDEAUX, fontsize=11)
    png("10-kmeans-rings.png", fig)


# =========================================================================
#  11  Databases
# =========================================================================
def fig_11():
    # --- join explosion -------------------------------------------------
    body = [T(20, 24, "SELECT * FROM purchase, product;   -- no WHERE, no ON", 15, fill=G5, mono=True)]
    body.append(T(20, 60, "purchase (8 rows)", 14, fill=G4))
    for i in range(8):
        body.append(R(20, 70 + i * 22, 120, 20, fill="#fff", stroke=G3, rx=3, sw=1))
        body.append(T(80, 85 + i * 22, f"purchase {i+1}", 12, "middle"))
    body.append(T(200, 60, "product (2 rows)", 14, fill=G4))
    for j, nm in enumerate(["Milk", "Tea"]):
        body.append(R(200, 70 + j * 22, 100, 20, fill="#fff", stroke=G3, rx=3, sw=1))
        body.append(T(250, 85 + j * 22, nm, 12, "middle"))
    body.append(T(380, 60, "result: every purchase paired with every product = 8 × 2 = 16 rows", 14, fill=BORDEAUX))
    k = 0
    for i in range(8):
        for j, nm in enumerate(["Milk", "Tea"]):
            x = 380 + (k // 8) * 190
            y = 70 + (k % 8) * 22
            body.append(R(x, y, 180, 20, fill="#fde2e2" if True else "#fff", stroke=G3, rx=3, sw=1))
            body.append(T(x + 90, y + 15, f"purchase {i+1}  ×  {nm}", 12, "middle"))
            k += 1
    body.append(T(20, 270, "with  WHERE purchase.product_id = product.id  only the 8 matching pairs survive", 14, fill=SEEGRUEN))
    body.append(T(20, 294, "a forgotten join condition on two million-row tables produces 10¹² rows", 15, fill=KARPFEN, weight="bold"))
    svg("11-join-explosion.svg", 800, 310, "\n".join(body))

    # --- LEFT JOIN and the customers with no orders -----------------------
    body = [T(20, 24, "customers", 14, fill=G4), T(300, 24, "orders", 14, fill=G4)]
    cust = [(1, "Anna"), (2, "Ben"), (3, "Cem"), (4, "Dana")]
    orders = [(10, 1), (11, 1), (12, 3)]
    for i, (cid, nm) in enumerate(cust):
        body.append(R(20, 34 + i * 26, 160, 24, fill="#fff", stroke=G3, rx=3, sw=1))
        body.append(T(30, 51 + i * 26, f"{cid}  {nm}", 13, mono=True))
    for i, (oid, cid) in enumerate(orders):
        body.append(R(300, 34 + i * 26, 170, 24, fill="#fff", stroke=G3, rx=3, sw=1))
        body.append(T(310, 51 + i * 26, f"{oid}  customer {cid}", 13, mono=True))
    body.append(T(20, 165, "INNER JOIN", 14, fill=BORDEAUX, weight="bold"))
    inner = [("Anna", 10), ("Anna", 11), ("Cem", 12)]
    for i, (nm, oid) in enumerate(inner):
        body.append(R(20, 175 + i * 26, 200, 24, fill="#fff", stroke=G3, rx=3, sw=1))
        body.append(T(30, 192 + i * 26, f"{nm}   order {oid}", 13, mono=True))
    body.append(T(20, 268, "Ben and Dana are gone: the rows we wanted", 13, fill=BORDEAUX))
    body.append(T(300, 165, "LEFT JOIN", 14, fill=SEEGRUEN, weight="bold"))
    left = [("Anna", "10"), ("Anna", "11"), ("Ben", "NULL"), ("Cem", "12"), ("Dana", "NULL")]
    for i, (nm, oid) in enumerate(left):
        fill = "#e0f3ec" if oid == "NULL" else "#fff"
        body.append(R(300, 175 + i * 26, 200, 24, fill=fill, stroke=G3, rx=3, sw=1))
        body.append(T(310, 192 + i * 26, f"{nm}   order {oid}", 13, mono=True))
    body.append(T(560, 190, "… WHERE orders.id IS NULL", 14, fill=SEEGRUEN, mono=True))
    body.append(T(560, 214, "→ exactly the customers who never ordered", 13, fill=G4))
    svg("11-left-join-null.svg", 900, 320, "\n".join(body))


# =========================================================================
#  12  Parallel programming
# =========================================================================
def fig_12():
    # --- race condition timeline ----------------------------------------
    body = [T(20, 24, "two threads, both running:   counter ← counter + 1   (really: read, add, write)", 15, fill=G4)]
    rows = [("thread A", "read 41", "", "add 1 → 42", "", "write 42", ""),
            ("thread B", "", "read 41", "", "add 1 → 42", "", "write 42")]
    for r, row in enumerate(rows):
        y = 60 + r * 60
        body.append(T(20, y + 22, row[0], 15, fill=G5, weight="bold"))
        for c, txt in enumerate(row[1:]):
            x = 120 + c * 125
            if txt:
                bad = txt.startswith("write") and c == 5
                body.append(R(x, y, 115, 34, fill="#fde2e2" if "write" in txt else "#fff", stroke=BORDEAUX if "write" in txt else G3, rx=5))
                body.append(T(x + 57, y + 23, txt, 13, "middle", mono=True))
    body.append(L(120, 185, 870, 185, stroke=G4, sw=1.5, arrow=True))
    body.append(T(495, 205, "time →", 13, "middle", G4))
    body.append(T(20, 240, "two increments happened, the counter went from 41 to 42: one update is lost", 15, fill=BORDEAUX, weight="bold"))
    body.append(T(20, 264, "neither thread has a bug: the bug is in the interleaving, which no single program shows", 14, fill=G4))
    svg("12-race-condition.svg", 900, 280, "\n".join(body))

    # --- SIMD lanes vs a single core ------------------------------------
    body = [T(20, 24, "CPU core: one instruction, one number at a time, but any instruction, any branch", 15, fill=G4)]
    body.append(R(20, 36, 70, 44, fill=SEEBLAU2, stroke=SEEBLAU, rx=5))
    body.append(T(55, 63, "×", 22, "middle"))
    body.append(T(110, 63, "3–5 GHz, deep pipeline, branch prediction, big cache", 14, fill=G4))
    body.append(T(20, 120, "GPU: one instruction applied to thousands of numbers at once, provided they all do the same thing", 15, fill=G4))
    for i in range(24):
        body.append(R(20 + i * 36, 132, 30, 30, fill="#e0f3ec", stroke=SEEGRUEN, rx=3, sw=1))
        body.append(T(35 + i * 36, 153, "×", 16, "middle", SEEGRUEN))
    body.append(T(20 + 24 * 36 + 8, 153, "… × thousands", 14, fill=G4))
    body.append(T(20, 200, "matrix multiply: every cell does the same multiply-add  →  GPU wins by 50×", 15, fill=SEEGRUEN, weight="bold"))
    body.append(T(20, 226, "a loop with an if inside: lanes that take the other branch sit idle  →  GPU can lose by 10×", 15, fill=BORDEAUX, weight="bold"))
    svg("12-simd-vs-cpu.svg", 940, 245, "\n".join(body))

    # --- MapReduce word count ------------------------------------------
    body = [T(20, 24, "Map: each machine counts its own chunk", 14, fill=G4),
            T(340, 24, "Shuffle: same word → same reducer", 14, fill=G4),
            T(660, 24, "Reduce: add the partial counts", 14, fill=G4)]
    chunks = [["the: 3", "vote: 1"], ["the: 2", "party: 2"], ["vote: 2", "party: 1"]]
    for i, ch in enumerate(chunks):
        y = 40 + i * 70
        body.append(R(20, y, 90, 56, fill=SEEBLAU2, stroke=SEEBLAU, rx=6))
        body.append(T(65, y + 33, f"chunk {i+1}", 14, "middle"))
        for j, kv in enumerate(ch):
            body.append(R(130, y + 4 + j * 26, 100, 22, fill="#fff", stroke=G3, rx=3, sw=1))
            body.append(T(180, y + 20 + j * 26, kv, 13, "middle", mono=True))
    reducers = {"the": (670, 50), "vote": (670, 120), "party": (670, 190)}
    src = {"the": [(1, 0), (2, 0)], "vote": [(1, 1), (3, 0)], "party": [(2, 1), (3, 1)]}
    for w, (rx, ry) in reducers.items():
        for (ci, j) in src[w]:
            y = 40 + (ci - 1) * 70 + 15 + j * 26
            body.append(f'<path d="M232,{y} C400,{y} 500,{ry+12} {rx-4},{ry+12}" fill="none" stroke="{G3}" stroke-width="1.5" marker-end="url(#ar)"/>')
        body.append(R(rx, ry, 90, 26, fill="#fff", stroke=G5, rx=4))
        body.append(T(rx + 45, ry + 18, w, 14, "middle", mono=True))
    totals = {"the": "3 + 2 = 5", "vote": "1 + 2 = 3", "party": "2 + 1 = 3"}
    for w, (rx, ry) in reducers.items():
        body.append(T(rx + 110, ry + 18, totals[w], 14, fill=SEEGRUEN, mono=True))
    body.append(T(20, 265, "only the small (word, count) pairs cross the network: the text never moves", 15, fill=KARPFEN, weight="bold"))
    svg("12-mapreduce.svg", 900, 280, "\n".join(body))


# =========================================================================
#  13  Social science applications
# =========================================================================
def fig_13():
    # --- Schelling, simulated ------------------------------------------
    N, F, empty = 40, 0.3, 0.10
    rnd = random.Random(11)
    cells = ["R"] * int(N * N * (1 - empty) / 2) + ["B"] * int(N * N * (1 - empty) / 2)
    cells += ["."] * (N * N - len(cells))
    rnd.shuffle(cells)
    grid = [cells[i * N:(i + 1) * N] for i in range(N)]

    def frac_same(g, r, c):
        me = g[r][c]; same = occ = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == dc == 0: continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < N and 0 <= cc < N and g[rr][cc] != ".":
                    occ += 1
                    same += g[rr][cc] == me
        return same / occ if occ else 1.0

    def segregation(g):
        vals = [frac_same(g, r, c) for r in range(N) for c in range(N) if g[r][c] != "."]
        return sum(vals) / len(vals)

    before = [row[:] for row in grid]
    seg0 = segregation(grid)
    moves = 0
    for step in range(60):
        unsat = [(r, c) for r in range(N) for c in range(N) if grid[r][c] != "." and frac_same(grid, r, c) < F]
        if not unsat:
            break
        rnd.shuffle(unsat)
        empties = [(r, c) for r in range(N) for c in range(N) if grid[r][c] == "."]
        for r, c in unsat:
            rnd.shuffle(empties)
            for k, (er, ec) in enumerate(empties):
                kind = grid[r][c]
                grid[er][ec] = kind
                if frac_same(grid, er, ec) >= F:
                    grid[r][c] = "."
                    empties[k] = (r, c)
                    moves += 1
                    break
                grid[er][ec] = "."
    seg1 = segregation(grid)
    print(f"   Schelling F={F}: mean same-kind share {seg0:.2f} → {seg1:.2f} after {step} rounds, {moves} moves")

    def draw(g, name, title):
        cs = 12
        out = [T(4, 16, title, 14, fill=G5, weight="bold")]
        for r in range(N):
            for c in range(N):
                col = {"R": "#d7301f", "B": "#2166ac", ".": "#fff"}[g[r][c]]
                out.append(f'<rect x="{c*cs}" y="{24 + r*cs}" width="{cs}" height="{cs}" fill="{col}" stroke="#fff" stroke-width="0.5"/>')
        svg(name, N * cs, 24 + N * cs, "\n".join(out))
    draw(before, "13-schelling-before.svg", f"random start · like-me neighbours: {seg0:.0%}")
    draw(grid, "13-schelling-after.svg", f"F = {F}: everyone wants ≥ 30% like them · result: {seg1:.0%}")

    # --- Likes vs human judges (Youyou et al. 2015) ------------------------
    fig, ax = plt.subplots(figsize=(7.5, 4))
    anchors = [(10, "work colleague"), (70, "friend or flatmate"), (150, "family member"), (300, "spouse")]
    xs = [1, 3, 10, 30, 70, 100, 150, 200, 300, 500]
    # schematic accuracy curve (self-other agreement), rising with the log of likes
    ys = [0.15 + 0.16 * math.log10(x) for x in xs]
    ax.plot(xs, ys, "-", color=SEEBLAU, lw=2.5, label="computer, from Likes (schematic)")
    for n, who in anchors:
        y = 0.15 + 0.16 * math.log10(n)
        ax.plot([n], [y], "o", color=KARPFEN)
        ax.annotate(f"{who}\n({n} Likes)", (n, y), textcoords="offset points", xytext=(6, -28), fontsize=10, color=G5)
    ax.set_xscale("log"); ax.set_xlabel("number of Facebook Likes available (log scale)")
    ax.set_ylabel("agreement with self-reported\npersonality (r)"); ax.set_ylim(0, .7)
    ax.set_title("How many Likes to beat a human judge", loc="left", color=G5)
    ax.grid(alpha=.3, which="both")
    png("13-likes-accuracy.png", fig)

    # --- Literary Digest 1936 ------------------------------------------
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1.45, 1]})
    ax = axs[0]
    labels = ["Literary Digest\n2.4 million\nballots", "Gallup\n~50 000\ninterviews", "Election\nresult"]
    roosevelt = [43, 56, 60.8]
    ax.bar(labels, roosevelt, color=[BORDEAUX, SEEBLAU, G5])
    for i, v in enumerate(roosevelt):
        ax.text(i, v + 1.5, f"{v:g}%", ha="center", color=G5, fontsize=13, fontweight="bold")
    ax.set_ylim(0, 75); ax.set_ylabel("Roosevelt's share, predicted / actual")
    ax.set_title("1936 US presidential election", loc="left", color=G5)
    ax = axs[1]
    ax.bar(["Literary Digest", "Gallup"], [2_400_000, 50_000], color=[BORDEAUX, SEEBLAU])
    ax.set_yscale("log"); ax.set_ylabel("sample size (log scale)")
    ax.text(0, 2_400_000 * 1.3, "2 400 000", ha="center", color=G5)
    ax.text(1, 50_000 * 1.3, "50 000", ha="center", color=G5)
    ax.set_ylim(1e3, 2e7)
    ax.set_title("48× larger, and wrong by 18 points", loc="left", color=BORDEAUX, fontsize=11)
    png("13-literary-digest.png", fig)


if __name__ == "__main__":
    if "--crop" in sys.argv:            # crop the existing SVGs only, without recomputing any figure
        import glob
        for f in sorted(glob.glob(os.path.join(EXDIR, "*-Examples", "figures", "*.svg"))):
            crop(f)
            print("  cropped", os.path.basename(f))
        sys.exit()
    for f in (fig_02, fig_03, fig_04, fig_05, fig_06, fig_07, fig_08, fig_09, fig_10, fig_11, fig_12, fig_13):
        print(f.__name__)
        f()
