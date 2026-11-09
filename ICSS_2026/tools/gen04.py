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
    who = {"Requirements": "you: analyst", "Specification": "you: analyst", "Design": "you: architect",
           "Implementation": "coding agent", "Testing": "you: tester", "Maintenance": "you: maintainer"}
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


def class_objects(name="04-class-objects.svg", cls="Respondent", attrs=("name", "age"),
                  methods=("is_adult()", "describe()"), objects=(("ana", '"Ana"', "34"), ("ben", '"Ben"', "16")),
                  fields=("name", "age"), sep=" = "):
    """A class on the left and two of its objects on the right; the same layout for every class."""
    body = []
    b, h = class_box(20, 40, 300, f"class {cls}", list(attrs), list(methods), fill=SEEBLAU2, stroke=KARPFEN)
    body += b
    body.append(txt(170, 24, "the blueprint", 16, fill=KARPFEN, style="italic"))
    body.append(txt(26, 40 + h + 26, "attributes: the data · methods: what it can do", 15, fill="#333", anchor="start"))
    for k, (nm, v1, v2) in enumerate(objects):
        y = 30 + k * 130
        ob, oh = class_box(520, y, 280, f"{nm}: a {cls}", [f"{fields[0]}{sep}{v1}", f"{fields[1]}{sep}{v2}"], [])
        body += ob
        body.append(arrow(512, y + oh / 2, 326, 100 + (k - 0.5) * 50, dash="6 5"))
    body.append(txt(420, 134, "instance of", 15, fill=KARPFEN, style="italic"))
    body.append(txt(660, 320, "the objects: each has its own data", 16, fill=KARPFEN, style="italic"))
    write(name, 820, 332, body)


def dict_objects():
    """A dict as an object, in the layout of class_objects: its data are key-value pairs."""
    class_objects("04-dict-objects.svg", cls="dict", attrs=("keys", "values"),
                  methods=("get(key, default)", "keys()"),
                  objects=(("votes", '"yes" \u2192 12', '"no" \u2192 7'), ("ages", '"Ana" \u2192 34', '"Ben" \u2192 16')),
                  fields=("", ""), sep="")


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
    body = [box(190, 14, 220, 50, fill=SEEBLAU2, stroke=KARPFEN),
            txt(300, 47, "p.describe()", 23, mono=True, weight="bold")]
    cases = [("ana", "Respondent", "'Ana, 34 years'"), ("bea", "Student", "'Bea: SEDS'")]
    for k, (obj, cls, res) in enumerate(cases):
        x = 30 + k * 290
        body.append(arrow(300, 66, x + 125, 118))
        body.append(box(x, 122, 250, 108, fill=SEEBLAU1, stroke=SEEBLAU, sw=2))
        body.append(txt(x + 125, 152, f"{obj}: a {cls}", 19, weight="bold"))
        body.append(txt(x + 125, 182, f"{cls}.describe()", 16, mono=True, fill=GREY))
        body.append(txt(x + 125, 212, f"\u2192 {res}", 17, mono=True, fill=KARPFEN, weight="bold"))
    body.append(txt(300, 266, "the same call; each object runs", 18, fill=KARPFEN, style="italic"))
    body.append(txt(300, 288, "the method of its own class", 18, fill=KARPFEN, style="italic"))
    write("04-oop-polymorphism.svg", CW, CH, body)


