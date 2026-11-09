# Exercise sheets

One sheet per lecture, for the pen-and-paper exercise sessions.

| | Session | Topics |
|---|---|---|
| 01 | [Introduction](Exercise01.md) | selection sort traces, I Can't Believe It Can Sort |
| 02 | [Information Coding](Exercise02.md) | biased dice and codes, base conversion, IEEE 754 |
| 03 | [Data Structures](Exercise03.md) | hash tables, binary search and BSTs, linked lists |
| 04 | [Software](Exercise04.md) | the software engineering flow for two cases: survey ages, climate in parliamentary speeches |
| 05 | [Algorithms](Exercise05.md) | flowcharts, graph representation, BFS, Bellman-Ford |
| 06 | [Recursion](Exercise06.md) | min-heaps, DFS, Euclid's algorithm |
| 07 | [Sorting Algorithms](Exercise07.md) | selection sort, mergesort, bubblesort, stability |
| 08 | [Time Complexity](Exercise08.md) | O-notation proofs, runtime analysis |
| 09 | [Theoretical Computer Science](Exercise09.md) | automata, grammars, Turing machines, CLIQUE and SAT |
| 10 | [Machine Learning](Exercise10.md) | evaluation metrics, train/test splits, clustering |
| 11 | [Databases](Exercise11.md) | keys and normal forms, schema design, SQL, injection |
| 12 | [Parallel Programming](Exercise12.md) | Amdahl's law, MapReduce, concurrency, pipelining |
| 13 | [Social Science Applications](Exercise13.md) | trace-data validity, Schelling's model, privacy |

## Structure of a sheet

Each sheet has two parts.

**Exercises 1–3** (1–4 on sheet 9) are the ones worked through together in the
exercise session. Where a 2023/24 or 2024/25 sheet existed, they are its ported
and re-typeset version, so they are the ones with a track record, and they are the best guide to the style and size
of exam questions. The sheets themselves carry no answers: bring your attempt.

**Additional practice** is a battery of extra exercises for studying on your own.
These are new, and they go a little beyond the lecture where that is useful,
into practical consequences (encoding bugs, performance traps, pseudonymization)
and into the reasoning the exam rewards.

## Solutions

[`Solutions/`](Solutions/) holds one file per sheet,
`ExerciseNN-Solutions.md`, with worked solutions to every exercise on the
sheet, the session ones and the additional practice. Each solution opens with a
**Where to look** line that names the slides (deck and slide numbers, counting
the title slide as 1) and the handout sections (lecture transcripts, with links)
where the material needed to develop it is found. Try an exercise before opening
its solution; the sheets link to their solutions file from the header note.

Sheets **10** and **13** had no predecessor, sessions 10 and 13 were never given
an exercise sheet before, so those two are new throughout. Sheet 9 also absorbs
the Turing machine and CLIQUE exercises from the 2024 sheet 10, which covered
what is now lecture 9.

Every exercise on these sheets is indexed in the
[exam question pool](../Exams/README.md), which flags the items no cohort has
seen.

## Conventions

All sheets follow the [course conventions](../Transcripts/00-Conventions.md).
The one to keep in mind constantly: **pseudocode arrays are indexed from 1**,
Python lists from 0.

Figures specific to the exercises are in `figures/`; they have been redrawn as
SVG from the 2023/24 sheets.

## Rendering

Plain Markdown with LaTeX math. Since the answers live in separate files, a sheet
can be printed for the session as it is; print the matching file in `Solutions/`
when you want the solutions.
