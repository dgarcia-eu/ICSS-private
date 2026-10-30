#!/usr/bin/env python3
"""Generate the figures of the theory-exercise solutions as SVG.

    python3 tools/gensolfigs.py        # writes TheoryExercises/figures/sol-*.svg

Everything is drawn with matplotlib from the data of the solutions (traces are
recomputed here, not copied), so a figure cannot disagree with the text unless
the data in this script is changed.
"""
import math
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, FancyBboxPatch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "TheoryExercises", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif",
                     "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"], "font.size": 11})
BLUE, GREY, RED, GREEN, LIGHT = "#1f77b4", "#8a8a8a", "#d62728", "#2e8b3a", "#cceef9"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("  ", name)


def clean(ax, xlim=None, ylim=None):
    ax.set_axis_off()
    if xlim: ax.set_xlim(*xlim)
    if ylim: ax.set_ylim(*ylim)
    ax.set_aspect("equal")


def node(ax, x, y, label, r=0.32, fc="white", ec="#111", fs=11, lw=1.2, text_color="#111"):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs if len(str(label)) < 3 else fs * 0.8, zorder=4, color=text_color)


def edge(ax, p, q, r=0.32, color="#111", lw=1.2, arrow=False, style="-", rad=0.0, label=None, lpos=0.5, loff=(0, 0), lcolor="#111", shrink=True):
    """Edge between two node centers, shortened by r at both ends (geometrically, in data units).
    rad > 0 bulges to the right of the direction p -> q (matplotlib's arc3 convention)."""
    (x1, y1), (x2, y2) = p, q
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = dy / L, -dx / L                       # right-hand normal of p -> q
    cx, cy = (x1 + x2) / 2 + nx * rad * L, (y1 + y2) / 2 + ny * rad * L   # arc3 control point
    def shorten(a, b, r):
        vx, vy = b[0] - a[0], b[1] - a[1]; m = math.hypot(vx, vy) or 1
        return (a[0] + vx / m * r, a[1] + vy / m * r)
    if shrink:
        p2 = shorten(p, (cx, cy), r); q2 = shorten(q, (cx, cy), r)
    else:
        p2, q2 = p, q
    if arrow or rad:
        a = FancyArrowPatch(p2, q2, arrowstyle="-|>" if arrow else "-", mutation_scale=14, color=color, lw=lw,
                            linestyle=style, connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=2)
        ax.add_patch(a)
    else:
        ax.plot([p2[0], q2[0]], [p2[1], q2[1]], color=color, lw=lw, linestyle=style, zorder=1, solid_capstyle="round")
    if label is not None:
        t = lpos
        # point on the quadratic Bezier at parameter t
        mx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t ** 2 * x2 + loff[0]
        my = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t ** 2 * y2 + loff[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=10, color=lcolor, zorder=5,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))


# ------------------------------------------------------------ binary trees
def tree_positions(t, depth=0, x=[0], pos=None):
    """In-order layout: t = (label, left, right) or None. Returns {id: (x, y)}."""
    if pos is None:
        pos = {}
        x[0] = 0
    if t is None:
        return pos
    tree_positions(t[1], depth + 1, x, pos)
    pos[id(t)] = (x[0], -depth)
    x[0] += 1
    tree_positions(t[2], depth + 1, x, pos)
    return pos


def draw_tree(ax, t, pos, r=0.3, hl=(), fs=11, edge_labels=None, sx=1.0, sy=1.0, ox=0.0, oy=0.0):
    if t is None:
        return
    x, y = pos[id(t)]
    x, y = x * sx + ox, y * sy + oy
    for child, side in ((t[1], "L"), (t[2], "R")):
        if child is not None:
            cx, cy = pos[id(child)]
            cx, cy = cx * sx + ox, cy * sy + oy
            edge(ax, (x, y), (cx, cy), r=r)
            if edge_labels:
                lab = edge_labels(t, side)
                if lab:
                    ax.text((x + cx) / 2 + (-0.12 if side == "L" else 0.12), (y + cy) / 2 + 0.05, lab,
                            ha="right" if side == "L" else "left", va="center", fontsize=9, color=GREY)
            draw_tree(ax, child, pos, r, hl, fs, edge_labels, sx, sy, ox, oy)
    node(ax, x, y, str(t[0]), r=r, fc="#ffe9a8" if t[0] in hl else "white", fs=fs)


def T(v, l=None, r=None):
    return (v, l, r)


