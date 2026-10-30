"""Notebook cells for the question/answer examples, sessions 2-7.
Each entry: title, then a list of ('md', text) / ('code', source) cells.
Kept deliberately simple: standard library + numpy/matplotlib, no frameworks."""

NB = {}


def md(s): return ("md", s.strip("\n"))
def code(s): return ("code", s.strip("\n"))


# ---------------------------------------------------------------- 02-A
NB["X02-A"] = ("The clock that ends on 19 January 2038", [
md("""
# The clock that ends on 19 January 2038

Many systems store time as **the number of seconds since 1 January 1970** in a
**32-bit signed integer**. This notebook shows exactly what happens at the last
second such a counter can hold, and what comes after.
"""),
code("""
from datetime import datetime, timezone

MAX32 = 2**31 - 1          # the largest value of a signed 32-bit integer
print("largest value:", MAX32)
print("as a date:    ", datetime.fromtimestamp(MAX32, timezone.utc))
"""),
md("""
## The bit pattern

Two's complement uses the first bit as the sign. The largest positive value is a
`0` followed by 31 ones.
"""),
code("""
print(format(MAX32, "032b"))
"""),
md("""
## Adding one second

Python integers never overflow, so we have to *emulate* a 32-bit integer: keep
only the low 32 bits, then interpret the result as signed. `struct` does exactly
that: pack as unsigned 32-bit, unpack as signed.
"""),
code("""
import struct

def as_int32(n):
    \"\"\"Interpret the low 32 bits of n as a signed 32-bit integer.\"\"\"
    return struct.unpack("<i", struct.pack("<I", n & 0xFFFFFFFF))[0]

after = as_int32(MAX32 + 1)
print("bits after +1: ", format((MAX32 + 1) & 0xFFFFFFFF, "032b"))
print("value:         ", after)
print("as a date:     ", datetime.fromtimestamp(after, timezone.utc))
"""),
md("""
The carry ran into the sign bit: `1000…0` is $-2^{31}$, and the clock jumps
back to **13 December 1901**.

## The fix: 64 bits

With a 64-bit counter the same overflow is $2^{63}$ seconds away.
"""),
code("""
seconds_per_year = 365.2425 * 24 * 3600
print(f"{(2**63 - 1) / seconds_per_year / 1e9:.0f} billion years")
"""),
md("""
**What we used:** positional number systems, two's complement, and the fact that
a data type has a fixed size (transcript sections 4, 6 and 10 of session 2).
"""),
])

# ---------------------------------------------------------------- 02-B
NB["X02-B"] = ("0.1 + 0.2 is not 0.3", [
md("""
# 0.1 + 0.2 is not 0.3

The most famous wrong answer in computing, and it is not a bug.
"""),
code("""
print(0.1 + 0.2 == 0.3)
print(0.1 + 0.2)
"""),
md("""
## What is actually stored

`Decimal(x)` shows the *exact* value of a float, and `float.hex()` shows its bits.
"""),
code("""
from decimal import Decimal

for label, x in [("0.1", 0.1), ("0.2", 0.2), ("0.1 + 0.2", 0.1 + 0.2), ("0.3", 0.3)]:
    print(f"{label:10} {x.hex():24} {Decimal(x)}")
"""),
md("""
None of the four is the decimal number you typed: $1/10$ has a factor 5 in the
denominator, so its binary expansion never terminates and the 52-bit significand
has to round. `0.1` and `0.2` are both stored slightly *high*; their sum rounds
up, while `0.3` on its own rounds down. The two results are one unit in the last
place apart.
"""),
code("""
print("difference:", (0.1 + 0.2) - 0.3)
print("one unit in the last place near 0.3:", 2.0**-54)
"""),
md("""
## Errors accumulate
"""),
code("""
total = 0.0
for _ in range(10):
    total += 0.1
print(total, total == 1.0)
"""),
md("""
## What to do about it

Compare with a tolerance, and keep money and counts in exact types.
"""),
code("""
import math
from fractions import Fraction

print(math.isclose(0.1 + 0.2, 0.3))          # tolerance-based comparison
print(Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))   # exact arithmetic
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))     # decimal type for money
"""),
md("""
**What we used:** IEEE 754 floating point and rounding (session 2, sections 7 and 8).
"""),
])

