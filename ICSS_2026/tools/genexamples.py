#!/usr/bin/env python3
"""Emit the question/answer example decks: Slides/Examples/NN-Examples/ICSS-2026-NN-Examples.qmd

One deck per session 2-13, three examples per deck.  Each example is four
slides: the opening question, the closing answer (with "what we used"), and a
notes slide for the lecturer.  Some examples carry a fourth, supplementary
slide (extra figures) -- see EXTRA.

    python3 tools/genexamples.py          # write the 12 decks + README
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from examples_data_a import X as XA  # noqa: E402
from examples_data_b import X as XB  # noqa: E402

X = {**XA, **XB}
# Titles and hooks: keep digit groups together ("100 000" must not break across lines on a slide)
for _x in X.values():
    for _k in ("title", "tagline"):
        if _x.get(_k):
            _x[_k] = re.sub(r"(?<=\d) (?=\d{3}\b)", "\u00a0", _x[_k])
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "Slides", "Examples")
os.makedirs(OUT, exist_ok=True)

SESSIONS = {
    "02": ("Information Coding", "28.10.2025"), "03": ("Data Structures", "04.11.2025"),
    "04": ("Software", "11.11.2025"), "05": ("Algorithms", "18.11.2025"),
    "06": ("Recursion", "25.11.2025"), "07": ("Sorting Algorithms", "02.12.2025"),
    "08": ("Time Complexity", "09.12.2025"), "09": ("Theoretical Computer Science", "16.12.2025"),
    "10": ("Machine Learning", "06.01.2026"), "11": ("Databases", "13.01.2026"),
    "12": ("Parallel Programming", "20.01.2026"), "13": ("Social Science Applications", "27.01.2026"),
}
DECKFILE = {
    "02": "ICSS-2026-02-InformationCoding", "03": "ICSS-2026-03-DataStructures",
    "04": "ICSS-2026-04-Software", "05": "ICSS-2026-05-Algorithms",
    "06": "ICSS-2026-06-Recursion", "07": "ICSS-2026-07-SortingAlgorithms",
    "08": "ICSS-2026-08-TimeComplexity", "09": "ICSS-2026-09-TheoreticalCS",
    "10": "ICSS-2026-10-MachineLearning", "11": "ICSS-2026-11-Databases",
    "12": "ICSS-2026-12-ParallelProgramming", "13": "ICSS-2026-13-SocialScienceApplications",
}

# Supplementary slides: (example id) -> list of (title, markdown body)
EXTRA = {
    "X10-C": [("C · How many groups? · choosing K, and when K-means is wrong", """
:::: {.columns}
::: {.column width="50%"}
![](figures/10-kmeans-elbow.png){height="10.4em"}
:::
::: {.column width="50%"}
![](figures/10-kmeans-rings.png){height="10.4em"}
:::
::::

::: {.sm}
Left: within-cluster sum of squares for $K = 1 \\ldots 8$; the elbow is at 3. Right: two rings with $K = 2$: K-means
splits them down the middle because it can only make convex, roughly round clusters. It returned two clusters
because it was asked for two, not because there are two.
:::
""")],
    "X05-C": [("C · Solve the maze · BFS versus DFS", """
::: {.sm}
Both find *a* path. Only breadth-first search finds the **shortest**, because it explores in order of
distance. Depth-first search commits to a corridor and backtracks only at dead ends: cheaper in memory,
because the stack holds one path, and more expensive in path length.
:::

| | Breadth-first | Depth-first |
|---|---|---|
| next cell | oldest discovered (queue) | newest discovered (stack) |
| finds | shortest path | some path |
| memory | the whole frontier | one path |
| used for | distances, contact tracing, Erdős numbers | recursion, cycle detection, mazes by hand |

::: {.sm}
Session 6 introduces DFS properly; this table is a preview.
:::
""")],
}


def yaml(sess):
    topic, date = SESSIONS[sess]
    n = int(sess)
    return f"""---
