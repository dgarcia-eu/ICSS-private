# Review of the ICSS 2026 theory materials

Started 2026-09-11. Scope: the 13 lecture decks (`Slides/*.qmd`) and the 13
transcripts plus the conventions page (`Transcripts/*.md`). Everything found is
logged here, per session, so the review can be resumed and so David can see
exactly what changed and why.

Four things are checked for every session:

1. **Sources.** Every paper, book, chapter, page number, quotation, date and
   website is checked against the original (the PDFs in
   `ICSS_2022/ReadingMaterials` for the course books, the web for the rest).
2. **Equations and notation.** Every formula is re-derived; notation is made
   consistent within the session and with `Transcripts/00-Conventions.md`,
   which is the course-wide standard (updated below where a decision changed).
3. **Algorithms.** Every piece of pseudocode is checked against its source
   (Cormen, *Algorithms Unlocked*; CLRS; Sipser) and traced by hand or by running it.
4. **Prose.** Transcripts rewritten in David's style: article-style paragraphs,
   no em dashes, American spelling, no rhetorical flourishes.

## Style rules used for the rewrite

Derived from David's own texts: the 2022 transcripts
(`ICSS_2022/Github-handouts/*/*.Rmd`), the syllabus, and the slide text.

- Paragraphs of four to eight sentences that develop one idea, as in a book
  chapter or a paper. Bullet lists only for genuinely enumerable things (steps
  of an algorithm, properties, a list of readings). No one-sentence paragraphs.
- No em dashes anywhere. Commas, parentheses, colons, or a new sentence
  instead. En dashes stay only inside numeric ranges (1815–1852, pp. 33–34).
- American spelling (analyze, behavior, color, optimize), matching the slides
  and David's writing. Exception: proper names and quotations.
- "We" for the course and the lecturer, "you" for the student; "for example"
  rather than "e.g." in running text; "we will see in session 8" rather than
  cross-reference arrows.
- Terms being defined in *italics* at first use; **bold** reserved for the few
  things a student must remember. No bold-led one-line paragraphs.