# ---------------------------------------------------------------- 02-C
NB["X02-C"] = ("Why your boarding pass spells you MUELLER", [
md("""
# Why your boarding pass spells you MUELLER

The same name, three encodings: what the machine-readable zone of a passport
does, what happens when two programs disagree about bytes, and what UTF-8 fixed.
"""),
code("""
name = "Jörg Müller"
print(name.encode("utf-8"))      # ö is two bytes: C3 B6
print(name.encode("latin-1"))    # ö is one byte:  F6
"""),
md("""
## Mojibake: reading UTF-8 bytes as if they were Latin-1
"""),
code("""
raw = name.encode("utf-8")
print(raw.decode("latin-1"))     # every byte becomes one character
"""),
md("""
Nothing crashed, because both results are valid strings. The bytes never
changed; the *assumption* about them did.

## ASCII cannot spell ö at all
"""),
code("""
try:
    name.encode("ascii")
except UnicodeEncodeError as e:
    print("ASCII refuses:", e)
"""),
md("""
## The machine-readable zone

ICAO Doc 9303 allows 37 symbols (A–Z, 0–9 and `<`) so that any reader anywhere
decodes the line identically. German umlauts and ß have their own
transliterations (ö becomes OE, ß becomes SS); every other accented letter
loses its accent. The line is padded with `<` to 44 characters.
"""),
code("""
import unicodedata

TRANSLIT = {"Ä": "AE", "Ö": "OE", "Ü": "UE", "ä": "AE", "ö": "OE", "ü": "UE", "ß": "SS",
            "Æ": "AE", "æ": "AE", "Ø": "OE", "ø": "OE"}
MRZ_ALPHABET = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<")

def to_mrz(text):
    \"\"\"Transliterate a name into the 37-symbol MRZ alphabet.\"\"\"
    out = []
    for ch in text:
        if ch in TRANSLIT:                                   # the ICAO table for these letters
            out.append(TRANSLIT[ch])
        else:                                                # Ç is C plus a cedilla mark: drop the mark
            parts = unicodedata.normalize("NFKD", ch)
            out.append("".join(c for c in parts if not unicodedata.combining(c)).upper())
    result = "".join(out).replace(" ", "<")
    assert set(result) <= MRZ_ALPHABET, result
    return result

def mrz_line(surname, given):
    line = f"P<D<<{to_mrz(surname)}<<{to_mrz(given)}"
    return line.ljust(44, "<")[:44]

print(mrz_line("Müller", "Jörg"))
print(mrz_line("Çağla", "Ayşe"))
"""),
md("""
**What we used:** everything stored is a number, and a text encoding is the
convention that maps numbers to characters (session 2, sections 3 and 9).
The practical rule: always say which encoding, as in `open(path, encoding="utf-8")`.
"""),
])

# ---------------------------------------------------------------- 03-A
NB["X03-A"] = ("Where does the Back button keep the pages?", [
md("""
# Where does the Back button keep the pages?

Two stacks are all a browser needs. Let us build one.
"""),
code("""
class History:
    def __init__(self):
        self.back, self.forward, self.current = [], [], None

    def visit(self, page):
        if self.current is not None:
            self.back.append(self.current)   # push
        self.current = page
        self.forward = []                    # a new page throws the forward stack away

    def go_back(self):
        if self.back:
            self.forward.append(self.current)
            self.current = self.back.pop()   # pop: last in, first out

    def go_forward(self):
        if self.forward:
            self.back.append(self.current)
            self.current = self.forward.pop()

    def __repr__(self):
        return f"current={self.current}  back={self.back}  forward={self.forward}"
"""),
code("""
h = History()
for page in "ABC":
    h.visit(page)
print("visit A, B, C :", h)
h.go_back(); h.go_back()
print("back, back    :", h)
h.visit("D")
print("visit D       :", h)
h.go_forward()
print("forward       :", h, "  <- nothing happened")
"""),
md("""
After going back to A and opening D, pages B and C are gone: the forward stack
was cleared when D was pushed. That is not a bug. A stack can hold only one
"future", and the newest one wins.

## Why a stack is the right choice here

`append` and `pop` on the end of a Python list are both $O(1)$: the cost does
not grow with the length of the history.
"""),
code("""
import time
big = History()
t0 = time.perf_counter()
for i in range(200_000):
    big.visit(i)
for i in range(200_000):
    big.go_back()
print(f"400 000 stack operations in {time.perf_counter() - t0:.3f} s")
"""),
md("""
**What we used:** stacks (LIFO) and the linked list or array they are built on
(session 3; stacks and queues are defined formally in session 5, section 6).
"""),
])

