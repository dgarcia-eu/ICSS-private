#!/usr/bin/env python3
"""Generate the diagrams of ICSS session 7 (Sorting Algorithms) as SVG."""
import os

OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/07-SortingAlgorithms/figures"
FONT = 'font-family="Arial, Helvetica, sans-serif"'
DEFS = '''  <defs>
    <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
            orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#111"/></marker>
  </defs>
'''
SORTED, TOSORT, MARK = "#cceef9", "#ffffff", "#ffd75e"


def svg(w, h, body, defs=True):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" {FONT}>\n' + (DEFS if defs else "") + body + '</svg>\n')


def txt(x, y, t, fs=13, anchor="middle", fill="#111", weight="normal", style="normal"):
    return (f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{fill}" '
            f'font-weight="{weight}" font-style="{style}">{t}</text>\n')


def write(name, content):
    open(os.path.join(OUT, name), "w").write(content)
    print("  ", name)


# ======================================================= row-based sort traces
CW, CH, X0 = 54, 30, 10


def rows_fig(name, rows, legend=True):
    """rows: list of (values, n_sorted, smallest_index or None)"""
    n = len(rows[0][0])
    w = X0 + n * CW + (150 if legend else 20)
    h = 14 + len(rows) * (CH + 22)
    body = ""
    for r, (vals, nsorted, sm) in enumerate(rows):
        y = 10 + r * (CH + 22)
        for i, v in enumerate(vals):
            x = X0 + i * CW
            fill = SORTED if i < nsorted else TOSORT
            body += (f'  <rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{fill}" '
                     f'stroke="#111" stroke-width="1"/>\n')
            body += txt(x + CW / 2, y + 21, str(v), 15)
            if sm is not None and i == sm:
                body += txt(x + CW / 2, y + CH + 15, "smallest", 10, fill="#444")
    if legend:
        lx = X0 + n * CW + 22
        body += (f'  <rect x="{lx}" y="10" width="20" height="16" fill="{SORTED}" stroke="#111" '
                 f'stroke-width="1"/>\n')
        body += txt(lx + 26, 23, "L: sorted", 12, anchor="start")
        body += (f'  <rect x="{lx}" y="36" width="20" height="16" fill="{TOSORT}" stroke="#111" '
                 f'stroke-width="1"/>\n')
        body += txt(lx + 26, 49, "R: to sort", 12, anchor="start")
    write(name, svg(w, h, body, defs=False))


# repeated minimum search (insert in front)
rows_fig("07-repeated-minimum.svg", [
    ([3, 6, 8, 4, 1, 2, 7], 0, 4),
    ([1, 3, 6, 8, 4, 2, 7], 1, 5),
    ([1, 2, 3, 6, 8, 4, 7], 2, 2),
    ([1, 2, 3, 6, 8, 4, 7], 3, 5),
    ([1, 2, 3, 4, 6, 8, 7], 4, 4),
    ([1, 2, 3, 4, 6, 8, 7], 5, 6),
    ([1, 2, 3, 4, 6, 7, 8], 7, None),
])

# selection sort (swap)
rows_fig("07-selection-sort.svg", [
    ([3, 6, 8, 4, 1, 2, 7], 0, 4),
    ([1, 6, 8, 4, 3, 2, 7], 1, 5),
    ([1, 2, 8, 4, 3, 6, 7], 2, 4),
    ([1, 2, 3, 4, 8, 6, 7], 3, 3),
    ([1, 2, 3, 4, 8, 6, 7], 4, 5),
    ([1, 2, 3, 4, 6, 8, 7], 5, 6),
    ([1, 2, 3, 4, 6, 7, 8], 7, None),
])


# ============================================================== MERGE example
def merge_fig(name, steps, B, C, bi, ci):
    n = max(len(s) for s in steps)
    w = X0 + 9 * CW + 40
    h = 96 + len(steps) * (CH + 8)
    body = ""
    # source arrays
    body += txt(X0 - 2, 30, "B", 15, anchor="start", weight="bold")
    for i, v in enumerate(B):
        x = X0 + 24 + i * CW
        body += (f'  <rect x="{x}" y="12" width="{CW}" height="{CH}" fill="{TOSORT}" stroke="#111" '
                 f'stroke-width="1"/>\n') + txt(x + CW / 2, 33, str(v), 15)
        if i == bi:
            body += txt(x + CW / 2, 58, "i", 13, style="italic")
    off = X0 + 24 + 4 * CW + 46
    body += txt(off - 22, 30, "C", 15, anchor="start", weight="bold")
    for i, v in enumerate(C):
        x = off + i * CW
        body += (f'  <rect x="{x}" y="12" width="{CW}" height="{CH}" fill="{TOSORT}" stroke="#111" '
                 f'stroke-width="1"/>\n') + txt(x + CW / 2, 33, str(v), 15)
        if i == ci:
            body += txt(x + CW / 2, 58, "j", 13, style="italic")
    for r, vals in enumerate(steps):
        y = 72 + r * (CH + 8)
        for i, v in enumerate(vals):
            x = X0 + 24 + i * CW
            body += (f'  <rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{SORTED}" '
                     f'stroke="#111" stroke-width="1"/>\n') + txt(x + CW / 2, y + 21, str(v), 15)
    write(name, svg(w, h, body, defs=False))


