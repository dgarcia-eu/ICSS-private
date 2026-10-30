# Exam Blueprint

*How ICSS theory exams are built, and how to assemble the next one from the
[question pool](README.md).*

---

## 1. Format

Constant across all years:

- **90 minutes**, closed book, **no calculators**.
- **6 questions**, each with **3–6 subquestions** that go from mechanical to
  conceptual.
- Answers written in the space provided between questions, so the paper is
  9–12 single-sided pages after the cover sheet.
- Cover sheet with registration number, page count, instructions, and the
  examiner's point table.

What has varied:

| Year | Total | Pass | Pass fraction |
|---|---|---|---|
| 2023/24 example, E1, E2 | 60 | 36 | 60% |
| 2024/25 example, E1 | 60 | 36 | 60% |
| 2024/25 E2 | 60 | 30 | 50% |
| 2025/26 example | 70 | 35 | 50% |
| 2025/26 E1, E2 | 60 | 30 | 50% |

**Recommended for 2026/27:** 60 points total, pass at 30 (50%), matching the two
most recent real exams. Use 70 only for the released example, where the extra
questions are there to show coverage rather than to be finished in 90 minutes.

### Timing sanity check

At 60 points in 90 minutes the budget is **1.5 minutes per point**. Every item
in the pool carries the point value it had in its source exam; the useful check
when assembling is whether a 4-point item really is a 6-minute task by hand,
without a calculator. The items that most often overrun their budget:

- IEEE 754 multiplication (`IC-04`): 4 points is right, 3 is not.
- Bellman-Ford or Dijkstra traces (`GP-08`, `GP-11`): 5 points minimum.
- A database schema from a verbal specification (`DB-05`): 5 points minimum.

---

## 2. The six questions

The structure has been stable since 2023 and follows the lecture order. Each
question draws on one or two adjacent sessions:

| Q | Topic | Sessions | Pool file | Typical points |
|---|---|---|---|---|
| 1 | Information coding | 2 | [Pool 1](Pool-1-InformationCoding.md) | 7–11 |
| 2 | Data structures (+ recursion) | 3, 6 | [Pool 2](Pool-2-DataStructures.md) | 9–13 |
| 3 | Algorithms, sorting and complexity | 5, 7, 8 | [Pool 3](Pool-3-AlgorithmsComplexity.md) | 10–12 |
| 4 | Graph algorithms (+ parallelization) | 5, 12 | [Pool 4](Pool-4-GraphsParallel.md) | 9–11 |
| 5 | Theoretical computer science | 9 | [Pool 5](Pool-5-TheoreticalCS.md) | 9–12 |
| 6 | Databases and applications | 10, 11, 13 | [Pool 6](Pool-6-DatabasesApplications.md) | 9–12 |

Parallelization (session 12) has always been an appendix to question 4 or 6
rather than a question of its own, usually a single Amdahl's law item worth 2–4
points. Machine learning (session 10) and social science applications (session
13) have historically been **absent** from the exam; the 2025/26 example is the
first to include Schelling's model. See §5.

### Subquestion shape

Within a question, subquestions escalate:

1. **(a) Mechanical.** A trace, a conversion, a construction. Marked right or
   wrong. 2–4 points.
2. **(b) Constructive.** Write pseudocode, design an automaton, write a query,
   design a schema. 2–5 points.
3. **(c) Analytical.** Complexity of what you just wrote, or why it works.
   2–3 points.
4. **(d) Conceptual/transfer.** A trade-off, a limitation, a "what would you do
   if", often the discriminating question. 2–3 points.

Keep this shape. It means a student who can only compute still scores, and a
student who only talks does not.

---

## 3. Assembling an exam

1. **Pick the point total** (60) and the per-question budget from the table
   above. The sum must be exactly the total, check it.
2. **For each question, pick one anchor item**, the mechanical or constructive
   one that carries most of the points, then 2–3 shorter items around it.
3. **Check reuse.** Do not use an item tagged with either of the two previous
   years' exams. §4 has the rotation.
4. **Check the figures.** Items that need one are marked; the figures are in
   `figures/` as SVG and can be pasted into the Word template.
5. **Check the arithmetic.** Every numeric item in this pool has a worked
   solution; re-derive it if you change any number, and update the solution in
   the pool if you keep the variant.
6. **Read it as a student.** 90 minutes, no calculator, no notes. If a question
   requires remembering an exact formula, either state the formula in the paper
   (as the exams do for Dijkstra, Bellman-Ford and Counting-Sort) or drop it.