# ---------------------------------------------------------------- 03-B
NB["X03-B"] = ("Count a million words: 49 seconds or 0.01", [
md("""
# Count a million words: 49 seconds or 0.01

Two ways to count how often each word appears. Same loop shape, different
container, and a difference that keeps growing.
"""),
code("""
import random, time

def make_stream(n, seed=1):
    rnd = random.Random(seed)
    vocab = [f"w{i}" for i in range(n // 2)]       # half of the words are distinct
    return [rnd.choice(vocab) for _ in range(n)]

def count_with_list(stream):
    pairs = []                                       # [[word, count], ...]
    for w in stream:
        for p in pairs:                              # search the list every time
            if p[0] == w:
                p[1] += 1
                break
        else:
            pairs.append([w, 1])
    return pairs

def count_with_dict(stream):
    counts = {}
    for w in stream:
        counts[w] = counts.get(w, 0) + 1             # hash the word, go straight there
    return counts
"""),
code("""
for n in [1_000, 3_000, 10_000, 30_000]:
    s = make_stream(n)
    t0 = time.perf_counter(); count_with_list(s); t_list = time.perf_counter() - t0
    t0 = time.perf_counter(); count_with_dict(s); t_dict = time.perf_counter() - t0
    print(f"n = {n:>6}   list {t_list:8.4f} s   dict {t_dict:8.5f} s   ratio {t_list / t_dict:8.0f}x")
"""),
md("""
Each time $n$ triples, the list version takes about **nine** times longer
(quadratic) and the dictionary about **three** times longer (linear). The gap is
not a constant; it is a different growth rate.

## Why

The list must be *searched* for every word: up to $m$ comparisons per word, with
$m$ the number of distinct words seen so far. The dictionary computes a hash of
the word and looks in one slot.
"""),
code("""
print(hash("vote") % 8, hash("party") % 8, hash("the") % 8)   # which of 8 slots each word lands in
"""),
md("""
**What we used:** hash tables and dictionaries (session 3, sections 8 and 9), and a
preview of growth rates (session 8).
"""),
])

# ---------------------------------------------------------------- 03-C
NB["X03-C"] = ("The waiting room that gets slower the fuller it is", [
md("""
# The waiting room that gets slower the fuller it is

Removing the first element of a Python list shifts every other element. A queue
does the same job in constant time.
"""),
code("""
import time
from collections import deque

def serve_all_list(n):
    waiting = list(range(n))
    while waiting:
        waiting.pop(0)                 # remove the front: shifts n-1 elements

def serve_all_deque(n):
    waiting = deque(range(n))
    while waiting:
        waiting.popleft()              # remove the front: moves one pointer

for n in [10_000, 20_000, 40_000, 80_000]:
    t0 = time.perf_counter(); serve_all_list(n);  t_list = time.perf_counter() - t0
    t0 = time.perf_counter(); serve_all_deque(n); t_deq  = time.perf_counter() - t0
    print(f"n = {n:>6}   list.pop(0) {t_list:7.3f} s   deque.popleft {t_deq:7.4f} s")
"""),
md("""
Doubling the waiting room quadruples the time of the list version: each call
costs $O(n)$ and there are $n$ calls. The deque stays linear.

## What was given up

A deque gives up cheap access *by position*: `waiting[k]` is $O(k)$ for a linked
structure and $O(1)$ for a list. Every data structure is a choice about which
questions will be cheap.
"""),
code("""
q = deque(["Anna", "Ben", "Cem"])
q.append("Dana")          # arrives at the back
print(q.popleft(), q)     # served from the front: first in, first out
"""),
md("""
**What we used:** arrays versus linked lists and the editing/searching
trade-off (session 3, sections 2 to 4); queues (session 5, section 6).
"""),
])

# ---------------------------------------------------------------- 04-A
NB["X04-A"] = ("The survey whose ages summed to a 40 000-digit number", [
md("""
# The survey whose ages summed to a 40 000-digit number

Values read from a file are text until you say otherwise. Here is the bug,
reproduced in miniature.
"""),
code("""
import csv, io

raw = \"\"\"id,age
1,23
2,41
3,35
4,29
\"\"\"
rows = list(csv.DictReader(io.StringIO(raw)))
print(rows[0], type(rows[0]["age"]))
"""),
code("""
total = ""
for row in rows:
    total = total + row["age"]       # + on strings is concatenation
print(total, "<-", len(total), "characters")
"""),
md("""
Nobody wrote a wrong line: `+` did exactly what it means for the type it was
given. The fix is a conversion.
"""),
code("""
total = 0
for row in rows:
    total = total + int(row["age"])  # now + is addition
print(total)
"""),
md("""
## Why Python let it happen

Python is *dynamically typed*: the operator is chosen at run time from the
types of the operands. Mixing the two types is caught, but two strings are a
valid pair for `+`.
"""),
code("""
print(type("23"), type(23))
try:
    0 + "23"
except TypeError as e:
    print("mixed types are refused:", e)
"""),
md("""
## The same bug without a loop

A pandas column of text does the same thing when you ask for its sum, and it
does it silently.
"""),
code("""
import pandas as pd

ages = pd.Series([row["age"] for row in rows])
print(repr(ages.sum()), "   dtype:", ages.dtype)
print(ages.astype(int).sum())
"""),
md("""
The debugging habit this teaches: when a result looks wrong, print the **type**
of the value, not just the value.

**What we used:** the type system, dynamic typing and operator semantics
(session 4, sections 4 and 5); debugging (section 12).
"""),
])