- No rhetorical flourishes or aphorisms ("that is a feature, not
  sloppiness"); explain instead.
- Structure of each transcript is kept: header, contents, numbered sections
  following the slides, worked examples, "check yourself" with answers,
  references. Section headings are kept verbatim wherever possible, because
  the example posts in `Examples/posts` link to them by anchor.
- Motivating-example blocks (`<!-- MOTIVATION … -->`) are generated from
  `tools/motivation_data.py`; they are rewritten there and re-inserted with
  `tools/genmotivation.py`, not edited in the transcripts.

## Course-wide notation decisions

Consolidated into `Transcripts/00-Conventions.md`, rewritten on 2026-09-11 so
that it states exactly what the decks and transcripts now do.

- **Pseudocode** follows Cormen, *Algorithms Unlocked*, adapted: a header
  `Procedure NAME(args)` with `Inputs:`, `Data:` (only when needed) and
  `Result:`; procedure names in capitals with hyphens (SELECTION-SORT,
  BINARY-SEARCH, DFS-VISIT, INITIALIZE-BFS); blocks by indentation only, no
  line numbers, no `begin`/`end`, no trailing punctuation; `x ← y` for
  assignment and `=` for comparison; `For i = 1 to n:`, `While cond:`,
  `If cond` / `then …` / `else …` on indented lines; `return`; `swap A[i] with
  A[j]`; `a mod b`; `⌊ ⌋`; comments after `#`. Queue and stack operations are
  ENQUEUE/DEQUEUE and PUSH/POP. Every numbered or `repeat … until` procedure
  in the 2025 material (deck 5 K-smallest, deck 6 factorial/GCD/FIB, deck 7
  MERGE, deck 8 insertion sort, deck 9 halting proof, deck 13 Schelling, the
  motivating examples) was rewritten in this format.
- **Indices** are 1-based in pseudocode and mathematics and 0-based in Python;
  wherever a transcript shows both versions it says so. Deck 8 insertion sort
  is `For i = 2 to n` with `While j > 0 and A[j] > key` (Cormen), on all four
  copies.
- **Graph search** uses `color[u]` (WHITE/GRAY/BLACK), `d[u]`, `π[u]`, `f[u]`
  and NIL, with alphabetical tie-breaking; BFS is INITIALIZE-BFS + BFS
  (session 5), DFS is DFS + DFS-VISIT (session 6), both as in Cormen.
- **Sorting**: a sorted sequence satisfies `s(u_{i_k}) ≤ s(u_{i_{k+1}})`
  (non-decreasing); MERGE uses the ∞ sentinels `B[n1+1] ← ∞`, `C[n2+1] ← ∞`.
- **Complexity**: the input size is `n` everywhere (deck 8 mixed `N` and
  `n`); `log` inside `O(·)` has no base; the class ordering is written with
  `⊂`: `O(1) ⊂ O(log n) ⊂ O(n) ⊂ O(n log n) ⊂ O(n²) ⊂ O(2ⁿ) ⊂ O(n!)`.
- **Number systems**: the base is a subscript (`100111₂`); digit `x_k` has
  weight `β^k` and `x_{-k}` sits after the point; the conversion procedures
  are DECIMAL-TO-BINARY(n), DECIMAL-TO-BASE(n, β) and FRACTION-TO-BINARY(n);
  the IEEE 754 sign factor is `(−1)^S`.
- **Hash tables**: key `k`, hash `h(k)`, `m` slots, key universe `K` with
  `|K| ≫ m`.
- **Automata and machines**: a DFA is the 5-tuple `(Q, Σ, δ, q₀, X)` with
  accept states `X` (deck and transcript 9 mixed `F` and `X`); an NFA maps into
  the power set `P(Q)`; `ε` is the empty word and appears in the Kleene star;
  a grammar is `(N, Σ, P, S)` with `N` the non-terminals; a Turing machine is
  the 7-tuple `(Q, Σ, Γ, δ, q₀, □, F)`.
- **Machine learning**: features `X`, target `Y`, prediction `ŷ = f(x)`, `n`
  examples, `d` features, `K` clusters (K-means with `C(i)`, `N_k`, `m_k`),
  `k` neighbors in kNN; `TP`, `FP`, `FN` and `F₁` written with a subscript.
- **Spelling and punctuation**: American spelling throughout decks,
  transcripts, conventions page and motivating examples; "Modelling" survives
  only inside the proper name *Computational Modelling of Social Systems*. No
  em dashes anywhere in `Slides/*.qmd`, `Transcripts/*.md`,
  `MotivatingExamples.md` or the generator that writes them.

## Status

| # | Deck checked | Deck fixed + rebuilt | Transcript checked | Transcript rewritten | Knitted |
|---|---|---|---|---|---|
| 00 Conventions | – | – | ✓ | ✓ | ✓ |
| 01 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 02 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 03 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 04 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 05 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 06 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 07 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 08 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 09 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 10 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 11 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 12 | ✓ | ✓ | ✓ | ✓ | ✓ |
| 13 | ✓ | ✓ | ✓ | ✓ | ✓ |

"Knitted" means the transcript was re-rendered to HTML with
`tools/knitexamples.py` and the link check passed. Deck 13 was rebuilt only
for the spelling change in its slide titles ("Modeling").

## Findings and changes, per session

### Session 1: Introduction

Deck (`ICSS-2026-01-Introduction.qmd`), corrected and rebuilt (42 pages, no overflow):

- "Colossus Mark 2 computer cracks Enigma code" was wrong: Colossus broke the
  Lorenz (Tunny) cipher; Enigma was broken with the bombes. Fixed.
- Timeline: the Analytical Engine dates from 1837 (the 1820s machine was the
  Difference Engine) and Lovelace's notes from 1843; the IBM PC was delivered in
  1981, not 1980; "Gary" Kasparov is Garry Kasparov; "message send" → "sent".
- Literature slide had Evans and Guttag swapped: Guttag's book uses Python;
  Evans' book is mostly in Scheme (a LISP dialect). Fixed.
- Zelle's definition of a computer is cited as (Zelle, 2016), the edition on
  the syllabus, instead of 2004. Wording verified against Zelle 2016, ch. 1 and
  glossary ("a machine that stores and manipulates information under the
  control of a changeable program").
- Left for the year rollover: tutor names/e-mails do not match, exercise room
  K505 (deck) vs K503 (syllabus).

Transcript (`01-Introduction.md`), rewritten:

- Dijkstra quotation note corrected: Quote Investigator finds the earliest
  printed instance as an anonymous saying in George Johnson, *Machinery of the
  Mind* (1986), a claim for Alan Perlis (1968, unpublished), and no evidence for
  Dijkstra. The old note ("computing folklore of the 1970s") was unsupported.
- Selection sort pseudocode page reference corrected to Cormen 2013, pp. 32–34
  (verified in the PDF; the old "33–34" missed the procedure itself).
- Timeline dates aligned with the deck (1837/1843/1981); Simon's Nobel (1978)
  and Turing Award (1975) years added.
- Cross-references verified: Euclid's algorithm is in deck 06, von Neumann
  architecture in deck 04, finiteness/definiteness in deck 05, universal
  Turing machines in deck 09.
- Worked trace and check-yourself answers re-traced by hand (3 comparisons,
  2 swaps for [3, 1, 2]).

### Session 2: Information Coding

Deck (`ICSS-2026-02-InformationCoding.qmd`), corrected and rebuilt (57 = 54 + 3
pages, no overflow):

- Three conversion procedures had an off-by-one in the returned digits: they
  returned `x_k … x_0` after incrementing `k` past the last digit, so `x_k` was
  never assigned; the fraction procedure counted `k` downwards and returned
  `x_-k` with the wrong sign. Rewritten as `DECIMAL-TO-BINARY(n)`,
  `DECIMAL-TO-BASE(n, β)` (β is now an explicit input) and
  `FRACTION-TO-BINARY(n)`, returning `x_(k-1) … x_0` and `0.x_-1 … x_-(k-1)`.
  Names follow the course convention (UPPER-CASE-WITH-HYPHENS, **Procedure**
  in bold) like SELECTION-SORT; the old CamelCase names were used nowhere else.
- IEEE 754 sign written as `s = -1^S` (which is always −1); now `(-1)^S`.
- "Underflow example" label on the 0.1 accumulation renamed "Rounding error
  example" (underflow is a different phenomenon). Output verified by running
  the code.
- UTF-8 "up to three UTF-8 characters" → "a sequence of up to four bytes".
- Unicode 1.0 "65 536 different characters" → "a 16-bit code space (65 536 code
  points)"; version 1.0 encoded about 7 000 characters.
- Python encoding example updated to Python 3 output (`b'…'` prefixes,
  `'ꀀ'` in the error message); verified by running it.
- "Python Primitive Data Types" table is the C/Java type table; slide retitled
  "Primitive Data Types" with a note on what Python actually has. Maximum of
  `char` corrected to 1 114 111 (U+10FFFF); 1 114 112 is the number of code
  points.
- Operators: "rest of the integer division" → "remainder"; `^` example written
  with `^`; `~1 = 0` (false in Python, where `~1 == -2`) replaced by "flips every
  bit; `~x = -x - 1`". Division table header "Rest" → "Remainder".
- COBOL "developed in the 1960s" → "designed in 1959".
- Sources verified: Skeel, *SIAM News* 25(4), July 1992, p. 11 (quotation on
  the slide is verbatim); Weber-Wulff, RISKS 13.37 (4.97% displayed as 5%,
  5 April 1992, SPD one-seat majority after recount); Ziemann, Eren & El-Osta,
  *Genome Biology* 17 (2016), "approximately one-fifth" of papers; Bruford et
  al. (2020) 27 genes renamed; McCullough & Vinod, *JEL* 37(2), 633–665; ESA
  press release 33-1996.
- All numeric examples re-computed (base conversions, complements, overflow,
  18.625 and −1 703 936 IEEE examples, Llama memory table).

Transcript (`02-InformationCoding.md`), rewritten (motivation block untouched):

- Linear question tree now described as the figure draws it (2? 3? 4? 5? 6?,
  with 1 as the last "no"), not the reverse order.
- Entropy statement corrected: the entropy is the minimum average number of
  questions, reached exactly only when all probabilities are powers of two;
  the old text said the average of the tree "is exactly" the entropy.
- Vancouver index: the old text said it drifted "from 1098 to 524"; it started
  at 1000.000, was displayed as 524.811, and was 1098.892 once recomputed.
- Schleswig-Holstein consequence stated precisely (Greens shown above the
  threshold; after the recount the SPD gained one seat and a one-seat majority).
- Pseudocode aligned with the corrected deck; Python 3 outputs; `char` maximum;
  `~` semantics; 0.1 binary expansion written out (0.0001100110011…).
- Grace Hopper: "co-designed COBOL" → wrote the first compiler (1952) and
  designed FLOW-MATIC, the model for COBOL; technical adviser to the committee.
- Cross-reference to session 6 (call stack; the heap is in deck 04) corrected.

### Session 3: Data Structures

Deck (`ICSS-2026-03-DataStructures.qmd`), corrected and rebuilt (52 = 49 + 3
pages, no overflow):

- BINARY-SEARCH pseudocode (three slides) put in the course format: bold
  **Procedure**, UPPER-CASE name, `While p ≤ r:` without "do", `If`/`then`/`else`
  as in the conventions page, and a Result line that says what is returned.
  Variables p, q, r and the structure are Cormen's (2013, pp. 28–30, verified).
- Hash function requirement "$|K| = n \gg m$" mixed up $n$ (the number of stored
  entries, used later on the same slides) with the size of the key space; now
  "$|K| \gg m$".
- "Lookup … much faster than an `in` operation on `keys()`" is false in Python 3
  (`key in d.keys()` is hashed and just as fast; verified by timing). Replaced
  by the true contrast, `key in d` versus `key in list(d)`.
- Regular expressions are taught in session 9, not 8 (AWK slide).
- All arithmetic re-checked: mod 97 / mod 100 table, chaining example
  (50, 700, 76, 85, 92, 73, 101 mod 7), binary search trace, 2 × 10¹² pairs.

Transcript (`03-DataStructures.md`), rewritten (motivation block untouched):

- The explanation of the "is this a BST?" slide was wrong: it said the 11 under
  15 "is fine". From the figure (root 10; 4: 2, 9; 13: 15, 21; 2: 5, 3; 15: 11)
  there are three violations: 15 as left child of 13, 5 as left child of 2,
  and 11 as right child of 15 (also inside the right subtree of 13). Fixed.
- `key in d.keys()` claim corrected as above; cross-reference to session 9 for
  regular expressions; Cormen page numbers added.
- Deletion of a two-child node: added why the moved successor has at most one
  child (the leftmost node of a subtree has no left child).

### Session 4: Programming

Deck (`ICSS-2026-04-Programming.qmd`), corrected and rebuilt (71 = 68 + 3
pages, no overflow):

- "Careful planning of flow with flow charts (session 6)": flowcharts are in
  deck 05. Fixed.
- Employee example: `print("Name: ", self.name, ", Salary: ", self.salary)`
  prints `Name:  Zara , Salary:  2000` (extra spaces), not the output shown on
  the slide; the method now uses an f-string that produces exactly the shown
  output. Bare string statements used as comments turned into comments. List
  outputs written as Python prints them (`['a', 'b']`).
- "Abstraction" was defined as data hiding (attributes only via methods);
  reworded to the standard meaning (expose what, hide how) while keeping the
  original point.
- Sources verified: Reinhart & Rogoff (AER 2010) −0.1% / Herndon, Ash & Pollin
  (CJE 2014) +2.2%, five countries dropped from 20; Baker (Nature 533, 2016)
  1 576 researchers, >70% / >50%; the `isPal`/`silly` example is Guttag 2016,
  chapter 6 (verified in the PDF); Brainfuck and LOLCODE snippets are the
  standard "Hello World" programs.

Transcript (`04-Programming.md`), rewritten (motivation block untouched):

- False claim removed: "in Python, a syntax error in line 400 will not stop
  lines 1–399 from running". Python parses the whole file first; a syntax
  error stops everything. The true statement is about run-time errors.
- Flowcharts cross-reference (session 5), f-string example output, Guttag
  chapter citation, exercise sheet 4 pointer for inheritance (verified).

### Session 5: Algorithms

Deck (`ICSS-2026-05-Algorithms.qmd`), corrected and rebuilt (52 = 49 + 3
pages, no overflow):

- K-SMALLEST-ELEMENT pseudocode used 0-based indices (`For i = 0 to k-1`,
  `return M[k-1]`) against the course convention; now 1-based (`For i = 1 to
  k`, `return M[k]`), with the input `k` described as "which smallest element
  to find" instead of "the index … given the list is sorted".
- Pseudocode template (`begin … while … do … ;`) and the `input/data/output`
  spec blocks put in the course format (**Procedure** NAME, Inputs/Data/Result,
  indentation, no `begin`/semicolons).
- BFS: `InitialiseBFS`/`Enqueue (Q, s)`/`if` replaced on all 11 pseudocode
  slides by INITIALIZE-BFS, ENQUEUE/DEQUEUE, `If`, `color[u]` (no space);
  queue and stack operations written ENQUEUE, DEQUEUE, PUSH, POP as in CLRS.
- "heaps (= binary trees)" on the abstract data structures slide: heaps were
  not covered (session 7) and are not the same as binary trees; now "binary
  search trees".
- "partial correctness: every step … has to be correct" replaced by the
  standard definition (whenever the algorithm terminates, its output is
  correct); "unordered tuple" → "unordered pairs".
- Verified: adjacency matrix and list agree with each other and are symmetric;
  BFS trace from c re-run by hand (b, f, g at 1; e, d at 2; a at 3); Facebook
  455 PB = (2.7·10⁹)²/2 bits (upper half of the symmetric matrix); Milgram
  1967 (296 chains, 64 arrived, mean 5.2) and Edunov et al. 2016 (3.57).

Transcript (`05-Algorithms.md`), rewritten (motivation block untouched):

- Pseudocode aligned with the deck; the 455 PB figure explained (half matrix);
  "Dijkstra or Bellman-Ford, see exercise sheet 5" corrected to Bellman-Ford,
  which is what the sheet contains.
- Alphabetical-order convention for neighbors stated in the BFS trace.

### Session 6: Recursion

Deck (`ICSS-2026-06-Recursion.qmd`), corrected and rebuilt (88 = 85 + 3
pages, no overflow):

- Iterative Fibonacci had an off-by-one: `for i from 2 to n+1` (a Python
  `range` habit) computes one element past `memo[n]`. Now `For i = 2 to n`.
- Pseudocode put in the course format on 26 slides: ITERATIVE-FACTORIAL,
  RECURSIVE-FACTORIAL, GCD (returns directly, `a mod b` instead of
  `mod(a,b)`, no trailing comma), DFS / DFS-VISIT (assignments with ← instead
  of `=`, `If`, `color[u]`, `time` initialized with ←, Result lines that say
  what is computed), FIB in three versions (Procedure/Inputs/Data/Result
  header instead of "Algorithm for … Input/Output").
- DFS example text said "starting vertex u = c" while DFS(G) loops over G.V;
  now "the For loop takes vertex c first; among neighbors, go alphabetically",
  which is what the trace does.
- "Greedy … e.g. BFS": BFS is not a greedy optimization; example replaced by
  building a Huffman code (the prefix-code construction of session 2's
  exercises).
- Verified: DFS trace against the generated figures (a 4/5, b 2/9, c 1/14,
  d 11/12, e 3/8, f 6/7, g 10/13, edges c→b, c→f, c→g, b→e, e→a, e→f, g→d);
  gcd(270, 192) trace; Euclid, Elements VII.1–2; Ackermann 1928, Math. Ann.
  99; ack(4,3) has 19 729 digits.

Transcript (`06-Recursion.md`), rewritten (motivation block untouched):

- Reference "Cormen (2013), ch. 10" was wrong (ch. 10 of *Algorithms Unlocked*
  is NP-completeness); recursion is discussed in ch. 2, pp. 21–23 (verified).
- Pseudocode aligned with the deck; the halving argument for Euclid stated
  correctly (a mod b < a/2, so the larger argument at least halves every two
  calls).

### Session 7: Sorting Algorithms

Deck (`ICSS-2026-07-SortingAlgorithms.qmd`), corrected and rebuilt (81 = 78 + 3
pages, no overflow):

- MERGE pseudocode was wrong: it copied the two halves into B and C and looped
  `For k = p to r` comparing `B[i] ≤ C[j]` with no sentinels, so once one half
  is exhausted it reads past the end of the array. Cormen's version (verified,
  *Algorithms Unlocked* p. 46) appends ∞ to both copies; the slide now does the
  same. The transcript carried the same bug and is fixed.
