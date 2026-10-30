#!/usr/bin/env python3
"""Generate the diagrams of ICSS session 3 (Data Structures) as SVG."""
import os

OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/03-DataStructures/figures"
FONT = 'font-family="Arial, Helvetica, sans-serif"'

ROOT_FILL = "#a6a6a6"
LEAF_FILL = "#dbeedb"
PLAIN_FILL = "#ffffff"
MARK_FILL = "#fdf3c8"      # highlighted node (yellow)
PINK_FILL = "#f3d9e8"

ARROW = '''  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#222"/></marker>
    <marker id="ab" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#1f6fb2"/></marker>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#cc2222"/></marker>
  </defs>
'''

NW, NH = 38, 27          # node box size


def svg(w, h, body, defs=True):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" {FONT}>\n' + (ARROW if defs else "") +
            body + '</svg>\n')


def node(x, y, label, fill=PLAIN_FILL, stroke="#111", fs=15, w=NW, h=NH, sw=1.1,
         color="#111"):
    """x,y = centre of the node box."""
    return (f'  <rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>\n'
            f'  <text x="{x}" y="{y+5:.1f}" text-anchor="middle" font-size="{fs}" '
            f'fill="{color}">{label}</text>\n')


def edge(p, c, pos, color="#111", sw=1.1):
    (x1, y1), (x2, y2) = pos[p], pos[c]
    return (f'  <line x1="{x1}" y1="{y1+NH/2}" x2="{x2}" y2="{y2-NH/2}" stroke="{color}" '
            f'stroke-width="{sw}"/>\n')


def txt(x, y, t, fs=14, anchor="middle", fill="#111", weight="normal", style="normal"):
    return (f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{fill}" '
            f'font-weight="{weight}" font-style="{style}">{t}</text>\n')


# ---------------------------------------------------------------- canonical BST
#            10
#        4        13
#      2   9    11   21
#     1 3          12          (6 optionally as left child of 9)
BASE_POS = {
    "10": (250, 24), "4": (140, 92), "13": (360, 92),
    "2": (85, 160), "9": (195, 160), "11": (305, 160), "21": (415, 160),
    "1": (55, 228), "3": (115, 228), "12": (335, 228), "6": (170, 228),
}
BASE_EDGES = [("10", "4"), ("10", "13"), ("4", "2"), ("4", "9"),
              ("13", "11"), ("13", "21"), ("2", "1"), ("2", "3"), ("11", "12")]
BASE_LEAVES = {"1", "3", "9", "21", "12"}
CANVAS = (470, 258)


def draw_tree(pos, edges, fills, extra="", canvas=CANVAS, dx=0, dy=0, only=None,
              labels=None, colors=None):
    """Return SVG body for a tree; `only` restricts which nodes are drawn."""
    p = {k: (v[0] + dx, v[1] + dy) for k, v in pos.items()}
    keys = only if only is not None else list(pos.keys())
    labels = labels or {}
    colors = colors or {}
    body = ""
    for a, b in edges:
        if a in keys and b in keys:
            body += edge(a, b, p)
    for k in keys:
        body += node(p[k][0], p[k][1], labels.get(k, k), fills.get(k, PLAIN_FILL),
                     color=colors.get(k, "#111"))
    return body + extra


def base_fills(nodes, root="10", leaves=None, marks=None):
    leaves = BASE_LEAVES if leaves is None else leaves
    f = {}
    for n in nodes:
        f[n] = ROOT_FILL if n == root else (LEAF_FILL if n in leaves else PLAIN_FILL)
    for k, v in (marks or {}).items():
        f[k] = v
    return f


def write(name, content):
    open(os.path.join(OUT, name), "w").write(content)
    print("  ", name)


NODES = [n for n in BASE_POS if n != "6"]

# 1. plain canonical BST -------------------------------------------------------
write("03-bst-base.svg",
      svg(*CANVAS, draw_tree(BASE_POS, BASE_EDGES, base_fills(NODES), only=NODES)))

# 2. root rule: <= and > with two dashed ellipses -------------------------------
ell = (f'  <ellipse cx="140" cy="165" rx="105" ry="88" fill="none" stroke="#999" '
       f'stroke-width="1.2" stroke-dasharray="5 4"/>\n'
       f'  <ellipse cx="362" cy="163" rx="86" ry="84" fill="none" stroke="#999" '
       f'stroke-width="1.2" stroke-dasharray="5 4"/>\n'
       + txt(198, 52, "&#8804;", 17, weight="bold")
       + txt(303, 52, "&gt;", 17, weight="bold"))
write("03-bst-root-rule.svg",
      svg(*CANVAS, draw_tree(BASE_POS, BASE_EDGES, base_fills(NODES), ell, only=NODES)))

# 3. level-2 rule --------------------------------------------------------------
lvl2 = (txt(103, 128, "&#8804;", 16, weight="bold") + txt(178, 128, "&gt;", 16, weight="bold")
        + txt(322, 128, "&#8804;", 16, weight="bold") + txt(398, 128, "&gt;", 16, weight="bold"))
write("03-bst-level2-rule.svg",
      svg(*CANVAS, draw_tree(BASE_POS, BASE_EDGES, base_fills(NODES), lvl2, only=NODES)))

# 4. level-3 rule --------------------------------------------------------------
lvl3 = (txt(58, 196, "&#8804;", 16, weight="bold") + txt(112, 196, "&gt;", 16, weight="bold")
        + txt(310, 196, "&gt;", 16, weight="bold"))
write("03-bst-level3-rule.svg",
      svg(*CANVAS, draw_tree(BASE_POS, BASE_EDGES, base_fills(NODES), lvl3, only=NODES)))

# 5. "is this a BST?" — invalid tree -------------------------------------------
BAD_POS = dict(BASE_POS)
BAD_POS = {"10": (250, 24), "4": (140, 92), "13": (360, 92),
           "2": (85, 160), "9": (195, 160), "15": (305, 160), "21": (415, 160),
           "5": (55, 228), "3": (115, 228), "11": (335, 228)}
BAD_EDGES = [("10", "4"), ("10", "13"), ("4", "2"), ("4", "9"),
             ("13", "15"), ("13", "21"), ("2", "5"), ("2", "3"), ("15", "11")]
bad_leaves = {"5", "3", "9", "21", "11"}
write("03-bst-not-a-bst.svg",
      svg(*CANVAS, draw_tree(BAD_POS, BAD_EDGES,
                             base_fills(BAD_POS.keys(), leaves=bad_leaves))))

# the same tree with the violating relationships circled in red
viol = ('  <ellipse cx="332" cy="126" rx="70" ry="25" transform="rotate(129 332 126)" fill="none" '
        'stroke="#cc2222" stroke-width="2.4"/>\n'
        '  <ellipse cx="70" cy="194" rx="64" ry="24" transform="rotate(114 70 194)" fill="none" '
        'stroke="#cc2222" stroke-width="2.4"/>\n'
        '  <path d="M 120 86 Q 6 104 34 226" fill="none" stroke="#cc2222" stroke-width="2.2" '
        'stroke-dasharray="6 4"/>\n'
        '  <ellipse cx="320" cy="194" rx="58" ry="22" transform="rotate(66 320 194)" fill="none" '
        'stroke="#cc2222" stroke-width="2.4"/>\n')
write("03-bst-not-a-bst-marked.svg",
      svg(*CANVAS, draw_tree(BAD_POS, BAD_EDGES,
                             base_fills(BAD_POS.keys(), leaves=bad_leaves), viol)))

