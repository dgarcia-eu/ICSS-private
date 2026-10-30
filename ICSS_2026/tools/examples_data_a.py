"""Question/answer examples for sessions 2-7.  See examples_data_b.py for 8-13
and genexamples.py for how they become decks.

Each example: an OPENING slide (a question, mystery or problem for the start
of the lecture), a CLOSING slide (the answer, pointing at what the lecture
taught), and a NOTES slide for the lecturer (sources, facts, how to present).

Image paths are relative to Slides/Examples/.  `imgh` is the image height in
em (24em = full slide height).  `wide=True` puts the image above the text
instead of beside it.  Section numbers (§) refer to the numbered headings of
the matching transcript in Transcripts/.
"""

X = {}


def ex(xid, title, tagline, open_, close, notes):
    X[xid] = dict(title=title, tagline=tagline, open=open_, close=close,
                  notes=notes.strip("\n"))


# ===========================================================================
#  02  Information Coding
# ===========================================================================

ex("X02-A", "The clock that ends on 19 January 2038",
   "Why one specific second breaks a 32-bit counter, and what it wraps to.",
   dict(img="figures/02-y2038-q.svg", imgh=7.2, wide=True, credit="",
        body=r"""
Many systems count time as **the number of seconds since 1 January 1970**,
stored in a **32-bit signed integer**. On **19 January 2038, at 03:14:07 UTC**,
that counter reaches the pattern above, and one second later something goes
badly wrong.
""",
        ask="Why *that* second? And what date will the computer think it is at 03:14:08?"),
   dict(img="figures/02-y2038.svg", imgh=7.2, wide=True, credit="",
        body=r"""
- A signed 32-bit integer holds $-2^{31} \ldots 2^{31}-1$; the largest value is
  $2\,147\,483\,647 = 0111\ldots1_2$, which is exactly 03:14:07 UTC on that day.
- Adding 1 carries into the **sign bit**: $1000\ldots0_2$, which in two's
  complement is $-2^{31}$, that is, **20:45:52 UTC on 13 December 1901**.
- The fix is a 64-bit counter: $2^{63}$ seconds is about 292 billion years.
""",
        uses="§4 positional number systems · §6 negative numbers and two's complement · §10 data types and integer size"),
   r"""
**Source.** The Year 2038 problem is documented for every C standard library
and by the Linux kernel, which supports a 64-bit `time_t` on 32-bit
architectures since version 5.6 (2020). The dates are exact:
`datetime.fromtimestamp(2**31 - 1)` and `datetime.fromtimestamp(-2**31)`; the
figure computes them.

**Facts.** $2^{31} - 1 = 2\,147\,483\,647$ seconds is 68.05 years after the
epoch. The wrap goes to the most negative value, so time jumps *backwards* by
136 years. Early cases are documented: AOLserver crashed in May 2006 because a
timeout of one billion seconds pointed past 2038, and any program that computes
a date twenty years ahead has been able to overflow since January 2018.

**How to present.** Open by showing only the bit pattern and the date, and ask
the room to guess what comes next; most guesses are "it resets to 1970". Close
by adding one to the bits on the board: the carry into the sign bit *is* the
whole answer, and it lands the moment two's complement has been taught.

**Where it plugs in.** After the two's-complement slides of the main deck; the
transcript's §6 has the wheel diagram, which makes the wrap visual.
""")