# ---------------------------------------------------------------- 04-B
NB["X04-B"] = ("The rocket that exploded because a number did not fit", [
md("""
# The rocket that exploded because a number did not fit

Ariane 5, 4 June 1996. A 64-bit floating-point value was converted to a 16-bit
integer, as it had been on Ariane 4 since 1988. Ariane 5 flew faster.
"""),
code("""
import numpy as np

ariane4_max = 30_000.0     # the largest horizontal-bias value the old rocket ever produced
ariane5_value = 36_000.0   # the new rocket, 37 seconds after launch

INT16_MAX = 2**15 - 1
print("16-bit signed range:", -2**15, "…", INT16_MAX)
print(ariane4_max <= INT16_MAX, ariane5_value <= INT16_MAX)
"""),
md("""
## What a conversion does when the value does not fit

Depending on the language and the settings it either **wraps silently** or
**raises**. NumPy shows both behaviors.
"""),
code("""
print("array conversion wraps silently:", np.array([ariane5_value]).astype(np.int16)[0])
try:
    np.int16(ariane5_value)
except OverflowError as e:
    print("scalar conversion raises:      ", e)
"""),
md("""
On Ariane 5 the conversion raised, the exception was not handled, and the
inertial reference unit shut itself down. The backup unit, identical in hardware
and software, had failed the same way 50 milliseconds earlier.

## The fix is a check, and the lesson is where the assumption lives
"""),
code("""
def to_int16_checked(x):
    if not -2**15 <= x <= INT16_MAX:
        raise ValueError(f"{x} does not fit in 16 bits: input outside the assumed range")
    return int(x)

for v in (ariane4_max, ariane5_value):
    try:
        print(v, "->", to_int16_checked(v))
    except ValueError as e:
        print(v, "->", e)
"""),
md("""
The Ariane 4 engineers *had* analyzed the range, in a document rather than in
the code. When the inputs changed, nothing in the program knew.

**What we used:** integer types and their ranges, exceptions, and the practice of
putting assumptions in the code (session 4, sections 5, 11 and 12).
"""),
])

# ---------------------------------------------------------------- 04-C
NB["X04-C"] = ("Was 1900 a leap year? Excel says yes", [
md("""
# Was 1900 a leap year? Excel says yes

A three-condition rule, and a spreadsheet that gets it wrong on purpose.
"""),
code("""
def is_leap_naive(year):
    return year % 4 == 0

def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

for y in [1900, 2000, 2024, 2100]:
    print(y, "naive:", is_leap_naive(y), "  correct:", is_leap(y))
"""),
md("""
## Write the parentheses

`A and B or C` is read by Python as `(A and B) or C`, because `and` binds
tighter than `or`. Here the two groupings happen to agree, because a year that
is divisible by 400 is also divisible by 4; the cell below finds no year on
which they differ. That is luck rather than design, and a reader who assumes
the other grouping reads a different rule.
"""),
code("""
def is_leap_no_parentheses(year):
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0   # same tokens, no parentheses

print([y for y in range(1896, 2104) if is_leap(y) != is_leap_no_parentheses(y)])
"""),
md("""
## Check against the standard library
"""),
code("""
import calendar
print(all(is_leap(y) == calendar.isleap(y) for y in range(1, 3000)))
"""),
md("""
## The Excel bug

Excel treats 1900 as a leap year for compatibility with Lotus 1-2-3. Its serial
number 60 is the non-existent 29 February 1900, so the day count before
1 March 1900 is off by one.
"""),
code("""
from datetime import date, timedelta

def excel_serial_to_date(serial):
    \"\"\"Excel's 1900 date system, bug included.\"\"\"
    if serial < 60:
        return date(1899, 12, 31) + timedelta(days=serial)
    if serial == 60:
        return "1900-02-29 (does not exist)"
    return date(1899, 12, 30) + timedelta(days=serial)   # from March 1900 on, the offset absorbs the bug

for s in [1, 59, 60, 61, 45000]:
    print(s, excel_serial_to_date(s))
"""),
md("""
**What we used:** conditionals, operator precedence and control flow
(session 4, sections 4 and 8); flowcharts (session 5, section 5).
"""),
])

