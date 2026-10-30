# Session 3: Data Structures

*Introduction to Computing for the Social Sciences · lecture transcript*

**Reading for this session:** Chapter 10 of Cormen, Leiserson, Rivest & Stein,
*Introduction to Algorithms* (2009). References at the end.

---

## Contents

0. [Motivating examples](#motivating-examples)
1. [What a data structure is, and why it matters](#1-what-a-data-structure-is-and-why-it-matters)
2. [Arrays](#2-arrays)
3. [Linked lists](#3-linked-lists)
4. [The trade-off: editing versus searching](#4-the-trade-off-editing-versus-searching)
5. [Binary search](#5-binary-search)
6. [Binary trees and binary search trees](#6-binary-trees-and-binary-search-trees)
7. [Operations on a BST](#7-operations-on-a-bst)
8. [Hashing and hash tables](#8-hashing-and-hash-tables)
9. [Dictionaries](#9-dictionaries)
10. [Why this matters for social science](#10-why-this-matters-for-social-science)
11. [Check yourself](#11-check-yourself)
12. [References](#12-references)

---

## Motivating examples

### A · Two million respondents, one duplicate

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
million million. Even at ten million comparisons per second, this would take over two days. Now the same
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
That single move, to stop searching and start indexing, is the most valuable skill you
will learn in this session and it will recur often in later sessions.

### B · Six thousand rows, and the answer in thirteen steps

Recoding is the other unglamorous constant of empirical work. You have 40
million observations carrying an occupation code, a region code or a product
number, and a codebook of 6,000 entries that says what each code means. The
straightforward loop checks the codebook entries one after another until it
finds a match. On average that is half the codebook, 3,000 comparisons, and
6,000 in the worst case; times 40 million observations, it is on the order of
$10^{11}$ comparisons, which is an overnight job. If the codebook is sorted,
binary search applies: look at the middle entry, decide whether the target is
in the left or in the right half, and repeat. Each step halves the range, so
the number of steps is $\lceil \log_2 6\,000 \rceil = 13$. With this, the whole recoding effort
drops from $10^{11}$ comparisons to about $5 \times 10^8$, from overnight to
under a minute.
That is a factor of 460 for free, except that it is not totally free and this session you will learn what is the cost.
The list has to be sorted, which
costs something up front and session 07 will help us understand how much.

---

## 1. What are data structures?

A *data structure* is a set of data types together with the operations defined
on them that enable and realize access and management of that data. The
word "together" is the important one in this definition. A data structure is
not just a way of laying data out in memory; it is a layout plus a set of
operations, and the layout is chosen to make those operations have some desired properties, like speed.
Every structure in this lecture stores the same thing (a collection of items) and the
only thing that distinguishes them is the cost of the operations we perform on
the collection, such as looking something up, inserting something, and deleting
something. There is no universally best data structure. There is a best structure
for a given pattern of operations, and choosing it is a real engineering
decision.

Each item in these collections has a *key*, the part we search by, such as a
respondent ID or a name, and a *value*, the content stored with it, such as
the answers of that respondent. A search is not just to check whether a key
is there, it can also be used to retrieve the value stored with the key. Diagrams in this session
often show only the keys, assuming that the values are implicit.

![Four data structures, with keys and values](../Slides/03-DataStructures/figures/03-data-structures.svg)

The table below summarizes what we will find in this session; we
fill in the reasoning below and make "instant" and "slow" precise in session 8.

| Structure | Look up by index | Look up by key | Insert / delete |
|---|---|---|---|
| Array | instant | slow | slow |
| Linked list | slow | slow | fast |
| Binary search tree | not possible | fast (if balanced) | fast |
| Hash table | not possible | usually instant | usually instant |

---

## 2. Arrays

An *array* is a systematic arrangement of similar objects, usually in rows and
columns. We access its elements by *index*. In most programming languages the
indices of an array of length $n$ run from $0$ to $n-1$; in MATLAB, in R and in
our pseudocode they run from $1$ to $n$, as explained in the
[conventions](00-Conventions.md).

![An array with indices](../Slides/03-DataStructures/figures/03-array.svg)

The great advantage of an array is very fast access: if you know the index, one
operation is enough, because the address of `A[i]` is computed arithmetically
from the address of `A[1]` and the size of an element, with no searching
involved. Arrays are also the standard structure implemented in every language.
They have three disadvantages, and each of them motivates one of the structures
that follow. First, the memory requirement depends on the range of index values
and not on how many things you store: if you have 4 entries whose indices happen
to be spread between 1 and 1,000,000, you need 1,000,000 cells, and all but
four of them are empty but still use memory. Second, if you
fill the array linearly, inserting or removing an element in the middle either
leaves gaps or requires moving the rest of the content. Third, indices must be
integers, so you cannot index an array by a student's name.

![Four values in an array of 1,000,000 cells](../Slides/03-DataStructures/figures/03-array-gaps.svg)

---

## 3. Linked lists

A *linked list* is a linear collection of data elements, called *nodes*, each
pointing to the next node by means of a *pointer*. A node holds a key, with its
data, and a pointer `next` to the following node; the list is reached through a
pointer `head` to the first node, and the last node points to NIL. The list is
held together by the pointers and not by being contiguous in memory. Keys can
be anything that can be checked for equality, not necessarily integers: strings,
for example, or other pointers.

![A linked list](../Slides/03-DataStructures/figures/03-linked-list.svg)

This makes a linked list easy and cheap to edit: deleting a node only changes
the pointer of its predecessor, and inserting a node only changes the pointers
of its neighbors, so nothing has to be shifted.

![Deleting a node from a linked list](../Slides/03-DataStructures/figures/03-linked-list-delete.svg)

 Memory grows only with the
number of nodes and not with the range of any index. The price is paid on the
other operations. A linked list is hard to index, because there is no
arithmetic that gets you to the 500th element and you must follow 500 pointers
to reach it. It is slow to iterate through for the same reason, and also
because the nodes may be scattered in memory, which is bad for the cache of the
processor. And the pointers themselves have to be stored, which costs memory.

---

## 4. The trade-off: editing versus searching

Put side by side, the two structures have complementary weaknesses. Linked
lists have efficient editing but very slow, linear search: to find a value you
look at every node until you find it. Arrays have fast access by index but
inefficient editing. This raises the question that drives the rest of the
lecture: can we have a search that is faster than linear, but still allows
editing without moving all the data? There is a partial answer available
immediately. If a list is sorted, we can search it cleverly by halving the
search space at every step. That is binary search, and it is the idea that
binary search trees will later make dynamic. Remember that we do not search
just for keys: we also retrieve the values associated with them.

![Editing versus searching in a sorted array and a linked list](../Slides/03-DataStructures/figures/03-edit-vs-search.svg)

In a sorted array we can jump to any index by position, but inserting 8 in
position 4 means shifting 9, 13 and 21 one place to the right. In a linked list,
inserting 8 changes two pointers, but searching means following every pointer
from the head.

---

## 5. Binary search

```
Procedure BINARY-SEARCH(A, n, x)
Inputs:
      A: a sorted array
      n: the number of elements in A
      x: the value to find
Result: an index i with A[i] = x, or NOT-FOUND if x is not in A
p ← 1; r ← n
While p ≤ r:
      q ← ⌊(p + r)/2⌋
      If A[q] = x
            then return q
      else if A[q] > x
            then r ← q - 1
      else p ← q + 1
return NOT-FOUND
```

The variables $p$ and $r$ bracket the part of the array that could still
contain $x$, and $q$ is the middle of that bracket. Each comparison throws away
half of what is left. As a worked example, let us find 43 in the sorted array
`15 28 30 34 36 43 62 73 81 82`. In the first step $p=1$ and $r=10$, so $q =
\lfloor 11/2 \rfloor = 5$; since $A[5] = 36 < 43$, positions 1 to 5 are
discarded and $p$ becomes 6. In the second step $p=6$ and $r=10$, so $q = 8$;
since $A[8] = 73 > 43$, positions 8 to 10 are discarded and $r$ becomes 7. In
the third step $p=6$ and $r=7$, so $q = 6$, and $A[6] = 43$ is the value we are
looking for, so the procedure returns 6.

The figures show the three pointers in every step; a pointer that has just been
updated is drawn in orange, and the grey cells are the part of the array that
has been discarded.

![Binary search, first steps](../Slides/03-DataStructures/figures/03-binary-search-steps-1.svg)

![Binary search, found](../Slides/03-DataStructures/figures/03-binary-search-steps-2.svg)

That is three comparisons instead of up to ten. In general binary search needs
about $\log_2 n$ comparisons, which is why doubling the data adds only one
step. The catch is that the array has to be sorted, and keeping a sorted array
sorted under insertion means shifting elements, so we have fast search and slow
editing again. The fix is to stop storing the order in the positions and start
storing it in the pointers.

---

## 6. Binary trees and binary search trees

A *binary tree* is a tree data structure that is either empty or consists of a
node, the *root* $S$, with at most two children, the left child $L$ and the
right child $R$, both of which are themselves binary trees. Note that the
definition is recursive: a tree is defined in terms of trees. Session 6 makes
that pattern its main topic, but it is already doing work here, because it
means that any algorithm on a tree can be written as "do something to the root,
then do the same thing to the two subtrees". The vocabulary is the one of a
family tree. The root is the top node, a *leaf* is a node with no children,
parent and child are the two ends of an edge, siblings share a parent, and a
*subtree* is a node together with everything below it.

![A binary tree with terminology](../Slides/03-DataStructures/figures/03-binary-tree.svg)
![Legend](../Slides/03-DataStructures/figures/03-tree-legend.svg)

A *binary search tree* (BST) is a binary tree with comparable keys in which the
key at the root has to be

- larger than or equal to all keys in the left subtree, and
- strictly smaller than all keys in the right subtree,

and the same holds recursively at every node. Two housekeeping notes: every element has a key and
attached data, where the key is what we order by and the data is what we
actually want, and in this course we assume that there are no duplicate keys.

![A binary search tree](../Slides/03-DataStructures/figures/03-bst-base.svg)

The BST property is a condition on every node, not just on the root, and it is
worth seeing it applied level by level. At the root, everything in the left
subtree is at most 10 and everything in the right subtree is greater than 10.
At the second level, the same holds for 4 and for 13 with respect to their own
subtrees, and so on down to the leaves.

![The rule at the root](../Slides/03-DataStructures/figures/03-bst-root-rule.svg)

![The rule at the second level](../Slides/03-DataStructures/figures/03-bst-level2-rule.svg)

![The rule at the third level](../Slides/03-DataStructures/figures/03-bst-level3-rule.svg)

The lecture then asks whether the following tree is a binary search tree.

![A tree that is not a BST](../Slides/03-DataStructures/figures/03-bst-not-a-bst.svg)

It is not, and it breaks the rule in three places, circled in red. The node 15
is the left child of 13, but a left child must be at most 13. The node 5 is the
left child of 2 and in the left subtree of 4, but it is larger than both. And
the node 11 is the right child of 15, but a right child must be strictly
greater than 15.

![The violations](../Slides/03-DataStructures/figures/03-bst-not-a-bst-marked.svg)

Checking whether a tree is a
BST means checking the property at every node against all of its ancestors,
and this local-versus-global reasoning is exactly the kind of question the
exam likes.

---

## 7. Operations on a BST

### Searching

To search for a key, compare it with the root. If it is smaller, continue in
the left subtree; if it is larger, continue in the right subtree; and when you
run out of tree, the key is not there. Searching for 11 in the tree of the
lecture takes three steps: $11 > 10$ at the root, so we go right; $11 < 13$, so
we go left; and $11 = 11$, so we have found it. This is binary search again,
but now the halving is built into the shape of the structure rather than
computed from indices.

![Searching for 11](../Slides/03-DataStructures/figures/03-bst-search-11.svg)

### Inserting

To insert a key, assuming that it is not already in the tree, search for it.
The search will run out of tree at some empty position, and that empty
position is where the new key is added, as a leaf. This is the only place it
can go without breaking the BST property. Adding 6 to the tree of the lecture,
$6 < 10$ sends us left, $6 > 4$ sends us right, $6 < 9$ sends us left, and
since 9 has no left child, 6 becomes it.

![Before inserting 6](../Slides/03-DataStructures/figures/03-bst-base.svg)
![After inserting 6](../Slides/03-DataStructures/figures/03-bst-with-6.svg)

### Deleting

Deleting a key has three cases, in increasing difficulty. In the first case
the node is a leaf: search for the key, then remove the reference to it in its
parent. Deleting the leaf 6 that we just inserted returns the tree to its
original form.

![Deleting the leaf 6](../Slides/03-DataStructures/figures/03-bst-delete-6.svg)
![After deletion](../Slides/03-DataStructures/figures/03-bst-base.svg)

In the second case the node has one child, and it is replaced by that child.
The whole subtree of the child keeps satisfying the property, because it was
already on the correct side of everything above. In the lecture's example, 11
has the single child 12, so deleting 11 makes 12 the left child of 13.

![Deleting 11, which has one child](../Slides/03-DataStructures/figures/03-bst-delete-onechild-before.svg)
![12 takes its place](../Slides/03-DataStructures/figures/03-bst-delete-onechild-after.svg)

In the third case the node has two children, and this is the interesting one.
The node is replaced with either the leftmost node of its right subtree, which
is its *successor*, the smallest key larger than it, or with the rightmost
node of its left subtree, which is its *predecessor*. Either choice preserves
the ordering, because that node is by construction between the two subtrees in
value. Then the node that was moved is deleted from its old position, which is
a deletion of the first or the second kind, since the leftmost node of a
subtree cannot have a left child. Deleting the root 10 of the example, the
leftmost node of the right subtree is 11, so 11 becomes the root; 11 had one
child, 12, so we finish with a deletion of the second kind and 12 moves up.

![Deleting the root](../Slides/03-DataStructures/figures/03-bst-delete-root-a.svg)
![11 moves up](../Slides/03-DataStructures/figures/03-bst-delete-root-b.svg)
![12 fills the gap](../Slides/03-DataStructures/figures/03-bst-delete-root-c.svg)

### Advantages and applications

In a binary search tree, lookup is much faster than in an unsorted array and as
fast as binary search on a sorted array, while adding and removing values is
much faster than in a sorted array, because only pointers are updated, as in a
linked list, instead of shifting every element to the right of the key. That
is the answer to the question of [section
4](#4-the-trade-off-editing-versus-searching): a BST gives logarithmic search
and cheap editing at the same time. In practice BSTs are used for lookup
tables and dynamic sets, that is, collections that change in size but still
need efficient bookkeeping of their keys, and they are most useful when the key
is paired with data, for example in the indices of a database, which we will
see in session 11.

### The catch: balance

Lookup takes a number of steps that depends on the *depth* of the tree. If keys
are added in an unlucky order, for example already sorted, every new key goes
to the same side and the tree degenerates into a linked list. Then search is
linear again and we have gained nothing. Real implementations therefore use
self-balancing trees (AVL trees, red-black trees, B-trees) that rearrange
themselves on insertion to keep the depth around $\log_2 n$. We do not cover
the balancing algorithms in this course, but you should know that the problem
exists and that it is solved.

![An unbalanced tree](../Slides/03-DataStructures/figures/03-bst-unbalanced.svg)

---

## 8. Hashing and hash tables

Let us go back to the array. Its problems were that memory is tied to the range
of the indices and that indices must be integers, and hashing attacks both. Two
questions drive this part: can we have very fast lookup, about one operation
per access, without the index range problem of arrays? And can we use other
indices besides integers?
The lecture gives two motivating examples. Student ID numbers have six digits,
so there are 1,000,000 possible values, but only about 10,000 are in use at any
time; an array indexed by ID would waste 99% of its memory, so we would like
to map all possible IDs onto 10,000 slots. Book titles in a library have about
100 characters, so there are around $30^{100}$ possible titles, while the
library has about 2 million books; indexing by title directly is not merely
wasteful, it is impossible.

### Hash functions

A *hash function* $h: K \rightarrow \{0, 1, \dots, m-1\}$ assigns to any given
key $k$ an index $0 \le h(k) \le m-1$. A good hash function has to satisfy
several requirements. There are many more possible keys than slots, $|K| \gg
m$, which is the whole point. It has to be easy and fast to compute. It has to
distribute the keys evenly over the available indices, to avoid collisions. It
has to be fully deterministic, so that the same key always gives the same slot,
because otherwise we could never find anything again. And ideally it can be
adjusted when the number of slots $m$ changes. Hash functions are usually
built on natural numbers, so a key that is not a number, such as a character
string, is first turned into one.

![A hash function maps the many possible keys onto m slots](../Slides/03-DataStructures/figures/03-hash-function.svg)

With a hash function, every operation on a hash table starts by computing the
position $h(k)$ of the key $k$. To search, compute $h(k)$ and read position
$h(k)$. To add, compute $h(k)$ and write at position $h(k)$, which raises the
question of what to do if the position is already used. To delete, compute
$h(k)$ and empty position $h(k)$. In the best case each operation takes a
single step.

### Choosing $m$: the modulo function

The modulo operation automatically yields values in $0 \dots m-1$ and
distributes values evenly, so $h(k) = k \bmod m$ is the standard starting
point. But the choice of $m$ matters a lot: the best choice is a prime number
and the worst choice is a power of the base of the number system in which the
keys are written. The lecture shows why with dates written as numbers:

| key $k$ | $k \bmod 97$ | $k \bmod 100$ |
|---|---|---|
| 20100101 | 52 | 1 |
| 20100227 | 81 | **27** |
| 20100427 | 87 | **27** |
| 20110527 | **2** | **27** |
| 20090811 | 74 | **11** |
| 20101224 | 11 | **24** |
| 20111111 | **4** | **11** |
| 20120229 | **4** | 29 |
| 20091224 | **2** | **24** |

Collisions are in bold. Taking $k \bmod 100$ just keeps the last two digits,
which are the day of the month, so every date with the same day collides: seven
of the nine dates share a slot with another one. The prime 97 mixes the whole
number and spreads the keys out; it is not free of collisions, since 20110527
and 20091224 both go to slot 2, but they are rarer and not tied to the day. The general lesson is that if $m$ shares
structure with the keys, the hash function inherits that structure.

### Collisions

*Hash collisions* happen when two keys are mapped to the same position by the
hash function. Collisions are not a failure of the hash function; they are
unavoidable, because there are more possible keys than slots, so by the
pigeonhole principle some keys must share a slot. The question is only what to
do about them.

![Two keys colliding](../Slides/03-DataStructures/figures/03-hash-collisions.svg)

### Separate chaining

The first solution to collisions is *separate chaining*: every slot of the hash
table holds a linked list of all the keys hashed to it, and colliding entries
are appended to it. Searching for an entry
then means computing $h(k)$ and searching the linked list at that slot from
front to end; inserting means computing $h(k)$, searching the list and
appending the new element if it is not there; and deleting means computing
$h(k)$, searching the list and removing the element from it. The example of
the lecture uses $m = 7$ and $h(k) = k \bmod 7$. The key 50 goes to slot 1, 700
to slot 0, 76 to slot 6, 85 to slot 1 (a collision, so it is appended after
50), 92 to slot 1 again, and 73 and 101 both to slot 3.

![Separate chaining, step by step](../Slides/03-DataStructures/figures/03-separate-chaining.svg)

The time required is one step in the best case and $n$ steps in the worst case,
where $n$ is the number of entries stored. The worst case is every key hashing
to the same slot, which turns the table back into a linked list. This is why
the quality of the hash function is not a detail.

### Probing

The alternative is *open addressing*, which stores every key in the table
itself. With *linear probing*, if slot $h(k)$ is taken, we try $h(k)+1$,
$h(k)+2$, and so on (modulo $m$). Writing puts the key in the first free slot
of this sequence; reading follows the same probes until it finds the key or an
empty slot, which means the key is not there. In the example of the lecture,
with $m = 7$ and $h(k) = k \bmod 7$, the table already holds 700, 50 and 76.
Inserting 85 ($h = 1$) finds slot 1 taken and writes to slot 2; 92 ($h = 1$)
tries 1 and 2 and writes to 3; 101 ($h = 3$) tries 3 and writes to 4. Searching
for 101 probes slot 3, which holds 92, and finds 101 in slot 4. Searching for
64 ($h = 1$) probes slots 1 to 4 and stops at the empty slot 5: 64 is not in the
table.

![Linear probing: writing and reading](../Slides/03-DataStructures/figures/03-linear-probing.svg)

With *random probing*, the sequence is $h(k)+r_1$, $h(k)+r_2$, and so on, with a
fixed pseudo-random sequence $r$ (in the example 3, 6, 2, 5, 1, 4) that a
search can repeat, so the keys are spread out instead of forming one run.

![Random probing](../Slides/03-DataStructures/figures/03-random-probing.svg)

Three things need watching. *Clustering*: with linear probing, occupied slots
form runs, and every key that hashes into a run walks to its end and makes it
longer; in the example, a new key hashing to any slot except 5 ends in slot 5.
Random probing avoids these runs, but its sequence must be reproducible, fixed
or computed from the key, or a search could not find the key again. *Load*:
both slow down sharply as the table fills, so with $n$ keys in $m$ slots, keep
$n/m$ well below 1. *Deletion*: emptying a slot would cut the probe sequence of
the keys stored after it, so the slot is marked as *deleted* instead; searches
skip it and insertions may reuse it. The lecture leaves a home exercise here:
in the linear probing example, delete 85 by marking its slot, search for 92 and
for 101, insert 64, and work out what would go wrong if slot 2 were simply
emptied.

### Dictionaries in Python

Python stores its dictionaries in hash tables and solves collisions with random
probing: when a slot is full, it moves to another slot in a pseudo-random
sequence computed from the key, so that a search can repeat it. A dictionary
starts with 8 slots and is resized when it is about two thirds full, because
as a table fills up, collisions become common and performance degrades.
Resizing means re-hashing everything into a bigger table, which is expensive
but rare, so the average cost per insertion stays low. In the figure, "Ana" and
"Ben" go straight to slots 3 and 5; "Cem" also hashes to slot 3, finds it
taken, and probes on to slot 0. The lookup `ages["Ben"]` computes the hash of
"Ben", goes to slot 5, checks that the key matches and returns 16.

![A Python dictionary as a hash table](../Slides/03-DataStructures/figures/03-python-dict.svg)

### Dataset pseudonymization

Hashing is also a tool for research data. If a dataset has an identifying
column, replacing each value $v$ by $h(v)$ gives a column you can still group
and join on, because the same name always gives the same code. In the panel
survey of the lecture, Ana Weber answered in two waves, and both of her rows
get the code `c3305900d9`, so her answers can still be linked:

| name | wave | age | vote |  | person | wave | age | vote |
|---|---|---|---|---|---|---|---|---|
| Ana Weber | 1 | 34 | yes | &rarr; | `c3305900d9` | 1 | 34 | yes |
| Ben Koch | 1 | 27 | no | &rarr; | `f61798a8f3` | 1 | 27 | no |
| Clara Roth | 1 | 45 | yes | &rarr; | `f109d00beb` | 1 | 45 | yes |
| Ana Weber | 2 | 35 | no | &rarr; | `c3305900d9` | 2 | 35 | no |

A hash cannot be turned back into the name, but it can be guessed with some
effort: hash every name in a phone book and compare. The approach is to hash
the name together with a *secret* that only the research team knows; the codes
above are the first 10 characters of SHA-256 of the secret followed by the
name. And pseudonymized is not anonymous: age and answers together may still
identify a person.

---

## 9. Dictionaries

A *dictionary* is an abstract data type composed of a collection of (key,
value) pairs, such that each possible key appears at most once in the
collection. Note the words "abstract data type": a dictionary says what
operations exist, namely lookup by key, insertion and deletion, and not how they
are implemented. Hash tables are one implementation and balanced trees are
another. In a dictionary the keys are generalized, so they can be characters,
words or names rather than just indices, and they are not necessarily evenly
distributed, so an array spanning the whole range of possible values would
waste memory. If you keep the keys in a plain list, lookup is a sequential
search whose worst case looks at all $n$ entries, and this is exactly what
hashing avoids.

A practical rule for your own code: use a list when you need an ordered
sequence of items, including layered lists such as a table stored as a list of
rows, and use a dictionary when you need efficient lookup by key. Dictionaries
are also good as a "super-structure", for example to store ordered items as
lists inside a dictionary keyed by whatever you group by. One performance note
is worth remembering. The test `key in d` hashes the key and takes one step,
and so does `key in d.keys()` in Python 3, because the view of the keys uses
the same hash table. But `key in list(d)` or a loop over the keys scans them
one by one, which turns an instant operation into a linear scan, and in a loop
that becomes a quadratic algorithm, as we will see in session 8.

---

## 10. Why this matters for social science

Efficient data access is a precondition for most practical data analysis, and
since Python uses hashing for `dict`, you are already relying on it whether you
name it or not. The lecture closes with an example of a tool built around hash
tables. AWK is a small, specialized language for string processing and a
quiet favorite of many data scientists. It was created at Bell Labs by Alfred
Aho, Peter Weinberger and Brian Kernighan, whose initials give it its name, and
it is a key component of UNIX. It is extremely fast for what it does thanks to
two things: regular expressions, which we will learn in session 9, and hash
tables. Its default array type is an associative array backed by a hash table,
which is why counting things in AWK is a one-liner:

```awk
{ count[$1]++ }  END { for (k in count) print k, count[k] }
```

That is a word-frequency counter, and the `count` array is a hash table. MAWK
is a faster and more memory-efficient implementation of the same language.

---

## 11. Check yourself

**1.** You need to store 100,000 records and look them up by a 12-digit national ID. Array, BST or hash table?

<details><summary>Answer</summary>

A hash table. An array indexed by the ID would need $10^{12}$ cells for 100,000
records. A BST would work and give you logarithmic lookup plus the ability to
iterate in sorted order, so choose it if you need the ordering. If you only
ever look up by exact ID, the hash table is faster.

</details>

**2.** Insert 1, 2, 3, 4, 5 into an empty BST in that order. Draw it. What went wrong?

<details><summary>Answer</summary>

Every key is larger than the previous one, so each goes to the right, and the
result is a chain 1, 2, 3, 4, 5 of depth 5. The tree has degenerated into a
linked list and lookup is linear. Inserting in sorted order is the worst case
for an unbalanced BST, which is why real implementations rebalance.

</details>

**3.** Why does deleting a node with two children need a special rule, while one child does not?

<details><summary>Answer</summary>

With one child there is an obvious replacement, the child, whose whole subtree
is already on the correct side of every ancestor. With two children there is no
single subtree that can move up without breaking the ordering, so you must pick
the one key that sits between the two subtrees, the predecessor or the
successor, and promote that.

</details>

**4.** A hash table with m = 10 stores phone numbers using h(k) = k mod 10. Why is this bad?

<details><summary>Answer</summary>

The value of `k mod 10` is the last digit of the number. Last digits of phone
numbers are not uniformly distributed, because blocks are allocated, some
digits are reserved and people choose memorable numbers, so the table will be
lumpy. Worse, 10 is a power of the base of the number system, which is the
failure mode shown in the dates table. Use a prime.

</details>

**5.** Is hashing a column of names enough to anonymize a dataset?

<details><summary>Answer</summary>

No. Hashing is deterministic, so anyone who can guess the set of possible names
can hash them all and build a lookup table, which is called a dictionary
attack. Real pseudonymization adds a secret salt, and even then, joining a
pseudonymized dataset with another one can re-identify people.
Pseudonymization is not anonymization.

</details>

---

## 12. References

- **Cormen, T. H., Leiserson, C. E., Rivest, R. L. & Stein, C. (2009).**
  *Introduction to Algorithms*, 3rd ed., MIT Press. Chapter 10 (elementary data
  structures) is the reading for this session; chapter 11 (hash tables) and
  chapter 12 (binary search trees) go deeper.
- **Cormen, T. H. (2013).** *Algorithms Unlocked*, MIT Press. A gentler version
  of the same material; the BINARY-SEARCH pseudocode is adapted from pp.
  28–30.
- **Python Software Foundation.** *Time complexity of Python operations*.
  <https://wiki.python.org/moin/TimeComplexity>. The practical table behind
  section 9.
- **How Python dictionaries are implemented** (probing, resizing at two
  thirds):
  <https://stackoverflow.com/questions/327311/how-are-pythons-built-in-dictionaries-implemented>
  and the comments in the CPython source file `Objects/dictobject.c`.
- **Kernighan, B. W.** on hash tables, in conversation:
  <https://www.youtube.com/watch?v=qTZJLJ3Gm6Q>
- **Aho, A. V., Kernighan, B. W. & Weinberger, P. J. (1988).** *The AWK
  Programming Language*. Addison-Wesley.
- Linked-list diagrams after the illustrations at
  <https://www.tutorialspoint.com/>