# 6. search for 11 -------------------------------------------------------------
search = (
    f'  <path d="M 305 34 Q 340 20 352 62" fill="none" stroke="#1f6fb2" stroke-width="2" '
    f'marker-end="url(#ab)"/>\n'
    f'  <path d="M 352 108 Q 330 120 296 140" fill="none" stroke="#1f6fb2" stroke-width="2" '
    f'marker-end="url(#ab)"/>\n'
    + f'  <circle cx="292" cy="20" r="12" fill="#fff" stroke="#1f6fb2" stroke-width="1.4"/>\n'
    + txt(292, 25, "1.", 12, fill="#1f6fb2")
    + f'  <circle cx="384" cy="60" r="12" fill="#fff" stroke="#1f6fb2" stroke-width="1.4"/>\n'
    + txt(384, 65, "2.", 12, fill="#1f6fb2")
    + f'  <circle cx="268" cy="140" r="12" fill="#fff" stroke="#1f6fb2" stroke-width="1.4"/>\n'
    + txt(268, 145, "3.", 12, fill="#1f6fb2"))
write("03-bst-search-11.svg",
      svg(*CANVAS, draw_tree(BASE_POS, BASE_EDGES, base_fills(NODES), search, only=NODES)))

# 7. tree with key 6 inserted --------------------------------------------------
WITH6 = NODES + ["6"]
E6 = BASE_EDGES + [("9", "6")]
write("03-bst-with-6.svg",
      svg(*CANVAS, draw_tree(BASE_POS, E6,
                             base_fills(WITH6, leaves=(BASE_LEAVES | {"6"}) - {"9"}),
                             only=WITH6)))
# 6 highlighted, about to be deleted
write("03-bst-delete-6.svg",
      svg(*CANVAS, draw_tree(BASE_POS, E6,
                             base_fills(WITH6, leaves=(BASE_LEAVES | {"6"}) - {"9"},
                                        marks={"6": MARK_FILL}),
                             only=WITH6)))

# 8. delete a node with one child (11 -> 12) -----------------------------------
ONE_POS = dict(BASE_POS)
ONE_POS["12b"] = (305, 160)                     # 12 promoted into 11's slot
E_ONE = [e for e in E6 if e != ("13", "11") and e != ("11", "12")] + [("13", "12b")]
only_one = [n for n in WITH6 if n not in ("11", "12")] + ["12b"]
fills_one = base_fills(only_one, leaves=(BASE_LEAVES | {"6"}) - {"9", "12"})
fills_one["12b"] = LEAF_FILL
body = draw_tree(ONE_POS, E_ONE, fills_one, only=only_one, labels={"12b": "12"})
write("03-bst-delete-onechild-after.svg", svg(*CANVAS, body))
# before: 11 highlighted
write("03-bst-delete-onechild-before.svg",
      svg(*CANVAS, draw_tree(BASE_POS, E6,
                             base_fills(WITH6, leaves=(BASE_LEAVES | {"6"}) - {"9"},
                                        marks={"11": MARK_FILL}),
                             only=WITH6)))

# 9. delete the root (two children) -- three panels -----------------------------
#    (a) root 10 marked, (b) 11 copied to the root, (c) 12 promoted
p_a = draw_tree(BASE_POS, BASE_EDGES,
                base_fills(NODES, marks={"10": PINK_FILL, "11": MARK_FILL}), only=NODES)
write("03-bst-delete-root-a.svg", svg(*CANVAS, p_a))

ROOT11 = dict(BASE_POS)
fills_b = base_fills(NODES, root=None, marks={"11": MARK_FILL})
body_b = draw_tree(ROOT11, BASE_EDGES, fills_b, only=NODES,
                   labels={"10": "11"}, colors={"10": "#0a7d3e"})
body_b += (f'  <path d="M 305 150 Q 300 90 262 40" fill="none" stroke="#1f6fb2" '
           f'stroke-width="2.4" marker-end="url(#ab)"/>\n')
write("03-bst-delete-root-b.svg", svg(*CANVAS, body_b))

only_c = [n for n in NODES if n not in ("11", "12")] + ["12b"]
POS_C = dict(BASE_POS); POS_C["12b"] = (305, 160)
E_C = [e for e in BASE_EDGES if e not in (("13", "11"), ("11", "12"))] + [("13", "12b")]
fills_c = base_fills(only_c, root=None, leaves=BASE_LEAVES - {"12"})
fills_c["12b"] = LEAF_FILL
body_c = draw_tree(POS_C, E_C, fills_c, only=only_c,
                   labels={"12b": "12", "10": "11"}, colors={"10": "#0a7d3e"})
write("03-bst-delete-root-c.svg", svg(*CANVAS, body_c))

# 10. unbalanced tree ----------------------------------------------------------
UB_POS = {"3": (30, 22), "5": (95, 76), "7": (160, 130), "8": (225, 184)}
UB_E = [("3", "5"), ("5", "7"), ("7", "8")]
write("03-bst-unbalanced.svg",
      svg(260, 210, draw_tree(UB_POS, UB_E,
                              base_fills(UB_POS.keys(), root="3", leaves={"8"}),
                              canvas=(260, 210))))

# 11. binary tree with legend --------------------------------------------------
TP = {"A": (250, 22), "B": (160, 84), "C": (350, 84),
      "D": (110, 146), "E": (215, 146), "F": (305, 146), "G": (400, 146),
      "H": (75, 208), "I": (140, 208), "J": (215, 208)}
TE = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G"),
      ("D", "H"), ("D", "I"), ("E", "J")]


def circ(x, y, t, fill):
    return (f'  <circle cx="{x}" cy="{y}" r="15" fill="{fill}" stroke="#111" stroke-width="1.1"/>\n'
            + txt(x, y + 5, t, 14))


body = ""
for a, b in TE:
    (x1, y1), (x2, y2) = TP[a], TP[b]
    body += f'  <line x1="{x1}" y1="{y1+15}" x2="{x2}" y2="{y2-15}" stroke="#111" stroke-width="1.1"/>\n'
# sibling links (dotted) and sub-tree ellipse (dashed)
body += ('  <line x1="175" y1="84" x2="335" y2="84" stroke="#1f6fb2" stroke-width="1" '
         'stroke-dasharray="2 3"/>\n')
body += ('  <line x1="90" y1="208" x2="125" y2="208" stroke="#1f6fb2" stroke-width="1" '
         'stroke-dasharray="2 3"/>\n')
body += ('  <ellipse cx="352" cy="118" rx="72" ry="62" fill="none" stroke="#999" '
         'stroke-width="1.2" stroke-dasharray="5 4"/>\n')
for k, (x, y) in TP.items():
    fill = ROOT_FILL if k == "A" else (LEAF_FILL if k in ("H", "I", "J", "F", "G") else PLAIN_FILL)
    body += circ(x, y, k, fill)
write("03-binary-tree.svg", svg(440, 232, body))

# legend as its own figure
leg = ""
rows = [("root", "Root"), ("leaf", "Leaf Node"), ("pc", "Parent-Child"),
        ("sib", "Siblings"), ("sub", "Sub-tree")]
for i, (kind, label) in enumerate(rows):
    y = 20 + i * 36
    if kind == "root":
        leg += f'  <circle cx="22" cy="{y}" r="14" fill="{ROOT_FILL}" stroke="#111" stroke-width="1.1"/>\n'
    elif kind == "leaf":
        leg += f'  <circle cx="22" cy="{y}" r="14" fill="{LEAF_FILL}" stroke="#111" stroke-width="1.1"/>\n'
    elif kind == "pc":
        leg += f'  <line x1="6" y1="{y}" x2="38" y2="{y}" stroke="#111" stroke-width="1.4"/>\n'
    elif kind == "sib":
        leg += f'  <line x1="6" y1="{y}" x2="38" y2="{y}" stroke="#1f6fb2" stroke-width="1.2" stroke-dasharray="2 3"/>\n'
    else:
        leg += f'  <ellipse cx="22" cy="{y}" rx="17" ry="11" fill="none" stroke="#999" stroke-width="1.2" stroke-dasharray="5 4"/>\n'
    leg += (f'  <rect x="46" y="{y-15}" width="146" height="30" fill="#fff" stroke="#111" stroke-width="1"/>\n'
            + txt(52, y + 5, label, 14, anchor="start"))