merge_fig("07-merge-1.svg", [[1], [1, 2], [1, 2, 3], [1, 2, 3, 4]],
          [2, 3, 4, 6], [1, 5, 7, 8], 0, 0)
merge_fig("07-merge-2.svg",
          [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8]],
          [2, 3, 4, 6], [1, 5, 7, 8], 3, 1)


# =============================================================== mergesort rows
def mergesort_fig(name, rows, splits, nrows=4):
    """rows: list of lists; splits: list of group sizes per row for the boxes.
    The canvas always has room for nrows rows, so the split figure and the three
    merge steps have the same size and the rows stay in place from slide to slide."""
    n = len(rows[0])
    w = X0 + n * CW + 20
    h = 12 + max(nrows, len(rows)) * (CH + 16)
    body = ""
    for r, vals in enumerate(rows):
        y = 10 + r * (CH + 16)
        g = splits[r]
        for i, v in enumerate(vals):
            x = X0 + i * CW
            body += (f'  <rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{SORTED}" '
                     f'stroke="#9a9a9a" stroke-width="0.8"/>\n') + txt(x + CW / 2, y + 21, str(v), 15)
        for k in range(0, n, g):
            body += (f'  <rect x="{X0 + k*CW}" y="{y}" width="{g*CW}" height="{CH}" fill="none" '
                     f'stroke="#111" stroke-width="1.6"/>\n')
    write(name, svg(w, h, body, defs=False))


SPLIT = [[4, 2, 3, 6, 8, 5, 1, 7]] * 4
mergesort_fig("07-mergesort-split.svg", SPLIT, [8, 4, 2, 1])
mergesort_fig("07-mergesort-merge-1.svg",
              [[4, 2, 3, 6, 8, 5, 1, 7], [2, 4, 3, 6, 5, 8, 1, 7]], [1, 2])
mergesort_fig("07-mergesort-merge-2.svg",
              [[4, 2, 3, 6, 8, 5, 1, 7], [2, 4, 3, 6, 5, 8, 1, 7],
               [2, 3, 4, 6, 1, 5, 7, 8]], [1, 2, 4])
mergesort_fig("07-mergesort-merge-3.svg",
              [[4, 2, 3, 6, 8, 5, 1, 7], [2, 4, 3, 6, 5, 8, 1, 7],
               [2, 3, 4, 6, 1, 5, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8]], [1, 2, 4, 8])

# ======================================================== divide and conquer
body = ""
BW, BH = 150, 40


def dbox(cx, cy, label):
    return (f'  <rect x="{cx-BW/2}" y="{cy-BH/2}" width="{BW}" height="{BH}" fill="#fff" '
            f'stroke="#111" stroke-width="1.2"/>\n' + txt(cx, cy + 5, label, 14))


body += dbox(280, 24, "problem")
body += dbox(110, 108, "sub-problem")
body += dbox(450, 108, "sub-problem")
body += dbox(110, 196, "solution to sub-problem")
body += dbox(450, 196, "solution to sub-problem")
body += dbox(280, 278, "solution to problem")
for x1, y1, x2, y2 in [(250, 44, 140, 88), (310, 44, 420, 88),
                       (110, 128, 110, 176), (450, 128, 450, 176),
                       (140, 216, 250, 258), (420, 216, 310, 258)]:
    body += (f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="1.6" '
             f'marker-end="url(#a)"/>\n')
body += txt(300, 66, "Divide", 14, anchor="start", weight="bold")
body += txt(30, 152, "Conquer", 14, anchor="start", weight="bold")
body += txt(280, 240, "Combine", 14, weight="bold")
write("07-divide-and-conquer.svg", svg(560, 306, body))


# ==================================================================== heaps
NR = 17