ex("X02-B", "0.1 + 0.2 is not 0.3",
   "The most famous wrong answer in computing, resolved bit by bit.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
```python
>>> 0.1 + 0.2 == 0.3
False
>>> 0.1 + 0.2
0.30000000000000004
```

This is Python, but every language, every calculator app and every spreadsheet
does the same. It is not a bug and it will never be fixed.
""",
        ask="What does the computer actually store when you type `0.1`, and why does the error show up in the 17th decimal, not the 3rd?"),
   dict(img="figures/02-float-sum.svg", imgh=7.6, wide=True, credit="",
        body=r"""
- A double has **52 significand bits**; $0.1 = 1/10$ has a factor 5 in the
  denominator, so its binary expansion is infinite and it is stored **rounded**,
  slightly above $0.1$.
- $0.2$ is also stored slightly above. Their sum rounds **up**; the stored $0.3$
  rounds **down**. The two differ by **one unit in the last place**: $2^{-54}$.
- Compare floats with a tolerance, never with `==`; keep money and counts in integers.
""",
        uses="§7 IEEE 754: sign, exponent, significand · §8 when rounding errors matter"),
   r"""
**Source.** IEEE 754-2008; the site *0.30000000000000004.com* collects the
same result in about 40 languages. The hex patterns and exact decimal
expansions in the figure are computed with `float.hex` and `decimal`, not typed
in.

**Facts.** `0.1` is stored as `0x3FB999999999999A`, exactly
0.1000000000000000055511151231257827…; `0.3` as `0x3FD3333333333333`; the sum as
`0x3FD3333333333334`. The difference is $2^{-54} \approx 5.55 \times 10^{-17}$.

**How to present.** Open with the three REPL lines and *nothing else*; let it
sit. Ask for hypotheses ("Python is broken", "it is a display issue"). Close
with the figure, walking the last hex digit: `…33` against `…34`. Then the
practical rule (`math.isclose`, `Decimal` for money); students will meet this in
the practical part within weeks.

**Where it plugs in.** Directly after the IEEE 754 slides; pairs with the
$-1\,703\,936$ decoding example already in the deck. The Vancouver Stock
Exchange candidate (M02-C) is the accumulation version of the same point.
""")

ex("X02-C", "Why your boarding pass spells you MUELLER",
   "Passports, airlines and ASCII: what happens to a name when the alphabet has 37 symbols.",
   dict(img="figures/02-mrz.svg", imgh=8.2, wide=True, credit="",
        body=r"""
The **machine-readable zone** at the bottom of every passport renders *Jörg
Müller* as `MUELLER<<JOERG` and *Çağla* as `CAGLA`. Airlines and border systems
copy that spelling.
""",
        ask="Why can a document made in 2020 not spell an umlaut? And what happens when two systems disagree about the answer?"),
   dict(img="figures/02-mrz.svg", imgh=7.0, wide=True, credit="",
        body=r"""
- The MRZ is defined by ICAO 9303 over **37 symbols** (A–Z, 0–9, `<`) so that
  *any* reader anywhere decodes it identically: a deliberate, minimal alphabet.
- It is the ASCII problem in miniature: 7 bits gave 128 codes, none for ö, ç or
  ß; the 1980s code pages assigned byte 246 to ö in Germany and to ц in Russia.
- **UTF-8** solved it: ö is the two bytes `C3 B6`, ASCII stays one byte. Systems
  that still assume one byte per character produce `MÃ¼ller`.
""",
        uses="§3 storing information digitally · §9 character coding: ASCII, code pages, Unicode and UTF-8"),
   r"""
**Source.** ICAO Doc 9303, Part 3 (transliteration tables: ö → OE, ß → SS,
ç → C, ş → S). The passport shown is a mock-up with an invented number.

**Facts.** The MRZ line is 44 characters; the check digits are computed with
the weights 7, 3, 1. Germany's own convention writes *Müller* as `MUELLER`,
which is why boarding passes and tickets must be booked under that spelling, a
consequence students have usually met personally.

**How to present.** Open by asking who has seen their name "wrong" on a
boarding pass; in a German classroom that is most of the room. Close by
putting the three answers side by side: 37-symbol MRZ (by design), ISO-8859-1
(one byte, national), UTF-8 (variable length, universal). The point to land:
none of these is *the* right encoding; the failure is in *not saying which one*.

**Where it plugs in.** The character-coding block of the main deck (ASCII table,
code pages, UTF-8). Pairs with candidate M02-B (mojibake in survey data).
""")

# ===========================================================================
#  03  Data Structures
# ===========================================================================

ex("X03-A", "Where does the Back button keep the pages?",
   "Visit A, B, C, go back twice, then open D. Where did C go? Two stacks explain every browser.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
You open **A**, then **B**, then **C**. You press *Back* twice, so you are on A.
Now you click a link to **D**. Press *Forward*: nothing happens. **C and B are
gone.** Every browser since the first graphical ones behaves exactly like this.
""",
        ask="What structure is the history stored in, and why is throwing C away the *correct* behavior rather than a bug?"),
   dict(img="figures/03-browser-stacks.svg", imgh=8.6, wide=True, credit="",
        body=r"""
- Two **stacks**: *back* and *forward*. Opening a page **pushes** the current one
  onto *back*; pressing Back **pops** it and pushes the current page onto *forward*.
- Opening a new page from A **clears the forward stack**; otherwise Forward would
  have to choose between C and D, and a stack has no way to hold two futures.
- LIFO is exactly the order you want here: the most recent page is the one you
  return to. The same structure runs Undo, the call stack, and depth-first search.
""",
        uses="§1 what a data structure is · §3 linked lists (what the stack is built on) · session 5 §6 stacks and queues"),
   r"""
**Source.** The two-stack model is how Mosaic and Netscape implemented history;
modern browsers keep a session-history list with a current index, but the
visible behavior is unchanged. Any browser demonstrates it live.

**Facts.** Push and pop are $O(1)$. The clearing rule is in the HTML standard:
navigating to a new page removes all session-history entries after the current
one.

**How to present.** Open by doing it live on the projector: A, B, C, Back,
Back, click D, Forward is grayed out. Ask *why*. Close with the three-state
figure; the last panel is the punchline. Then contrast with a support
helpline, where LIFO is the *wrong* policy: same structure, opposite verdict,
decided by what the user needs next.

**Where it plugs in.** Stacks and queues are formally introduced in session 5
(§6 of that transcript), but the main deck of session 3 already presents the
linked list they are built on; use this right after linked lists. Depth-first
search, the stack-driven search, comes in session 6.
""")

