#!/usr/bin/env python3
"""Write the motivating examples of `motivation_data.py` into the decks and
transcripts, and generate the selector file `MotivatingExamples.md`.

Everything it writes is wrapped in HTML comment markers:

    <!-- MOTIVATION:M05-B:BEGIN -->  ...  <!-- MOTIVATION:M05-B:END -->

so a later pass (`pickmotivation.py`) can delete whichever candidates David did
not choose without touching anything else. The script is **idempotent**: it
strips every existing marked block before inserting, so it can be re-run after
editing `motivation_data.py`.

    python3 tools/genmotivation.py            # write decks + transcripts + selector
    python3 tools/genmotivation.py --strip    # remove everything it ever wrote

Slide insertion point: immediately after the last `## Outline` / `## Overview`
slide, i.e. before the first content slide.
Transcript insertion point: a new "Motivating examples" section between the
Contents list and section 1.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from motivation_data import M  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLIDES = os.path.join(ROOT, "Slides")
TRANSCRIPTS = os.path.join(ROOT, "Transcripts")

DECKS = {}      # "02" -> filename, filled in by discover()
TEXTS = {}


def discover():
    for d in sorted(os.listdir(SLIDES)):                     # Slides/NN-Name/ICSS-2026-NN-Name.qmd
        if not os.path.isdir(os.path.join(SLIDES, d)):
            continue
        for f in sorted(os.listdir(os.path.join(SLIDES, d))):
            m = re.match(r"ICSS-2026-(\d\d)-.*\.qmd$", f)
            if m:
                DECKS[m.group(1)] = os.path.join(SLIDES, d, f)
    for f in sorted(os.listdir(TRANSCRIPTS)):
        m = re.match(r"(\d\d)-.*\.md$", f)
        if m and m.group(1) != "00":
            TEXTS[m.group(1)] = os.path.join(TRANSCRIPTS, f)


def sessions():
    """The deck numbers that have motivating examples, in order."""
    return sorted({mid[1:3] for mid in M})


def ids_for(sess):
    return sorted(mid for mid in M if mid[1:3] == sess)


# --------------------------------------------------------------------- strip

BLOCK = re.compile(
    r"[ \t]*<!-- MOTIVATION:[A-Z0-9-]+:BEGIN -->.*?"
    r"<!-- MOTIVATION:[A-Z0-9-]+:END -->[ \t]*\n?",
    re.S)
SECTION = re.compile(
    r"[ \t]*<!-- MOTIVATION-SECTION:BEGIN -->.*?"
    r"<!-- MOTIVATION-SECTION:END -->[ \t]*\n?",
    re.S)
TOC = re.compile(
    r"[ \t]*<!-- MOTIVATION-TOC:BEGIN -->.*?"
    r"<!-- MOTIVATION-TOC:END -->[ \t]*\n?",
    re.S)


def strip_all(text):
    text = SECTION.sub("", text)
    text = TOC.sub("", text)
    text = BLOCK.sub("", text)
    return re.sub(r"\n{4,}", "\n\n\n", text)


# --------------------------------------------------------------------- slides

def slide_block(mid):
    d = M[mid]
    return (f"<!-- MOTIVATION:{mid}:BEGIN -->\n"
            f"## {d['title']}\n\n"
            f"{d['slide']}\n"
            f"<!-- MOTIVATION:{mid}:END -->\n")


def write_deck(sess, strip_only=False):
    path = DECKS[sess]
    with open(path) as f:
        text = strip_all(f.read())

    if not strip_only:
        # The opening slides of every deck are the title, "Course Outline",
        # and one or more overview slides -- which are the ones whose body uses
        # the `.outline` class. (Their titles vary: "Outline", "Overview", and
        # in deck 8 the session name itself.) Insert after the last of those,
        # i.e. immediately before the first real content slide.
        heads = [m for m in re.finditer(r"^## .*$", text, re.M)]
        bodies = [text[h.end():(heads[i + 1].start() if i + 1 < len(heads)
                                else len(text))]
                  for i, h in enumerate(heads)]
        last_ov = None
        course_outline = None
        for i in range(min(6, len(heads))):
            if re.match(r"^## Course Outline\s*$", heads[i].group(0)):
                course_outline = i
                continue
            if "{.outline" in bodies[i]:
                last_ov = i
        if last_ov is None:
            # Deck 6 has no overview slide at all -- go straight after the
            # course outline, which is still "towards the intro".
            last_ov = course_outline
        if last_ov is None:
            raise SystemExit(f"{path}: no overview or course outline slide")
        if last_ov + 1 >= len(heads):
            raise SystemExit(f"{path}: no content slide after the overview")
        at = heads[last_ov + 1].start()

        blocks = "\n".join(slide_block(mid) for mid in ids_for(sess))
        text = text[:at] + blocks + "\n" + text[at:]

    with open(path, "w") as f:
        f.write(text)
    return path


# ---------------------------------------------------------------- transcripts

INTRO = (
    "Three candidate openings for this session, each a real situation the\n"
    "material is the answer to. **One of these will be used in the lecture**;\n"
    "the others are kept here because they are worth reading anyway.\n")


def text_block(mid, letter):
    d = M[mid]
    return (f"<!-- MOTIVATION:{mid}:BEGIN -->\n"
            f"### {letter} · {d['title']}\n\n"
            f"{d['text']}\n"
            f"<!-- MOTIVATION:{mid}:END -->\n")


def write_transcript(sess, strip_only=False):
    path = TEXTS[sess]
    with open(path) as f:
        text = strip_all(f.read())

    if not strip_only:
        # 1. a Contents entry, numbered 0 so the existing numbering is untouched
        m = re.search(r"^## Contents\n\n", text, re.M)
        if not m:
            raise SystemExit(f"{path}: no '## Contents' section")
        toc = ("<!-- MOTIVATION-TOC:BEGIN -->\n"
               "0. [Motivating examples](#motivating-examples)\n"
               "<!-- MOTIVATION-TOC:END -->\n")
        text = text[:m.end()] + toc + text[m.end():]

        # 2. the section itself, before "## 1. ..."
        m = re.search(r"^## 1\. ", text, re.M)
        if not m:
            raise SystemExit(f"{path}: no '## 1. ' section")
        at = m.start()
        body = "".join(
            text_block(mid, chr(ord("A") + i))
            for i, mid in enumerate(ids_for(sess)))
        section = ("<!-- MOTIVATION-SECTION:BEGIN -->\n"
                   "## Motivating examples\n\n"
                   f"{INTRO}\n"
                   f"{body}"
                   "---\n\n"
                   "<!-- MOTIVATION-SECTION:END -->\n")
        text = text[:at] + section + text[at:]

    with open(path, "w") as f:
        f.write(text)
    return path


# ------------------------------------------------------------------- selector

SELECTOR_HEAD = """# Motivating examples: selector