# ================================================================ sheet 2
def fig_02_dice():
    # question tree; leaves are faces with code words
    tree = T("7 or 8?",
             T("7?", T("7 · 11"), T("8 · 10")),
             T("5 or 6?", T("5?", T("5 · 011"), T("6 · 010")),
               T("1 or 2?", T("1?", T("1 · 0011"), T("2 · 0010")),
                 T("3?", T("3 · 0001"), T("4 · 0000")))))
    pos = tree_positions(tree)
    fig, ax = plt.subplots(figsize=(9, 4.6))

    def lab(t, side):
        return "yes = 1" if side == "L" else "no = 0"
    # draw with rectangles for questions, circles for faces
    def draw(t):
        x, y = pos[id(t)]
        x, y = x * 0.75, y * 1.05
        for child, side in ((t[1], "L"), (t[2], "R")):
            if child is None: continue
            cx, cy = pos[id(child)]; cx, cy = cx * 0.75, cy * 1.05
            ax.plot([x, cx], [y - 0.18, cy + 0.18], color="#111", lw=1.1, zorder=1)
            ax.text((x + cx) / 2 + (-0.1 if side == "L" else 0.1), (y + cy) / 2 + 0.02, "1" if side == "L" else "0",
                    ha="right" if side == "L" else "left", va="center", fontsize=10, color=BLUE, fontweight="bold")
            draw(child)
        leaf = t[1] is None
        lab_ = str(t[0])
        if leaf:
            face, code = lab_.split(" · ")
            ax.add_patch(FancyBboxPatch((x - 0.36, y - 0.19), 0.72, 0.38, boxstyle="round,pad=0.02", fc="#ffe9a8", ec="#111", lw=1, zorder=3))
            ax.text(x, y + 0.02, face, ha="center", va="center", fontsize=11, fontweight="bold", zorder=4)
            ax.text(x, y - 0.42, code, ha="center", va="center", fontsize=10, color=BLUE, family="monospace", zorder=4)
        else:
            ax.add_patch(FancyBboxPatch((x - 0.5, y - 0.18), 1.0, 0.36, boxstyle="round,pad=0.02", fc="white", ec="#111", lw=1, zorder=3))
            ax.text(x, y, lab_, ha="center", va="center", fontsize=10, zorder=4)
    draw(tree)
    ax.text(0.0, 0.55, "left branch: yes (bit 1) · right branch: no (bit 0)", fontsize=9, color=GREY, ha="left")
    clean(ax, (-0.6, 11.2), (-4.9, 0.8))
    save(fig, "sol-02-dice-tree.svg")


# ================================================================ sheet 3
def fig_03_hash():
    keys = [6, 0, 2, 12, 3, 11, 10, 1, 14, 9]
    m = 8
    chains = {s: [] for s in range(m)}
    for k in keys:
        chains[(2 * k + 3) % m].append(k)
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    for s in range(m):
        y = -s * 0.5
        ax.add_patch(Rectangle((0, y - 0.2), 0.7, 0.4, fc=LIGHT if chains[s] else "#eeeeee", ec="#111", lw=1))
        ax.text(0.35, y, str(s), ha="center", va="center", fontsize=11, fontweight="bold")
        x = 1.3
        if not chains[s]:
            ax.text(0.95, y, "∅", ha="left", va="center", fontsize=11, color=GREY)
        for i, k in enumerate(chains[s]):
            ax.add_patch(Rectangle((x, y - 0.2), 0.7, 0.4, fc="#ffe9a8", ec="#111", lw=1))
            ax.text(x + 0.35, y, str(k), ha="center", va="center", fontsize=11)
            x0 = 0.7 if i == 0 else x - 0.6
            ax.add_patch(FancyArrowPatch((x0, y), (x, y), arrowstyle="-|>", mutation_scale=12, color="#111", lw=1))
            x += 1.3
    ax.text(0.35, 0.45, "slot", ha="center", fontsize=10, color=GREY)
    ax.text(1.3, 0.45, "chain (in insertion order)", ha="left", fontsize=10, color=GREY)
    ax.text(0, -4.1, "h(x) = (2x + 3) mod 8 is always odd: slots 0, 2, 4, 6 are never used", fontsize=10, color=RED)
    clean(ax, (-0.1, 6.6), (-4.4, 0.7))
    save(fig, "sol-03-hash-chaining.svg")


def fig_03_binary_search():
    A = [10, 19, 26, 27, 31, 33, 34, 35, 42, 44]
    steps = [(1, 10, 5), (6, 10, 8), (6, 7, 6)]
    fig, ax = plt.subplots(figsize=(8, 3.4))
    for r, (lo, hi, mid) in enumerate(steps):
        y = -r * 1.25
        ax.text(-0.3, y, f"step {r + 1}", ha="right", va="center", fontsize=10)
        for i, v in enumerate(A, start=1):
            active = lo <= i <= hi
            fc = "#ffe9a8" if i == mid else (LIGHT if active else "#f2f2f2")
            ax.add_patch(Rectangle((i - 1, y - 0.25), 1, 0.5, fc=fc, ec="#111" if active else "#bbbbbb", lw=1))
            ax.text(i - 0.5, y, str(v), ha="center", va="center", fontsize=11, color="#111" if active else GREY)
            if r == 0:
                ax.text(i - 0.5, 0.45, str(i), ha="center", va="center", fontsize=9, color=GREY)
        marks = {}
        for name, i, col in (("lo", lo, BLUE), ("hi", hi, BLUE), ("mid", mid, RED)):
            marks.setdefault(i, []).append((name, col))
        for i, ms in marks.items():
            ax.text(i - 0.5, y - 0.3, " = ".join(n for n, _ in ms), ha="center", va="top", fontsize=9,
                    color=RED if any(n == "mid" for n, _ in ms) else BLUE, fontweight="bold")
        note = {0: "A[5] = 31 < 33 → search right", 1: "A[8] = 35 > 33 → search left", 2: "A[6] = 33 found"}[r]
        ax.text(10.3, y, note, ha="left", va="center", fontsize=10)
    ax.text(-0.3, 0.45, "position", ha="right", va="center", fontsize=9, color=GREY)
    clean(ax, (-1.5, 15.2), (-3.3, 0.8))
    save(fig, "sol-03-binary-search.svg")


