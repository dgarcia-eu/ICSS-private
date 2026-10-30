#!/usr/bin/env python3
"""Emit the Quarto source of ICSS session 7 (Sorting Algorithms)."""

OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/07-SortingAlgorithms/ICSS-2026-07-SortingAlgorithms.qmd"

HEADER = '''---
title: "<span class='course'>Introduction to Computing for the Social Sciences</span><br><span class='session'>Session 7 &ndash; Sorting Algorithms</span>"
author: "David Garcia<br><span class='semester'>Winter Semester 2026-2027</span>"
format:
  revealjs:
    theme: [default, ../theme/unikn.scss]
    width: 1280
    height: 720
    margin: 0.06
    center: false
    slide-number: c
    show-slide-number: all
    progress: true
    controls: true
    history: true
    logo: ../theme/unikn-logo.png
    footer: "<span class='fbar-left'>Session 07</span><span class='fbar-mid'>Introduction to Computing for the Social Sciences</span><span class='fbar-right'>Winter Semester 2026-2027</span>"
    highlight-style: github
    link-external-newwindow: true
    fig-align: left
---

## Course Outline

:::: {.columns}
::: {.column width="50%"}
::: {.sm}
- Session 1: Introduction
- Session 2: Information Coding
- Session 3: Data Structures
- Session 4: Software
- Session 5: Algorithms
- Session 6: Recursion
- Session 7: Sorting Algorithms
:::
:::

::: {.column width="50%"}
::: {.sm}
- Session 8: Time Complexity
- Session 9: Theoretical Computer Science
- Session 10: Machine Learning (8.01)<br><span class="xs">K503, lecture 13:30-15:00, practice 15:15-16:45</span>
- Session 11: Databases
- Session 12: Parallel Programming
- Session 13: Social Science Applications
- Session 14: Exam Review
:::
:::
::::
'''

s = [HEADER]


def slide(title, body):
    s.append(f"\n## {title}\n\n{body}\n")


ITEMS = ["Sorting", "Iterative sorting: Selection sort",
         "Divide and Conquer: Mergesort and Quicksort",
         "Data structures for sorting: Heapsort"]


def outline(cur=None):
    marked = [f"[{t}]{{.current}}" if i + 1 == cur else t for i, t in enumerate(ITEMS)]
    cls = "{.outline .focus}" if cur else "{.outline}"
    body = "\n".join(f"{i+1}. {t}" for i, t in enumerate(marked))
    return f"::: {cls}\n{body}\n:::"


slide("Outline", outline())

# ------------------------------------------------------------------- motivation
slide("Sorting", """:::: {.columns}
::: {.column width="58%"}
![](figures/tiles-scattered.jpg){height="10.6em"}
:::

::: {.column width="42%"}
::: {.sm}
**Which numbers are duplicates?**
:::
:::
::::""")

slide("Sorting", """:::: {.columns}
::: {.column width="42%"}
![](figures/tiles-sorted.jpg){height="11.4em"}
:::

::: {.column width="58%"}
::: {.sm}
**Which numbers are duplicates?**
:::
:::
::::""")

slide("Sorting", """::: {.center-h .sm}
**Are the number sets different?**
:::

::: {.imgrow .middle}
![](figures/tiles-setA-scattered.jpg){height="8.4em"}
![](figures/tiles-setB-scattered.jpg){height="8.4em"}
:::""")

for _ in range(2):
    slide("Sorting", """::: {.center-h .sm}
**Are the number sets different?**
:::

::: {.imgrow .middle}
![](figures/tiles-setA-sorted.png){height="10.0em"}
![](figures/tiles-setB-sorted.png){height="10.0em"}
:::""")

slide("Sorting", """::: {.sm}
- **Fundamentals**
  - we are operating on:
    - set of objects $U$
    - set of keys $S$ with linear order relation $\\leq$ (i.e., a linearly ordered set)
    - sorting function that maps all objects $U$ to $S$ (i.e., $s: U \\rightarrow S$)
  - we are searching for a permutation of indices $i_1 \\dots i_n$ of the objects in $U$, such that:
:::

::: {.center-h}
$$\\forall\\, 1 \\leq i \\leq n-1: \\; s(u_i) \\leq s(u_{i+1})$$
:::""")