write("03-tree-legend.svg", svg(200, 200, leg, defs=False))

# 12. array with indices -------------------------------------------------------
cells = ["'a'", "'b'", "'c'", "'d'", "'e'", "'f'"]
cw, chh, x0, y0 = 84, 44, 72, 46
body = ""
body += (f'  <line x1="{x0}" y1="30" x2="{x0+6*cw}" y2="30" stroke="#111" stroke-width="1.2" '
         f'stroke-dasharray="7 5"/>\n')
body += f'  <rect x="{x0+3*cw-52}" y="14" width="104" height="20" fill="#fff"/>\n'
body += txt(x0 + 3 * cw, 30, "Length = 6", 16)
for i, c in enumerate(cells):
    x = x0 + i * cw
    body += (f'  <rect x="{x}" y="{y0}" width="{cw}" height="{chh}" fill="#fff" stroke="#111" '
             f'stroke-width="1.2"/>\n') + txt(x + cw / 2, y0 + 28, c, 16)
    body += txt(x + cw / 2, y0 + chh + 22, f"[{i}]", 14, fill="#1f6fb2")
body += txt(x0 - 8, y0 + chh + 22, "Index", 16, anchor="end")
write("03-array.svg", svg(x0 + 6 * cw + 20, y0 + chh + 34, body))

# 13. binary search on a sorted array — two figures of four steps each ---------
vals = [15, 28, 30, 34, 36, 43, 62, 73, 81, 82]
CW, CHH, X0 = 50, 34, 24
GREY, DARK, LIGHT, FOUND = "#c8c8c8", "#1f6fb2", "#cceef9", "#bfe3bf"


UPD = "#e07b00"          # a pointer that was updated in this step


def search_fig(name, steps):
    """steps: (greyed, dark, light, found, {"p": i, "q": i, "r": i}, updated letters)."""
    rowh = 100
    body = ""
    for r, (greyed, dark, light, found, ptr, upd) in enumerate(steps):
        y = 46 + r * rowh
        for i, v in enumerate(vals):
            x = X0 + i * CW
            fill, col = "#fff", "#111"
            if i + 1 in greyed:
                fill, col = GREY, "#666"
            if i + 1 in light:
                fill = LIGHT
            if i + 1 in found:
                fill = FOUND
            if i + 1 in dark:
                fill, col = DARK, "#fff"
            body += (f'  <rect x="{x}" y="{y}" width="{CW}" height="{CHH}" fill="{fill}" '
                     f'stroke="#111" stroke-width="1"/>\n')
            body += txt(x + CW / 2, y + 23, str(v), 15, fill=col)
            body += txt(x + CW / 2, y + CHH + 14, str(i + 1), 11, fill="#444")
        # one arrow per position, labelled with every pointer that sits there
        at = {}
        for letter in "pqr":
            if ptr.get(letter):
                at.setdefault(ptr[letter], []).append(letter)
        for pos, letters in at.items():
            xc = X0 + (pos - 0.5) * CW
            hot = any(l in upd for l in letters)
            spans = ", ".join(f'<tspan fill="{UPD if l in upd else "#111"}">{l}</tspan>' for l in letters)
            body += (f'  <text x="{xc}" y="{y-24}" text-anchor="middle" font-size="17" '
                     f'font-style="italic" font-weight="bold">{spans}</text>\n')
            body += (f'  <line x1="{xc}" y1="{y-19}" x2="{xc}" y2="{y-4}" stroke="{UPD if hot else "#111"}" '
                     f'stroke-width="1.8" marker-end="url(#{"ao" if hot else "a"})"/>\n')
    defs = ('  <defs><marker id="ao" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
            f'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{UPD}"/></marker></defs>\n')
    write(name, svg(X0 + 10 * CW + 20, 46 + len(steps) * rowh - 34, defs + body))


G5, G810 = set(range(1, 6)), {8, 9, 10}
# p = 1, r = 10 -> q = 5 (36 < 43) -> p = 6 -> q = 8 (73 > 43)
search_fig("03-binary-search-steps-1.svg", [
    (set(), set(), {6}, set(), {"p": 1, "r": 10}, "pr"),
    (set(), {5}, {6}, set(), {"p": 1, "q": 5, "r": 10}, "q"),
    (G5, set(), {6}, set(), {"p": 6, "q": 5, "r": 10}, "p"),
    (G5, {8}, {6}, set(), {"p": 6, "q": 8, "r": 10}, "q"),
])
# ... r = 7 -> q = 6 (43 = 43) -> return 6
search_fig("03-binary-search-steps-2.svg", [
    (G5, {8}, {6}, set(), {"p": 6, "q": 8, "r": 10}, ""),
    (G5 | G810, set(), {6}, set(), {"p": 6, "q": 8, "r": 7}, "r"),
    (G5 | G810, {6}, set(), set(), {"p": 6, "q": 6, "r": 7}, "q"),
    (G5 | {7} | G810, set(), set(), {6}, {"p": 6, "q": 6, "r": 7}, ""),
])

# 14. hash collisions ----------------------------------------------------------
names = ["Max Mustermann", "Petra Paul", "Michael Müller", "Anja Schmidt"]
targets = [3, 0, 3, 5]                    # Max & Michael collide on 3
body = ""
body += txt(150, 22, "key", 16, weight="bold")
body += txt(330, 16, "hash", 15, weight="bold") + txt(330, 34, "function", 15, weight="bold")
body += txt(430, 16, "hash", 15, weight="bold") + txt(430, 34, "value", 15, weight="bold")
body += f'  <rect x="300" y="46" width="60" height="230" fill="#6fa8f5"/>\n'
slot_y0, sh = 46, 27
for i in range(8):
    y = slot_y0 + i * sh
    lab = str(i) if i < 7 else "m"
    fill = "#fff"
    if i in (0, 5):
        fill = "#3ddc84"
    if i == 3:
        fill = "#ef4444"
    if i == 6:
        fill = "#e9edf2"
    if i == 7:
        body += txt(415, y + 4, "⋮", 16)
        y += 6
    body += (f'  <rect x="400" y="{y}" width="42" height="{sh-3}" fill="{fill}" stroke="#111" '
             f'stroke-width="1"/>\n')
    body += txt(421, y + 18, lab, 14, style=("italic" if i == 7 else "normal"))
for i, n in enumerate(names):
    y = 60 + i * 52
    body += (f'  <rect x="40" y="{y}" width="240" height="34" fill="#fbfbdc" stroke="none"/>\n')
    body += txt(160, y + 24, n, 16)
    col = "#cc2222" if i in (0, 2) else "#111"
    mk = "ar" if i in (0, 2) else "a"
    ty = slot_y0 + targets[i] * sh + (sh - 3) / 2
    body += (f'  <line x1="282" y1="{y+17}" x2="298" y2="{y+17}" stroke="{col}" stroke-width="1.6"/>\n')
    body += (f'  <line x1="362" y1="{y+17}" x2="396" y2="{ty}" stroke="{col}" stroke-width="1.6" '
             f'marker-end="url(#{mk})"/>\n')
write("03-hash-collisions.svg", svg(470, 292, body))