# ============================================================ why OOP: one class per responsibility
def oop_team():
    people = [("Lea", "class Survey", ["load()", "questions()"]),
              ("Tom", "class Respondent", ["is_adult()", "describe()"]),
              ("Ana", "class Report", ["table()", "save()"])]
    bw, gap, y = 300, 70, 52
    body = []
    for k, (who, cls, methods) in enumerate(people):
        x = 10 + k * (bw + gap)
        body.append(f'  <circle cx="{x + bw / 2}" cy="22" r="14" fill="{SEEBLAU4}"/>\n')
        body.append(txt(x + bw / 2 + 24, 29, f"{who} maintains", 17, fill="#333", anchor="start"))
        body.append(box(x, y, bw, 150, fill=SEEBLAU2, stroke=KARPFEN))
        body.append(txt(x + bw / 2, y + 30, cls, 20, weight="bold", mono=True))
        body.append(box(x + 20, y + 44, bw - 40, 40, fill="#d9d9d9", stroke=GREY, sw=1.5, rx=6))
        body.append(txt(x + bw / 2, y + 70, "inside: free to change", 16, fill="#555"))
        for j, m in enumerate(methods):
            mx = x + 20 + j * (bw - 40) / 2
            body.append(box(mx + 4, y + 100, (bw - 40) / 2 - 8, 34, fill="#ffffff", stroke=KARPFEN, sw=1.8, rx=6))
            body.append(txt(mx + (bw - 40) / 4, y + 123, m, 16, mono=True, fill=KARPFEN))
        if k < 2:
            body.append(arrow(x + bw + 4, y + 117, x + bw + gap - 4, y + 117))
    body.append(txt(10 + 1.5 * bw + gap, y + 186, "the classes talk only through their methods", 18, fill=KARPFEN,
                    style="italic"))
    write("04-oop-team.svg", 20 + 3 * bw + 2 * gap, y + 200, body)


# ============================================================ what software is
def software():
    body = []
    body.append(box(170, 10, 620, 196, fill=SEEBLAU1, stroke=KARPFEN))
    body.append(txt(480, 42, "software", 23, weight="bold"))
    parts = [("programs", ["the code that", "runs"]), ("data", ["files, settings,", "databases"]),
             ("documentation", ["how to use", "and change it"]), ("tests", ["checks that", "it works"])]
    for k, (name, desc) in enumerate(parts):
        x = 190 + k * 148
        body.append(box(x, 60, 136, 128, fill="#ffffff", stroke=SEEBLAU, sw=2))
        body.append(txt(x + 68, 92, name, 18, weight="bold"))
        for j, d in enumerate(desc):
            body.append(txt(x + 68, 124 + 22 * j, d, 16, fill="#444"))
    body.append(box(170, 252, 620, 60, fill=LIGHT, stroke=GREY, sw=2))
    body.append(txt(480, 290, "hardware: processor, memory, disk", 19, fill="#444"))
    body.append(arrow(480, 208, 480, 248))
    body.append(txt(492, 234, "runs on", 16, fill=KARPFEN, style="italic", anchor="start"))
    body.append(f'  <circle cx="70" cy="90" r="22" fill="{SEEBLAU4}"/>\n')
    body.append(f'  <path d="M 30 160 Q 70 110 110 160 Z" fill="{SEEBLAU4}"/>\n')
    body.append(txt(70, 190, "users", 17, fill="#333"))
    body.append(arrow(118, 110, 164, 110))
    write("04-software.svg", 800, 322, body)


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
    """The panel-wave example: three steps in a row, a helper below the main one."""
    steps = [("read_wave(path)", "read one wave file", "into a list of pairs"),
             ("link_waves(w1, w2)", "pair the answers of", "the people in both waves"),
             ("report(pairs)", "how many changed", "their answer")]
    data = ["2 lists of (email, answer)", "dict: pseudonym → pair"]
    bw, gap, y = 300, 96, 20
    body = []
    xs = [6 + k * (bw + gap) for k in range(3)]
    for k, (fn, a, b) in enumerate(steps):
        x = xs[k]
        hl = k == 1
        body.append(box(x, y, bw, 120, fill=SEEBLAU2 if hl else SEEBLAU1, stroke=KARPFEN if hl else SEEBLAU))
        body.append(txt(x + bw / 2, y + 34, fn, 18, mono=True, weight="bold"))
        body.append(txt(x + bw / 2, y + 70, a, 19, fill="#444"))
        body.append(txt(x + bw / 2, y + 96, b, 19, fill="#444"))
        if k < len(steps) - 1:
            body.append(arrow(x + bw + 3, y + 60, x + bw + gap - 3, y + 60))
    # data on the arrows, below the boxes
    body.append(txt(xs[0] + bw / 2 + 40, y + 152, data[0], 18, fill=KARPFEN, style="italic"))
    body.append(txt(xs[2] + bw / 2 - 40, y + 152, data[1], 18, fill=KARPFEN, style="italic"))
    # the helper, used by link_waves
    hx, hy = xs[1] + 10, y + 196
    body.append(arrow(xs[1] + bw / 2, hy - 2, xs[1] + bw / 2, y + 123, dash="6 5"))
    body.append(txt(xs[1] + bw / 2 + 8, y + 172, "uses", 17, fill=KARPFEN, style="italic", anchor="start"))
    body.append(box(hx, hy, bw - 20, 100, fill=SEEBLAU1, stroke=SEEBLAU))
    body.append(txt(hx + (bw - 20) / 2, hy + 32, "pseudonym(email)", 18, mono=True, weight="bold"))
    body.append(txt(hx + (bw - 20) / 2, hy + 62, "clean the email, then a", 18, fill="#444"))
    body.append(txt(hx + (bw - 20) / 2, hy + 86, "hash with a secret (session 3)", 18, fill="#444"))
    body.append(txt(xs[2] + bw / 2, hy + 56, "link_waves is specified and", 18, fill=KARPFEN, style="italic"))
    body.append(txt(xs[2] + bw / 2, hy + 80, "tested in the next sections", 18, fill=KARPFEN, style="italic"))
    write("04-design-pipeline.svg", xs[2] + bw + 6, hy + 106, body)


