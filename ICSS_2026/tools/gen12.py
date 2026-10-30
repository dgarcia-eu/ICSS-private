#!/usr/bin/env python3
"""Diagrams of ICSS session 12 (Parallel Programming)."""
import os
OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/12-ParallelProgramming/figures"
FONT = 'font-family="Arial, Helvetica, sans-serif"'
DEFS = ('  <defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
        'markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
        'fill="#4a7fbf"/></marker></defs>\n')
def svg(w,h,b,defs=True):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" {FONT}>\n' + (DEFS if defs else "") + b + '</svg>\n')
def txt(x,y,t,fs=13,anchor="middle",fill="#111",weight="normal"):
    return (f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{fs}" fill="{fill}" '
            f'font-weight="{weight}">{t}</text>\n')
def write(n,c): open(os.path.join(OUT,n),"w").write(c); print("  ",n)

BLUE, YELLOW, PINK = "#cfe8f5", "#fbe3a6", "#f5d3d6"
def bar(x,y,w,h,fill,label,fs=14):
    return (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#7a7a7a" '
            f'stroke-width="1"/>\n' + txt(x+w/2, y+h/2+5, label, fs))
def rail(x1,x2,y):
    return f'  <line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#7a7a7a" stroke-width="1"/>\n'

# ---------------------------------------------------- single-thread vs parallel
b=""
b += txt(20, 22, "Single-thread", 17, anchor="start", weight="bold")
b += rail(70, 700, 56); b += txt(66, 61, "CPU 1", 14, anchor="end")
b += bar(80, 38, 190, 36, BLUE, "task 1")
b += bar(280, 38, 190, 36, YELLOW, "task 2")
b += bar(480, 38, 200, 36, PINK, "task 3")
b += txt(20, 118, "Parallel", 17, anchor="start", weight="bold")
for i,(c,l) in enumerate([(BLUE,"task 1"),(YELLOW,"task 2"),(PINK,"task 3")]):
    y = 134 + i*46
    b += rail(70, 700, y+18); b += txt(66, y+23, f"CPU {i+1}", 14, anchor="end")
    b += bar(80, y, 190, 36, c, l)
write("12-single-vs-parallel.svg", svg(710, 290, b, defs=False))

# --------------------------------------------------- concurrent vs parallel
b=""
b += txt(20, 22, "Concurrent", 17, anchor="start", weight="bold")
SLOTS = [[(80,90),(340,90),(600,90)], [(180,80),(300,80),(480,80)], [(240,90),(420,90),(540,80)]]
for i,(c,l) in enumerate([(BLUE,"task 1"),(YELLOW,"task 2"),(PINK,"task 3")]):
    y = 40 + i*42
    b += rail(70, 700, y+16); b += txt(66, y+21, l, 14, anchor="end")
    for (x,w) in SLOTS[i]:
        b += (f'  <rect x="{x}" y="{y}" width="{w}" height="32" fill="{c}" stroke="#7a7a7a" '
              f'stroke-width="1"/>\n')
b += txt(20, 204, "Parallel", 17, anchor="start", weight="bold")
for i,(c,l) in enumerate([(BLUE,"task 1"),(YELLOW,"task 2"),(PINK,"task 3")]):
    y = 220 + i*42
    b += rail(70, 700, y+16); b += txt(66, y+21, l, 14, anchor="end")
    b += (f'  <rect x="80" y="{y}" width="600" height="32" fill="{c}" stroke="#7a7a7a" '
          f'stroke-width="1"/>\n')
write("12-concurrent-vs-parallel.svg", svg(710, 352, b, defs=False))

# -------------------------------------------------- concurrency switching cost
b = rail(70, 700, 26) + txt(66, 31, "CPU 1", 14, anchor="end")
b += bar(80, 8, 190, 36, BLUE, "task 1")
b += bar(272, 8, 130, 36, YELLOW, "task 2")
b += bar(404, 8, 120, 36, BLUE, "task 1")
b += bar(526, 8, 174, 36, PINK, "task 3")
b += ('  <circle cx="272" cy="26" r="22" fill="none" stroke="#cc2222" stroke-width="3"/>\n')
write("12-concurrency-switch.svg", svg(710, 56, b, defs=False))

# ------------------------------------------------------------ pipeline stages
STAGES = [("IF",16),("ID",16),("EX",16),("MEM",11),("WB",16)]
SW, SH = 52, 30
def instr(x, y, hl=None, fill="#dbe8f7"):
    s = ""
    for k,(name,fs) in enumerate(STAGES):
        col = "#e9eef5" if (hl is not None and k == hl) else fill
        stroke = "#4caf50" if (hl is not None and k == hl) else "#7a9ec4"
        sw = "2.2" if (hl is not None and k == hl) else "1"
        s += (f'  <rect x="{x+k*SW}" y="{y}" width="{SW}" height="{SH}" fill="{col}" '
              f'stroke="{stroke}" stroke-width="{sw}"/>\n')
        s += txt(x+k*SW+SW/2, y+SH/2+5, name, fs, weight="bold")
    return s