# 15. separate chaining --------------------------------------------------------
panels = [
    (["initial", "array"], {}),
    (["insert", "50"], {1: [50]}),
    (["insert", "700"], {0: [700], 1: [50]}),
    (["insert", "76"], {0: [700], 1: [50], 6: [76]}),
    (["insert", "85"], {0: [700], 1: [50, 85], 6: [76]}),
    (["insert", "92"], {0: [700], 1: [50, 85, 92], 6: [76]}),
    (["insert 73 and", "then 101"],
     {0: [700], 1: [50, 85, 92], 3: [73, 101], 6: [76]}),
]
NEWKEY = [None, 50, 700, 76, 85, 92, 101]      # value added in each panel
rowh, boxw, gap, linkw = 26, 40, 16, 22
body, x, xs = "", 22, []
for pi, (cap, content) in enumerate(panels):
    xs.append(x)
    for r in range(7):
        y = 26 + r * rowh
        body += txt(x - 5, y + 16, str(r), 11, anchor="end", fill="#444")
        chain = content.get(r, [])
        head = str(chain[0]) if chain else ""
        fill = "#cceef9" if chain and chain[0] == NEWKEY[pi] else "#fff"
        body += (f'  <rect x="{x}" y="{y}" width="{boxw}" height="{rowh-4}" fill="{fill}" '
                 f'stroke="#111" stroke-width="1"/>\n')
        if head:
            body += txt(x + boxw / 2, y + 16, head, 12)
        cx = x + boxw
        for v in chain[1:]:
            body += (f'  <line x1="{cx}" y1="{y+(rowh-4)/2}" x2="{cx+linkw-2}" '
                     f'y2="{y+(rowh-4)/2}" stroke="#111" stroke-width="1" '
                     f'marker-end="url(#a)"/>\n')
            cx += linkw
            f2 = "#cceef9" if v == NEWKEY[pi] else "#fff"
            body += (f'  <rect x="{cx}" y="{y}" width="{boxw}" height="{rowh-4}" fill="{f2}" '
                     f'stroke="#111" stroke-width="1"/>\n')
            body += txt(cx + boxw / 2, y + 16, str(v), 12)
            cx += boxw
    maxchain = max([len(v) for v in content.values()] or [1])
    width = boxw * maxchain + linkw * (maxchain - 1)
    cy = 26 + 7 * rowh + 14
    for j, line in enumerate(cap):
        body += txt(x, cy + j * 13, line, 11, anchor="start")
    x += width + gap + 12
# "Linked List" callout pointing at two chained cells
body += ('  <ellipse cx="' + str(xs[4] + boxw + linkw + boxw / 2) + '" cy="' +
         str(26 + rowh + (rowh - 4) / 2) + '" rx="34" ry="17" fill="none" stroke="#111" '
         'stroke-width="1" stroke-dasharray="4 3"/>\n')
write("03-separate-chaining.svg", svg(x, 26 + 7 * rowh + 44, body))

# 16. linked lists (singly, deletion, doubly) -- one canvas for the three slides
LL_KEYS = [7, 13, 21, 42]
LL_W, LL_H = 840, 140          # identical canvas, so the list does not move between slides
CELL_H, KEY_W, PTR_W, LL_GAP = 46, 58, 34, 52
LL_BLUE = "#cceef9"


def ll_figure(doubly=False, delete=None, height=LL_H):
    """head -> [key|next] -> ... -> NIL ; with doubly=True: [prev|key|next] and back links."""
    node_w = KEY_W + PTR_W * (2 if doubly else 1)
    n = len(LL_KEYS)
    total = n * node_w + (n - 1) * LL_GAP
    x0 = (LL_W - total) / 2 + 10
    y = 56
    body = ""
    # head pointer
    body += txt(x0 - 62, y + CELL_H / 2 + 6, "head", 17, anchor="middle", weight="bold")
    body += (f'  <line x1="{x0-40}" y1="{y+CELL_H/2}" x2="{x0-3}" y2="{y+CELL_H/2}" stroke="#111" '
             f'stroke-width="1.8" marker-end="url(#a)"/>\n')
    xs = []
    for i, k in enumerate(LL_KEYS):
        x = x0 + i * (node_w + LL_GAP)
        xs.append(x)
        gone = delete is not None and k == delete
        stroke = "#999" if gone else "#111"
        fill_key = "#eeeeee" if gone else LL_BLUE
        cx = x
        if doubly:
            body += (f'  <rect x="{cx}" y="{y}" width="{PTR_W}" height="{CELL_H}" fill="#fff" '
                     f'stroke="{stroke}" stroke-width="1.4"/>\n')
            cx += PTR_W
        body += (f'  <rect x="{cx}" y="{y}" width="{KEY_W}" height="{CELL_H}" fill="{fill_key}" '
                 f'stroke="{stroke}" stroke-width="1.4"/>\n')
        body += txt(cx + KEY_W / 2, y + CELL_H / 2 + 7, str(k), 20, fill=("#999" if gone else "#111"))
        cx += KEY_W
        body += (f'  <rect x="{cx}" y="{y}" width="{PTR_W}" height="{CELL_H}" fill="#fff" '
                 f'stroke="{stroke}" stroke-width="1.4"/>\n')
        body += f'  <circle cx="{cx+PTR_W/2}" cy="{y+CELL_H/2}" r="4" fill="{stroke}"/>\n'
    # field labels under the first node (left out when a deletion is drawn below the list)
    lx = xs[0]
    labels = (["prev"] if doubly else []) + ["key"] + ["next"]
    if doubly and delete is not None:
        labels = []
    widths = ([PTR_W] if doubly else []) + [KEY_W, PTR_W]
    for lab, w in zip(labels, widths):
        body += txt(lx + w / 2, y + CELL_H + 22, lab, 14, fill="#555", style="italic")
        lx += w
    # next pointers
    for i in range(n - 1):
        x_from = xs[i] + node_w - PTR_W / 2
        x_to = xs[i + 1] - 3
        ya = y + (CELL_H / 2 if not doubly else CELL_H / 2 - 9)
        if delete is not None and LL_KEYS[i + 1] == delete:
            continue
        if delete is not None and LL_KEYS[i] == delete:
            body += (f'  <line x1="{x_from}" y1="{ya}" x2="{x_to}" y2="{ya}" stroke="#999" '
                     f'stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#a)"/>\n')
            continue
        body += (f'  <line x1="{x_from}" y1="{ya}" x2="{x_to}" y2="{ya}" stroke="#111" '
                 f'stroke-width="1.8" marker-end="url(#a)"/>\n')
    # prev pointers (doubly)
    if doubly:
        for i in range(1, n):
            x_from = xs[i] + PTR_W / 2
            x_to = xs[i - 1] + node_w + 3
            yb = y + CELL_H / 2 + 9
            if delete is not None and LL_KEYS[i - 1] == delete:
                continue
            if delete is not None and LL_KEYS[i] == delete:
                body += (f'  <line x1="{x_from}" y1="{yb}" x2="{x_to}" y2="{yb}" stroke="#999" '
                         f'stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#ab)"/>\n')
                continue
            body += (f'  <line x1="{x_from}" y1="{yb}" x2="{x_to}" y2="{yb}" stroke="#1f6fb2" '
                     f'stroke-width="1.8" marker-end="url(#ab)"/>\n')
        # NIL before the first node
        body += txt(xs[0] + PTR_W / 2, y - 12, "NIL", 14, fill="#1f6fb2", weight="bold")
        body += (f'  <line x1="{xs[0]+PTR_W/2}" y1="{y+CELL_H/2+9}" x2="{xs[0]+PTR_W/2}" y2="{y-6}" '
                 f'stroke="#1f6fb2" stroke-width="1.4" marker-end="url(#ab)"/>\n')
    # NIL after the last node
    last = xs[-1] + node_w - PTR_W / 2
    ya = y + (CELL_H / 2 if not doubly else CELL_H / 2 - 9)
    body += (f'  <line x1="{last}" y1="{ya}" x2="{xs[-1]+node_w+34}" y2="{ya}" stroke="#111" '
             f'stroke-width="1.8" marker-end="url(#a)"/>\n')
    body += txt(xs[-1] + node_w + 60, ya + 6, "NIL", 17, weight="bold")
    # deletion: bypass arrow from the predecessor to the successor
    if delete is not None:
        i = LL_KEYS.index(delete)
        x_from = xs[i - 1] + node_w - PTR_W / 2
        x_to = xs[i + 1] + KEY_W / 2
        body += (f'  <path d="M {x_from} {y} C {x_from+20} {y-48}, {x_to-20} {y-48}, {x_to} {y-4}" '
                 f'fill="none" stroke="#cc2222" stroke-width="2.2" marker-end="url(#ar)"/>\n')
        label = (f"{LL_KEYS[i-1]}.next now points to {LL_KEYS[i+1]}" if doubly
                 else f"delete {delete}: the predecessor now points past it")
        body += txt((x_from + x_to) / 2, y - 40, label, 15, fill="#cc2222")
        if doubly:
            # the successor's prev pointer now skips the deleted node too
            xb_from = xs[i + 1] + PTR_W / 2
            xb_to = xs[i - 1] + node_w - PTR_W / 2
            yb = y + CELL_H
            body += (f'  <path d="M {xb_from} {yb} C {xb_from-20} {yb+48}, {xb_to+20} {yb+48}, {xb_to} {yb+4}" '
                     f'fill="none" stroke="#cc2222" stroke-width="2.2" marker-end="url(#ar)"/>\n')
            body += txt((xb_from + xb_to) / 2, yb + 58, f"{LL_KEYS[i+1]}.prev now points to {LL_KEYS[i-1]}", 15,
                        fill="#cc2222")
    return svg(LL_W, height, body)


