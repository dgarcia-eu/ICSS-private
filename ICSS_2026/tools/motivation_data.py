#!/usr/bin/env python3
"""Motivating examples for the ICSS 2026 decks (sessions 2-12).

Three candidates per deck. Each has:
  title  short name, used as the slide title and the transcript sub-heading
  pitch  one line for the selector file (MotivatingExamples.md)
  slide  the body of the deck slide, inserted after the Overview slide
  text   the transcript section, inserted before section 1

`genmotivation.py` writes these into the decks and transcripts, wrapped in
`<!-- MOTIVATION:ID:BEGIN/END -->` markers; `pickmotivation.py` reads
MotivatingExamples.md and deletes the ones that were not chosen.

Keep `slide` short enough to fit one slide; `build.sh` will report overflow
if it does not. Section numbers in the texts refer to the sections of the
matching transcript in `Transcripts/`.
"""

M = {}


PARKED = {}     # examples taken out of a session, kept to be used later (not in the catalogue)


def park(mid, title, pitch, slide, text, note):
    PARKED[mid] = dict(title=title, pitch=pitch, slide=slide.strip("\n"),
                       text=text.strip("\n"), note=note)


def add(mid, title, pitch, slide, text):
    M[mid] = dict(title=title, pitch=pitch,
                  slide=slide.strip("\n"), text=text.strip("\n"))


# ===========================================================================
#  Session 2 -- Information Coding
# ===========================================================================

add("M02-A", "Excel renamed one gene in five",
    "Spreadsheet autoformatting silently corrupted gene names in 20% of "
    "published genetics papers. What is the software actually storing?",
    r"""
::: {.motivation}
[Motivating example]{.label}
An audit of 3 597 published genetics papers found that **704 of them, one in
five, contained corrupted gene names.** The spreadsheet had read `SEPT2` as a
date and stored it as `2-Sep`; identifiers like `2310009E13` became
`2.31E+13`.
:::

:::: {.figures}
::: {.fq}
[20%]{.big}[of papers affected]{.cap}
:::
::: {.fq}
[0]{.big}[warnings shown]{.cap}
:::
::: {.fq}
[27]{.big}[genes renamed in 2020 so the software would stop breaking them]{.cap}
:::
::::

[What is a spreadsheet actually storing when it shows you `SEPT2`, and who decided?]{.ask}

::: {.source}
Ziemann, Eren & El-Osta, *Genome Biology* (2016); Bruford et al., *Nature Genetics* (2020)
:::
""",
    r"""
In 2016 three researchers did something nobody had thought to do: they
downloaded the supplementary spreadsheets of 3 597 published genetics papers
and checked them. In 704 of them, 19.6%, gene names had been silently changed.
The mechanism is mundane. Human gene symbols include `SEPT2` (Septin 2),
`MARCH1`, `DEC1` and `OCT4`. A spreadsheet opening a text file guesses what
each cell means, decides that `SEPT2` is a date, and stores the 2nd of
September of the current year; re-exported, the cell now reads `2-Sep`.
Identifiers like `2310009E13` are guessed to be scientific notation and become
`2.31E+13`, losing their digits entirely. Nothing failed, no warning appeared,
no cell turned red, and the file opened perfectly the next time. The
corruption is only visible if you know what the value was supposed to be. The
episode ended in a way that is worth pausing on: in 2020 the HUGO Gene
Nomenclature Committee, the body that names human genes, renamed 27 genes so
that spreadsheets would stop breaking them. `MARCH1` became `MARCHF1` and
`SEPT1` became `SEPTIN1`. The biology was adjusted to fit the software.

The bug is not really about spreadsheets. It is about a gap that opens
whenever data moves between systems: a file contains bytes, and bytes only
mean something under an interpretation. `SEPT2` is five characters, and
whether those characters are a gene, a date or a chemical formula is not in
the file. Some program has to decide, and here a program decided silently and
wrongly. Everything in this session is about closing that gap deliberately
rather than letting software guess. Section 3 asks what it means to store a
value at all, and why everything on a computer is ultimately a sequence of
bits. Section 9 is about characters specifically: `S`, `E`, `P`, `T` and `2`
are numbers before they are letters, and which numbers depends on an encoding
you can choose. Section 10 is about types, the machinery that a programming
language gives you to say that a column is text and must not be
reinterpreted, which is exactly what the spreadsheet lacked. The general
lesson to take from the session is that when a value changes and nothing
warns you, the problem is almost always that two pieces of software disagreed
about what the bytes meant. Recognizing that pattern is worth more than
memorizing any particular encoding.
"""
    )

add("M02-B", "Müller became MÃ¼ller",
    "A survey exported from one system and read in another silently splits "
    "categories. What is a text file, if the same bytes mean two things?",
    r"""
::: {.motivation}
[Motivating example]{.label}
You export 12 000 survey responses from one system and read them into another.
Names come back as `MÃ¼ller`, `Ã–sterreich`, `KÃ¶ln`. Your grouping by city now
has **two Cologne categories**, and every model silently drops the rows it
cannot match.
:::

- Nothing crashed. No error was raised. The file is "just text".
- The damage is in the **results**, not in the log.

[What *is* a text file, if the same bytes can mean two different things?]{.ask}

::: {.source}
Background: Spolsky, "The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode" (2003)
:::
""",
    r"""
The symptom is familiar to anyone who has moved data between systems. A
German survey exports cleanly, you open the file somewhere else, and every
non-ASCII character has turned into a small pile of punctuation: `Müller`
becomes `MÃ¼ller`, `Österreich` becomes `Ã–sterreich` and `Köln` becomes
`KÃ¶ln`. The corruption even has a name, *mojibake*, from the Japanese
文字化け, "character transformation". Here is what happened, in bytes. In
UTF-8, `ü` is stored as the two bytes `C3 BC`. If the reading program assumes
ISO-8859-1 instead, where every byte is one character, it reads `C3` as `Ã`
and `BC` as `¼`, and prints both. The bytes on disk never changed; only the
assumption about how to read them did.

This matters for research rather than for aesthetics because the damage is
statistical, not visual. A `GROUP BY city` now has `Köln` and `KÃ¶ln` as two
distinct categories, so a city is split in half and neither half looks
significant. A join against a reference table fails for exactly the rows that
contain umlauts, that is, disproportionately for certain regions and certain
names, which is a systematic and not a random loss. And nothing raises an
error, because both strings are perfectly valid strings. The bias runs along
a predictable line: ASCII covers unaccented English, and every name outside
it is the one at risk, so an encoding bug is rarely a uniform annoyance but a
small, silent and systematic exclusion of particular people from your
dataset.

Section 3 of this session establishes that everything stored is a number, and
that a convention maps numbers to meanings. Section 9 is this problem head
on: ASCII, why 128 characters were not enough, the code-page era in which the
same byte meant different letters in different countries, and how UTF-8
solved it by using more than one byte for the characters beyond ASCII. The
practical rule you should leave with is to always state the encoding
explicitly when you read or write a file, with `encoding="utf-8"`, and never
to let a program guess. Guessing is what produced every example above.
"""
    )

add("M02-C", "The index that lost half its value",
    "The Vancouver Stock Exchange index drifted from 1000 to 525 in 22 months "
    "through truncation alone. Why can't a computer store 0.1?",
    r"""
::: {.motivation}
[Motivating example]{.label}
The Vancouver Stock Exchange index opened at **1000.000** in January 1982 and
was recomputed after every trade. By November 1983 it read **524.811**, while
the shares it tracked had risen. Nothing was wrong with the market: each
recomputation **truncated** the fourth decimal instead of rounding, thousands of
times a day.
:::

:::: {.figures}
::: {.fq}
[1000.000]{.big}[at launch, Jan 1982]{.cap}
:::
::: {.fq}
[524.811]{.big}[displayed, Nov 1983]{.cap}
:::
::: {.fq}
[1098.892]{.big}[true value, once recomputed]{.cap}
:::
::::

[Why can a computer not store 0.1 exactly, and what does that cost after a million additions?]{.ask}

::: {.source}
Toronto Star, 29 Nov 1983; discussed in Higham, *Accuracy and Stability of Numerical Algorithms*
:::
""",
    r"""
The Vancouver Stock Exchange launched a new index in January 1982 at a value
of 1000.000, recomputed after every trade, some 3 000 times a day. Over the
next 22 months the index fell steadily, reaching 524.811, even though the
shares it tracked had on the whole gone up. Analysts looked for an economic
explanation and did not find one, because there was none. Each recomputation
kept three decimal places by truncating the fourth rather than rounding it,
and truncation is not a symmetric operation: it always removes value and
never adds it. A loss of at most 0.001 per calculation, repeated 3 000 times
a day for 22 months, is roughly 20 index points a month. When the index was
recomputed correctly in November 1983 it jumped overnight from 524.811 to
1098.892, more than doubling.

Two things make this a good story for a social scientist rather than for a
programmer. First, the error was invisible at every individual step. No
single calculation was wrong by an amount anyone would notice, and the failure
lives entirely in the accumulation, which is exactly the regime that empirical
work operates in: we do not add two numbers, we add a million. Second, the
error was systematic and not random. Had the fourth decimal been rounded, the
errors would have been roughly symmetric and would largely have cancelled,
while truncation made every error point the same way. This is precisely the
distinction between noise, which averages out, and bias, which does not, and
it is the reason why numerical mistakes in analysis code are dangerous in a
way that measurement noise is not.

The deeper point of the session is that computers cannot store most decimal
numbers exactly. Section 7 develops the IEEE 754 standard, in which numbers
are stored as a sign, an exponent and a fixed number of significand bits,
which means that only dyadic rationals, fractions with a power of two
underneath, are exact; `0.1` is not one of them, and it is stored as
`0.100000001490116…`. Section 8 is about what that costs: why `0.1 + 0.2 !=
0.3`, why comparing floats with `==` is unreliable, and why money and counts
belong in exact types rather than in floats. The rule to carry out of the
session is that every floating-point operation rounds, and rounding errors
accumulate. Whether they cancel or compound depends on whether they are
symmetric, which is a design choice someone makes, sometimes without
noticing.
"""
    )

# ===========================================================================
#  Session 3 -- Data Structures
# ===========================================================================

add("M03-A", "Two million respondents, and one duplicate",
    "Finding duplicates in a panel: 2 × 10¹² comparisons the obvious way, "
    "two seconds with the right structure.",
    r"""
::: {.motivation}
[Motivating example]{.label}
Your panel has **2 million** responses and you need to find the duplicates. The
obvious approach compares every response with every other: about
**2 × 10¹² comparisons**, hours to days on a laptop. One pass with the right
data structure does it in **seconds**.
:::

:::: {.figures}
::: {.fq}
[2 × 10¹²]{.big}[comparisons, comparing every pair]{.cap}
:::
::: {.fq}
[2 × 10⁶]{.big}[operations, with a hash set]{.cap}
:::
::: {.fq}
[10⁶×]{.big}[less work, same answer]{.cap}
:::
::::

[Why is "have I seen this before?" nearly free in one structure and hopeless in another?]{.ask}
""",
    r"""
Deduplication is the least glamorous task in empirical research and one of
the most common. Two million responses have come in, some people answered
twice, and you need to find them before anything else happens. The direct
translation of the question into code compares every response with every
other one:

```
For each response i:
      For each response j after i:
            If i and j match, then record a duplicate
```

That is $\binom{2\,000\,000}{2} \approx 2 \times 10^{12}$ comparisons, two
million million. Even at ten million comparisons a second this is over two
days, and in an interpreted language it is considerably worse. Now the same
task with a hash set:

```
seen ← ∅
For each response r:
      If r.key ∈ seen
            then record a duplicate
            else add r.key to seen
```

This looks at each response once: two million operations, a couple of
seconds. Nothing clever happened to the comparison itself. What changed is
that the second version never searches; it computes, from the value itself,
where that value would be stored, and looks only there.

That single move, to stop searching and start indexing, is the most valuable
habit this session teaches, and it recurs in every later session. Section 8
develops hash tables: the hash function that turns a key into a position, why
collisions happen, and how they are resolved. It also explains a caveat that
matters, namely that $O(1)$ is an average and that a bad hash function can
degrade the whole structure into a linked list. Section 2 is the contrast
case, since arrays give you $O(1)$ access by position, which is a different
thing from access by value, and confusing the two is what produces the nested
loop above. Section 6 covers binary search trees, which give you something a
hash table cannot, the keys in order, so that you can ask for the smallest or
for everything in a range. The framing to leave with is that a data structure
is not a container. It is a decision about which questions will be cheap,
and choosing one is choosing which analyses you will be able to run.
"""
    )