# ---------------------------------------------------------------- 05-A
NB["X05-A"] = ("What is your Erdős number?", [
md("""
# What is your Erdős number?

Breadth-first search on a co-authorship graph gives every author's distance to
Erdős, and a proof that it is the shortest.
"""),
code("""
coauthors = {
    "Erdős":  ["Graham", "Chung"],
    "Graham": ["Erdős", "Chung", "Knuth"],
    "Chung":  ["Erdős", "Graham", "Lovász"],
    "Knuth":  ["Graham", "Garcia"],
    "Lovász": ["Chung", "Garcia"],
    "Garcia": ["Knuth", "Lovász", "You"],
    "You":    ["Garcia"],
}
"""),
code("""
from collections import deque

def bfs(graph, start):
    dist, parent = {start: 0}, {start: None}
    queue = deque([start])
    while queue:
        u = queue.popleft()                 # oldest discovered first: whole layers finish in order
        for v in graph[u]:
            if v not in dist:               # first discovery is the shortest
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)
    return dist, parent

dist, parent = bfs(coauthors, "Erdős")
for author, d in sorted(dist.items(), key=lambda kv: kv[1]):
    print(f"{author:8} {d}")
"""),
md("""
## The chain itself

Follow the parent pointers back from any author.
"""),
code("""
def path_to(parent, target):
    chain = []
    while target is not None:
        chain.append(target)
        target = parent[target]
    return chain[::-1]

print(" -> ".join(path_to(parent, "You")))
"""),
md("""
## Why the first discovery is the shortest

BFS empties layer $k$ before it starts layer $k+1$, so a vertex is first reached
at the smallest possible distance. Swap the queue for a stack and you get
depth-first search, which finds *a* chain but not the shortest one:
"""),
code("""
def dfs_distance(graph, start, target):
    stack, seen = [(start, 0)], set()
    while stack:
        u, d = stack.pop()                  # newest first
        if u == target:
            return d
        if u in seen:
            continue
        seen.add(u)
        for v in graph[u]:
            stack.append((v, d + 1))

print("BFS distance to You:", dist["You"], "  first path found by DFS:", dfs_distance(coauthors, "Erdős", "You"))
"""),
md("""
**What we used:** graphs, adjacency lists and breadth-first search
(session 5, sections 7 to 9).
"""),
])

# ---------------------------------------------------------------- 05-B
NB["X05-B"] = ("The seven bridges of Königsberg", [
md("""
# The seven bridges of Königsberg

Can you cross all seven bridges exactly once? We check every possible route,
then see why Euler did not have to.
"""),
code("""
# land masses A (island), B (north bank), C (south bank), D (east island); bridges as edges
bridges = [("A", "B"), ("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("B", "D"), ("C", "D")]
"""),
md("""
## Brute force: try all 5 040 orderings of the bridges
"""),
code("""
from itertools import permutations

def is_walk(order):
    \"\"\"Can the bridges be crossed in this order, each in some direction, as one continuous walk?\"\"\"
    def extend(position, remaining):
        if not remaining:
            return True
        a, b = remaining[0]
        for here, there in ((a, b), (b, a)):
            if position is None or position == here:
                if extend(there, remaining[1:]):
                    return True
        return False
    return extend(None, list(order))

routes = sum(is_walk(order) for order in permutations(bridges))
print("orderings tried:", len(list(permutations(bridges))), "  valid walks:", routes)
"""),
md("""
Zero. But trying everything is an *algorithm*, not a *proof*: it says nothing
about a city with eight bridges.

## Euler's argument: count the degrees

On a walk you enter and leave each land mass, using two bridges per visit. So
every land mass except the start and the end must touch an **even** number of
bridges.
"""),
code("""
from collections import Counter

degree = Counter()
for a, b in bridges:
    degree[a] += 1
    degree[b] += 1
print(dict(degree))
odd = [v for v, d in degree.items() if d % 2 == 1]
print("vertices of odd degree:", odd, "->", "no walk exists" if len(odd) > 2 else "a walk may exist")
"""),
md("""
Four odd vertices; a walk allows at most two. Remove one bridge and the answer changes:
"""),
code("""
fewer = bridges[:-1]                           # drop the C-D bridge
degree = Counter(v for e in fewer for v in e)
print(dict(degree), "-> odd:", [v for v, d in degree.items() if d % 2])
print("valid walks now:", sum(is_walk(o) for o in permutations(fewer)))
"""),
md("""
**What we used:** graphs, vertices, edges and degree (session 5, sections 7 and 8);
the difference between exhaustive search and a proof (section 2).
"""),
])

