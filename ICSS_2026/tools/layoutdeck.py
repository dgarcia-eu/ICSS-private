#!/usr/bin/env python3
"""Report unused space and small text on the slides of a rendered deck (16:9, 1280 x 720).

    python3 tools/layoutdeck.py Slides/04-Software/ICSS-2026-04-Software.qmd [--render] [--all]

For every slide: free = empty height in px between the lowest content and the footer line
(the usable height is about 600 px), text = smallest font size in px of body text,
code = smallest font size of code or pseudocode. Listed are slides with free > 170 px
(more than a quarter of the slide empty), text < 20 px, code < 15 px, or body text larger
than the slide title (TEXT>TITLE; MathJax glyphs may exceed the title by up to 2 px). Divider slides
(an outline list only) and the title slide are skipped. --all lists every slide.
The measurements below are those of measuredeck.py, taken the same way.

Opens the deck in headless Chrome in print mode, waits for MathJax, and reports
every slide (title slide = 1) whose content
  - reaches below the footer line (bottom),
  - goes past the left or right page edge,
  - is wider than its column (col), or
  - sits in a code block that needs scrolling, sideways or down (code),
and every slide that the printer splits over more than one page.
"""
import html as H
import json
import os
import re
import subprocess
import sys

q = os.path.abspath(sys.argv[1])
d, b = os.path.dirname(q), os.path.basename(q)[:-4]
if "--render" in sys.argv:
    r = subprocess.run(["quarto", "render", q, "--quiet"], capture_output=True, text=True)
    if r.returncode:
        print("RENDER FAILED", b, r.stderr[-600:])
        sys.exit(1)

JS = r"""<script>
function measure(){
  const out=[]; let idx=0, last=null;
  document.querySelectorAll('.pdf-page').forEach(p=>{
    const sec=p.querySelector('section'); if(!sec) return;
    if(sec!==last){ idx++; last=sec; }
    const pr=p.getBoundingClientRect();
    let maxB=0, minL=0, maxR=0, code=0, col=0, low='', minT=999, minC=999, small='', nimg=0, words=0, maxT=0, big='', hT=0;
    sec.querySelectorAll('pre, pre code, div.sourceCode').forEach(e=>{ code=Math.max(code, e.scrollWidth-e.clientWidth, e.scrollHeight-e.clientHeight); });
    sec.querySelectorAll('.column').forEach(c=>{ const cr=c.getBoundingClientRect();
      c.querySelectorAll('*').forEach(e=>{ if(e.parentElement && e.parentElement.closest('pre')) return;
        const st=getComputedStyle(e); if(st.display==='none'||st.visibility==='hidden') return;
        const r=e.getBoundingClientRect(); if(r.width===0) return;
        col=Math.max(col, r.right-cr.right, cr.left-r.left); }); });
    sec.querySelectorAll('*').forEach(e=>{
      if(e.closest('.footer')||e.closest('.slide-logo')||e.closest('aside.notes')) return;
      if(e.parentElement && e.parentElement.closest('pre')) return;
      const st=getComputedStyle(e); if(st.display==='none'||st.visibility==='hidden') return;
      const r=e.getBoundingClientRect(); if(r.width===0&&r.height===0) return;
      if(r.bottom-pr.top>maxB){ maxB=r.bottom-pr.top; low=e.tagName+'.'+e.className; }
      if(e.tagName==='IMG'||e.tagName==='svg') nimg++;
      maxR=Math.max(maxR, r.right-pr.left); minL=Math.min(minL, r.left-pr.left);
    });
    const tw=document.createTreeWalker(sec, NodeFilter.SHOW_TEXT);
    while(tw.nextNode()){ const n=tw.currentNode; const t=n.textContent.trim(); if(!t) continue;
      const e=n.parentElement; if(!e||e.closest('.footer')||e.closest('.slide-logo')||e.closest('aside.notes')||e.closest('.source')||e.closest('.slide-number')||e.closest('h2')||e.closest('h1')) continue;
      const st=getComputedStyle(e); if(st.display==='none'||st.visibility==='hidden') continue;
      const r=e.getBoundingClientRect(); if(r.width===0&&r.height===0) continue;
      const fs=parseFloat(st.fontSize)*(pr.width?1:1);
      if(e.closest('pre')||e.closest('code')){ if(fs<minC) minC=fs; }
      else { words+=t.split(/\s+/).length; if(fs<minT){ minT=fs; small=t.slice(0,40); } if(fs>maxT){ maxT=fs; big=t.slice(0,40)+' <'+e.className+'>'; } } }
    const hh=sec.querySelector('h2,h1'); if(hh) hT=parseFloat(getComputedStyle(hh).fontSize);
    const h=sec.querySelector('h2,h1');
    out.push({i:idx, title:h?h.textContent.trim().slice(0,60):'', w:pr.width, b:maxB, l:minL, r:maxR, code:code, col:col, low:low, minT:minT, minC:minC, small:small, maxT:maxT, big:big, hT:hT, nimg:nimg, words:words, outline:!!sec.querySelector('.outline'), cls:sec.className});
  });
  const pre=document.createElement('pre'); pre.id='MEASURE'; pre.textContent=JSON.stringify(out); document.body.appendChild(pre);
}
function whenMath(f){
  if(window.MathJax && MathJax.Hub && MathJax.Hub.Queue){ MathJax.Hub.Queue(()=>setTimeout(f,800)); }
  else { setTimeout(f,2500); }
}
Reveal.on('pdf-ready', ()=>whenMath(measure));
</script></body>"""

