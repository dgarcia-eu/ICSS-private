# Lecture transcripts

Companion texts for the ICSS theory lectures. Each transcript follows its
lecture section by section and adds the explanations that were given out loud,
worked examples with every step shown, and *check yourself* questions with
answers. **They are meant to be studied from on their own**; you should not need
the books to follow them.

Start with the conventions page; everything else assumes it.

| | Session | Reading it is based on |
|---|---|---|
| | [Notation and pseudocode conventions](00-Conventions.md) | |
| 01 | [Introduction](01-Introduction.md) | Zelle ch. 1 |
| 02 | [Information Coding](02-InformationCoding.md) | Evans ch. 1 |
| 03 | [Data Structures](03-DataStructures.md) | Cormen et al. ch. 10 |
| 04 | [Software](04-Software.md) | Zelle ch. 2, 6–8; Guttag ch. 6 |
| 05 | [Algorithms](05-Algorithms.md) | Cormen ch. 1 |
| 06 | [Recursion](06-Recursion.md) | Zelle ch. 13 |
| 07 | [Sorting Algorithms](07-SortingAlgorithms.md) | Cormen ch. 2–3 |
| 08 | [Time Complexity](08-TimeComplexity.md) | Guttag ch. 9–10 |
| 09 | [Theoretical Computer Science](09-TheoreticalCS.md) | Sipser ch. 1; Evans ch. 6, 12; Cormen ch. 10 |
| 10 | [Machine Learning](10-MachineLearning.md) | Hastie, Tibshirani & Friedman ch. 2, 7, 14 |
| 11 | [Databases](11-Databases.md) | Course reading ch. 4; Garcia-Molina et al. |
| 12 | [Parallel Programming](12-ParallelProgramming.md) | Hennessy & Patterson; Dean & Ghemawat |
| 13 | [Social Science Applications](13-SocialScienceApplications.md) | Salganik, *Bit by Bit*; Lazer et al. |

Transcripts **02–12** open with a *Motivating examples* section carrying three
candidate openings for the lecture. That is a choice still to be made; see
[`../MotivatingExamples.md`](../MotivatingExamples.md); the unchosen ones will be
deleted.

## How they are put together

- **Figures are the ones from the slides.** They are referenced from
  `../Slides/figures/`, so a diagram here is exactly the diagram you saw in the
  lecture. If you move these files, keep the relative path.
- **Notation is consistent across all of them** and is defined once in
  [00-Conventions.md](00-Conventions.md). Pseudocode follows Cormen's
  *Algorithms Unlocked*; graph, automaton and complexity notation follows the
  standard in each field.
- **Sources are cited where they are used** and collected again at the end of
  each transcript. Anything taken from outside the course books, whether a paper,
  a blog post or a standard, is credited there.

## Rendering

They are plain Markdown with LaTeX maths and SVG figures, so they render on
GitHub and in most editors. To make a PDF or a website:

```bash
quarto render 03-DataStructures.md --to pdf
quarto render 03-DataStructures.md --to html
```