ex("X03-B", "Count a million words: 49 seconds or 0.01",
   "The same loop, two containers, a factor of 4,500, measured on this laptop.",
   dict(img="figures/03-wordcount.svg", imgh=7.4, wide=True, credit="",
        body=r"""
Two students count how often each word appears in a corpus of parliamentary
speeches. One keeps a **list of (word, count) pairs**; the other keeps a
**dictionary**. Both loops are five lines long and both give the same counts.
On 100,000 words, one takes **49 seconds** and the other **0.01**.
""",
        ask="Nothing in the loop changed except the container. Where do the 49 seconds go?"),
   dict(img="figures/03-wordcount-timing.png", imgh=9.4, wide=False, credit="measured with `tools/genexamples_figs.py`",
        body=r"""
- The list has to be **searched** for every incoming word: with $m$ distinct
  words that is up to $m$ comparisons per word, so the total grows like $n \cdot m$.
- The dictionary is a **hash table**: the hash of the word says which slot to
  look in, so each update costs the same whether the table holds 10 entries or
  10 million.
- On the log-log plot the list line has **slope 2**, the dictionary line slope 1:
  the gap is not a constant, it keeps widening.
""",
        uses="§4 the editing-versus-searching trade-off · §8 hashing and hash tables · §9 dictionaries in Python"),
   r"""
**Source.** Timings are produced by the figure script on the build machine and
printed to the console; re-run it for fresh numbers before the lecture if you
want to quote today's laptop.

**Facts.** 1,000 words: 0.003 s against 0.0001 s. 100,000 words: about 49 s
against 0.011 s. Half the words in the stream are distinct, which is a
realistic vocabulary ratio for short texts and makes the list version quadratic.

**How to present.** Open with the two code fragments side by side (they are on
the figure) and the two times; ask which is which and why. Close with the
log-log plot and the slope argument; this is also a preview of O-notation in
session 8, so name it as such. Then the caveat: $O(1)$ is an *average*; a bad
hash function degrades to the list case (the exam's $2x \bmod 16$ item).

**Where it plugs in.** Right before the hash-table slides; the transcript's §8
shows the collision handling that makes the average hold.
""")

ex("X03-C", "The waiting room that gets slower the fuller it is",
   "Calling the next patient costs 1,000 moves in one structure and one in another.",
   dict(img="figures/03-queue-shift-q.svg", imgh=8.8, wide=True, credit="",
        body=r"""
A clinic's software keeps the waiting patients in an array, in arrival order.
Calling the next patient removes the first entry, and **every remaining entry
shifts one place forward.** With 1,000 people waiting, each call costs 1,000
moves; the queue gets slower exactly when it is longest.
""",
        ask="What has to change so that 'call the next patient' costs the same whether 6 or 6,000 people are waiting?"),
   dict(img="figures/03-queue-shift.svg", imgh=8.8, wide=True, credit="",
        body=r"""
- Removing from the **front of an array** is $O(n)$ by construction: the elements
  are contiguous, so a hole must be closed.
- A **queue** keeps a *head pointer* (or is a linked list): removing the front is
  one pointer move, $O(1)$, regardless of length. Adding at the tail is also $O(1)$.
- The price: you lose $O(1)$ access to the $k$-th waiting patient. Choosing a
  structure is choosing which questions will be cheap.
""",
        uses="§2 arrays and why contiguity gives indexing · §3 linked lists · §4 the trade-off · session 5 §6 queues"),
   r"""
**Source.** Textbook material: arrays in Cormen, *Algorithms Unlocked*, ch. 2;
stacks and queues in CLRS §10.1. Python's `list.pop(0)` really is $O(n)$ and
`collections.deque.popleft()` is $O(1)$, a one-line change students can time
themselves.

**Facts.** Shifting $n-1$ elements per call; with a circular buffer or a deque
both ends are $O(1)$. The "slower when fuller" symptom is the diagnostic
signature of an $O(n)$ operation inside a loop.

**How to present.** Open with the top half of the figure only (the shift) and
the sentence "the system is slowest when the waiting room is fullest". Close by
revealing the head-pointer version: one arrow moves. Ask what was given up
(random access); that keeps it a trade-off rather than a trick.

**Where it plugs in.** After arrays and linked lists in the main deck; it is the
concrete version of the transcript's §4. Connects forward to BFS in session 5,
which is a queue with a purpose.
""")

# ===========================================================================
#  04  Software
# ===========================================================================

ex("X04-A", "The survey whose ages summed to a 40,000-digit number",
   "One operator, two types, two meanings: the most common bug in beginner data code.",
   dict(img="figures/04-string-sum-q.svg", imgh=8.0, wide=True, credit="",
        body=r"""
A student sums the *age* column of a 20,000-person survey with a four-line
loop. Instead of a number near 800,000, the program prints a **40,000-digit**
value beginning `23413529…`.

No error, no warning, and every line is correct.
""",
        ask="What did the program actually compute, and what one word in the lecture names the mistake?"),
   dict(img="figures/04-string-sum.svg", imgh=8.0, wide=True, credit="",
        body=r"""
- Values read from a file are **strings** until converted. For strings, `+` means
  **concatenation**: `"23" + "41"` is `"2341"`. Twenty thousand ages of two digits
  make a 40,000-character string; the program did exactly what it was told.
- The fix is one call: `total += int(value)`. The lesson is **polymorphism**:
  the same symbol is a different operation for each class of object, and Python
  decides which at run time.
- Statically typed languages would have refused to compile `"" + 23`.
""",
        uses="§4 objects: the same `+`, a different method for each class · §6 specifications: say what type the input is · §7 testing: one known answer catches it"),
   r"""
**Source.** Composite of a bug seen in essentially every first-year cohort; the
figure is illustrative. In Python, `sum(["23", "41"])` raises `TypeError`
because it starts from the integer 0; the silent version needs an accumulator
that starts as a string, which beginners write, or a pandas column of text, on
which `.sum()` concatenates without a word.

**Facts.** `"1" + "2" == "12"`; `1 + 2 == 3`; `1 + "2"` raises. The silent
version is the dangerous one, and it is silent because both operands are
strings. A CSV reader returns strings for every field unless told otherwise.

**How to present.** Open with the output only, the enormous number, and ask
what went wrong. Someone will spot it fast; the value is in naming *why* the
language allowed it (dynamic typing, operator overloading). Close by running the
four lines with `type(value)` printed, which is also the debugging habit to
teach: inspect the value, not the intention.

**Where it plugs in.** After the slide on objects and strings in the main deck,
or as the lead-in to testing; the transcript's §4 and §7. Recurs in exam item
`DS-14`.
""")