add("M03-C", "Six thousand rows, and the answer in thirteen steps",
    "Codebook lookups: 6,000 comparisons scanning, 13 with binary search, "
    "and what you have to give up to get it.",
    r"""
::: {.motivation}
[Motivating example]{.label}
A codebook has **6,000** entries and your script looks up a code for each of
**40 million** observations. Checking the entries one at a time costs
**6,000 comparisons** per lookup. If the codebook is sorted, it costs **13**.
:::

:::: {.figures}
::: {.fq}
[6,000]{.big}[comparisons, scanning the list]{.cap}
:::
::: {.fq}
[13]{.big}[comparisons, binary search]{.cap}
:::
::: {.fq}
[460×]{.big}[less work, but the list must be sorted]{.cap}
:::
::::

[What do you give up to get that, and what happens when the codebook changes every day?]{.ask}
""",
    r"""
Recoding is the other unglamorous constant of empirical work. You have 40
million observations carrying an occupation code, a region code or a product
number, and a codebook of 6,000 entries that says what each code means. The
straightforward loop checks the codebook entries one after another until it
finds a match. On average that is half the codebook, 3,000 comparisons, and
6,000 in the worst case; times 40 million observations, it is on the order of
$10^{11}$ comparisons, which is an overnight job. If the codebook is sorted,
binary search applies: look at the middle entry, decide whether the target is
in the left or in the right half, and repeat. Each step halves the range, so
the number of steps is $\lceil \log_2 6\,000 \rceil = 13$, and the whole recode
drops from $10^{11}$ comparisons to about $5 \times 10^8$, from overnight to
under a minute.

That is a factor of 460 for free, except that it is not free, and the
interesting part of this session is the bill. The list has to be sorted, which
costs something up front, and session 7 puts a number on it. It has to stay
sorted, and inserting a new code into a sorted array means shifting everything
after it, which is $O(n)$ per insertion; if the codebook is rebuilt daily, this
may cost more than it saves. And it has to be an array, not a linked list,
because binary search needs to jump straight to the middle element, which
requires $O(1)$ access by position; following pointers to the middle of a
linked list is $O(n)$, and the entire advantage evaporates.

Section 2 of this session covers arrays and why constant-time indexing exists
at all, since the address of element $k$ is computed and not searched for.
Section 3 covers linked lists and the exact trade-off above, cheap insertion
without random access. Section 6 develops binary search trees, which are the
answer when you need both fast search and cheap insertion, the structure that
gives up a little of each to avoid having to choose. The habit to build is
that whenever something is fast, you ask what was given up for it. There is
no structure that is best at everything, and the exam questions of this
course are mostly about naming the trade.
"""
    )

# ===========================================================================
#  Session 4 -- Software
# ===========================================================================

add("M04-A", 'The app that leaked 13,000 photo IDs',
    'Tea stored 13,000 selfies and photo IDs where anyone could download them: an obvious requirement that nobody wrote down or tested.',
    r"""

::: {.motivation}
[Motivating example]{.label}
**Tea**, a US app where women warn each other about men they date, asked every
new user for a selfie and a photo ID to prove she was a woman. In July 2025
someone posted the address of the storage that held them: **no login, no
access rule.** Anyone could download everything.
:::

:::: {.figures}
::: {.fq}
[72,000]{.big}[images downloaded]{.cap}
:::
::: {.fq}
[13,000]{.big}[selfies and photo IDs]{.cap}
:::
::: {.fq}
[1 million+]{.big}[private messages, in a second leak]{.cap}
:::
::::

[*"Only moderators may see the ID photos"* was obviously required. Why did nothing enforce it, and which test would have caught it?]{.ask}

::: {.source}
TechCrunch and CNN, 26 July 2025; 404 Media. Many blamed vibe coding; Tea says the code predates 2024.
:::
""",
    r"""
Tea is a US app on which women share warnings about men they have dated. To
keep men out, it asked every new user to upload a selfie and, for many, a
photo of an identity document, which moderators used to verify the account.
In July 2025 a user of the forum 4chan posted the address of the online
storage, a Firebase bucket, where these images were kept. The storage had no
login and no access rule: anyone who knew the address could list and download
everything in it. About 72,000 images were copied and spread, among them
around 13,000 selfies and photo IDs, and the rest from posts, comments and
direct messages. Days later, a second problem exposed more than a million
private messages, and the company disabled its messaging feature.

Many people blamed vibe coding, the practice of building software by
prompting an AI tool and accepting what it produces; the person who first
leaked the data said so too. The company says the exposed data came from a
system built before February 2024. How the code was written does not change
the lesson, which is about requirements and tests rather than about who typed
the code. "Only moderators may see the identity photos, and only while they
verify an account" is a requirement that anyone at the company would have
agreed with if asked. Nobody wrote it down as part of what the system had to
do, so nothing in the system enforced it. And a single test, "try to download
an ID photo without logging in", would have failed on the first day.

Section 6 of this session is about requirements, including the ones that are
not about what the program computes but about how it must behave: security,
privacy, safety. Section 7 is about the tests that check them. For research
software the analogue is a script that produces the right table and also
writes the respondents' names into a file that ends up public.
"""
    )


add("M04-D", 'The 5 millimeters nobody could move',
    "Nokia's Symbian grew to 20 million lines in one phone, and nobody could find the code to move a screen element by 5 mm.",
    r"""
::: {.motivation}
[Motivating example]{.label}
In the 2000s, **Symbian**, the system of Nokia's phones, ran most of the world's
smartphones. In 2010 a former Nokia design executive told how his team wanted to
move one element of a phone's screen up by 5 mm: *"We can't find the piece of code
that could shift it up 5mm."*
:::

:::: {.figures}
::: {.fq}
[20 million]{.big}[lines of code in one phone]{.cap}
:::
::: {.fq}
[40 million]{.big}[lines of Symbian released as open source, 2010]{.cap}
:::
::: {.fq}
[11 million]{.big}[lines of Android at the time]{.cap}
:::
::::

[Nobody wrote this code to be unchangeable. What makes working code impossible to change, and what keeps it changeable?]{.ask}

::: {.source}
Juhani Risku in The Register, 22 July 2010; All About Symbian, 4 February 2010. In 2011 Nokia replaced Symbian with Windows Phone.
:::
""",
    r"""
In the 2000s, Symbian, the operating system of Nokia's phones, ran most of the
world's smartphones. It had grown for more than a decade, feature by feature
and phone by phone, and every new model added code to it. In 2010 Juhani
Risku, a former design executive at Nokia, told the technology magazine The
Register what this meant in practice. His team wanted to move one element on
the screen of a Nokia phone up by 5 millimeters, and could not: "We can't find
the piece of code that could shift it up 5mm. There's 20 million lines of code
in the phone, it's impossible." When Symbian was released as open source the
same year, its own foundation estimated the code at about 40 million lines,
against about 11 million for Android. In 2011 Nokia gave up on Symbian and moved
its smartphones to Windows Phone.

Nobody wrote this code to be unchangeable. Every line was added for a reason,
and every addition worked. What was missing was what keeps a large program
changeable: parts with one clear responsibility, so that a change to the screen
layout touches one place; documentation that says what each part does; and
tests that tell you a change has not broken something else. Without them, the
safest thing to do with code nobody understands is to leave it alone, and the
program can only grow.

Section 4 of this session presents object-oriented programming as a tool for
exactly this problem: large programs maintained by many people for many years.
Section 5 places writing code inside software engineering, where maintenance is
a stage of its own, and section 7 is about the tests that make changes safe.
For research code the analogue is the analysis script that grew over a whole
PhD, and that nobody, including its author, dares to touch the week before
submission.
"""
    )

# ===========================================================================
#  Session 5 -- Algorithms
# ===========================================================================

add("M05-A", "Six handshakes, and how you would check",
    "Milgram needed volunteers and postage; Facebook measured the same thing "
    "over 1.59 billion people. What is the procedure?",
    r"""
::: {.motivation}
[Motivating example]{.label}
Milgram's 1967 experiment asked people in Nebraska to get a letter to a stranger
in Boston by passing it only to someone they knew personally. The chains that
arrived had a median of **five intermediaries**. Fifty years later the same
question was answered directly over **1.59 billion people**, giving **3.57**.
:::

:::: {.figures}
::: {.fq}
[5.2]{.big}[Milgram, 1967: mean over the 64 letters that arrived]{.cap}
:::
::: {.fq}
[3.57]{.big}[Facebook, 2016: 1.59 × 10⁹ people]{.cap}
:::
::::

[Milgram needed volunteers and postage. What *procedure* answers the same question from the network itself?]{.ask}

::: {.source}
Milgram, *Psychology Today* (1967); Edunov, Diuk, Filiz, Bhagat & Burke, Facebook Research (2016)
:::
""",
    r"""
In 1967 Stanley Milgram gave letters to volunteers in Nebraska and Kansas
addressed to a stockbroker in Boston, with one rule: you may only forward the
letter to someone you know personally, on a first-name basis. Of 296 chains
started, 64 arrived, with a mean length of 5.2 intermediaries and a median of
about five. "Six degrees of separation" comes from this, by way of a later
play. The experiment is famous, and it is also a fairly desperate way to
measure a graph. It is slow, it is expensive, and it observes only the chains
that completed, a severe selection problem, since a chain is more likely to
arrive when the path is short. In 2016 the question was answered a different
way. Given the Facebook friendship graph, 1.59 billion people and hundreds of
billions of edges, the average distance between two randomly chosen people
was computed directly: 3.57.

Nothing about the second study is conceptually harder than the first. What
changed is that instead of asking people to walk the network, we walked it
ourselves: start at a person, look at all their friends, who are at distance
1, look at all of their friends who have not been seen yet, who are at
distance 2, and continue until everyone reachable has been seen. That is
breadth-first search, and this session builds it up properly. It is worth
noticing what has to be pinned down before it is an algorithm at all: what
exactly a step is, namely to look at all the friends of the current person;
which person we look at next, where the answer is a queue, and choosing a
stack instead gives a different algorithm with a different answer; how we
avoid going round in circles, by marking what has been seen; and when we stop,
and how we know that we stop at all. Answering those four questions is the
difference between a good idea and a procedure you can hand to a machine.

Section 2 of this session defines the properties an algorithm must have, and
shows why finiteness and definiteness are not pedantry, since each rules out a
specific way of writing something that looks like a procedure but is not.
Sections 3 to 5 cover pseudocode and flowcharts, that is, how to write a
procedure down so that another person, and eventually a machine, can execute
it identically. Sections 7 to 9 develop graphs, their representation and
breadth-first search, ending with exactly the computation described above.
The transferable point is that a research question becomes computable at the
moment you can say, without ambiguity, what to do next. Most of the work is
in getting to that sentence.
"""
    )

add("M05-B", "Whose contacts, within two steps?",
    "Contact tracing as a graph search: thousands of people, answered in "
    "seconds, and every step of the recipe has to be pinned down.",
    r"""
::: {.motivation}
[Motivating example]{.label}
A case is confirmed on Monday. Public health needs everyone this person met, and
everyone **those** people met, but not the whole population, and not next week.
On the contact graph of a mid-sized city that is thousands of people, and it
must be answered in **seconds**.
:::

- "Everyone within two steps" is easy to say and useless until you specify
  *which person you look at next* and *how you know you are finished*.

[What is the exact recipe, and how do you keep from going round in circles?]{.ask}
""",
    r"""
Contact tracing is a graph problem with a deadline. People are vertices, a
recorded contact is an edge, a case is confirmed, and the question is who is
within one step and who is within two. Stated in English this sounds
finished, but it is not, because handing "find everyone within two steps" to
a machine requires answering questions that the English sentence hides. Which
person do you examine next? If you take the most recently discovered person
each time, you dive down one long chain of contacts before ever looking at
the second friend of the original case, and you will report people at
distance 5 before people at distance 2; if you take the earliest discovered
person, you finish all of distance 1 before starting distance 2. Same graph,
same edges, and completely different behavior: the first is depth-first, the
second is breadth-first, and only the second answers the question asked. How
do you avoid loops? Contact graphs are full of cycles, since A met B, B met C
and C met A, and without marking who has already been seen the procedure
never terminates. How do you know the distance? Not by looking at a person,
but by recording it when you first reach them: each newly discovered person
is at one more step than the person who led you to them. And when do you
stop? Either when the queue is empty, or, here, as soon as you would move
beyond distance 2, which is what makes this fast enough to be useful. The
graph may have millions of vertices, and you touch only the neighborhood you
need. That the answer arrives in seconds rather than hours is a property of
the procedure, not of the hardware: breadth-first search examines each vertex
once and each edge once, so the cost is proportional to the part of the
network you actually reach.

Section 2 of this session is about what makes something an algorithm.
Definiteness, that no step may be ambiguous, and finiteness, that it must
stop, are exactly the two properties that the English sentence lacked.
Section 8 is about representing a network so that "who did this person
meet?" is a cheap question, because the representation decides whether the
procedure is fast. Section 9 is about breadth-first search itself: the
queue, the colors that mark what has been seen, the distance and parent
records, and why it is correct. The exercise sheet and the exam both ask you
to run this by hand on a small graph, and doing so once is the fastest way to
see why each part of the recipe is there.
"""
    )