# ============================================================ roles and the panel example
ORANGE = "#e07b00"


def person(cx, cy, s=1.0, color=SEEBLAU4):
    """A person glyph: head and shoulders, centered at (cx, cy)."""
    r, w = 13 * s, 22 * s
    return (f'  <circle cx="{cx}" cy="{cy - 14 * s}" r="{r}" fill="{color}"/>\n'
            f'  <path d="M {cx - w} {cy + 24 * s} V {cy + 18 * s} A {w} {w} 0 0 1 {cx + w} {cy + 18 * s} '
            f'V {cy + 24 * s} Z" fill="{color}"/>\n')


def agent(cx, cy, s=1.0, color=KARPFEN):
    """A coding agent glyph: a robot head with an antenna."""
    w, h = 40 * s, 30 * s
    return (f'  <line x1="{cx}" y1="{cy - h / 2 - 12 * s}" x2="{cx}" y2="{cy - h / 2}" stroke="{color}" stroke-width="{2.5 * s}"/>\n'
            f'  <circle cx="{cx}" cy="{cy - h / 2 - 14 * s}" r="{4 * s}" fill="{color}"/>\n'
            f'  <rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{7 * s}" fill="{color}"/>\n'
            f'  <circle cx="{cx - 9 * s}" cy="{cy - 2 * s}" r="{4 * s}" fill="#ffffff"/>\n'
            f'  <circle cx="{cx + 9 * s}" cy="{cy - 2 * s}" r="{4 * s}" fill="#ffffff"/>\n'
            f'  <rect x="{cx - 10 * s}" y="{cy + 7 * s}" width="{20 * s}" height="{3 * s}" fill="#ffffff"/>\n'
            f'  <rect x="{cx - w / 2 + 4 * s}" y="{cy + h / 2 + 2 * s}" width="{w - 8 * s}" height="{10 * s}" rx="{3 * s}" fill="{color}"/>\n')


def document(x, y, w, h, title, lines=3, fill="#ffffff", stroke=GREY):
    out = [f'  <path d="M {x} {y} H {x + w - 18} L {x + w} {y + 18} V {y + h} H {x} Z" fill="{fill}" '
           f'stroke="{stroke}" stroke-width="2"/>\n']
    out.append(txt(x + w / 2, y + 28, title, 17, weight="bold", mono=True))
    for k in range(lines):
        out.append(f'  <line x1="{x + 14}" y1="{y + 46 + 14 * k}" x2="{x + w - 14 - (k % 2) * 30}" '
                   f'y2="{y + 46 + 14 * k}" stroke="#c8c8c8" stroke-width="5"/>\n')
    return out