def fig_03_bst():
    tb = T(4, T(2, T(1), T(3)), T(6, None, T(10, None, T(12))))
    tc = T(4, T(2, T(1), T(3)), T(10, T(6), T(12)))
    td1 = T(4, T(2, T(1), T(3)), T(12, T(6), None))
    td2 = T(4, T(2, T(1), T(3)), T(6, None, T(12)))
    fig, axes = plt.subplots(1, 4, figsize=(11, 3.2))
    for ax, t, title, hl in zip(axes, [tb, tc, td1, td2],
                                ["(a) inserted 4, 6, 2, 1, 3, 10, 12", "(b) same keys, depth 3",
                                 "(c) 10 replaced by successor 12", "(c) 10 replaced by predecessor 6"],
                                [(), (10, 6), (12,), (6,)]):
        pos = tree_positions(t)
        draw_tree(ax, t, pos, r=0.3, hl=hl, sx=0.75, sy=0.9)
        ax.set_title(title, fontsize=10)
        clean(ax, (-0.6, 5.3), (-3.3, 0.5))
    save(fig, "sol-03-bst.svg")


# ================================================================ sheet 4
# The 2026 sheet 4 has no OOP exercise; this figure is kept in figures/unused/.
def fig_04_inheritance():
    fig, ax = plt.subplots(figsize=(8.5, 3.6))
    boxes = {"RectangularObject": (1.6, 3.0, "x, y, width, height"), "MovingObject": (1.6, 1.6, "+ speed"),
             "LivingObject": (6.2, 3.0, "hp"), "FightingObject": (5.2, 1.6, "+ dmg"), "Healer": (7.6, 1.6, "+ healing"),
             "Hero": (3.4, 0.2, "+ dmg, healing (optional)")}
    for name, (x, y, attrs) in boxes.items():
        fc = "#ffe9a8" if name == "Hero" else LIGHT
        ax.add_patch(FancyBboxPatch((x - 1.05, y - 0.32), 2.1, 0.64, boxstyle="round,pad=0.02", fc=fc, ec="#111", lw=1.1, zorder=3))
        ax.text(x, y + 0.1, name, ha="center", va="center", fontsize=10.5, fontweight="bold", zorder=4)
        ax.text(x, y - 0.15, attrs, ha="center", va="center", fontsize=8.5, color="#333", zorder=4)

    def inherits(child, parent, rad=0.0):
        (x1, y1, _), (x2, y2, _) = boxes[child], boxes[parent]
        ax.add_patch(FancyArrowPatch((x1, y1 + 0.32), (x2, y2 - 0.32), arrowstyle="-|>", mutation_scale=16,
                                     color="#111", lw=1.2, connectionstyle=f"arc3,rad={rad}", zorder=2))
    inherits("MovingObject", "RectangularObject")
    inherits("FightingObject", "LivingObject")
    inherits("Healer", "LivingObject")
    inherits("Hero", "MovingObject", rad=0.0)
    inherits("Hero", "LivingObject", rad=-0.35)
    ax.text(3.4, -0.45, "arrow: \"inherits from\". Hero (b) inherits from MovingObject and LivingObject", ha="center", fontsize=9, color=GREY)
    clean(ax, (0.3, 8.9), (-0.7, 3.5))
    save(fig, "sol-04-inheritance.svg")


# ================================================================ sheet 5
def fig_05_bfs():
    pos = {"D": (0, 0), "A": (1.4, 0), "B": (2.8, 0), "E": (4.2, 0), "C": (5.4, 0.9), "F": (5.4, -0.9)}
    edges = [("A", "B"), ("A", "D"), ("B", "E"), ("C", "E"), ("C", "F"), ("E", "F")]
    tree = {("A", "B"), ("A", "D"), ("B", "E"), ("C", "E"), ("E", "F")}
    d = {"B": 0, "A": 1, "E": 1, "D": 2, "C": 2, "F": 2}
    par = {"B": "NIL", "A": "B", "E": "B", "D": "A", "C": "E", "F": "E"}
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    for u, v in edges:
        t = (u, v) in tree
        edge(ax, pos[u], pos[v], r=0.3, color="#111" if t else GREY, lw=2.4 if t else 1.0, style="-" if t else "--")
    for v, (x, y) in pos.items():
        node(ax, x, y, v, r=0.3, fc="#ffe9a8" if v == "B" else LIGHT)
        if v in "CF":
            ax.text(x + 0.45, y, f"d = {d[v]}\nπ = {par[v]}", ha="left", va="center", fontsize=9)
        else:
            ax.text(x, y - 0.55, f"d = {d[v]}\nπ = {par[v]}", ha="center", va="top", fontsize=9)
    ax.text(2.7, 1.45, "BFS from B: thick edges form the BFS tree, the dashed edge C–F is not in it", ha="center", fontsize=9.5, color=GREY)
    clean(ax, (-0.6, 6.9), (-1.9, 1.7))
    save(fig, "sol-05-bfs.svg")


def bellman_ford(edges, V, s):
    dist = {v: math.inf for v in V}; par = {v: None for v in V}; dist[s] = 0
    for _ in range(len(V) - 1):
        for u, v, w in edges:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w; par[v] = u
    return dist, par


