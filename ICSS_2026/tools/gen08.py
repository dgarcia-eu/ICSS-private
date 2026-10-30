#!/usr/bin/env python3
"""Diagrams of ICSS session 8 (Time Complexity)."""
import os
OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/08-TimeComplexity/figures"
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


CW, CH = 48, 30


def insertion_fig(name, rows, keys):
    """rows: list of value lists; keys: index of the highlighted key per row (or None)."""
    w, h = 20 + 5 * CW + 20, 30 + len(rows) * (CH + 26)
    body = txt(20 + 1.5 * CW, 16, "key", 13, style="italic")
    for r, vals in enumerate(rows):
        y = 26 + r * (CH + 26)
        for i, v in enumerate(vals):
            x = 20 + i * CW
            sortedpart = i < r
            fill = "#cceef9" if sortedpart else "#eaf7fd"
            body += (f'  <rect x="{x}" y="{y}" width="{CW}" height="{CH}" fill="{fill}" '
                     f'stroke="#111" stroke-width="1"/>\n')
            bold = "bold" if keys[r] == i else "normal"
            body += txt(x + CW / 2, y + 21, str(v), 15, weight=bold)
            body += txt(x + CW / 2, y + CH + 13, str(i), 10, fill="#555")
        if r < len(rows) - 1 and keys[r] is not None:
            kx = 20 + keys[r] * CW + CW / 2
            body += (f'  <line x1="{kx}" y1="{y+CH+18}" x2="{kx-6}" y2="{y+CH+24}" '
                     f'stroke="#111" stroke-width="1.4" marker-end="url(#a)"/>\n')
    write(name, svg(w, h, body))


insertion_fig("08-insertion-sort.svg",
              [[96, 57, 6, 12, 44], [57, 96, 6, 12, 44], [6, 57, 96, 12, 44],
               [6, 12, 57, 96, 44], [6, 12, 44, 57, 96]],
              [1, 2, 3, 4, None])
insertion_fig("08-insertion-sort-best.svg",
              [[10, 20, 30, 40, 50]] * 5, [1, 2, 3, 4, None])

# asymptotic sketch
body = ('  <rect x="60" y="14" width="440" height="220" fill="none" stroke="#111" '
        'stroke-width="1.4"/>\n')
pts = []
for i in range(0, 101):
    x = 70 + i * 4.1
    t = i / 100
    y = 222 - 190 * (t ** 4)
    pts.append(f"{x:.1f},{y:.1f}")
body += ('  <polyline points="' + " ".join(pts) + '" fill="none" stroke="#111" '
         'stroke-width="5" marker-end="url(#a)"/>\n')
body += txt(462, 44, "?", 20)
body += (f'  <text x="42" y="130" text-anchor="middle" font-size="14" '
         f'transform="rotate(-90 42 130)">f(x)</text>\n')
body += txt(280, 256, "x", 15)
write("08-asymptotic.svg", svg(520, 268, body))
print("deck 8 figures written")
