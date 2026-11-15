#!/usr/bin/env python3
"""Print a rendered deck to PDF and write contact sheets of its slides as PNG.

    python3 tools/contactsheet.py Slides/05-Algorithms/ICSS-2026-05-Algorithms.qmd OUTDIR [FIRST LAST]

Six slides per sheet (2 x 3), each 640 px wide, so the text stays readable.
The sheets are OUTDIR/sheet-01.png, sheet-02.png, ... and each slide carries its number.
Use it to look at the slides the way the audience sees them on a 16:9 screen.
"""
import os, subprocess, sys, glob
q = os.path.abspath(sys.argv[1]); out = os.path.abspath(sys.argv[2])
first = int(sys.argv[3]) if len(sys.argv) > 3 else 1
last = int(sys.argv[4]) if len(sys.argv) > 4 else 9999
d, b = os.path.dirname(q), os.path.basename(q)[:-4]
os.makedirs(out, exist_ok=True)
pdf = os.path.join(d, b + ".pdf")
subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--run-all-compositor-stages-before-draw",
                "--virtual-time-budget=60000", "--no-pdf-header-footer", "--print-to-pdf=" + pdf,
                "file://" + os.path.join(d, b + ".html") + "?print-pdf"], capture_output=True, timeout=300)
for f in glob.glob(os.path.join(out, "p-*.png")) + glob.glob(os.path.join(out, "sheet-*.png")): os.remove(f)
subprocess.run(["pdftoppm", "-f", str(first), "-l", str(last), "-r", "48", "-png", pdf, os.path.join(out, "p")], check=True)
pages = sorted(glob.glob(os.path.join(out, "p-*.png")))
for k in range(0, len(pages), 6):
    sheet = os.path.join(out, f"sheet-{k // 6 + 1:02d}.png")
    subprocess.run(["montage"] + pages[k:k + 6] + ["-tile", "2x3", "-geometry", "640x360+6+6", "-background", "#888888", sheet], check=True)
    print(sheet, "slides", first + k, "to", first + min(k + 5, len(pages) - 1))
for f in pages: os.remove(f)