write("03-linked-list.svg", ll_figure())
write("03-linked-list-delete.svg", ll_figure(delete=13))
# the doubly linked list is explained on exercise sheet 3, no longer in the deck
open(os.path.join(OUT, "..", "..", "..", "TheoryExercises", "figures", "ex03-doubly-linked-list.svg"),
     "w").write(ll_figure(doubly=True))

# 17. root deletion, three panels on a tight canvas (the trees use the full slide width)
TIGHT = (414, 238)          # crop of CANVAS around the nodes: x 30..444, y 6..244
def tight(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="34 6 {TIGHT[0]} {TIGHT[1]}" '
            f'width="{TIGHT[0]}" height="{TIGHT[1]}" {FONT}>\n' + ARROW + body + '</svg>\n')


write("03-bst-delete-root-a.svg", tight(p_a))
write("03-bst-delete-root-b.svg", tight(body_b))
write("03-bst-delete-root-c.svg", tight(body_c))

# 18. open addressing: linear and random probing, same keys and table as separate chaining
PROBE_KEYS = [50, 700, 76, 85, 92, 73, 101]
PM = 7
RANDOM_OFFSETS = [3, 6, 2, 5, 1, 4]      # a fixed pseudo-random permutation of 1..m-1


def probe_sequence(k, kind):
    h = k % PM
    if kind == "linear":
        return [(h + i) % PM for i in range(PM)]
    return [h] + [(h + r) % PM for r in RANDOM_OFFSETS]


def probe_figure(name, kind):
    table = [None] * PM
    states = [(None, [], list(table))]
    for k in PROBE_KEYS:
        seq = probe_sequence(k, kind)
        path = []
        for slot in seq:
            path.append(slot)
            if table[slot] is None:
                table[slot] = k
                break
        states.append((k, path, list(table)))
    rowh, cw, panel = 30, 54, 96
    y0 = 30
    body = ""
    for pi, (k, path, tab) in enumerate(states):
        x = 34 + pi * panel
        for r in range(PM):
            y = y0 + r * rowh
            if pi == 0:
                body += txt(x - 8, y + 20, str(r), 13, anchor="end", fill="#444")
            v = tab[r]
            fill = "#fff"
            if k is not None and v == k:
                fill = LL_BLUE
            elif k is not None and r in path[:-1]:
                fill = "#f9d6d6"            # probed and found occupied
            body += (f'  <rect x="{x}" y="{y}" width="{cw}" height="{rowh-4}" fill="{fill}" '
                     f'stroke="#111" stroke-width="1"/>\n')
            if v is not None:
                body += txt(x + cw / 2, y + 19, str(v), 14)
        # probe order: a numbered marker right of every probed cell (all probes of this insertion)
        if k is not None and len(path) > 1:
            for j, slot in enumerate(path):
                yc = y0 + slot * rowh + (rowh - 4) / 2
                xc = x + cw + (26 if kind == "linear" else 12)
                body += (f'  <circle cx="{xc}" cy="{yc}" r="8" fill="#fff" stroke="#cc2222" '
                         f'stroke-width="1.2"/>\n')
                body += txt(xc, yc + 4, str(j + 1), 11, fill="#cc2222", weight="bold")
        # linear probing: arrows between the adjacent probed cells
        for a, b in (zip(path, path[1:]) if kind == "linear" else []):
            ya, yb = y0 + a * rowh + (rowh - 4) / 2, y0 + b * rowh + (rowh - 4) / 2
            bend = 12
            body += (f'  <path d="M {x+cw+1} {ya} C {x+cw+bend} {ya}, {x+cw+bend} {yb}, {x+cw+4} {yb}" '
                     f'fill="none" stroke="#cc2222" stroke-width="1.6" marker-end="url(#ar)"/>\n')
        cy = y0 + PM * rowh + 16
        if k is None:
            body += txt(x, cy, "initial", 13, anchor="start")
            body += txt(x, cy + 16, "array", 13, anchor="start")
        else:
            body += txt(x, cy, f"insert {k}", 13, anchor="start")
            np_ = len(path)
            body += txt(x, cy + 16, f"{np_} probe" + ("" if np_ == 1 else "s"), 13, anchor="start",
                        fill=("#cc2222" if np_ > 1 else "#444"))
    write(name, svg(34 + len(states) * panel + 4, y0 + PM * rowh + 40, body))
    return table


rnd = probe_figure("03-random-probing.svg", "random")
print("   random probing ->", rnd)