title: "<span class='course'>Introduction to Computing for the Social Sciences</span><br><span class='session'>Session {n} &ndash; {topic}</span><br><span class='session' style='font-size:.7em'>Question &amp; answer examples</span>"
author: "David Garcia<br><span class='semester'>Winter Semester 2026-2027</span>"
format:
  revealjs:
    theme: [default, ../../theme/unikn.scss]
    width: 1280
    height: 720
    margin: 0.06
    center: false
    slide-number: c
    show-slide-number: all
    progress: true
    controls: true
    history: true
    logo: ../../theme/unikn-logo.png
    footer: "<span class='fbar-left'>Session {sess}</span><span class='fbar-mid'>Introduction to Computing for the Social Sciences</span><span class='fbar-right'>Winter Semester 2026-2027</span>"
    highlight-style: github
    link-external-newwindow: true
    fig-align: left
    auto-stretch: false
---
"""


_DIM = {}


def dims(rel):
    """(width, height) in px of an image in the figures/ folder of an example deck."""
    if rel in _DIM:
        return _DIM[rel]
    import glob
    hits = glob.glob(os.path.join(OUT, "*-Examples", rel))
    assert hits, f"figure not found in any Slides/Examples/NN-Examples/: {rel}"
    path = hits[0]
    if rel.endswith(".svg"):
        head = open(path, errors="ignore").read(6000)
        m = re.search(r'viewBox="[\d.\-]+[ ,]+[\d.\-]+[ ,]+([\d.]+)[ ,]+([\d.]+)"', head)
        if m:
            w, h = float(m.group(1)), float(m.group(2))
        else:
            mw = re.search(r'<svg[^>]*\swidth="([\d.]+)', head)
            mh = re.search(r'<svg[^>]*\sheight="([\d.]+)', head)
            w, h = float(mw.group(1)), float(mh.group(1))
    else:
        from PIL import Image
        w, h = Image.open(path).size
    _DIM[rel] = (w, h)
    return w, h


def fit(rel, maxw, maxh):
    """Width in slide px so the image fits a maxw x maxh box (1280x720 slide)."""
    w, h = dims(rel)
    return int(w * min(maxw / w, maxh / h)), int(h * min(maxw / w, maxh / h))


def title_lines(heading):
    """Lines the slide title takes on its plate: the text is set in Arial at 1.18 x 37.5 px
    (Liberation Sans has the same metrics), and the plate holds about 1000 px of text."""
    from PIL import ImageFont
    font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 44)
    return 1 if font.getlength(heading) <= 1000 else 2


# Figure heights tuned on the rendered slides (tools/tuneexamples.py): slide heading -> max height in px.
# A slide without an entry uses the default box below; the tuner grows or shrinks each figure until its
# slide is full without overflowing.
FIGSIZE_FILE = os.path.join(HERE, "examples_figsize.json")
FIGSIZE = json.load(open(FIGSIZE_FILE)) if os.path.exists(FIGSIZE_FILE) else {}
FIGSLIDES = {}          # heading -> {"img": rel, "maxw": px}, read by the tuner


def img_px(part, maxw, maxh, heading=""):
    if not part["img"]:
        return "", 0
    if heading in FIGSIZE:
        maxh = FIGSIZE[heading]
    else:
        maxh -= 55 * (title_lines(heading) - 1)      # a two-line title takes one line of figure room
    FIGSLIDES[heading] = {"img": part["img"], "maxw": maxw}
    w, h = fit(part["img"], maxw, maxh)
    cred = f"\n\n::: {{.source}}\n{part['credit']}\n:::" if part["credit"] else ""
    return f'![]({part["img"]}){{width="{w}px"}}{cred}', h


def is_wide(part):
    w, h = dims(part["img"])
    return w / h >= 1.7


def img_block(part, default_h):
    if not part["img"]:
        return ""
    h = part["imgh"] or default_h
    cred = f"\n\n::: {{.source}}\n{part['credit']}\n:::" if part["credit"] else ""
    return f'![]({part["img"]}){{height="{h}em"}}{cred}'


def slide_open(xid, letter, d):
    o = d["open"]
    tag = '[Opening question · place after the Overview slide]{.tag .ex-open}'
    head = f'## {letter} · {d["title"]}\n\n{tag}\n\n'
    body = "::: {.sm}\n" + o["body"].strip("\n") + f'\n\n[{o["ask"]}]{{.ask}}\n:::'
    if not o["img"]:
        return head + body + "\n"
    if is_wide(o):
        img, _ = img_px(o, 1150, 215, f'{letter} · {d["title"]}')
        return head + img + "\n\n" + body + "\n"
    img, _ = img_px(o, 540, 470, f'{letter} · {d["title"]}')
    return (head + ':::: {.columns}\n::: {.column width="46%"}\n' + img
            + '\n:::\n::: {.column width="54%"}\n' + body + "\n:::\n::::\n")


def slide_close(xid, letter, d):
    """The answer is two slides when it has a figure: the figure at a size that
    can be read from the back of the room (with the question as a callback if
    there is room), and then the reasoning with the 'what we used' box."""
    c = d["close"]
    o = d["open"]
    tag = '[The answer · place before the Summary slide]{.tag .ex-close}'
    body = "::: {.sm}\n" + c["body"].strip("\n") + "\n:::"
    uses = f'\n\n::: {{.uses}}\n**What we used:** {c["uses"]}\n:::'
    if not c["img"]:
        return f'## {letter} · {d["title"]} · answer\n\n{tag}\n\n' + body + uses + "\n"
    callback = f'::: {{.sm}}\n*The question was:* {o["ask"]}\n:::'
    head = f'## {letter} · {d["title"]} · answer\n\n{tag}\n\n'
    if is_wide(c):
        img, h = img_px(c, 1150, 470, f'{letter} · {d["title"]} · answer')
        w0, h0 = dims(c["img"])
        flat = 1150 * h0 / w0 <= 300                 # a flat figure leaves room for the question callback
        fig = head + img + ("\n\n" + callback if flat else "") + "\n"
    else:
        img, h = img_px(c, 600, 470, f'{letter} · {d["title"]} · answer')
        fig = (head + ':::: {.columns}\n::: {.column width="52%"}\n' + img
               + '\n:::\n::: {.column width="48%"}\n' + callback + "\n:::\n::::\n")
    why = (f'## {letter} · {d["title"]} · why\n\n{tag}\n\n' + body + uses + "\n")
    return fig + "\n" + why


def slide_notes(xid, letter, d):
    links = (f"**Self-study:** post `Examples/posts/{xid}-….md` · "
             f"notebook `Examples/notebooks/{xid}.ipynb`, the problem and the solution in a few cells.")
    return (f'## {letter} · {d["title"]} · notes\n\n'
            f'[{xid}]{{.tag .ex-id}}\n\n::: {{.xxs}}\n{d["notes"]}\n\n{links}\n:::\n')


def overview(sess, ids):
    topic, _ = SESSIONS[sess]
    rows = []
    for letter, xid in zip("ABC", ids):
        d = X[xid]
        rows.append(f'| **{letter}** | {d["title"]} | {d["tagline"]} | `{xid}` |')
    return ("## Three questions for this session\n\n"
            "::: {.sm}\n"
            "Each example is an **opening** question for the start of the lecture and an **answer** for the\n"
            "end, followed by a notes slide. Copy the slides you want into the main deck.\n"
            ":::\n\n"
            "::: {.xs}\n| | Question | Hook | id |\n|-|-----------|---------------|---|\n" + "\n".join(rows) + "\n:::\n\n"
            "::: {.xs}\n"
            f"Main deck `Slides/{DECKFILE[sess][10:]}/` · transcript `Transcripts/{sess}-…md` (the § in the answers)\n:::\n")


def write_deck(sess):
    ids = [f"X{sess}-{c}" for c in "ABC"]
    parts = [yaml(sess), overview(sess, ids)]
    for letter, xid in zip("ABC", ids):
        d = X[xid]
        parts.append(f"<!-- EXAMPLE:{xid}:BEGIN -->")
        parts.append(slide_open(xid, letter, d))
        parts.append(slide_close(xid, letter, d))
        for title, body in EXTRA.get(xid, []):
            parts.append(f"## {title}\n\n{body.strip()}\n")
        parts.append(slide_notes(xid, letter, d))
        parts.append(f"<!-- EXAMPLE:{xid}:END -->")
    os.makedirs(os.path.join(OUT, f"{sess}-Examples", "figures"), exist_ok=True)
    path = os.path.join(OUT, f"{sess}-Examples", f"ICSS-2026-{sess}-Examples.qmd")
    text = keep_fit("\n".join(parts), path)
    with open(path, "w") as f:
        f.write(text)
    return path


FIT = re.compile(r"^(## .*?)\s*\{\.(fit\d)\}\s*$")


def keep_fit(text, path):
    """Carry the per-slide {.fitN} classes of the existing deck over to the regenerated one.
    They are set by measuring the rendered slides (see Slides/theme/unikn.scss)."""
    if not os.path.exists(path):
        return text
    fits = {}
    for line in open(path).read().split("\n"):
        m = FIT.match(line)
        if m:
            fits[m.group(1).strip()] = m.group(2)
    out = []
    for line in text.split("\n"):
        if line.startswith("## ") and line.strip() in fits:
            line = f"{line.rstrip()} {{.{fits[line.strip()]}}}"
        out.append(line)
    return "\n".join(out)


def write_readme():
    lines = ["# Question & answer example decks", "",
             "One deck per session (2–13), three examples each. Every example is a pair of slides,",
             "an **opening** question for the start of the lecture and an **answer** for the end that",
             "names what the lecture taught, plus a notes slide for the lecturer (sources, facts,",
             "how to present, where it plugs into the main deck).", "",
             "Each deck lives in its own folder, `NN-Examples/`, with a `figures/` folder holding only",
             "the figures it uses; the theme and the logo are shared in `Slides/theme/`.", "",
             "Built like the main decks: `bash tools/buildex.sh ICSS-2026-05-Examples`. Content lives in",
             "`tools/examples_data_a.py` (sessions 2–7) and `tools/examples_data_b.py` (8–13); figures",
             "are generated by `tools/genexamples_figs.py`; `tools/genexamples.py` writes the decks.", "",
             "Images from outside the project are credited on the slide: XKCD (CC BY-NC 2.5),",
             "Wikimedia Commons (CC BY-SA 3.0 / CC BY 2.0 / public domain, as noted).", "",
             "| Session | Deck | A | B | C |", "|---|---|---|---|---|"]
    for sess in SESSIONS:
        t = [X[f"X{sess}-{c}"]["title"] for c in "ABC"]
        lines.append(f"| {int(sess)} {SESSIONS[sess][0]} | `ICSS-2026-{sess}-Examples.qmd` | {t[0]} | {t[1]} | {t[2]} |".replace(f"`ICSS-2026-{sess}-Examples.qmd`", f"`{sess}-Examples/ICSS-2026-{sess}-Examples.qmd`"))
    lines += ["", "To move a pair into a main deck, copy the block between `<!-- EXAMPLE:Xnn-L:BEGIN -->` and",
              "`…:END -->` from the examples deck, and copy the figures it uses from the deck's `figures/` folder",
              "into the main deck's `figures/` folder. The `.ex-open` / `.ex-close` tags are meant to be deleted",
              "at that point.", ""]
    with open(os.path.join(OUT, "README.md"), "w") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    for sess in SESSIONS:
        print("deck", write_deck(sess))
    write_readme()
    json.dump(FIGSLIDES, open(os.path.join(HERE, "examples_figslides.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{len(X)} examples, {len(SESSIONS)} decks")
