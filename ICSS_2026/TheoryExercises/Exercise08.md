# Exercise Sheet 8: Time Complexity

*Introduction to Computing for the Social Sciences · Prof. Dr. David Garcia*

Exercises 1 to 3 will be covered in the exercise session. The *Additional practice* section is for self-study and to be covered if time allows.

---

## Exercise 1: Algorithmic complexity

a) What is the time complexity of **repeated minimum search** in O-notation?
   Explain how you reach your answer from the pseudocode of the algorithm.

b) Using O-notation, describe the time complexity of **Bellman-Ford** (see
   the exercise sheet of the Algorithms session). Explain your answer based on
   its pseudocode.

---

## Exercise 2: A complexity example

a) Write the pseudocode of an algorithm that finds the $k$-th smallest element in
   any list by doing $k$ searches for the smallest element.

b) Assuming that $k = 1$ and $N$ is the length of the list, is the runtime of the
   above algorithm $O(N^2)$? Explain your answer **formally**.

c) Consider a situation in which the possible values of $k$ tend to grow with
   $N^{0.5}$, where $N$ is the length of the list. Explain in your own words how
   you would modify your pseudocode to make it more time-efficient, and explain
   your rationale for the improvement.

For (b), remember that $O$ is an **upper** bound. The question is whether this
bound is valid and not what the tightest bound is. Answering it formally means
giving the constants $c$ and $n_0$ from the definition.

---

## Exercise 3: O-notation

a) We have an algorithm whose running time grows with the size of the problem $n$
   following the function $f(n) = 200n + 1{,}000{,}000$. Is this function in
   $O(n^3)$? Explain your answer formally.

b) We have an algorithm whose running time grows with the size of the problem $n$
   following the function $f(n) = e^n$. Is this function in $O(n^n)$? Explain
   your answer formally.

---

## Additional practice

### A1. From code to complexity

Give the time complexity of each piece of code in O-notation in terms of
$n$ = `len(data)` and justify it in one sentence.

```python
# (a)
total = 0
for x in data:
    total += x

# (b)
for x in data:
    for y in data:
        if x == y:
            count += 1

# (c)
for x in data:
    if x in lookup_list:      # lookup_list is a list of length n
        hits += 1

# (d)
for x in data:
    if x in lookup_set:       # lookup_set is a set of length n
        hits += 1

# (e)
i = n
while i > 1:
    i = i // 2
```

### A2. Formal proofs

Prove or disprove each claim and give constants $c$ and $n_0$ where the claim is true.

a) $3n^2 + 5n + 2 \in O(n^2)$
b) $n^3 \in O(n^2)$
c) $n \log n \in O(n^2)$
d) $2^{n+1} \in O(2^n)$
e) $2^{2n} \in O(2^n)$

### A3. Best, average, worst

For each algorithm, state the best-, average- and worst-case complexity and give
the input that produces each extreme.

a) Linear search in an unsorted array.
b) Binary search in a sorted array.
c) Insertion sort.
d) Selection sort.
e) Quicksort with the last element as pivot.

### A4. Recurrences

Solve each recurrence by unrolling it, as we did for mergesort.

a) $T(n) = T(n/2) + c$, with $T(1) = c$. *(binary search)*
b) $T(n) = 2T(n/2) + cn$, with $T(1) = c$. *(mergesort)*
c) $T(n) = T(n-1) + cn$, with $T(1) = c$. *(quicksort, worst case)*
d) $T(n) = 2T(n-1) + c$, with $T(1) = c$. *(naive Fibonacci-like recursion)*

### A5. Reasoning about real code

You inherit a script that took 3 minutes on 10,000 rows. Your new dataset has
1,000,000 rows.

a) If the script is $O(n)$, estimate the new runtime.
b) If it is $O(n^2)$, estimate it.
c) You measure the actual runtime on 20,000 and 40,000 rows and get 12 minutes
   and 48 minutes. What is the complexity and what do you predict for
   1,000,000 rows?
d) Your supervisor suggests renting a machine that is 10 times faster. Comment on this suggestion.

### A6. Complexity of the algorithms in this course

Fill in the table from memory and then check your answers.

| Algorithm | Session | Time complexity |
|---|---|---|
| Binary search | Data Structures | |
| Search in a balanced BST | Data Structures | |
| Search in a hash table (average) | Data Structures | |
| BFS | Algorithms | |
| DFS | Recursion | |
| Naive recursive Fibonacci | Recursion | |
| Memoized Fibonacci | Recursion | |
| Selection sort | Sorting Algorithms | |
| Mergesort | Sorting Algorithms | |
| Quicksort (average / worst) | Sorting Algorithms | |
| Heapsort | Sorting Algorithms | |

---

## Sources

- Exercises 1–3 are adapted from the 2023/24 Time Complexity sheet of this course.
- **Guttag, J. V. (2016).** *Introduction to Computation and Programming Using
  Python*, 2nd ed., MIT Press, ch. 9–10. Reading for this session.
- **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C. (2009).**
  *Introduction to Algorithms*, 3rd ed., ch. 3 (asymptotic notation, source of
  the formal definitions used in A2) and ch. 4 (recurrences, A4).
- **Cormen, T. H. (2013).** *Algorithms Unlocked*, ch. 1–2, 6.
- **Python time complexity of built-in operations:**
  <https://wiki.python.org/moin/TimeComplexity>, the reference behind A1(c–d).
- **Big-O cheat sheet:** <https://www.bigocheatsheet.com/>, a useful poster for
  A6, but do not trust it over your own derivation.