Each deck from session 2 to session 12 currently carries **three** candidate
opening examples, inserted right after the Overview slide, and each is developed
at length in the matching transcript under *Why this matters*.

## How to choose

Put an `x` in the brackets of the ones you want to **keep**. Leave the rest
empty. You can keep more than one per session, or none.

```
- [x] M05-A ...     keep this one
- [ ] M05-B ...     delete this one
```

Then run:

```bash
python3 tools/pickmotivation.py          # show what would change
python3 tools/pickmotivation.py --apply  # delete the unselected ones and rebuild
```

The script deletes the unchosen candidates from **both** the deck and the
transcript, re-renders every affected deck, and reports the new page counts. It
only ever removes text between the `<!-- MOTIVATION:... -->` markers, so nothing
else can be touched.

If you change your mind afterwards, `python3 tools/genmotivation.py` puts all
three back and you can start again.

## A note on page counts

Until you choose, each deck from 2 to 12 has **3 more slides** than its 2025
original, so the page-parity check in `PROGRESS.md` is off by three for those
decks. After selection it will be off by however many you kept, usually one.

---
"""

SELECTOR_FOOT = """
---

## If none of the three works

Say what the session should open with and I will write it. The ones that tend to
work best are: a **specific number** that is surprising, a **decision someone
actually had to make**, or a **failure with a named cause**, rather than a
general statement that the topic is important.
"""


def write_selector():
    path = os.path.join(ROOT, "MotivatingExamples.md")
    out = [SELECTOR_HEAD]
    titles = {
        "02": "Information Coding", "03": "Data Structures",
        "04": "Software", "05": "Algorithms", "06": "Recursion",
        "07": "Sorting Algorithms", "08": "Time Complexity",
        "09": "Theoretical Computer Science", "10": "Machine Learning",
        "11": "Databases", "12": "Parallel Programming",
    }
    for sess in sessions():
        deck = os.path.relpath(DECKS[sess], SLIDES)
        text = os.path.basename(TEXTS[sess])
        out.append(f"\n## Session {int(sess)}: {titles.get(sess, '')}\n")
        out.append(f"<small>Deck: `Slides/{deck}` · "
                   f"Transcript: `Transcripts/{text}`</small>\n")
        for mid in ids_for(sess):
            d = M[mid]
            pitch = d["pitch"]
            out.append(f"- [ ] **{mid}**: *{d['title']}*  \n"
                       f"  <small>{pitch}</small>")
        out.append("")
    out.append(SELECTOR_FOOT)
    with open(path, "w") as f:
        f.write("\n".join(out))
    return path


# ----------------------------------------------------------------------- main

def main():
    strip_only = "--strip" in sys.argv
    discover()
    for sess in sessions():
        if sess not in DECKS or sess not in TEXTS:
            raise SystemExit(f"session {sess}: deck or transcript missing")
        print("deck      ", write_deck(sess, strip_only))
        print("transcript", write_transcript(sess, strip_only))
    if not strip_only:
        print("selector  ", write_selector())
        print(f"\n{len(M)} candidates across {len(sessions())} sessions "
              f"({len(M) // len(sessions())} per deck).")
        print("Now: bash tools/build.sh <deck> for each, then edit "
              "MotivatingExamples.md.")
    else:
        print("\nall motivating examples removed.")


if __name__ == "__main__":
    main()
