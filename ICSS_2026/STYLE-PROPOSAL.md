# Style changes proposed for sessions 5 to 13

Drafted 2026-11-15 from David's revision of sessions 1 to 4. **Nothing here is
applied yet.** Mark each item keep / change / drop and I apply the result to
the rest of the materials.

## Evidence

- Before and after pairs exist for transcript 3 (Oct 30 version against the
  published one), transcript 4 (my Nov 9 clarity-pass text against the
  published one), deck 4, sheet 4 and its solutions, the sheet 3 solutions,
  and small parts of transcripts 1 and 2 and decks 1 and 2.
- For most of sessions 1 and 2, and for the notebooks, only the revised
  version exists. There I compared the revised text with the unrevised
  sessions 5 to 13.
- Counts quoted below are from the transcripts of sessions 5 to 13.

## A. Sentences

[OK] **A1. Say the logical link with a word.** Where I joined two clauses with a
colon, a semicolon or a bare comma, the revision names the relation:
*because, so, i.e., namely, for example, while, Instead, Rather, However,
Therefore, First / Then / Finally*.

| Mine | Revised |
|---|---|
| the second version never searches; it computes | never searches. Instead, it computes |
| not just a way of laying data out in memory; it is a layout plus | in memory. Rather, it is a layout plus |
| looks at each response once: two million operations | once, i.e. two million operations |
| two things: regular expressions ... and hash tables | two things, namely regular expressions |
| easy and cheap to edit: deleting a node only changes | to edit, because deleting a node only changes |
| $11 > 10$ at the root, so we go right; $11 < 13$, so we go left; and | First ... Then ... Finally |

[OK] **A2. No fragments and no clipped sentences.** Every sentence gets a subject
and a verb and says its point in full. 148 sentences of five words or fewer
remain in sessions 5 to 13.

| Mine | Revised |
|---|---|
| Parts with one clear responsibility, so that ... Documentation that says what each part does. Tests that tell you ... | The code could not be navigated and separated into parts with one clear responsibility ... this also requires documentation ... and tests ... |
| Instructions are a request. | Think about instructions as a request and not as an order that is guaranteed to be followed. |
| Found after the code is written, it costs the code. | A misunderstanding in requirements found after the code is written costs much more. |
| That separation is the point. | ..., which is the main point of writing a specification before designing and implementing the solution directly. |
| A stopped program cannot. | ... but a test stops the program instead, warning everyone involved. |
| Two housekeeping notes: | There are two housekeeping notes. |

[OK] **A3. No epigram endings.** I often end a paragraph on a short, quotable
contrast. The revision ends on the plain consequence instead. Patterns to
remove: a final ", not Y." (23 cases), ", which is exactly ..." and ", and
that is ..." (37 cases), "X is not a detail".

| Mine | Revised |
|---|---|
| everything around it is the part you cannot delegate. | ... the part you should be very careful about. Coding agents can assist you ... but without the right requirements, specifications, and tests, you will never know what vibe-coded software actually does. |
| the program can only grow. | the program can only grow and the problem gets larger and larger. |
| the quality of the hash function is not a detail. | is not just a detail but an essential design decision. |
| you should know that the problem exists and that it is solved. | keep in mind that the problem exists and that you can find a solution if you have it. |

[OK] **A4. Fewer commas inside a sentence.** Three habits were edited out.

- A comma before "and" or "to" in a short coordination: "better code from any
  coder, and they give" became "coder and they give"; "up by 5 millimeters,
  and could not" became "but could not"; "side by side, to see" lost its comma.
- A list hung on a comma where a colon used to be: "splits the list into two
  parts, a sorted part and an unsorted part". The revision uses "namely",
  "i.e." or a real list (31 cases left).
- Inserted appositions: "a coder, a person or a coding agent, wrote" became
  "a coder wrote".

[OK] **A5. Literal wording instead of metaphor.** "sit on a ladder ... on each
rung" became "are placed into levels"; "hashing attacks both" became "Hashing
attempts to solve both by addressing two questions"; "Two words in this
definition carry the weight" was deleted; "this is the interesting one" became
"an interesting and most common case in large trees".