- Sorting definition: `s(u_i) ≤ s(u_{i+1})` did not use the permutation it
  quantifies over; now `s(u_{i_k}) ≤ s(u_{i_{k+1}})` for 1 ≤ k ≤ n−1.
- Page references corrected against the PDF: selection sort pp. 32–34 (was
  33–34), merge sort pp. 40–47 (was 42–43), heapsort pp. 98–99 (was 98).
- SELECTION-SORT (2 slides, and the 2 copies in deck 01), MERGE-SORT,
  QUICK-SORT and I-CANT-BELIEVE-IT-CAN-SORT put in the course pseudocode
  format (bold Procedure, no trailing commas/periods, `swap … with …`,
  `then/else` indented under `If`, recursive calls written as calls).
- Verified: merge example B = [2,3,4,6], C = [1,5,7,8]; heapsort start
  [2,4,14,10,8,15,18,17,11,16] and the array layout figure; heap example
  (8 under 4); Fung 2021 arXiv:2110.01111; von Neumann 1945 mergesort and the
  1955 climate warning; break-even q ≈ 25 lookups (76 000 + 13q < 3 000q).

Transcript (`07-SortingAlgorithms.md`), rewritten (motivation block untouched):

- Reference "Cormen 2013, ch. 2 (selection, insertion, merge sort) and ch. 3
  (quicksort)" was wrong: all four sorts are in ch. 3, and ch. 4 has the lower
  bound and counting sort. Fixed with page numbers.
- Check-yourself 5 said "factor n / log₂ n = 50 000" while quoting 5·10¹¹ vs
  2·10⁷; the factor is n / (2 log₂ n) = 25 000. Fixed.
- Motivation block B ("eleven days") and A (mentions insertion/counting sort
  and wrong section numbers) are noted for the `motivation_data.py` pass:
  5·10¹¹ comparisons at 10⁷/s is about 14 hours, not 11 days.

### Session 8: Time Complexity

Deck (`ICSS-2026-08-TimeComplexity.qmd`), corrected and rebuilt (54 = 51 + 3
pages, no overflow):

- Running-time tables (two slides): the mergesort row for the home computer
  said "1 sec" for a million and "18 min" for a billion, which does not
  follow from n log₂ n at 10⁸ operations/s (2·10⁷ ops = 0.2 s; 3·10¹⁰ ops =
  300 s = 5 min). The selection-sort rows were consistent (10¹² ops = 2.8 h,
  10¹⁸ ops = 317 years, 10⁶ s = 1.65 weeks). Fixed to 0.2 sec / 5 min.
- Insertion sort was 0-based on the first slide (`For i = 1 to n-1`,
  `While j ≥ 0`) and `For i = 1 to n` on the next three, both against the
  1-based convention and against Cormen's version; now `For i = 2 to n`,
  `While j > 0 and A[j] > key` on all four slides, worst-case count written
  with n−1 outer iterations.
- "we have to search n times for the minimum" → n−1 times (matches the sum).
- Two slide titles read "0-Notation" with a digit zero; now "O-Notation".
- Mergesort recurrence and the "common use" slide used N while the rest of the
  deck uses n; unified to n (the conventions allow both, but not mixed).
- Manuel Blum: "CS prof at UC Berkeley" → Berkeley and, since 2001, Carnegie
  Mellon (the cited MIT Technology Review article is about his CMU years).
- SELECTION-SORT, MERGE-SORT and the four BFS blocks put in the course format.
- Verified: 5n² − 4n − 1 expansion; T(n) unrolling; |V| + 2|E| for BFS on
  adjacency lists; Knuth 1976 SIGACT News 8(2); Blum's Turing citation and
  three Turing-Award students.

Transcript (`08-TimeComplexity.md`), rewritten (motivation block untouched):

- Same table, insertion sort and Blum fixes; check-yourself 5 replaced by a
  clean proof (c = 1, n₀ = 101, with the monotonicity argument) instead of
  the muddled two-attempt one.

### Session 9: Theoretical Computer Science

Deck (`ICSS-2026-09-TheoreticalCS.qmd`), corrected and rebuilt (82 = 79 + 3
pages, no overflow):

- Grammar derivation table: the first step "(1) Expr" was wrong (S is Expr,
  and rule 1 is Expr → Term), and the rows "(1) a*(Term + Fact)+a" and
  "(3) a*(Fact + a)+a" each apply two rules. Relabeled (1)(3) and (3)(5);
  every row re-derived.
- Grammar-to-automaton mapping: X was used for the set of accept states in
  the DFA definition and for a single new state here, and the accept set was
  written "E = {X}". Now the automaton is (Q, Σ, δ, q₀, {X}) with the clash
  noted; the mapping is stated for regular grammars (rules A → aB, A → a),
  which is the only case where it holds. "Q = {S, A, B}" → N = {S, A, B} on
  two slides (those are the variables, not automaton states).
- NFA definition: "𝒫(Q) is a set of states" → the power set of Q; "Σ can
  contain ε" → ε-transitions (ε is not an alphabet symbol).
- Kleene star example now includes ε (the next bullet defines V⁺ as V* without
  ε, so ε must be in V*).
- TM transition example omitted that the machine writes b; added.
- Chomsky table: "Recursively enumerated" → recursively enumerable; type 3
  class named "Regular language" (it said "Regular expression").
- Accept-state wording: "terminal state" → "accept state" (as in the
  definition); "make the automaton stop" → "the automaton accepts";
  "(#a − #b) = 3 mod 4" → ≡ 3 (mod 4).
- Church-Turing thesis "has no formal proof or empirical evidence" → no formal
  proof; supported by the equivalence of all proposed models.
- Sokoban is PSPACE-complete (Culberson 1997), not Turing complete; stated as
  such. Turing's death and the Bombe (electromechanical, not a computer)
  reworded to what the sources support.
- Verified: DFA example ((#a − #b) ≡ 3 mod 4 on all six sample words and both
  traces); L(G) = (abb)ⁿ; both SAT examples by hand; 40³⁰⁰ has 481 digits;
  Turing 1936 Proc. LMS s2-42; Rabin & Scott 1959; Chomsky 1956; Cook 1971;
  Churchill et al. arXiv:1904.09828; Culberson TR 97-02; Cloudflare outage
  2 July 2019, 27 minutes.
- Cross-course: deck 08 ordered the O-classes with "<" while deck 09 and the
  conventions page use ⊂; deck 08 and its transcript now use ⊂.

Transcript (`09-TheoreticalCS.md`), rewritten (motivation block untouched):

- Same corrections; the garbled sentence introducing the tape trace removed;
  Cook 1971 venue spelled out.

### Session 10: Machine Learning

Deck (`ICSS-2026-10-MachineLearning.qmd`), corrected and rebuilt (45 = 42 + 3
pages, no overflow):

- History slide placed "The Perceptron Problem: AI Winter" in the
  1990s–2000s. The perceptron limits (Minsky & Papert, 1969) caused the first
  AI winter in the 1970s; the 1980s were expert systems plus the return of
  neural networks; the second winter followed in the 1990s. Timeline rewritten
  in six lines.
- Verified: TF-IDF formulas; error/loss table (2/5, 60%); class-imbalance
  arithmetic; precision/recall/F₁; kNN formula and figure sources (Hastie et
  al. §2.3, figures 2.2–2.4, test set 10 000); Naive Bayes derivation;
  K-means objective (Hastie et al. eq. 14.33, with the N_k weights) versus the
  unweighted WSS of the elbow plot; Hinton's 2018 Turing Award (with Bengio
  and LeCun) and 2024 Nobel Prize in Physics; Ginsberg et al. Nature 2009 and
  Lazer et al. Science 2014; Buolamwini & Gebru PMLR 81; Kosinski et al. PNAS
  110(15); Belkin et al. PNAS 116(32); Boué arXiv:1904.12320.