tmp = os.path.join(d, "_measure_" + b + ".html")
open(tmp, "w").write(open(os.path.join(d, b + ".html")).read().replace("</body>", JS, 1))
try:
    dom = subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--window-size=1280,720",
                          "--virtual-time-budget=60000", "--run-all-compositor-stages-before-draw", "--dump-dom",
                          "file://" + tmp + "?print-pdf"], capture_output=True, text=True, timeout=240).stdout
finally:
    os.remove(tmp)
m = re.search(r'<pre id="MEASURE">(.*?)</pre>', dom, re.S)
if not m:
    print("NO MEASURE", b)
    sys.exit(1)
slides = {}
for p in json.loads(H.unescape(m.group(1))):
    k = p["w"] / 1280.0
    s = slides.setdefault(p["i"], dict(title=p["title"], bottom=0, minT=999, minC=999, small="", nimg=0, words=0, outline=p["outline"], cls=p["cls"], maxT=0, big="", hT=0))
    if p["maxT"] / k > s["maxT"]: s["maxT"], s["big"] = p["maxT"] / k, p["big"]
    s["hT"] = max(s["hT"], p["hT"] / k)
    s["bottom"] = max(s["bottom"], p["b"] / k)
    if p["minT"] / k < s["minT"]: s["minT"], s["small"] = p["minT"] / k, p["small"]
    s["minC"] = min(s["minC"], p["minC"] / k); s["nimg"] += p["nimg"]; s["words"] += p["words"]
show_all = "--all" in sys.argv
rows = []
for i, s in sorted(slides.items()):
    free = 720 * 0.945 - s["bottom"]
    skip = i == 1 or s["outline"] or "title-slide" in s["cls"] or (s["words"] == 0 and s["nimg"] == 0)
    flags = []
    if free > 170 and not skip: flags.append("EMPTY")
    if s["minT"] < 20: flags.append("SMALL-TEXT")
    if s["minC"] < 15: flags.append("SMALL-CODE")
    if s["hT"] and s["maxT"] > s["hT"] + 2 and not skip: flags.append("TEXT>TITLE")
    if flags or show_all:
        rows.append(f"  {i:3}  free {free:4.0f}  text {s['minT'] if s['minT'] < 900 else 0:4.0f}  code {s['minC'] if s['minC'] < 900 else 0:4.0f}"
                    f"  img {s['nimg']:2}  words {s['words']:3}  {' '.join(flags):22}  {s['title']}" + (f"  [{s['small']}]" if "SMALL-TEXT" in flags else "") + (f"  [max {s['maxT']:.0f}px > title {s['hT']:.0f}px: {s['big']}]" if "TEXT>TITLE" in flags else ""))
print(f"{os.path.relpath(q)}  slides {len(slides)}  flagged {sum(1 for r in rows if 'EMPTY' in r or 'SMALL' in r)}")
print("\n".join(rows))
sys.exit(0)
