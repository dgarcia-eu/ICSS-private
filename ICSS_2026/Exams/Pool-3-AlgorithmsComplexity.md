# Pool 3: Algorithms, Sorting and Complexity

*Exam question pool · sessions 5, 7 and 8 · typically **question 3** (and
sometimes 4), 10–12 points.*
See [README](README.md) for the item format, [Blueprint](Blueprint.md) for
assembly.

---

## AC-01 · The h-index · 3 pts · [2025-E1 Q3a]

> The **h-index** of a scientist is a number that summarizes their scientific
> impact based on the number of citations to their published articles. The
> h-index is defined as the maximum value of $h$ such that the given researcher
> has published at least $h$ articles that have each been cited at least $h$
> times. For example, Prof. Garcia has an h-index of 52 in Google Scholar because
> he has at least 52 articles there with at least 52 citations, but not 53
> articles with at least 53 citations.
>
> Write the pseudocode of an algorithm that calculates the h-index of a
> scientist. The algorithm receives as input an array of length $N$ with the
> number of citations of each of the articles of the scientist **in any order**.

**Solution.**

```
Procedure H-INDEX(C)
Inputs:
      C: an array C[1..N] with the citation count of each article
Result: the h-index of the scientist
sort C in decreasing order
h ← 0
For i = 1 to N:
      If C[i] ≥ i
            then h ← i
            else return h         # once the test fails it can never hold again
return h
```

After sorting, `C[i] ≥ i` says "there are at least $i$ articles with at least $i$
citations". The largest $i$ for which this holds is the h-index. The early
`return` is sound because `C` is non-increasing while $i$ grows, so once `C[i] < i` the
condition fails for every larger $i$.

*Worked example:* `C = [3, 0, 6, 1, 5]` sorts to `[6, 5, 3, 1, 0]`.
$C[1]=6\ge 1$ ✓, $C[2]=5\ge 2$ ✓, $C[3]=3\ge 3$ ✓, $C[4]=1 < 4$ ✗ → **h = 3**.

**Notes.** Accept a version without the early return (it just scans the whole array),
and accept an unsorted $O(N^2)$ version that counts, for each candidate $h$, how
many articles pass, but then `AC-02` must be marked consistently with what the
student actually wrote.

---

## AC-02 · Complexity of the h-index algorithm · 2 pts · [2025-E1 Q3b]

> Based on your pseudocode above, describe the time complexity of your algorithm
> using O-notation.

**Solution.** $\mathbf{O(N \log N)}$, dominated by the sort. The scan afterwards
is a single pass over at most $N$ elements, $O(N)$, and $O(N \log N) + O(N) =
O(N \log N)$.

**Worth an extra point if mentioned:** the sort is not necessary. Since the
h-index can never exceed $N$, you can bucket the citation counts, one bucket per
value $0..N$, with everything above $N$ counted in bucket $N$, and then sweep the
buckets from high to low accumulating the count. That is counting sort applied to
a bounded range and runs in $\mathbf{O(N)}$, beating the comparison-sort lower
bound because it does not compare (see `AC-10`).

---

## AC-03 · Memory requirements of the h-index algorithm · 2 pts · [2025-E1 Q3c]

> Describe in your own words the memory requirements of your algorithm as a
> function of the size of the input.