Transcript (`10-MachineLearning.md`), rewritten (motivation block untouched):

- History aligned with the corrected timeline.
- K-means: the transcript used m_k in the objective and μ_k in the WSS and
  did not say that the two sums differ by the cluster-size weights; now one
  notation (C(i), N_k, m_k) and the difference stated.
- kNN: the decision rule (class 1 if the average is above one half) made
  explicit; F₁ written consistently as $F_1$.

### Session 11: Databases

Deck (`ICSS-2026-11-Databases.qmd`), corrected and rebuilt (56 = 53 + 3
pages, no overflow):

- Three queries filtered on `Manufacturer = 'Gizmo Works'` while the table
  holds `GizmoWorks`; as written they return nothing. Fixed on the selection,
  projection and aggregation slides. `Pname` → `PName` in the schema (the
  table header spells it `PName`).
- `SELECT AVG(Price) FROM Product GROUP BY Manufacturer` shows a Manufacturer
  column in its result that the query does not select; now `SELECT
  Manufacturer, AVG(Price) …`.
- INNER JOIN result kept the column name `Nr` although the previous slide
  renamed the key of `purchase` to `ID`; fixed.
- Verified: the relational tables reproduce the flat table row by row; the
  query `Product = Tea and Birth < 1999` (Hans and Pat, not Fred); AVG
  19.99/29.99 = 24.99; 8 × 2 = 16 for the Cartesian product; PHE case (15 841
  results, 25 Sep–2 Oct 2020, .xls 65 536 rows); ACID from Härder & Reuter
  1983; Codd 1970 CACM 13(6).

Transcript (`11-Databases.md`), rewritten (motivation block untouched):

- Header cited a non-existent "Ledgard & Marcotty / course reading material,
  chapter 4"; the syllabus reading is chapter 4, "Databases" (Ian Foster and
  Pascal Heus), of Foster et al. (eds.), *Big Data and Social Science*, CRC
  Press 2017 (verified in the PDF). Added to the references.
- The manual-join example uses a `purchase` table whose rows 5–8 refer to
  products 3 and 4 (unlike the earlier table); the transcript now says so,
  and notes that `SELECT *` also returns `Product.Nr`.
- Same query and column-name fixes as the deck.

### Session 12: Parallel Programming

Deck (`ICSS-2026-12-ParallelProgramming.qmd`), corrected and rebuilt (52 = 49 + 3
pages, no overflow):

- "EX: execute – perform calculation based on registry information" (four
  slides): registers, not registry.
- "GPUs have large memories and high clock speeds": GPU clocks are lower than
  CPU clocks; what is high is the memory bandwidth. Fixed. "Cannot do any
  operation efficiently" → "cannot do every operation efficiently".
- Spectre/Meltdown: private data is read from the processor cache left by
  speculatively executed instructions, not "from the registers of speculated
  execution".
- Verified: Amdahl arithmetic in the motivation (P ≈ 0.64 from 2.5× on 16
  cores; 2.70× on 64; ceiling 2.8×) and in the P = 0.8 table; brain/Blue
  Gene table (36× throughput at 1.2 MW); Flynn 1972; Amdahl 1967 AFIPS 30;
  Gustafson 1988 CACM 31(5); Dean & Ghemawat 2008 CACM 51(1); Zaharia et al.
  2016 CACM 59(11); Jordan, Lee & Yang 2019 JASA 114(526); Moore 1965.

Transcript (`12-ParallelProgramming.md`), rewritten (motivation block untouched):

- "Per operation per watt, biology wins by five orders of magnitude": from
  the table it is 5·10¹¹ vs 3·10⁸ operations per joule, a factor of about
  1 700, i.e. three orders of magnitude. Fixed.
- Reading line added (syllabus): DeNero, *Composing Programs* §4.8, and Vo &
  Silva, "Programming with Big Data", ch. 5 of Foster et al. (verified in
  the PDF: ch. 5, p. 125).
- The Map phase of the correlation example now returns the sample size plus
  five sums (six numbers, as the motivation says), and the variance formula
  is written as E[(θ̂ − E[θ̂])²].

### Session 13: Social Science Applications

Deck (`ICSS-2026-13-SocialScienceApplications.qmd`): checked, no change
needed (no em dashes; all sources verified: Lazer et al. 2009 Science
323(5915); Salganik 2017; Earle, Bowden & Guy, Annals of Geophysics 54(6),
708–715, doi 10.4401/ag-5364; Preis, Moat & Stanley 2013 Sci. Rep. 3, 1684;
Garcia et al. 2018 PNAS 115(27); Lazer et al. 2021 Nature 595; Pew 2021 table
values; Hutto & Gilbert 2014 ICWSM; Youyou et al. 2015 PNAS 112(4); Kosinski
et al. 2013; Garcia et al. 2018 EPJ Data Science 7:3; Schelling 1971 JMS
1(2); Lasser, Hell & Garcia 2022 CID 75(1)).

Transcript (`13-SocialScienceApplications.md`), rewritten:

- "Garcia et al., Social media emotion macroscopes …" had no year or venue;
  it is Garcia, Pellert, Lasser & Metzler (2021), arXiv:2107.13236.
- Earle et al. pages and DOI added; Hutto & Gilbert venue spelled out.
- The SCHELLING pseudocode used numbered lines and `repeat … until`; rewritten
  in the course format (`While moved:` with a flag).
- "Modelling" kept only in the proper names of courses; "modeling" elsewhere.

### Motivating examples (`tools/motivation_data.py`)

All 33 candidates (sessions 2–12, three each) rewritten in the same style as
the transcripts and regenerated with `tools/genmotivation.py`; decks 02–12
rebuilt with their previous page counts (57, 52, 71, 52, 88, 81, 54, 82, 45,
56, 52) and no overflow.

- Every "Where this session picks it up" paragraph pointed at section numbers
  that did not match the transcripts (for example hash tables were cited as
  section 3 of session 3 when they are section 8; stacks and queues were
  attributed to session 3 although they are defined in session 5; sessions 4
  to 9 had similar slips). All section references now match the numbered
  headings of the transcripts.
- M07-B: the second figure said "14 hours" for 10¹² comparisons, which is not
  what 10⁷ comparisons per second gives (10⁵ s ≈ 28 h) nor what 10⁸ gives
  (10⁴ s ≈ 2.8 h); the example is now stated at 10⁷ comparisons per second with
  the numbers that follow from it.
- M07-A: which sorting algorithms are stable now matches the transcript
  (selection sort and heapsort unstable, mergesort stable, quicksort as
  usually implemented unstable).
- M09-A: the title no longer claims "5% of the web"; Cloudflare's own report
  gives no such figure. Cloudflare, 2 July 2019, 27 minutes, verified.
- M10-A: "140% of the real rate" was a misreading of Lazer et al. (2014), who
  report that Google Flu Trends predicted more than double the CDC figure in
  the 2012–13 season; slide and text now say "more than double".
- M12-B: the Amdahl arithmetic was re-derived (P ≈ 0.64 from 2.5× on 16
  cores gives 2.70× on 64 cores and a ceiling of 2.8×); M12-C: the six
  sufficient statistics and the correlation formula re-checked.
- The pseudocode inside the examples (HEADCOUNT-BELOW, THREAD-DEPTH, the
  nested-loop and hash-set versions of the filter, TROUBLE, the seat-booking
  race) is in the course format; numbered lines and `repeat … until` removed.
- Pitches, slide bodies and `.ask` lines no longer contain " -- " or em
  dashes; `genmotivation.py` no longer converts " -- " into an em dash and its
  selector header, session headings and item lines use colons instead.
- Slides that carry three big numbers (`.fq` blocks) were left at three
  figures each so that the slide layout is unchanged.

## Final checks (2026-09-11)

- Em dashes: none in `Slides/*.qmd`, `Transcripts/*.md`,
  `MotivatingExamples.md`, `tools/motivation_data.py` or `tools/genmotivation.py`
  (`grep -c '—'`).
- British spellings: none in the decks or transcripts except the proper
  name *Computational Modelling of Social Systems*; "Agent-Based Modeling",
  "Modeling computation through automata" and "Unified Modeling Language"
  corrected in decks 13, 9 and 5 and the three decks rebuilt (41, 82, 52
  pages).
- All 13 decks rebuilt at least once after their last edit: 42, 57, 52, 71,
  52, 88, 81, 54, 82, 45, 56, 52, 41 pages, overflow none; the `.pdf` next to
  each `.qmd` refreshed from the same build.
- `tools/knitexamples.py`: 49 posts, index, 14 transcripts, 36 notebooks;
  link and anchor check over the 100 HTML files: 1 082 relative links, 0
  broken (the four Examples posts that linked to the renamed anchors
  `#8-asymptotic-behavior-and-o-notation` and `#13-agent-based-modeling`
  were updated).