[OK] **A6. Add the example or the consequence.** After an abstract statement the
revision adds a short "for example" or what follows from it.

- "touches one place" + ", for example just a file"
- "indices must be integers, so you cannot index an array by" + "strings, for
  example a student's name"
- "is first turned into one" + ", for example reading its binary
  representation as an integer"
- "we have gained nothing" + "and wasted some memory in left pointers"

[OK] **A7. Softer claims.** "can turn the same request into different code each
time" became "will often turn"; "Many errors are found before" became "Some
errors appear before it runs, others require a debugger"; "one line becomes
many" became "usually becomes"; "collisions are unavoidable" became
"eventually unavoidable".

[OK]**A8. Questions are asked directly.** "The lecture then asks whether the
following tree is a binary search tree." became "Is this tree a binary search
tree?"

## B. Voice

[OK] **B1. "We" and "you", with the future for what comes.** "Section 6 of this
session is about requirements" became "In this session you will learn about
requirements"; "This section and the next follow one example" became "Let's
follow an example of a small software project"; "as we will see in session 8"
became "as we will learn how to calculate in session 8".

[OK - also do not talk about the lecturer]**B2. No talk about "the lecture" as an event.** "The lecture gives two
motivating examples" became "We can see this with two examples"; "the example
of the lecture" became "the example of the figure" or "the example below";
"The lecture closes with" was rewritten around the content. 68 cases left.

[OK] **B3. No exam talk in transcripts.** "exactly the kind of question the exam
likes" was deleted. 12 cases left.

[OK] **B4. Room for David's own asides.** The revision adds remarks like "(and tend
to hate each other)" and "(imagine the amount of work without AI)". I will not
write jokes; I note it so I do not flatten them when I edit.

## C. Transcript structure

[OK but not necessarily everything. I want bullet point lists when there is some extra content in each item, not just listing words or elements]**C1. Enumerations become lists.** Anything of three or more parallel items
that I wrote as running prose is now a bulleted or numbered list with a bold
or italic lead term: the six stages, the design steps, the kinds of test case,
the requirements of a hash function, the three disadvantages of arrays, the
three steps of the loop invariant, the three points about probing.

[OK -- blockquotes should be very rare, they are a way to highlight something very important that someone else said]**C2. Quotes.** A client's message or a long quotation is a blockquote. Short
quoted requirements are in italics with quotation marks.

