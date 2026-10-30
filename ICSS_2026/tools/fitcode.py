#!/usr/bin/env python3
"""Make the code on given slides as large as possible without scrolling.

    python3 tools/fitcode.py Slides/04-Software/ICSS-2026-04-Software.qmd 12 15 29

For each slide (title slide = 1), every `::: {style="font-size:Xem"}` wrapper on that
slide is scaled by one common factor, found by bisection with tools/measuredeck.py, so
that the slide has no scrolling code and no overflow. Blocks on one slide keep their
relative sizes.
"""
import re, subprocess, sys

q, idxs = sys.argv[1], [int(x) for x in sys.argv[2:]]
WRAP = re.compile(r'(::: \{style="font-size:)([0-9.]+)(em"\})')


def slide_span(text, i):
    heads = [m.start() for m in re.finditer(r"^## ", text, re.M)]
    a = heads[i - 2]
    b = heads[i - 1] if i - 1 < len(heads) else len(text)
    return a, b


def bad(i):
    out = subprocess.run(["python3", "tools/measuredeck.py", q, "--render"], capture_output=True, text=True).stdout
    return any(re.match(rf"\s+{i}\s+pages", l) for l in out.splitlines())


for i in idxs:
    text = open(q).read()
    a, b = slide_span(text, i)
    base = [float(m.group(2)) for m in WRAP.finditer(text[a:b])]
    if not base:
        print(f"slide {i}: no size wrappers"); continue

    def setf(f):
        t = open(q).read()
        a, b = slide_span(t, i)
        it = iter(base)
        seg = WRAP.sub(lambda m: f"{m.group(1)}{round(next(it) * f, 2)}{m.group(3)}", t[a:b])
        open(q, "w").write(t[:a] + seg + t[b:])

    lo, hi = 0.5, 1.6                      # factor bounds; lo assumed to fit
    for _ in range(7):
        mid = (lo + hi) / 2
        setf(mid)
        if bad(i): hi = mid
        else: lo = mid
    setf(lo * 0.99)
    print(f"slide {i}: factor {lo * 0.99:.2f}, sizes {[round(x * lo * 0.99, 2) for x in base]}")
