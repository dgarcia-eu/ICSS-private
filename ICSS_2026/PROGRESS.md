# ICSS 2026 (Theory) — project state

Working file for the revision of the **theory** part of ICSS: lectures,
pen-and-paper exercises, and the written exam. Nothing here concerns coding
assignments, tutorials, or the practical part.

Source of truth for the task list: `ICSS-local/Instructions.txt`.

## Where this stands

**All four tasks of `Instructions.txt` are done for all thirteen sessions.**

- **Task 1** — decks converted to Quarto: **13 of 13**.
- **Task 2** — lecture transcripts: **13 of 13**, plus a shared conventions page.
- **Task 3** — exercise sheets: **13 of 13**.
- **Task 4** — exam question pool: **done**, in `Exams/`. 93 items across six
  files, covering every question from the 2023, 2024 and 2025 exams and every
  exercise on the new sheets, plus an assembled 70-point example exam.

On top of that, decks **2–12** each carry **three candidate motivating
examples** at the front, developed at length in the matching transcript. They
are waiting for a decision — see [`MotivatingExamples.md`](MotivatingExamples.md)
and *Pending* below.

There is also a second, separate set: **question & answer example decks** in
`Slides/Examples/` — one deck per session 2–13, three examples each, every one
an *opening* question for the start of the lecture and an *answer* for the end
that names what was learned. These are extra material to pick from, not
inserted into the main decks.

What is left is that decision, the **year rollover pass** (dates, semester
string, staff names), and the open questions listed under *Pending*.

Every finished deck has been verified three ways: it renders, it prints to
exactly the same number of pages as the 2025 PDF (so no slide was dropped,
merged or split), and an automatic scan confirms no slide has content running
off an edge or into the footer bar.

## Layout

```
ICSS_2026/
  PROGRESS.md              this file
  MotivatingExamples.md    tick the opening examples to keep; the rest get deleted
  tools/             deckprep.sh, build.sh, figure generators (see tools/README.md)
    motivation_data.py   the 33 candidate opening examples (slide + transcript text)
    examples_data_a/b.py the 36 question/answer examples (sessions 2-7 / 8-13)
    genexamples.py       writes Slides/Examples/*.qmd;  genexamples_figs.py draws their figures
    buildex.sh           build.sh for the Examples decks
    exnb_a/b.py          notebook cells for the 36 examples; genexnotebooks.py builds + executes them
    knitexamples.py      knits posts, index, transcripts and notebooks to HTML with browser-ready links
    genmotivation.py     writes them into the decks and transcripts
    pickmotivation.py    reads MotivatingExamples.md and deletes the rest
  Slides/            Quarto decks (one per session) + unikn.scss theme
    Examples/        question & answer example decks, one per session 2-13 (see its README)
      figures/       generated figures (tools/genexamples_figs.py)
      images/        fetched images with licences: XKCD (CC BY-NC), Wikimedia Commons
    images/NN/       bitmap images cut from the original pptx, per deck
    figures/         diagrams re-drawn as SVG (mine, not cut from the pptx)
  Transcripts/       markdown lecture transcripts (01-13 + 00-Conventions)
  TheoryExercises/   markdown exercise sheets (01-13)
    figures/         figures redrawn from the 2023/24 and 2024/25 sheets
  Examples/          the 36 question/answer examples for self-study
    README.md          index: post + notebook + slides for every example  (index.html = knitted)
    style.css          the one stylesheet for all knitted pages
    posts/             blog-style posts, one per example, linking to transcript sections
    notebooks/         executed Jupyter notebooks, one per example (+ data/titanic.csv)
  Exams/             exam question pool
    README.md          item format, source tags, errata found in past papers
    Blueprint.md       exam format, the six questions, assembly recipe, rotation
    Pool-1..6-*.md     the items themselves, one file per exam question
    ExamExample-2026.md  a complete 70-point example assembled from the pool
    figures/           figures redrawn from past exam papers
```

## Session list

Slide counts are the check that nothing was lost: the printed 2026 deck must
have exactly as many pages as the 2025 PDF it came from — **plus the motivating
examples**, which are currently 3 per deck for sessions 2–12 and will drop to
however many are chosen.

| # | Topic | Slides | 2025 → 2026 pages | Transcript | Exercises |
|---|---|---|---|---|---|
| 01 | Introduction | done | 42 → 42 | done | done |
| 02 | Information Coding | done | 54 → 54 **+3** | done | done |
| 03 | Data Structures | done | 49 → 49 **+3** | done | done |
| 04 | Programming | done | 68 → 68 **+3** | done | done |
| 05 | Algorithms | done | 49 → 49 **+3** | done | done |
| 06 | Recursion | done | 85 → 85 **+3** | done | done |
| 07 | Sorting Algorithms | done | 78 → 78 **+3** | done | done |
| 08 | Time Complexity | done | 51 → 51 **+3** | done | done |
| 09 | Theoretical Computer Science | done | 79 → 79 **+3** | done | done |
| 10 | Machine Learning | done | 42 → 42 **+3** | done | done |
| 11 | Databases | done | 53 → 53 **+3** | done | done |
| 12 | Parallel Programming | done | 49 → 49 **+3** | done | done |
| 13 | Social Science Applications | done | 41 → 41 | done | done |