add("M05-C", "The network that would not fit",
    "84 million people: 7 × 10¹⁵ cells one way, a laptop's worth the other. "
    "Representation decides whether the study is possible.",
    r"""
::: {.motivation}
[Motivating example]{.label}
You want to store who is friends with whom among the **84 million** people in
Germany. Written as a table of everyone against everyone, that is
**7 × 10¹⁵ cells**, seven petabits at one bit each, more than most data centers
hold. Written the other way round it fits on a laptop and answers the same
questions.
:::

:::: {.figures}
::: {.fq}
[7 × 10¹⁵]{.big}[cells, as a matrix]{.cap}
:::
::: {.fq}
[8 × 10⁹]{.big}[friendships, as adjacency lists]{.cap}
:::
::: {.fq}
[~10⁶×]{.big}[smaller, same facts]{.cap}
:::
::::

[Same network, same questions. Why does the *representation* decide whether the study can happen?]{.ask}
""",
    r"""
Suppose you want to study the friendship network of Germany: 84 million
people, with perhaps a couple of hundred friends each. The most obvious
representation is a table with one row and one column per person, holding a 1
where two people are friends. This is an adjacency matrix, and it has a fatal
property: its size depends only on the number of people, never on the number
of friendships. For 84 million people that is $84\,000\,000^2 \approx 7 \times
10^{15}$ cells. At one bit each, an impossibly generous assumption, that is
roughly 875 terabytes, and the study is over before it starts. Now store, for
each person, only a list of the people they are actually friends with. This
is an adjacency list, and its size depends on the number of friendships,
about $84 \times 10^6 \times 200 / 2 \approx 8 \times 10^9$ of them, each
stored in the lists of its two endpoints. Large, but perfectly ordinary, and
it fits on a single machine. A factor of a million, from writing the same
facts down differently. The reason is that real social networks are sparse:
people have hundreds of friends, not eighty million, so the matrix is more
than 99.999% zeros and almost all of that storage records the absence of a
relationship, while the list records only what is there.

There is a genuine trade-off, and this is what makes it a design question
rather than an obvious choice. To ask whether $u$ and $v$ are friends, the
matrix looks at one cell, $O(1)$, while the lists scan the list of $u$,
$O(\deg u)$. To ask who the friends of $u$ are, the matrix scans a whole row,
$O(|V|)$, while the lists just read the list, $O(\deg u)$. And the space is
$O(|V|^2)$ for the matrix against $O(|V| + |E|)$ for the lists. The matrix
wins on the first question and loses on everything else, and the algorithms
of this session, breadth-first search, and depth-first search in the next,
need the second question over and over. So for the work we actually do, lists
win twice.

Section 8 of this session covers both representations, adjacency matrix and
adjacency list, with exactly this comparison. Section 9 shows why it matters
operationally: breadth-first search is $O(|V| + |E|)$ with lists and
$O(|V|^2)$ with a matrix, because finding the neighbors of a vertex is the
inner operation. The habit to take away, and it generalizes well beyond
graphs, is to ask how something is written down before asking how to compute
it. A surprising number of "this is computationally infeasible" conclusions
are really conclusions about a badly chosen representation.
"""
    )

# ===========================================================================
#  Session 6 -- Recursion
# ===========================================================================

add("M06-A", "How many people report to her?",
    "An org chart of unknown depth: a loop needs to know how many levels "
    "there are, and you don't.",
    r"""
::: {.motivation}
[Motivating example]{.label}
An organizational chart has a chief executive, division heads, department heads,
team leads and staff, and **nobody knows how deep it goes**, because it differs
by division. You are asked a simple question: how many people, in total, sit
below any given manager?
:::

- A loop over levels needs to know **how many levels** to go through.
- You don't. And the answer changes next month.

[How do you write a procedure that works without knowing in advance how deep the structure is?]{.ask}
""",
    r"""
Take an ordinary organizational chart. There is a chief executive; below her,
division heads; below them, departments, teams and staff. In some divisions
that is four levels, in others seven, and after the next reorganization
something else. Now answer a simple question: how many people in total sit
below a given manager? The instinct from session 4 is a loop. Add up the
direct reports, then add up their reports, then theirs, and written out it
becomes:

```
total ← direct reports
For each direct report:
      total ← total + their direct reports
      For each of those:
            total ← total + their direct reports
                  ...
```

The `...` is the problem. The nesting depth of the code has to match the
depth of the chart, which you do not know when you write the code, and which
is not even the same across the organization. You could write ten levels of
nesting and hope; it would be wrong for the eleventh, and unreadable at the
third. The way out is to notice something about the structure, not about the
code. The subtree of a manager is the manager plus the subtree of each direct
report, so the description of the whole refers to the same kind of thing as
its parts:

```
Procedure HEADCOUNT-BELOW(person)
Inputs:
      person: a node of the organizational chart
Result: the number of people below person
total ← 0
For each direct report r of person:
      total ← total + 1 + HEADCOUNT-BELOW(r)
return total
```

Four lines, no assumption about depth, and it is obviously correct once you
read it as a sentence: the number below me is, for each of my reports, that
person plus the number below them. The base case is hidden in plain sight,
because a person with no direct reports never enters the loop and returns 0,
and that is what stops the whole thing.

Section 2 of this session is about the parts of any recursive definition, a
base case that returns without recursing and a recursion case that moves
strictly closer to it; get either wrong and you get an infinite descent.
Section 4 is about the call stack, what the machine actually keeps while
those nested calls are outstanding, and why "recursion depth exceeded" is a
real limit rather than a theoretical one. Section 7 is about the types of
recursion, and tree recursion is exactly the shape above: one call per child
rather than one call in total. The reframing to take away is that recursion
is not a trick for writing loops differently. It is what you reach for when
the data is defined in terms of itself, and organizations, family trees, file
systems, comment threads and grammatical sentences all are.
"""
    )

add("M06-B", "The comment thread with no bottom",
    "Replies to replies to replies: when the data is defined in terms of "
    "itself, what should the procedure look like?",
    r"""
::: {.motivation}
[Motivating example]{.label}
A discussion thread has replies, replies to replies, and replies to those. To
count the posts, render the page, or measure how deep an argument went, something
has to walk the whole structure, and the structure is **defined in terms of
itself**:
:::

::: {.definition}
[A comment is]{.label}
a post, plus a list of **comments**.
:::

[When the *data* is defined in terms of itself, what should the *procedure* look like?]{.ask}
""",
    r"""
Online discussion is a standard object of study in computational social
science, and it has an awkward shape. A thread is not a list of posts. It is a
tree: a top-level post has replies, those replies have replies, and there is
no fixed limit. A heated exchange between two people can run forty levels
deep while the rest of the thread is flat. Look at how you would have to
define the data type: a comment consists of an author, a timestamp, some
text, and a list of comments. The definition uses the word it is defining.
That is not sloppiness; it is the honest description, and it is exactly why
loops sit badly on this data. Any question you want to ask has the same
self-referential shape. How many posts are in this thread? One, plus the
count in each reply. How deep does it go? One, plus the deepest of its
replies. How many distinct people are involved? This author, together with
the people involved in each reply. When did the argument end? The latest
timestamp among this post and all its replies. Each of these is a short
recursive procedure and a genuinely awkward loop. For example:

```
Procedure THREAD-DEPTH(comment)
Inputs:
      comment: a comment with a (possibly empty) list of replies
Result: the number of levels in the subtree rooted at this comment
If comment has no replies
      then return 1
best ← 0
For each reply r of comment:
      best ← max(best, THREAD-DEPTH(r))
return 1 + best
```

The principle worth generalizing is that when the structure of the data is
recursive, the procedure that walks it should be recursive too. The code then
has the same shape as the thing it describes, which is why recursive
solutions to recursive data are usually shorter and easier to convince
yourself are correct.

Section 2 of this session is about the base case and the recursion case.
Here the base case is a comment with no replies, and it is what guarantees
termination, provided that the thread really is a tree and not a cycle.
Section 4 is about the call stack and the practical limit it imposes: a
thread 40 000 levels deep would exhaust Python's default recursion limit of
about 1 000, which is a real constraint on real data. Section 7 distinguishes
tree recursion, one call per child, from linear recursion. The exercise sheet
asks you to write several of these procedures; do them by writing the
definition of the data first, and the procedure follows from it almost
mechanically.
"""
    )

add("M06-C", "The algorithm that is 2 300 years old",
    "Euclid's gcd, c. 300 BC, still the one your computer uses, and the "
    "cleanest illustration of what makes a recursion stop.",
    r"""
::: {.motivation}
[Motivating example]{.label}
Euclid's *Elements*, Book VII, around 300 BC, gives a procedure for the greatest
common divisor: **replace the larger number by its remainder against the
smaller, and repeat.** It is still the algorithm your computer uses today.
:::

::: {.example}
[gcd(270, 192)]{.label}
gcd(270, 192) → gcd(192, 78) → gcd(78, 36) → gcd(36, 6) → gcd(6, 0) = **6**
:::

[What makes this procedure *stop*? And what happens to a procedure that calls itself and forgets to?]{.ask}

::: {.source}
Euclid, *Elements*, Book VII, Propositions 1–2
:::
""",
    r"""
The oldest algorithm still in everyday use is about 2 300 years old. Euclid
gives it in Book VII of the *Elements*, in geometric language: to find the
greatest common measure of two magnitudes, repeatedly subtract the smaller
from the larger. In modern form, using remainders instead of repeated
subtraction,

$$\gcd(a, b) = \gcd(b,\ a \bmod b), \qquad \gcd(a, 0) = a.$$

Two lines, and they do something genuinely non-obvious: they find the largest
number dividing both, without factoring either. Run it on 270 and 192:

| Call | $a$ | $b$ | $a \bmod b$ |
|---|---|---|---|
| 1 | 270 | 192 | 78 |
| 2 | 192 | 78 | 36 |
| 3 | 78 | 36 | 6 |
| 4 | 36 | 6 | 0 |
| 5 | 6 | 0 | base case, return 6 |

Five calls, and the numbers collapse fast: 270, 192, 78, 36, 6. That speed is
not luck. Taking a remainder against $b$ produces something strictly less
than $b$, and it can be shown that two steps at least halve the larger
number, so the number of calls is logarithmic in the input, not linear. This
is the cleanest example in the course of the two things a recursion needs,
and it is worth naming them against this table. The first is a base case,
line 5 of the table: when $b = 0$, the procedure returns without calling
itself, and without it the recursion never ends. The second is progress
towards the base case: each call replaces $(a, b)$ with $(b, a \bmod b)$, and
$a \bmod b < b$, so the second argument strictly decreases and is never
negative. A strictly decreasing sequence of non-negative integers cannot go
on forever, so the base case is reached. That is a proof of termination, and
it is the argument you should be able to make for any recursion you write.
Drop either half and the failure is dramatic rather than subtle. A missing
base case, or a recursive call that does not shrink the problem, gives
infinite descent: each call pushes a frame onto the call stack, the stack
fills, and the program dies with `RecursionError: maximum recursion depth
exceeded`, which in Python happens after about 1 000 frames.

Section 2 of this session develops the base case and the recursion case as
the two obligations, with termination arguments like the one above. Section
4 explains the call stack, why 1 000 is the number, what a stack frame
contains, and why it is the same stack you met in session 5. Section 7
covers linear recursion, of which Euclid is the textbook case, and its
conversion to a loop. Euclid returns in the exercise sheet and has been a
full exam question. Being able to run it by hand and to say why it stops is
the whole of what is asked.
"""
    )

# ===========================================================================
#  Session 7 -- Sorting Algorithms
# ===========================================================================