def fig_05_bellman_ford():
    V = list("ABCDE")
    edges = [("A", "B", 6), ("A", "D", 7), ("B", "C", 5), ("B", "D", 8), ("B", "E", -4),
             ("C", "B", -2), ("D", "C", -3), ("D", "E", 9), ("E", "A", 3), ("E", "C", 7)]
    dist, par = bellman_ford(edges, V, "A")
    assert dist == {"A": 0, "B": 2, "C": 4, "D": 7, "E": -2}
    pos = {"A": (0, 0.8), "B": (2.2, 2.0), "D": (2.2, -0.4), "C": (4.6, 2.0), "E": (4.6, -0.4)}
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    tree = {(par[v], v) for v in V if par[v]}
    lp = {("D", "C"): 0.3, ("B", "E"): 0.72, ("E", "A"): 0.3, ("A", "D"): 0.6}
    for u, v, w in edges:
        t = (u, v) in tree
        rad = 0.25 if (v, u, None) in [(a, b, None) for a, b, _ in edges] else 0.0
        edge(ax, pos[u], pos[v], r=0.32, color="#111" if t else GREY, lw=2.4 if t else 1.0, arrow=True,
             rad=rad, label=str(w), lpos=lp.get((u, v), 0.5), lcolor="#111" if t else GREY)
    off = {"A": (0, -0.5, "center", "top"), "B": (0, 0.5, "center", "bottom"), "C": (0, 0.5, "center", "bottom"),
           "D": (0, -0.5, "center", "top"), "E": (0.45, 0, "left", "center")}
    for v, (x, y) in pos.items():
        node(ax, x, y, v, r=0.32, fc="#ffe9a8" if v == "A" else LIGHT)
        ox, oy, ha, va = off[v]
        ax.text(x + ox, y + oy, f"{dist[v]}", ha=ha, va=va, fontsize=11, color=RED, fontweight="bold")
    ax.text(2.3, -1.4, "final distances in red; thick edges form the shortest-path tree A → D → C → B → E",
            ha="center", fontsize=9.5, color=GREY)
    clean(ax, (-0.6, 5.6), (-1.7, 2.9))
    save(fig, "sol-05-bellman-ford.svg")


# ================================================================ sheet 6
def heap_tree(arr):
    def build(i):
        if i > len(arr): return None
        return T(arr[i - 1], build(2 * i), build(2 * i + 1))
    return build(1)


def fig_06_heap_reduce():
    states = [([2, 4, 5, 13, 200, 7], "before", ()),
              ([2, 4, 5, 13, 200, 1], "write 1 into position 6", (1,)),
              ([2, 4, 1, 13, 200, 5], "swap with parent (5)", (1, 5)),
              ([1, 4, 2, 13, 200, 5], "swap with parent (2): done", (1, 2))]
    fig, axes = plt.subplots(1, 4, figsize=(11, 2.9))
    for ax, (arr, title, hl) in zip(axes, states):
        t = heap_tree(arr); pos = tree_positions(t)
        draw_tree(ax, t, pos, r=0.36, hl=hl, sx=0.8, sy=1.0, fs=10)
        ax.set_title(title, fontsize=10)
        ax.text(2.0, -2.9, "[" + ", ".join(map(str, arr)) + "]", ha="center", fontsize=9, family="monospace")
        clean(ax, (-0.5, 4.6), (-3.2, 0.5))
    save(fig, "sol-06-heap-reduce.svg")


def fig_06_dfs():
    pos = {"B": (0, 1.2), "A": (0, -1.2), "C": (1.8, 0), "D": (3.8, 1.2), "E": (3.8, -1.2), "F": (5.8, 0)}
    edges = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("C", "E"), ("D", "F"), ("E", "F")]
    par = {"B": None, "A": "B", "C": "A", "D": "C", "F": "D", "E": "F"}
    d = {"B": 1, "A": 2, "C": 3, "D": 4, "F": 5, "E": 6}
    f = {"E": 7, "F": 8, "D": 9, "C": 10, "A": 11, "B": 12}
    tree = {frozenset((par[v], v)) for v in par if par[v]}
    fig, ax = plt.subplots(figsize=(7.5, 3.3))
    for u, v in edges:
        t = frozenset((u, v)) in tree
        edge(ax, pos[u], pos[v], r=0.32, color="#111" if t else GREY, lw=2.4 if t else 1.0, style="-" if t else "--")
    for v, (x, y) in pos.items():
        node(ax, x, y, v, r=0.32, fc="#ffe9a8" if v == "B" else LIGHT)
        dy = 0.5 if y >= 0 and v != "C" else -0.5
        if v == "C": dy = 0.5
        if v == "F": dy = 0.5
        ax.text(x, y + dy, f"{d[v]} / {f[v]}", ha="center", va="bottom" if dy > 0 else "top", fontsize=10, color=RED, fontweight="bold")
    ax.text(2.9, -2.45, "labels: discovery / finishing time. Thick edges: DFS tree B → A → C → D → F → E; dashed: back edges",
            ha="center", fontsize=9, color=GREY)
    clean(ax, (-0.6, 6.4), (-2.7, 2.1))
    save(fig, "sol-06-dfs.svg")


