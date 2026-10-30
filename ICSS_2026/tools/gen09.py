#!/usr/bin/env python3
"""Diagrams of ICSS session 9 (Theoretical Computer Science)."""
import os, math
OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/09-TheoreticalCS/figures"
FONT = 'font-family="Arial, Helvetica, sans-serif"'
DEFS = ('  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
        'markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
        'fill="#111"/></marker></defs>\n')


def svg(w, h, body, defs=True):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" {FONT}>\n' + (DEFS if defs else "") + body + '</svg>\n')


def txt(x, y, t, fs=13, anchor="middle", fill="#111", weight="normal", style="normal"):
    return (f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{fill}" '
            f'font-weight="{weight}" font-style="{style}">{t}</text>\n')


def write(n, c):
    open(os.path.join(OUT, n), "w").write(c); print("  ", n)


# ---------------------------------------------------- Turing machine tape trace
TAPE = [
    "# ( ( ) ( ) ) #",
    "# ( ( X ( ) ) #",
    "# ( X X ( ) ) #",
    "# ( X X ( X ) #",
    "# ( X X X X ) #",
    "# ( X X X X X #",
    "# X X X X X X #",
    "1 X X X X X X #",
]
HEADS = [1, 3, 2, 5, 4, 6, 1, 0]      # index of the head cell per row (approximate)
CWD, CHD = 40, 30
for k in range(1, len(TAPE) + 1):
    rows = TAPE[:k]
    w = 20 + 8 * CWD + 20
    h = 14 + len(rows) * (CHD + 8)
    body = ""
    for r, row in enumerate(rows):
        y = 10 + r * (CHD + 8)
        for i, ch in enumerate(row.split()):
            x = 20 + i * CWD
            body += (f'  <rect x="{x}" y="{y}" width="{CWD}" height="{CHD}" fill="#fff" '
                     f'stroke="#111" stroke-width="1"/>\n')
            body += txt(x + CWD / 2, y + 21, ch, 15)
    write(f"09-tm-tape-{k}.svg", svg(w, h, body, defs=False))

# ------------------------------------------------------------- graph with s, t
NR = 16


def graph(nodes, edges, w, h, labels=None, directed=False, extra=""):
    body = ""
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        d = math.hypot(x2 - x1, y2 - y1) or 1
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        body += (f'  <line x1="{x1+ux*NR:.1f}" y1="{y1+uy*NR:.1f}" x2="{x2-ux*NR:.1f}" '
                 f'y2="{y2-uy*NR:.1f}" stroke="#111" stroke-width="1.2"'
                 + (' marker-end="url(#a)"' if directed else '') + '/>\n')
    for k, (x, y) in nodes.items():
        body += (f'  <circle cx="{x}" cy="{y}" r="{NR}" fill="#fff" stroke="#111" '
                 f'stroke-width="1.3"/>\n') + txt(x, y + 5, (labels or {}).get(k, k), 13)
    return svg(w, h, body + extra)


N1 = {"s": (40, 70), "b": (120, 26), "c": (120, 114), "d": (210, 70),
      "e": (290, 26), "f": (290, 114), "t": (370, 70)}
E1 = [("s", "b"), ("s", "c"), ("b", "d"), ("c", "d"), ("d", "e"), ("d", "f"),
      ("e", "t"), ("f", "t")]
write("09-graph-st.svg", graph(N1, E1, 410, 150,
                               labels={k: ("s" if k == "s" else "t" if k == "t" else "")
                                       for k in N1},
                               extra=txt(205, 142, "?", 18)))

# Hamiltonian path examples
G1 = {"1": (40, 30), "2": (130, 30), "3": (220, 30),
      "4": (40, 120), "5": (130, 120), "6": (220, 120)}
E_G1 = [("1", "2"), ("2", "3"), ("1", "4"), ("2", "5"), ("3", "6"),
        ("4", "5"), ("5", "6")]
write("09-hamiltonian-yes.svg",
      graph(G1, E_G1, 262, 156, labels={k: "" for k in G1}))
G2 = {"1": (40, 30), "2": (130, 30), "3": (220, 30),
      "4": (40, 120), "5": (130, 120), "6": (220, 120)}
E_G2 = [("1", "2"), ("1", "4"), ("2", "5"), ("3", "6"), ("4", "5")]
write("09-hamiltonian-no.svg",
      graph(G2, E_G2, 262, 156, labels={k: "" for k in G2}))

# --------------------------------------------------------------- P vs NP Venn
def venn(name, layers):
    """layers: list of (rx, ry, cx, cy, label, label_dy, fill)"""
    body = ""
    for rx, ry, cx, cy, label, ldy, fill in layers:
        body += (f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" '
                 f'stroke="#111" stroke-width="1.3"/>\n')
        body += txt(cx, cy + ldy, label, 15)
    write(name, svg(320, 230, body, defs=False))


venn("09-p-np.svg", [
    (140, 100, 160, 115, "NP", -70, "#e8f6fd"),
    (66, 46, 120, 140, "P", 6, "#cceef9"),
])
venn("09-np-complete.svg", [
    (145, 102, 160, 114, "NP", -78, "#e8f6fd"),
    (96, 26, 164, 178, "NP-complete", 5, "#a6e1f4"),
    (52, 30, 112, 96, "P", 5, "#cceef9"),
])
venn("09-np-hard.svg", [
    (152, 106, 160, 114, "NP-hard", -84, "#f6e6e6"),
    (112, 74, 146, 128, "NP", -50, "#e8f6fd"),
    (74, 20, 156, 176, "NP-complete", 5, "#a6e1f4"),
    (40, 22, 110, 110, "P", 5, "#cceef9"),
])