ROLES = [("Requirements", "analyst", "with the client", "requirements"),
         ("Specification", "analyst", "writes it down", "specification"),
         ("Design", "architect", "splits the work", "design"),
         ("Implementation", "coder", "human or agent", "code"),
         ("Testing", "tester", "checks the code", "test report"),
         ("Maintenance", "maintainer", "fixes, extends", "new requests")]


def roles(name="04-roles.svg"):
    """The six stages of the flow, each with the role that owns it and what it hands on."""
    body = []
    xs = [X0 + i * (BW + GAP) for i in range(len(ROLES))]
    for i, (stage, role, note, hands) in enumerate(ROLES):
        x, cx = xs[i], xs[i] + BW / 2
        body.append(box(x, 10, BW, 52, fill=SEEBLAU1, stroke=SEEBLAU))
        body.append(txt(cx, 43, stage, 19, weight="bold"))
        if i < len(ROLES) - 1:
            body.append(arrow(x + BW + 3, 36, x + BW + GAP - 3, 36))
        if role == "coder":
            body.append(person(cx - 28, 112, 1.0))
            body.append(agent(cx + 28, 114, 0.95))
        else:
            if role == "analyst" and i == 0:          # the client sits next to the analyst
                body.append(person(cx + 24, 112, 1.0))
                body.append(person(cx - 34, 118, 0.7, color="#bbbbbb"))
                body.append(txt(cx - 34, 152, "client", 14, fill=GREY))
            else:
                body.append(person(cx, 112, 1.0))
        body.append(txt(cx, 172 if role != "coder" else 172, role, 21, weight="bold", fill=KARPFEN))
        body.append(txt(cx, 196, note, 16, fill="#444", style="italic"))
        body += document(x + 20, 214, BW - 40, 74, "", lines=2)
        body.append(txt(cx, 238, hands, 16, fill="#111", weight="bold"))
        if i < len(ROLES) - 1:
            body.append(arrow(x + BW - 20 + 2, 251, xs[i + 1] + 20 - 2, 251, sw=2))
    body.append(txt(FLOW_W / 2, 318, "each role hands its result to the next one; in a small project, one person plays several roles",
                    17, fill=KARPFEN, style="italic"))
    write(name, FLOW_W, 330, body)


def table(x, y, title, header, rows, colw, hl=None, title_fill=KARPFEN):
    """A small data table. hl maps a row index to an outline color."""
    out = [txt(x + sum(colw) / 2, y - 10, title, 18, weight="bold", fill=title_fill)]
    rh = 36
    cx = x
    for w, h in zip(colw, header):
        out.append(box(cx, y, w, rh, fill=SEEBLAU2, stroke=SEEBLAU, sw=1.5, rx=0))
        out.append(txt(cx + w / 2, y + 24, h, 16, weight="bold"))
        cx += w
    for r, row in enumerate(rows):
        cx = x
        for w, v in zip(colw, row):
            out.append(box(cx, y + rh * (r + 1), w, rh, fill="#ffffff", stroke=SEEBLAU, sw=1.5, rx=0))
            out.append(txt(cx + w / 2, y + rh * (r + 1) + 24, v, 16, mono=True))
            cx += w
        if hl and r in hl:
            out.append(f'  <rect x="{x - 3}" y="{y + rh * (r + 1) - 3}" width="{sum(colw) + 6}" height="{rh + 6}" '
                       f'rx="6" fill="none" stroke="{hl[r]}" stroke-width="3"/>\n')
    return out