slide("Stable vs. unstable sorting", """::: {.xs}
- **Stable sorting methods**
  - different objects can have the same key value used for sorting, e.g., students with the exact same name
  - If a sorting algorithm, after sorting the contents, does not change the sequence of similar content in which they appear, it is called **stable** sorting. Otherwise it is **unstable** sorting.
  - stable sorting methods ensure that
    - objects with the same value for a given sorting function $s_1$ have different values for another function $s_2$
    - sorting according to $s_1$ in this case does not change the order of the objects
:::

:::: {.columns}
::: {.column width="30%"}
::: {.xs}
**example: sort by first name**

| | |
|---|---|
| 123456 | Christina |
| 234567 | Sandra |
| 345678 | Sandra |
| 456789 | Carl |
:::
:::

::: {.column width="30%"}
::: {.xs}
&nbsp;

| | |
|---|---|
| 456789 | Carl |
| 123456 | Christina |
| 234567 | Sandra |
| 345678 | Sandra |

**stable**
:::
:::

::: {.column width="30%"}
::: {.xs}
&nbsp;

| | |
|---|---|
| 456789 | Carl |
| 123456 | Christina |
| 345678 | Sandra |
| 234567 | Sandra |

**unstable**
:::
:::
::::""")

# ------------------------------------------------------------- iterative sorting
slide("Iterative sorting", outline(2))

slide("Iterative Sorting: Repeated Minimum Search", """::: {.sm}
**Sorting through selection as fundamental principle**

- intuitive strategy:
  - find maximum/minimum of a set and move it to front
  - iteratively apply the logic to the remaining set
- algorithmic strategy (**repeated minimum search**)
  - split list into two parts
    - sorted part on left, $L$
    - unsorted part on right, $R$
  - at start: sorted part is empty, i.e. $L = \\emptyset$, unsorted part $R$ is the entire list
  - find minimum in unsorted $R$ and append to sorted $L$
  - stop if $\\text{length}(R) = 1$
:::""")

slide("Repeated minimum search", """::: {.center-h}
![](figures/07-repeated-minimum.svg){height="12.6em"}
:::""")

SELSORT = """<pre class="pseudocode" style="width:74%"><i>Procedure</i> SELECTION-SORT(<i>A</i>, <i>n</i>)
<i>Inputs:</i>
  <i>A</i>: an array
  <i>n</i>: the number of elements in <i>A</i> to sort
<i>Result:</i> The elements of <i>A</i> are sorted into nondecreasing order
<b>For</b> i = 1 <b>to</b> n - 1:
      smallest &larr; i
      <b>For</b> j = i + 1 <b>to</b> n:
            <b>If</b> A[j] &lt; A[smallest],
                  <b>then</b> smallest &larr; j.
      Swap A[i] <b>with</b> A[smallest]</pre>"""

slide("Selection sort", SELSORT + """

::: {.source}
From *Algorithms Unlocked*. Thomas Cormen, 2013, p. 33-34
:::""")

slide("Selection sort", f""":::: {{.columns}}
::: {{.column width="74%"}}
{SELSORT.replace(' style="width:74%"', '')}
:::

::: {{.column width="26%"}}
::: {{.tag .xs}}
Find the smallest in R
:::

<br><br>

::: {{.tag .xs}}
Swap it to be the last of L
:::
:::
::::

::: {{.source}}
From *Algorithms Unlocked*. Thomas Cormen, 2013, p. 33-34
:::""")

slide("Selection sort example", """::: {.center-h}
![](figures/07-selection-sort.svg){height="12.6em"}
:::""")

slide("Repeated minimum search vs selection sort", """::: {.xs}
**Characteristics of iterative sorting algorithms**

- both algorithms are **partially correct**
  - any element still in $R$ is larger or equal to any in $L$, $L$ is sorted
- both algorithms **terminate**
  - remaining part $R$ shrinks in every step, eventually it has to have length 1
- different use depending on data structure of list:
  - repeated minimum appends in the middle of the list: better for **linked lists**
  - selection sort uses swaps: better for **arrays**
- **stability**:
  - repeated minimum is *stable*:
    - in case of ambiguity, takes the first minimum in $R$
    - this always correctly preserves any other ordering
  - selection sort is *unstable*:
    - swapping does not necessarily preserve other ordering in $R$
:::""")