def probe_rw():
    """Linear probing from a table that holds 700, 50, 76: three writes, then two reads."""
    table = [700, 50, None, None, None, None, 76]
    panels = [("start", None, [], list(table), None)]
    for k in (85, 92, 101):
        path = []
        for slot in probe_sequence(k, "linear"):
            path.append(slot)
            if table[slot] is None:
                table[slot] = k
                break
        panels.append(("write", f"insert {k}", path, list(table), "new"))
    for k in (101, 64):
        path = []
        for slot in probe_sequence(k, "linear"):
            path.append(slot)
            if table[slot] is None or table[slot] == k:
                break
        panels.append(("read", f"search {k}", path, list(table),
                       "found" if table[path[-1]] == k else "empty"))
    rowh, cw, panel, y0 = 30, 54, 96, 58
    body = ""
    xs = []
    for pi, (kind, label, path, tab, end) in enumerate(panels):
        x = 34 + pi * panel + (36 if kind == "read" else 0)
        xs.append(x)
        for r in range(PM):
            y = y0 + r * rowh
            if pi == 0:
                body += txt(x - 8, y + 20, str(r), 13, anchor="end", fill="#444")
            v = tab[r]
            fill, dash = "#fff", ""
            if path and r == path[-1]:
                fill = {"new": LL_BLUE, "found": "#bfe3bf", "empty": "#fff7d6"}[end]
                if end == "empty":
                    dash = ' stroke-dasharray="4 3"'
            elif r in path:
                fill = "#f9d6d6"                # probed and occupied by another key
            body += (f'  <rect x="{x}" y="{y}" width="{cw}" height="{rowh-4}" fill="{fill}" '
                     f'stroke="#111" stroke-width="1"{dash}/>\n')
            if v is not None:
                body += txt(x + cw / 2, y + 19, str(v), 14)
        if len(path) > 1:
            for j, slot in enumerate(path):
                yc = y0 + slot * rowh + (rowh - 4) / 2
                body += (f'  <circle cx="{x+cw+26}" cy="{yc}" r="8" fill="#fff" stroke="#cc2222" '
                         f'stroke-width="1.2"/>\n')
                body += txt(x + cw + 26, yc + 4, str(j + 1), 11, fill="#cc2222", weight="bold")
            for a, b in zip(path, path[1:]):
                ya, yb = y0 + a * rowh + (rowh - 4) / 2, y0 + b * rowh + (rowh - 4) / 2
                body += (f'  <path d="M {x+cw+1} {ya} C {x+cw+12} {ya}, {x+cw+12} {yb}, {x+cw+4} {yb}" '
                         f'fill="none" stroke="#cc2222" stroke-width="1.6" marker-end="url(#ar)"/>\n')
        cy = y0 + PM * rowh + 16
        if label is None:
            body += txt(x, cy, "start", 13, anchor="start")
            body += txt(x, cy + 16, "3 keys stored", 13, anchor="start", fill="#444")
        else:
            body += txt(x, cy, label, 13, anchor="start")
            n = len(path)
            note = {"new": f"{n} probe" + ("" if n == 1 else "s"),
                    "found": f"found, {n} probes", "empty": f"empty slot: not there"}[end]
            body += txt(x, cy + 16, note, 13, anchor="start", fill=("#cc2222" if n > 1 else "#444"))
    # group headers and the line between writing and reading
    w_end, r_start = xs[3] + cw + 40, xs[4] - 4
    body += (f'  <rect x="{xs[0]-6}" y="6" width="{w_end-xs[0]+6}" height="26" rx="6" fill="#eef7fb"/>\n'
             + txt((xs[0] + w_end) / 2, 25, "Write: insert in the first free slot", 15, weight="bold"))
    body += (f'  <rect x="{r_start}" y="6" width="{xs[5]+cw+40-r_start}" height="26" rx="6" fill="#eef7fb"/>\n'
             + txt((r_start + xs[5] + cw + 40) / 2, 25, "Read: same probes", 15, weight="bold"))
    xm = (w_end + r_start) / 2
    body += f'  <line x1="{xm}" y1="8" x2="{xm}" y2="{y0+PM*rowh+36}" stroke="#999" stroke-width="1.4"/>\n'
    write("03-linear-probing.svg", svg(xs[5] + cw + 64, y0 + PM * rowh + 40, body))
    return table


print("   linear probing ->", probe_rw())

# 8. overview: four data structures side by side (slide "Data Structures") ----
OK, BAD = "#0a7d3e", "#cc2222"


def ov_cell(x, y, w, h, label, fill="#fff", fs=17):
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#111" '
            f'stroke-width="1.3"/>\n') + txt(x + w / 2, y + h / 2 + 6, label, fs)


def arrow(x1, y1, x2, y2, color="#111", sw=1.6, marker="a", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d} '
            f'marker-end="url(#{marker})"/>\n')


VAL = "#555"             # values are written in grey italics, keys in black on blue


def val_cell(x, y, w, h, label):
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="#111" '
            f'stroke-width="1.3"/>\n') + txt(x + w / 2, y + h / 2 + 5, label, 15, fill=VAL, style="italic")


def overview():
    body = ""
    panels = [("Array", 0, 250, "the index is the key"),
              ("Linked list", 264, 372, "nodes joined by pointers"),
              ("Binary search tree", 650, 245, "smaller left, larger right"),
              ("Hash table", 909, 290, "the key's hash gives the slot")]
    for name, x, w, cap in panels:
        body += (f'  <rect x="{x+2}" y="2" width="{w-4}" height="286" rx="12" fill="#f6fbfd" '
                 f'stroke="#cceef9" stroke-width="2"/>\n')
        body += txt(x + w / 2, 34, name, 21, weight="bold")
        body += txt(x + w / 2, 272, cap, 16, fill="#333", style="italic")
    # array: values in the cells, the index is the key
    x0, y0, cw = 15, 130, 44
    for i, v in enumerate(["Ana", "Ben", "Cem", "Dan", "Eva"]):
        body += val_cell(x0 + i * cw, y0, cw, 46, v)
        body += (f'  <rect x="{x0+i*cw+6}" y="{y0+56}" width="{cw-12}" height="22" rx="4" fill="{LL_BLUE}"/>\n'
                 + txt(x0 + i * cw + cw / 2, y0 + 72, str(i), 15, weight="bold"))
    body += txt(x0 + 3.5 * cw, 80, "a[3]", 17, fill="#1f6fb2", weight="bold")
    body += arrow(x0 + 3.5 * cw, 88, x0 + 3.5 * cw, y0 - 4, color="#1f6fb2", marker="ab")
    body += txt(x0 + cw / 2, y0 + 98, "key", 13, fill="#1f6fb2", style="italic")
    body += txt(x0 + cw / 2, y0 - 8, "value", 13, fill=VAL, style="italic")
    # linked list: [key | value | next]
    y, kw, vw, pw, gap = 130, 28, 34, 18, 12
    nw = kw + vw + pw
    xs = [325 + i * (nw + gap) for i in range(3)]
    body += txt(287, y + 29, "head", 16, weight="bold")
    body += arrow(307, y + 23, xs[0] - 3, y + 23)
    for i, (x, k, v) in enumerate(zip(xs, [7, 21, 42], ["Ana", "Ben", "Cem"])):
        body += ov_cell(x, y, kw, 46, str(k), LL_BLUE)
        body += (f'  <rect x="{x+kw}" y="{y}" width="{vw}" height="46" fill="#fff" stroke="#111" stroke-width="1.3"/>\n'
                 + txt(x + kw + vw / 2, y + 28, v, 14, fill=VAL, style="italic"))
        body += ov_cell(x + kw + vw, y, pw, 46, "")
        body += f'  <circle cx="{x+nw-pw/2}" cy="{y+23}" r="3" fill="#111"/>\n'
        nxt = xs[i + 1] - 3 if i < 2 else x + nw + 16
        body += arrow(x + nw - pw / 2, y + 23, nxt, y + 23)
    body += txt(xs[2] + nw + 19, y + 28, "NIL", 14, anchor="start", weight="bold")
    for lab, dx, col in [("key", kw / 2, "#1f6fb2"), ("value", kw + vw / 2, VAL), ("next", kw + vw + pw / 2 + 5, "#111")]:
        body += txt(xs[0] + dx, y + 66, lab, 12, fill=col, style="italic")
    # binary search tree: keys only
    cx = 772
    pos = {"21": (cx, 72), "7": (cx - 60, 136), "42": (cx + 60, 136),
           "2": (cx - 90, 200), "13": (cx - 30, 200), "34": (cx + 30, 200), "57": (cx + 90, 200)}
    for a, b in [("21", "7"), ("21", "42"), ("7", "2"), ("7", "13"), ("42", "34"), ("42", "57")]:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        body += f'  <line x1="{x1}" y1="{y1+14}" x2="{x2}" y2="{y2-14}" stroke="#111" stroke-width="1.4"/>\n'
    for k, (x, yy) in pos.items():
        body += node(x, yy, k, fill=LL_BLUE, fs=17, w=40, h=28, sw=1.3)
    body += txt(cx, 244, "(values not shown)", 13, fill=VAL, style="italic")
    # hash table: slot | key | value
    tx, ty, rh = 1036, 62, 34
    for i in range(5):
        body += ov_cell(tx, ty + i * rh, 26, rh, str(i), "#eeeeee", fs=14)
        body += ov_cell(tx + 26, ty + i * rh, 50, rh, "", "#fff")
        body += ov_cell(tx + 76, ty + i * rh, 74, rh, "", "#fff")
    for key, val, slot in [("Ana", 34, 3), ("Ben", 16, 1)]:
        yy = ty + slot * rh
        body += ov_cell(tx + 26, yy, 50, rh, key, LL_BLUE, fs=15)
        body += txt(tx + 113, yy + rh / 2 + 5, str(val), 15, fill=VAL, style="italic")
        body += txt(922, yy + rh / 2 + 6, f'"{key}"', 16, anchor="start", fill="#1f6fb2", weight="bold")
        body += arrow(970, yy + rh / 2, tx - 3, yy + rh / 2, color="#1f6fb2", marker="ab")
    body += txt(1000, ty + 2 * rh + rh / 2 + 5, "h(key)", 14, fill="#1f6fb2", style="italic")
    body += txt(tx + 51, ty + 5 * rh + 18, "key", 13, fill="#1f6fb2", style="italic")
    body += txt(tx + 113, ty + 5 * rh + 18, "value", 13, fill=VAL, style="italic")
    return svg(1200, 290, body)