**Solution.** The input itself is $N$ numbers, so $O(N)$. Beyond that the
algorithm needs only the loop counter `i` and the variable `h`, two numbers,
independent of $N$, so the **additional** memory is $\mathbf{O(1)}$ *if* the sort
is done in place (heapsort, or quicksort's in-place partition).

If sorting produces a copy, mergesort, or Python's `sorted()`, the extra memory
is $O(N)$. The counting variant of `AC-02` also needs $O(N)$ for the buckets: it
buys time with space.

**Notes.** The distinction the question is after is **input size versus
additional working memory**, and whether the chosen sort is in place. A bare
"$O(N)$" with no reasoning gets one point.

---

## AC-04 · Formal O-notation argument · 3 pts · [2023-Ex Q3d, 2025-E1 Q3d, 2025-E2 Q3d]

> We have an algorithm with running time that grows with the size of the problem
> $n$ following the function $f(n) = 345\,n^3$. Is this function in
> $O(n^2 \log n)$? Explain your answer **formally**.

**Solution.** **No.**

By definition, $f(n) \in O(g(n))$ iff there exist constants $c > 0$ and
$n_0 \ge 1$ such that $f(n) \le c\,g(n)$ for all $n \ge n_0$.

Suppose such $c$ and $n_0$ existed. Then for all $n \ge n_0$
$$345\,n^3 \le c\,n^2 \log n \quad\Longleftrightarrow\quad \frac{345\,n}{\log n} \le c .$$
But $n/\log n \to \infty$ as $n \to \infty$, so the left-hand side eventually
exceeds any fixed $c$, a contradiction. Hence no such constants exist and
$345\,n^3 \notin O(n^2 \log n)$.

Equivalently: $\lim_{n\to\infty} \dfrac{345\,n^3}{n^2\log n} = \infty$, which
rules out membership in $O$.

**Variants.**

| Source | Question | Answer |
|---|---|---|
| 2025-E2 Q3d | Is $345\,n^2\log n \in O(n^5)$? | **Yes.** For $n \ge 2$, $\log n \le n$, so $345 n^2\log n \le 345 n^3 \le 345 n^5$. Take $c = 345$, $n_0 = 2$. |
| 2023-Ex Q3d | Is $200n + 1\,000\,000 \in O(n^3)$? | **Yes.** For $n \ge 100$ we have $1\,000\,000 \le n^3$ and $200n \le 200n^3$, so $f(n) \le 201\,n^3$. Take $c = 201$, $n_0 = 100$. |
| 2023-E1 Q3c / 2024-Ex Q3c | Is $k$-th-smallest with $k=1$ in $O(N^2)$? | **Yes**, see `AC-14`. |

**Notes.** Both directions appear in the pool on purpose. The "yes" cases are
easier: exhibit $c$ and $n_0$ and you are done. The "no" case needs the
contradiction or the limit, a student who only says "$n^3$ grows faster than
$n^2 \log n$" has the right intuition and has not answered "formally", which is
worth about half the points.

Constants and lower-order terms never matter: $345$ is absorbed by $c$, and
$1\,000\,000$ is absorbed by choosing $n_0$ large enough. Say so.

---

## AC-05 · Selection sort trace · 2–3 pts · [2023-Ex Q3a, 2023-E2 Q3a, 2025-E1 Q4a]

> Consider the following array: `[1, 2, 10, 4, 3, 7, 9, 11]`.
> Show how **selection sort** reorders the array. Indicate each state of the
> array in temporal sequence, marking what entries are compared and/or swapped in
> each state of the array.

**Solution.** Selection sort finds the minimum of the unsorted suffix and swaps
it into position $i$.

| $i$ | Unsorted suffix | Minimum | Swap | Array after |
|---|---|---|---|---|
| 1 | positions 1–8 | 1 (pos 1) | none | `[1, 2, 10, 4, 3, 7, 9, 11]` |
| 2 | positions 2–8 | 2 (pos 2) | none | `[1, 2, 10, 4, 3, 7, 9, 11]` |
| 3 | positions 3–8 | **3** (pos 5) | 3 ↔ 5 | `[1, 2, `**`3`**`, 4, `**`10`**`, 7, 9, 11]` |
| 4 | positions 4–8 | 4 (pos 4) | none | `[1, 2, 3, 4, 10, 7, 9, 11]` |
| 5 | positions 5–8 | **7** (pos 6) | 5 ↔ 6 | `[1, 2, 3, 4, `**`7`**`, `**`10`**`, 9, 11]` |
| 6 | positions 6–8 | **9** (pos 7) | 6 ↔ 7 | `[1, 2, 3, 4, 7, `**`9`**`, `**`10`**`, 11]` |
| 7 | positions 7–8 | 10 (pos 7) | none | `[1, 2, 3, 4, 7, 9, 10, 11]` |

Sorted: `[1, 2, 3, 4, 7, 9, 10, 11]`. **Three swaps**, and $\binom{8}{2} = 28$
comparisons regardless of the input.

**Variant** [2023-Ex Q3a], array `[1, 2, 10, 4, 3, 7, 9]`: the same first three
steps, then $i=5$ swaps 7 into place and $i=6$ swaps 9 into place, giving
`[1, 2, 3, 4, 7, 9, 10]` in two swaps after the first.

**Notes.** The array is chosen so that most positions need no swap, students who
have memorized "swap at every step" get it wrong immediately. Insist on the
*comparisons*, not only the swaps: the point of selection sort is that it always
does $\Theta(n^2)$ comparisons even on sorted input.

---

## AC-06 · Selection sort versus repeated minimum search · 2 pts · [2023-Ex Q3b, 2023-E2 Q3b, 2025-E1 Q4b]

> Explain the advantages and disadvantages of selection sort compared to repeated
> minimum search.

**Solution.** *Repeated minimum search* means: find the minimum of the array,
remove it and append it to a new output array; repeat.

**Advantage of selection sort:** it is **in place**. It swaps the minimum into
position $i$ within the same array, needing only $O(1)$ extra memory, whereas
repeated minimum search needs a second array of size $n$ and must physically
remove elements from the first, which, in an array, costs $O(n)$ shifting per
removal and so raises the total from $O(n^2)$ to the same order but with a much
larger constant.

**Disadvantage of selection sort:** it is **not stable**. Swapping a distant
minimum into position $i$ jumps over intervening elements and can reverse the
relative order of records with equal keys. Repeated minimum search, which appends
in the order found, preserves it. Selection sort is also harder to read.

Both perform the same $\Theta(n^2)$ comparisons and neither adapts to
already-sorted input.

**Notes.** Accept "same time complexity, better memory" plus one further point.
The stability answer is the strongest and is worth remarking on in the exam
review, since it is why mergesort is preferred in libraries.

---

## AC-07 · Complexity of selection sort from its pseudocode · 3 pts · [2023-Ex Q3c]

> What is the time complexity of selection sort in O-notation? Explain how you
> reach your answer **from the pseudocode** of selection sort.

**Solution.**

```
Procedure SELECTION-SORT(A)
Inputs:
      A: an array of n elements
Result: A sorted in increasing order
For i = 1 to n − 1:                     # outer loop: n − 1 iterations
      min ← i
      For j = i + 1 to n:               # inner loop: n − i iterations
            If A[j] < A[min]
                  then min ← j
      swap A[i] with A[min]             # O(1)
```

The inner loop runs $n-i$ times for each $i$, so the total number of comparisons
is
$$\sum_{i=1}^{n-1}(n-i) = (n-1) + (n-2) + \cdots + 1 = \frac{n(n-1)}{2}$$
which is $\Theta(n^2)$, and each iteration does constant work. The $n-1$ swaps
are $O(n)$ and do not change the order. Hence
$\mathbf{O(n^2)}$, and in fact $\Theta(n^2)$ in **best, average and worst
case**, since the loop bounds do not depend on the data at all.

**Notes.** The "explain from the pseudocode" instruction means the summation is
the answer, not the assertion. The best-case remark distinguishes selection sort
from insertion sort, and connects to `AC-12`.

---

## AC-08 · Mergesort trace and its advantage · 5 pts · [2023-E2 Q3c+d]

> a) Using the array `[1, 2, 10, 4, 3, 7, 9, 11]`, show how **merge sort** would
>    sort it.
> b) What is the advantage of mergesort compared to selection sort? Explain the
>    reasoning behind your answer.