ex("X04-B", "The rocket that exploded because a number did not fit",
   "Ariane 5, 4 June 1996: US$370 million, 37 seconds, one integer conversion.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
On its maiden flight, **Ariane 5** self-destructed about 37 seconds after
launch. Its guidance software was **reused from Ariane 4**, where it had flown
without fault since 1988. Nothing in the code had changed.
""",
        ask="If the code was correct for eight years, what could possibly have changed? And why did the *backup* computer fail in the same way?"),
   dict(img="figures/04-ariane-overflow.svg", imgh=7.8, wide=True, credit="",
        body=r"""
- Ariane 5 flies faster: a horizontal-velocity value that always fitted a
  **16-bit integer** on Ariane 4 now exceeded 32,767. The conversion from a 64-bit
  float **overflowed**, raising an exception the code did not handle.
- The backup unit shut down first, as designed. The active unit ran **identical
  code on identical data** and shut down 50 ms later. With no attitude data, the
  rocket steered into aerodynamic breakup.
- The conversion was left unprotected *on purpose*, a decision from an Ariane 4
  analysis that no longer held. Types have ranges; reuse changes the inputs.
""",
        uses="§5 software engineering: reused code carries old requirements · §6 specifications: the range of a value is part of them · §7 testing: never tested with Ariane 5 data"),
   r"""
**Source.** Lions, J.-L. et al. (1996), *Ariane 5 Flight 501 Failure: Report by
the Inquiry Board*, ESA/CNES. Public and short; the numbers here are from it.
The cost estimate (about US$370 million) is from contemporary press; no one was
hurt.

**Facts.** The variable was the horizontal bias (BH). Of seven such
conversions, four were protected and three were not, on the reasoning that the
values were physically bounded, which held for Ariane 4. The alignment function
that failed was not even needed after lift-off; it kept running for 40 s by an
old requirement. The backup failed at 36.7 s after H0, the active unit 0.05 s
later, and the launcher disintegrated at about 39 s. Redundancy did not help
because the failure was deterministic.

**How to present.** Open with the launch story and the paradox "unchanged code,
new failure". Close by drawing the 64-to-16-bit funnel on the board: the number
is too big for the box. The deeper lesson for social scientists: every reused
analysis script carries assumptions about the data's range that nobody wrote
down. Ask them to name one from their own work.

**Where it plugs in.** In the specifications section of the main deck, next to
functional and non-functional requirements; the transcript's §6. Image note: no public-domain photo of Flight 501 exists; the figure
is a diagram deliberately.
""")

ex("X04-C", "Was 1900 a leap year? Excel says yes",
   "A three-line rule, a 120-year-old bug, and why control flow has to be written down exactly.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
Type `=DATE(1900,2,29)` into Excel: it accepts it. **29 February 1900 did not
exist**; 1900 was not a leap year. Excel's day count before 1 March 1900 is
off by one, and Microsoft has documented that it will never be fixed.

- 2024 was a leap year. 1900 was not. **2000 was.**
""",
        ask="Write the rule that decides. Why is *divisible by 4* not enough, and why did a 1980s spreadsheet get it wrong on purpose?"),
   dict(img="figures/04-leap-year.svg", imgh=9.6, wide=True, credit="",
        body=r"""
- Gregorian rule: a leap year is divisible by 4, **except** century years, **unless**
  divisible by 400. Three nested conditions; the flowchart is the program.
- `year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)`: one line of Python,
  and every parenthesis matters.
- Lotus 1-2-3 (1983) got it wrong; Excel copied the bug in 1987 so spreadsheets
  would stay compatible, and keeps it to this day: **compatibility beat correctness**.
""",
        uses="§6 specifications: a rule with three clauses · §3 imperative programming: conditions · §7 testing: 1900 and 2000 are the boundary cases · session 5 §5 flowcharts"),
   r"""
**Source.** Microsoft support article "Excel incorrectly assumes that the year
1900 is a leap year" (KB 214326). The Gregorian rule is from the 1582 papal
bull *Inter gravissimas*.

**Facts.** Excel's serial number 60 is the non-existent 29 February 1900, so
weekdays and day differences that cross that date are off by one. LibreOffice
and Google Sheets count from 30 December 1899 instead: their serial numbers
agree with Excel's from 1 March 1900 on and differ by one before it. Excel for
Mac historically used a 1904 epoch to sidestep the problem.

**How to present.** Open with the three-line quiz (2024 / 1900 / 2000) and get
a show of hands on 1900; then reveal that Excel accepts 29.2.1900. Close by
building the flowchart *with* the room, one diamond at a time; students write
the Python line themselves, and most forget the parentheses the first time,
which is the teaching moment about precedence.

**Where it plugs in.** The imperative programming slide or the test-case slide
of the main deck; it is also a
natural first flowchart for session 5 (§5 of that transcript), so it can be
reused there.
""")