# ================================================================ sheet 7
def fig_07_mergesort():
    fig, ax = plt.subplots(figsize=(9, 5.2))

    def box(x, y, arr, fc="white"):
        s = " ".join(map(str, arr))
        w = 0.16 * len(s) + 0.3
        ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.2), w, 0.4, boxstyle="round,pad=0.02", fc=fc, ec="#111", lw=1, zorder=3))
        ax.text(x, y, s, ha="center", va="center", fontsize=9.5, family="monospace", zorder=4)
        return w

    def link(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1 - 0.2, y2 + 0.2], color=GREY, lw=1, zorder=1)

    levels_split = [[[1, 2, 10, 4, 3, 7, 9, 11]], [[1, 2, 10, 4], [3, 7, 9, 11]],
                    [[1, 2], [10, 4], [3, 7], [9, 11]], [[1], [2], [10], [4], [3], [7], [9], [11]]]
    levels_merge = [[[1, 2], [4, 10], [3, 7], [9, 11]], [[1, 2, 4, 10], [3, 7, 9, 11]], [[1, 2, 3, 4, 7, 9, 10, 11]]]
    W = 9.0
    xs_prev = None
    y = 0
    for lv, level in enumerate(levels_split):
        n = len(level); xs = [W * (i + 0.5) / n for i in range(n)]
        for i, arr in enumerate(level):
            box(xs[i], y, arr)
            if xs_prev is not None:
                link(xs_prev[i // 2], y + 1, xs[i], y)
        xs_prev = xs; y -= 1
    ax.text(-0.3, 0, "split", ha="right", va="center", fontsize=10, color=BLUE)
    ax.text(-0.3, y + 1, "", ha="right")
    y_m = y
    for lv, level in enumerate(levels_merge):
        n = len(level); xs = [W * (i + 0.5) / n for i in range(n)]
        for i, arr in enumerate(level):
            box(xs[i], y_m, arr, fc="#ffe9a8")
            link(xs_prev[2 * i], y_m + 1, xs[i], y_m); link(xs_prev[2 * i + 1], y_m + 1, xs[i], y_m)
        xs_prev = xs; y_m -= 1
    ax.text(-0.3, y_m + 1, "merge", ha="right", va="center", fontsize=10, color=BLUE)
    clean(ax, (-1.3, W + 0.3), (y_m + 0.6, 0.5))
    save(fig, "sol-07-mergesort.svg")


# ================================================================ sheet 8
def fig_08_bigo():
    import numpy as np
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    n = np.linspace(1, 200, 400)
    a1.plot(n, 200 * n + 1e6, label="f(n) = 200n + 10⁶", color=BLUE, lw=2)
    a1.plot(n, 201 * n ** 3, label="c·g(n) = 201·n³", color=RED, lw=2)
    a1.axvline(100, color=GREY, ls="--", lw=1); a1.text(102, 3e6, "n₀ = 100", fontsize=9, color=GREY)
    a1.set_yscale("log"); a1.set_xlabel("n"); a1.set_title("(a) 200n + 10⁶ ∈ O(n³)", fontsize=10); a1.legend(fontsize=8, loc="lower right")
    n2 = np.arange(1, 9)
    a2.plot(n2, np.e ** n2, "o-", label="eⁿ", color=BLUE, lw=2)
    a2.plot(n2, n2.astype(float) ** n2, "s-", label="nⁿ  (c = 1)", color=RED, lw=2)
    a2.axvline(3, color=GREY, ls="--", lw=1); a2.text(3.1, 2e-0 * 1.5, "n₀ = 3", fontsize=9, color=GREY)
    a2.set_yscale("log"); a2.set_xlabel("n"); a2.set_title("(b) eⁿ ∈ O(nⁿ)", fontsize=10); a2.legend(fontsize=8, loc="lower right")
    for a in (a1, a2):
        a.grid(alpha=0.3)
    fig.tight_layout()
    save(fig, "sol-08-big-o.svg")


# ================================================================ sheet 9
def fig_09_dfa_icss():
    fig, ax = plt.subplots(figsize=(9, 3.6))
    xs = [0, 2, 4, 6, 8]
    names = ["q0", "q1", "q2", "q3", "q4"]
    for i, (x, nm) in enumerate(zip(xs, names)):
        node(ax, x, 0, nm, r=0.36, fc="#ffe9a8" if i == 4 else LIGHT)
        if i == 4:
            ax.add_patch(Circle((x, 0), 0.44, fc="none", ec="#111", lw=1.2, zorder=3))
    ax.add_patch(FancyArrowPatch((-1.2, 0), (-0.42, 0), arrowstyle="-|>", mutation_scale=14, color="#111", lw=1.2))
    for i, sym in enumerate(["I", "C", "S", "S"]):
        edge(ax, (xs[i], 0), (xs[i + 1], 0), r=0.36, arrow=True, lw=1.6)
        ax.text((xs[i] + xs[i + 1]) / 2, 0.22, sym, ha="center", fontsize=11, fontweight="bold")

    def loop(x, label):
        a = FancyArrowPatch((x - 0.16, 0.33), (x + 0.16, 0.33), arrowstyle="-|>", mutation_scale=12, color="#111", lw=1.2,
                            connectionstyle="arc3,rad=-2.4", zorder=2)
        ax.add_patch(a)
        ax.text(x, 1.0, label, ha="center", va="center", fontsize=9.5)
    loop(0, "C, S, X"); loop(2, "I"); loop(8, "I, C, S, X")
    # arcs above: back to q0 on any symbol that is not I; arcs below: back to q1 on I
    edge(ax, (4, 0), (0, 0), r=0.36, arrow=True, rad=-0.6, label="C, S, X", lpos=0.5)
    edge(ax, (6, 0), (0, 0), r=0.36, arrow=True, rad=-0.55, label="C, S, X", lpos=0.5)
    edge(ax, (4, 0), (2, 0), r=0.36, arrow=True, rad=-0.6, label="I", lpos=0.5)
    edge(ax, (6, 0), (2, 0), r=0.36, arrow=True, rad=-0.55, label="I", lpos=0.5)
    ax.text(4, -2.35, "q0: nothing matched · q1: I · q2: IC · q3: ICS · q4: ICSS found (accepting, stays forever)",
            ha="center", fontsize=9, color=GREY)
    clean(ax, (-1.4, 9.0), (-2.6, 2.3))
    save(fig, "sol-09-dfa-icss.svg")


def fig_09_pda_stack():
    inp = list("0111X1110") + ["□"]
    stacks = [["#"], ["#", "B"], ["#", "B", "A"], ["#", "B", "A", "A"], ["#", "B", "A", "A", "A"],
              ["#", "B", "A", "A", "A"], ["#", "B", "A", "A"], ["#", "B", "A"], ["#", "B"], ["#"], []]
    states = ["Q0", "Q0", "Q0", "Q0", "Q0", "Q1", "Q1", "Q1", "Q1", "Q1", "Q1"]
    fig, ax = plt.subplots(figsize=(9.5, 3.4))
    for i, st in enumerate(stacks):
        x = i * 1.0
        for j, s in enumerate(st):
            ax.add_patch(Rectangle((x - 0.3, j * 0.42), 0.6, 0.42, fc="#ffe9a8" if s != "#" else LIGHT, ec="#111", lw=1))
            ax.text(x, j * 0.42 + 0.21, s, ha="center", va="center", fontsize=11)
        ax.plot([x - 0.4, x + 0.4], [0, 0], color="#111", lw=1.5)
        ax.text(x, -0.35, "start" if i == 0 else f"read {inp[i - 1]}", ha="center", va="top", fontsize=9)
        ax.text(x, -0.72, states[i], ha="center", va="top", fontsize=9, color=BLUE)
        if i == len(stacks) - 1:
            ax.text(x, 0.3, "empty:\naccept", ha="center", va="bottom", fontsize=9, color=GREEN, fontweight="bold")
    ax.text(5.0, 2.55, "stack after each symbol of 0111X1110□ (bottom is #); Q0 pushes, Q1 pops and checks",
            ha="center", fontsize=9.5, color=GREY)
    clean(ax, (-0.7, 10.6), (-1.2, 2.8))
    save(fig, "sol-09-pda-stack.svg")


# ================================================================ sheet 10
def fig_10_metrics():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.2), gridspec_kw={"width_ratios": [1, 1.3]})
    cm = [[60, 40], [30, 870]]
    labels = [["TP = 60", "FN = 40"], ["FP = 30", "TN = 870"]]
    cols = [["#ffe9a8", "#f7c6c6"], ["#f7c6c6", LIGHT]]
    for i in range(2):
        for j in range(2):
            a1.add_patch(Rectangle((j, 1 - i), 1, 1, fc=cols[i][j], ec="#111"))
            a1.text(j + 0.5, 1.5 - i, labels[i][j], ha="center", va="center", fontsize=11)
    a1.text(0.5, 2.15, "predicted hate", ha="center", fontsize=9); a1.text(1.5, 2.15, "predicted normal", ha="center", fontsize=9)
    a1.text(-0.1, 1.5, "hate\n(100)", ha="right", va="center", fontsize=9); a1.text(-0.1, 0.5, "normal\n(900)", ha="right", va="center", fontsize=9)
    clean(a1, (-0.9, 2.1), (-0.1, 2.4))
    names = ["accuracy", "precision", "recall", "F1"]
    model = [0.93, 60 / 90, 0.60, 2 * (60 / 90) * 0.6 / (60 / 90 + 0.6)]
    dummy = [0.90, 0.0, 0.0, 0.0]
    import numpy as np
    x = np.arange(4)
    a2.bar(x - 0.2, model, 0.4, label="classifier", color=BLUE)
    a2.bar(x + 0.2, dummy, 0.4, label="always \"normal\"", color=GREY)
    for i, (m, d) in enumerate(zip(model, dummy)):
        a2.text(i - 0.2, m + 0.02, f"{m:.2f}", ha="center", fontsize=8.5)
        a2.text(i + 0.2, d + 0.02, f"{d:.2f}", ha="center", fontsize=8.5)
    a2.set_xticks(x, names); a2.set_ylim(0, 1.1); a2.legend(fontsize=8.5, loc="upper right"); a2.set_title("the accuracy trap", fontsize=10)
    a2.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save(fig, "sol-10-metrics.svg")