**Solution.**
a) Divide to single elements, then merge upwards.

```
                [1, 2, 10, 4, 3, 7, 9, 11]
                 /                      \
        [1, 2, 10, 4]               [3, 7, 9, 11]
         /        \                  /         \
     [1, 2]     [10, 4]           [3, 7]      [9, 11]
     /   \       /   \            /   \        /   \
   [1]   [2]  [10]   [4]        [3]   [7]    [9]   [11]

merge:  [1,2]      [4,10]        [3,7]       [9,11]
merge:      [1,2,4,10]               [3,7,9,11]
merge:            [1,2,3,4,7,9,10,11]
```

The last merge in detail, comparing the heads of the two runs `[1,2,4,10]`
and `[3,7,9,11]`: 1 and 2 come from the left run, 3 from the right, 4 from the
left, 7 and 9 from the right, 10 from the left, and 11 is copied at the end.
Seven comparisons for eight elements; 15 in the whole sort, against the 28 of
selection sort.

b) **Mergesort is $O(n \log n)$ while selection sort is $O(n^2)$.**
The reasoning is in the recursion: mergesort halves the problem, so the
recursion tree has $\log_2 n$ levels, and each level merges a total of $n$
elements in linear time, hence $n \log n$. Selection sort, by `AC-07`, does
$n(n-1)/2$ comparisons: it re-scans the whole remaining array to find each
minimum, and never uses the work of the previous scan. For $n = 10^6$ the
difference is roughly $2\times 10^7$ operations against $5 \times 10^{11}$.

Mergesort is also **stable** and parallelizes naturally, since the two recursive
calls work on disjoint halves (session 12). Its cost is $O(n)$ extra memory for
the merge, where selection sort is in place.

---

## AC-09 · Counting-Sort trace · 3 pts · [2025-E1 Q4c]