# ===========================================================================
#  05  Algorithms
# ===========================================================================

ex("X05-A", "What is your Erdős number?",
   "Six degrees, measured: how to compute a distance in a graph of two million authors.",
   dict(img="figures/05-erdos-q.svg", imgh=8.0, wide=True, credit="",
        body=r"""
Paul Erdős wrote about 1 500 papers with 500 co-authors. Your **Erdős number**
is the length of the shortest co-authorship chain from you to him: co-authors
have 1, their co-authors 2, and so on. Most mathematicians have one below 8.
(Kevin Bacon numbers work the same way for actors.)
""",
        ask="Given the co-authorship graph, two million authors and ten million edges, what exact procedure computes *your* number? And how do you know it is the shortest?"),
   dict(img="figures/05-erdos-bfs.svg", imgh=8.0, wide=True, credit="",
        body=r"""
- **Breadth-first search** from Erdős: visit all co-authors (distance 1), then
  all *their* unvisited co-authors (distance 2), and so on, using a **queue** so
  that whole layers finish before the next begins.
- The first time BFS reaches you, the distance recorded is the shortest,
  because every shorter path would have been discovered in an earlier layer.
- Cost: each author and each co-authorship looked at once, $O(|V| + |E|)$,
  which is seconds for ten million edges.
""",
        uses="§7 graphs · §8 representing graphs (adjacency lists) · §9 breadth-first search and why it finds shortest paths · §10 graphs in social science"),
   r"""
**Source.** The Erdős Number Project (Oakland University) maintains the data;
Grossman & Ion (1995). The small graph in the figure is illustrative except for
Graham, Chung, Lovász and Knuth, who really do have Erdős numbers 1, 1, 1 and 2;
"Garcia" and "You" are placeholders. BFS in the figure is actually run by the
script.

**Facts.** Median Erdős number among mathematicians with a finite one is about
5; the maximum known is 13. Facebook's 2016 estimate of 3.57 average degrees of
separation among 1.59 billion users (candidate M05-A) used a probabilistic
version of the same layer-by-layer expansion.

**How to present.** Open with the definition and ask for a *procedure*, not an
answer; write the room's suggestions on the board. Most will describe DFS
("follow a chain"), which does *not* give the shortest path. Close by running
BFS on the figure layer by layer, then state the invariant (layer $k$ contains
exactly the vertices at distance $k$). That invariant is the exam question.

**Where it plugs in.** Immediately before the BFS slides; the ten BFS state
figures in the main deck are the formal trace of this.
""")

ex("X05-B", "The seven bridges of Königsberg",
   "Euler, 1736: the first graph problem, and the first proof that something cannot be done.",
   dict(img="figures/konigsberg-bridges.png", imgh=8.6, wide=False,
        credit="Map: Bogdan Giuşcă, Wikimedia Commons, CC BY-SA 3.0",
        body=r"""
Königsberg (now Kaliningrad) had **seven bridges** joining two river banks and
two islands. The townspeople's puzzle: **walk across every bridge exactly once**
and return home.

Nobody managed it. In 1736 Leonhard Euler proved that nobody ever would, and
in doing so invented graph theory.
""",
        ask="How do you *prove* that no route exists, without trying all of them? What is the right way to write the city down?"),
   dict(img="figures/05-konigsberg-graph.svg", imgh=8.6, wide=False, credit="",
        body=r"""
- **Representation is the whole trick.** Land masses become vertices, bridges
  become edges. The geography of the map is irrelevant; only the connections matter.
- On such a walk you *enter* and *leave* each land mass, using two bridges per
  visit. So every vertex except the start and end needs an **even degree**.
- Königsberg's four vertices have degrees **5, 3, 3, 3**, all odd. No such walk
  exists. Euler's theorem: an Eulerian circuit exists iff every degree is even.
""",
        uses="§7 graphs: vertices, edges, degree · §8 representing graphs · §2 properties of an algorithm; a proof of impossibility is not an exhaustive search"),
   r"""
**Source.** Euler, L. (1736), *Solutio problematis ad geometriam situs
pertinentis*. The map image is CC BY-SA 3.0 (Bogdan Giuşcă, Wikimedia Commons);
the credit is on the slide. The multigraph is drawn by the script.

**Facts.** Degrees: A (Kneiphof island) 5; B, C, D 3 each. An Eulerian *path*
(not returning) needs exactly 0 or 2 odd vertices; Königsberg has 4. Two of the
bridges were destroyed in 1944 and two more were later replaced by a highway;
the five that remain allow an Eulerian path, from one island to the other.

**How to present.** Open with the map and the puzzle; give 90 seconds for the
room to try (nobody succeeds, which is the point). Close by redrawing the map as
the four-vertex graph *live*; the moment the geography disappears is the
lesson. Then the degree count. Emphasize that this is a proof, not a search:
trying all $7!$ orderings is an algorithm too, but Euler's argument is a
different kind of thing.

**Where it plugs in.** The introduction of graphs in the main deck; also a
bridge (sic) to session 9's theme that some things can be proven impossible.
""")