- Not verified: the "wounding 260" casualty figure for the 1991 Dhahran
  Patriot failure on deck 2 (the Wikipedia page used as the source no longer
  resolves; the GAO report gives 28 killed and does not state a wounded count
  that could be matched to the slide). Left unchanged and flagged.
- Out of scope for this pass and still in the old style: the Examples decks
  and posts (`Examples/`), the exercise sheets, the exam pool and the history
  posts; they contain 593 em dashes and British spellings (49 of 49 posts).

## Second pass (2026-09-11): example decks, posts and notebooks

Scope: the 12 question-and-answer decks (`Slides/Examples/*.qmd`, generated
from `tools/examples_data_a.py` and `_b.py` by `tools/genexamples.py`), the 36
example posts and 13 history posts (`Examples/posts/*.md`), the 36 notebooks
(`Examples/notebooks/*.ipynb`, generated and executed from `tools/exnb_a.py`
and `_b.py` by `tools/genexnotebooks.py`), `Examples/README.md`, the figure
placement (`tools/figposts.py`) and two example figures. The same four checks
as in the first pass: sources, equations and numbers, algorithms and code,
prose in the course style with no em dashes and American spelling.

Method: the generated decks and notebooks were first compared with their
generators (identical, so the data files are the only source of truth); every
example was then read in its three forms side by side, its claims checked
against the source named in its notes slide, its section references checked
against the transcript headings, its notebook outputs read, and all three
forms rewritten together. Section references and exam-item ids were verified
by grep against `Transcripts/` and `Exams/`.

### Corrections of fact

- **X02-A** (Year 2038). "A 32-bit counter of milliseconds after 49 days (an
  actual bug in Boeing 787 generators, 2015)": the 787 counter overflowed
  after 248 days (FAA AD 2015-09-07); the 49.7-day case is Windows 95/98.
  "Pension systems, 2018" is not a documented incident; replaced by AOLserver
  (May 2006) and the general 20-years-ahead statement, both from the Wikipedia
  article on the problem. Notebook and post now say Linux 5.6 (2020) precisely.
- **X02-C** (MRZ). The notebook transliterated "Ayşe" to `AYŞE`, which is not a
  legal MRZ string; the transliteration now uses the ICAO table for German
  letters and strips accents from everything else, and asserts that the output
  is inside the 37-symbol alphabet.
- **X03-A** (Back button). Depth-first search was placed in session 5; it is
  session 6. "Every browser since 1994" dropped.
- **X03-B** (word count). Further reading pointed at *Algorithms Unlocked*
  ch. 2 for hash tables, which the book does not cover (one aside on p. 176);
  now CLRS ch. 11.
- **X04-A** (string sum). The numbers did not agree: 10 000 respondents give a
  20 000-character string, not 40 000 digits, and the question figure started
  the total at `0`, which Python refuses (`TypeError`). Now 20 000 respondents,
  expected sum about 800 000, 40 000 characters, `total = ""` in the figure
  (`genexamples_figs.py` fixed and the two SVGs regenerated), plus the case that
  actually happens in practice, `Series.sum()` on a text column, added to the
  notebook.
- **X04-B** (Ariane 5). The sequence of failures was reversed: per the inquiry
  report the *backup* SRI failed first at 36.7 s after H0 and the active unit
  0.05 s later, so the main computer switched to a unit that had already
  stopped; "72 ms later" was the data-cycle period, not the interval. "Flown
  flawlessly for a decade" is eight years (Ariane 4 first flew in 1988).
  "€370 million" is anachronistic for 1996; now "about US$370 million".
  Disintegration at about 39 s added from the report.
- **X04-C** (leap year). "Google Sheets and LibreOffice replicate the bug when
  importing .xls" is not right; they count from 30 December 1899, so their
  serial numbers agree with Excel's from 1 March 1900 on and differ by one
  before it. The precedence note in the notebook was muddled; rewritten.
- **X05-A** (Erdős). Facebook's 3.57 degrees (Edunov et al. 2016) was not
  computed "with the same algorithm" but with a probabilistic estimate of the
  same layer-by-layer expansion. The chain separator in the notebook output was
  an em dash.
- **X05-B** (Königsberg). "Euler drew four dots and seven lines": he did not
  draw the graph; the teaser now says he reduced the city to four land masses
  and seven bridges. Two bridges were destroyed in 1944 and two more replaced
  later; the five remaining allow an Eulerian path. The 5 040 and 48 walk
  counts were re-run and confirmed.
- **X05-C** (maze). Further reading pointed at *Algorithms Unlocked* ch. 5 for
  BFS and DFS; the book contains neither. Now CLRS §22.2–22.3. Title without
  the em dash: "Solve the maze without luck".
- **X06-A** (Hanoi). "The exercise sheet has a Hanoi item": there is none.
- **X06-B** (fractal tree). The deck claimed 512 tips and 1 023 segments for
  the depth-9 panel, which has 256 and 511 under the procedure as written; the
  figure now draws depth 10 (`genexamples_figs.py`), and the caption, deck and
  post agree. The pseudocode is in the course format.
- **X06-C** (ancestors). "Chang (1999) showed that the most recent common
  ancestor of all Europeans lived about 600 years ago" is not what the paper
  shows; it gives about $\log_2 n$ generations for a randomly mating population.
- **X07-A** (radix sort). "Hollerith's 1890 census tabulators sorted punched
  cards this way": the 1890 equipment had a sorting box whose lid opened at the
  right pocket; automatic sorters came in 1901 (H07 corrected the same way).
  "How numpy and pandas do it under the hood for integer keys" is overstated;
  NumPy's stable sort uses radix sort for 16-bit and smaller integers.
- **X07-B** (lower bound). Mergesort's measured worst case is at the bound for
  n ≤ 4 and one above it for n = 5 to 7, not "one or two above for every n".
- **X07-C** (Quickselect). "`median()` in a statistics library does not sort":
  Python's `statistics.median` sorts; NumPy's `median`, `partition` and
  `percentile` use selection. Expected comparisons about 3.4n stated.
- **X09-A** (coffee machine). "Sipser ch. 1 has a coin machine": it has an
  automatic-door controller. The minimal *complete* machine has seven states
  (six amounts plus reject); deck, post and notebook now say so.
- **X10-A** (husky/wolf). "About 90% accurate on the test set": the paper shows
  10 test predictions with 2 wrong; now "eight out of ten". Training images
  were hand-picked so that wolves had snow behind them (stated).
- **X10-B** (Titanic). Title without the em dash. Counts re-checked against the
  notebook output (TP 233, FP 81, FN 109, TN 468; majority 0.616).
- **X10-C** (K-means). The post quoted the figure script's WSS values (3 489,
  1 503, 299) as "the notebook's data"; the notebook prints 3 472, 1 557, 306.
  K-means is now given in the course pseudocode with the $C(i)$, $m_k$ notation
  of session 10.
- **X11-B** (join). "The purchase/product tables are the ones in the main deck
  and the exam (DB-03, DB-04)": the exam items restructure a different
  purchases table; rephrased.
- **X12-A** (race). The post referred to "the databases example X11-B (two
  seats, one aeroplane)"; that is motivating example M11-B. The post title now
  matches the deck title; the notebook says it runs the 20 000-increment version.
- **X12-B** (GPU). "The notebook shows it running a hundred times faster": the
  stored run shows 13×; now "more than ten times".
- **X13-A** (Literary Digest). "Correctly predicted 1920–1932": every election
  since 1916.
- **X13-B** (Schelling). Coins on the chessboard were 1969, publication 1971.
  "The exam item DB-14e is the inference question": DB-14(e) asks about
  F = 0.5; rephrased.
- **X13-C** (Likes). The post said the model reached the human average
  (r ≈ 0.49) at 70 Likes; the paper gives r ≈ 0.56 for the average number of
  Likes and the 10/70/150/300 thresholds against colleague, friend, family
  member and spouse. Kosinski et al. 2013 title added.
- **H02**: no change of fact. **H03**: Nilsson (2009) "ch. 3" is not where the
  Logic Theorist is; now "the chapters on the Logic Theorist"; "programme",
  "encyclopaedia" Americanized. **H04**: Hopper "at the age of 37" in 1943
  (she was 36) now "in her late thirties"; COBOL: she advised the committee
  rather than "drove" it; Plankalkül "drawn up in Germany by 1945". **H05**:
  "worked in the resistance under a false name" softened to "worked in the
  political resistance before emigrating" (Herzenberg does not support the
  false name). **H06**: Bellman's sponsor was in Washington, not "at the Air
  Force". **H07**: 1890 sorter (above); Knuth vol. 3 "opening chapter" is the
  end of the sorting chapter (§5.5). **H08**: Edmonds's remark paraphrased more
  carefully. **H09**: the Chomsky hierarchy's four classes are from 1959, the
  1956 paper argued that English is not finite-state; "each of the three
  papers" showed the Entscheidungsproblem unsolvable is two of the three
  (Church and Turing). **H10**: AlexNet cut the error rate by more than a third
  (15.3% against 26.2%), not "nearly in half"; *Gender Shades* is fifteen
  pages, not eleven. **H12**: the Connection Machine was built for AI work, not
  specifically "the neural networks of session 10"; Amdahl 1967 is three
  pages. **H01**: the 1890 tabulation claim ("about a year") replaced by the
  population total announced within weeks.

### Consistency and notation