> Counting-Sort takes an array of integers $A$ (indexed between 1 and
> `A.length`) and stores a sorted version of it in $B$. The range of values
> allowed in $A$ is from 0 to $k$.
>
> ```
> COUNTING-SORT(A, B, k)
>  1  let C[0..k] be a new array
>  2  for i = 0 to k
>  3      C[i] = 0
>  4  for j = 1 to A.length
>  5      C[A[j]] = C[A[j]] + 1
>  6  // C[i] now contains the number of elements equal to i.
>  7  for i = 1 to k
>  8      C[i] = C[i] + C[i − 1]
>  9  // C[i] now contains the number of elements less than or equal to i.
> 10  for j = A.length downto 1
> 11      B[C[A[j]]] = A[j]
> 12      C[A[j]] = C[A[j]] − 1
> ```
>
> Show how Counting-Sort sorts the following array for $k = 4$:
> `[1, 3, 0, 3, 1]`. Write the changes that take place on the arrays $B$ and $C$.

**Solution.**

**After the counting loop (lines 4–5)**: `C[i]` = how many elements equal $i$:

| index | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| C | 1 | 2 | 0 | 2 | 0 |

**After the prefix loop (lines 7–8)**: `C[i]` = how many elements are $\le i$:

| index | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| C | 1 | 3 | 3 | 5 | 5 |

**The placement loop (lines 10–12)**, right to left:

| $j$ | $A[j]$ | $C[A[j]]$ | Write | $B$ so far | $C$ after |
|---|---|---|---|---|---|
| 5 | 1 | 3 | $B[3] \leftarrow 1$ | `[_,_,1,_,_]` | `[1,2,3,5,5]` |
| 4 | 3 | 5 | $B[5] \leftarrow 3$ | `[_,_,1,_,3]` | `[1,2,3,4,5]` |
| 3 | 0 | 1 | $B[1] \leftarrow 0$ | `[0,_,1,_,3]` | `[0,2,3,4,5]` |
| 2 | 3 | 4 | $B[4] \leftarrow 3$ | `[0,_,1,3,3]` | `[0,2,3,3,5]` |
| 1 | 1 | 2 | $B[2] \leftarrow 1$ | `[0,1,1,3,3]` | `[0,1,3,3,5]` |

$B = \mathbf{[0, 1, 1, 3, 3]}$ ✓

**Notes.** Two details are worth a point each: the prefix sums turn *counts* into
*positions*, and the last loop runs **downto 1** so that equal keys keep their
original relative order, that is what makes Counting-Sort **stable**, which
matters when it is used as the inner sort of radix sort.

---

## AC-10 · Counting-Sort complexity versus QuickSort · 3 pts · [2025-E1 Q4d]

> What is the time efficiency of Counting-Sort in O-notation? Explain your answer
> and how it compares to the time efficiency of QuickSort.

**Solution.** Reading the pseudocode: the initialization loop runs $k+1$ times,
the counting loop $n$ times, the prefix loop $k$ times and the placement loop $n$
times, each with constant-time bodies. Total:
$$\mathbf{O(n + k)}$$
where $n$ = `A.length` and $k$ = the largest allowed value. It is **linear in
$n$** when $k = O(n)$, and worse than useless when $k \gg n$, sorting five
32-bit integers would allocate a counting array of four billion entries.

**Compared with QuickSort:** QuickSort is $O(n \log n)$ on average and $O(n^2)$ in
the worst case. So for $k = O(n)$ Counting-Sort is asymptotically **faster** than
any comparison sort.

That does not contradict the $\Omega(n \log n)$ lower bound for sorting, because
that bound applies only to **comparison-based** sorts. Counting-Sort never
compares two elements: it uses each value directly as an *array index*, which is
extra information about the input, namely that the values are small integers.
QuickSort makes no assumption about the values and works on anything with an
order.

Counting-Sort also needs $O(n + k)$ extra memory, where QuickSort sorts in place
with $O(\log n)$ stack space.

**Notes.** The comparison-lower-bound point is the discriminating one and should
carry at least one of the three points. Connect it to `AC-02`: the same trick
gives a linear-time h-index.

---

## AC-11 · QuickSort from a given Partition · 2 pts · [2025-E2 Q3a]

> Remember the pseudocode of the `Partition` function for QuickSort *(printed in
> the exam)*:
> ```
> PARTITION(A, p, r)
>  1  x = A[r]
>  2  i = p − 1
>  3  for j = p to r − 1
>  4      if A[j] ≤ x
>  5          i = i + 1
>  6          exchange A[i] with A[j]
>  7  exchange A[i + 1] with A[r]
>  8  return i + 1
> ```
> Write the pseudocode of QuickSort using the `Partition` function provided
> above.

**Solution.**

```
Procedure QUICKSORT(A, p, r)
Inputs:
      A: an array
      p, r: the bounds of the subarray to sort
Result: A[p..r] is sorted in place
If p < r
      then q ← PARTITION(A, p, r)
           QUICKSORT(A, p, q − 1)
           QUICKSORT(A, q + 1, r)
```