ex("X05-C", "Solve the maze without luck",
   "A procedure that finds the shortest way out of any maze, and knows when it has.",
   dict(img="figures/05-maze.svg", imgh=10.4, wide=False, credit="",
        body=r"""
Green in, red out. A person solves this by looking. A robot, or a program
exploring a network, a state space or a set of possible moves, has to be told
**exactly** what to do at every junction.
""",
        ask="Write the rule. Which cell do you look at next? How do you avoid loops? How do you know the path you found is the *shortest*?"),
   dict(img="figures/05-maze-solved.svg", imgh=10.4, wide=False, credit="",
        body=r"""
- The maze is a **graph**: open cells are vertices, adjacent open cells share an
  edge. Then it is BFS again.
- The numbers are BFS distances from the entrance; the red line follows the
  **parent pointers** back from the exit. Length **88**, and BFS guarantees that no
  shorter path exists.
- **119** cells explored, every reachable cell once. Depth-first search would
  also find *a* path, but not necessarily this one.
""",
        uses="§3 representing algorithms · §4 pseudocode · §7–§9 graphs and breadth-first search, including the parent array"),
   r"""
**Source.** The maze is generated by the figure script (recursive backtracker,
seed 7) and solved by BFS in the same script; the numbers on the slide are read
from that run, so regenerating changes them together.

**Facts.** Shortest path 88 steps; 119 cells reachable. The distance shading
shows the BFS "wave" expanding from the start. DFS on the same maze explores in
a completely different order and returns a path that is usually longer.

**How to present.** Open with the unsolved maze and the three questions; ask
students to write pseudocode in pairs for five minutes; most produce something
close to DFS. Close with the solved figure: point at the numbers, then ask
which cell was explored *first* at distance 3; the queue makes that a
well-defined question. Good moment to contrast BFS and DFS explicitly, since
session 6 will use DFS for recursion.

**Where it plugs in.** After the eight-node BFS trace in the main deck, as the
"now on something bigger" step.
""")

# ===========================================================================
#  06  Recursion
# ===========================================================================

ex("X06-A", "The monks, the 64 disks, and the end of the world",
   "A legend, a two-line recursive plan, and an exact count of 18 446 744 073 709 551 615 moves.",
   dict(img="figures/tower-of-hanoi.jpg", imgh=8.4, wide=False,
        credit="Photo: Wikimedia Commons, CC BY-SA 3.0",
        body=r"""
The legend: in a temple, monks move **64 golden disks** between three pegs, one
disk at a time, never placing a larger disk on a smaller one. When the last
disk is placed, the world ends.

With 3 disks it takes 7 moves. With 4, 15.
""",
        ask="How many moves for 64? And, the harder question, how do you write down the *procedure* for moving them, for any number of disks?"),
   dict(img="figures/06-hanoi.svg", imgh=7.0, wide=True, credit="",
        body=r"""
- **Recursive plan:** to move $n$ disks A→C, move $n-1$ disks A→B, move the
  largest A→C, move $n-1$ disks B→C. The base case is zero disks: nothing to do.
- Moves: $M(n) = 2M(n-1) + 1$, so $M(n) = 2^n - 1$. For 64 disks that is
  $2^{64} - 1 \approx 1.8 \times 10^{19}$: **585 billion years** at one move per second.
- The procedure is four lines. The iterative version exists but nobody can read
  it. This is what recursion is *for*: the plan is self-similar.
""",
        uses="§2 the three parts of a recursive definition · §4 how recursion runs: the program stack · §7 types of recursion (two calls: tree recursion)"),
   r"""
**Source.** Lucas, É. (1883), who invented the puzzle and the legend. Photo CC
BY-SA 3.0 via Wikimedia Commons; the diagram is generated. Number computed:
$2^{64}-1 = 18\,446\,744\,073\,709\,551\,615$; at $31\,557\,600$ s/year
that is about $5.85 \times 10^{11}$ years.

**Facts.** $M(n) = 2^n - 1$ is also a lower bound: the largest disk can only
move once all others are on one peg. Recursion depth is $n$, so the call stack
holds at most 64 frames, which is trivially fine; it is the *number* of calls
that explodes, not the depth.

**How to present.** Open with the physical puzzle if you have one (or the
photo), do 3 disks live, ask for 64. Guesses range wildly. Close by writing the
four-line procedure and *then* deriving $2^n-1$ from it; the recurrence falls
out of the code. Note the distinction between exponential *work* and linear
*depth*, which the fractal-tree example (X06-B) reinforces.

**Where it plugs in.** After the factorial and program-stack slides; before
"types of recursion". Counting the moves is a natural exercise.
""")