write("03-data-structures.svg", overview())


# 17. editing vs search: an array and a linked list, sorted by key ---------------
def edit_vs_search():
    body = ""
    # array, sorted: reading position i is one step, inserting 8 shifts everything after it
    body += txt(20, 28, "Array, sorted", 23, anchor="start", weight="bold")
    x0, y0, cw = 20, 44, 56
    for i, v in enumerate([2, 4, 7, 9, 13, 21, ""]):
        body += ov_cell(x0 + i * cw, y0, cw, 48, str(v), "#fde3e3" if i >= 3 and v != "" else "#fff", fs=20)
    for i in (3, 4, 5):
        xa, xb = x0 + i * cw + cw / 2, x0 + (i + 1) * cw + cw / 2
        body += (f'  <path d="M {xa} {y0+50} Q {(xa+xb)/2} {y0+80} {xb-3} {y0+52}" fill="none" '
                 f'stroke="{BAD}" stroke-width="2" marker-end="url(#ar)"/>\n')
    body += txt(20, 158, "✓ search: jump to any index by position", 19, anchor="start", fill=OK)
    body += txt(20, 186, "✗ insert 8 in position 4: shift 9, 13, 21", 19, anchor="start", fill=BAD)
    # linked list: inserting 8 changes two pointers, searching follows every pointer
    body += txt(20, 244, "Linked list, sorted", 23, anchor="start", weight="bold")
    y, kw, pw, gap = 260, 42, 20, 20
    xs = [76 + i * (kw + pw + gap) for i in range(4)]
    body += txt(34, y + 29, "head", 17, weight="bold")
    body += arrow(56, y + 23, xs[0] - 3, y + 23)
    for i, (x, v) in enumerate(zip(xs, [2, 7, 9, 13])):
        body += ov_cell(x, y, kw, 46, str(v), LL_BLUE, fs=20)
        body += ov_cell(x + kw, y, pw, 46, "")
        body += f'  <circle cx="{x+kw+pw/2}" cy="{y+23}" r="3.5" fill="#111"/>\n'
        if i < 3:
            dash, col = ("5 4", "#999") if i == 1 else ("", "#111")
            body += arrow(x + kw + pw / 2, y + 23, xs[i + 1] - 3, y + 23, color=col, dash=dash)
    body += arrow(xs[3] + kw + pw / 2, y + 23, xs[3] + kw + pw + 20, y + 23)
    body += txt(xs[3] + kw + pw + 24, y + 29, "NIL", 16, anchor="start", weight="bold")
    # the new node 8 sits below the gap between 7 and 9
    nx, ny = xs[1] + kw + pw + gap / 2 - (kw + pw) / 2, y + 86
    body += ov_cell(nx, ny, kw, 46, "8", "#fde3e3", fs=20)
    body += ov_cell(nx + kw, ny, pw, 46, "")
    body += f'  <circle cx="{nx+kw+pw/2}" cy="{ny+23}" r="3.5" fill="#111"/>\n'
    x7 = xs[1] + kw + pw / 2                            # 7.next now points down to 8
    body += (f'  <line x1="{x7}" y1="{y+23}" x2="{x7}" y2="{ny-4}" stroke="{OK}" stroke-width="2.2" '
             f'marker-end="url(#ag)"/>\n')
    x9 = xs[2] + kw / 2                                 # 8.next points up to 9
    body += (f'  <path d="M {nx+kw+pw/2} {ny+23} L {x9-8} {ny+23} Q {x9} {ny+23} {x9} {ny+15} L {x9} {y+50}" '
             f'fill="none" stroke="{OK}" stroke-width="2.2" marker-end="url(#ag)"/>\n')
    body += txt(20, 432, "✓ insert 8: change two pointers", 19, anchor="start", fill=OK)
    body += txt(20, 460, "✗ search: follow every pointer from head", 19, anchor="start", fill=BAD)
    # what we want
    body += (f'  <rect x="20" y="486" width="470" height="70" rx="10" fill="#f6fbfd" stroke="#1f6fb2" '
             f'stroke-width="2"/>\n')
    body += txt(255, 516, "Wanted: fast search and cheap editing", 20, weight="bold")
    body += txt(255, 543, "next: binary search, then binary search trees", 17, fill="#333", style="italic")
    defs = ('  <defs><marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
            f'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{OK}"/></marker></defs>\n')
    return svg(510, 562, defs + body)


write("03-edit-vs-search.svg", edit_vs_search())


# blockchain: a linked list in which each block points back to the previous one by its hash
def blockchain():
    body = ""
    bw, bh, gap, y = 158, 112, 48, 20
    blocks = [("Block 1", "none", "7c1e"), ("Block 2", "7c1e", "a3f9"),
              ("Block 3", "a3f9", "51d0"), ("Block 4", "51d0", "e82b")]
    for i, (name, prev, own) in enumerate(blocks):
        x = 10 + i * (bw + gap)
        body += (f'  <rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="8" fill="#f6fbfd" '
                 f'stroke="#111" stroke-width="1.5"/>\n')
        body += txt(x + bw / 2, y + 24, name, 17, weight="bold")
        body += (f'  <rect x="{x+10}" y="{y+36}" width="{bw-20}" height="28" fill="{LL_BLUE}" stroke="#111"/>\n'
                 + txt(x + bw / 2, y + 56, f"prev: {prev}", 15))
        body += (f'  <rect x="{x+10}" y="{y+70}" width="{bw-20}" height="28" fill="#fff" stroke="#111"/>\n'
                 + txt(x + bw / 2, y + 90, "data: transactions", 14, fill=VAL, style="italic"))
        body += txt(x + bw / 2, y + bh + 22, f"hash {own}", 15, fill="#1f6fb2", weight="bold")
        if i > 0:
            body += arrow(x + 10, y + 50, x - gap + 3, y + 50, color="#1f6fb2", sw=2, marker="ab")
    x = 10 + 4 * (bw + gap)
    body += (f'  <rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="8" fill="#fff" stroke="#0a7d3e" '
             f'stroke-width="1.8" stroke-dasharray="6 4"/>\n')
    body += txt(x + bw / 2, y + 50, "new block", 17, fill=OK, weight="bold")
    body += txt(x + bw / 2, y + 76, "only appended", 15, fill=OK, style="italic")
    body += arrow(x + 10, y + 50, x - gap + 3, y + 50, color=OK, sw=2, marker="ag", dash="6 4")
    defs = ('  <defs><marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
            f'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{OK}"/></marker></defs>\n')
    return svg(10 + 5 * bw + 4 * gap + 10, y + bh + 34, defs + body)


write("03-blockchain.svg", blockchain())