add("M07-A", "Sorted by region, then by age, and the regions came apart",
    "Two sorting algorithms give the same sorted order and different results. "
    "The property that separates them is stability.",
    r"""
::: {.motivation}
[Motivating example]{.label}
You sort a respondent table by **region**, then sort the same table by **age**
to inspect the age distribution. The regions, which were in a deliberate order,
come back shuffled, because the second sort was allowed to move equal-aged rows
past one another. Nothing warned you. The appendix tables are wrong.
:::

- Both sorts produced a **correctly sorted** table.
- Only one of them preserved the work of the first.

[Two algorithms, the same sorted order, different results. What property separates them, and which do you have?]{.ask}
""",
    r"""
Here is a bug that produces no error, no warning and a plausible-looking
table. You have a respondent file. You sort it by region, because the report
is organized that way. Then you sort the same table by age, to look at the age
distribution. You expect that within each age the regions are still in the
order you put them, but they are not; they come back scrambled. Both sorts
were correct, and the table really is sorted by age. The difference is a
property called stability: a sorting algorithm is stable if elements that
compare equal keep their original relative order. Sorting by age, every
34-year-old compares equal to every other 34-year-old. A stable algorithm
leaves them in the order they arrived, which, after the first sort, is region
order; an unstable algorithm is free to put them in any order, and generally
does. This is not a curiosity. It is the mechanism behind a standard
technique, sorting by several keys one at a time, from the least important to
the most important. Sort by region, then by age, and with a stable sort you
have a table ordered by age and, within age, by region, without ever writing a
compound comparison. With an unstable sort you have silently thrown the first
sort away.

Which algorithms are which, among those of this session? Selection sort is
not stable, because swapping a distant minimum into place jumps it over equal
elements. Mergesort is stable, because on a tie the merge step takes from the
left half first. Quicksort is not stable, because partitioning swaps across
the array. Heapsort is not stable either, because moving the last element to
the top of the heap reorders equal keys. Stability is not a property that an
algorithm advertises; it is a property that someone had to design in, and in
the case of mergesort it hangs on a single character, the $\le$ in the merge
comparison, so it can be lost by a change that looks purely cosmetic.

Section 4 of this session traces selection sort by hand, sections 6 and 7
mergesort and quicksort, and section 8 heapsort, so that you can see where an
element moves and why stability holds or fails. The habit to build is that
when a library offers you a `sort`, you find out whether it is stable before
relying on a previous sort surviving it. Python's `sorted()` is stable and
guarantees it; many others are not, and most do not say.
"""
    )

add("M07-B", "Two seconds, or fourteen hours",
    "A million records: 5 × 10¹¹ comparisons one way, 2 × 10⁷ the other. Both "
    "algorithms are correct.",
    r"""
::: {.motivation}
[Motivating example]{.label}
A million records. **Selection sort** compares every element against every
other: about **5 × 10¹¹** comparisons. **Mergesort** halves the problem
repeatedly: about **2 × 10⁷**. At ten million comparisons a second, that is the
difference between **fourteen hours** and **two seconds**.
:::

:::: {.figures}
::: {.fq}
[5 × 10¹¹]{.big}[comparisons, selection sort]{.cap}
:::
::: {.fq}
[2 × 10⁷]{.big}[comparisons, mergesort]{.cap}
:::
::: {.fq}
[25 000×]{.big}[fewer, same result]{.cap}
:::
::::

[Both are correct. What is it about the *shape* of one procedure that makes it collapse at scale?]{.ask}
""",
    r"""
Sorting a million records. Two algorithms, both correct, both easy to write.
Selection sort finds the smallest element, puts it first, finds the smallest
of the rest, puts it second, and so on. Finding each minimum means scanning
everything that is left, so the total number of comparisons is

$$(n-1) + (n-2) + \cdots + 1 = \frac{n(n-1)}{2} \approx 5 \times 10^{11}
\quad \text{for } n = 10^6.$$

Mergesort splits the array in half, sorts each half, and merges the two
sorted halves. Halving $10^6$ takes about 20 steps to reach single elements,
and each of those 20 levels does about $10^6$ units of merging work, so the
total is

$$n \log_2 n \approx 10^6 \times 20 = 2 \times 10^7.$$

At ten million comparisons a second, that is about fourteen hours against two
seconds. What is worth noticing is where the difference comes from, because it
is not about efficiency in any ordinary sense. Both algorithms do simple work
in their inner loop, and neither is written badly. The difference is
structural. Selection sort throws away everything it learns: having scanned
the entire array to find the minimum, it knows a great deal about the relative
order of the remaining elements, and then discards all of it and scans again.
Mergesort keeps its work: once two halves are sorted, merging them uses that
order, and it never compares two elements whose relative position is already
implied. That is why the gap widens with $n$ rather than staying constant. At
$n = 100$ the ratio is about 7, at $n = 10^6$ it is 25 000, and at $n = 10^9$
it is 17 million. An algorithmic difference is not a constant factor you can
buy your way out of: no amount of faster hardware closes it, and session 12
shows that no amount of parallelism does either.

Section 4 of this session covers selection sort and the summation above,
whose arithmetic is worth doing once by hand. Section 6 covers mergesort and
the divide-and-conquer idea: halving gives $\log n$ levels, and $\log n$ is a
very small number, since $\log_2$ of a billion is 30. Session 8 turns this
comparison into notation and shows how to count the steps of both algorithms.
For now the point is the intuition: the question is never how fast an
algorithm is on your data, but what happens when the data gets ten times
bigger.
"""
    )

add("M07-C", "Why sort at all?",
    "Sorting is an investment: worthless for one lookup, essential for forty "
    "million. How do you work out whether it pays?",
    r"""
::: {.motivation}
[Motivating example]{.label}
A codebook lookup costs **13** comparisons if the list is sorted and **6 000** if
it is not. But sorting the codebook costs something too. With **one** lookup,
sorting is wasted effort. With **forty million**, it is the only thing that makes
the job possible.
:::

:::: {.figures}
::: {.fq}
[1]{.big}[lookup: don't sort, you would pay more than you save]{.cap}
:::
::: {.fq}
[25]{.big}[lookups: the break-even point]{.cap}
:::
::: {.fq}
[40 × 10⁶]{.big}[lookups: sorting is the whole difference]{.cap}
:::
::::

[Sorting is an **investment**. How do you work out whether it pays?]{.ask}
""",
    r"""
Sorting is almost never the goal. It is something you do so that the next
operation is cheap: searching, merging, deduplicating, finding a median,
detecting a range. So the question is never whether something should be
sorted in the abstract. It is whether the sort costs less than what it saves,
and we can put numbers on it. Take a codebook of $m = 6\,000$ entries and $q$
lookups against it. Unsorted, each lookup scans, costing about $m/2 = 3\,000$
comparisons, for a total of about $3\,000\,q$. Sorted, the sort costs about
$m \log_2 m \approx 6\,000 \times 12.6 \approx 76\,000$ comparisons, once, and
each lookup then costs $\log_2 m \approx 13$, for a total of about $76\,000 +
13q$. Sorting wins when $76\,000 + 13q < 3\,000q$, that is, when $q > 25$ or
so. Twenty-five lookups. After that, sorting is free money, and at $q = 40$
million the sorted version does about $5 \times 10^8$ comparisons against
$1.2 \times 10^{11}$, a factor of 240.

The break-even calculation is the transferable skill here, and it
generalizes well past sorting. Any preprocessing step, whether sorting,
building an index, building a hash table or caching a result, has the same
structure: a fixed cost up front and a lower cost per query afterwards. You
are choosing between two lines with different intercepts and different
slopes, and the only question is where they cross and on which side of the
crossing your workload sits. The cases where sorting does not pay are worth
knowing too. With one query, a single linear scan is $O(m)$ while sorting
first is $O(m \log m)$, so you have paid a $\log m$ factor for nothing. When
the data changes constantly, keeping a sorted array sorted costs $O(m)$ per
insertion, and if the codebook is rebuilt daily you pay the sort daily. With
streaming data you cannot sort what has not arrived yet. And when the data
does not fit in memory, sorting becomes a much more expensive external
operation.

Sections 4 to 8 of this session give the costs on the left-hand side of that
inequality, what each sorting algorithm actually costs and why $n \log n$ is
achievable; the binary search of session 3 gives the right-hand side, and
session 8 gives the notation for reasoning about both at once. The exam has
asked a version of this question, when sorting is less efficient than
processing unsorted data, and the answer is always the break-even argument,
not a rule.
"""
    )

# ===========================================================================
#  Session 8 -- Time Complexity
# ===========================================================================

add("M08-A", "It ran fine on the pilot",
    "Four seconds on 1 000 rows. On a million: one hour, or forty-six days, "
    "and nothing about the code changed.",
    r"""
::: {.motivation}
[Motivating example]{.label}
Your script processes the 1 000-row pilot in **four seconds**. The full dataset
has 1 000 000 rows, a thousand times bigger. You start it on Friday expecting it
on Saturday. It is still running three weeks later.
:::

:::: {.figures}
::: {.fq}
[4 s]{.big}[at n = 1 000]{.cap}
:::
::: {.fq}
[~1 hour]{.big}[at n = 10⁶ if the cost is linear]{.cap}
:::
::: {.fq}
[46 days]{.big}[at n = 10⁶ if it is quadratic]{.cap}
:::
::::

[Nothing about the code changed. What property of it decides which of those two numbers you get?]{.ask}
""",
    r"""
The pilot runs in four seconds. The full dataset is a thousand times larger.
How long will it take? The honest answer is that you cannot tell from the
four seconds, because that single measurement is compatible with wildly
different futures. If the cost grows linearly with $n$, one pass over the
data, then a thousand times more data means a thousand times more time, $4
\,\text{s} \times 1\,000 = 4\,000\,\text{s}$, about 67 minutes. If it grows
quadratically, a loop inside a loop over the same data, then a thousand times
more data means a million times more time, $4\,\text{s} \times 10^6 = 4
\times 10^6\,\text{s}$, about 46 days. If it grows as $n \log n$, as a sort
does, then about 90 minutes. And if it is exponential, the pilot was the
largest instance you will ever solve. Same code, same machine, same four
seconds. What separates 67 minutes from 46 days is not the speed of anything:
it is the shape of the growth, and that is a property you can read off the
code before running it at all.

This is why timing on a small case tells you so little, and why the advice
to optimize later if it turns out slow is bad advice. A constant-factor
optimization, whether better hardware, a faster language or more cores, buys
you a factor of ten or a hundred; going from quadratic to linear at $n =
10^6$ buys you a factor of a million. The first cannot substitute for the
second, and no amount of engineering rescues the wrong growth rate. There is
a second-order lesson in the arithmetic: the crossover is often past the
pilot. At $n = 1\,000$ a quadratic algorithm with a small constant can easily
beat a linear one with a large constant, which is exactly why the pilot did
not warn you. Asymptotic behavior is invisible at small $n$ by definition.

Section 4 of this session is about measuring the cost of an algorithm by
counting operations rather than seconds, so that the answer does not depend
on which laptop you used. Section 8 is about O-notation, the tool for saying
"linear", "quadratic" or "$n \log n$" precisely, and for justifying it from
the code. Section 5 is about the best, average and worst cases, because "how
long will it take" has three answers, and they can be very far apart.
Sections 3 and 9 put the growth rates side by side, which is the table to
keep: the difference between $\log n$, $n$, $n \log n$, $n^2$ and $2^n$ at
realistic sizes. The skill this session really teaches is to look at a piece
of code and say how its cost grows before you run it. After this session you
should be able to look at your own pilot script and predict which of the four
numbers above you are heading for.
"""
    )