### Formulas and code always given in the paper

Never ask students to reproduce these from memory, past exams print them:

- The pseudocode of Dijkstra, Bellman-Ford, Counting-Sort, Partition.
- The IEEE 754 layout note ("8 bits for the exponent and a bias of 127").
- The definition of a min-heap and the index arithmetic
  (`left = 2x`, `right = 2x+1`, `parent = ⌊x/2⌋`).
- Pearson's correlation formula, when a distributed version is asked for.

Students **are** expected to know without prompting: number-base conversion,
Amdahl's law, O-notation and its formal definition, BFS/DFS, selection sort,
mergesort, quicksort, binary search, the automaton 5-tuple, and basic SQL.

---

## 4. Rotation

Two exams are written per year (final and resit), plus a released example. With
roughly 100 items in the pool and 20–24 subquestions used per year, an item can
safely return after **three years**.

Current state, by topic. "Unseen" counts items no cohort has met on an exam,
those tagged `new`, plus those drawn only from the 2026 exercise sheets
(`TE-NN`):

| Pool | Items | Unseen |
|---|---|---|
| 1 Information coding | 14 | 1 |
| 2 Data structures | 15 | 1 |
| 3 Algorithms and complexity | 17 | 1 |
| 4 Graphs and parallelization | 17 | 0 |
| 5 Theoretical CS | 14 | 2 |
| 6 Databases and applications | 16 | 6 |
| **total** | **93** | **11** |

Eleven unseen items is not enough to build a whole paper from, and it does not
need to be: at three years' rotation, the 2023 items are already free to reuse
for the 2026/27 cohort, which has never sat an ICSS exam. The unseen items are
best spent on the **discriminating** subquestion of each of the six questions,
with the trusted older items carrying the mechanical parts.

Beyond these, the **Additional practice** sections of the 2026 exercise sheets
(`../TheoryExercises/`) are a reservoir of exam-shaped items with worked
solutions that no cohort has seen. They are indexed at the end of each pool file.

---

## 5. Known coverage gaps

Worth deciding on before the 2026/27 exam:

- **Session 10 (Machine Learning) has never been examined.** The lecture has been
  in the course since 2024/25. Pool 6 now has items for it (`DB-10` to `DB-13`),
  all tagged `new`. Decide whether ML is examinable and tell the students either
  way, the exam review session is the place.
- **Session 13 (Social Science Applications) appears only once**, as the
  Schelling item `DB-14` in the 2025/26 example. Pool 6 has three more.
- **Session 4 (Software) is examined only indirectly**, through pseudocode. Its
  new sections on specifications and testing (2026/27) have no pool items yet.
  The one exception is `DS-14` (rewriting a slow Python loop), from 2024-E1.
  This seems right for a theory exam: the practical part examines programming.
- **Session 1 (Introduction) is never examined**, which is also fine.
- **Recursion** has thinned out: it was a question in 2023 (Euclid) and is now
  only a subquestion (BST minimum). If recursion matters, `DS-11`, `DS-12` and
  `DS-13` restore it, and `Exercise06.md` has more.

---

## 6. Cover sheet template

```
Introduction to Computing for the Social Sciences – <Final Exam | Resit Exam>
Prof. Dr. David Garcia
Winter Semester 20XX-XX

Exam Date: DD.MM.YYYY
Duration: 90 minutes
Total points: 60 points

Registration Number (Matrikelnummer): ________________________________

Instructions
 • Please make sure before you start that this exam contains, after this cover
   sheet, N single-sided printed pages with 6 questions in total. If you miss any
   page, call an examiner before you start.
 • Write your registration number before starting in a clearly readable way.
   Do not obscure or cross your registration number.
 • Please write the answers in the space provided between questions. If you need
   more space, leave a note on the space for the question and continue behind
   that page or behind the previous one. Please clearly indicate the question
   number and letter for the solution in this case.
 • Please only write solutions to the questions and refrain from writing any
   other comments or text not related to the questions.
 • Do not use an erasable pencil or a red pen.
 • The exam is closed book and no calculators are allowed.
 • Note that each question has subquestions that go in depth in each topic. Make
   sure you do not get stuck in any question and that you read and think about
   every question in the exam before the time is over.
 • The passing grade corresponds to 50% of the total: 30 points

For examiner only:
  Question | Points | Achieved
     1     |   10   |
     2     |   10   |
     3     |   10   |
     4     |   10   |
     5     |   10   |
     6     |   10   |
   total   |   60   |
```
