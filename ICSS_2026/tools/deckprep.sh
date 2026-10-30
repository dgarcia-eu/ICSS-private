#!/bin/bash
# deckprep.sh <NN> — prepare working files for one ICSS deck
# Produces in $W/<NN>/ : text.txt, pages/*.png, media/, map.txt, montage.png
set -e
NN=$1
SL=/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/Slides
W=/tmp/claude-1000/-home-dgarcia-Dropbox-Teaching-Konstanz/ae14631a-a710-45c4-83e5-f88e31d81a65/scratchpad/decks
BASE=$(cd $SL && ls ICSS-2025-$NN-*.pdf | head -1 | sed 's/\.pdf$//')
OUT=$W/$NN
rm -rf $OUT; mkdir -p $OUT/pages $OUT/pptx
echo "deck: $BASE"

pdftotext -layout "$SL/$BASE.pdf" "$OUT/text.txt"
pdftoppm -png -r 72 "$SL/$BASE.pdf" "$OUT/pages/p"
unzip -o -q "$SL/$BASE.pptx" -d "$OUT/pptx"

python3 - "$OUT" <<'EOF'
import sys, os
from xml.etree import ElementTree as ET
out = sys.argv[1]
ns = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
RID = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
base = os.path.join(out, 'pptx', 'ppt')
pres = ET.parse(base + '/presentation.xml').getroot()
prels = {r.get('Id'): r.get('Target')
         for r in ET.parse(base + '/_rels/presentation.xml.rels').getroot()}
order = [prels[s.get(RID + 'id')] for s in pres.find('p:sldIdLst', ns)]
EMU = 914400
lines = []
for i, t in enumerate(order, 1):
    fn = base + '/' + t.replace('../', '')
    rf = os.path.join(os.path.dirname(fn), '_rels', os.path.basename(fn) + '.rels')
    rels = {r.get('Id'): r.get('Target') for r in ET.parse(rf).getroot()}
    root = ET.parse(fn).getroot()
    pics = []
    for pic in root.iter('{http://schemas.openxmlformats.org/presentationml/2006/main}pic'):
        blip = pic.find('.//a:blip', ns)
        if blip is None: continue
        rid = blip.get(RID + 'embed')
        if rid is None or rid not in rels: continue
        img = os.path.basename(rels[rid])
        x = y = cx = cy = 0
        xf = pic.find('.//a:xfrm', ns)
        if xf is not None:
            off, ext = xf.find('a:off', ns), xf.find('a:ext', ns)
            if off is not None: x, y = int(off.get('x'))/EMU, int(off.get('y'))/EMU
            if ext is not None: cx, cy = int(ext.get('cx'))/EMU, int(ext.get('cy'))/EMU
        pics.append(f"    {img:16s} @({x:5.2f},{y:5.2f})  {cx:5.2f} x {cy:5.2f} in")
    if pics:
        lines.append(f"--- page {i}")
        lines += pics
open(os.path.join(out, 'map.txt'), 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
EOF

M=$OUT/pptx/ppt/media
if [ -d "$M" ]; then
  ( cd "$M" && montage $(ls | sort -V) -label '%f' -tile 8x -geometry 120x120+4+4 \
      -background white -pointsize 10 "$OUT/montage.png" ) || true
fi
echo "pages: $(ls $OUT/pages | wc -l)   media: $(ls $M 2>/dev/null | wc -l)"