- Every deck's `uses` line and every notebook's "What we used" line checked
  against the numbered transcript headings; all now match (session 3's stacks
  and queues correctly attributed to session 5 §6, DFS to session 6 §6).
- Pseudocode in the examples (TREE in X06-B, K-MEANS in X10-C) in the course
  format; PARTITION named as in session 7.
- Notebook identifiers Americanized (`neighbors`, `centers`); no em dashes in
  markdown cells, code comments or printed strings.
- Deck templates in `genexamples.py`: slide titles now "A · Title · answer /
  why / notes" instead of em dashes; supplementary slides (X05-C, X10-C) and the
  overview text rewritten.
- `Examples/README.md` regenerated from the data (titles and taglines), prose
  without em dashes, "person of color".
- Main decks 9, 10 and 13 still carried eleven em dashes written as the HTML
  entity `&mdash;`, which the first pass's grep for the character missed; fixed
  and the three decks rebuilt.

### Style

All 49 posts rewritten in the transcript style: paragraphs of four to eight
sentences, bullet lists only for the "What we used" links and the reading
lists (plus the two genuinely tabular comparisons, the browser actions in
X03-A and BFS against DFS in X05-C), no em dashes, American spelling, "we" and
"you". Section headings kept so that `figposts.py` markers and the transcript
anchors still resolve; four text-fragment markers updated to the new wording.

### Checks

- `python3 tools/genexnotebooks.py`: 36/36 notebooks executed cleanly; the
  changed cells re-checked (X02-C now prints `CAGLA<<AYSE`, X04-A's pandas
  cell prints `'23413529'`, X06-B counts 1 023 segments at depth 10, X10-C's
  elbow values unchanged at 3 472 / 1 557 / 306).
- Example decks rebuilt with `buildex.sh`: 14, 14, 14, 15, 14, 14, 14, 14,
  15, 13, 14, 14 pages (unchanged), overflow none; the X04-A opening slide
  overflowed by one line after the rewrite and its text was shortened.
- Main decks 9, 10 and 13 rebuilt after the `&mdash;` fix: 82, 45, 41 pages,
  overflow none; PDFs refreshed. The rendered HTML of all 13 main decks
  contains neither `—` nor `&mdash;`.
- `python3 tools/figposts.py`: 129 figures inserted into 49 posts, no
  missing marker.
- `python3 tools/knitexamples.py`: 49 posts, index, 14 transcripts, 36
  notebooks; link check over the 100 HTML files: 1 084 relative links, 0
  broken (the one flagged anchor, in `X08-A.html`, is the checker misreading
  an HTML-escaped `&amp;` in an id that nbconvert generates and that resolves
  in the browser).
- Em dashes: none in `Examples/posts/*.md`, `Examples/README.md`,
  `Slides/Examples/*.qmd`, `Slides/Examples/README.md`,
  `tools/examples_data_*.py`, `tools/exnb_*.py`, `tools/figposts.py`,
  `tools/genexamples.py`, or the notebook cells. British spellings: none
  (the proper name *Computational Modelling of Social Systems* excepted).
- Outside this pass: the exercise sheets (`TheoryExercises/`) and the exam
  pool (`Exams/`) were not reviewed and keep their em dashes and spellings.

## Third pass (2026-09-18): exercise sheets, exam pools and solution files

Scope: the 13 theory exercise sheets (`TheoryExercises/TheoryExercises01.md`
to `13.md`), the six exam question pools (`Exams/Pool-*.md`), the exam
blueprint and example exam, and the READMEs of both folders. Same four
checks as before: sources, numbers, algorithms and code, prose in the course
style. In addition, every exercise and every pool item now has a solution
file with references to the slides and the handouts.

Method: every trace, count and numeric answer on the sheets and in the pools
was recomputed by script (selection-sort and ICBICS swaps and comparisons,
Huffman codes and average lengths, base conversions, IEEE 754 encodings,
hash-table layouts, binary-search comparison counts, BST insertions and
deletions, heap traces, BFS and DFS orders, Bellman-Ford and Dijkstra tables,
Amdahl speedups, the confusion-matrix metrics, the K-means elbow values, the
snowflake timestamps, the Schelling neighborhood counts). The figures used by
the sheets and pools were rendered and read (the automaton, the min-heap, the
flowchart, the Turing machine, the clique graph, the Schelling grid). Slide
numbers were taken from the `## ` headings of each `Slides/*.qmd` (title
slide = 1, matching the section count of the rendered HTML) and handout
anchors from the `## N. Title` headings of `Transcripts/*.md`; all links in
the new files were checked by script.

### Corrections of fact

- **Sheet 2, A2(a)**: `0xC0FFEE − 0xC0C0A` was given as `0xB43FE4`; the
  difference is 11 858 916 = `0xB4F3E4` (two hex digits were transposed).
- **Sheet 2, A6**: the snowflake id decoded to the wrong instant. The id's
  timestamp field is 1 583 178 896 824 ms after the Twitter epoch, that is
  2020-03-02 19:54:56 UTC; the sheet said 1 583 020 469.654 s. The Python
  check now uses `datetime.fromtimestamp(…, timezone.utc)` rather than the
  deprecated `utcfromtimestamp`.
- **Sheet 5, Exercise 3(b)**: the Bellman-Ford question did not say from
  which node to start; "starting from node **A**" added, which is what the
  2024 sheet and the pool item `GP-08` assume.
- **Sheet 6, A3(c)**: the naive Fibonacci estimate for $n = 100$ was
  "$1.6^{100} \approx 2 \times 10^{20}$ calls, about 6 300 years";
  $1.618^{100} \approx 2.6 \times 10^{20}$ calls at $10^9$ per second is
  about 8 000 years.
- **Sheet 7, A4(a)**: the array after the first pass of the trace was
  wrong; corrected to `[3, 5, 4]`.
- **Sheet 3, Exercise 2(a)**: the list given for binary search is unsorted.
  This is deliberate (the hint on the sheet says so, and the 2023 exam made
  the same mistake by accident, see erratum 2 in `Exams/README.md`); the
  solution explains it before searching the sorted list.
- Pool items: all 93 solutions recomputed, no numeric error found (the
  numbers in `IC-01` to `IC-14`, `DS-04`, `DS-06`, `DS-09`, `DS-10`, `AC-05`,
  `AC-08`, `AC-09`, `AC-13`, `AC-14`, `GP-03`, `GP-04`, `GP-08`, `GP-11`,
  `GP-13`, `DB-07`, `DB-10`, `DB-14` and `TC-13` were checked individually;
  the seven unsatisfied cells of the Schelling grid in `DB-14` were
  recounted from `tools/genexam.py`).

### Solutions

- New folder `TheoryExercises/Solutions/` with `TheoryExercisesNN-Solutions.md`
  for each of the 13 sheets. The session exercises (1 to 3, or 1 to 4 on
  sheet 9) never had written solutions; they are now worked in full, in the
  course pseudocode where code is asked for. The additional-practice
  answers, previously in collapsible `<details>` blocks on the sheets, moved
  into the same files. Every solution opens with a **Where to look** line
  naming the slides (deck, slide numbers and titles) and the handout
  sections (transcript, section number and title, linked to the anchor).
- The 87 `<details>` blocks were removed from the sheets, which now carry
  questions only; each sheet's header note links to its solutions file.
  Copies of the sheets as they were before this pass are in the session
  scratchpad, not in the repository.
- New folder `Exams/Solutions/` with one `Pool-N-…-Solutions.md` per pool,
  generated from the pool files by the new `tools/gensolutions.py`: the
  solution and marking notes of each item, preceded by the same kind of
  **Where to look** line (references for all 93 items are in the script's
  `REFS` table; the script reports items without references). The pool files
  stay the master copy and keep their solutions; `Exams/Solutions/README.md`
  is generated with the files.
- Both READMEs describe the new folders and how to regenerate the pool
  solutions.

### Consistency and notation

- Nineteen pseudocode blocks in the pool solutions were still in numbered
  Cormen style (`1  if n = 0 then`) rather than the course format of the
  conventions page (`Procedure`, `Inputs:`, `Result:`, `If … then … else`,
  `For i = 1 to n:`, `←`, `#` comments): `IC-12`, `DS-08`, `DS-10` to
  `DS-13`, `AC-01`, `AC-07`, `AC-11`, `AC-14` to `AC-16`, `TC-14`, `DB-07`,
  `DB-12`. All converted; `break` replaced by an early `return` or a flag,
  `NULL` by `NIL`, the prose that referred to line numbers reworded. The
  four numbered listings quoted inside *questions* (`AC-09` counting sort,
  the `PARTITION` of `AC-11`, `GP-08` Bellman-Ford, `GP-11` Dijkstra)
  reproduce what past exam papers printed and were left as they are.
- `IC-12`'s procedure used a helper `DIGIT(d)` without saying what it is;
  one sentence added.

### Style

- Em dashes: 267 removed from the sheets and 277 from the pools, blueprint
  and example exam (all 23 files now have none), each rewritten as a comma,
  a colon, a period or parentheses as the sentence required; table cells
  that held a lone em dash now hold an en dash.
- Spelling Americanized throughout (memorisation, randomised, grey,
  labelled, analyse, optimise and the like).
- The new solution files follow the same rules from the start.

### Checks

- `python3 tools/gensolutions.py`: 14, 15, 17, 17, 14, 16 items, no item
  without references.