write("12-pipeline-stages.svg", svg(5*SW+4, SH+4, instr(2, 2), defs=False))

# no parallelism: three instructions one after another, staggered down-right
b=""
for i in range(3):
    b += instr(30 + i*270, 10 + i*40)
b += (f'  <line x1="14" y1="14" x2="14" y2="86" stroke="#4a7fbf" stroke-width="3" '
      f'marker-end="url(#a)"/>\n') + txt(6, 52, "i", 15, anchor="end")
b += (f'  <line x1="120" y1="108" x2="220" y2="108" stroke="#4a7fbf" stroke-width="3" '
      f'marker-end="url(#a)"/>\n') + txt(168, 102, "time", 14)
write("12-pipeline-none.svg", svg(830, 124, b))

# pipelined: five instructions staggered by one stage
def pipelined(hl_col=None, n=5):
    b=""
    for i in range(n):
        hl = (hl_col - i) if hl_col is not None else None
        if hl is not None and not (0 <= hl < 5): hl = None
        b += instr(60 + i*SW, 10 + i*(SH+4), hl)
    b += (f'  <line x1="30" y1="16" x2="30" y2="{10+n*(SH+4)}" stroke="#4a7fbf" '
          f'stroke-width="3" marker-end="url(#a)"/>\n') + txt(20, 90, "i", 15, anchor="end")
    yy = 20 + n*(SH+4)
    b += (f'  <line x1="70" y1="{yy}" x2="180" y2="{yy}" stroke="#4a7fbf" stroke-width="3" '
          f'marker-end="url(#a)"/>\n') + txt(124, yy-8, "time", 14)
    return svg(60 + n*SW + 5*SW + 20, yy + 16, b)
write("12-pipeline-full.svg", pipelined(4))
write("12-pipeline-caveat.svg", pipelined(4))

# ------------------------------------------------------------- Flynn taxonomy
CELLS = [("SISD","Single Instruction stream","Single Data stream","#d6d9f5"),
         ("SIMD","Single Instruction stream","Multiple Data stream","#f5cdd4"),
         ("MISD","Multiple Instruction stream","Single Data stream","#cdefd6"),
         ("MIMD","Multiple Instruction stream","Multiple Data stream","#c3cdf0")]
CW2, CH2, X0, Y0 = 200, 130, 150, 20
b = f'  <rect x="{X0-6}" y="{Y0-6}" width="{2*CW2+12}" height="{2*CH2+12}" fill="#e0e0e0"/>\n'
for k,(name,l1,l2,col) in enumerate(CELLS):
    x = X0 + (k%2)*CW2; y = Y0 + (k//2)*CH2
    b += (f'  <rect x="{x}" y="{y}" width="{CW2}" height="{CH2}" fill="{col}" stroke="#111" '
          f'stroke-width="1.4"/>\n')
    b += txt(x+CW2/2, y+52, name, 30, fill="#1f3f9e", weight="bold")
    b += txt(x+CW2/2, y+82, l1, 10, weight="bold")
    b += txt(x+CW2/2, y+96, l2, 10, weight="bold")
def callout(x, y, w, h, lines, arrow_to):
    s = (f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#d8ecfa" stroke="#1f6fb2" '
         f'stroke-width="1.6"/>\n')
    for i,l in enumerate(lines):
        s += txt(x+w/2, y+20+i*16, l, 12, weight="bold")
    ax, ay = arrow_to
    sx = x+w if ax > x else x
    s += (f'  <line x1="{sx}" y1="{y+h/2}" x2="{ax}" y2="{ay}" stroke="#1f6fb2" '
          f'stroke-width="2" marker-end="url(#a)"/>\n')
    return s
b += callout(10, 52, 116, 34, ["One CPU"], (X0-8, 69))
b += callout(2, 176, 132, 62, ["Fault-tolerant","system","(e.g. airplane)"], (X0-8, 200))
b += callout(566, 52, 128, 46, ["Graphic","cards (GPU)"], (X0+2*CW2+8, 74))
b += callout(566, 176, 140, 62, ["Supercomputers,","Multiple CPUs","per chip"], (X0+2*CW2+8, 202))
write("12-flynn.svg", svg(720, 292, b))
print("deck 12 figures written")