# ---------------------------------------------------------------- 05-C
NB["X05-C"] = ("Solve the maze without luck", [
md("""
# Solve the maze without luck

A maze is a graph. Breadth-first search finds the shortest way out and knows
that it has.
"""),
code("""
maze = \"\"\"
#############
#S....#.....#
#.###.#.###.#
#...#...#...#
###.#####.#.#
#.....#...#.#
#.###.#.###.#
#...#.....#E#
#############
\"\"\".strip().split("\\n")

H, W = len(maze), len(maze[0])
start = next((r, c) for r in range(H) for c in range(W) if maze[r][c] == "S")
goal  = next((r, c) for r in range(H) for c in range(W) if maze[r][c] == "E")
print(H, "x", W, "  start", start, " goal", goal)
"""),
code("""
from collections import deque

def neighbors(cell):
    r, c = cell
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if maze[r + dr][c + dc] != "#":
            yield (r + dr, c + dc)

def bfs(start, goal):
    dist, parent, queue = {start: 0}, {start: None}, deque([start])
    while queue:
        u = queue.popleft()
        if u == goal:
            break
        for v in neighbors(u):
            if v not in dist:
                dist[v], parent[v] = dist[u] + 1, u
                queue.append(v)
    path, cell = [], goal
    while cell is not None:
        path.append(cell); cell = parent[cell]
    return path[::-1], dist

path, dist = bfs(start, goal)
print("shortest path:", len(path) - 1, "steps;  cells explored:", len(dist))
"""),
code("""
def show(path):
    grid = [list(row) for row in maze]
    for r, c in path[1:-1]:
        grid[r][c] = "o"
    print("\\n".join("".join(row) for row in grid))

show(path)
"""),
md("""
## The same maze with a stack (depth-first search)
"""),
code("""
def dfs(start, goal):
    parent, stack = {start: None}, [start]
    while stack:
        u = stack.pop()                       # newest first
        if u == goal:
            break
        for v in neighbors(u):
            if v not in parent:
                parent[v] = u
                stack.append(v)
    path, cell = [], goal
    while cell is not None:
        path.append(cell); cell = parent[cell]
    return path[::-1]

dpath = dfs(start, goal)
print("DFS path:", len(dpath) - 1, "steps  (BFS:", len(path) - 1, ")")
show(dpath)
"""),
md("""
Both procedures are correct, in the sense that they find a path. Only BFS
guarantees the shortest, because it explores in order of distance.

**What we used:** representing a problem as a graph, pseudocode into code, and
breadth-first search with parent pointers (session 5, sections 3, 4 and 7 to 9).
"""),
])

# ---------------------------------------------------------------- 06-A
NB["X06-A"] = ("The monks, the 64 disks, and the end of the world", [
md("""
# The monks, the 64 disks, and the end of the world

Four lines of recursion, and an exact count of the moves.
"""),
code("""
def hanoi(n, source, target, spare, moves):
    if n == 0:                                   # base case: nothing to move
        return
    hanoi(n - 1, source, spare, target, moves)   # move n-1 disks out of the way
    moves.append((n, source, target))            # move the largest disk
    hanoi(n - 1, spare, target, source, moves)   # move n-1 disks back on top

moves = []
hanoi(3, "A", "C", "B", moves)
for disk, s, t in moves:
    print(f"disk {disk}: {s} -> {t}")
print(len(moves), "moves")
"""),
md("""
## Counting moves

$M(n) = 2M(n-1) + 1$ with $M(1) = 1$, which gives $2^n - 1$.
"""),
code("""
for n in range(1, 11):
    moves = []
    hanoi(n, "A", "C", "B", moves)
    print(n, len(moves), 2**n - 1)
"""),
code("""
seconds = 2**64 - 1
years = seconds / (365.2425 * 24 * 3600)
print(f"{seconds:,} moves = {years:.3e} years")
"""),
md("""
## Work versus depth

The *number of calls* is exponential; the *depth* of the recursion is only $n$.
The call stack never holds more than 64 frames for the monks' puzzle. It is the
count of moves, not the memory, that ends the world.
"""),
code("""
import sys
depth = 0
def hanoi_depth(n, d=1):
    global depth
    depth = max(depth, d)
    if n == 0: return
    hanoi_depth(n - 1, d + 1); hanoi_depth(n - 1, d + 1)

hanoi_depth(20)
print("calls:", 2**21 - 1, " max depth:", depth, " Python's limit:", sys.getrecursionlimit())
"""),
md("""
**What we used:** base case and recursive case, the program stack, tree
recursion (session 6, sections 2, 4 and 7).
"""),
])

# ---------------------------------------------------------------- 06-B
NB["X06-B"] = ("Draw this tree in five lines", [
md("""
# Draw this tree in five lines

A tree is a segment with two smaller trees on top. The code says exactly that.
"""),
code("""
import math
import matplotlib.pyplot as plt

def tree(ax, x, y, angle, length, depth):
    if depth == 0:                                       # base case
        return 0
    x2 = x + length * math.cos(math.radians(angle))
    y2 = y + length * math.sin(math.radians(angle))
    ax.plot([x, x2], [y, y2], color="#0a9086" if depth <= 2 else "#333", lw=max(0.5, depth * 0.6))
    calls = 1
    calls += tree(ax, x2, y2, angle - 25, length * 0.72, depth - 1)
    calls += tree(ax, x2, y2, angle + 25, length * 0.72, depth - 1)
    return calls
"""),
code("""
fig, axs = plt.subplots(1, 4, figsize=(12, 3.5))
for ax, d in zip(axs, [1, 3, 6, 10]):
    n = tree(ax, 0, 0, 90, 1.0, d)
    ax.set_title(f"depth {d}: {n} segments"); ax.set_aspect("equal"); ax.axis("off")
plt.show()
"""),
md("""
## Exponential work, linear depth

Every level doubles the number of segments ($2^{d}-1$ in total), but at any
moment only `depth` calls are waiting on the stack.
"""),
code("""
for d in [5, 10, 15, 20]:
    print(f"depth {d:2}: {2**d - 1:>9,} segments, {d:2} frames on the stack")
"""),
md("""
Change the two constants (25° and 0.72) and you get a different species; try
15° and 0.8.

**What we used:** base case and recursive case, tree recursion, the program stack
(session 6, sections 2, 4 and 7).
"""),
])