slide("Outtake &ndash; Social Science Applications", """::: {.sm}
**Why should we care about sorting?**

- Sorting for the sake of sorting
  - we are sorting data more often than we think
  - especially for data science applications complex data often needs to be sorted to be analyzed or shown
  - in practice, speed matters here for analysts and users
  - sorting is healthy: it helps to notice data issues
- Sorting for searching
  - many search algorithms require sorted sets of data to work (e.g., binary search)
  - it is in practice much easier to find items in an ordered than an unordered list
:::

::: {.refresh}
Exercise: write the pseudocode of repeated minimum search
:::""")

# --------------------------------------------------------- divide and conquer
slide("Divide and Conquer", outline(3))

slide("Divide and Conquer", """:::: {.columns}
::: {.column width="46%"}
::: {.sm}
- Fundamental algorithmic principle inspired by military history: *divide et impera*
  - separate a problem into separate sub-problems
  - continue until those sub-problems are solvable
  - then recombine partial results to full solution
:::
:::

::: {.column width="54%"}
![](figures/07-divide-and-conquer.svg){height="11.4em"}
:::
::::""")

slide("Divide and Conquer", """::: {.sm}
**Divide and conquer $\\neq$ recursion**

- it is not the same as recursion, i.e., recursive calls of the same function
- recursion is a natural implementation strategy for algorithms following a divide and conquer approach
  - by definition, the sub-problems in divide and conquer are self-similar
  - generate overall solution by combining solutions of sub-problems
- BUT we can also implement a divide and conquer strategy iteratively
:::""")

slide("Mergesort", """::: {.sm}
- **Mergesort** first divides the list into equal halves and then combines them in a sorted manner. Mergesort sorts by *merging* (sub-)lists
- principle:
  - a list with one element is trivially sorted
  - merging two sorted lists is simple:
    - compare first element of each sub-list
    - append smaller of the two to merged list and remove from sub-list
    - continue with remaining sub-lists
- algorithmic strategy
  - repeated division of list until just one element is remaining per list
  - repeated merging of sorted sub-lists until only one sorted list remains
:::""")

slide("Mergesort", """<pre class="pseudocode" style="width:88%"><i>Procedure</i> MERGE-SORT(<i>A</i>, <i>p</i>, <i>r</i>)
<i>Inputs:</i>
      <i>A</i>: an array
      <i>p</i>, <i>r</i>: the starting and ending index of the subarray
<i>Result:</i> The elements of the subarray A[p..r] are sorted into nondecreasing order
<b>If</b> p &ge; r,
      <b>then</b> the subarray A[p..r] has at most one element and is already sorted.
      Just return without doing anything.
<b>else</b>
      q &larr; ⌊(p + r) / 2⌋.
      Recursively call MERGE-SORT(A, p, q).
      Recursively call MERGE-SORT(A, q + 1, r).
      MERGE(A, p, q, r).</pre>

::: {.source}
From *Algorithms Unlocked*. Thomas Cormen, 2013, p. 42-43
:::""")

slide("The MERGE function", """<pre class="pseudocode" style="width:82%"><i>Procedure</i> MERGE(<i>A</i>, <i>p</i>, <i>q</i>, <i>r</i>)
<i>Inputs:</i>
      <i>A</i>: an array
      <i>p</i>, <i>q</i>, <i>r</i>: indices of sorted subarrays A[p … q], A[q+1 … r]
<i>Result:</i> A[p … r] contains both sorted subarrays fully sorted
B &larr; copy(A[p … q]); C &larr; copy(A[q+1 … r]);
i &larr; 1; j &larr; 1;
<b>For</b> k = p <b>to</b> r:
      <b>If</b> B[i] &le; C[j],
            <b>then</b> A[k] &larr; B[i];
                  i &larr; i+1
            <b>else</b> A[k] &larr; C[j];
                  j &larr; j+1</pre>""")

slide("MERGE example", """::: {.center-h}
![](figures/07-merge-1.svg){height="10.6em"}
:::""")
slide("MERGE example", """::: {.center-h}
![](figures/07-merge-2.svg){height="10.6em"}
:::""")

slide("Mergesort", """::: {.sm}
- **Mergesort split:** first divides the whole list iteratively into equal halves (no change in sequence of items in the original) until atomic values are achieved.
:::

::: {.center-h}
![](figures/07-mergesort-split.svg){height="8.0em"}
:::""")

for k in (1, 2, 3):
    slide("Mergesort", f"""::: {{.sm}}
- **Mergesort algorithm** &ndash; merge them into another list in a sorted manner
:::

::: {{.center-h}}
![](figures/07-mergesort-merge-{k}.svg){{height="{2.2 * (k + 1):.1f}em"}}
:::""")