def fig_10_elbow():
    K = list(range(1, 11)); wss = [8400, 5100, 3200, 2900, 2700, 2560, 2440, 2340, 2250, 2170]
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(K, wss, "o-", color=BLUE, lw=2)
    ax.plot([3], [3200], "o", color=RED, ms=11, mfc="none", mew=2)
    ax.annotate("elbow at K = 3", (3, 3200), (4.5, 5500), fontsize=10, color=RED, arrowprops=dict(arrowstyle="->", color=RED))
    for k, w0, w1 in zip(K[1:], wss[:-1], wss[1:]):
        ax.text(k - 0.5, (w0 + w1) / 2 + 250, f"−{w0 - w1}", fontsize=7.5, color=GREY, ha="center")
    ax.set_xlabel("K"); ax.set_ylabel("WSS"); ax.set_xticks(K); ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save(fig, "sol-10-elbow.svg")


# ================================================================ sheet 11
def fig_11_schema():
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    tables = {
        "Speaker": (1.4, 3.0, ["SpeakerID (PK)", "Name", "BirthYear", "Constituency"]),
        "Party": (8.2, 3.0, ["PartyID (PK)", "Name", "FoundingYear"]),
        "Membership": (4.8, 3.0, ["SpeakerID (PK, FK)", "FromDate (PK)", "ToDate", "PartyID (FK)"]),
        "Speech": (4.8, 0.5, ["SpeechID (PK)", "SpeakerID (FK)", "DebateID (FK)", "Time, Text, Length"]),
        "Debate": (8.2, 0.5, ["DebateID (PK)", "Title", "Date", "Topic"]),
    }
    H = {}
    for name, (x, y, attrs) in tables.items():
        h = 0.34 * (len(attrs) + 1)
        H[name] = (x, y, h)
        ax.add_patch(Rectangle((x - 1.2, y - h / 2), 2.4, h, fc="white", ec="#111", lw=1.1, zorder=2))
        ax.add_patch(Rectangle((x - 1.2, y + h / 2 - 0.34), 2.4, 0.34, fc=LIGHT, ec="#111", lw=1.1, zorder=3))
        ax.text(x, y + h / 2 - 0.17, name, ha="center", va="center", fontsize=10.5, fontweight="bold", zorder=4)
        for i, a in enumerate(attrs):
            ax.text(x - 1.1, y + h / 2 - 0.34 * (i + 1) - 0.17, a, ha="left", va="center", fontsize=9, zorder=4,
                    fontweight="bold" if "(PK" in a else "normal")

    def fk(src, dst, rad=0.0):
        (x1, y1, h1), (x2, y2, h2) = H[src], H[dst]
        dx = 1.2 if x2 > x1 else -1.2
        p = (x1 + dx, y1) if abs(y1 - y2) < 0.5 else (x1, y1 + (h1 / 2 if y2 > y1 else -h1 / 2))
        q = (x2 - dx, y2) if abs(y1 - y2) < 0.5 else (x2, y2 - (h2 / 2 if y2 > y1 else -h2 / 2))
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, color=BLUE, lw=1.4,
                                     connectionstyle=f"arc3,rad={rad}", zorder=1))
    fk("Membership", "Speaker"); fk("Membership", "Party"); fk("Speech", "Debate")
    # Speech -> Speaker: from left side of Speech up to bottom of Speaker
    ax.add_patch(FancyArrowPatch((3.6, 0.5), (1.4, 3.0 - H["Speaker"][2] / 2), arrowstyle="-|>", mutation_scale=14,
                                 color=BLUE, lw=1.4, connectionstyle="arc3,rad=0.0", zorder=1))
    ax.text(4.8, -0.85, "arrows: foreign key → the table whose primary key it references", ha="center", fontsize=9, color=GREY)
    clean(ax, (-0.1, 9.7), (-1.1, 4.1))
    save(fig, "sol-11-schema.svg")


