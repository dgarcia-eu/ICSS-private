#!/usr/bin/env python3
"""Measure which slides of a rendered deck do not fit.

    python3 tools/measuredeck.py Slides/04-Software/ICSS-2026-04-Software.qmd [--render]

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
    let maxB=0, minL=0, maxR=0, code=0, col=0, low='';
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
      maxR=Math.max(maxR, r.right-pr.left); minL=Math.min(minL, r.left-pr.left);
    });
    const h=sec.querySelector('h2,h1');
    out.push({i:idx, title:h?h.textContent.trim().slice(0,60):'', w:pr.width, b:maxB, l:minL, r:maxR, code:code, col:col, low:low});
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
    s = slides.setdefault(p["i"], dict(title=p["title"], pages=0, bottom=0, left=0, right=0, code=0, col=0, low=""))
    k = p["w"] / 1280.0
    s["pages"] += 1
    if p["b"] / k - 720 * 0.945 > s["bottom"]:
        s["bottom"], s["low"] = p["b"] / k - 720 * 0.945, p["low"]
    s["left"] = max(s["left"], -p["l"] / k)
    s["right"] = max(s["right"], p["r"] / k - 1280)
    s["code"] = max(s["code"], p["code"])
    s["col"] = max(s["col"], p["col"] / k)
bad = {i: s for i, s in slides.items() if s["pages"] > 1 or s["bottom"] > 0.5 or s["left"] > 0.5
       or s["right"] > 0.5 or s["code"] > 1 or s["col"] > 3}
print(f"{os.path.relpath(q)}  slides {len(slides)}  overflow {len(bad)}")
for i, s in sorted(bad.items()):
    print(f"  {i:3}  pages {s['pages']}  bottom {s['bottom']:+5.0f}  left {s['left']:3.0f}  right {s['right']:3.0f}"
          f"  code {s['code']:3.0f}  col {s['col']:3.0f}  {s['title']}  [{s['low'] if s['bottom'] > 0.5 else ''}]")
sys.exit(0)