<details><summary>old table (kept so nothing is lost)</summary>

| # | Topic | Slides | Transcript | Exercises |
|---|---|---|---|---|
| 01 | Introduction | done | – | – |
| 02 | Information Coding | done | – | – |
| 03 | Data Structures | done | – | – |
| 04 | Programming | done | – | – |
| 05 | Algorithms | done | – | – |
| 06 | Recursion | done | – | – |
| 07 | Sorting Algorithms | done | – | – |
| 08 | Time Complexity | done | – | – |
| 09 | Theoretical Computer Science | done | – | – |
| 10 | Machine Learning | – | – | – |
| 11 | Databases | – | – | – |
| 12 | Parallel Programming | – | – | – |
| 13 | Social Science Applications | – | – | – |

</details>

(Session 14 in the old plan was an exam review with no prepared material.)

Rendered `.html` and `.pdf` sit next to each `.qmd`. The `*_files/` folders are
Quarto's per-deck copy of reveal.js (~5 MB each) — they are build output and can
be deleted and regenerated at any time.

## Conventions

- Decks are named `ICSS-2026-NN-Topic.qmd`, theme is the shared `unikn.scss`.
- Deck content is a **faithful** conversion of the 2025 pptx. Year, dates,
  rooms, and staff names are **not** updated yet — that is a separate pass once
  the conversion is finished (see "Pending" below).
- Image sizes use `em` (24em = full slide height) so they scale with reveal.
- Re-drawn diagrams live in `Slides/figures/` as SVG and are referenced from
  the deck; the original cut bitmap stays in `Slides/images/NN/` so the two can
  be compared. Where the redraw is not clearly faithful, the deck keeps the
  original and carries the redraw in an HTML comment for David to check.

## How to resume

### Converting the next deck (10, 11, 12, 13)

```bash
bash tools/deckprep.sh 10          # unpack the 2025 deck into the scratch dir
```

Then, in order:

1. Read `text.txt` — that is the full content of the deck.
2. Get the slide list. The footer line separates slides, so the title of each
   slide is the first non-empty line after each footer; `tools/README.md` shows
   the snippet. **Write this list down** — the deck must end up with exactly
   this many slides.
3. Look at `map.txt` and `montage.png` together to work out which image is
   which. `map.txt` gives position and size in inches on a 10 × 5.625 in slide;
   the montage shows the pictures in `ls | sort -V` order. Render the individual
   pages in `pages/` for anything ambiguous.
4. Copy and rename the images into `Slides/images/NN/`, then
   `mogrify -resize '1500x1500>' -strip` them and convert the large opaque PNGs
   to JPEG (the loop used for every deck so far is in the session history; it
   keeps the images folder around 1–3 MB per deck).
5. Write `Slides/ICSS-2026-NN-Topic.qmd`, re-drawing diagrams into
   `Slides/figures/` with a `tools/genNN.py`.
6. `bash tools/build.sh ICSS-2026-NN-Topic` until `pages` matches step 2 and
   `overflow: none`.

All thirteen decks are converted, so this recipe is now only needed if a 2025
deck changes or a new session is added.

## Pending / to decide

- **Year rollover pass** (not started, deliberately): semester string, session
  dates in the footer, room numbers, staff names. Each deck carries these in
  exactly two places — the YAML `footer:` and the YAML `author:` — so this is a
  quick mechanical pass once the conversion is finished.
- Slide numbers: the 2025 decks are inconsistent (deck 1 has none, decks 2–13
  number some slides). All 2026 decks currently have **no** slide numbers. If
  you want them for exam review, `slide-number: true` in the YAML plus a small
  rule in `unikn.scss` to keep them clear of the footer bar.
- Number of sessions: 13 content sessions + 1–2 Q&A sessions.
- Deck 6: the eight call-stack slides are page crops rather than re-drawn
  figures (see the log entry). Decks 11 and 13 also use page crops — see the
  log — for figures that are screenshots or composites.
- **Which motivating example opens each of sessions 2–12?** Three candidates
  per deck are in place; tick the keepers in
  [`MotivatingExamples.md`](MotivatingExamples.md) and run
  `python3 tools/pickmotivation.py --apply`. Until then every deck from 2 to 12
  is three pages longer than its 2025 original. If none of the three works for a
  session, say what it should open with instead.
- **Is machine learning examinable?** Session 10 has been in the course since
  2024/25 and has never appeared on an exam. The pool now has items for it
  (`DB-10`–`DB-13`) and the example exam includes two. Decide, and tell the
  students either way in the exam review session. The same question applies, more
  weakly, to session 13.
- Exam total: 60 points with a 30-point pass matches the two most recent real
  exams; the released example uses 70. `Exams/Blueprint.md` recommends keeping
  that split.

## Corrections made to the original decks

Content is otherwise faithful; these are places where the 2025 pptx was wrong
and the Quarto version says something different. Please check you agree.