slide("Mergesort", """::: {.sm}
**Mergesort as a divide and conquer strategy**

- **Divide:** splitting into two sub-lists (with half the size)
  - recursive implementation of sub-list sorting
    - call mergesort on itself
    - assume that output is a sorted list in each recursion step
    - requires well-defined base case (= list with one element)
- **Combine:** merging two lists preserving order
  - systematic and efficient merger of partial lists to one large sorted list
  - see *Algorithms Unlocked* (Cormen, 2013) for MERGE pseudocode
:::""")

slide("Mergesort", """::: {.sm}
**Characteristics of mergesort**

- **correctness**
  - merge steps sort correctly
  - no changing of order outside of merging
  - all elements are sorted and algorithm terminates
- **memory and stability**
  - need additional memory (in addition to list) for handling sub-lists
  - stable algorithm because other ordering structure is preserved during merging
:::""")

slide("John von Neumann: more than mergesort's father", """:::: {.columns}
::: {.column width="68%"}
::: {.sm}
**John von Neumann** (Neumann János Lajos, Budapest, 1903-1957)

- One of the most influential figures of Computer Science, Math, and Physics in the 20th century
- Inventor of the mergesort algorithm
- Among the first to talk about the time complexity of algorithms in the 1950s
- Popularized the modern computer architecture with main memory, ALU, registries, etc.
- Proposed cellular automata that self-replicated
- Warned about anthropogenic global warming as early as 1955
:::
:::

::: {.column width="32%"}
![](figures/von-neumann.png){height="9.4em"}
:::
::::""")

slide("Quicksort", """::: {.sm}
- Similar divide and conquer logic to mergesort but division into sub-lists not necessarily regular
- **Quicksort rationale:**
  - pick **pivot** element from list
  - sort list such that all elements left (right) of pivot are smaller (larger) than its value
  - after this **partition** operation the pivot element is already in its final (sorted) position, sorting now occurs only right/left of the pivot element
  - split list at pivot and apply logic recursively to left and right sub-list
:::""")

slide("Quicksort", """<pre class="pseudocode" style="width:76%;margin:0.6em auto"><i>Procedure</i> QUICK-SORT(<i>A</i>, <i>p</i>, <i>r</i>)
<i>Inputs and Result:</i> Same as MERGE-SORT
<b>If</b> p &ge; r,
      <b>then</b> return without doing anything
<b>else</b>
      q &larr; PARTITION(A, p, r)
      Recursively call QUICK-SORT(A, p, q - 1)
      Recursively call QUICK-SORT(A, q + 1, r)</pre>""")

slide("The PARTITION function", """::: {.center-h}
![](figures/cormen-partition.png){height="9.6em"}
:::

::: {.refresh}
Exercise: run quicksort on pen and paper on the same example as mergesort
:::""")

slide("Quicksort: properties", """::: {.sm}
- **advantages**
  - very memory efficient
  - in-place procedure: is (usually) faster than merge sort
- **disadvantages**
  - efficiency depends on choice of pivot and the partition scheme chosen (more next week)
- **differences from mergesort:**
  - in quicksort all the heavy lifting is done while dividing the array into subarrays, while in mergesort all the real work happens during merging the subarrays
  - in quicksort, the combine step does absolutely nothing
:::""")

# ---------------------------------------------------------------------- heaps
slide("Data structures for sorting", outline(4))

HEAP_TEXT = """::: {.sm}
- partially ordered binary trees without gaps (or holes)
  - children of any node not larger than the node
  - not a binary search tree, i.e., just require local ordering of nodes and children. All levels filled, last filled from the left
:::"""

slide("Heaps", f"""::: {{.sm}}
- Search algorithms can use data structures for help: **heaps** as an example
:::

{HEAP_TEXT}

::: {{.sm}}
- example: does this tree satisfy the heap property?
:::

::: {{.center-h}}
![](figures/07-heap-example.svg){{height="7.0em"}}
:::""")

slide("Heaps", f"""{HEAP_TEXT}

::: {{.sm}}
- example: does this tree satisfy the heap property? &nbsp;&nbsp; **No** &ndash; 8 is larger than its parent 4
:::

::: {{.center-h}}
![](figures/07-heap-example.svg){{height="7.0em"}}
:::""")