def panel_example():
    """The running example: two waves of a panel survey, linked without email addresses."""
    body = []
    cw = [210, 92]
    body += table(10, 40, "wave 1 (spring)", ["email", "answer"],
                  [['"ana@uni.de"', '"yes"'], ['"ben@uni.de"', '"no"']], cw, hl={0: ORANGE})
    body += table(10, 220, "wave 2 (autumn)", ["email", "answer"],
                  [['" Ana@Uni.de"', '"no"'], ['"eva@uni.de"', '"yes"']], cw, hl={0: ORANGE})
    # notes next to the waves
    body.append(txt(330, 136, "Ben: only in wave 1", 16, fill=GREY, anchor="start", style="italic"))
    body.append(txt(330, 316, "Eva: only in wave 2", 16, fill=GREY, anchor="start", style="italic"))
    body.append(txt(330, 266, "the same person as", 16, fill=ORANGE, anchor="start", weight="bold"))
    body.append(txt(330, 286, "ana@uni.de?", 16, fill=ORANGE, anchor="start", weight="bold", mono=True))
    # the linking step
    bx, by = 600, 140
    body.append(box(bx, by, 220, 92, fill=SEEBLAU2, stroke=KARPFEN))
    body.append(txt(bx + 110, by + 38, "link_waves", 20, weight="bold", mono=True))
    body.append(txt(bx + 110, by + 66, "pair the answers", 16, fill="#444"))
    body.append(arrow(318, 58, bx - 4, by + 26))
    body.append(arrow(318, 238, bx - 4, by + 66))
    body.append(arrow(bx + 224, by + 46, 874, by + 46))
    body += table(880, 150, "linked, to share", ["pseudonym", "spring", "autumn"],
                  [['"3f9a1c07e2"', '"yes"', '"no"']], [138, 84, 84])
    body.append(txt(880 + 153, 262, "one row per person in both waves,", 16, fill=KARPFEN, style="italic"))
    body.append(txt(880 + 153, 284, "no email addresses", 16, fill=KARPFEN, style="italic", weight="bold"))
    write("04-panel-example.svg", 1196, 336, body)


def any_coder():
    """One specification, two coders, the same tests."""
    body = []
    body += document(10, 92, 200, 150, "link_waves", lines=6, fill=SEEBLAU1, stroke=KARPFEN)
    body.append(txt(110, 270, "the specification", 18, weight="bold", fill=KARPFEN))
    body.append(txt(110, 292, "(analyst)", 16, fill="#444", style="italic"))
    # two coders
    for k, (label, glyph) in enumerate([("a colleague", "person"), ("a coding agent", "agent")]):
        y = 70 + k * 170
        cx = 340
        body.append(arrow(214, 167, cx - 50, y + 20))
        body.append(person(cx, y + 18, 1.2) if glyph == "person" else agent(cx, y + 18, 1.15))
        body.append(txt(cx, y + 74, label, 18, weight="bold", fill=KARPFEN))
        body.append(arrow(cx + 52, y + 18, 470, y + 18))
        body += document(476, y - 26, 150, 90, "panel.py", lines=2)
        body.append(arrow(630, y + 18, 726, 167 + (k * 2 - 1) * 26))
    # tests
    body.append(box(732, 92, 196, 150, fill=SEEBLAU2, stroke=KARPFEN))
    body.append(txt(830, 128, "the tests", 20, weight="bold"))
    body.append(txt(830, 156, "written by the tester", 16, fill="#444"))
    body.append(txt(830, 178, "from the specification,", 16, fill="#444"))
    body.append(txt(830, 200, "before the code", 16, fill="#444"))
    body.append(arrow(932, 140, 990, 112))
    body.append(arrow(932, 196, 990, 226))
    body.append(txt(998, 118, "pass", 19, weight="bold", fill=KARPFEN, anchor="start"))
    body.append(txt(998, 222, "fail: back", 19, weight="bold", fill=ORANGE, anchor="start"))
    body.append(txt(998, 244, "to the coder", 19, weight="bold", fill=ORANGE, anchor="start"))
    write("04-any-coder.svg", 1140, 326, body)