Call it as `QUICKSORT(A, 1, A.length)`.

**Notes.** Two points, and both are easy to lose. (i) The base case is `p < r`,
not `p ≤ r`, with `≤` the algorithm never terminates on a single element.
(ii) The pivot at position `q` is **excluded** from both recursive calls, because
`Partition` has already put it in its final position; recursing on `(p, q)` and
`(q, r)` gives infinite recursion.

---

## AC-12 · QuickSort worst case · 3 pts · [2025-E2 Q3b]

> What is the time complexity of QuickSort in its worst-case scenario? Explain
> the rationale of your answer.

**Solution.** $\mathbf{O(n^2)}$.

`Partition` always costs $\Theta(m)$ on a subarray of size $m$, it scans it once.
The total therefore depends entirely on how the subarray sizes shrink. In the
**worst case** the pivot is the smallest or largest element of every subarray, so
each partition splits $m$ into a part of size $m-1$ and an empty part. The
recurrence is
$$T(n) = T(n-1) + \Theta(n)$$
whose solution is $\Theta(n^2)$, the same $n + (n-1) + \cdots + 1$ sum as
selection sort in `AC-07`. The recursion is also $n$ levels deep, so the stack
usage becomes $O(n)$.

With the `Partition` above, which takes the **last** element as pivot, this
happens precisely on **already sorted or reverse-sorted input**, the most common
case in practice, which is the joke of it.

In the best and average cases the pivot splits the array roughly evenly, giving
$T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$.

**The standard fix** is to choose the pivot randomly, or as the median of the
first, middle and last elements, which makes the worst case vanishingly unlikely
without changing the algorithm.

---

## AC-13 · QuickSort trace · 3 pts · [2025-E2 Q3c]

> Consider the following array: `[8, 2, 3, 4, 5, 6, 7, 1]`.
> Show how quicksort reorders the array. Indicate each state of the array in
> temporal sequence, marking what entries are swapped in each state of the array.
> Clearly identify the calls to `Partition` and `QuickSort` as the algorithm
> runs.

**Solution.** With `Partition` taking `A[r]` as pivot.

**`QUICKSORT(A, 1, 8)` on `[8, 2, 3, 4, 5, 6, 7, 1]`**
`PARTITION(A, 1, 8)`: pivot $x = A[8] = 1$, $i = 0$.
No element of `A[1..7]` is $\le 1$, so the loop never advances $i$.
Line 7 exchanges `A[1]` with `A[8]`: **8 ↔ 1**.
→ `[1, 2, 3, 4, 5, 6, 7, 8]`, returns $q = 1$.

**`QUICKSORT(A, 1, 0)`**, empty, returns immediately.

**`QUICKSORT(A, 2, 8)`**
`PARTITION(A, 2, 8)`: pivot $x = A[8] = 8$. Every element of `A[2..7]` is $\le 8$,
so $i$ advances with $j$ and every exchange is an element with itself. Line 7
exchanges `A[8]` with `A[8]`. → array unchanged, returns $q = 8$.

**`QUICKSORT(A, 2, 7)`**: pivot $A[7] = 7$, again the maximum → $q = 7$, no
change.
**`QUICKSORT(A, 2, 6)`**: pivot 6 → $q = 6$.
**`QUICKSORT(A, 2, 5)`**: pivot 5 → $q = 5$.
**`QUICKSORT(A, 2, 4)`**: pivot 4 → $q = 4$.
**`QUICKSORT(A, 2, 3)`**: pivot 3 → $q = 3$.
**`QUICKSORT(A, 2, 2)`**: $p = r$, returns.

**Final array: `[1, 2, 3, 4, 5, 6, 7, 8]`**, sorted after the very first
exchange, with **exactly one swap** in the whole run.

**But it took 7 calls to `Partition` and 7 levels of recursion**, because after
the first partition the array is sorted and every subsequent pivot is the maximum
of its subarray, exactly the worst case described in `AC-12`. Total comparisons
$\approx n^2/2$ to sort an array that was one swap away from sorted.

**Notes.** Print the `PARTITION` pseudocode of `AC-11` with this item, since the
trace depends on it (last element as pivot). This is the best item in the pool for showing that a correct answer
and an efficient one are different things. Mark the *recursion structure*, not
just the final array: a student who writes "sorted after the first swap" and
stops has missed the question.

---

## AC-14 · The $k$-th smallest element · 3+2+3+3 pts · [2023-E1 Q3a–d, 2024-Ex Q3a–d]

