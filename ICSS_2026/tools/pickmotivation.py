#!/usr/bin/env python3
"""Apply the choices in `MotivatingExamples.md`: delete every motivating example
that was not ticked, from both the deck and the transcript.

    python3 tools/pickmotivation.py            # dry run -- report only
    python3 tools/pickmotivation.py --apply    # delete, then re-render the decks
    python3 tools/pickmotivation.py --apply --no-build   # delete only

Only text between `<!-- MOTIVATION:ID:BEGIN -->` and the matching `:END` marker
is ever touched. If a session ends up with **no** examples kept, the wrapping
"Motivating examples" section and its Contents entry are removed from the
transcript as well, so nothing empty is left behind.

To start over with all three candidates restored:

    python3 tools/genmotivation.py
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import genmotivation as G  # noqa: E402
from motivation_data import M  # noqa: E402

ROOT = G.ROOT
SELECTOR = os.path.join(ROOT, "MotivatingExamples.md")

TICK = re.compile(r"^\s*-\s*\[([ xX])\]\s*\*\*(M\d\d-[A-Z])\*\*", re.M)


def read_choices():
    if not os.path.exists(SELECTOR):
        raise SystemExit(f"{SELECTOR} not found -- run genmotivation.py first")
    with open(SELECTOR) as f:
        text = f.read()
    found = {mid: (mark.lower() == "x") for mark, mid in TICK.findall(text)}
    missing = sorted(set(M) - set(found))
    if missing:
        raise SystemExit("selector file does not list: " + ", ".join(missing))
    return found


def block_re(mid):
    return re.compile(
        rf"[ \t]*<!-- MOTIVATION:{mid}:BEGIN -->.*?"
        rf"<!-- MOTIVATION:{mid}:END -->[ \t]*\n?", re.S)


def drop(path, mids):
    with open(path) as f:
        text = f.read()
    before = text
    for mid in mids:
        text = block_re(mid).sub("", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text, (text != before)


def prune_empty_section(text):
    """If the 'Motivating examples' section has no candidates left, drop it."""
    m = G.SECTION.search(text)
    if m and "<!-- MOTIVATION:" not in m.group(0):
        text = G.SECTION.sub("", text)
        text = G.TOC.sub("", text)
    return text


def single_heading(text, kept):
    """With one candidate left, the 'A ·' / 'B ·' prefix is noise -- drop it."""
    if len(kept) != 1:
        return text
    return re.sub(r"^### [A-Z] · ", "### ", text, flags=re.M)


def fix_intro(text, n_kept):
    """The transcript blurb says 'Three candidate openings' -- correct it once
    the choice has been made."""
    if n_kept == 1:
        new = ("The situation this session is the answer to. It is the example\n"
               "used to open the lecture; the rest of the transcript is the\n"
               "material that resolves it.\n")
    elif n_kept > 1:
        new = (f"The {n_kept} situations this session is the answer to. They are\n"
               "the examples used to open the lecture; the rest of the\n"
               "transcript is the material that resolves them.\n")
    else:
        return text
    return text.replace(G.INTRO, new)


def main():
    apply = "--apply" in sys.argv
    build = "--no-build" not in sys.argv
    G.discover()
    choices = read_choices()

    touched_decks = []
    print(f"{'session':>8}  kept                     removed")
    print("-" * 62)
    for sess in G.sessions():
        ids = G.ids_for(sess)
        keep = [i for i in ids if choices[i]]
        cut = [i for i in ids if not choices[i]]
        print(f"{int(sess):>8}  {', '.join(keep) or '(none)':<24} "
              f"{', '.join(cut) or '(none)'}")
        if not cut:
            continue

        deck_text, deck_changed = drop(G.DECKS[sess], cut)
        text_text, text_changed = drop(G.TEXTS[sess], cut)
        text_text = prune_empty_section(text_text)
        text_text = fix_intro(text_text, len(keep))
        text_text = single_heading(text_text, keep)

        if apply:
            if deck_changed:
                with open(G.DECKS[sess], "w") as f:
                    f.write(deck_text)
                touched_decks.append(G.DECKS[sess])
            if text_changed:
                with open(G.TEXTS[sess], "w") as f:
                    f.write(text_text)

    total_keep = sum(1 for v in choices.values() if v)
    print("-" * 62)
    print(f"keeping {total_keep} of {len(choices)}")

    if not apply:
        print("\nDry run. Re-run with --apply to make the changes.")
        return
    if not build:
        print("\nDone. Decks not re-rendered (--no-build).")
        return

    print("\nre-rendering:")
    build_sh = os.path.join(ROOT, "tools", "build.sh")
    for path in touched_decks:
        base = os.path.basename(path)[:-4]
        out = subprocess.run(["bash", build_sh, base],
                             capture_output=True, text=True).stdout
        print(f"  {base:<44} {' '.join(out.split())}")
    print("\nExpected page count: the 2025 original plus the number of "
          "examples kept for that deck.")


if __name__ == "__main__":
    main()
