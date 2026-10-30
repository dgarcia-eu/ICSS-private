#!/usr/bin/env python3
"""Knit the self-study material to HTML so every link opens in a browser.

  Examples/posts/*.md      -> posts/*.html      (pandoc, MathJax, style.css)
  Examples/README.md       -> Examples/index.html
  Examples/notebooks/*.ipynb -> notebooks/*.html (nbconvert, outputs included)
  Transcripts/*.md         -> Transcripts/*.html (so "what we used" links resolve)

Links are rewritten for the HTML world: .ipynb -> .html (the rendered
notebook), .md -> .html, .qmd -> .html (the rendered deck).  The .ipynb files
themselves stay where they are for Jupyter.

    python3 tools/knitexamples.py
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "Examples")
TR = os.path.join(ROOT, "Transcripts")
CSS = os.path.join(EX, "style.css")

LINK = re.compile(r'(\[([^\]]*)\]\()([^)#\s]+?)(\.ipynb|\.md|\.qmd)(#[^)]*)?(\))')


def rewrite(text):
    def sub(m):
        label, target = m.group(2), m.group(3)
        if target.startswith(("http://", "https://")) or label == "ipynb":
            return m.group(0)          # raw notebook files stay downloadable for Jupyter users
        return f"{m.group(1)}{target}.html{m.group(5) or ''}{m.group(6)}"
    return LINK.sub(sub, text)


def nav(depth_to_examples, extra=""):
    p = "../" * depth_to_examples
    return (f'<p class="nav"><a href="{p}index.html">← all examples</a>'
            f'<a href="{p}../Transcripts/00-Conventions.html">notation</a>{extra}</p>\n\n')


def pandoc(md_text, out_html, css_rel, title=None):
    args = ["pandoc", "--from", "markdown+smart+gfm_auto_identifiers", "--to", "html5", "--standalone",
            "--mathjax", "--css", css_rel, "--output", out_html]
    if title:
        args += ["--metadata", f"title={title}"]
    else:
        args += ["--metadata", "pagetitle=ICSS"]
    subprocess.run(args, input=md_text, text=True, check=True)


def first_heading(text):
    m = re.search(r"^# (.+)$", text, re.M)
    return m.group(1) if m else "ICSS"


def knit_posts():
    n = 0
    for f in sorted(os.listdir(os.path.join(EX, "posts"))):
        if not f.endswith(".md"):
            continue
        src = os.path.join(EX, "posts", f)
        text = rewrite(open(src).read())
        text = text.replace("# " + first_heading(text) + "\n", "", 1)  # pandoc gets the title from metadata
        pandoc(nav(1) + text, src[:-3] + ".html", "../style.css", title=first_heading(open(src).read()))
        n += 1
    return n


def knit_index():
    text = rewrite(open(os.path.join(EX, "README.md")).read())
    title = first_heading(text)
    text = text.replace("# " + title + "\n", "", 1)
    text = "<style>body { max-width: 66em; }</style>\n\n" + text
    pandoc(text, os.path.join(EX, "index.html"), "style.css", title=title)


def knit_transcripts():
    n = 0
    for f in sorted(os.listdir(TR)):
        if not f.endswith(".md") or f == "README.md":
            continue
        src = os.path.join(TR, f)
        raw = open(src).read()
        text = rewrite(raw)
        title = first_heading(text)
        text = text.replace("# " + title + "\n", "", 1)
        pandoc(nav(0, "").replace("index.html", "../Examples/index.html").replace("../Transcripts/", "")
               + text, src[:-3] + ".html", "../Examples/style.css", title=title)
        n += 1
    return n


def knit_notebooks():
    nbdir = os.path.join(EX, "notebooks")
    files = sorted(f for f in os.listdir(nbdir) if f.endswith(".ipynb"))
    subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "html", "--log-level", "ERROR"]
                   + [os.path.join(nbdir, f) for f in files], check=True)
    return len(files)


if __name__ == "__main__":
    print("posts      ", knit_posts())
    knit_index(); print("index       1")
    print("transcripts", knit_transcripts())
    print("notebooks  ", knit_notebooks())