# ---------------------------------------------------------------- 06-C
NB["X06-C"] = ("You have more ancestors than there were people", [
md("""
# You have more ancestors than there were people

The recursion is right. The assumption behind it is wrong, and simulating a
small population shows exactly how.
"""),
code("""
def ancestors(g):
    \"\"\"Number of ancestor *slots* g generations back, if nobody appears twice.\"\"\"
    if g == 0:
        return 1
    return 2 * ancestors(g - 1)

for g in [1, 2, 10, 20, 30]:
    print(f"{g:2} generations: {ancestors(g):>13,}")
print("world population around 1275:  ~400,000,000")
"""),
md("""
## A population where every person has two parents from the previous generation

Simulate 40 generations of a constant population of 500 people. For one person
in the last generation, count *distinct* ancestors per generation.
"""),
code("""
import random
rnd = random.Random(0)
N, G = 500, 40

# parents[g][i] = (mother index, father index) in generation g-1
parents = [None] + [[(rnd.randrange(N), rnd.randrange(N)) for _ in range(N)] for g in range(1, G + 1)]

current = {0}                      # person 0 of the last generation
for g in range(1, 16):
    gen = G - g + 1
    current = {p for i in current for p in parents[gen][i]}
    print(f"{g:2} back: {2**g:>6} slots, {len(current):>4} distinct people (population {N})")
"""),
md("""
The number of distinct ancestors stops doubling within a few generations and
saturates at the population size: the same people fill many slots. This is
**pedigree collapse**, and it is why the family "tree" is really a directed
acyclic graph.

## The same lesson in code: count each shared node once
"""),
code("""
def distinct_ancestors(person, gen, seen):
    \"\"\"DFS over the ancestry graph with a visited set: the fix for over-counting.\"\"\"
    if gen == 0 or (gen, person) in seen:
        return
    seen.add((gen, person))
    for p in parents[gen][person]:
        distinct_ancestors(p, gen - 1, seen)

seen = set()
distinct_ancestors(0, G, seen)
print("distinct ancestors over 40 generations:", len(seen), " (tree recursion would count", 2**41 - 2, ")")
"""),
md("""
**What we used:** recursive definitions and what they assume about the data;
DFS with a visited set; overlapping subproblems (session 6, sections 2, 6 and 8).
"""),
])

# ---------------------------------------------------------------- 07-A
NB["X07-A"] = ("How the post office sorts 20 million letters a night", [
md("""
# How the post office sorts 20 million letters a night

Radix sort: no comparisons, one digit at a time, and every pass must be stable.
"""),
code("""
def radix_sort(codes, digits=5):
    for pos in range(digits - 1, -1, -1):             # last digit first
        bins = [[] for _ in range(10)]
        for code in codes:                            # stable: each bin keeps arrival order
            bins[int(code[pos])].append(code)
        codes = [c for b in bins for c in b]          # collect the bins in order
        print(f"after digit {pos + 1}:", codes)
    return codes

letters = ["78464", "10115", "78462", "80331", "78457", "10117", "50667", "78464"]
result = radix_sort(letters)
print(result == sorted(letters))
"""),
md("""
## Why each pass must be stable

If a pass reordered equal digits, it would destroy the work of the previous
passes. Watch what happens with an unstable pass:
"""),
code("""
def radix_sort_unstable(codes, digits=5):
    for pos in range(digits - 1, -1, -1):
        bins = [[] for _ in range(10)]
        for code in codes:
            bins[int(code[pos])].insert(0, code)      # prepend: reverses arrival order
        codes = [c for b in bins for c in b]
    return codes

print(radix_sort_unstable(letters) == sorted(letters))
"""),
md("""
## Linear time

$d$ passes over $n$ letters: $O(d \\cdot n)$, with $d = 5$ fixed. Compare with
a comparison sort on 300 000 codes:
"""),
code("""
import random, time
rnd = random.Random(2)
big = [f"{rnd.randrange(100000):05d}" for _ in range(300_000)]

def radix_quiet(codes, digits=5):
    for pos in range(digits - 1, -1, -1):
        bins = [[] for _ in range(10)]
        for code in codes:
            bins[int(code[pos])].append(code)
        codes = [c for b in bins for c in b]
    return codes

t0 = time.perf_counter(); r = radix_quiet(big);  t_radix = time.perf_counter() - t0
t0 = time.perf_counter(); s = sorted(big);       t_sort  = time.perf_counter() - t0
print(r == s, f"radix {t_radix:.2f} s   sorted() {t_sort:.2f} s  (sorted() is C code; the point is the growth rate)")
"""),
md("""
**What we used:** stable sorting (session 7, section 3), and the comparison
lower bound that radix sort escapes by not comparing (section 9).
"""),
])