def test_first():
    """The order of work, with the role that does each step."""
    steps = [("1", "analyst", "specification", "the docstring"),
             ("2", "tester", "tests", "from the specification"),
             ("3", "coder", "implementation", "human or agent"),
             ("4", "tester", "run the tests", "read what passes"),
             ("5", "maintainer", "bug found later", "becomes a new test")]
    bw, gap, y = 196, 34, 70
    body = []
    xs = [6 + k * (bw + gap) for k in range(5)]
    for k, (n, role, what, note) in enumerate(steps):
        x, cx = xs[k], xs[k] + bw / 2
        if role == "coder":
            body.append(person(cx - 26, 30, 0.85))
            body.append(agent(cx + 26, 32, 0.8))
        else:
            body.append(person(cx, 30, 0.85))
        hl = role == "tester"
        body.append(box(x, y, bw, 108, fill=SEEBLAU2 if hl else SEEBLAU1, stroke=KARPFEN if hl else SEEBLAU))
        body.append(txt(cx, y + 30, f"{n}. {role}", 19, weight="bold", fill=KARPFEN))
        body.append(txt(cx, y + 62, what, 18, weight="bold"))
        body.append(txt(cx, y + 88, note, 16, fill="#444", style="italic"))
        if k < 4:
            body.append(arrow(x + bw + 3, y + 54, x + bw + gap - 3, y + 54))

    def back(i_from, i_to, depth, label, color):
        x1, x2 = xs[i_from] + bw / 2, xs[i_to] + bw / 2
        yb, yl = y + 108 + 3, y + 108 + depth
        body.append(f'  <path d="M {x1} {yb} V {yl} H {x2} V {yb + 3}" fill="none" stroke="{color}" '
                    f'stroke-width="2.2" stroke-dasharray="6 5" marker-end="url(#a)"/>\n')
        body.append(txt((x1 + x2) / 2, yl + 20, label, 16, fill=color, style="italic"))

    back(3, 2, 26, "a test fails: back to the coder", ORANGE)
    back(4, 1, 74, "regression test: the bug can never come back unnoticed", KARPFEN)
    write("04-test-first.svg", xs[4] + bw + 6, y + 108 + 74 + 32, body)


def maintenance():
    """The design of the example after the client asks for a third wave."""
    steps = [("read_wave(path)", "unchanged", "reads wave 3 like the others", "same"),
             ("link_waves(waves)", "changed", "any number of waves:", "spec, tests, code, in order"),
             ("report(pairs)", "changed", "one more column", "")]
    bw, gap, y = 300, 96, 40
    xs = [6 + k * (bw + gap) for k in range(3)]
    body = []
    for k, (fn, status, a, b) in enumerate(steps):
        x = xs[k]
        ch = status == "changed"
        stroke = ORANGE if ch else SEEBLAU
        body.append(box(x, y, bw, 120, fill="#fff3e0" if ch else SEEBLAU1, stroke=stroke, dash="" if ch else ""))
        body.append(txt(x + bw / 2, y - 12, status, 17, weight="bold", fill=ORANGE if ch else GREY))
        body.append(txt(x + bw / 2, y + 34, fn, 18, mono=True, weight="bold"))
        body.append(txt(x + bw / 2, y + 70, a, 18, fill="#444"))
        if b and b != "same":
            body.append(txt(x + bw / 2, y + 96, b, 18, fill="#444"))
        if k < 2:
            body.append(arrow(x + bw + 3, y + 60, x + bw + gap - 3, y + 60))
    hx, hy = xs[1] + 10, y + 186
    body.append(arrow(xs[1] + bw / 2, hy - 30, xs[1] + bw / 2, y + 123, dash="6 5"))
    body.append(box(hx, hy, bw - 20, 100, fill=SEEBLAU1, stroke=SEEBLAU))
    body.append(txt(hx + (bw - 20) / 2, hy - 10, "unchanged", 17, weight="bold", fill=GREY))
    body.append(txt(hx + (bw - 20) / 2, hy + 32, "pseudonym(email)", 18, mono=True, weight="bold"))
    body.append(txt(hx + (bw - 20) / 2, hy + 62, "the secret must stay the same,", 17, fill="#444"))
    body.append(txt(hx + (bw - 20) / 2, hy + 84, "or wave 3 cannot be linked", 17, fill="#444"))
    body.append(person(xs[0] + 60, hy + 34, 1.0))
    body.append(txt(xs[0] + 60, hy + 84, "maintainer", 18, weight="bold", fill=KARPFEN))
    body.append(txt(xs[2] + bw / 2, hy + 40, "the four old tests run again", 18, fill=KARPFEN, style="italic"))
    body.append(txt(xs[2] + bw / 2, hy + 64, "after every change:", 18, fill=KARPFEN, style="italic"))
    body.append(txt(xs[2] + bw / 2, hy + 88, "regression tests", 18, fill=KARPFEN, style="italic", weight="bold"))
    write("04-maintenance.svg", xs[2] + bw + 6, hy + 106, body)