slide("Heaps", f"""{HEAP_TEXT}

::: {{.sm}}
- Heap property can be efficiently "recovered"
:::

::: {{.imgrow .middle}}
![](figures/07-heap-fix-1.svg){{height="6.4em"}}
![](figures/07-heap-fix-2.svg){{height="6.4em"}}
![](figures/07-heap-fix-3.svg){{height="6.4em"}}
:::""")

MINHEAP_TEXT = """::: {.sm}
- Same as a heap but:
  - children of any node not **smaller** than the node
  - All levels filled, last filled from the left
:::"""

slide("Min-Heaps", MINHEAP_TEXT + """

::: {.center-h}
![](figures/07-min-heap.svg){height="9.4em"}
:::""")

slide("Min-Heaps", MINHEAP_TEXT + """

::: {.center-h}
![](figures/07-min-heap-array.svg){height="10.4em"}
:::""")

slide("Heapsort", """::: {.sm}
- **conceptual foundation:**
  - in a min-heap the smallest element is on top
  - children are not smaller because of heap property
  - same is recursively true for the entire tree
  - we can start by building a heap of the list
- **idea:**
  - remove the top (smallest) element from tree
  - replace it with the last element of the tree
  - recover the heap property through permuting elements
:::""")

CAPTIONS = None
import importlib.util
spec = importlib.util.spec_from_file_location(
    "gen07", "/tmp/claude-1000/-home-dgarcia-Dropbox-Teaching-Konstanz/"
             "ae14631a-a710-45c4-83e5-f88e31d81a65/scratchpad/gen07.py")
# recompute the captions without re-writing the SVGs
MINHEAP = [2, 4, 14, 10, 8, 15, 18, 17, 11, 16]


def sift_down(a, i):
    n = len(a)
    l, r = 2 * i + 1, 2 * i + 2
    m = i
    if l < n and a[l] < a[m]:
        m = l
    if r < n and a[r] < a[m]:
        m = r
    if m == i:
        return None
    a[i], a[m] = a[m], a[i]
    return m


heap, out, caps, first = list(MINHEAP), [], [], True
while heap:
    caps.append("Extract top (minimum)<br>and place it first" if first else "Extract min")
    first = False
    out.append(heap[0])
    if len(heap) == 1:
        break
    heap[0] = heap[-1]
    heap.pop()
    caps.append("Move last to top")
    i = 0
    while True:
        j = sift_down(heap, i)
        if j is None:
            break
        caps.append("Recover min-heap<br>property")
        i = j

for k, cap in enumerate(caps):
    slide("Heapsort: Example", f""":::: {{.columns}}
::: {{.column width="76%"}}
![](figures/07-heapsort-{k:02d}.svg){{height="12.4em"}}
:::

::: {{.column width="24%"}}
::: {{.tag .xs}}
{cap}
:::
:::
::::""")

slide("Heapsort: Pseudocode", """::: {.center-h}
![](figures/cormen-heapsort.png){height="9.0em"}
:::

::: {.source}
See *Algorithms Unlocked* (Cormen, 2013, p. 98)
:::

::: {.refresh}
Exercise: what is the pseudocode to build a heap and of EXTRACT-MIN? Is Heapsort stable?
:::""")

slide("To learn more about sorting", """:::: {.columns}
::: {.column width="52%"}
<pre class="pseudocode"><i>Procedure</i> ICan'tBelieveItCanSort(<i>A</i>, <i>n</i>)
<i>Inputs:</i>
  <i>A</i>: an array
  <i>n</i>: the number of elements in <i>A</i> to sort
<i>Result:</i> The elements of the array are sorted
into nondecreasing order
<b>For</b> i = 1 <b>to</b> n:
      <b>For</b> j = 1 <b>to</b> n:
            <b>If</b> A[i] &lt; A[j],
                  <b>then</b> swap A[i] <b>with</b> A[j].</pre>

::: {.xs}
*Is this the simplest (and most surprising) sorting algorithm ever?* Stanley Fung, 2021
:::
:::

::: {.column width="48%"}
![](figures/sorting-visualisation.png){height="8.0em"}

::: {.source}
<https://www.youtube.com/watch?v=kPRA0W1kECg>
:::
:::
::::""")

slide("Next Session", """1. Time complexity
2. O-notation""")

open(OUT, "w").write("".join(s))
print("slides:", "".join(s).count("\n## "))