ex("X06-B", "Draw this tree in five lines",
   "A picture that is made of smaller copies of itself, and the code that has the same shape.",
   dict(img="figures/06-fractal-tree.svg", imgh=8.0, wide=True, credit="",
        body=r"""
Four drawings. The last one has **512 branch tips**. A loop that draws it needs
to know how many levels there are, where each branch starts, and the angle of
every one of the 1 023 segments.
""",
        ask="What is the *shortest* program that draws the right-hand tree, and why does it look so much like the definition of the tree?"),
   dict(img="figures/06-fractal-tree.svg", imgh=6.6, wide=True, credit="",
        body=r"""
```
Procedure TREE(x, y, angle, length, depth)
If depth = 0
      then return                                    # base case
draw a segment from (x, y) at angle, of length; its end is tip
TREE(tip, angle − 25°, 0.72 · length, depth − 1)
TREE(tip, angle + 25°, 0.72 · length, depth − 1)
```

- A tree **is** a segment with two smaller trees on top; the code says exactly that.
- Two recursive calls per level give $2^{\text{depth}-1}$ tips, but the **stack** is
  only `depth` frames deep: exponential work, linear memory.
""",
        uses="§2 base case and recursive case · §4 the program stack · §7 tree recursion versus linear recursion"),
   r"""
**Source.** The classic "fractal tree" (Mandelbrot 1982 popularized the family);
this one is drawn by `tools/genexamples_figs.py` with the procedure shown, so
the picture *is* the program's output.

**Facts.** Depth 10: $2^{9} = 512$ tips, $2^{10} - 1 = 1\,023$ segments. Branch
length factor 0.72, angle ±25°. Change the two constants and you get a
different species, a nice thing to show live in the practical part.

**How to present.** Open with the four panels and the "512 tips" number; ask
for the program. Close with the five lines and run through depth 2 by hand on
the board, drawing the stack beside it: at any moment only `depth` calls are
alive. This is the cleanest place to separate *number of calls* from *depth of
recursion*, which students conflate.

**Where it plugs in.** After factorial (linear recursion) and before or
alongside DFS (§6); DFS on a tree has the same shape.
""")

ex("X06-C", "You have more ancestors than there were people",
   "Thirty generations back, 2³⁰ ancestors, but the world held 400 million. What gives?",
   dict(img="figures/06-ancestors.svg", imgh=8.6, wide=True, credit="",
        body=r"""
Two parents, four grandparents, eight great-grandparents. Thirty generations
back, around the year 1275, that is **$2^{30}$ ≈ 1.07 billion** ancestors.
The world population at the time was about **400 million**.
""",
        ask="Where is the mistake? Write the recursive definition that produced $2^{30}$, and find the assumption that makes it wrong."),
   dict(img="figures/06-ancestors.svg", imgh=7.0, wide=True, credit="",
        body=r"""
- The definition: $\text{ancestors}(0) = 1$; $\text{ancestors}(g) = 2 \cdot
  \text{ancestors}(g-1)$. It is a correct recursion, for a **tree**.
- The assumption is that all $2^g$ slots hold *different* people. They do not:
  your family tree is a **directed acyclic graph** where the same person appears
  many times. This is **pedigree collapse**, and it is universal.
- Every recursive definition rests on the shape of its data. Tree recursion on a
  DAG **over-counts**, which is exactly why DFS marks visited nodes.
""",
        uses="§2 the three parts of a recursive definition · §6 depth-first search and the visited mark · §8 dynamic programming: don't recompute a shared subproblem"),
   r"""
**Source.** Pedigree collapse: Shoumatoff, *The Mountain of Names* (1985).
Chang (1999) showed that in a randomly mating population the most recent
common ancestor of everyone alive lies only about $\log_2 n$ generations back.
Population around 1275: McEvedy & Jones, *Atlas of World Population History*,
roughly 400 million.

**Facts.** $2^{30} = 1\,073\,741\,824$. Generation length about 25 years, so 30
generations is about 750 years. The recursion is right; the *model* (a tree) is
wrong.

**How to present.** Open with the doubling table and the population line; the
contradiction is obvious and the diagnosis is not. Close by drawing a small
family graph where two cousins marry: one grandparent pair appears twice in the
grandchildren's tree. Then the connection: DFS keeps a *visited* set for this
reason, and dynamic programming (Fibonacci with memoization) is the same idea,
which is to count each shared subproblem once.

**Where it plugs in.** After the DFS slides or as the lead-in to dynamic
programming; it makes "overlapping subproblems" concrete before Fibonacci.
""")

# ===========================================================================
#  07  Sorting Algorithms
# ===========================================================================

