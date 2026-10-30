#!/bin/bash
# build.sh <qmd-basename> [expected-pages] — render, print to PDF, scan for overflow
D=/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/${1#ICSS-2026-}
S=/tmp/claude-1000/-home-dgarcia-Dropbox-Teaching-Konstanz/ae14631a-a710-45c4-83e5-f88e31d81a65/scratchpad
B=$1
OUT=$S/out/$B
mkdir -p $OUT
quarto render "$D/$B.qmd" --quiet 2>&1 | tail -5
google-chrome --headless=new --disable-gpu --no-sandbox --virtual-time-budget=40000 \
  --run-all-compositor-stages-before-draw --no-pdf-header-footer \
  --print-to-pdf=$OUT/deck.pdf "file://$D/$B.html?print-pdf" 2>/dev/null
echo -n "pages: "; pdfinfo $OUT/deck.pdf | awk '/^Pages/{print $2}'
rm -f $OUT/p-*.png
pdftoppm -png -r 72 $OUT/deck.pdf $OUT/p
python3 - "$OUT" <<'EOF'
import sys, glob
from PIL import Image
bad = []
for f in sorted(glob.glob(sys.argv[1] + '/p-*.png')):
    im = Image.open(f).convert('L'); w, h = im.size
    fy = int(h * 0.945)
    L = any(im.getpixel((1, y)) < 245 for y in range(60, fy))
    R = any(im.getpixel((w - 2, y)) < 245 for y in range(60, fy))
    B = any(im.getpixel((x, fy - 2)) < 245 for x in range(5, w - 5))
    if L or R or B:
        bad.append(f"{f.split('/')[-1]} {'L' if L else ''}{'R' if R else ''}{' BOTTOM' if B else ''}")
print("overflow:", "; ".join(bad) if bad else "none")
EOF