> a) Write the pseudocode of an algorithm that finds the $k$-th smallest element
>    in any list by doing $k$ searches for the smallest element.
> b) Run it over the following list for $k = 3$. Show any intermediate states of
>    the list and the final result: `10 12 1 8 4 7 33 54`
> c) Assuming $k = 1$ and $N$ is the length of the list, is the runtime of the
>    above algorithm $O(N^2)$? Explain your answer formally.
> d) Consider a situation in which the possible values of $k$ tend to grow with
>    $N^{0.5}$. Explain in your own words how you would modify your pseudocode to
>    make it more time-efficient, and explain your rationale.

**Solution.**

a)
```
Procedure KTH-SMALLEST(L, k)
Inputs:
      L: a list of N comparable elements
      k: an integer with 1 ≤ k ≤ N
Result: the k-th smallest element of L
For t = 1 to k:
      m ← 1
      For j = 2 to L.length:
            If L[j] < L[m]
                  then m ← j
      smallest ← L[m]
      If t < k
            then remove L[m] from L
return smallest
```

b) `L = [10, 12, 1, 8, 4, 7, 33, 54]`, $k = 3$.

| Pass | Minimum found | List after removal |
|---|---|---|
| 1 | **1** | `[10, 12, 8, 4, 7, 33, 54]` |
| 2 | **4** | `[10, 12, 8, 7, 33, 54]` |
| 3 | **7** | *(not removed, this is the answer)* |

**Result: 7.**

c) **Yes.** With $k = 1$ the outer loop runs once and the inner loop does $N-1$
comparisons, so $f(N) = N - 1 + c'$ for some constant $c'$ of bookkeeping.
Take $c = 1$ and $n_0 = c' + 2$: for all $N \ge n_0$ we have $c' \le N - 2$,
so $N - 1 + c' \le 2N \le N^2$ (the last step because $N \ge 2$). Hence
$f(N) \in O(N^2)$.

The point of the question is that **$O$ is an upper bound, not a tight one**.
$f(N) \in O(N)$ as well, and $O(N)$ is the tight bound ($f(N) \in \Theta(N)$),
but membership in $O(N^2)$ is still a true statement. A student who answers "no,
it is $O(N)$" has confused $O$ with $\Theta$.

d) With $k \sim \sqrt{N}$ the algorithm costs $k \cdot N \approx N^{1.5}$, which
grows faster than $N \log N$. So **sort the list once and index it**: $O(N \log
N)$ for the sort and $O(1)$ to read off element $k$, total $O(N \log N)$, which
beats $N^{1.5}$ for large $N$. Sorting also makes any *further* order-statistic
query free, whereas the repeated-minimum version pays again for each one.

A better answer still: use a **max-heap of size $k$**, scan the list once,
keeping the $k$ smallest seen so far; the answer is the heap's root. That is
$O(N \log k) = O(N \log \sqrt{N}) = O(N \log N)$ time, with half the constant
of the sort, and only $O(k)$ memory. (Or Quickselect, which is $O(N)$ on average.)

**Notes.** This four-part item is a complete 11-point question 3 on its own, and
it has been used twice unchanged. Part (c) is the most instructive question in
the whole pool about what O-notation means.

---

## AC-15 · Posts, comments and users · 2+2+2+3+3 pts · [2024-E1 Q3a–e, 2025-Ex Q3a–e]

> As part of a new research project, you have gathered data from millions of
> posts, comments and users. `uid` refers to unique ids of users and `post_id` to
> unique ids of posts. **The data is not sorted by any criteria.**
> ```
> posts = [                comments = [                users = [
>   {"id": 1,                {"id": 4,                   {"uid": 11, "name": "..."},
>    "text": "...",           "text": "...",             {"uid": 12, "name": "..."},
>    "timestamp": 1092,       "timestamp": 703,          {"uid": 13, "name": "..."}
>    "tags": [1, 2, 3],       "uid": 11,                 ...
>    "uid": 10},              "post_id": 2},            ]
>   ...                      ...
> ]                        ]
> ```
> a) Write the pseudocode of an algorithm that returns only the posts that were
>    created by users that are in your users list.
> b) We denote $P$ as the number of posts, $C$ as the number of comments and $U$
>    as the number of users. Is the runtime of your algorithm above in
>    $O(U^2P^3 + C^4)$? Explain your answer in your own words.
> c) Is there an algorithm to solve the above problem with complexity $O(P + U)$?
>    If yes, explain in your own words how it achieves that runtime.
> d) Assume you have discarded the posts not created by users in your list. You
>    are only interested in the comments created within the time window between
>    timestamps $t_1$ and $t_2$, with $t_2 > t_1$. Write pseudocode that, for each
>    post, returns a list of all the comments made within that window.
> e) Explain how sorting comments by timestamp as part of the pseudocode can
>    increase the efficiency of solving the previous task. Describe a situation in
>    which sorting the comments is *less* efficient than processing them unsorted.