add("M08-B", "Two students, the same answer, 20 000× apart",
    "Both correct, both hand in the same numbers. One finishes in 90 minutes, "
    "the other in under a second.",
    r"""
::: {.motivation}
[Motivating example]{.label}
Both are asked to keep only the posts written by users in a list of 20 000. One
writes a loop inside a loop. The other builds a lookup table first. **Both are
correct and both hand in the same numbers.** On a million posts, one finishes in
about **an hour and a half** and the other in **under a second**.
:::

:::: {.figures}
::: {.fq}
[2 × 10¹⁰]{.big}[operations, nested loops]{.cap}
:::
::: {.fq}
[10⁶]{.big}[operations, with a hash set]{.cap}
:::
::: {.fq}
[20 000×]{.big}[fewer, identical output]{.cap}
:::
::::

[How do you *see* that difference by reading the code, before you run it?]{.ask}
""",
    r"""
This is a real exam question in this course, and both answers to it are
correct. You have a million posts and a list of 20 000 users, and you must
return only the posts written by users on the list. The first version is the
direct translation of the sentence:

```
For each post p:
      For each user u in users:
            If p.uid = u.uid
                  then keep p
```

The second version does the same thing with one preparatory step:

```
U ← ∅
For each user u in users:
      add u.uid to U                     # U is a hash set
For each post p:
      If p.uid ∈ U
            then keep p
```

They produce identical output, and if you only ever ran them on the seminar
example with 20 posts you would never tell them apart. Count the operations.
The first version makes $P \times U = 10^6 \times 2 \times 10^4 = 2 \times
10^{10}$ comparisons. The second makes $P + U \approx 10^6$ operations,
because each membership test computes the slot from the value and looks only
there. That is a factor of 20 000, and at a few million operations per second
in an interpreted language it is roughly an hour and a half against well
under a second.

Now the part that matters for how you read code: you did not have to run
anything to know this, you read the shapes. A loop inside a loop over a
different collection costs the product of the two sizes; this is the single
most common source of accidental quadratic behavior, and it appears every
time someone writes "for each X, look through the Y". Two loops one after
another cost the sum of the two sizes. Nested means multiply and sequential
means add, and that one rule, applied by eye, catches most complexity
problems in analysis code. It is what O-notation formalizes.

Section 4 of this session is about counting operations from the code, which
is exactly the reading above done carefully. Section 8 is about O-notation,
$O(P \cdot U)$ against $O(P + U)$, why constants and lower-order terms drop
out so that only the shape remains, and the rules for combining, where nested
loops multiply, sequential blocks add, and the largest term dominates.
Section 10 connects this to the data structures of session 3, so that "a hash
set makes membership $O(1)$" is a fact you can justify rather than remember.
The habit to build is that whenever you write a loop inside a loop, you ask
what the two collections are. If they are both large, you have just written
the slow version, and there is almost always a lookup table that turns it
into the fast one.
"""
    )

add("M08-C", "Ten billion pages in a third of a second",
    "No machine can look at 10¹⁰ pages in 0.3 s. What class of procedure "
    "makes it possible, and what did it cost up front?",
    r"""
::: {.motivation}
[Motivating example]{.label}
A web search returns results from an index of well over **10¹⁰ pages** in about
**0.3 seconds**. Looking at each page just once, even at a billion per second,
would take **ten seconds**, and that is only to *look*, before any ranking.
:::

:::: {.figures}
::: {.fq}
[10¹⁰]{.big}[pages indexed]{.cap}
:::
::: {.fq}
[0.3 s]{.big}[to answer]{.cap}
:::
::: {.fq}
[~34]{.big}[steps, if the cost is log n]{.cap}
:::
::::

[No machine is fast enough to brute-force this. What class of procedure makes it possible, and what did it cost up front?]{.ask}
""",
    r"""
Type a query into a search engine and the results come back in a fraction of
a second, from an index of more than ten billion pages. It is worth pausing
on how impossible that should be. Suppose the engine simply looked at every
page and checked whether it matched. At an implausibly generous one billion
pages per second, that is ten seconds per query, and only for the looking,
with no ranking, no relevance and no concurrent users. Real answers arrive in
about 0.3 seconds, for millions of simultaneous queries. Brute force is not
slow here; it is off by orders of magnitude that no hardware budget closes.
So the answer cannot be that the machines are fast. It has to be that the
procedure does not look at most of the data, and two ideas do the work, both
of them in this session.

The first is sub-linear search. A procedure whose cost grows like $\log n$
rather than $n$ touches a vanishing fraction of the data: $\log_2 (10^{10})
\approx 34$, a few dozen steps for ten billion items. The binary search of
session 3 is the elementary case, and a hash lookup, at $O(1)$, is better
still. The reason why logarithms matter so much in this course is exactly
this: $\log n$ barely grows, so a $\log n$ procedure scales to data that a
linear one cannot touch. The second is pre-computation. The search engine
does not answer your question from the web. It answers from an inverted
index, built in advance, which maps each word to the pages containing it.
Building it is enormously expensive and happens continuously, and the query
then costs a lookup rather than a scan. This is exactly the trade of session
7, where sorting is an investment, at industrial scale: pay a lot once, pay
almost nothing per query, and the arithmetic works because there are billions
of queries. The general form is the thing to take away: where you cannot
afford to compute the answer, arrange the data in advance so that the answer
is cheap to look up. That is the same move as building a hash set in session
3, sorting a codebook in session 7, and creating a database index in session
11, and this session gives you the vocabulary to say how much it buys.

Section 8 of this session is about O-notation, and sections 3 and 9 put the
growth rates side by side; the gap between $\log n$ and $n$ at $n = 10^{10}$
is the whole of the story above. Section 2 distinguishes time from memory
complexity, which is the other half of the trade: a pre-computed index is a
very large object, and someone pays for it. The framing to carry forward is
that complexity analysis is not about making slow code faster. It is about
knowing, in advance, which designs are possible at all at the size you care
about.
"""
    )

# ===========================================================================
#  Session 9 -- Theoretical Computer Science
# ===========================================================================

add("M09-A", "The regular expression that took down a large part of the web",
    "One line of pattern, 27 minutes of global outage. A pattern matcher is a "
    "machine with a precise definition, and precise limits.",
    r"""
::: {.motivation}
[Motivating example]{.label}
On 2 July 2019 Cloudflare deployed **one line**: a pattern meant to spot
malicious JavaScript. On some inputs it made the matcher try an **exponentially
growing** number of possibilities. CPU across the global network went to 100%,
and a large share of the web was unreachable for **27 minutes**.
:::

:::: {.figures}
::: {.fq}
[1 line]{.big}[of pattern deployed]{.cap}
:::
::: {.fq}
[100%]{.big}[CPU, worldwide, within seconds]{.cap}
:::
::: {.fq}
[27 min]{.big}[global outage]{.cap}
:::
::::

[A pattern matcher is a machine with a precise definition. What can it do, what can it not, and what makes it explode?]{.ask}

::: {.source}
Cloudflare, "Details of the Cloudflare outage on July 2, 2019"
:::
""",
    r"""
On 2 July 2019, Cloudflare, which sits in front of a large fraction of the
world's websites, pushed a routine update to its firewall rules. One of them
was a regular expression intended to detect malicious JavaScript. Within
seconds, CPU usage across the entire global network hit 100% and a
substantial share of the web returned errors. The outage lasted 27 minutes.
The offending pattern contained, in simplified form, the fragment
`.*(?:.*=.*)`, a repetition nested inside a repetition. On certain inputs, a
backtracking matcher has to try an exponential number of ways to split the
input between the two repetitions before concluding that there is no match.
This failure mode is common enough to have a name and a vulnerability
category, catastrophic backtracking, or ReDoS.

What makes this the right story to open this session with is that the
explanation is theoretical, not an engineering slip. A regular expression, in
the mathematical sense, describes exactly what a finite-state automaton can
recognize, a machine with finitely many states that reads the input once,
from left to right, with no memory beyond its current state. Such a machine
has a guaranteed cost, linear in the length of the input, always, and it
cannot backtrack because it has nowhere to backtrack to. The regular
expression engines of most programming languages are not that machine. They
implement extra features, such as backreferences and lookahead, that push the
language beyond regular, and they are built on backtracking search rather
than on an automaton. That is where the exponential comes from. Engines built
as true automata, such as Go's `regexp`, Rust's `regex` and RE2, cannot
exhibit this behavior at all, and pay for it by refusing the extra features.
So the practical question, why one line took down a large part of the web,
has an answer that is entirely about what class of machine is doing the
work, and that is what this session is about.

Section 2 of this session is about finite-state automata, the 5-tuple, the
deterministic and nondeterministic versions, and the guarantee that comes
with them. Section 5 is about regular expressions and their equivalence to
those automata. Section 6 is about what automata cannot do, such as matching
balanced brackets or $a^n b^n$, because they have no unbounded memory, and
about the Chomsky hierarchy, regular, context-free, context-sensitive and
recursively enumerable, with a machine for each level and a strictly higher
price for each. The transferable idea is that the class of machine
determines the guarantee. Once you know that a problem needs only a
finite-state machine, you know it is linear; once you leave that class, you
have given the guarantee up, and it is worth knowing on which side of the
line you are before deploying to a third of the internet.
"""
    )

add("M09-B", "300 students, 40 seminars, and no schedule",
    "The assignment problem the department does by hand. There is a "
    "mathematical reason why no clever program makes it easy.",
    r"""
::: {.motivation}
[Motivating example]{.label}
Every student ranks the seminars; every seminar has a cap; some combinations
clash. You want an assignment that satisfies the constraints. The department has
done this by hand for years. Written down properly, the number of possible
assignments exceeds the number of atoms in the observable universe.
:::

- Trying harder does not help. Buying a faster computer does not help.
- There is a **mathematical reason**, and it is one of the seven Millennium Prize
  Problems.

[How can we *prove* a problem is hard, rather than concluding that we were not clever enough?]{.ask}
""",
    r"""
The department assigns 300 students to 40 seminars. Students rank their
preferences, seminars have caps, some students have timetable clashes, and a
few combinations are forbidden. Someone does this by hand every semester and
it takes a week. Ask a programmer to automate it and you will get one of two
answers: a program that produces an assignment quickly, or an admission that
producing the best assignment is out of reach, and the gap between those is
the subject of this session. The reason is not lack of cleverness. Assigning
300 students to 40 seminars allows $40^{300}$ configurations, a number with
481 digits, against roughly 80 digits for the count of atoms in the
observable universe. The constraints prune that enormously, but not enough:
problems of this family, constrained assignment, timetabling and scheduling,
are NP-complete, and no polynomial-time algorithm for any of them is known.

Here is why that is a theoretical statement rather than an engineering
complaint, and why it is genuinely useful to know. Checking is easy and
finding is hard: hand me a proposed assignment and I can verify in seconds
that every cap is respected and that no student has a clash, and that
asymmetry, cheap to verify and expensive to find, is the definition of the
class NP. The hard problems are all the same problem: a polynomial-time
algorithm for any NP-complete problem would give one for all of them, because
each can be transformed into the others in polynomial time, so timetabling,
satisfiability, graph coloring and the traveling salesman problem are, in
this precise sense, the same question in different clothes. So "we were not
clever enough" is a claim about thousands of problems and fifty years of
collective effort, not about you and this timetable, and that is what makes
it worth knowing, because it tells you when to stop looking for an exact
efficient algorithm and start looking for a good-enough one. Once you know
that a problem is NP-complete, the options are clear and legitimate: accept
an approximation with a stated quality bound, use a heuristic that is usually
good, restrict the problem to a special case that is tractable, or solve
smaller instances exactly. What you do not do is keep searching for the fast
exact algorithm.

Section 9 of this session covers the classes P and NP, what "verifiable in
polynomial time" means precisely and why it is not the same as "solvable",
the technique of reduction, by which a new problem is shown to be at least as
hard as a known one, which is how hardness is proved rather than assumed,
NP-completeness, and the P versus NP question itself. The exam has repeatedly
asked what NP-completeness means and how it relates to P versus NP. The
answer to have ready is the two-condition definition plus the collapse
statement: solve one in polynomial time and you have solved them all.
"""
    )