# ============================================================ how pytest works
def pytest_flow():
    body = []
    # the folder with two files
    body.append(f'  <path d="M 10 30 H 90 L 106 46 H 318 V 296 H 10 Z" fill="#fbfbfb" stroke="{GREY}" stroke-width="2"/>\n')
    body.append(txt(164, 70, "survey/", 20, fill=GREY, mono=True))
    body += document(26, 88, 112, 78, "", lines=2)
    body.append(txt(82, 114, "panel.py", 17, mono=True, weight="bold"))
    body.append(txt(82, 184, "the code", 17, fill="#444", style="italic"))
    body += document(150, 88, 160, 78, "", lines=0)
    body.append(txt(230, 112, "test_panel.py", 16, mono=True, weight="bold"))
    body.append(txt(230, 134, "def test_typical", 14, mono=True, fill=KARPFEN))
    body.append(txt(230, 152, "def test_empty_wave", 14, mono=True, fill=KARPFEN))
    body.append(txt(230, 184, "the tests", 17, fill="#444", style="italic"))
    body.append(box(64, 212, 200, 46, fill="#222222", stroke="#222222", rx=6))
    body.append(txt(164, 242, "$ pytest", 22, fill="#ffffff", mono=True))
    body.append(txt(164, 282, "one command, in the folder", 17, fill="#444", style="italic"))
    body.append(arrow(324, 163, 372, 163, sw=3))
    # pytest box
    bx, by, bw, bh = 378, 36, 400, 262
    body.append(box(bx, by, bw, bh, fill=SEEBLAU2, stroke=KARPFEN))
    body.append(txt(bx + bw / 2, by + 38, "pytest", 26, weight="bold"))
    steps = [("1", "finds every file", "test_*.py"),
             ("2", "finds every function", "test_*  in those files"),
             ("3", "runs each one", "failed assert or error = fail"),
             ("4", "reports", "which failed, and why")]
    for k, (n, a, b) in enumerate(steps):
        y = by + 76 + k * 48
        body.append(f'  <circle cx="{bx + 34}" cy="{y - 7}" r="15" fill="{KARPFEN}"/>\n')
        body.append(txt(bx + 34, y - 1, n, 17, fill="#ffffff", weight="bold"))
        body.append(txt(bx + 62, y - 9, a, 19, anchor="start"))
        body.append(txt(bx + 62, y + 13, b, 16, anchor="start", fill="#444", mono=k < 2))
    body.append(arrow(bx + bw + 6, 163, bx + bw + 54, 163, sw=3))
    # report
    rx, ry = 836, 56
    body.append(box(rx, ry, 330, 222, fill="#222222", stroke="#222222", rx=8))
    lines = [("test_panel.py .F", "#ffffff"), ("", ""),
             ("FAILED test_empty_wave_raises", "#ff8080"), ("  DID NOT RAISE ValueError", "#ff8080"),
             ("", ""), ("1 failed, 1 passed", "#ffd27f")]
    for k, (l, c) in enumerate(lines):
        if l:
            body.append(txt(rx + 16, ry + 38 + k * 28, l, 17, fill=c, mono=True, anchor="start"))
    body.append(txt(rx + 165, ry + 246, ". passed    F failed", 17, fill="#444", style="italic"))
    write("04-pytest.svg", rx + 340, 310, body)


if __name__ == "__main__":
    flow("04-se-flow.svg")
    flow("04-se-flow-vibe.svg", vibe=True)
    interpreter()
    compiler()
    class_objects()
    dict_objects()
    oop_team()
    software()
    encapsulation()
    abstraction()
    inheritance()
    polymorphism()
    script_to_software()
    design_pipeline()
    roles()
    panel_example()
    any_coder()
    test_first()
    maintenance()
    pytest_flow()
