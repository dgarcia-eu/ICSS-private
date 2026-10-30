#!/usr/bin/env python3
"""Size the figures of the example decks to the room their slides actually have.

    python3 tools/tuneexamples.py [ROUNDS] [--clear]

Each round regenerates the decks (tools/genexamples.py), renders them, measures every slide in
headless Chrome in print layout, and for every slide with a generated figure grows or shrinks the
figure so that the content ends just above the footer bar. The result is stored in
tools/examples_figsize.json (slide heading -> figure height in px), which genexamples.py reads.
--clear first removes all per-slide {.fitN} classes from the example decks, so text is at full size.
Needs quarto and google-chrome. Figures never grow beyond the width box set in genexamples.py, and
shrink at most to MIN_H px; a slide that still overflows then needs a fit class (measure, then fit).
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EX = os.path.join(ROOT, "Slides", "Examples")
SAFE = 674          # px of the 1280x720 slide: content must end above this (footer bar starts at 680)
MIN_H = 230         # never shrink a figure below this height
FIGSIZE = os.path.join(HERE, "examples_figsize.json")

JS = r"""<script>
function measure(){ try { measure2(); } catch(err) {
  const pre=document.createElement('pre'); pre.id='MEASURE'; pre.textContent=JSON.stringify({error:String(err)}); document.body.appendChild(pre); } }
function measure2(){
  const out=[]; let idx=0, last=null;
  document.querySelectorAll('.pdf-page').forEach(p=>{
    const sec=p.querySelector('section'); if(!sec) return;
    if(sec!==last){ idx++; last=sec; } else return;
    const pr=p.getBoundingClientRect(); const sc=pr.width/1280;
    let maxB=0;
    sec.querySelectorAll('*').forEach(e=>{
      if(e.closest('.footer')||e.closest('.slide-logo')||e.closest('aside.notes')) return;
      const st=getComputedStyle(e); if(st.display==='none'||st.visibility==='hidden') return;
      const r=e.getBoundingClientRect(); if(r.width===0&&r.height===0) return;
      maxB=Math.max(maxB,(r.bottom-pr.top)/sc);
    });
    const imgs=[...sec.querySelectorAll('img')].map(im=>{const r=im.getBoundingClientRect();
      const col=im.closest('.column'); let colB=0, ownB=0;
      if(col){ col.parentElement.querySelectorAll(':scope > .column').forEach(c=>{ c.querySelectorAll('*').forEach(e=>{
         const rr=e.getBoundingClientRect(); if(rr.width===0&&rr.height===0) return;
         const bb=(rr.bottom-pr.top)/sc;
         if(c.contains(im)) ownB=Math.max(ownB,bb); else colB=Math.max(colB,bb); }); }); }
      return {src:im.getAttribute('src'), w:r.width/sc, h:r.height/sc, top:(r.top-pr.top)/sc, incol:!!col, otherColB:colB, ownColB:ownB, cw:(col||im.closest('section')).getBoundingClientRect().width/sc};});
    out.push({i:idx, maxB, imgs});
  });
  const pre=document.createElement('pre'); pre.id='MEASURE'; pre.textContent=JSON.stringify(out); document.body.appendChild(pre);
}
Reveal.on('pdf-ready', ()=>setTimeout(measure,500));
</script></body>"""


def probe(qmd, tries=3):
    for k in range(tries):
        try:
            return _probe(qmd)
        except SystemExit as e:
            if k == tries - 1 or "no measurement" not in str(e):
                raise


def _probe(qmd):
    qmd = os.path.abspath(qmd)
    d, b = os.path.dirname(qmd), os.path.basename(qmd)[:-4]
    r = subprocess.run(["quarto", "render", qmd, "--quiet"], capture_output=True, text=True)
    if r.returncode:
        sys.exit("render failed: " + qmd + r.stderr[-300:])
    page = open(os.path.join(d, b + ".html")).read()
    tmp = os.path.join(d, "_tune_" + b + ".html")
    open(tmp, "w").write(page.replace("</body>", JS, 1))
    try:
        dom = subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
                              "--window-size=1280,720", "--virtual-time-budget=60000",
                              "--run-all-compositor-stages-before-draw", "--dump-dom",
                              "file://" + tmp + "?print-pdf"], capture_output=True, text=True, timeout=180).stdout
    finally:
        os.remove(tmp)
    import html
    m = re.search(r'<pre id="MEASURE">(.*?)</pre>', dom, re.S)
    if not m:
        sys.exit("no measurement for " + qmd)
    data = json.loads(html.unescape(m.group(1)))
    if isinstance(data, dict):
        sys.exit("measurement error in " + qmd + ": " + data["error"])
    return data


def headings(qmd):
    return [re.sub(r"\s*\{[^}]*\}\s*$", "", l[3:]).strip() for l in open(qmd).read().split("\n") if l.startswith("## ")]


def main():
    rounds = int(next((a for a in sys.argv[1:] if a.isdigit()), "3"))
    decks = sorted(os.path.join(EX, d, f"ICSS-2026-{d[:2]}-Examples.qmd") for d in os.listdir(EX) if d.endswith("-Examples"))
    if "--clear" in sys.argv:
        for q in decks:
            t = open(q).read(); open(q, "w").write(re.sub(r"(?m)^(## .*?) \{\.fit\d\}$", r"\1", t))
    sizes = json.load(open(FIGSIZE)) if os.path.exists(FIGSIZE) else {}
    for rnd in range(rounds):
        subprocess.run([sys.executable, os.path.join(HERE, "genexamples.py")], check=True, capture_output=True)
        slides = json.load(open(os.path.join(HERE, "examples_figslides.json")))
        moved = 0
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(6) as pool:
            measured = dict(zip(decks, pool.map(probe, decks)))
        for q in decks:
            heads = headings(q)
            for s in measured[q]:
                if s["i"] < 2: continue
                head = heads[s["i"] - 2]
                if head not in slides: continue
                name = os.path.basename(slides[head]["img"])
                im = next((x for x in s["imgs"] if x["src"].endswith(name)), None)
                if not im or im["h"] < 1: continue
                slack = SAFE - s["maxB"]
                # widest allowed: the generator's box (pages are scaled by 1/1.06 in print) or the container
                wmax = min(slides[head]["maxw"] / 1.06, im["cw"])
                hmax_w = wmax * im["h"] / im["w"]
                if im["incol"]:
                    # only the figure's own column moves: fill that column down to the safe line
                    # (an overflowing text column next to it needs a fit class, not a smaller figure)
                    target = im["h"] + (SAFE - 10 - im["ownColB"])     # the column box adds paragraph margins
                else:
                    target = im["h"] + slack
                target = int(max(MIN_H, min(target - 2, hmax_w)) * 1.06)   # back to requested px
                old = sizes.get(head)
                if old is None or abs(old - target) > 3:
                    if "-v" in sys.argv:
                        print(f"   {head[:60]:60} {old} -> {target}  (img h {im['h']:.0f}, slack {slack:.0f}, col {im['incol']})")
                    sizes[head] = target; moved += 1
        json.dump(sizes, open(FIGSIZE, "w"), indent=1, ensure_ascii=False, sort_keys=True)
        print(f"round {rnd + 1}: {moved} figures resized")
        if moved == 0:
            break
    subprocess.run([sys.executable, os.path.join(HERE, "genexamples.py")], check=True, capture_output=True)


if __name__ == "__main__":
    main()