add("M09-C", "Can a program check your program?",
    "A marking system that rejects submissions which loop forever. Turing "
    "proved in 1936 that no such program can exist.",
    r"""
::: {.motivation}
[Motivating example]{.label}
A marking system receives 300 student submissions and would like to reject the
ones that loop forever, before running them. This sounds like a matter of
engineering effort. In **1936** Turing proved that **no program can do this**,
for any programming language, ever.
:::

- Not "too slow". Not "not yet". **Impossible**, and provably so.
- The proof is one page, and assumes only that the checker exists.

[What are the limits of computation itself, and how would you prove something *cannot* be done?]{.ask}

::: {.source}
Turing, "On Computable Numbers, with an Application to the Entscheidungsproblem", *Proc. London Math. Soc.* (1936)
:::
""",
    r"""
A perfectly reasonable request: before running 300 student submissions on
the marking server, reject the ones that will never stop, because nobody
wants an infinite loop holding a machine for a weekend. It sounds like an
engineering problem, to write an analyzer, look for unbounded loops, and be
conservative. It is not. In 1936 Alan Turing proved that no program can
decide, for an arbitrary program and input, whether it halts. This is the
halting problem, and it is not a statement about our current tools: it holds
for every language, every computer, and every future one. The proof is short
enough to sketch, and it is the most elegant argument in this course. Suppose
a program HALTS($P$, $x$) exists that returns TRUE if program $P$ halts on
input $x$ and FALSE otherwise, and build:

```
Procedure TROUBLE(P)
Inputs:
      P: the source code of a program
Result: halts exactly when HALTS says that P does not halt on itself
If HALTS(P, P)
      then loop forever
      else halt
```

Now ask what TROUBLE(TROUBLE) does. If it halts, then HALTS(TROUBLE,
TROUBLE) returned TRUE, so the first branch ran and it loops forever, a
contradiction. If it loops forever, then HALTS returned FALSE, so the second
branch ran and it halted, again a contradiction. Both branches are
impossible, so the assumption was wrong and HALTS cannot exist. The whole
argument uses nothing about hardware, speed or language, only
self-reference, and that is why it is permanent.

The consequences reach further than the marking server, and they are worth
knowing because they set the boundary of what any tool can promise. By
reduction to the halting problem, none of the following is decidable in
general either: whether a program ever prints a particular string, whether
two programs compute the same function, whether a program ever accesses
memory it should not, or whether a piece of code is unreachable. This is why
compilers give conservative warnings rather than guarantees, why static
analyzers report false positives, and why no antivirus can be complete; each
is doing the best possible job on a problem that has no complete solution.
Note the contrast with the bounded version. Whether a program halts within 1
000 steps is decidable, since you just run it for 1 000 steps, so adding a
bound turns an undecidable question into a decidable one. That is what real
marking systems do: a timeout, not an analysis.

Section 6 of this session presents Turing machines, the model that makes
"any program at all" a mathematically precise notion, and section 7 the
Church-Turing thesis that says it captures everything computable, together
with the halting problem, with the argument above set out properly. Section
9 covers reduction, the technique that converts one impossibility result
into a hundred, and the complexity classes. The distinction to carry away,
and to keep separate from session 8, is that hard means that we do not know a
fast algorithm, while undecidable means that no algorithm exists. The second
is a much stronger claim, and one of the few things in computing that will
never change.
"""
    )

# ===========================================================================
#  Session 10 -- Machine Learning
# ===========================================================================

add("M10-A", "Google predicted the flu, until it didn't",
    "Google Flu Trends beat the CDC in 2009 and predicted more than double the "
    "real rate in 2013. It fitted the past almost perfectly.",
    r"""
::: {.motivation}
[Motivating example]{.label}
In 2009, Google Flu Trends estimated influenza rates from search queries **two
weeks ahead** of the CDC, and it worked. By the 2012–13 season it was predicting
**more than double** the real rate. It had been fitted to millions of queries and
had learned seasonal search patterns, winter, basketball, snow, rather than flu.
:::

:::: {.figures}
::: {.fq}
[2009]{.big}[ahead of the CDC, and celebrated]{.cap}
:::
::: {.fq}
[2×]{.big}[the real rate, 2012–13 season]{.cap}
:::
::: {.fq}
[2015]{.big}[quietly shut down]{.cap}
:::
::::

[The model fitted the past almost perfectly. Why is that not a good sign, and how would you have caught it?]{.ask}

::: {.source}
Ginsberg et al., *Nature* (2009); Lazer, Kennedy, King & Vespignani, "The Parable of Google Flu", *Science* (2014)
:::
""",
    r"""
In 2009 *Nature* published a paper that looked like the future of social
measurement. Google Flu Trends estimated influenza-like illness in US regions
from the volume of certain search queries, and it tracked the official
figures of the CDC closely while being available two weeks earlier, because
the data of the CDC depends on doctors filing reports. It was selected from
50 million candidate search terms by finding the 45 that best fitted the CDC
series. And then it broke. It missed the 2009 H1N1 pandemic entirely, a
non-seasonal outbreak; it ran persistently high from 2011; and in the
2012–13 season it predicted more than double the actual rate. The service
was quietly retired in 2015.

The post-mortem by Lazer and colleagues in *Science* named two causes, and
both are squarely in this session. The first is overfitting. Searching 50
million terms for the 45 that best match 128 weekly data points is nearly
guaranteed to find terms that fit the past and mean nothing, and some of the
selected terms had no plausible connection to influenza; they were seasonal
for other reasons, such as the high-school basketball season, which peaks in
winter. The model had learned "it is winter" with great accuracy. A model that
fits the training data almost perfectly is reporting a symptom, not an
achievement, and the standard defense, evaluating on data the model has never
seen, is what this session builds. The second cause is algorithmic
confounding. The measuring instrument was not independent of what it
measured: Google changed its search product repeatedly over the period,
adding suggestions and related-search features that themselves increase the
volume of health-related queries, so the model was partly measuring Google's
own interface changes. This is a problem specific to digital trace data and
has no counterpart in survey methodology, because the platform is not a
passive sensor. The episode does not show that search data is useless; later
work found that Google Flu Trends combined with CDC data outperformed either
alone. What it shows is that a predictive instrument needs the same scrutiny
as any other instrument, validation against something external and a check
that it has not simply memorized the past.

Section 6 of this session is about generalization, why the test set must be
held out before training begins, and what information leakage does to a
reported score. Section 8 is about overfitting and the bias-variance
trade-off, which is the formal version of "45 terms out of 50 million".
Section 5 is about error and loss, and why the number you report depends on
which question you are actually asking. Section 12 is about responsible use,
where algorithmic confounding sits alongside the other ways in which a model
can be confidently wrong. The sentence to leave the session with is that
fitting the past well is evidence of nothing until you have shown that the
model works on data it has never seen.
"""
    )

add("M10-B", "93% accurate, and it never finds anyone",
    "A dropout-risk model with 93% accuracy that identifies nobody. Which "
    "number should have been on the report?",
    r"""
::: {.motivation}
[Motivating example]{.label}
A university builds a model to flag students at risk of dropping out. It reports
**93% accuracy** and is approved. Only 7% of students actually drop out, and the
model has learned to answer **"no" every time**. Its accuracy is 93% and it
identifies **nobody**.
:::

:::: {.figures}
::: {.fq}
[93%]{.big}[accuracy]{.cap}
:::
::: {.fq}
[0]{.big}[students identified]{.cap}
:::
::: {.fq}
[0]{.big}[recall, and therefore F₁]{.cap}
:::
::::

[Which number should have been on the report instead, and what does the right answer depend on?]{.ask}
""",
    r"""
A university wants to identify students at risk of dropping out early enough
to offer support. A model is built, evaluated, and reported as 93% accurate,
and the committee approves it. Seven percent of students drop out. A model
that predicts "will not drop out" for every single student, a model
containing no information whatsoever, is correct 93% of the time. If the
reported model is doing anything at all, the report does not show it, and the
report does not distinguish the two cases. This is class imbalance, and it is
the normal condition rather than a special case: fraud is rare, disease is
rare, hate speech is rare, dropping out is rare. Accuracy weights every case
equally, so it is dominated by the majority class, precisely the class nobody
cares about. The metrics that reveal the problem are all computed on the
minority class. Precision asks, of the students we flagged, how many really
were at risk, $TP/(TP+FP)$; recall asks, of the students really at risk, how
many we caught, $TP/(TP+FN)$; and $F_1$ is the harmonic mean of the two,
$2PR/(P+R)$. The always-"no" model has recall 0, so $F_1 = 0$. The metric
collapses to zero the instant the model stops finding anything, which is
exactly the behavior you want from a metric.

The second half of the question is the one that carries the real weight, and
it has no purely technical answer: precision and recall trade off against
each other, and which one you want depends on what happens next. If flagged
students are automatically enrolled in a mandatory program, a false positive
imposes something unwanted on someone who did not need it, so you optimize
precision. If flagged students are offered an appointment they can decline, a
false positive costs an email, while a false negative is a student who needed
help and was never contacted, so you optimize recall. Same model, same data,
opposite thresholds, decided by the intervention and not by the statistics.
That decision belongs to the people designing the program, which is why it
needs to be stated in terms that a committee can actually discuss.

Section 5 of this session covers error, loss, class imbalance, precision,
recall and $F_1$, with this exact arithmetic worked through. Section 3
presents the supervised setup, so that $TP$ and $FN$ refer to something
concrete. Section 12 is about responsible use: whether a prediction should be
made at all, what happens to the person on the receiving end, and who is
accountable when it is wrong. The rule to carry out is never to report
accuracy alone on imbalanced data, and always to state the base rate
alongside it, so that the reader can see the comparison you should have made
yourself.
"""
    )

add("M10-C", "A million speeches nobody can read",
    "Every Bundestag speech since 1949: forty person-years to hand-code. You "
    "can code 2 000. Now what?",
    r"""
::: {.motivation}
[Motivating example]{.label}
You have every speech given in the Bundestag since 1949, on the order of a
**million** of them. You want to know how the tone changed. Coding them by hand
at five minutes each would take one person about **forty working years**. Coding
a sample of **2 000** takes a week.
:::

:::: {.figures}
::: {.fq}
[~10⁶]{.big}[speeches]{.cap}
:::
::: {.fq}
[~40 yr]{.big}[to hand-code them all]{.cap}
:::
::: {.fq}
[2 000]{.big}[you can actually code]{.cap}
:::
::::

[How do you turn 2 000 human judgments into a measurement of a million documents, and how do you know whether to believe it?]{.ask}
""",
    r"""
Content analysis is one of the oldest methods in the social sciences, and it
does not scale. Two trained coders, a codebook, an intercoder reliability
check, and a sample of a few hundred documents: this is rigorous, well
understood, and it caps out at roughly the number of documents two people can
read. Now the corpus is every Bundestag speech since 1949, around a million
documents. At five minutes each, one person needs about 83 000 hours, some
forty working years, and two coders with double coding make it eighty. The
method that is correct is not available. The obvious move is to sample. Two
thousand speeches, coded properly, is a week's work and supports perfectly
good inference about the population, but it forecloses the questions that
made the corpus interesting: how the rhetoric of one party shifted across a
specific decade, what happened in the three months after a particular event,
how a single speaker changed over a career. Those are questions about
subsets, and a sample of 2 000 has too few documents in any of them.

The move this session is about is different. Instead of using the 2 000
coded documents as the data, use them as examples of the judgment you want
made, and train a model to reproduce that judgment on the other 998 000. That
reframing is the whole of supervised learning: the 2 000 hand-coded speeches
are the training data, pairs of an input $x$, the text, and a label $y$, your
judgment; a model $f$ is fitted so that $f(x) \approx y$ on those examples;
and the model is then applied to documents no human has read. It immediately
raises the question that decides whether the study is any good: how do you
know that the model reproduces your judgment rather than something correlated
with it? Hold out part of your coded data, never let the model see it, and
measure the agreement there. That measurement, not the confidence of the
model and not how sensible the output looks, is your evidence. Two warnings
belong in the same breath, and both are developed later in the session. The
model learns what your coders did, including their systematic mistakes; it
industrializes your codebook, biases and all. And agreement can be high
overall and poor exactly where it matters, on rare categories, on the years
you care about, or on the speeches of one party, so check by subgroup and not
only in aggregate.

Section 3 of this session presents the supervised setup, features, labels,
model and prediction. Section 4 is about features, how a speech becomes
something a model can take as input, and why TF-IDF is a better
representation than raw word counts. Section 6 is about the train/test
split, which is how the question of how you know gets an answer. Section 9
presents the models themselves, starting with Naive Bayes, which is a strong
and interpretable baseline for exactly this task. The framing to keep is
that a supervised model here is a measurement instrument, and instruments
have to be validated. The fact that it was fitted rather than designed
changes nothing about that obligation.
"""
    )

# ===========================================================================
#  Session 11 -- Databases
# ===========================================================================