# ---------------------------------------------------------------- 07-B
NB["X07-B"] = ("Can you sort 8 things in 10 comparisons?", [
md("""
# Can you sort 8 things in 10 comparisons?

A bound on every comparison sort ever written, checked by brute force on small
cases.
"""),
code("""
import math
for n in range(2, 11):
    print(f"n = {n:2}: {n}! = {math.factorial(n):>8}  log2 = {math.log2(math.factorial(n)):6.2f}  -> at least {math.ceil(math.log2(math.factorial(n)))} comparisons")
"""),
md("""
## Count what a real algorithm does

Wrap the comparison in a counter and run mergesort on **every** permutation of
$n$ elements; the worst case must be at least $\\lceil \\log_2 n! \\rceil$.
"""),
code("""
from itertools import permutations

def mergesort(a, count):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = mergesort(a[:mid], count), mergesort(a[mid:], count)
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        count[0] += 1
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]

for n in range(2, 8):
    worst = 0
    for p in permutations(range(n)):
        count = [0]
        assert mergesort(list(p), count) == sorted(p)
        worst = max(worst, count[0])
    print(f"n = {n}: mergesort worst case {worst:2} comparisons; lower bound {math.ceil(math.log2(math.factorial(n)))}")
"""),
md("""
Mergesort is close to the bound but not always on it; for $n = 8$ the true
optimum, 16, is reached by a specialized algorithm. Ten is impossible for
anyone.

## The argument in one picture

A comparison sort is a decision tree with $n!$ leaves; a binary tree with $L$
leaves has depth at least $\\log_2 L$.
"""),
code("""
n = 8
print(f"leaves needed: {math.factorial(n)}   a tree of depth 10 has at most {2**10} leaves")
"""),
md("""
**What we used:** the formal sorting problem, mergesort, and the comparison lower
bound (session 7, sections 2, 6 and 9).
"""),
])

# ---------------------------------------------------------------- 07-C
NB["X07-C"] = ("The median of a billion salaries, without sorting", [
md("""
# The median without sorting

Quicksort's `partition` places one element in its final position. Recurse on one
side only and you have Quickselect.
"""),
code("""
import random

def partition(a, lo, hi):
    pivot, i = a[hi], lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1

def quickselect(a, k):
    \"\"\"k-th smallest (0-based) of a, modifying a in place.\"\"\"
    lo, hi = 0, len(a) - 1
    while True:
        q = partition(a, lo, hi)
        if q == k:
            return a[q]
        if q > k:
            hi = q - 1
        else:
            lo = q + 1

a = [38, 12, 71, 25, 56, 90, 44, 17, 63]
print("median:", quickselect(a[:], len(a) // 2), "  check:", sorted(a)[len(a) // 2])
"""),
md("""
## How much work does it do?

Count comparisons for Quickselect against sorting, on random data of growing size.
"""),
code("""
def count_quickselect(a, k):
    n, lo, hi, comps = len(a), 0, len(a) - 1, 0
    while True:
        pivot, i = a[hi], lo - 1
        for j in range(lo, hi):
            comps += 1
            if a[j] <= pivot:
                i += 1; a[i], a[j] = a[j], a[i]
        a[i + 1], a[hi] = a[hi], a[i + 1]
        q = i + 1
        if q == k: return comps
        lo, hi = (lo, q - 1) if q > k else (q + 1, hi)

rnd = random.Random(1)
for n in [1_000, 10_000, 100_000]:
    data = [rnd.random() for _ in range(n)]
    c = count_quickselect(data[:], n // 2)
    print(f"n = {n:>7}: quickselect {c:>9,} comparisons  ~{c / n:.1f} n;   n log2 n = {n * n.bit_length():>10,}")
"""),
md("""
About $3n$ comparisons on average, which is linear, against $n \\log_2 n$ for
a sort. The shrinking active region is a geometric series:
$n + n/2 + n/4 + \\cdots < 2n$.

**What we used:** divide and conquer, quicksort's partition (session 7,
sections 5 and 7); the geometric series is session 8.
"""),
])