**Solution.**

a) The direct version, and the one most students write:
```
Procedure FILTER-POSTS(posts, users)
Inputs:
      posts: a list of posts, each with the id uid of its author
      users: a list of users, each with an id uid
Result: the posts whose author is in the users list
result ← empty list
For each p in posts:
      found ← FALSE
      For each u in users:
            If p.uid = u.uid
                  then found ← TRUE
      If found
            then append p to result
return result
```
This is $O(P \cdot U)$.

b) **Yes.** $O$ is an **upper bound**: $P\cdot U \le U^2P^3 + C^4$ for all
$P, U, C \ge 1$, so the runtime is certainly in that class. But the bound is
grossly loose and therefore uninformative, it would also hold for an algorithm
billions of times slower. The **tight** statement is $\Theta(P \cdot U)$. Note
also that $C$ does not appear in the algorithm at all; a bound containing $C^4$
is describing a resource the algorithm never uses.

c) **Yes**, with a **hash set**:
```
Procedure FILTER-POSTS-FAST(posts, users)
Inputs:
      posts, users: as in FILTER-POSTS
Result: the posts whose author is in the users list
U ← empty hash set
For each u in users:                    # O(U)
      add u.uid to U
result ← empty list
For each p in posts:                    # O(P)
      If p.uid ∈ U                      # O(1) on average
            then append p to result
return result
```
Building the set is one pass over the users; each membership test is $O(1)$
average because the hash function computes the slot directly instead of scanning.
Total $O(P + U)$ time and $O(U)$ extra memory, the same time/space trade as
`AC-02` and `DS-14`.

d)
```
Procedure COMMENTS-IN-WINDOW(posts, comments, t1, t2)
Inputs:
      posts: the filtered posts
      comments: all comments, each with a post_id and a timestamp
      t1, t2: the bounds of the window, t1 < t2
Result: a table mapping each post id to the list of its comments in [t1, t2]
M ← empty hash table whose entries default to an empty list
For each c in comments:                       # one pass, O(C)
      If t1 ≤ c.timestamp and c.timestamp ≤ t2
            then append c to M[c.post_id]
R ← empty hash table
For each p in posts:                          # O(P)
      R[p.id] ← M[p.id]                       # an empty list if absent
return R
```
$O(C + P)$, again by indexing rather than searching. The naive version, for each
post, scan all comments, is $O(P \cdot C)$.

e) **How sorting helps.** If the comments are sorted by timestamp, the ones in
$[t_1, t_2]$ form a **contiguous block**. Binary search finds each boundary in
$O(\log C)$ and the block is read directly, so a query costs $O(\log C + k)$ for
$k$ results instead of $O(C)$. With $Q$ different time windows to examine, the
total is $O(C \log C + Q(\log C + k))$ rather than $O(Q \cdot C)$, the sort is
paid once and amortized over all queries.

**When sorting is worse.** When the task is done **once**. A single linear scan
is $O(C)$; sorting first is $O(C \log C)$, so you have paid a $\log C$ factor for
nothing. It is also worse when the window contains most of the comments (there is
nothing to skip), when the data arrives as a stream that cannot be sorted, or
when $C$ is so large that the sort does not fit in memory. **Sorting is an
investment: it pays off only if you query more than once.**

**Notes.** This five-part item is a complete question. Parts (b) and (e) carry
the conceptual weight and are where marks separate; (a), (c) and (d) are
mechanical for anyone who has done the exercise sheets.

---

## AC-16 · Building a comment network · 3+2+3+2 pts · [2024-E2 Q3a–d]

> Using the same `posts`, `comments` and `users` data as above:
> a) Write the pseudocode of an algorithm that creates a list with the number of
>    posts of each user.
> b) Is there an algorithm to solve (a) with complexity $O(P + U)$? If yes,
>    explain how.
> c) You want to visualize a directed network in which nodes are users and there
>    is an edge from user $a$ to user $b$ if user $a$ commented at least once on a
>    post written by user $b$. Edges have a weight that is the number of times $a$
>    commented on posts of $b$. Write the pseudocode of an algorithm that builds a
>    new data structure with the information necessary to visualize the edges.
> d) Describe the time complexity of your algorithm for (c) in terms of the number
>    of posts, comments and users. Use O-notation and explain your answer.

**Solution.**

