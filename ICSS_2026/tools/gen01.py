#!/usr/bin/env python3
"""Figures of ICSS session 1 (Introduction), written into Slides/01-Introduction/figures/."""
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Slides", "01-Introduction", "figures")
FONT = 'font-family="Arial, Helvetica, sans-serif"'
SEEBLAU, SEEBLAU1, SEEBLAU2, KARPFEN = "#00a9e0", "#cceef9", "#a6e1f4", "#3e5496"


def txt(x, y, t, fs=17, fill="#111", weight="normal", style="normal", anchor="start"):
    return (f'  <text x="{x}" y="{y}" font-size="{fs}" fill="{fill}" font-weight="{weight}" '
            f'font-style="{style}" text-anchor="{anchor}">{t}</text>\n')


# ------------------------------------------------- solving a problem computationally
STEPS = [
    ("Problem", "Who holds a research field together?"),
    ("Representation", "authors as nodes, papers as edges"),
    ("Algorithm", "breadth-first search from everyone"),
    ("Program", "Python code for 2 million authors"),
    ("Solution", "authors ranked by closeness"),
]
W, BOX_H, GAP, X0, BW = 470, 80, 24, 6, 404
H = 12 + len(STEPS) * BOX_H + (len(STEPS) - 1) * GAP + 6
body = ['  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{KARPFEN}"/></marker></defs>\n']
for i, (name, example) in enumerate(STEPS):
    y = 6 + i * (BOX_H + GAP)
    first, last = i == 0, i == len(STEPS) - 1
    fill = SEEBLAU2 if first or last else SEEBLAU1
    body.append(f'  <rect x="{X0}" y="{y}" width="{BW}" height="{BOX_H}" rx="10" fill="{fill}" '
                f'stroke="{SEEBLAU}" stroke-width="2"/>\n')
    body.append(txt(X0 + 14, y + 32, name, 26, weight="bold"))
    body.append(txt(X0 + 14, y + 64, example, 21, fill=KARPFEN, style="italic"))
    if not last:
        cx = X0 + BW / 2
        body.append(f'  <line x1="{cx}" y1="{y + BOX_H + 2}" x2="{cx}" y2="{y + BOX_H + GAP - 3}" '
                    f'stroke="{KARPFEN}" stroke-width="3" marker-end="url(#a)"/>\n')
# feedback loop: from the solution back to the problem
ytop, ybot = 6 + BOX_H / 2, 6 + (len(STEPS) - 1) * (BOX_H + GAP) + BOX_H / 2
xr = X0 + BW + 26
body.append(f'  <path d="M {X0 + BW + 2} {ybot} H {xr} V {ytop} H {X0 + BW + 6}" fill="none" '
            f'stroke="{KARPFEN}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#a)"/>\n')
body.append(f'  <text x="{xr + 20}" y="{(ytop + ybot) / 2}" font-size="20" fill="{KARPFEN}" text-anchor="middle" '
            f'transform="rotate(90 {xr + 20} {(ytop + ybot) / 2})">check and refine</text>\n')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>\n'
       + "".join(body) + "</svg>\n")
open(os.path.join(OUT, "01-solving-computationally.svg"), "w").write(svg)
print("01-solving-computationally.svg", W, H)
