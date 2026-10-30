#!/usr/bin/env python3
"""Figures of ICSS session 4 (Software), written into Slides/04-Software/figures/.

    python3 tools/gen04.py

Plain SVG in the style of the other session figures: Uni Konstanz colors,
Arial, rounded boxes. Figures that appear on consecutive slides (the four OOP
concepts, the two flows) share one canvas size so they do not move.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Slides", "04-Software", "figures")
os.makedirs(OUT, exist_ok=True)
FONT = 'font-family="Arial, Helvetica, sans-serif"'
MONO = 'font-family="DejaVu Sans Mono, Consolas, monospace"'
SEEBLAU, SEEBLAU1, SEEBLAU2, SEEBLAU4 = "#00a9e0", "#cceef9", "#a6e1f4", "#59c7eb"
KARPFEN, BORDEAUX, GREY, LIGHT = "#3e5496", "#8e2043", "#666666", "#f2f2f2"


def txt(x, y, t, fs=18, fill="#111", weight="normal", style="normal", anchor="middle", mono=False):
    fam = f" {MONO}" if mono else ""
    return (f'  <text x="{x}" y="{y}" font-size="{fs}" fill="{fill}" font-weight="{weight}" '
            f'font-style="{style}" text-anchor="{anchor}"{fam}>{t}</text>\n')


def box(x, y, w, h, fill=SEEBLAU1, stroke=SEEBLAU, sw=2.5, rx=10, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>\n')


def arrow(x1, y1, x2, y2, color=KARPFEN, sw=2.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d} '
            f'marker-end="url(#a)"/>\n')


DEFS = ('  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{KARPFEN}"/></marker></defs>\n')


def write(name, w, h, body):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>\n'
           + DEFS + "".join(body) + "</svg>\n")
    open(os.path.join(OUT, name), "w").write(svg)
    print(f"  {name:32} {w} x {h}")


# ============================================================ software engineering flow
STAGES = [
    ("Requirements", ["what problem,", "for whom"]),
    ("Specification", ["what the program", "must do, exactly"]),
    ("Design", ["how to split it", "into parts"]),
    ("Implementation", ["write the", "code"]),
    ("Testing", ["check it does", "what was specified"]),
    ("Maintenance", ["use, fix, extend,", "hand over"]),
]
BW, BH, GAP, Y0, X0 = 168, 104, 34, 50, 6
FLOW_W = X0 + 6 * BW + 5 * GAP + X0           # the whole last box fits on the canvas


def flow(name, vibe=False):
    body = []
    xs = [X0 + i * (BW + GAP) for i in range(len(STAGES))]
    who = {"Requirements": "you and your client", "Specification": "you", "Design": "you",
           "Implementation": "the LLM", "Testing": "you", "Maintenance": "you"}
    for i, (stage, desc) in enumerate(STAGES):
        x = xs[i]
        fill, stroke, dash = SEEBLAU1, SEEBLAU, ""
        if vibe and stage == "Implementation":
            fill, stroke, dash = "#ffffff", GREY, "7 5"
        elif vibe:
            fill, stroke = SEEBLAU2, KARPFEN
        body.append(box(x, Y0, BW, BH, fill, stroke, dash=dash))
        body.append(txt(x + BW / 2, Y0 + 34, stage, 21, weight="bold"))
        for k, line in enumerate(desc):
            body.append(txt(x + BW / 2, Y0 + 64 + k * 22, line, 17, fill="#444"))
        if i < len(STAGES) - 1:
            body.append(arrow(x + BW + 3, Y0 + BH / 2, x + BW + GAP - 3, Y0 + BH / 2))
        if vibe:
            col = GREY if stage == "Implementation" else KARPFEN
            body.append(txt(x + BW / 2, Y0 - 16, who[stage], 19, fill=col, weight="bold"))

    def back(i_from, i_to, depth, label):
        x1, x2 = xs[i_from] + BW / 2, xs[i_to] + BW / 2
        yb, yl = Y0 + BH + 3, Y0 + BH + depth
        body.append(f'  <path d="M {x1} {yb} V {yl} H {x2} V {yb + 3}" fill="none" stroke="{KARPFEN}" '
                    f'stroke-width="2" stroke-dasharray="6 5" marker-end="url(#a)"/>\n')
        body.append(txt((x1 + x2) / 2, yl + 20, label, 16, fill=KARPFEN, style="italic"))

    back(4, 3, 26, "a test fails: fix the code")
    back(4, 1, 74, "the specification was wrong or incomplete")
    back(5, 0, 122, "new needs, new data")
    write(name, FLOW_W, Y0 + BH + 122 + 30, body)


# ============================================================ interpreter and compiler
PW, PH = 560, 196          # both diagrams share this canvas, one per column


def code_lines(x, y, lines, w=150):
    out = [box(x, y, w, 30 + 28 * len(lines), fill="#ffffff", stroke=GREY, sw=1.6, rx=6)]
    for k, l in enumerate(lines):
        out.append(txt(x + 12, y + 30 + 28 * k, l, 19, anchor="start", mono=True))
    return out


def interpreter():
    body = [txt(10, 22, "source code", 19, fill=GREY, anchor="start")]
    body += code_lines(6, 32, ["x = 3", "y = x * 2", "print(y)"], w=150)
    body.append(box(208, 40, 190, 96, fill=SEEBLAU2, stroke=KARPFEN))
    body.append(txt(303, 76, "Interpreter", 23, weight="bold"))
    body.append(txt(303, 106, "one line: translate,", 17, fill="#333"))
    body.append(txt(303, 126, "run, next line", 17, fill="#333"))
    body.append(arrow(160, 88, 204, 88))
    body.append(f'  <path d="M 356 138 C 356 178, 250 178, 250 140" fill="none" stroke="{KARPFEN}" '
                f'stroke-width="2.4" marker-end="url(#a)"/>\n')
    body.append(txt(303, 190, "on every run", 17, fill=KARPFEN, style="italic"))
    body.append(box(444, 58, 110, 62, fill="#ffffff", stroke=GREY, sw=1.6, rx=6))
    body.append(txt(499, 84, "output", 18, fill=GREY))
    body.append(txt(499, 110, "6", 21, mono=True))
    body.append(arrow(400, 88, 440, 88))
    write("04-interpreter.svg", PW, PH, body)


def compiler():
    body = [txt(10, 22, "source code", 19, fill=GREY, anchor="start")]
    body += code_lines(6, 32, ["x = 3", "y = x * 2", "print(y)"], w=150)
    body.append(box(196, 40, 128, 96, fill=SEEBLAU2, stroke=KARPFEN))
    body.append(txt(260, 80, "Compiler", 22, weight="bold"))
    body.append(txt(260, 108, "once, the", 17, fill="#333"))
    body.append(txt(260, 128, "whole program", 17, fill="#333"))
    body.append(arrow(160, 88, 192, 88))
    body.append(box(358, 40, 96, 96, fill=LIGHT, stroke=GREY, sw=1.6, rx=6))
    for k, l in enumerate(["0100", "1101", "0011"]):
        body.append(txt(406, 70 + 26 * k, l, 18, mono=True))
    body.append(txt(406, 162, "machine code", 17, fill=GREY))
    body.append(arrow(326, 88, 354, 88))
    body.append(box(484, 58, 72, 62, fill="#ffffff", stroke=GREY, sw=1.6, rx=6))
    body.append(txt(520, 84, "run", 18, fill=GREY))
    body.append(txt(520, 110, "6", 21, mono=True))
    body.append(arrow(456, 88, 480, 88))
    body.append(txt(406, 190, "runs many times, fast", 17, fill=KARPFEN, style="italic"))
    write("04-compiler.svg", PW, PH, body)


# ============================================================ class and objects
def class_box(x, y, w, title, attrs, methods, fill=SEEBLAU1, stroke=SEEBLAU, mono_vals=True):
    h_title, line = 40, 26
    h = h_title + 14 + line * len(attrs) + 14 + line * len(methods) + 8
    out = [box(x, y, w, h, fill=fill, stroke=stroke)]
    out.append(txt(x + w / 2, y + 27, title, 19, weight="bold"))
    yy = y + h_title
    out.append(f'  <line x1="{x}" y1="{yy}" x2="{x + w}" y2="{yy}" stroke="{stroke}" stroke-width="1.5"/>\n')
    for k, a in enumerate(attrs):
        out.append(txt(x + 14, yy + 24 + line * k, a, 16, anchor="start", mono=mono_vals))
    yy2 = yy + 14 + line * len(attrs)
    if methods:
        out.append(f'  <line x1="{x}" y1="{yy2}" x2="{x + w}" y2="{yy2}" stroke="{stroke}" stroke-width="1.5"/>\n')
        for k, m in enumerate(methods):
            out.append(txt(x + 14, yy2 + 24 + line * k, m, 16, anchor="start", mono=True, fill=KARPFEN))
    return out, h


def class_objects():
    body = []
    b, h = class_box(20, 40, 300, "class Respondent", ["name", "age"], ["is_adult()", "describe()"],
                     fill=SEEBLAU2, stroke=KARPFEN)
    body += b
    body.append(txt(170, 24, "the blueprint", 16, fill=KARPFEN, style="italic"))
    body.append(txt(26, 40 + h + 26, "attributes: the data · methods: what it can do", 15, fill="#333", anchor="start"))
    for k, (nm, name, age) in enumerate([("ana", '"Ana"', "34"), ("ben", '"Ben"', "16")]):
        y = 30 + k * 130
        ob, oh = class_box(520, y, 280, f"{nm}: a Respondent", [f"name = {name}", f"age = {age}"], [])
        body += ob
        body.append(arrow(512, y + oh / 2, 326, 100 + (k - 0.5) * 50, dash="6 5"))
    body.append(txt(420, 134, "instance of", 15, fill=KARPFEN, style="italic"))
    body.append(txt(660, 320, "the objects: each has its own data", 16, fill=KARPFEN, style="italic"))
    write("04-class-objects.svg", 820, 332, body)


# ============================================================ the four OOP concepts
CW, CH = 600, 344          # one canvas for all four, so the diagram stays in place


def encapsulation():
    body = [f'  <rect x="40" y="30" width="520" height="210" rx="105" fill="{SEEBLAU1}" stroke="{KARPFEN}" stroke-width="2.5"/>\n',
            txt(300, 62, "object ana", 22, weight="bold")]
    body.append(box(110, 84, 170, 110, fill="#ffffff", stroke=SEEBLAU, sw=2))
    body.append(txt(195, 112, "data", 19, fill=GREY))
    body.append(txt(195, 142, 'name = "Ana"', 19, mono=True))
    body.append(txt(195, 168, "age = 34", 19, mono=True))
    body.append(box(320, 84, 170, 110, fill="#ffffff", stroke=SEEBLAU, sw=2))
    body.append(txt(405, 112, "methods", 19, fill=GREY))
    body.append(txt(405, 142, "is_adult()", 19, mono=True, fill=KARPFEN))
    body.append(txt(405, 168, "describe()", 19, mono=True, fill=KARPFEN))
    body.append(arrow(318, 150, 284, 150))
    body.append(txt(40, 274, "data and the code that uses it,", 18, fill=KARPFEN, style="italic", anchor="start"))
    body.append(txt(40, 296, "in one place", 18, fill=KARPFEN, style="italic", anchor="start"))
    body.append(arrow(405, 296, 405, 198))
    body.append(txt(405, 316, "ana.is_adult()", 20, mono=True))
    write("04-oop-encapsulation.svg", CW, CH, body)


def abstraction():
    body = [box(126, 30, 348, 210, fill=SEEBLAU1, stroke=KARPFEN),
            txt(300, 62, 'a str object: "Konstanz"', 21, weight="bold")]
    body.append(box(190, 84, 220, 96, fill="#d9d9d9", stroke=GREY, sw=1.5, rx=6))
    body.append(txt(300, 124, "how the text", 19, fill="#555"))
    body.append(txt(300, 146, "is stored: hidden", 19, fill="#555"))
    for k, m in enumerate(["upper()", "count()", "replace()"]):
        x = 134 + k * 112
        body.append(box(x, 200, 108, 32, fill="#ffffff", stroke=KARPFEN, sw=1.8, rx=6))
        body.append(txt(x + 54, 222, m, 17, mono=True, fill=KARPFEN))
    body.append(txt(250, 274, "you use the methods it offers,", 18, fill=KARPFEN, style="italic", anchor="start"))
    body.append(txt(250, 296, "not what is inside", 18, fill=KARPFEN, style="italic", anchor="start"))
    body.append(arrow(205, 316, 205, 234))
    body.append(txt(205, 326, "s.upper()", 18, mono=True, anchor="end"))
    write("04-oop-abstraction.svg", CW, CH, body)


def inheritance():
    body = []
    b, h = class_box(170, 4, 260, "Respondent", ["name", "age"], ["is_adult()", "describe()"])
    body += b
    b2, h2 = class_box(170, 238, 260, "Student", ["program"], [], fill=SEEBLAU2, stroke=KARPFEN)
    body += b2
    body.append(arrow(300, 236, 300, 4 + h + 4))
    body.append(txt(312, 220, "is a", 19, fill=KARPFEN, style="italic", anchor="start"))
    body.append(txt(450, 268, "+ everything", 18, fill=KARPFEN, style="italic", anchor="start"))
    body.append(txt(450, 290, "a Respondent has", 18, fill=KARPFEN, style="italic", anchor="start"))
    write("04-oop-inheritance.svg", CW, CH, body)


def polymorphism():
    body = [box(210, 20, 180, 50, fill=SEEBLAU2, stroke=KARPFEN),
            txt(300, 52, "len(x)", 23, mono=True, weight="bold")]
    cases = [('"data"', "str", "4"), ("[3, 1, 2]", "list", "3"), ('{"yes": 12, "no": 7}', "dict", "2")]
    for k, (val, cls, res) in enumerate(cases):
        x = 20 + k * 196
        body.append(arrow(300, 72, x + 88, 128))
        body.append(box(x, 132, 176, 92, fill=SEEBLAU1, stroke=SEEBLAU, sw=2))
        body.append(txt(x + 88, 160, cls, 19, fill=GREY))
        body.append(txt(x + 88, 188, val, 14 if len(val) > 12 else 18, mono=True))
        body.append(txt(x + 88, 214, f"→ {res}", 20, mono=True, fill=KARPFEN, weight="bold"))
    body.append(txt(300, 262, "one name, the right operation for each class:", 18, fill=KARPFEN, style="italic"))
    body.append(txt(300, 284, "characters, elements, keys", 18, fill=KARPFEN, style="italic"))
    write("04-oop-polymorphism.svg", CW, CH, body)


# ============================================================ from a script to software
def script_to_software():
    body = []
    # the script: one page
    body.append(f'  <path d="M 30 20 H 170 L 204 54 V 230 H 30 Z" fill="#ffffff" stroke="{GREY}" stroke-width="2"/>\n')
    for k in range(6):
        body.append(f'  <line x1="50" y1="{80 + 24 * k}" x2="{176 - (k % 3) * 20}" y2="{80 + 24 * k}" '
                    f'stroke="#bbbbbb" stroke-width="6"/>\n')
    body.append(txt(112, 48, "analysis.py", 18, mono=True))
    body.append(txt(117, 264, "a script:", 21, weight="bold"))
    body.append(txt(117, 292, "one file, one person,", 18, fill="#444"))
    body.append(txt(117, 316, "run once", 18, fill="#444"))
    body.append(arrow(226, 130, 318, 130, sw=3))
    body.append(txt(272, 114, "grows into", 18, fill=KARPFEN, style="italic"))
    parts = [("requirements", 340, 10), ("tests", 660, 10), ("documentation", 340, 196),
             ("versions", 660, 196), ("users and data", 500, 252)]
    cx0, cy0 = 590, 130
    for name, x, y in parts:                      # connectors first, so the boxes cover them
        w = 190
        body.append(f'  <line x1="{x + w / 2}" y1="{y + 26}" x2="{cx0}" y2="{cy0}" stroke="{SEEBLAU}" '
                    f'stroke-width="1.8" stroke-dasharray="5 5"/>\n')
    body.append(box(500, 88, 180, 84, fill=SEEBLAU2, stroke=KARPFEN))
    body.append(txt(590, 124, "code in", 21, weight="bold"))
    body.append(txt(590, 150, "small parts", 21, weight="bold"))
    for name, x, y in parts:
        w = 190
        body.append(box(x, y, w, 52, fill=SEEBLAU1, stroke=SEEBLAU, sw=2))
        body.append(txt(x + w / 2, y + 33, name, 19))
    body.append(txt(595, 340, "software: many parts, many people, many years", 19, fill="#444"))
    write("04-script-to-software.svg", 860, 352, body)


# ============================================================ design: small parts with specifications
def design_pipeline():
    steps = [("load_responses(path)", "read the file into a", "list of dicts"),
             ("clean_ages(rows)", "turn text into int,", "blank into None"),
             ("mean_age(ages)", "mean of the ages", "that were answered"),
             ("report(mean, n)", "one line of text", "for the report")]
    data = ["list of dicts", "list of int / None", "float"]
    bw, gap, y = 260, 50, 30
    body = []
    for k, (fn, a, b) in enumerate(steps):
        x = 6 + k * (bw + gap)
        hl = fn.startswith("mean_age")
        body.append(box(x, y, bw, 120, fill=SEEBLAU2 if hl else SEEBLAU1, stroke=KARPFEN if hl else SEEBLAU))
        body.append(txt(x + bw / 2, y + 34, fn, 18, mono=True, weight="bold"))
        body.append(txt(x + bw / 2, y + 70, a, 19, fill="#444"))
        body.append(txt(x + bw / 2, y + 96, b, 19, fill="#444"))
        if k < len(steps) - 1:
            body.append(arrow(x + bw + 3, y + 60, x + bw + gap - 3, y + 60))
            body.append(txt(x + bw + gap / 2, y + 152, data[k], 18, fill=KARPFEN, style="italic"))
    body.append(txt(6 + 2 * (bw + gap) + bw / 2, y + 186, "specified and tested in the next sections", 18,
                    fill=KARPFEN, style="italic"))
    write("04-design-pipeline.svg", 6 + 4 * bw + 3 * gap + 6, 226, body)


if __name__ == "__main__":
    flow("04-se-flow.svg")
    flow("04-se-flow-vibe.svg", vibe=True)
    interpreter()
    compiler()
    class_objects()
    encapsulation()
    abstraction()
    inheritance()
    polymorphism()
    script_to_software()
    design_pipeline()