def heap_tree(arr, w=520, h=250, x0=None, dy=54, top=26, marks=None, gap=None):
    """Draw a binary heap stored in `arr` (1-based conceptually) as a tree."""
    n = len(arr)
    if n == 0:
        return ""
    import math
    levels = int(math.floor(math.log2(n))) + 1
    body = ""
    pos = {}
    for i in range(n):
        lvl = int(math.floor(math.log2(i + 1)))
        first = 2 ** lvl - 1
        cnt = 2 ** lvl
        idx = i - first
        span = w / (cnt + 1)
        pos[i] = (span * (idx + 1), top + lvl * dy)
    for i in range(1, n):
        p = (i - 1) // 2
        (x1, y1), (x2, y2) = pos[p], pos[i]
        body += (f'  <line x1="{x1:.1f}" y1="{y1+NR}" x2="{x2:.1f}" y2="{y2-NR}" stroke="#111" '
                 f'stroke-width="1.1"/>\n')
    for i, v in enumerate(arr):
        x, y = pos[i]
        fill = (marks or {}).get(i, "#fff")
        body += (f'  <circle cx="{x:.1f}" cy="{y}" r="{NR}" fill="{fill}" stroke="#111" '
                 f'stroke-width="1.2"/>\n') + txt(x, y + 5, str(v), 14)
    return body


def out_array(vals, y, w, cw=34, ch=24):
    if not vals:
        return ""
    x0 = (w - len(vals) * cw) / 2
    s = ""
    for i, v in enumerate(vals):
        x = x0 + i * cw
        s += (f'  <rect x="{x:.1f}" y="{y}" width="{cw}" height="{ch}" fill="{SORTED}" '
              f'stroke="#111" stroke-width="1"/>\n') + txt(x + cw / 2, y + 17, str(v), 13)
    return s


# heap property examples (max-heap)
write("07-heap-example.svg",
      svg(520, 210, heap_tree([7, 4, 5, 8, 3, 2, 6, 1], 520, 210), defs=False))
write("07-heap-fix-1.svg",
      svg(400, 210, heap_tree([7, 4, 5, 8, 3, 2, 6, 1], 400, 210), defs=False))
write("07-heap-fix-2.svg",
      svg(400, 210, heap_tree([7, 4, 6, 8, 3, 2, 5, 1], 400, 210), defs=False))
write("07-heap-fix-3.svg",
      svg(400, 210, heap_tree([7, 8, 5, 4, 3, 2, 6, 1], 400, 210), defs=False))

MINHEAP = [2, 4, 14, 10, 8, 15, 18, 17, 11, 16]
write("07-min-heap.svg", svg(560, 220, heap_tree(MINHEAP, 560, 220), defs=False))

# min-heap with indices and the array representation
body = heap_tree(MINHEAP, 560, 220)
import math
for i in range(len(MINHEAP)):
    lvl = int(math.floor(math.log2(i + 1)))
    first = 2 ** lvl - 1
    cnt = 2 ** lvl
    span = 560 / (cnt + 1)
    x = span * (i - first + 1)
    y = 26 + lvl * 54
    body += txt(x, y + 30, str(i + 1), 11, fill="#1f6fb2")
body += txt(148, 254, "Min-heap as an array:", 13, anchor="end")
cw = 34
x0 = 158
for i, v in enumerate(MINHEAP):
    x = x0 + i * cw
    body += (f'  <rect x="{x}" y="240" width="{cw}" height="24" fill="#fff" stroke="#111" '
             f'stroke-width="1"/>\n') + txt(x + cw / 2, 257, str(v), 13)
    body += txt(x + cw / 2, 278, str(i + 1), 11, fill="#1f6fb2")
write("07-min-heap-array.svg", svg(560, 290, body, defs=False))


# ============================================================ heapsort trace
def sift_down(a, i):
    """One step of sift-down; returns the new index or None when settled."""
    n = len(a)
    l, r = 2 * i + 1, 2 * i + 2
    m = i
    if l < n and a[l] < a[m]:
        m = l
    if r < n and a[r] < a[m]:
        m = r
    if m == i:
        return None
    a[i], a[m] = a[m], a[i]
    return m


heap = list(MINHEAP)
out = []
states = []          # (heap, out, caption)
first = True
while heap:
    states.append((list(heap), list(out),
                   "Extract top (minimum) and place it first" if first else "Extract min"))
    first = False
    out.append(heap[0])
    if len(heap) == 1:
        heap = []
        break
    heap[0] = heap[-1]
    heap.pop()
    states.append((list(heap), list(out), "Move last to top"))
    i = 0
    while True:
        j = sift_down(heap, i)
        if j is None:
            break
        states.append((list(heap), list(out), "Recover min-heap property"))
        i = j

for k, (h, o, cap) in enumerate(states):
    W, H = 560, 300
    body = heap_tree(h, W, 232) if h else ""
    body += out_array(o, 246, W)
    write(f"07-heapsort-{k:02d}.svg", svg(W, H, body, defs=False))
print("heapsort states:", len(states))
print("deck 7 figures written")