# array with a huge index range and few values: most cells are empty
def array_gaps():
    body = ('  <defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" '
            'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#c8c8c8" '
            'stroke-width="3"/></pattern></defs>\n')
    rows = [("1", "Ana"), ("2", None), ("3", None), ("4", "Ben"), ("5", None), ("6", None), ("⋮", "gap"),
            ("500,000", "Cem"), ("⋮", "gap"), ("999,999", None), ("1,000,000", "Dan")]
    y, rh, x, w = 10, 36, 118, 120
    for idx, v in rows:
        if v == "gap":
            body += txt(x + w / 2, y + 24, "⋮", 24, fill="#666")
            body += txt(x - 12, y + 24, "", 14)
        else:
            fill = "#fff" if v else "url(#hatch)"
            body += (f'  <rect x="{x}" y="{y}" width="{w}" height="{rh-4}" fill="{fill}" stroke="#111" '
                     f'stroke-width="1.2"/>\n')
            body += txt(x - 10, y + 21, f"[{idx}]", 15, anchor="end", fill="#1f6fb2")
            if v:
                body += txt(x + w / 2, y + 22, v, 17)
        y += rh
    body += txt(x + w / 2, y + 22, "4 values,", 17, weight="bold")
    body += txt(x + w / 2, y + 44, "1,000,000 cells", 17, weight="bold", fill=BAD)
    body += (f'  <rect x="{x+w+14}" y="48" width="18" height="18" fill="url(#hatch)" stroke="#111"/>\n'
             + txt(x + w + 38, 62, "empty,", 14, anchor="start", fill="#444")
             + txt(x + w + 38, 80, "but uses", 14, anchor="start", fill="#444")
             + txt(x + w + 38, 98, "memory", 14, anchor="start", fill="#444"))
    return svg(x + w + 104, y + 54, body, defs=False)


write("03-array-gaps.svg", array_gaps())


# hash function: many possible keys K mapped onto m slots
def hash_map():
    body = ""
    body += (f'  <ellipse cx="120" cy="150" rx="108" ry="136" fill="#f6fbfd" stroke="#1f6fb2" '
             f'stroke-width="2"/>\n')
    body += txt(120, 40, "K", 26, weight="bold", style="italic", fill="#1f6fb2")
    body += txt(120, 62, "all possible keys", 14, fill="#1f6fb2", style="italic")
    keys = [("Ana", 80, 98, 0), ("Ben", 150, 124, 1), ("Zoe", 76, 156, 3),
            ("2010-01-01", 136, 192, 3), ("Moritz", 84, 228, 4), ("…", 160, 252, None)]
    sx, sy, sh = 330, 70, 40
    for j in range(5):
        lab = "m−1" if j == 4 else str(j)
        body += ov_cell(sx, sy + j * sh, 50, sh, lab, "#eeeeee" if j < 4 else "#eeeeee", fs=16)
    body += txt(sx + 25, sy - 16, "m slots", 15, fill="#333", style="italic")
    for k, x, y, slot in keys:
        body += txt(x, y + 5, k, 15, weight="bold")
        if slot is not None:
            ys = sy + slot * sh + sh / 2
            body += arrow(x + 4.5 * len(k) + 6, y, sx - 3, ys, color="#1f6fb2", sw=1.5, marker="ab")
    body += txt(282, 52, "h", 22, style="italic", fill="#1f6fb2", weight="bold")
    return svg(400, 300, body)


write("03-hash-function.svg", hash_map())


# a Python dict as a hash table: three keys, eight slots, one collision, one lookup
def python_dict():
    MONO = 'font-family="DejaVu Sans Mono, Consolas, monospace"'
    body = ""
    # the code
    body += (f'  <rect x="10" y="10" width="300" height="168" rx="8" fill="#f2f2f2" stroke="#999"/>\n')
    lines = ['ages = {}', 'ages["Ana"] = 34', 'ages["Ben"] = 16', 'ages["Cem"] = 51', 'ages["Ben"]']
    for i, t in enumerate(lines):
        body += (f'  <text x="26" y="{42+i*30}" font-size="19" {MONO} fill="#111">'
                 f'{t.replace("<", "&lt;")}</text>\n')
    body += txt(176, 162, "→ 16", 19, anchor="start", fill=OK, weight="bold")
    # the hash of each key, and its slot
    rows = [("Ana", 4619, 3, OK), ("Ben", 9813, 5, OK), ("Cem", 2755, 3, BAD)]
    hy = {}
    for i, (k, h, slot, col) in enumerate(rows):
        y = 232 + i * 76
        hy[k] = y
        body += txt(14, y, f'hash("{k}") = {h}', 19, anchor="start")
        body += txt(14, y + 28, f'{h} mod 8 = {slot}', 19, anchor="start", fill=col)
    # the table: slot | hash | key | value
    tx, ty, rh = 420, 46, 50
    cols = [("slot", 46), ("hash", 76), ("key", 84), ("value", 76)]
    x = tx
    for name, w in cols:
        body += txt(x + w / 2, ty - 12, name, 16, fill="#444", style="italic")
        x += w
    content = {3: ("4619", "Ana", "34"), 5: ("9813", "Ben", "16"), 0: ("2755", "Cem", "51")}
    for r in range(8):
        y = ty + r * rh
        x = tx
        fill_row = "#bfe3bf" if r == 5 else "#fff"
        for ci, (name, w) in enumerate(cols):
            fill = "#eeeeee" if ci == 0 else (LL_BLUE if ci == 2 and r in content else fill_row)
            body += (f'  <rect x="{x}" y="{y}" width="{w}" height="{rh}" fill="{fill}" stroke="#111" '
                     f'stroke-width="1.2"/>\n')
            label = str(r) if ci == 0 else (content[r][ci - 1] if r in content else "")
            body += txt(x + w / 2, y + rh / 2 + 7, label, 19,
                        fill=(VAL if ci == 3 else "#111"), style=("italic" if ci == 3 else "normal"))
            x += w
    def slot_y(r):
        return ty + r * rh + rh / 2
    # Ana and Ben go straight to their slots
    for k, slot in (("Ana", 3), ("Ben", 5)):
        body += arrow(240, hy[k] + 20, tx - 4, slot_y(slot), color=OK, sw=2, marker="ag")
    # Cem collides with Ana in slot 3 and probes on to slot 0
    yc = hy["Cem"] + 20
    body += arrow(240, yc, tx - 4, slot_y(3) + 12, color=BAD, sw=2, marker="ar")
    body += txt(352, slot_y(3) + 66, "taken", 16, fill=BAD, weight="bold")
    body += (f'  <path d="M {tx-4} {slot_y(3)+4} C {tx-70} {slot_y(3)-30}, {tx-70} {slot_y(0)+10}, {tx-4} {slot_y(0)}" '
             f'fill="none" stroke="{BAD}" stroke-width="2" stroke-dasharray="6 4" marker-end="url(#ar)"/>\n')
    body += txt(tx - 76, slot_y(1) + 8, "probe", 16, anchor="end", fill=BAD, weight="bold")
    # the lookup of "Ben"
    xe = tx + sum(w for _, w in cols)
    body += (f'  <path d="M {xe+6} {slot_y(5)} l 22 0" stroke="{OK}" stroke-width="2"/>\n'
             + txt(xe + 32, slot_y(5) - 6, 'ages["Ben"]:', 15, anchor="start", fill=OK, weight="bold")
             + txt(xe + 32, slot_y(5) + 14, "key matches,", 15, anchor="start", fill=OK)
             + txt(xe + 32, slot_y(5) + 32, "return 16", 15, anchor="start", fill=OK))
    body += txt(tx, ty + 8 * rh + 30, "8 slots; hash values made up for the example", 14, anchor="start",
                fill="#555", style="italic")
    defs = ('  <defs><marker id="ag" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
            f'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{OK}"/></marker></defs>\n')
    return svg(xe + 150, ty + 8 * rh + 40, defs + body)


write("03-python-dict.svg", python_dict())

print("deck 3 figures written to", OUT)