a) and b), one pass with a hash table:
```
Procedure POSTS-PER-USER(posts, users)
Inputs:
      posts: a list of posts, each with the id uid of its author
      users: a list of users, each with an id uid
Result: a table count mapping each user id to the number of posts of that user
count ← empty hash table whose entries default to 0
For each u in users:                    # O(U), so that users with 0 posts appear
      count[u.uid] ← 0
For each p in posts:                    # O(P)
      count[p.uid] ← count[p.uid] + 1
return count
```
**Yes, $O(P + U)$**: each of the two loops runs once over its list and every hash
operation is $O(1)$ on average. The first loop matters: without it, users who posted
nothing are missing from the result rather than recorded as zero.

c)
```
Procedure COMMENT-NETWORK(posts, comments)
Inputs:
      posts: a list of posts, each with an id and the id uid of its author
      comments: a list of comments, each with the id uid of its author and a post_id
Result: a table W mapping (commenter, author) pairs to a weight
author ← empty hash table
For each p in posts:                          # O(P)
      author[p.id] ← p.uid
W ← empty hash table whose entries default to 0
For each c in comments:                       # O(C)
      b ← author[c.post_id]
      If b ≠ NIL and b ≠ c.uid                # skip self-comments
            then W[(c.uid, b)] ← W[(c.uid, b)] + 1
return W
```
`W` is a weighted **edge list** keyed by the ordered pair, exactly the structure
a visualization tool needs.

d) $\mathbf{O(P + C)}$. The first loop is one pass over the posts, the second one
pass over the comments, and each hash lookup or update is $O(1)$ average. $U$
does not appear, because the users list is never consulted, the authorship
information is already in the posts. Memory is $O(P + E)$ where $E \le C$ is the
number of distinct edges.

**Notes.** The lookup table `author` in (c) is the same *index-don't-search*
move as in `AC-15c` and `DS-14`; students who have understood it once get all
three. The `b ≠ c.uid` guard (people comment on their own posts constantly) is a
good half-point.

---

## AC-17 · Complexity of the algorithms in this course · 3 pts · `new`

> Fill in the table with the worst-case time complexity in O-notation, and for
> each row give the one-sentence reason.
>
> | Algorithm | Worst case | Why |
> |---|---|---|
> | Linear search in an array of $n$ | | |
> | Binary search in a sorted array of $n$ | | |
> | Selection sort | | |
> | Mergesort | | |
> | Quicksort | | |
> | Breadth-first search on $G = (V, E)$ | | |
> | Lookup in a hash table of $n$ | | |
> | Insertion in a min-heap of $n$ | | |

<details><summary>Solution</summary>

| Algorithm | Worst case | Why |
|---|---|---|
| Linear search | $O(n)$ | The target may be last, or absent. |
| Binary search | $O(\log n)$ | The range halves at every step; $\log_2 n$ halvings reach one element. |
| Selection sort | $O(n^2)$ | $n$ passes, each scanning the remaining suffix: $n(n-1)/2$ comparisons regardless of input. |
| Mergesort | $O(n \log n)$ | $\log n$ levels of halving, $O(n)$ merging work per level. |
| Quicksort | $O(n^2)$ | An extreme pivot every time gives splits of size $n-1$ and 0; average is $O(n\log n)$. |
| BFS | $O(\|V\| + \|E\|)$ | Each vertex is enqueued once and each edge examined once (twice if undirected). |
| Hash table lookup | $O(n)$ | Worst case all keys collide into one chain; **average $O(1)$**. |
| Min-heap insertion | $O(\log n)$ | The new element bubbles up at most the height of a nearly-complete tree. |

</details>

**Notes.** A fast, wide item that is hard to bluff: the "why" column stops
students from reciting a memorized table. Use it as the closing subquestion of
question 3 when the anchor item is a trace.

---

## Also available from the 2026 exercise sheets

| Sheet | Contents | Suitable as |
|---|---|---|
| [`Exercise05.md`](../TheoryExercises/Exercise05.md) | Algorithm definition, flowcharts, pseudocode, search, BFS | Constructive 3–5 point items |
| [`Exercise07.md`](../TheoryExercises/Exercise07.md) | Selection sort, mergesort, quicksort, heapsort, stability, lower bound | Trace and comparison items |
| [`Exercise08.md`](../TheoryExercises/Exercise08.md) | A1 code→complexity, A2 formal proofs, A3 best/average/worst, A4 recurrences, A5 real code, A6 the course's algorithms, A7 memory complexity | A2 and A4 are directly reusable as `AC-04`-style items with different functions |

Sheet 8's A4 (recurrences) covers ground no exam has touched: $T(n) = 2T(n/2) +
n$, $T(n) = T(n-1) + n$, $T(n) = T(n/2) + 1$. Solving a recurrence would be a
good 3-point subquestion for a cohort that has seen `AC-04` recently.