| Deck | Slide | Original | Now |
|---|---|---|---|
| 02 | IEEE 754, float → decimal | result $-1\,703\,946.0$ | $-1\,703\,936.0$ (1.625 × 2²⁰ = 1 703 936) |
| 02 | ConvertDecimalToBinary | Result written as `x_l … n_2 n_1 n_0` | `x_l … x_2 x_1 x_0` (consistent notation) |
| 02 | Code Pages | "IS0-8859-1" | "ISO-8859-1" |
| 02 | Type Conversion | "Expressions can turned into" | "can be turned into" |

Errata found in **past exam papers** while building the question pool are listed
in `Exams/README.md` — five of them, including an unsorted array given for a
binary-search trace and a base subscript lost from a conversion question.

Not changed, but worth a look:

- Deck 01, *The ICSS Team*: the tutor e-mail addresses do not match the tutor
  names (`Anastasia Siebers → liane.strauch@`, `Niklas Bacher → claire.jordan@`).
  Looks like leftovers from an earlier year.

## Log

- 2026-08-14: theme built (`unikn.scss`), session 1 converted and verified
  (42 slides, one printed page each, no overflow).
- 2026-08-14: session 2 converted (54 slides, exact page parity, no overflow).
  Nine diagrams re-drawn as SVG in `Slides/figures/` (decision trees, IEEE 754
  layouts, two's-complement wheel, ASCII table, snowflake bit layout). The
  extended code-page table was deliberately **not** re-drawn — see the comment
  in the deck. Section-divider slides harmonised across decks 1 and 2
  (`.outline.focus`, current item black + bold, rest grey).
- 2026-08-14: session 3 converted (49 slides, exact page parity, no overflow).
  Twenty diagrams re-drawn as SVG, generated by a parametric script so the
  binary-search-tree variants stay consistent: array, binary-search trace,
  binary tree + legend, the BST family (rules, search, insert, all three delete
  cases, unbalanced), hash collisions, separate chaining. Tree colours are
  harmonised across every figure (grey root, white internal node, green leaf) —
  the original mixed in pink/yellow palettes on the delete slides.
- 2026-08-14: session 4 converted (68 slides, exact page parity, no overflow).
  The von Neumann architecture diagram re-drawn as SVG; the language-type table,
  the paradigm boxes and the code snippet plates rebuilt as HTML/CSS instead of
  pictures, so they are editable. The `Person -> Employee` inheritance boxes are
  CSS boxes; the detailed UML picture is kept as the original bitmap.
- 2026-08-14: session 5 converted (49 slides, exact page parity, no overflow).
  Fifteen figures re-drawn as SVG: the flowchart symbol legend, the profit/loss
  flowchart, queue and stack diagrams, the eight-node example graph and the ten
  states of the breadth-first-search trace (generated from a state table, so the
  distances, parents and queue contents cannot drift apart). The adjacency
  matrix and adjacency list are now LaTeX/HTML rather than pictures.
- 2026-08-14: session 6 converted (85 slides, exact page parity, no overflow).
  Its source is **generated** by `scratchpad/mk06.py`-style scripting logic that
  has been baked into the .qmd — the file is plain Quarto, edit it directly.
  Figures: the seven factorial-evaluation trees, the 21 depth-first-search
  states (again from a state table), the process-memory diagram, the greatest
  common divisor bars and the factorial slot boxes are re-drawn SVGs. The eight
  call-stack build-up slides are **crops of the original PDF pages**, not
  re-drawings: they are screenshots overlaid with hand-drawn arrows, and the
  arrows carry the meaning. Worth re-drawing later if you want them editable.
- 2026-08-14: session 7 converted (78 slides, exact page parity, no overflow).
  All sorting traces re-drawn as SVG. The 31 heapsort states are **simulated**
  by the generator (a real min-heap extract-min with sift-down), so the tree,
  the output array and the captions are guaranteed consistent with each other —
  the original had them drawn by hand. Mergesort split/merge, MERGE, repeated
  minimum search, selection sort, the divide-and-conquer diagram and the heap
  examples are re-drawn too; the Cormen PARTITION and HEAPSORT pseudocode
  pictures are kept as originals (they are quotations from the book).
- 2026-08-14: session 8 converted (51 slides, exact page parity, no overflow).
  Insertion-sort traces and the asymptotic sketch re-drawn as SVG; the runtime
  tables are now HTML. The three bound plots (O, Omega, Theta) and the Big-O
  growth chart are kept as the original bitmaps — they are textbook figures.
- 2026-08-14: session 9 converted (79 slides, exact page parity, no overflow).
  The z0..z3 automaton is now a re-drawn SVG with a highlighted current state
  (nine variants) rather than a bitmap with hand-drawn markers — the original's
  highlight overlays sit on top of the picture and could not be cropped cleanly.
  Turing-machine tape traces, the P/NP/NP-complete/NP-hard Venn diagrams, the
  reduction diagram, the verifier tape and the Hamiltonian-path graphs are also
  re-drawn. Textbook figures (Evans' TM, Sipser cover, XKCD, Pac-Man DFA) stay
  as originals.
- 2026-08-14: **transcripts and exercise sheets for sessions 1–9** written.
  - `Transcripts/00-Conventions.md` fixes the notation once for the whole course
    (pseudocode style, 1-based indices, graph and automaton symbols, complexity
    notation). Every transcript and sheet links to it. This is the answer to the
    "consistent terminology and notation" requirement in `Instructions.txt` —
    if you change a convention, change it there and the rest follows.
  - Transcripts are ~3000–5800 words each and reuse the slide figures from
    `Slides/figures/`, so a diagram in the text is the diagram from the lecture.
    Each ends with a *check yourself* section (answers in collapsible blocks) and
    a references list; sources are also cited inline where used.
  - Exercise sheets port the 2023/24 exercises 1–3 unchanged in substance
    (re-typeset in the course notation, figures redrawn as SVG) and add a
    *battery* of 6–7 further exercises with worked answers, drawn from the
    reading materials and from practical experience — encoding bugs,
    performance traps, pseudonymisation, reductions.
  - All 133 figure links and all cross-links verified to resolve.

- 2026-08-14: sessions 10–13 converted (42/53/49/41 slides, exact page parity,
  no overflow on any of them). Notes per deck:
  - **10 (Machine Learning)** — the most image-heavy deck. `image15` and
    `image34` are single book pages placed three and two times with different
    `a:srcRect` crops; they were cropped with ImageMagick using the srcRect
    percentages into `kmeans-*.png`. Images were identified by rendering each
    page rather than from the contact sheet, as the note above warned.
  - **11 (Databases)** — the running `Product` table is now an **HTML table**
    with CSS highlight variants (`.hl-relation`, `.hl-row`, `.hl-col`,
    `.hl-schema`, …) instead of the repeated bitmap, so the six "what is a
    relation / row / column / schema" slides share one source. Pages 5–10 (the
    vaccine and flight flow diagrams) are page crops. New SVG: `11-sql-flow.svg`.
  - **12 (Parallel Programming)** — eight new SVGs: single-vs-parallel,
    concurrent-vs-parallel, the concurrency context-switch bar, the four
    pipeline diagrams and Flynn's taxonomy.
  - **13 (Social Science Applications)** — all 38 figures are **crops of the
    rendered PDF pages**, positioned from the pptx coordinates in `map.txt`,
    rather than named images. This deck's pictures are screenshots of papers,
    tweets and plots that cannot be meaningfully re-drawn, and cropping from the
    page avoids any risk of attaching the wrong image to a slide.
- 2026-08-14: **transcripts and exercise sheets for sessions 10–13** written,
  following the same pattern as 1–9. Two notes:
  - Sessions 10 and 13 never had an exercise sheet, so sheets 10 and 13 are new
    throughout rather than ported.
  - The 2024 sheet numbering was offset by one: its sheet 10 (Turing machines and
    CLIQUE) covers what is now **lecture 9**. Those two exercises have been added
    to `TheoryExercises09.md` as exercises 3 and 4, with the transition diagram
    and the 5-clique graph re-drawn as SVG (`tools/gen09b.py`).
- 2026-08-14: **Task 4 — exam question pool** built in `Exams/`.
  - Sources read in full: the 2023, 2024 and 2025 exam examples, final exams and
    resit exams (nine papers), plus all thirteen new exercise sheets.
  - 93 items, organised into six files matching the six exam questions. Each item
    carries a stable ID, the point value it had in its source exam, the list of
    exams it has appeared in (so reuse can be tracked), a full worked solution,
    and marking notes naming the errors students actually make.
  - Every numeric answer was **recomputed** rather than copied: the IEEE 754
    encodings were checked against `struct.pack`, the Bellman-Ford and Dijkstra
    traces re-run by hand pass by pass, and the Schelling grid's unsatisfied
    agents computed by `tools/genexam.py`, which also draws the figure — so the
    answer and the picture cannot disagree.
  - `Blueprint.md` records the exam format, the stable six-question structure,
    the point budgets, the formulas that must always be printed in the paper, the
    reuse rotation, and the coverage gaps.
  - Figures redrawn as SVG in `Exams/figures/`: the min-heap before and after
    extract-min, the Dijkstra graph, the Schelling grid. The z0–z3 automaton is
    shared with deck 9.
  - `ExamExample-2026.md` is a complete 70-point paper assembled from the pool,
    with a marking key that must be removed before release.
- 2026-08-15: **motivating examples** added to the front of decks 2–12. Three
  candidates per deck, 33 in all, each one slide plus a full section in the
  matching transcript (under *Motivating examples*, before section 1). Every one
  is a real, cited case: the Excel gene-name corruption, the Vancouver Stock
  Exchange truncation drift, Reinhart–Rogoff, Milgram against the Facebook
  graph, Google Flu Trends, the Public Health England 65 536-row loss, the
  Cloudflare regex outage, and so on. Each slide ends with the question the
  session answers, and each transcript section closes with a *what this session
  gives you* map into the numbered sections.
  - New in the theme: `.motivation`, `.ask`, `.figures`/`.fq` in `unikn.scss`.
  - All eleven decks rebuilt: exactly **+3 pages** each, `overflow: none`.
  - Everything is wrapped in `<!-- MOTIVATION:ID:BEGIN/END -->` markers, so
    removal is mechanical and cannot touch anything else. `genmotivation.py`
    (re)writes all three; `pickmotivation.py` reads the ticks in
    `MotivatingExamples.md` and deletes the rest, tidying up the section heading
    and the Contents entry when a deck ends up with one or none.
- 2026-09-11: **question & answer example decks** built in `Slides/Examples/`,
  one per session 2–13, three examples each (36 in all). Each example is an
  opening question slide, an answer (figure slide + reasoning slide with a
  *what we used* box pointing at transcript sections), and a notes slide for the
  lecturer with sources, facts and how to present. All twelve decks render
  with `overflow: none`.
  - Everything numeric is **computed** by `tools/genexamples_figs.py`: the 2038
    wrap dates, the IEEE 754 hex of 0.1 + 0.2, the word-count timings (measured),
    the BFS maze solution, the Hanoi move count, the quickselect trace, the
    Titanic confusion matrix, the K-means elbow, the Schelling run.
  - Six images are fetched with licences credited on the slide: XKCD 327, 936
    and 1667 (CC BY-NC 2.5), the Königsberg map (CC BY-SA 3.0), a Hanoi photo
    (CC BY-SA 3.0), a Sudoku (public domain). Everything else is drawn.
  - These are separate from the 33 motivating-example candidates in the main
    decks (`MotivatingExamples.md`); they do not overlap in content.
- 2026-09-11: **notebooks and self-study posts for all 36 examples** in `Examples/`.
  - Every example turned out to be illustrable in a simple Python notebook —
    no session needed replacement examples. The 36 notebooks are built from
    `tools/exnb_a.py` / `exnb_b.py` by `tools/genexnotebooks.py`, which also
    executes them; all 36 run cleanly and ship with their outputs.
  - Notebooks stay deliberately small (standard library, NumPy, matplotlib,
    pandas for the Titanic set, scikit-learn for one logistic regression,
    SQLite for the three database examples, threading for the race). Where the
    lecture's claim is numeric — the wrap dates, the float hex, 5 040 bridge
    orderings, the BFS path, quickselect's ~3n comparisons, the Titanic
    confusion matrix, the elbow, the Schelling run, the biased-poll simulation
    — the notebook computes it rather than asserting it.
  - Two notebooks needed care to be honest: the race condition (Python's
    interpreter lock hides it, so the notebook yields explicitly between read
    and write and says so) and the Likes/personality simulation (tuned so the
    accuracy curve sits in the paper's range; labelled as a simulation).
  - 36 blog-style posts in `Examples/posts/`, ~600–900 words each: the puzzle,
    *try it first* (notebook link), what is going on, the answer, why it matters
    for research, and *what we used from the lecture* with links to the numbered
    transcript sections (all anchors verified). `Examples/README.md` indexes
    post, notebook and slide deck for every example.
- 2026-09-11: **everything knitted to HTML** by `tools/knitexamples.py`:
  `Examples/index.html`, `Examples/posts/*.html`, `Examples/notebooks/*.html`
  (nbconvert, outputs included) and `Transcripts/*.html`, so the *what we used*
  links from a post land on the right transcript section in the browser. Links
  are rewritten at knit time (`.ipynb`/`.md`/`.qmd` → `.html`; the `ipynb` links
  on the index keep pointing at the raw files for Jupyter). Anchors use
  GitHub's slug rules so the Markdown and HTML versions share them. 87 pages,
  1 011 local links and anchors checked, none broken. Open
  `Examples/index.html` to start.
- 2026-09-11: **13 historical-background posts**, `Examples/posts/H01…H13`, one per
  session, ~1 000–1 300 words each, on the people and developments behind the
  topic rather than the technique. Each starts from the lecture's own person
  slide where there is one (Hopper, Lovelace, al-Khwarizmi, von Neumann,
  Hinton) and widens the cast; every post includes at least one woman or
  person of colour — e.g. the Harvard and NASA computers and the ENIAC six
  (1), Betty Shannon and Hedy Lamarr (2), Barbara Liskov and Kathleen Booth
  (3), Jean Sammet and Clarence Ellis (4), al-Khwarizmi and Grete Hermann
  (5), Rózsa Péter (6), Betty Holberton (7), Shafi Goldwasser, Manuel Blum and
  the AKS trio (8), Julia Robinson (9), Fei-Fei Li, Fukushima, Buolamwini and
  Gebru (10), Patricia Selinger (11), Frances Allen and Philip Emeagwali (12),
  Lada Adamic, danah boyd, Safiya Noble, Ruha Benjamin and Kathleen Carley
  (13). Dates and attributions were checked against the standard sources
  listed in each post's *Further reading*. Indexed in `Examples/README.md`
  and knitted to HTML with the rest.
- 2026-09-11: **figures in all 49 posts** — 177 figures placed by `tools/figposts.py`
  (a marker → figure spec per post, idempotent), one every two or three
  paragraphs, floated to the side or full width. Example posts reuse the slide
  figures; history posts use 135 portraits and photographs fetched from
  Wikipedia/Commons by `tools/fetchportraits.py`, which keeps only free
  licences (public domain, CC, GFDL) and records author and licence in
  `Examples/posts/img/credits.json`; every caption repeats the credit with a
  link to the Commons page. People without a free portrait (Codd, Church,
  Hamming, Luhn, Kathleen Booth, Grete Hermann, Ellis, Fukushima, Granovetter
  among them) are simply not pictured. Re-knitted; links checked.

## 2026-09-11 — history posts pared back to at most three people each

David: "you overdid it a bit … between 1 and 3 people at most … focus on the
bigger picture … keep at least one minority individual and only keep at most
two of the others."

- All 13 `Examples/posts/H*.md` rewritten. Featured people now (minority
  individual first): H01 Katherine Johnson · Babbage · Lovelace; H02 Hopper ·
  Shannon · Kahan; H03 Liskov · Simon · Knuth; H04 Clarence Ellis · Lovelace ·
  Hopper; H05 al-Khwarizmi · Grete Hermann · Euler; H06 Rózsa Péter · Gödel ·
  McCarthy; H07 Holberton · von Neumann · Hoare; H08 Goldwasser · Agrawal · Cook;
  H09 Julia Robinson · Hilbert · Turing; H10 Fei-Fei Li · Buolamwini · Hinton;
  H11 Selinger · Codd; H12 Fran Allen · Amdahl · Moore; H13 Noble · Simon ·
  Schelling. Everyone else is folded into the narrative unnamed ("a 1965 paper",
  "an IBM memo", "two of its members") so the posts read as the arc of each
  field.
- `tools/figposts.py` H-entries trimmed to one portrait per featured person
  plus context images (machines, cards, ENIAC, ILLIAC, Cray-1, Königsberg,
  Bletchley); 50 figures in the history posts, 129 overall.
- **Incident, fixed:** `figposts.py --strip` truncated every post before
  reading it (`open(p,"w")` was evaluated before `open(p).read()`). The 36
  example posts were restored from the session transcript and verified
  byte-identical against the previously knitted HTML; the bug is fixed.
- Re-knitted; link check 86 html / 666 links / 0 broken. README history
  section updated.

## 2026-09-11 — full review of decks and transcripts against sources

David: "review all materials for ICSS. The slides and the transcripts. Double
check everything against original sources … Rewrite for clarity in my style,
get rid of em dashes completely and merge your mini-paragraphs into larger
more article-style paragraphs … Check that all equations are right and
notation is consistent … Do the same for algorithms."

- Every paper, book chapter, page number, quotation, date and URL in the 13
  decks and 13 transcripts checked against the original (course-book PDFs
  under `ICSS_2022/ReadingMaterials`, the web for the rest); every equation
  re-derived; every algorithm checked against Cormen/CLRS/Sipser and traced.
  All findings and changes are in `REVIEW-2026.md`, one section per session,
  plus a consolidated list of the course-wide notation decisions.
- Notable corrections: Colossus/Lorenz vs Enigma (deck 1); base-conversion
  procedures and IEEE sign factor (deck 2); running-time table 0.2 s / 5 min
  and insertion sort `For i = 2 to n` on all four copies (deck 8); DFA tuple
  with accept states X, ε in the Kleene star, Chomsky names, Sokoban is
  PSPACE-complete (deck 9); Blum at CMU (deck 8); GizmoWorks queries and join
  result (deck 11); Google Flu Trends "more than double", not 140%
  (motivating example M10-A); M07-B arithmetic; section references inside all
  33 motivating examples.
- All pseudocode across the course in one format (Cormen-style `Procedure
  NAME(args)` header, indentation only, 1-based indices in pseudocode and
  0-based in Python), documented in the rewritten `Transcripts/00-Conventions.md`.
- Transcripts 01–13 rewritten in article-style paragraphs, American spelling,
  no em dashes; section headings kept (two Americanized: "Asymptotic behavior
  and O-notation", "Agent-based modeling") and the four posts linking to them
  updated. Motivating examples rewritten in `tools/motivation_data.py` and
  regenerated; `genmotivation.py` no longer produces em dashes.
- All 13 decks rebuilt with the expected page counts and no overflow; the
  `.pdf` copies refreshed. Re-knitted: 100 HTML files, 1 082 links, 0 broken.
- Still to do, outside this pass: the Examples decks and posts, exercise
  sheets and exam pool keep their em dashes and British spellings; the "260
  wounded" figure on deck 2 could not be verified; the open decisions (tick
  `MotivatingExamples.md`, whether ML is examinable, the year rollover) are
  unchanged.

## 2026-09-11 — second review pass: example decks, posts and notebooks

David: "Do now the example decks and posts. Also verify the jupyter
notebooks."

- All 36 question-and-answer examples reviewed in their three forms (deck
  data in `tools/examples_data_*.py`, post, notebook cells in
  `tools/exnb_*.py`) plus the 13 history posts: sources checked against the
  originals, numbers recomputed, section references checked against the
  transcript headings, exam-item ids checked against `Exams/`. Findings and
  changes are in `REVIEW-2026.md`, "Second pass".
- Corrections of fact include the Boeing 787 counter (248 days, not 49), the
  Ariane 5 failure sequence (backup first), the string-sum example whose
  figure started the total at `0` (Python refuses) and whose numbers did not
  agree, the fractal tree (512 tips needs depth 10, figure regenerated), two
  reading references to *Algorithms Unlocked* for topics it does not cover,
  the Sipser "coin machine", Facebook's 3.57 degrees (a probabilistic
  estimate), the K-means WSS values quoted from the wrong run, and an MRZ
  notebook that emitted a Turkish Ş.
- All 49 posts rewritten in the transcript style (article paragraphs, no em
  dashes, American spelling); deck text and notebook markdown likewise; the
  K-means and fractal-tree procedures in the course pseudocode; notebook
  identifiers Americanized. `genexamples.py` titles now use "· answer / why /
  notes"; `figposts.py` markers and captions updated; `Examples/README.md`
  regenerated from the data.
- Eleven em dashes hidden as `&mdash;` in main decks 9, 10 and 13 (missed by
  the first pass) fixed; the three decks rebuilt (82, 45, 41 pages) and PDFs
  refreshed.
- Verified: 36/36 notebooks execute cleanly; 12 example decks rebuilt with
  unchanged page counts and no overflow; 100 HTML files knitted, 1 084 links,
  0 broken.
- Still outside the review: `TheoryExercises/` and `Exams/`.

## 2026-09-18 — third pass: exercise sheets, exam pools and solution files

David: "I need you to make a pass over the TheoryExercise sheets and the
Exams exercise pools. I want you to make a subfolder inside each of the two
folders with the solutions. For each pool or theory exercise sheet, make one
file with the solutions. For each solution, add a reference to the slides and
the handouts where the content can be found to develop the solution."

- All 13 sheets and all 93 pool items reviewed: every number and trace
  recomputed by script, figures rendered and read, sources checked. Five
  errors found on the sheets (a transposed hex digit, a snowflake timestamp,
  a missing start node, a Fibonacci estimate, a sorting-trace array) and
  fixed; none in the pools. Details in `REVIEW-2026.md`, "Third pass".
- `TheoryExercises/Solutions/TheoryExercisesNN-Solutions.md`, 13 files,
  hand-written: full solutions to the session exercises (which had none) plus
  the additional-practice answers, each with a "Where to look" line giving
  slide numbers and titles and linked handout sections. The collapsible
  answers were removed from the sheets, which now link to their solutions
  file.
- `Exams/Solutions/Pool-N-…-Solutions.md`, 6 files plus a README, generated
  from the pools by the new `tools/gensolutions.py`, whose `REFS` table holds
  the slide and handout references of all 93 items. Pools remain the master.
- Nineteen numbered Cormen-style pseudocode blocks in the pool solutions
  converted to the course format; em dashes removed from all 23 files of
  the two folders (544 in total); spelling Americanized; both READMEs
  updated.
- Verified: generator runs clean; all links and anchors in the 19 new files
  resolve; no em dash, no `<details>`, no numbered pseudocode outside quoted
  exam listings.

## 2026-09-18 — "why it matters" notebooks, solution figures, clarity review

David: "For each lecture excluding the first one, develop a notebook with
python code that illustrates why the content of the lecture matters. […] The
idea is that the notebooks are standalone and complete but also minimal […]
I am not sure if this makes sense for the last lecture, think about it. Then
make a pass over exercise solutions and make sure they are not too verbose
[…] and that they contain graphics and visualizations […] Then make a pass
over everything to check that exercises and exam pools are clear, complete,
and unambiguous for students, that the solutions are correct and complete,
and that they are explained in a way such that a student can understand
them."

- New `WhyItMatters/`: 12 notebooks (W02 to W13), each two or three small,
  seeded, standalone experiments with a figure and a "What we used" line
  linking the handout sections; built, executed and knitted to HTML by the
  new `tools/genwhy.py` from `tools/why_NN.py`; README generated. Session 13
  included (algorithmic confounding, equifinality and parallel worlds), since
  both of its computational lessons are demonstrable in a few lines.
- New `tools/gensolfigs.py`: 19 figures for the sheet solutions (trees,
  graphs with traces, heaps, automaton, stack, plots, schema, Schelling
  grid); ASCII diagrams replaced; the BFS and Bellman-Ford figures reused in
  pool items `GP-03` and `GP-08`. Solutions of sheets 9 to 13 tightened.
- Third reading of every sheet, pool item, the blueprint and the example
  exam: eight question wordings made precise, ten solution errors fixed
  (mergesort comparison count 15 not 17, a wrong back edge in the DFS, invalid
  O-notation constants in two places, a bubblesort trace, an SQL injection
  input that was a syntax error, a memory ratio, and smaller ones), `DB-14`
  relabeled and completed. Details in `REVIEW-2026.md`, "Fourth pass".
- Verified: 12/12 notebooks execute; generator, figure and pool-solution
  scripts run clean; 0 broken links or anchors; no em dashes, no `<details>`
  on sheets, no British spellings.

## 2026-10-18 — exercise sheets renamed

David: "under ICSS-local/ICSS_2026/TheoryExercises, rename all files instead
of TheoryExercises*.md to Exercise*.md"

- `TheoryExercises/TheoryExercisesNN.md` → `TheoryExercises/ExerciseNN.md`
  and `TheoryExercises/Solutions/TheoryExercisesNN-Solutions.md` →
  `TheoryExercises/Solutions/ExerciseNN-Solutions.md` (26 files).
- All links and mentions updated in the sheets, solutions, READMEs, pools,
  blueprint and `tools/gen09b.py`; `Exams/Solutions/` regenerated. Earlier
  entries of this log and of `REVIEW-2026.md` keep the old names as written.

## 2026-10-18 — slide layout, larger fonts, per-deck folders

David asked for the course title on one line, the new semester, fonts about
25% larger, one folder with its own figures per deck, "Session NN" footers,
slide numbers, updated session-1 slides (lab, team, calendar), all content
visible with stable schemas, full table borders, readable code, new
session-3 diagrams and probing slides, and Summary slides instead of "Next
Session". Done for all 13 lecture decks and 12 example decks; details in
`REVIEW-2026.md`, "Fifth pass". Session 3 gained slides 46 to 48 (references
renumbered); session 13 lost its last slide.
- Session 1, slide 12 ("Goals of the Course"): new schema of solving a problem
  computationally (problem → representation → algorithm → program →
  solution, with a check-and-refine loop and a running co-authorship
  example), drawn by the new `tools/gen01.py`. The lab and research-topics
  images were resized for the new, wider `AboutUS.svg`.

## 2026-10-30 — session 4 reworked as "Software"

Programming cut to ten slides (languages, interpreter and compiler,
paradigms, imperative basics, OOP with a string and a class of your own);
syntax, semantics, types and debugging removed; new sections on software
engineering, specifications and testing; new motivating examples on vibe
coding (Replit, Lovable, METR). Deck 34 slides, handout rewritten, all links,
references, posts, notebook and examples updated. Details in
`REVIEW-2026.md`, "Sixth pass". Open: exercise sheet 4 and the exam pool
have no specification or testing material yet.

## 2026-10-30 — session 4, second round

Deck now 40 slides: code aligned with the language levels, interpreter and
compiler diagrams, etymology box, class/object diagram, dictionary methods,
four incremental OOP-concept slides with diagram and code, a figure for
software engineering, the full flow diagram with "you and your client" /
"you" / "the LLM", the section "Requirements, specifications, and design"
(requirements, functional/non-functional, specification, two design slides),
and software verification. Motivating examples now Tea, Antigravity, Replit.
Handout, catalogue, notebook W04 (objects part out, vibe coding with a test
suite in) and exercise sheet 4 (four requirements-to-tests cases, no OOP or
debugging) rewritten. Details in `REVIEW-2026.md`, "Seventh pass".
- Session 3: new slide 15, "Doubly Linked Lists: advantages and disadvantages"
  (deletion in a doubly linked list, figure `03-doubly-linked-list-delete.svg`
  from `tools/gen03.py`). Later slide references shifted by one in
  `gensolutions.py` (exam solutions regenerated) and in the sheet 3 solutions;
  handout §3 extended to match.
- Session 3: slide 8 shows four data structures (array, linked list, BST, hash
  table; `03-data-structures.svg`) instead of three icons, now in
  `Slides/unused/03-DataStructures/`; slide 17 has the editing-vs-search
  figure `03-edit-vs-search.svg` in a right column. Both from `tools/gen03.py`.
- Numbers: thousands now written with commas (13,000), not spaces, in all
  session 3 and 4 materials (decks, handouts, sheets, solutions, example
  decks and posts, catalogue entries). Rule for every later revision.
- Session 3, second round (deck now 54 slides): keys and values on slides 8
  and 16; doubly linked list slides replaced by a blockchain slide (doubly
  linked lists moved to sheet 3, exercise 3, rewritten: search, delete,
  singly vs doubly); empty-cells figure on the array slide; binary search
  with p, q, r pointers (updates in orange), pseudocode the same size on all
  three slides; BST definition as two items; violations circled; hashing
  questions boxed; K -> m figure; operation rows explained; nine dates with
  collisions in both hashes; separate chaining as a fix for collisions;
  shorter linear probing with write and read (search 101, search 64); home
  exercise on deletion; Python: random probing only; own pseudonymization
  example without external link; outtake slide removed. Figures from
  `tools/gen03.py`; unused ones in `Slides/unused/03-DataStructures/`; slide
  references in gensolutions and the sheet 3 solutions updated.
- Session 3: motivating example M03-B (the helpline served newest-first)
  removed from deck and handout and parked for the sessions on stacks, queues
  and heaps: `PARKED` in `tools/motivation_data.py` and
  `MotivatingExamples-parked.md`. Deck now 53 slides; references updated.
- Session 3: slide "Dictionaries in Python" shows a drawn dict (`03-python-dict.svg`, from gen03.py) instead of the Stack Overflow image; the link stays.
- Session 3: slide "Dictionaries in Python" shows a drawn dict (`03-python-dict.svg`, from gen03.py) instead of the Stack Overflow image; the link stays.
- Session 3 handout updated to the current deck (binary search kept before BSTs as §5); third BST violation (15-11) circled in the figure.
- Sheet 3 solutions follow David's revised sheet (exercise 2 reordered, A1 without undo, old A5 removed, A6/A7 renumbered); BST figure relabeled; session 3 slide references updated in solutions and exam solutions.