add("M11-A", "The 15 841 cases that fell off the end of a spreadsheet",
    "Public Health England lost 16 000 COVID results to a 65 536-row limit. "
    "No error appeared. 50 000 contacts were never traced.",
    r"""
::: {.motivation}
[Motivating example]{.label}
Between 25 September and 2 October 2020, Public Health England lost **15 841
positive COVID-19 test results**. Labs sent results as CSV; the collating process
used an old spreadsheet format whose worksheets hold **65 536 rows**. When a file
exceeded that, the extra rows were simply not read. **No error appeared.**
:::

:::: {.figures}
::: {.fq}
[15 841]{.big}[positive cases lost]{.cap}
:::
::: {.fq}
[65 536]{.big}[row limit, silently applied]{.cap}
:::
::: {.fq}
[~50 000]{.big}[contacts never traced]{.cap}
:::
::::

[What does a database give you that a file on someone's computer does not?]{.ask}

::: {.source}
BBC News and *The Guardian*, 5 October 2020; Public Health England statement
:::
""",
    r"""
Between 25 September and 2 October 2020, at the height of the second wave,
the English contact-tracing system lost 15 841 positive COVID-19 test
results. The people who tested positive were told their result, but their
contacts were not traced, an estimated 50 000 people who had been exposed and
were never contacted. The cause was a file format. Laboratories submitted
results as CSV files, and the process that collated them loaded these into
`.xls`, the pre-2007 Excel format, whose worksheets hold a maximum of 65 536
rows. When the file of a lab exceeded that, the rows beyond the limit were
silently discarded. Nothing was logged, nothing failed, and the collation
completed successfully every day.

It is easy to file this under "someone used the wrong tool", and the tabloid
version did. The more useful reading is to ask what a proper database would
have given, item by item, because each item is a topic of this session. Scale
is not the point; silence is. Any storage system has limits, and what matters
is whether exceeding one produces an error or a wrong answer; a database
rejects an insert it cannot perform and tells you, and it does not quietly
keep the first 65 536 rows. Constraints are enforced by the store and not by
the user: a schema declaring that a test result must have a patient
identifier, a date and a valid result code makes malformed data impossible to
insert, while in a spreadsheet the rules live in the head of whoever is doing
the work. Transactions are all or nothing: a load that fails halfway leaves
the database as it was, not partially updated with no record of which part,
and that is atomicity, one of the ACID properties. Concurrency is handled:
multiple labs writing at once is the normal case for a database and a recipe
for lost updates with files on a shared drive. And there is one copy, so the
question of how many positives there were on 28 September has exactly one
answer, rather than one per person who has a copy of the file. None of this
is exotic. It is what a database is, and the reason why the answer to "why
not just use a spreadsheet?" is not snobbery but a list of specific
guarantees you lose.

Section 2 of this session says what a database and a DBMS actually are, and
why the distinction matters. Section 4 gives the reasons to use one, data
independence, standardization and concurrency, and the standardization point
is exactly the CSV-to-`.xls` failure. Section 5 is about transactions and
ACID, which is the formal version of the requirement that it should not be
possible to half-load a file. Sections 6 and 7 present the relational model,
keys and normal forms, that is, how the store itself enforces that a fact is
recorded once and correctly. The question to ask of any research data setup
is whether anyone would find out if it silently lost 5% of the records. If the
answer is no, the format is the problem.
"""
    )

add("M11-B", "Two seats, one airplane",
    "Two agents book the last seat in the same second. Each program checked "
    "availability and found one. Neither has a bug.",
    r"""
::: {.motivation}
[Motivating example]{.label}
Two travel agents, in two cities, book the last seat on the same flight in the
**same second**. Each system checked availability, found one seat free, and sold
it. Both passengers have a valid booking and a boarding pass.
:::

- Neither program has a bug. Each is correct **on its own**.
- The failure only exists **between** them.

[What has to be guaranteed for "check, then book" to be safe when thousands of people do it at once?]{.ask}
""",
    r"""
One seat left. Two agents, in two cities, click "book" in the same second,
and each program does the obvious and correct thing:

```
free ← read the number of free seats          # both agents read 1
If free > 0
      then write free - 1 as the number of free seats
           issue the ticket
```

Trace the interleaving. Agent A reads 1. Before A writes, agent B also reads
1. Both see a free seat, both write 0, both issue a ticket. The seat has been
sold twice, and the seat count says 0, which is consistent with either one
sale or a hundred. Read the code of either program in isolation and it is
flawless. The defect does not exist in either one; it exists in the
interleaving, and interleavings are not visible in the source of any single
program. This is a race condition, and it is the reason why concurrent
systems are hard in a way that sequential ones are not. It is also not a rare
corner case. It is the normal condition for anything with more than one user,
such as booking systems, ticketing, inventory, appointment slots or vaccine
doses, and any pattern of the form "read a value, decide, write it back" has
this shape.

The database answer is the transaction, a group of operations that must
happen completely or not at all, and that must behave as though nothing else
ran at the same time. The four guarantees go by the acronym ACID. Atomicity
means all of it or none of it, so a booking that fails partway leaves no
trace. Consistency means that a transaction that succeeds leaves the database
valid, so a constraint like "seats sold ≤ capacity" cannot be violated.
Isolation means that the outcome of running transactions concurrently must
equal the outcome of running them one after another in some order, and this
is the property that rules out the interleaving above. Durability means that
once a transaction is confirmed, it survives a crash, a power cut, or the
server catching fire. Isolation is the deep one and worth stating carefully:
it does not say that transactions run one at a time, which would be unusably
slow. It says that the result must be indistinguishable from some serial
order, and the database is free to interleave as aggressively as it likes,
provided that nobody can tell.

Section 5 of this session covers transactions and ACID in full, with this
scenario as the worked case. Section 4 presents concurrency as one of the
three reasons why databases exist, alongside data independence and
standardization. Section 1 introduces the flight-reservation and
vaccine-distribution examples that run through the lecture, both of which
are this problem at scale. The connection forward is that session 12 meets
the same problem in the hardware, two threads incrementing a shared counter,
and reaches for the same solution: any time two things share mutable state,
"check, then act" is unsafe unless something guarantees that it is one step.
"""
    )

add("M11-C", "Whose number is right?",
    "Three copies of the participant list, three people doing their jobs, and "
    "three different answers to 'how many participants'.",
    r"""
::: {.motivation}
[Motivating example]{.label}
Three people in a department each keep a copy of the participant list. One
corrects a misspelled name, one adds the new wave, one removes a withdrawn
respondent. Three months later the three files disagree about how many
participants there are, by **47**.
:::

- Everyone did their job correctly.
- There is **no version that is right**, and no way to reconstruct one.

[Where should a fact live, so that changing it once changes it everywhere?]{.ask}
""",
    r"""
This one has no dramatic outcome and no news coverage, which is why it is
worth including: it is what actually happens in research groups. A project
keeps a participant list. It starts as one file. Someone needs it for an
analysis and copies it. Someone else needs a version with the new wave merged
in. A third person keeps the master but is on leave when a participant
withdraws, so the withdrawal is applied to somebody else's copy. Three months
on there are three files. One has the corrected spelling of a name, one has
the new wave, one has the withdrawal, and none has all three. The counts
differ by 47, nobody knows which file is authoritative, and the only way to
find out is to reconcile three files by hand, assuming that the changes are
even recoverable, which they usually are not, because none of them was
recorded as a change. Nobody was careless. Each person did a correct and
necessary thing to the copy in front of them. The failure is architectural:
the same fact was stored in more than one place, so it became possible for
the copies to disagree, and once that is possible it is only a matter of
time.

The answer of the relational model is a design principle, and it is the
through-line of this session: every fact should be stored in exactly one
place. That is what a primary key enforces within a table, one row per
participant, identified by an identifier that never changes even if the name
does. It is what a foreign key enforces between tables, since other tables
refer to that participant rather than repeating their details. And it is what
normalization is for, the systematic removal of the repetition that makes
disagreement possible. The failure modes have names, and the session works
through them. An update anomaly changes a value in one place and not in
another, so that the data contradicts itself, which is exactly the story
above. An insertion anomaly means that you cannot record a fact because there
is nowhere to put it without inventing unrelated data. A deletion anomaly
means that removing one record silently destroys unrelated information that
happened to live in the same row. A shared database does not make people more
careful. It makes the careless outcome structurally impossible: there is one
row for each participant, one place to change the name, and a record of who
changed it and when.

Sections 6 and 7 of this session present the flat versus the relational
model, keys, foreign keys and normal forms, with a worked example of exactly
the repetition above. Section 4 is about data independence and why a single
store beats a folder of files. Section 5 is about transactions, which is the
same argument for simultaneous edits rather than sequential ones. The
question to ask of your own project is how many files you have to edit if a
value changes. If the answer is more than one, you have already built the
failure above; it just has not surfaced yet.
"""
    )

# ===========================================================================
#  Session 12 -- Parallel Programming
# ===========================================================================

add("M12-A", "Your laptop stopped getting faster in 2005",
    "Clock speeds flat at about 3 GHz for twenty years while transistor "
    "counts kept doubling. The extra transistors became cores, not speed.",
    r"""
::: {.motivation}
[Motivating example]{.label}
For thirty years, slow code got faster by waiting: the same program ran twice as
quickly on the hardware of two years later. Then clock speeds flattened, around
**3 GHz, where they still are**, while the transistor count kept doubling. The
extra transistors went into **more cores, not faster ones**.
:::

:::: {.figures}
::: {.fq}
[~3 GHz]{.big}[clock speed, since about 2005]{.cap}
:::
::: {.fq}
[2 → 128+]{.big}[cores per chip in the same period]{.cap}
:::
::: {.fq}
[0×]{.big}[automatic speedup for sequential code]{.cap}
:::
::::

[The free lunch is over. Making the extra cores useful is now a software problem, which means it is yours.]{.ask}
""",
    r"""
Between roughly 1975 and 2005 there was a reliable way to make slow code
fast: wait. Processor clock speeds doubled every couple of years alongside
transistor counts, so the same unmodified program ran twice as fast on the
hardware of two years later, and nobody had to do anything. That stopped.
Clock speeds hit a wall around 3 GHz in the mid-2000s and have essentially
stayed there for twenty years, because power consumption and heat rise faster
than the clock frequency and there is no way to remove the heat. Moore's law
itself did not stop, since transistor counts kept roughly doubling; the
transistors simply went somewhere else, into cores. The consequence is a
genuine break in how performance works. A sequential program gets no faster
on a 128-core machine than on a 4-core one: it uses one core, and the other
127 sit idle. Making use of them requires the program to be written to use
them, which is a software problem, and increasingly the only remaining source
of speedup. This is what Herb Sutter called "the free lunch is over", and it
is why a course like this has a session on parallelism at all: for the first
time in the history of computing, performance is something you have to ask
for.

Two qualifications belong right here, before any enthusiasm sets in. First,
parallelism does not change complexity. An $O(n^2)$ algorithm on 100 cores is
still $O(n^2)$, because you have divided the work by 100, which is a constant
factor. The lesson of session 8 holds: if your program is too slow, check
whether you have an algorithm problem before you reach for hardware, because
no number of cores rescues the wrong growth rate. Second, the speedup is
bounded, and by less than you would guess. Whatever fraction of your program
cannot be parallelized sets a hard ceiling on the whole thing, no matter how
many processors you buy, and that fraction is usually larger than people
expect, since reading the input, writing the output and the sequential
combination step all count. The formula that quantifies it, Amdahl's law, is
the last thing in this session and the most commonly misapplied idea in it.

Section 1 of this session is about Moore's law, its physical limits, and why
parallelization is the workaround. Sections 4 and 5 give the vocabulary,
multiprocessor, multicore and multithreading, and the distinction between
concurrency, a way of structuring a program, and parallelism, a way of
executing one; confusing those two is the most common error in this
material. Sections 7 and 8 show where the parallelism actually lives in your
machine, in instruction pipelines, cores, GPUs and clusters, and section 11
presents Amdahl's law and the ceiling. The practical framing is that your
laptop has had multiple cores for your entire adult life, and almost every
analysis script you have written has used one of them. This session is about
when that is worth changing and when it is not.
"""
    )

