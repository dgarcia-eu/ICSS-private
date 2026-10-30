# Exercise Sheet 7: Sorting Algorithms

*Introduction to Computing for the Social Sciences · Prof. Dr. David Garcia*

> Exercises 1–3 are worked through in the exercise session. The *Additional
> practice* section is for self-study. Worked solutions to every exercise, with
> pointers to the slides and the handout sections that cover the material, are
> in [`Solutions/Exercise07-Solutions.md`](Solutions/Exercise07-Solutions.md); try before you open them.
> Notation: [course conventions](../Transcripts/00-Conventions.md).

---

## Exercise 1: Selection sort

a) Consider the following array:

$$[1,\; 2,\; 10,\; 4,\; 3,\; 7,\; 9,\; 11]$$

Show how **selection sort** reorders the array. Indicate each state of the array
in temporal sequence, marking which entries are compared and/or swapped in each
state.

b) Explain the advantages and disadvantages of selection sort compared to
   repeated minimum search.

---

## Exercise 2: Mergesort

a) Using the same array as in exercise 1, show how **merge sort** would sort it.
   Show the splitting phase and each merging step.

b) What is the advantage of mergesort compared to selection sort? Explain the
   reasoning behind your answer.

---

## Exercise 3: More sorting algorithms

Consider the pseudocode of **Bubblesort**:

```
Procedure BUBBLESORT(A)
 1  For i = 1 to length(A) - 1:
 2        For j = length(A) downto i + 1:
 3              If A[j] < A[j - 1]
 4                    then exchange A[j] with A[j - 1]
```

a) Show how it sorts the same array as in exercise 1.

b) Is it a stable sorting algorithm? Why?

> For (b), find the exact line that decides the answer, and construct a small
> input with two equal keys that proves your case.

---

## Additional practice

### A1. Stability in practice

You have a dataset of 10 000 social media posts with columns `user`, `timestamp`
and `text`.

a) You want it ordered by user, and within each user chronologically. In which
   order do you sort, and what property must the sort have?
b) Your language's sort is not stable. How can you still get the result you want?
c) Python's `sorted` is stable. Write the two lines that produce the ordering in
   (a).

### A2. Counting operations

For an array of $n$ elements:

a) How many **comparisons** does selection sort make? Does it depend on the
   input?
b) How many **swaps**?
c) How many comparisons does bubblesort make as written above? How could you
   improve it for nearly-sorted input?
d) How many comparisons does mergesort make at each level of recursion, and how
   many levels are there?

### A3. Mergesort by hand

Sort `[38, 27, 43, 3, 9, 82, 10]` with mergesort.

a) Draw the split tree.
b) Show every merge.
c) The array has 7 elements, an odd number. Where does the extra element go, and
   does it matter?

### A4. Quicksort and the pivot

Assume `PARTITION` always chooses the **last** element as the pivot.

a) Sort `[3, 1, 4, 1, 5, 9, 2, 6]` and show the pivot at each recursive call.
b) What happens on `[1, 2, 3, 4, 5, 6, 7, 8]`? How deep does the recursion go?
c) Why is that bad, and what do real implementations do about it?

### A5. Heaps

a) Is `[3, 9, 5, 10, 12, 6]` a valid min-heap? Check every node.
b) Insert 2 into it and restore the heap property.
c) Extract the minimum from the result and restore the heap property.
d) Why is the depth of a heap always about $\log_2 n$, while a BST's can be $n$?

### A6. Choosing an algorithm

Which sorting algorithm would you choose, and why?

a) 20 items, sorted by hand on paper in an exam.
b) 10 million records on disk, far more than fits in RAM.
c) A nearly-sorted list of 100 000 items that gains a few new entries daily.
d) Records so large that moving one is very expensive.
e) An embedded device with no spare memory at all.

### A7. Reasoning about lower bounds

a) Any sorting algorithm that works by comparing pairs of elements needs at least
   about $n \log_2 n$ comparisons in the worst case. Give an informal argument.
   *(Hint: how many possible orderings of $n$ items are there, and how much
   information does one comparison give? Session 2 has the tools.)*
b) Counting sort can sort $n$ integers in the range 0…$k$ in about $n + k$ steps
   faster than $n \log n$. Does that contradict (a)?

---

## Sources

- Exercises 1–3 are adapted from the 2023/24 sheet 7 of this course; the
  Bubblesort pseudocode has been reset in the course's notation.
- **Cormen, T. H. (2013).** *Algorithms Unlocked*, MIT Press, ch. 2–3.: Reading
  for this session.
- **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C. (2009).**
  *Introduction to Algorithms*, 3rd ed., ch. 2 (bubblesort is problem 2-2),
  ch. 6 (heapsort), ch. 7 (quicksort and pivot choice), ch. 8 (the
  $n \log n$ lower bound and counting sort, the source for A7).
- **Knuth, D. E. (1998).** *The Art of Computer Programming, Vol. 3*, 2nd ed.
- **Peters, T.** *Timsort*:
  <https://github.com/python/cpython/blob/main/Objects/listsort.txt>,
  background for A6(c).
- **Musser, D. R. (1997).** "Introspective Sorting and Selection Algorithms".
  *Software: Practice and Experience* 27(8).: Introsort, for A4(c).