- Link check over `TheoryExercises/Solutions/*.md` and
  `Exams/Solutions/*.md`: every relative link resolves and every transcript
  anchor exists (0 bad links).
- `grep '—'` over `TheoryExercises/`, `TheoryExercises/Solutions/`,
  `Exams/` and `Exams/Solutions/`: 0. No numbered-line pseudocode left
  outside the four quoted exam listings. No `<details>` left on any sheet.

## Fourth pass (2026-09-18): "why it matters" notebooks, solution figures, clarity review

Scope: a new folder `WhyItMatters/` with one notebook per lecture from 2 to
13; figures for the theory-sheet solutions and a trim of the longest ones;
and a clarity, completeness and correctness review of every exercise sheet,
every pool item, the blueprint and the example exam, read as a student would
read them.

### Notebooks

- `WhyItMatters/W02-…` to `W13-…` (`.ipynb` with stored outputs and a knitted
  `.html`), built and executed by the new `tools/genwhy.py` from
  `tools/why_NN.py`; `WhyItMatters/README.md` is generated from the same
  files. Each notebook runs two or three small experiments (under 30 s each
  on this machine, W09 about 25 s by design) showing why the lecture's content
  matters for computing with data: accumulated rounding error, the one-pass
  variance formula returning 0 on timestamps, silent int32 overflow and a
  CSV read with the wrong encoding (2); list against set for matching two
  surveys, comparison counts of binary search and `bisect` on unsorted data
  (3); interpreted loop against NumPy, aliasing and the mutable default
  argument, a wrong mean caught by an `assert` (4); adjacency matrix against
  lists at 100 000 people, BFS distances and what happens with a stack (5);
  naive against memoized Fibonacci, the recursion limit, Euclid (6); selection
  sort, mergesort and `sorted` timed, stability of ties, sort once then
  `bisect` (7); three duplicate finders, the exponent read off a log-log plot
  and extrapolated to a billion rows, best/average/worst case (8); a regular
  expression with exponential backtracking, the partition problem searched
  against verified, the Collatz loop and the halting problem (9); kNN training
  against test error, 91% accuracy on pure noise through leaky feature
  selection, the accuracy trap with imbalance (10); SQLite index against scan
  with `EXPLAIN QUERY PLAN`, GROUP BY in the database against pandas, a
  transfer that crashes halfway with and without a transaction (11);
  `multiprocessing.Pool` speedups against Amdahl's law (measured 1.9×, 3.0×,
  3.3× for 2, 4, 8 workers on this machine), exact combination of split
  statistics against averaging local ones, threads for waiting against
  computing (12); algorithmic confounding producing a rise in "attention"
  that is not there, and two mechanisms (cumulative advantage, fixed quality)
  producing the same heavy tail, told apart by parallel worlds (13).
- Session 13 does get a notebook: the lecture's two computational claims,
  that platform data can carry the platform's software as a signal and that a
  model reproducing a pattern proves sufficiency and not mechanism, are both
  demonstrable in a few lines and are not covered by the existing X13
  examples (which do Literary Digest and Schelling).
- No duplication of the 36 `Examples/` notebooks; all handout links checked;
  every claim in the markdown checked against the stored outputs (three
  corrected during review: the float32 step thresholds in W02, a heading in
  W10 that said 78% where the output says 91%, and a mechanism attributed to
  the lecture in W13 that the lecture does not name).

### Solution figures and trimming

- New `tools/gensolfigs.py` draws 19 SVG figures into
  `TheoryExercises/figures/sol-*.svg` from the data of the solutions (the
  traces are recomputed in the script): the question tree of the biased die;
  the hash table with chains; the three steps of the binary search; the four
  BSTs of sheet 3; the inheritance diagram with `Hero`; the BFS and
  Bellman-Ford graphs with distances, parents and tree edges; the heap before,
  during and after `reduce`; the DFS graph with discovery and finishing times,
  tree and back edges; the mergesort split and merge tree; the two O-notation
  bounds with $n_0$ marked; the DFA for `ICSS`; the PDA stack after each
  symbol; the confusion matrix with the four metrics against the always-normal
  classifier; the elbow plot; the schema with foreign-key arrows; Amdahl's
  curve; the MapReduce data flow for the correlation; the Schelling
  neighborhood with a simulated grid before and after the moves. The ASCII
  trees and diagrams they replace were removed. The BFS and Bellman-Ford
  figures are also copied to `Exams/figures/` and shown in `GP-03` and
  `GP-08`.
- Sheets 9 to 13 solutions tightened (9: 3 223 to about 2 900 words with two
  figures added; 10: 2 478 to 2 300; 11: 2 109 to 2 000; 12: 2 505 to 2 400;
  13: 3 802 to 3 360). The additional-practice answers, which were reviewed
  earlier, were kept as they were.

### Clarity and correctness review (all sheets, all pools, blueprint, example exam)

Every number recomputed again by script, this time by three independent
readers; the questions were read for missing definitions and conventions.

Question wording fixed:
- Sheet 2, Ex 1(c): the bit convention ("yes" = 1, "no" = 0) is now stated.
- Sheet 4, Ex 3: "up to 30 days later" made precise (strictly later, at most
  30 days), matching the solution and `DB-07`.
- Sheet 6, A3(a): base cases fib(0) = 0, fib(1) = 1 stated (the call count
  15 depends on them).
- Sheet 10, Ex 1(b), `DB-10`(b) and the example exam Q6(d): "if a metric is
  not defined, say so and why" (precision of the always-normal classifier is
  0/0).
- Sheet 11, A5(a) and its solution: the injection input had an unmatched `)`
  and is a syntax error against the given query; replaced by one that works,
  with a note on why XKCD's version has the parenthesis.
- Sheet 12, A3: a code snippet rewritten in the course pseudocode.
- `GP-10`: the question now names the graph and the algorithm it refers to.
- `DB-14`: parts relabeled a, b, c (were c, d, e) and the question now
  defines the neighborhood, the satisfaction rule and the (row, column)
  labeling of the figure; `DB-13` still wrapped its solution in `<details>`,
  converted to `**Solution.**`.

Solution corrections:
- Sheet 6, Ex 2(b): "A–C's twin direction" was called a back edge; A–C is a
  tree edge. The two back edges are B–C and C–E.
- Sheet 7, Ex 2(b) and `AC-08`(a): mergesort on the eight-element array makes
  15 comparisons, not 17; the merge order in `AC-08` was wrong.
- Sheet 7, Ex 3(a): the two exchanges of pass 1 were listed in the wrong
  order; Ex 3(b): the `≤` counterexample happens in pass 2 at j = 3, not "at
  j = 2 in a later pass".
- Sheet 8, Ex 2(b) and `AC-14`(c): the constants $c = 1$, $n_0 = c' + 1$ do
  not work when $c' = 0$; now $n_0 = c' + 2$ with the chain of inequalities.
  `AC-14`(d): "$O(N \log N / 2)$" is $O(N \log N)$.
- Sheet 5, A6(c): ratio 5 PB to 160 GB is about $3 \times 10^4$, not "$10^5$
  to $10^6$".
- Sheet 4, Ex 1: the quoted `TypeError` message updated to the actual Python
  3 text; Ex 3 notes that same-day registrations do not count.
- Sheet 3, Ex 2(c): how depth is counted (levels, root at 1) stated.
- Sheet 10, A5(c): the micro-average (about 0.86 against 0.64) computed
  rather than asserted.
- Sheet 6, A2 and A7: `Inputs`/`Result` headers added to three procedures.
- `GP-11`: a `|, |` table cell left by the dash cleaner; `AC-13` notes say
  that the `PARTITION` listing must be printed with the item; `TC-14`,
  `IC-14`, `DB-15`: punctuation and spelling.

Verified and left alone: sheet 5 Ex 3 and `GP-08`/`GP-11` keep their
numbered listings because the questions refer to line numbers; sheet 7 Ex 3
likewise ("find the exact line"); the four quoted exam listings in Pool 3;
`IC-06`'s "previous question" wording (quoted exam text, solution covers all
predecessors); `DS-08`'s figure tag; the blueprint needed no change.

### Checks

- `python3 tools/genwhy.py`: 12 notebooks execute without error; W12 re-run
  on an idle machine; `WhyItMatters/README.md` regenerated.
- `python3 tools/gensolfigs.py`: 19 figures, all rendered to PNG and read.
- `python3 tools/gensolutions.py`: 14, 15, 17, 17, 14, 16 items, no missing
  references.
- Link and anchor check over the sheets, both `Solutions/` folders, the
  pools, the WhyItMatters README and the notebook markdown: 0 problems; code
  fences balanced; no em dash, no British spelling, no `<details>` on any
  sheet.

## Fifth pass (2026-10-18): slide layout, fonts, structure

Requests from David, in order: course title on one line on the title slide;
"Winter Semester 2026-2027"; fonts about 25% larger, the smallest more; each
deck in its own folder with its own figures; footer "Session NN" without
date; slide numbers; the lab slide with AboutUS.svg; the ICSS Team and
course calendar slides from the new syllabus; all content visible, no wasted
space, photos smaller before text; schemas that do not move between
consecutive slides; tables with four visible edges; code that never scrolls
and is otherwise as large as possible; new linked-list diagrams, a larger
BST root-deletion example and new slides on linear and random probing in
session 3; and a Summary slide in place of every "Next Session" slide.