# -------------------------------------------------------- reducing problems
body = ""
for cx, label in [(100, "Problem A"), (330, "Problem B")]:
    body += (f'  <ellipse cx="{cx}" cy="90" rx="82" ry="70" fill="#fff" stroke="#111" '
             f'stroke-width="1.3"/>\n')
    body += txt(cx, 12, label, 15, weight="bold")
    body += txt(cx, 62, "True", 13)
    body += txt(cx, 128, "False", 13)
body += ('  <line x1="128" y1="58" x2="286" y2="58" stroke="#1f6fb2" stroke-width="1.6" '
         'marker-end="url(#a)"/>\n') + txt(207, 50, "f", 14, fill="#1f6fb2", style="italic")
body += ('  <line x1="128" y1="124" x2="286" y2="124" stroke="#1f6fb2" stroke-width="1.6" '
         'marker-end="url(#a)"/>\n') + txt(207, 142, "f", 14, fill="#1f6fb2", style="italic")
write("09-reduction.svg", svg(430, 170, body))

# ------------------------------------------------------------- verifier tape
cells = [("1", 0), ("2", 0), ("…", 0), ("#", 0), ("1", 1), ("3", 1), ("x", 1), ("y", 1),
         ("…", 1), ("#", 1), ("s", 2), ("t", 2), ("#", 2), ("s", 3), ("a", 3), ("…", 3),
         ("t", 3), ("#", 3), ("T/F", 4)]
FILLS = ["#cceef9", "#a6e1f4", "#e5e5e5", "#dbeedb", "#ffd75e"]
CAPS = ["Vertex list", "edge list", "indices s,t", "sequence of nodes", "V?"]
body, x, CW2 = "", 10, 44
groups = {}
for lab, g in cells:
    body += (f'  <rect x="{x}" y="10" width="{CW2}" height="{30}" fill="{FILLS[g]}" '
             f'stroke="#111" stroke-width="1"/>\n') + txt(x + CW2 / 2, 31, lab, 13)
    groups.setdefault(g, []).append(x)
    x += CW2
for g, xs in groups.items():
    cx = (xs[0] + xs[-1] + CW2) / 2
    body += txt(cx, 58, CAPS[g], 12)
body += txt((groups[0][0] + groups[1][-1] + CW2) / 2, 78, "p", 14, style="italic")
body += txt((groups[2][0] + groups[3][-1] + CW2) / 2, 78, "c", 14, style="italic")
write("09-verifier-tape.svg", svg(x + 10, 90, body, defs=False))
print("deck 9 figures written")

# ================================================== the z0..z3 DFA of session 9
# delta(z0,a)=z1  delta(z0,b)=z3   delta(z1,a)=z2  delta(z1,b)=z0
# delta(z2,a)=z3  delta(z2,b)=z1   delta(z3,a)=z0  delta(z3,b)=z2
DP = {"z0": (110, 250), "z1": (330, 250), "z2": (330, 60), "z3": (110, 60)}
DR = 34
DE = [("z0", "a", "z1"), ("z0", "b", "z3"), ("z1", "a", "z2"), ("z1", "b", "z0"),
      ("z2", "a", "z3"), ("z2", "b", "z1"), ("z3", "a", "z0"), ("z3", "b", "z2")]
HL = "#f5a3a3"


def dfa(highlight=None, name="09-dfa.svg"):
    body = ""
    for src, sym, dst in DE:
        (x1, y1), (x2, y2) = DP[src], DP[dst]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        # perpendicular offset so the two directions do not overlap
        px, py = -uy, ux
        off = 13
        sx, sy = x1 + ux * DR + px * off, y1 + uy * DR + py * off
        ex, ey = x2 - ux * (DR + 6) + px * off, y2 - uy * (DR + 6) + py * off
        mx, my = (sx + ex) / 2 + px * 16, (sy + ey) / 2 + py * 16
        body += (f'  <path d="M {sx:.1f} {sy:.1f} Q {mx:.1f} {my:.1f} {ex:.1f} {ey:.1f}" '
                 f'fill="none" stroke="#111" stroke-width="2" marker-end="url(#a)"/>\n')
        lx, ly = (sx + ex) / 2 + px * 26, (sy + ey) / 2 + py * 26
        body += txt(lx, ly + 5, sym, 17)
    body += ('  <line x1="18" y1="250" x2="66" y2="250" stroke="#111" stroke-width="2" '
             'marker-end="url(#a)"/>\n')
    for k, (x, y) in DP.items():
        fill = HL if k == highlight else "#fff"
        if k == "z3":
            body += (f'  <circle cx="{x}" cy="{y}" r="{DR+5}" fill="none" stroke="#111" '
                     f'stroke-width="2"/>\n')
        body += (f'  <circle cx="{x}" cy="{y}" r="{DR}" fill="{fill}" stroke="#111" '
                 f'stroke-width="2"/>\n')
        body += txt(x, y + 7, k, 20)
    write(name, svg(420, 320, body))


dfa(None, "09-dfa.svg")
for page, hl in [(10, "z0"), (11, "z1"), (12, "z0"), (13, "z3"),
                 (14, "z0"), (15, "z1"), (16, "z2"), (17, "z1")]:
    dfa(hl, f"09-dfa-{page}.svg")