[OK] **C3. Figures.** The shared style block after the title; captions in italics
ending with a period and saying what the figure is ("Example of a tree that is
not a BST."); a blank line between two consecutive figures.

[OK] **C4. Contents.** Three or four thematic entries that match the outline of the
deck, each pointing to a custom `{#id}` on a heading, instead of one entry per
numbered section.

[OK] **C5. Motivating examples.** No introductory paragraph above them; only the
examples actually used (sessions 5 to 13 still open with "Three candidate
openings ... One of these will be used"); the closing paragraph says "In this
session you will learn" and ends on a sentence about the student's own
situation.

[OK] **C6. Cross-references.** No links to numbered section anchors ("the question
of [section 4](#4-...)" became "the question of editing and search"). Far-away
sessions are sometimes named by topic ("the Databases session"). See question
Q1 below.

[OK, make sure this is consistent in sessions 01-04 and edit them if necessary] **C7. Practical examples.** A section "Why does this matter? Practical Python
examples" before *Check yourself*, with the notebook link and one sentence on
what it shows, plus pointers from the text where the notebook has a matching
part.

[OK] **C8. Trimmed asides.** Deleted from the revised transcripts: forward-looking
digressions ("it is the reason why session 9 spends time on universal Turing
machines", the "Two questions organize the whole field" paragraph), repeated
biographical material, a sixth *Check yourself* question, and a closing caveat
on floats. Rule: keep a transcript to what the session covers.

## D. Slides

[OK] **D1. One idea per bullet, and bullets may be full sentences.** "installed
once with `pip install pytest`" became its own bullet; "Each line answers one
of the five questions, and one more line settles the empty case" became two.

[OK] **D2. Connective words instead of a colon inside a bullet.** "choose what runs
next: conditions, loops" became "choose what runs next, for example
conditionals and loops"; "a **state**: the current values of its variables"
became "a **state** composed of the current values".

[OK] **D3. Titles.** Spelled out and concrete: "Why do we use Object-Oriented
Programming?", "20 million lines of code to move 5 millimeters", "From
ambiguous request to specification". Example slides say so: "Example: A quick
implementation meets the tests", "Maintenance example: the third wave arrives".

[OK] **D4. Boxes.** A bold lead sentence, then "In the example:" and the bullets.

[OK] **D5. Course outline slide.** Past sessions in italics, the current one in
bold.

[OK] **D6. Practical examples slide.** Deck 2 has one before the summary
(screenshot of the notebook, three bullets, link). See Q4.

## E. Exercise sheets and solutions

[OK] **E1. Sheet header.** One plain sentence, no blockquote, no link to the
solutions, no notation link: "Exercises 1 and 2 will be covered in the
exercise session. The *Additional practice* section is for self-study and to
be covered if time allows."

[OK] **E2. Solutions.** No header blockquote and no "Where to look" lines. All
slide numbers and handout links are gone from the published solutions of
sheets 1 to 4. Sheets 5 to 13 still carry 8 to 11 such lines each.

[OK] **E3. Wording.** "by hand" became "with pen and paper"; "from session 3" was
dropped from task texts; the note "The exercises are new in 2026/27" was
removed from the sources of sheet 4.

[OK] **E4. Fewer additional exercises.** A4 to A6 of sheet 4 were removed and the
rest renumbered. See Q5.

## F. Notebooks

[OK] **F1.** Published as `PythonExamples/ExamplesNN-Topic.ipynb`.
[OK] **F2.** Links go to the published transcript pages and their custom anchors.
[OK] **F3.** No before versions exist for the notebook text, so I have no wording
rules beyond A and B.

## Questions before I apply anything

**Q1. Session references.** The revised text keeps "session 8" in some places
and uses "the Databases session" in others. Should I refer to sessions by
topic name everywhere? That would also survive a change of order (see Q2).

[Refer to them by name because the order might change in the future. Make sure this is consistent in all sessions including 01-04]


**Q2. Order of sessions 10 and 11.** The README and deck 1 say 10 Databases,
11 Machine Learning. The outline slides of decks 2 to 4 and the file names say
10 Machine Learning, 11 Databases. Which is right, and should the files be
renumbered?

[YES, now 10 is DB and 11 is ML. Change everything consistently. You can see the final schedule in /home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-github/README.html]

**Q3. Pseudocode `If`.** In the sheet 3 solutions you changed
`If c / then A / else B` to `If c / A / else / B`. The conventions page and
every other procedure still use `then`. Which form should all materials use?

[I want you to use then but there have to be a line break and a tab before so the block for then and for else are completely clear. I changed it because the tabulation was wrong. Go over everything and make sure that all ifs in pseudocode are exactly as in the conventions, with a line break followed by an extra tabulation and then with the code block consistently tabulated]


**Q4. Practical examples slide.** Should every deck get one before the
summary, as deck 2 has?

[YES]

**Q5. Additional practice.** Should I cut the conceptual additional exercises
from sheets 5 to 13 as well, or was that specific to sheet 4?

[Keep them but don't put too many, see the scale of extra tasks for sessions 02 and 03]

**Q6. Semicolons and colons.** Your revision keeps a colon before a list or a
quotation and almost no semicolons. I would keep that rule: no semicolons in
prose, colons only before lists, code and quotations.

[Yes]

**Q7. "Where to look" in the exam pool solutions.** They have the same lines
as the sheet solutions. Remove them there too?

[No]

## Found on the way, not style rules

[DO NOT DO THESE THREE]

- Typos in the revised text that I would fix rather than copy: "More
  references area available", "implicitely", "pseydonymize", "identfiable",
  "the the other", "entrymeans", "sofware", "Tests are done against was
  asked". 
- Deck 2's outline slide says "Session 4: Programming"; the other decks say
  "Software". 
- The published deck 3 is the version of 30 October. The local deck 3 has the
  later changes (doubly linked lists, the redrawn figures, binary search in
  the appendix). 