### Structure
- `Slides/NN-Name/ICSS-2026-NN-Name.qmd` with `figures/` holding exactly the
  figures that deck uses; example decks in `Slides/Examples/NN-Examples/`;
  theme and logo shared in `Slides/theme/`; 34 images used by no deck, plus
  those dropped in this pass (lab photos, tutorialspoint linked-list images,
  the QR code of the last session-13 slide), in `Slides/unused/`.
- The session 3 deck had been moved into ICSS-github; a copy was restored.
- Every reference in the repository was rewritten (transcripts, posts,
  solutions, pool solutions, tools); the generators (`genNN.py`,
  `genexamples.py`, `genexamples_figs.py`, `figposts.py`, `genmotivation.py`,
  `gensolutions.py`, `build.sh`, `buildex.sh`, the legacy `mkNN.py`) write
  and read the new layout.

### Theme (`Slides/theme/unikn.scss`)
- Base font 30px → 37.5px; sub-1em sizes raised further (factor f → f^0.75),
  footer and code larger; title-slide plate 1.32em so the course name stays
  on one line (`.course` is `nowrap`).
- Per-slide fit levels `{.fit1}`..`{.fit4}` (section font 0.9 / 0.8 / 0.72 /
  0.64, slide title unchanged; fit2 equals the old base size).
- Slide number at the right end of the footer, on screen and in the printed
  PDFs (in print the bar stops short of the corner so the per-page number is
  not painted over).
- Every table has an outer border; person icons keep their aspect ratio.

### Decks
- Final state: all 25 decks render, every slide fits (no content below the
  footer line, past the page edges, out of its column, or in a scrolling code
  block), and every PDF has one page per slide.
- Slide counts are unchanged except session 3 (+3: slides 46 to 48, "Hash
  Collisions - Linear Probing", "Random Probing", "Probing: what to watch")
  and session 13 (−1: its last slide was merged into the Summary). Solution
  and pool references to session 3 slides from 46 on were shifted by +3.
- Fit levels: most slides at full size; the rest mostly fit1, few fit2, fit3
  on four slides, none at fit4.
- Session 1: AboutUS.svg lab slide; ICSS Team, Structure and Course calendar
  slides updated to the WS 2026/27 syllabus (tutors Aaron Siebert, Eli
  Schwarer, Anna Luise Harnischmacher; lecture Wednesday 10:00-11:30 and
  exercises Tuesday 15:15-16:45, both D301; the two no-class notices).
- Session 3: generated linked-list, deletion and doubly-linked-list diagrams;
  root-deletion example across the full width; probing figures on the same
  keys and table as separate chaining; BST sequences pixel-stable.
- Trace sequences made stable in sessions 2, 4, 5, 6, 7, 8, 9, 11, 12, 13
  (shared SVG canvases in `gen05/06/07.py`, identical containers and sizes).
- Code blocks sized per block so the longest line just fits.
- Summary slides with a final "Next session:" line in every lecture deck.
- Example decks: figure sizes measured by the new `tools/tuneexamples.py`
  (stored in `tools/examples_figsize.json`); SVG canvases cropped to their
  content; reveal's auto-stretch disabled; em dashes removed from figure
  labels; Literary Digest plot labels no longer overlap.

### Left as they are
- The "Lectures Outline" slide (decks 1 and 2) still lists "Session 4:
  Programming" and "Session 14: Exam Review", while the new syllabus calls
  session 4 "Software" and has no session 14.
- The decks copied earlier into `ICSS-github/Slides/` (01 to 03) are the old
  versions and use the old layout.

## Sixth pass (2026-10-30): session 4 becomes "Software"

David: rework session 4, renamed "Software": a much shorter part on
programming languages; no syntax, semantics or type systems; a short
imperative part; the basics of OOP with a method call on a string and a class
of your own; no debugging; two new sections on software engineering,
specifications and testing, after a typical software engineering flow; new
motivating examples on vibe coding going wrong, with specifications and tests
as the answer.

### Deck (`Slides/04-Software/ICSS-2026-04-Software.qmd`, 34 slides, was 71)
- Motivating examples, all checked against several independent reports:
  A, Replit's agent deleting SaaStr's production database during a code
  freeze (July 2025; Fortune, AI Incident Database; Replit then separated
  development and production databases); B, the Lovable apps exposing their
  users' data (CVE-2025-48757: 170 of 1 645 showcase apps); C, METR's
  randomized trial (Becker et al. 2025, arXiv 2507.09089: 19% slower with AI
  tools, believed 20% faster). A fourth candidate, Gemini CLI deleting a
  user's files, was dropped because only one source reports it.
- Programming in a nutshell (10 slides): what programming is, levels of
  language (one slide), interpreter vs compiler (one slide), paradigms (one
  slide), imperative programming (one slide), OOP (four slides: concepts;
  methods on a string; a `Respondent` class with two objects; encapsulation,
  abstraction, inheritance, polymorphism). Removed: Ada Lovelace (also in
  session 1), syntax, semantics, type systems, why so many languages, von
  Neumann, the Employee example, functional programming and LISP, esoteric
  languages, good practices, debugging.
- Software engineering: definition (IEEE 610.12), a six-stage flow with
  feedback loops, and the same flow marking what an LLM can take over
  (implementation) and what stays with the programmer (specification,
  testing). New figures drawn by `tools/gen04.py`.
- Specifications: definition with pre- and postconditions; an ambiguous
  request ("the mean age of the respondents") and the five questions it
  hides; the specification as a docstring; functional and non-functional
  requirements, tied to examples A and B; the specification as the prompt,
  and why must-never rules are enforced, not prompted.
- Testing: definition and `assert`; pytest tests derived from the
  specification; a plausible generated implementation that fails two of
  them (26.7 instead of 40; returns 0 instead of raising), with the real
  pytest output; choosing test cases; test first, then generate; what tests
  cannot do (Dijkstra 1970). All code was run to produce the outputs shown.
- Summary slide with "Next session: Algorithms". Every slide fits; code
  blocks sized by `tools/fitcode.py` to the largest size without scrolling.

### Handout and dependants
- `Transcripts/04-Software.md` rewritten to follow the deck (sections 1 to 7,
  check yourself, references). The old `04-Programming` deck and handout are
  not in the repository any more.
- Links to the old handout sections were remapped across the repository
  (example posts, solutions, notebook, README); link texts that named removed
  sections were rewritten. Five sentences in the handouts of sessions 1, 5,
  7, 11 and 12 that pointed to removed material were reworded.
- Exercise sheet 4 and its solutions: renamed; every "Where to look" line
  points to the new slides; for exercises whose topic left the lecture
  (debugging, syntax and semantics, naming), the line says so and names the
  book chapter instead. Pool references: `DS-14` no longer cites session 4,
  `DB-07` cites slide 12 and handout §3.
- Example deck 4, its three posts and the history post, the session 4
  notebook (now `WhyItMatters/W04-Software`), the motivating-examples
  catalogue and its data, the course outline of every deck, and deck 3's
  next-session line now say "Software".
- Unused images of the old deck moved to `Slides/unused/04-Software/`.

### Open
- Exercise sheet 4 still has an exercise on debugging and practice items on
  syntax and semantics, naming and debugging, which the lecture no longer
  covers, and none on specifications or tests.
- The exam pool has no items on specifications or testing.

## Seventh pass (2026-10-30): session 4, second round

David's list of changes to session 4, all done.

- **Deck** (40 slides, `measuredeck` overflow 0, PDF reprinted): see
  PROGRESS.md. Figures from `tools/gen04.py`; replaced figures moved to
  `Slides/unused/04-Software/`. New section 3 "Requirements, specifications,
  and design" (slides 24 to 32); testing is slides 33 to 39.
- **Motivating examples**: A Tea (July 2025: 72 000 images, 13 000 selfies and
  IDs, an unsecured Firebase bucket; a second leak of more than a million
  messages). The vibe-coding attribution is disputed: the leaker and many
  commentators blamed it, Tea says the exposed system predates February 2024;
  the slide and handout say so. B Antigravity (Google's agent deleted a
  developer's D: drive with `rmdir /s /q d:\`; TechRadar, AI Incident
  Database 7050). C Replit (kept, with the record counts). Catalogue entries
  in `tools/motivation_data.py` rebuilt from deck and handout;
  `MotivatingExamples.md` regenerated with `write_selector()` only.
- **Handout** `Transcripts/04-Software.md` rewritten to the deck; section 6
  renamed, anchor `#6-requirements-specifications-and-design` updated in the
  posts and in `why_04.py`; all anchors into handouts 03 and 04 checked.
- **WhyItMatters W04**: part 2 (aliasing, mutable default) removed; new part 3
  "Vibe coding with a test suite": a generated `interviews_per_month` parses
  day-first German dates month first, silently, until four tests fail; the
  failures plus the specification become the prompt; the corrected version
  (hardcoded, so the notebook runs offline) passes.
- **Exercise sheet 4**: four cases (survey answer counts, seminar waiting
  list, respondents in both waves, exercise-point grades), each with
  requirements, docstring specification, design with session-3 data
  structures, and tests; new practice A1 to A6. Solutions rewritten; all 23
  model tests run green against reference implementations. The old
  inheritance figure moved to `TheoryExercises/figures/unused/` and dropped
  from `gensolfigs.py`'s main.

### Open
- The exam pool still has no items on requirements, specifications or tests;
  the sheet 4 cases are natural candidates.