# ================================================================ sheet 12
def fig_12_amdahl():
    import numpy as np
    N = np.arange(1, 65)
    P = 0.8
    S = 1 / ((1 - P) + P / N)
    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(N, S, color=BLUE, lw=2, label="P = 0.8")
    ax.axhline(5, color=RED, ls="--", lw=1.2); ax.text(2, 5.2, "ceiling 1/(1 − P) = 5", color=RED, fontsize=9)
    ax.axhline(10, color=GREY, ls=":", lw=1.2); ax.text(40, 10.15, "speedup 10: unreachable", color=GREY, fontsize=9)
    ax.plot([4], [2.5], "o", color=RED); ax.annotate("N = 4: S = 2.5", (4, 2.5), (10, 1.6), fontsize=9, arrowprops=dict(arrowstyle="->", color="#333"))
    ax.set_xlabel("processors N"); ax.set_ylabel("speedup S"); ax.set_ylim(0, 11); ax.grid(alpha=0.3); ax.legend(fontsize=9, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save(fig, "sol-12-amdahl.svg")


def fig_12_mapreduce():
    fig, ax = plt.subplots(figsize=(9, 3.0))
    for i in range(3):
        x = i * 2.6
        ax.add_patch(FancyBboxPatch((x, 1.6), 2.0, 0.7, boxstyle="round,pad=0.03", fc=LIGHT, ec="#111", lw=1.1, zorder=2))
        ax.text(x + 1.0, 2.05, f"machine {i + 1}: map()", ha="center", va="center", fontsize=10, fontweight="bold", zorder=3)
        ax.text(x + 1.0, 1.78, f"its m{['₁', '₂', '₃'][i]} pairs (x, y)", ha="center", va="center", fontsize=8.5, zorder=3)
        ax.add_patch(FancyArrowPatch((x + 1.0, 1.55), (3.9, 0.55), arrowstyle="-|>", mutation_scale=14, color="#111", lw=1.2, zorder=1))
        lx, ly, ha = [(0.2, 1.15, "left"), (3.9, 0.82, "center"), (7.6, 1.15, "right")][i]
        ax.text(lx, ly, "(m, Σx, Σy, Σx², Σy², Σxy)", ha=ha, va="center", fontsize=8, color=BLUE,
                bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"), zorder=4)
    ax.add_patch(FancyBboxPatch((1.6, -0.2), 4.6, 0.7, boxstyle="round,pad=0.03", fc="#ffe9a8", ec="#111", lw=1.1, zorder=2))
    ax.text(3.9, 0.25, "reduce(): add the six sums, apply the formula once", ha="center", va="center", fontsize=9.5, zorder=3)
    ax.text(3.9, -0.55, "ρ = (nΣxy − ΣxΣy) / √(nΣx² − (Σx)²) √(nΣy² − (Σy)²)   with n = m₁ + m₂ + m₃", ha="center", fontsize=9, color="#333")
    clean(ax, (-0.2, 7.9), (-0.8, 2.5))
    save(fig, "sol-12-mapreduce.svg")


# ================================================================ sheet 13
def schelling(n=30, empty=0.1, F=0.4, seed=1, max_iter=60):
    rnd = random.Random(seed)
    cells = [0] * int(n * n * empty) + [1] * ((n * n - int(n * n * empty)) // 2)
    cells += [2] * (n * n - len(cells))
    rnd.shuffle(cells)
    grid = [cells[i * n:(i + 1) * n] for i in range(n)]

    def frac(i, j, kind):
        sim = occ = 0
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == dj == 0: continue
                a, b = i + di, j + dj
                if 0 <= a < n and 0 <= b < n and grid[a][b]:
                    occ += 1; sim += grid[a][b] == kind
        return sim / occ if occ else 1.0

    def mean_similar():
        vals = [frac(i, j, grid[i][j]) for i in range(n) for j in range(n) if grid[i][j]]
        return sum(vals) / len(vals)
    history = [mean_similar()]
    start = [row[:] for row in grid]
    for _ in range(max_iter):
        moved = False
        agents = [(i, j) for i in range(n) for j in range(n) if grid[i][j]]
        rnd.shuffle(agents)
        for i, j in agents:
            k = grid[i][j]
            if frac(i, j, k) < F:
                empties = [(a, b) for a in range(n) for b in range(n) if grid[a][b] == 0]
                good = [(a, b) for a, b in empties if frac(a, b, k) >= F]
                if good:
                    a, b = min(good, key=lambda p: abs(p[0] - i) + abs(p[1] - j))
                    grid[a][b], grid[i][j] = k, 0; moved = True
        history.append(mean_similar())
        if not moved: break
    return start, grid, history


def fig_13_schelling():
    start, end, hist = schelling()
    import numpy as np
    cmap = matplotlib.colors.ListedColormap(["white", "#d62728", "#1f77b4"])
    fig, axes = plt.subplots(1, 4, figsize=(11.5, 3.0), gridspec_kw={"width_ratios": [0.8, 1, 1, 1.3]})
    # neighborhood of exercise 2b
    nb = [["R", "B", "B"], ["B", "R", "·"], ["R", "B", "B"]]
    a0 = axes[0]
    for i in range(3):
        for j in range(3):
            v = nb[i][j]
            fc = {"R": "#f7c6c6", "B": "#cfe0f5", "·": "white"}[v]
            a0.add_patch(Rectangle((j, 2 - i), 1, 1, fc=fc, ec="#111", lw=1.5 if (i, j) == (1, 1) else 0.8))
            a0.text(j + 0.5, 2.5 - i, v if v != "·" else "empty", ha="center", va="center", fontsize=10 if v != "·" else 7)
    a0.set_title("(b) f = 2/7 ≈ 0.29", fontsize=10); clean(a0, (-0.1, 3.1), (-0.1, 3.1))
    for ax, g, title in zip(axes[1:3], [start, end], ["(c) random start", f"after {len(hist) - 1} rounds, F = 0.4"]):
        ax.imshow(np.array(g), cmap=cmap, vmin=0, vmax=2, interpolation="nearest")
        ax.set_title(title, fontsize=10); ax.set_axis_off()
    a3 = axes[3]
    a3.plot(range(len(hist)), hist, "o-", color="#111", ms=3)
    a3.set_xlabel("round"); a3.set_ylabel("mean fraction of similar neighbors"); a3.set_ylim(0.4, 1.0)
    a3.axhline(0.4, color=GREY, ls="--", lw=1); a3.text(len(hist) * 0.5, 0.415, "F = 0.4", fontsize=8, color=GREY)
    a3.spines[["top", "right"]].set_visible(False); a3.grid(alpha=0.3)
    fig.tight_layout()
    save(fig, "sol-13-schelling.svg")
    return hist


if __name__ == "__main__":
    fig_02_dice(); fig_03_hash(); fig_03_binary_search(); fig_03_bst()
    fig_05_bfs(); fig_05_bellman_ford(); fig_06_heap_reduce(); fig_06_dfs(); fig_07_mergesort()
    fig_08_bigo(); fig_09_dfa_icss(); fig_09_pda_stack(); fig_10_metrics(); fig_10_elbow()
    fig_11_schema(); fig_12_amdahl(); fig_12_mapreduce()
    h = fig_13_schelling()
    print("schelling similar-neighbor fraction: start %.2f end %.2f rounds %d" % (h[0], h[-1], len(h) - 1))
    # the two graphs shared with the exam pool (GP-03 and GP-08) are copied next to the pool figures
    import shutil
    for name in ("sol-05-bfs.svg", "sol-05-bellman-ford.svg"):
        shutil.copy(os.path.join(OUT, name), os.path.join(ROOT, "Exams", "figures", name))
        print("   copied", name, "to Exams/figures")