ex("X07-A", "How the post office sorts 20 million letters a night",
   "No comparisons at all: sorting by postcode, one digit at a time.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
Deutsche Post sorts on the order of **20 million letters** a night by postcode,
far faster than any comparison between two letters could be made.
""",
        ask=r"Mergesort needs about $n \log_2 n \approx 5 \times 10^8$ comparisons for 20 million items. The machines do none. How?"),
   dict(img="figures/07-radix-postcodes.svg", imgh=8.6, wide=True, credit="",
        body=r"""
- **Radix sort:** put each letter in one of ten bins by its *last* digit, collect
  the bins in order, repeat for the next digit. After five passes the pile is
  sorted, and each pass is a **stable** counting sort.
- Cost $O(d \cdot n)$ with $d = 5$: **linear** in $n$. No two letters are ever
  compared; the digit is used directly as a bin index.
- This does not contradict the $n \log n$ lower bound: that bound is for
  *comparison* sorts. Knowing the keys are short digit strings is extra information.
""",
        uses="§3 stable sorting (each pass must be stable or the previous pass is undone) · §9 why sorting matters · the comparison lower bound"),
   r"""
**Source.** Radix sorting predates computers: Hollerith's tabulating equipment
sorted punched cards this way from the 1890 census on. Deutsche Post volumes:
about 50 million letters per working day (DHL Group annual reports); machine
throughput 30 000 to 40 000 per hour. Counting sort is the exam's `AC-09`.

**Facts.** LSD radix sort: $d$ passes of a stable bucket sort; $O(d(n + k))$
with $k = 10$. Stability of each pass is what makes the order of the earlier
digits survive; that is the link to §3.

**How to present.** Open with the volume figure and the lower-bound number;
ask how it can possibly be done. Close with the first pass on the figure, then
ask the room *why the pass must be stable*; let them discover that an unstable
second pass would scramble the first. This is the best available argument for
why stability is not a footnote.

**Where it plugs in.** After the comparison-based sorts and the lower bound
(§9 of the transcript), as the "unless you know more" coda.
""")

ex("X07-B", "Can you sort 8 things in 10 comparisons?",
   "A colleague claims a sorting algorithm that beats every known one. Prove them wrong without seeing it.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
Selection sort needs 28 comparisons for 8 elements; mergesort about 17. A
colleague says they have a comparison-based algorithm that sorts **any 8
elements in at most 10 comparisons**.

You have not seen the code. You do not need to.
""",
        ask="What is the smallest number of comparisons that *any* algorithm needs in the worst case for 8 elements, and how can you know that about algorithms nobody has written yet?"),
   dict(img="figures/07-decision-tree.svg", imgh=8.4, wide=True, credit="",
        body=r"""
- A comparison sort is a **decision tree**: each comparison is a branch, each
  leaf a final ordering. To sort correctly it needs a leaf for **every** one of
  the $n!$ possible orderings.
- A binary tree with $n!$ leaves has depth at least $\log_2 n!$. For $n = 8$:
  $\log_2 40\,320 = 15.3$, so **at least 16 comparisons** in the worst case.
- Ten is impossible; **16 is achievable** (it is the known optimum for $n = 8$).
  In general $\log_2 n! \approx n \log_2 n$: mergesort is within a constant of optimal.
""",
        uses="§2 the formal sorting problem · §5 divide and conquer · §6 mergesort · the comparison lower bound argument in §9"),
   r"""
**Source.** Knuth, *TAOCP* vol. 3, §5.3.1 (minimum-comparison sorting). The
optimum $S(8) = 16$ is known exactly; the Ford–Johnson algorithm achieves it.
The figure draws the full decision tree for $n = 3$ (six leaves, depth 3), which
is small enough to see the argument.

**Facts.** $8! = 40\,320$; $\lceil \log_2 40\,320 \rceil = 16$. For $n = 3$:
$\lceil \log_2 6 \rceil = 3$. Stirling: $\log_2 n! = n\log_2 n - 1.44n + O(\log n)$.

**How to present.** Open with the claim; someone will say "you'd have to test
it". Close with the decision tree for three elements on the board, count leaves,
and generalize. The rhetorical point is strong and worth stating: this is a
statement about *every algorithm that could ever be written*, proved on one
slide. Session 9 builds a whole theory of such statements.

**Where it plugs in.** After mergesort, at the lower-bound slide of the main
deck; pairs with X07-A, which shows how the bound is *escaped*.
""")

ex("X07-C", "The median of a billion salaries, without sorting",
   "You only need the middle value; sorting all of them is work you did not ask for.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
A ministry wants the **median** income across a billion records. The obvious
plan: sort, take the middle element. On one machine that is roughly $10^9 \times
30 = 3 \times 10^{10}$ comparisons and a full copy of the data.

But the median is *one number*. The other 999 999 999 sorted positions are
thrown away.
""",
        ask="Is there a way to find the $k$-th smallest element without putting all the others in order? What in this session's toolkit gets you halfway?"),
   dict(img="figures/07-quickselect.svg", imgh=8.6, wide=True, credit="",
        body=r"""
- **Quicksort's PARTITION** puts the pivot in its final position $q$ and every
  smaller element to its left. If $q$ is the position you want, you are done.
- Otherwise recurse into **only the side that contains position $k$**; the
  other side never needs sorting. This is **Quickselect** (Hoare, 1961).
- Expected cost $n + n/2 + n/4 + \cdots = O(n)$: one pass's worth, not
  $n \log n$. Worst case is still $O(n^2)$, from the same bad pivots as quicksort.
""",
        uses="§5 divide and conquer · §7 quicksort and the PARTITION procedure · session 8: the geometric series that makes it linear"),
   r"""
**Source.** Hoare, C. A. R. (1961), "Algorithm 65: Find". CLRS §9.2. The trace
in the figure is produced by running Lomuto partition on `[38, 12, 71, 25, 56,
90, 44, 17, 63]`; the median found is 44 in five partitions.

**Facts.** Expected comparisons about $3.4n$ for the median. The worst case is
avoidable with median-of-medians (Blum et al. 1973), which is $O(n)$
deterministically; mention it, do not teach it.

**How to present.** Open with the "one number, a billion sorted for nothing"
framing. Close by pointing at the PARTITION slide of the main deck and asking
what happens if you *only recurse on one side*; the figure then shows the
shrinking active region. The geometric-series argument is a preview of session
8 and worth doing on the board: $n(1 + 1/2 + 1/4 + \ldots) < 2n$.

**Where it plugs in.** Immediately after the quicksort slides; it is
quicksort with one recursive call removed, which is also a good exercise.
""")