add("M12-B", "Sixteen cores, and 2.5× faster",
    "40 hours becomes 16 on 16 cores, and 15 on 64. Where did the other "
    "thirteen cores go? There is an exact formula, from 1967.",
    r"""
::: {.motivation}
[Motivating example]{.label}
A simulation takes **40 hours**. You move it to a 16-core machine expecting two
and a half. It takes **16 hours**. You move it to **64 cores**. It takes
**15**.
:::

:::: {.figures}
::: {.fq}
[2.5×]{.big}[faster, on 16 cores]{.cap}
:::
::: {.fq}
[2.7×]{.big}[faster, on 64 cores]{.cap}
:::
::: {.fq}
[2.8×]{.big}[the ceiling, at any number of cores]{.cap}
:::
::::

[Where did the other thirteen cores go? There is an exact formula, and it was written down in 1967.]{.ask}
""",
    r"""
An agent-based model takes 40 hours on your laptop. The department has a
16-core node on the cluster. You expect two and a half hours and you get 16.
You request a 64-core node and you get 15. Nothing is broken, nobody
misconfigured anything, and the numbers are exactly what theory predicts.
Gene Amdahl wrote the formula down in 1967:

$$S = \frac{1}{(1 - P) + \dfrac{P}{N}},$$

where $P$ is the fraction of the computation that can be parallelized and
$N$ the number of processors. Read the denominator: $(1-P)$ is the serial
part, which $N$ never touches, and $P/N$ is the parallel part shared out. Fit
it to the observation. A speedup of 2.5 on 16 cores means

$$2.5 = \frac{1}{(1-P) + P/16} \;\Longrightarrow\; P \approx 0.64,$$

so 64% of the runtime parallelizes and 36% does not: reading the input
files, seeding the model, collecting results, writing output, and the parts
of the simulation that are inherently sequential. Now predict the 64-core
run,

$$S = \frac{1}{0.36 + 0.64/64} = \frac{1}{0.37} = 2.70 \;\Longrightarrow\;
40 / 2.70 \approx 15\ \text{hours},$$

which is what happened. And the ceiling, as $N \to \infty$, is

$$S_{\max} = \frac{1}{1 - P} = \frac{1}{0.36} = 2.8\times.$$

Forty hours will never become less than fourteen, on any machine that will
ever exist, until the 36% is reduced. Two things follow, and both are
counterintuitive enough to be worth stating plainly. Diminishing returns
arrive immediately: going from 1 to 4 cores buys most of what there is, the
64th core contributes essentially nothing, and the efficiency, speedup per
core, falls from 100% to 4%, so on a shared cluster you are occupying 64
cores to do the work of three, which is a cost to other people. And the lever
is the serial fraction, not the core count: reducing $1-P$ from 36% to 10%
would raise the ceiling from 2.8× to 10×, which means profiling to find where
the serial time actually goes, and it is usually somewhere dull, like parsing
input files, rather than in the interesting part of the model.

Section 11 of this session presents Amdahl's law itself, with the worked
table and the limit. Sections 4 and 5 are about what can and cannot be
parallelized in the first place, and why the answer usually comes down to
shared mutable state. Section 9 is about software parallelization, including
the observation that divide-and-conquer algorithms like mergesort parallelize
almost for free because their subproblems touch disjoint data. The rule to
take to the cluster is to measure $P$ before requesting nodes. One profiling
run tells you the ceiling, and it is frequently low enough that the right
answer is to fix the serial part instead.
"""
    )

add("M12-C", "Three billion posts, one million rows of memory",
    "Correlating likes and reshares across data that does not fit. Averaging "
    "the chunk correlations gives a number, and it is the wrong number.",
    r"""
::: {.motivation}
[Motivating example]{.label}
You are asked for the **correlation** between likes and reshares across
**3 billion** posts. Your machine holds **one million** at a time. Computing the
correlation on each chunk and averaging gives a number, and it is **the wrong
number**.
:::

:::: {.figures}
::: {.fq}
[3 × 10⁹]{.big}[posts]{.cap}
:::
::: {.fq}
[10⁶]{.big}[fit in memory at once]{.cap}
:::
::: {.fq}
[6]{.big}[numbers per chunk are enough for the exact answer]{.cap}
:::
::::

[Which statistics can be split across machines and reassembled exactly, and which cannot?]{.ask}
""",
    r"""
Three billion posts. You want the correlation between likes and reshares.
Your machine holds a million rows at a time, so the data must be processed in
about 3 000 chunks. The natural thing to do is to compute the correlation
within each chunk and to average the 3 000 results. It produces a number, and
it is not the correlation. The reason is that Pearson's $\rho$ is a nonlinear
function of the data, and averaging a nonlinear function computed on subsets
does not recover the function of the whole. Plotting the chunk-average
estimate against the true whole-sample value gives a cloud, not a line. Do
the same thing with the mean and you get a perfect line, because the mean is
linear, and an average of averages, with equal chunk sizes, is the average.
So the question is not how to split the data, but which quantities survive
being split.

For the correlation, the answer is that $\rho$ can be written entirely in
terms of sums,

$$\rho_{xy} = \frac{n\sum x_i y_i - \sum x_i \sum y_i}
{\sqrt{n\sum x_i^2 - (\sum x_i)^2}\ \sqrt{n\sum y_i^2 - (\sum y_i)^2}},$$

and sums are additive across a partition. So each chunk returns six numbers,
$n$, $\sum x$, $\sum y$, $\sum x^2$, $\sum y^2$ and $\sum xy$, the coordinator
adds them, and evaluates the formula once. The result is exactly the
whole-data correlation, not an approximation, and memory never exceeds one
chunk plus six accumulators. Six numbers per chunk instead of a million rows:
that is the whole idea behind distributed computing on data at this scale,
bring the code to the data and move only the summaries. The general
principle is worth more than the formula. Look for quantities that are
additive over partitions and sufficient to determine the statistic you want.
Where they exist, the computation distributes exactly. Where they do not,
as for the median, the quantiles or the number of distinct values, you need
several communication rounds or an approximation with a stated error bound.
That is a genuine limitation, not an implementation detail, and knowing on
which side of it your estimator falls is the useful skill.

Section 9 of this session presents MapReduce, with the Map phase computing
partial results locally, the communication phase, and the Reduce phase
combining them. Section 10 is about distributed statistical inference
specifically, with the mean as the easy case, the correlation as the
instructive one, and the trade of extra communication time against extra
variance in the estimate. Section 11 presents Amdahl's law, since the Reduce
step is serial and therefore sets the ceiling. The warning to carry into your
own work is that you cannot distribute an estimator just because you can
distribute a mean. Medians, quantiles, variances, regression coefficients and
correlations each need to be thought about separately, and the naive answer
is wrong for most of them.
"""
    )


# ===========================================================================
#  Parked examples
# ===========================================================================

park("M03-B", 'The helpline that answered the newest caller first',
    "A support queue built on the wrong structure serves people "
    "most-recent-first; nobody notices, and early callers wait all day.",
    r"""
::: {.motivation}
[Motivating example]{.label}
A support system stores incoming requests in whatever structure the developer
reached for. Under load, callers are answered **most-recent-first**. Someone who
called at 9 a.m. is still waiting at 5 p.m., while a 4:55 p.m. caller is served
immediately.
:::

- No request was lost and the **average** waiting time looks
  reasonable.
- The failure is in *who* waits: early ones wait more and not just a little bit more.

[What was the problem with the structure of the data about calls and what would be the structure to serve people fairly?]{.ask}
""",
    r"""
A public service runs a support line. Requests that cannot be handled
immediately are stored and dealt with when a caseworker frees up, and the
developer, needing somewhere to put the pending ones, used a stack. A stack
is LIFO, last in, first out: whatever went in most recently comes out first.
So under sustained load, precisely when the system matters, the person who
has been waiting longest is at the bottom of the stack, underneath everyone
who arrived after them, and a request that arrives during a busy period can
be buried indefinitely. This has a name, *starvation*. The instructive part is
how well the system hides it. Nothing is lost, since every request is still
there; no error occurs, since the code is correct in the sense of doing what
it says; and the mean waiting time can look perfectly acceptable, because most
people are served instantly. The damage is entirely in the tail, and the tail
is people.

Change one structure and the outcome changes. A queue is FIFO, first in,
first out: requests are appended at the rear and served from the front, so
every request is served after a bounded number of others, and callers are
served in the order they called. Both operations still cost $O(1)$, so the
fair version is not slower. You could also use a priority queue, which serves
the most urgent case first. That is often the right thing, and it
reintroduces the original problem in a new form, because low-priority cases
can starve unless their priority rises with their waiting time. The design
question does not go away; it becomes explicit.

Section 3 of this session covers the linked lists on which stacks and queues
are usually built, and why insertion at one end is cheap in one representation
and expensive in another; the two structures themselves, with their operations
PUSH and POP, ENQUEUE and DEQUEUE, are defined in session 5, where they drive
the two ways of searching a graph. The general point is worth stating plainly,
because it is the reason why this material belongs in a social science course:
a data structure encodes a policy. LIFO and FIFO are not two implementations of
the same thing; they are two different answers to the question of who gets
served first, and that question is not technical. Somebody chose, possibly
without realizing that they were choosing.
""",
    "Removed from session 3 on 2026-10-30, to be used when stacks, queues and "
    "heaps are covered (sessions 5 and 6). The slide is the deck version as it was "
    "on that day; see also MotivatingExamples-parked.md."
    )

park("M04-B", '"Clear the cache", said the developer',
    "Asked to clear a cache, Google's Antigravity agent deleted a developer's whole D: drive, then apologized: a command nobody checked against what was meant.",
    r"""

::: {.motivation}
[Motivating example]{.label}
Late 2025, posted on Reddit: a developer asks Google's coding agent
**Antigravity** to clear a project's cache. The agent runs
`rmdir /s /q d:\`, which deletes **the entire D: drive**, past the Recycle Bin.
Its answer: *"I am deeply, deeply sorry. This is a critical failure on my part."*
:::

:::: {.figures}
::: {.fq}
[1]{.big}[command]{.cap}
:::
::: {.fq}
[1 drive]{.big}[deleted instead of 1 folder]{.cap}
:::
::: {.fq}
[0]{.big}[confirmations asked ("Turbo mode")]{.cap}
:::
::::

[What should have been specified, and checked, before a command that deletes files is allowed to run?]{.ask}

::: {.source}
TechRadar, December 2025; AI Incident Database, report 7050
:::
""",
    r"""
In late 2025 a developer posted on Reddit what had happened while using
Antigravity, a new programming environment by Google in which an AI agent can
edit files and run commands on the developer's computer. The developer asked
the agent to clear the cache of a project, a folder of temporary files that
can safely be deleted. The agent ran the Windows command `rmdir /s /q d:\`,
which removes a folder and everything in it, silently and without using the
Recycle Bin. The folder it named was not the cache folder but the root of the
whole D: drive. The agent's reply, once it noticed, was "I am deeply, deeply
sorry. This is a critical failure on my part." The developer had enabled a
mode in which the agent runs commands without asking for confirmation. Most of
the data had been backed up elsewhere; the rest was lost.

The story spread because the apology is funny, but the failure is the most
common one in software: a command whose effect was never checked before it
ran. What the developer wanted was specified only as "clear the cache". A
specification of the task would have said which folder and nothing else, and a
system that takes the specification seriously checks, before deleting
anything, that the target is that folder. That is what tests do for code, and
what confirmations and permissions do for commands: they compare what is about
to happen with what was meant.

Section 6 treats "what the program must never do" as part of every
specification, and section 7 shows how tests turn a specification into
something that is checked rather than hoped for.
""",
    'Removed from session 4 on 2026-11-08 (David: replaced by the Symbian example M04-D). Kept for later use.'
    )

park("M04-C", 'The code freeze that was only a sentence',
    "Replit's AI agent deleted a production database during a code freeze that existed only as a sentence in a chat.",
    r"""

::: {.motivation}
[Motivating example]{.label}
July 2025: the founder of SaaStr spends twelve days vibe coding an app with
Replit's AI agent. On day nine, during a code freeze he had declared in the
chat, the agent **deletes the production database**, then reports that a
rollback is impossible. It was not; the data came back.
:::

:::: {.figures}
::: {.fq}
[1,206]{.big}[executives' records deleted]{.cap}
:::
::: {.fq}
[1,196]{.big}[companies' records deleted]{.cap}
:::
::: {.fq}
[0]{.big}[barriers between the agent and production]{.cap}
:::
::::

[A rule in a chat message is a wish. What would have made "never touch production" impossible to break?]{.ask}

::: {.source}
Fortune, 23 July 2025; AI Incident Database. Replit then separated development and production databases.
:::
""",
    r"""
In July 2025 Jason Lemkin, the founder of the software community SaaStr,
documented a twelve-day experiment in building an application by vibe coding
with the AI agent of the platform Replit. On day nine he had declared a code
freeze, a period in which nothing may be changed, and told the agent in the
chat to make no changes without his permission. The agent then deleted the
live production database, which held records on 1,206 executives and
1,196 companies. Asked about it, the agent admitted that it had ignored the
instruction, and it told Lemkin that a rollback was impossible, which turned
out to be wrong: the data could be restored. Replit's chief executive called
the deletion unacceptable, and the company separated development databases
from production databases so that an agent working on the code cannot reach
the real data.

The code freeze existed only as a sentence in a chat. Nothing in the system
enforced it: the agent had the permissions to delete the database, and the
development and the production data were the same data. A rule that matters
has to be part of the requirements of the system, and a rule that must never
be broken has to be enforced by the system itself, through permissions,
backups and separate environments, not requested in a prompt. Replit's fix is
exactly that: it turned a wish into a property of the system.

Section 5 places writing code inside the larger process of software
engineering, and section 6 explains why a prompt is a specification and why
some rules do not belong in a prompt at all.
""",
    'Removed from session 4 on 2026-11-08 (David: replaced by the Symbian example M04-D). Kept for later use.'
    )
