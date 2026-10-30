"""Notebook cells for the question/answer examples, sessions 8-13."""

NB = {}


def md(s): return ("md", s.strip("\n"))
def code(s): return ("code", s.strip("\n"))


# ---------------------------------------------------------------- 08-A
NB["X08-A"] = ("Tr0ub4dor&3 or correct horse battery staple?", [
md("""
# Tr0ub4dor&3 or correct horse battery staple?

Guessing a password is a search whose cost is *alphabet size to the power of the
length*. Length is the exponent, and that is where the leverage is.
"""),
code("""
def seconds_to_crack(alphabet, length, guesses_per_second=1e10):
    return alphabet ** length / guesses_per_second

def human(s):
    for unit, size in [("years", 3.156e7), ("days", 86400), ("hours", 3600), ("minutes", 60)]:
        if s >= size:
            return f"{s / size:,.0f} {unit}"
    return f"{s:.0f} seconds"

cases = [("8 lowercase letters", 26, 8), ("8 chars from 95 symbols", 95, 8),
         ("4 words from a 2048-word list", 2048, 4), ("12 lowercase letters", 26, 12),
         ("12 chars from 95 symbols", 95, 12), ("6 words from a 2048-word list", 2048, 6)]
for label, A, L in cases:
    print(f"{label:32} {human(seconds_to_crack(A, L)):>20}")
"""),
md("""
## Actually brute-forcing a (tiny) password

Time the search for 3, 4 and 5 lowercase letters and watch each extra letter
multiply the time by 26.
"""),
code("""
import itertools, string, time

def brute_force(target):
    alphabet = string.ascii_lowercase
    for guess in itertools.product(alphabet, repeat=len(target)):
        if "".join(guess) == target:
            return

for target in ["zzz", "zzzz", "zzzzz"]:            # the worst case: last guess
    t0 = time.perf_counter(); brute_force(target); dt = time.perf_counter() - t0
    print(f"{len(target)} letters: {26**len(target):>10,} guesses  {dt:8.3f} s")
"""),
md("""
## Hardware versus length

A 100× faster attacker shifts every bar by a constant factor; one more word
multiplies the work by 2 048.
"""),
code("""
print("4 words, attacker 100x faster:", human(seconds_to_crack(2048, 4, 1e12)))
print("5 words, same attacker:       ", human(seconds_to_crack(2048, 5, 1e12)))
"""),
md("""
**What we used:** exponential versus polynomial growth, and why a constant factor
cannot compete with an exponent (session 8, sections 3, 8 and 9).
"""),
])

# ---------------------------------------------------------------- 08-B
NB["X08-B"] = ("The clustering script that ran out of memory at 100 000", [
md("""
# The clustering script that ran out of memory at 100 000

A pairwise-distance matrix has $n^2$ cells. Ten times the data is a hundred times
the memory, and an allocation that does not fit never starts.
"""),
code("""
import numpy as np

for n in [1_000, 10_000, 100_000, 1_000_000]:
    print(f"n = {n:>9,}: matrix {8 * n * n / 1e9:>12,.1f} GB    the data itself (12 columns) {8 * n * 12 / 1e6:>8,.1f} MB")
"""),
md("""
## See it happen (safely)

Allocate the matrix for a small $n$ and read its size; the failure at $10^5$ is
what the error message in the lecture shows, so we stop at $10^4$.
"""),
code("""
from scipy.spatial.distance import cdist

for n in [1_000, 3_000, 10_000]:
    X = np.random.default_rng(0).normal(size=(n, 12))
    D = cdist(X, X)                       # the full n x n matrix
    print(f"n = {n:>6}: {D.nbytes / 1e6:8.1f} MB")
"""),
md("""
## The escape: never form the matrix

K-means compares each point with $K$ centers, not with every other point:
$O(nK)$ memory per step instead of $O(n^2)$.
"""),
code("""
def kmeans_step(X, centers):
    d = cdist(X, centers)                # n x K, not n x n
    labels = d.argmin(axis=1)
    return np.array([X[labels == k].mean(axis=0) for k in range(len(centers))]), d.nbytes

X = np.random.default_rng(0).normal(size=(100_000, 12))
centers, nbytes = kmeans_step(X, X[:5])
print(f"n = 100,000, K = 5: {nbytes / 1e6:.1f} MB for the distances instead of 80,000 MB")
"""),
md("""
**What we used:** memory complexity as a growth rate you can read off the code
before running it (session 8, sections 2, 8 and 9); K-means is session 10.
"""),
])

# ---------------------------------------------------------------- 08-C
NB["X08-C"] = ("Computers got 1 000× faster. Solving got 43 000 000× faster.", [
md("""
# Where the speed came from

Hardware gives a constant factor. A better algorithm gives a factor that
*grows with the problem*. Here is that difference, measured.
"""),
code("""
import random, time

def pairs_summing_to(values, target):
    \"\"\"Count pairs (i < j) with values[i] + values[j] == target.  O(n^2).\"\"\"
    n, count = len(values), 0
    for i in range(n):
        for j in range(i + 1, n):
            if values[i] + values[j] == target:
                count += 1
    return count

def pairs_summing_to_fast(values, target):
    \"\"\"Same answer with a hash table.  O(n).\"\"\"
    seen, count = {}, 0
    for v in values:
        count += seen.get(target - v, 0)
        seen[v] = seen.get(v, 0) + 1
    return count
"""),
code("""
rnd = random.Random(3)
for n in [1_000, 2_000, 4_000, 8_000]:
    values = [rnd.randrange(n) for _ in range(n)]
    t0 = time.perf_counter(); a = pairs_summing_to(values, n);      t_slow = time.perf_counter() - t0
    t0 = time.perf_counter(); b = pairs_summing_to_fast(values, n); t_fast = time.perf_counter() - t0
    assert a == b
    print(f"n = {n:>5}: slow {t_slow:7.3f} s   fast {t_fast:8.5f} s   algorithmic speed-up {t_slow / t_fast:7.0f}x")
"""),
md("""
Each doubling of $n$ roughly **doubles the speed-up** of the better algorithm.
A machine that is 1 000× faster gives 1 000× at every $n$, and no more.
"""),
code("""
hardware = 1000
for n in [1e3, 1e4, 1e5, 1e6]:
    algorithmic = n / 2          # the ratio n^2 / n up to a constant, roughly what the timings show
    print(f"n = {n:>9,.0f}: hardware {hardware:>6}x    algorithm {algorithmic:>10,.0f}x    together {hardware * algorithmic:>14,.0f}x")
"""),
md("""
**What we used:** asymptotic growth and why an exponent beats a constant
(session 8, sections 3, 8 and 10). The historical numbers (1 000× hardware,
43 000× algorithms, 1988 to 2003) are from the PCAST 2010 report.
"""),
])

# ---------------------------------------------------------------- 09-A
NB["X09-A"] = ("Design a coffee machine that cannot be cheated", [
md("""
# A coffee machine that cannot be cheated

A deterministic finite automaton as a Python dictionary: one state per amount
paid so far, a reject state, two coins, one accepting state.
"""),
code("""
states = [0, 10, 20, 30, 40, 50]
alphabet = [10, 20]
start, accept = 0, {50}

delta = {}
for s in states:
    for coin in alphabet:
        delta[(s, coin)] = s + coin if s + coin <= 50 else "reject"
for coin in alphabet:
    delta[("reject", coin)] = "reject"

def run(coins):
    state = start
    for c in coins:
        state = delta[(state, c)]
    return state in accept

for seq in [[10, 20, 20], [20, 20, 10], [10] * 5, [20, 20, 20], [10, 10, 20], [50]]:
    try:
        print(seq, "->", "coffee" if run(seq) else "no coffee")
    except KeyError as e:
        print(seq, "-> not a coin:", e)
"""),
md("""
## The 5-tuple, made explicit
"""),
code("""
print("Q      =", states + ["reject"])
print("Sigma  =", alphabet)
print("q0     =", start)
print("X      =", accept)
print("delta  : every (state, symbol) pair has exactly one entry ->", all((s, c) in delta for s in states + ["reject"] for c in alphabet))
"""),
md("""
That last line is what *deterministic and complete* means: for every state and
every symbol there is exactly one next state. There is no sequence of coins the
table does not cover, so "cannot be cheated" is a property of the table, not a
hope.

## Why none of the amount states can be merged

Two amounts paid so far can be told apart by some future coin (20 and 30 differ
on the coin 20), so no two of the six amount states can be merged; the reject
state accepts nothing and is distinct from all of them. Seven states is the
minimum for a complete machine.
"""),
code("""
def distinguishable(s1, s2, depth=3):
    from itertools import product
    for seq in product(alphabet, repeat=depth):
        a, b = s1, s2
        for c in seq:
            a, b = delta[(a, c)], delta[(b, c)]
        if (a in accept) != (b in accept):
            return True
    return False

print(all(distinguishable(a, b) for a in states for b in states if a < b))
"""),
md("""
**What we used:** the finite-state automaton, its 5-tuple, determinism and
completeness (session 9, sections 2 and 3).
"""),
])

# ---------------------------------------------------------------- 09-B
NB["X09-B"] = ("Can a finite machine check your brackets?", [
md("""
# Can a finite machine check your brackets?

A finite automaton can count only up to the number of states it has. A stack
counts without bound.
"""),
code("""
def balanced_with_stack(s):
    stack = []
    for ch in s:
        if ch == "(":
            stack.append(ch)
        elif ch == ")":
            if not stack:
                return False           # pop on an empty stack
            stack.pop()
    return not stack                   # everything closed

for s in ["(()(()))", "(()", "())(", "", "((((((((()))))))))"]:
    print(f"{s!r:22} {balanced_with_stack(s)}")
"""),
md("""
## The best a finite automaton can do

With $k$ states it can track the depth up to $k$. Here is a "counter automaton"
with 3 states, and the input that breaks it.
"""),
code("""
def balanced_with_k_states(s, k):
    depth = 0
    for ch in s:
        if ch == "(":
            depth = min(depth + 1, k)   # a finite machine cannot remember more than k
        elif ch == ")":
            if depth == 0:
                return False
            depth -= 1
    return depth == 0

k = 3
for s in ["(())", "((()))", "(((())))", "((((()))"]:
    print(f"k = {k}: {s!r:12} stack says {balanced_with_stack(s)!s:5}  {k}-state machine says {balanced_with_k_states(s, k)}")
"""),
md("""
Whatever $k$ you choose, the string with $k+1$ opening brackets fools it: it
cannot tell depth $k$ from depth $k+1$. Formally, $a^n b^n$ is not a regular
language.

## The grammar that generates the language
"""),
code("""
import random
rnd = random.Random(4)

def generate(depth=0):
    \"\"\"S -> ( S ) S | empty\"\"\"
    if depth > 3 or (depth > 0 and rnd.random() < 0.3):
        return ""
    return "(" + generate(depth + 1) + ")" + generate(depth + 1)

samples = [generate() for _ in range(6)]
print(samples)
print(all(balanced_with_stack(s) for s in samples))
"""),
md("""
**What we used:** the limits of finite automata, push-down automata and
context-free grammars (session 9, sections 2, 4 and 5).
"""),
])

# ---------------------------------------------------------------- 09-C
NB["X09-C"] = ("Is there a fast way to solve any Sudoku?", [
md("""
# Is there a fast way to solve any Sudoku?

Checking a solution is fast. Finding one is search. That asymmetry is the whole
of NP in one puzzle.
"""),
code("""
puzzle = [
    "53..7....", "6..195...", ".98....6.",
    "8...6...3", "4..8.3..1", "7...2...6",
    ".6....28.", "...419..5", "....8..79",
]
grid = [[0 if ch == "." else int(ch) for ch in row] for row in puzzle]
"""),
code("""
def valid(grid):
    \"\"\"The verifier: every row, column and box holds 1..9 exactly once. Polynomial.\"\"\"
    full = set(range(1, 10))
    rows = all(set(r) == full for r in grid)
    cols = all({grid[r][c] for r in range(9)} == full for c in range(9))
    boxes = all({grid[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)} == full
                for br in (0, 3, 6) for bc in (0, 3, 6))
    return rows and cols and boxes

def solve(grid, stats):
    \"\"\"The solver: backtracking search. Exponential in the worst case.\"\"\"
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                for v in range(1, 10):
                    if all(v != grid[r][k] for k in range(9)) and all(v != grid[k][c] for k in range(9)) \\
                       and all(v != grid[br][bc] for br in range(r // 3 * 3, r // 3 * 3 + 3) for bc in range(c // 3 * 3, c // 3 * 3 + 3)):
                        grid[r][c] = v
                        stats["placements"] += 1
                        if solve(grid, stats):
                            return True
                        grid[r][c] = 0          # backtrack
                return False
    return True
"""),
code("""
import time
stats = {"placements": 0}
t0 = time.perf_counter(); solve(grid, stats); t_solve = time.perf_counter() - t0
t0 = time.perf_counter(); ok = valid(grid);   t_check = time.perf_counter() - t0
for row in grid: print(" ".join(map(str, row)))
print(f"\\nsolved in {t_solve:.3f} s with {stats['placements']} placements;  verified in {t_check * 1e6:.0f} µs -> {ok}")
"""),
md("""
Checking took microseconds; finding took thousands of tries. For $9 \\times 9$
that is fine. Generalized Sudoku ($n^2 \\times n^2$) is NP-complete, so a
polynomial-time solver for it would give one for every problem in NP.

## Verify fast, find slow: the definition of NP

`valid` is a polynomial-time *verifier*; that alone puts Sudoku in NP. The
reduction from other NP problems is what makes it NP-*complete*.
"""),
md("""
**What we used:** P, NP, verifiers and NP-completeness (session 9, sections 7 and 9).
"""),
])

# ---------------------------------------------------------------- 10-A
NB["X10-A"] = ("The wolf detector that only saw snow", [
md("""
# The wolf detector that only saw snow

A model that scores well on its test set and has learned the wrong thing. We
build one on purpose, with two features: *ear shape* (the real signal) and
*snow in the background* (the shortcut).
"""),
code("""
import numpy as np
from sklearn.linear_model import LogisticRegression
rng = np.random.default_rng(0)

def make_data(n, p_snow_given_wolf, p_snow_given_husky):
    is_wolf = rng.random(n) < 0.5
    ears = np.where(is_wolf, rng.normal(0.35, 0.6, n), rng.normal(-0.35, 0.6, n))  # weak but real signal
    snow = np.where(is_wolf, rng.random(n) < p_snow_given_wolf, rng.random(n) < p_snow_given_husky)
    return np.column_stack([ears, snow.astype(float)]), is_wolf.astype(int)

X_train, y_train = make_data(400, p_snow_given_wolf=0.95, p_snow_given_husky=0.05)   # snow ~ label
X_test,  y_test  = make_data(200, p_snow_given_wolf=0.95, p_snow_given_husky=0.05)   # same bias!
model = LogisticRegression().fit(X_train, y_train)
print("test accuracy:", model.score(X_test, y_test))
print("coefficients  ears: %.2f   snow: %.2f" % tuple(model.coef_[0]))
"""),
md("""
Excellent test score, and the coefficient on *snow* is larger than the one on
*ears*: the model leaned on the background.

## The world where the model is used
"""),
code("""
X_zoo, y_zoo = make_data(200, p_snow_given_wolf=0.5, p_snow_given_husky=0.5)   # snow no longer tells you anything
print("accuracy at the zoo:", model.score(X_zoo, y_zoo))
"""),
md("""
## Ask the feature, not the score

A model trained where the shortcut does not exist has to use the real signal.
It does worse on the biased test set while being right for the right reasons.
"""),
code("""
X_fair, y_fair = make_data(400, p_snow_given_wolf=0.5, p_snow_given_husky=0.5)
fair = LogisticRegression().fit(X_fair, y_fair)
print("coefficients  ears: %.2f   snow: %.2f" % tuple(fair.coef_[0]))
print("fair model on the biased test set:", fair.score(X_test, y_test), "   at the zoo:", fair.score(X_zoo, y_zoo))
"""),
md("""
**What we used:** features, generalization, why a test set can share the
bias of the training set, and explanation (session 10, sections 4, 6, 8 and 12).
"""),
])

# ---------------------------------------------------------------- 10-B
NB["X10-B"] = ("Predict who survived the Titanic in five words", [
md("""
# Predict who survived the Titanic in five words

The Kaggle Titanic training set (891 passengers), a one-feature rule, and the
numbers every model has to beat. Data file: `data/titanic.csv`
(source: datasciencedojo/datasets on GitHub, a mirror of the Kaggle set).
"""),
code("""
import pandas as pd
df = pd.read_csv("data/titanic.csv")
print(len(df), "passengers")
print(df.groupby("Sex")["Survived"].mean().round(3))
print(df.groupby("Pclass")["Survived"].mean().round(3))
"""),
md("""
## The rule: women survive, men do not
"""),
code("""
y_true = df["Survived"].values
y_rule = (df["Sex"] == "female").astype(int).values

tp = ((y_rule == 1) & (y_true == 1)).sum()
fp = ((y_rule == 1) & (y_true == 0)).sum()
fn = ((y_rule == 0) & (y_true == 1)).sum()
tn = ((y_rule == 0) & (y_true == 0)).sum()
print(f"TP={tp} FP={fp} FN={fn} TN={tn}")
print(f"accuracy  {(tp + tn) / len(df):.3f}")
print(f"precision {tp / (tp + fp):.3f}")
print(f"recall    {tp / (tp + fn):.3f}")
"""),
md("""
## Baselines

Always know what a trivial rule gets before believing a model.
"""),
code("""
majority = max(y_true.mean(), 1 - y_true.mean())
print(f"predict 'died' for everyone:      accuracy {majority:.3f}")
print(f"women survive, men do not:        accuracy {(tp + tn) / len(df):.3f}")

rule2 = ((df['Sex'] == 'female') | ((df['Age'] < 10) & (df['Pclass'] < 3))).astype(int).values
print(f"... or a child in 1st/2nd class:  accuracy {(rule2 == y_true).mean():.3f}")
"""),
md("""
A model reporting 80% has added one point over a rule anyone could state.
Published models reach 0.82 to 0.84; the ceiling is low because the outcome is
noisy.

**What we used:** the supervised setup, accuracy versus precision and recall,
and the confusion matrix (session 10, sections 3 and 5).
"""),
])

# ---------------------------------------------------------------- 10-C
NB["X10-C"] = ("How many groups are there?", [
md("""
# How many groups are there?

K-means in twelve lines, the elbow, and the case where it confidently finds
groups that do not exist.
"""),
code("""
import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng(3)

centers_true = np.array([[2, 2], [7, 7], [8, 1.5]])
X = np.vstack([rng.normal(c, 0.8, size=(80, 2)) for c in centers_true])

def kmeans(X, K, iters=30, seed=0):
    r = np.random.default_rng(seed)
    means = X[r.choice(len(X), K, replace=False)]
    for _ in range(iters):
        labels = np.argmin(((X[:, None, :] - means[None, :, :]) ** 2).sum(axis=2), axis=1)  # assign
        means = np.array([X[labels == k].mean(axis=0) for k in range(K)])                  # update
    wss = sum(((X[labels == k] - means[k]) ** 2).sum() for k in range(K))
    return means, labels, wss

means, labels, wss = kmeans(X, 3)
plt.scatter(X[:, 0], X[:, 1], c=labels, s=15); plt.scatter(*means.T, marker="X", s=200, c="k")
plt.title("K = 3"); plt.show()
"""),
md("""
## Choosing K: the elbow
"""),
code("""
Ks = range(1, 9)
wss = [min(kmeans(X, K, seed=s)[2] for s in range(5)) for K in Ks]
plt.plot(Ks, wss, "o-"); plt.xlabel("K"); plt.ylabel("within-cluster sum of squares"); plt.show()
print([round(w) for w in wss])
"""),
md("""
WSS always falls, and it is zero at $K = n$, so you cannot minimize it. The
elbow is where the drop stops being steep: here, 3.

## When K-means is wrong
"""),
code("""
angles = rng.random(240) * 2 * np.pi
r = np.where(np.arange(240) < 80, 1.0, 4.0)
rings = np.column_stack([r * np.cos(angles), r * np.sin(angles)]) + rng.normal(0, 0.15, (240, 2))
_, lab, _ = kmeans(rings, 2, seed=2)
plt.scatter(rings[:, 0], rings[:, 1], c=lab, s=15); plt.gca().set_aspect("equal")
plt.title("two rings, K = 2: split down the middle"); plt.show()
"""),
md("""
K-means returned two clusters because it was asked for two. It never says "there
are no groups"; that judgment is yours.

**What we used:** unsupervised learning, K-means and the elbow method
(session 10, sections 2 and 10).
"""),
])

# ---------------------------------------------------------------- 11-A
NB["X11-A"] = ("Little Bobby Tables", [
md("""
# Little Bobby Tables

Building a query by pasting a name into a string turns data into code. SQLite
in memory, no setup.
"""),
code("""
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Students (name TEXT, grade REAL)")
db.executemany("INSERT INTO Students VALUES (?, ?)", [("Anna", 1.7), ("Ben", 2.3), ("Cem", 1.3)])

def lookup_unsafe(name):
    query = "SELECT * FROM Students WHERE name = '" + name + "'"      # concatenation
    print("   query:", query)
    return db.execute(query).fetchall()

print(lookup_unsafe("Anna"))
"""),
md("""
## The injection

The input closes the quote and adds its own condition.
"""),
code("""
print(lookup_unsafe("' OR '1'='1"))       # every row, no DROP needed
"""),
md("""
Bobby's full name needs two statements in one call. `sqlite3.execute` refuses
that (one of several protections a driver can offer); `executescript` does not.
"""),
code("""
bobby = "Robert'); DROP TABLE Students;--"
statement = "INSERT INTO Students (name) VALUES ('" + bobby + "')"
print(statement)
try:
    db.executescript(statement)
    db.execute("SELECT * FROM Students")
except sqlite3.OperationalError as e:
    print("after running it:", e)
"""),
md("""
## The fix: keep data and code apart
"""),
code("""
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Students (name TEXT)")
db.execute("INSERT INTO Students (name) VALUES (?)", (bobby,))          # parameterized
print(db.execute("SELECT name FROM Students").fetchall())
print(db.execute("SELECT * FROM Students WHERE name = ?", ("' OR '1'='1",)).fetchall())
"""),
md("""
The value is sent separately from the query text and is never parsed as SQL,
whatever it contains.

**What we used:** SQL as an executable language, INSERT/DROP, and parameterized
queries (session 11, sections 8, 10 and 13).
"""),
])

# ---------------------------------------------------------------- 11-B
NB["X11-B"] = ("The join that returned more rows than the table", [
md("""
# The join that returned more rows than the table

Two tables in `FROM` without a condition is the Cartesian product.
"""),
code("""
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript(\"\"\"
CREATE TABLE product  (id INTEGER PRIMARY KEY, name TEXT, price REAL);
CREATE TABLE purchase (id INTEGER PRIMARY KEY, product_id INTEGER, units INTEGER);
INSERT INTO product VALUES (1, 'Milk', 1.20), (2, 'Tea', 3.50);
INSERT INTO purchase VALUES (1,1,1),(2,2,2),(3,1,3),(4,2,1),(5,1,2),(6,1,1),(7,2,4),(8,1,1);
\"\"\")

def count(sql):
    return db.execute(f"SELECT COUNT(*) FROM ({sql})").fetchone()[0]

print("purchases:", count("SELECT * FROM purchase"), " products:", count("SELECT * FROM product"))
print("no condition:  ", count("SELECT * FROM purchase, product"))
"""),
md("""
## And the report doubled
"""),
code("""
print(db.execute("SELECT SUM(units * price) FROM purchase, product").fetchone()[0], "<- every purchase paired with both prices")
print(db.execute("SELECT SUM(units * price) FROM purchase JOIN product ON purchase.product_id = product.id").fetchone()[0], "<- correct")
"""),
md("""
## Explicit joins fail loudly
"""),
code("""
print("with WHERE:      ", count("SELECT * FROM purchase, product WHERE purchase.product_id = product.id"))
print("with JOIN ... ON:", count("SELECT * FROM purchase JOIN product ON purchase.product_id = product.id"))
try:
    db.execute("SELECT * FROM purchase JOIN product ON").fetchall()    # a forgotten ON is a syntax error
except sqlite3.OperationalError as e:
    print("forgotten ON:     syntax error ->", e)
"""),
md("""
The habit: print the row count before and after every join. A join can be
silently wrong only if nobody looks.

**What we used:** tables as sets of tuples, selection, and joins with and
without a condition (session 11, sections 9, 11 and 12).
"""),
])

# ---------------------------------------------------------------- 11-C
NB["X11-C"] = ("Find the customers who never ordered", [
md("""
# Find the customers who never ordered

An `INNER JOIN` drops the rows you are looking for before `WHERE` can see them.
"""),
code("""
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript(\"\"\"
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER);
INSERT INTO customers VALUES (1,'Anna'),(2,'Ben'),(3,'Cem'),(4,'Dana');
INSERT INTO orders VALUES (10,1),(11,1),(12,3);
\"\"\")

print("INNER:", db.execute(\"\"\"
    SELECT c.name FROM customers c JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL
\"\"\").fetchall())
"""),
code("""
print("LEFT: ", db.execute(\"\"\"
    SELECT c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL
\"\"\").fetchall())
"""),
md("""
## What the two joins actually produce
"""),
code("""
for kind in ["JOIN", "LEFT JOIN"]:
    rows = db.execute(f"SELECT c.name, o.id FROM customers c {kind} orders o ON o.customer_id = c.id").fetchall()
    print(f"{kind:9}", rows)
"""),
md("""
`NULL` means *absent*, and it matches nothing, not even itself.
"""),
code("""
print(db.execute("SELECT NULL = NULL, NULL IS NULL").fetchone())
print("COUNT(*)   per customer:", db.execute("SELECT c.name, COUNT(*)   FROM customers c LEFT JOIN orders o ON o.customer_id = c.id GROUP BY c.name").fetchall())
print("COUNT(o.id) per customer:", db.execute("SELECT c.name, COUNT(o.id) FROM customers c LEFT JOIN orders o ON o.customer_id = c.id GROUP BY c.name").fetchall())
"""),
md("""
`COUNT(*)` counts the NULL row as one order and `COUNT(o.id)` does not, which
is the difference between "Ben has 1 order" and the truth.

**What we used:** INNER versus LEFT joins, NULL, and the order in which a query
is evaluated (session 11, sections 11 and 12).
"""),
])

# ---------------------------------------------------------------- 12-A
NB["X12-A"] = ("One million increments, and the counter says 712 431", [
md("""
# One million increments, and the counter says 712 431

`counter += 1` is three steps, read, add and write, and threads interleave
between them. The notebook runs a smaller version, 20 000 increments over four
threads. Python's interpreter lock hides the race for tiny loops, so we put an
explicit "let someone else run" between the read and the write: that is what
the hardware does on its own, uninvited, in any other language.
"""),
code("""
import threading, time

counter = 0
def worker(n):
    global counter
    for _ in range(n):
        value = counter          # read
        time.sleep(0)            # let another thread run here: what the hardware does on its own, uninvited
        counter = value + 1      # add, write

threads = [threading.Thread(target=worker, args=(5_000,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print("expected 20,000   got", f"{counter:,}")
"""),
md("""
Most of the increments vanished: each thread read the counter, let the others
run, and then wrote back a value that ignored everything they had done in the
meantime. Without the explicit yield the loss is smaller and random, and in C,
Java or Go it happens with no help at all.

## Fix 1: a lock makes the three steps one step
"""),
code("""
counter, lock = 0, threading.Lock()
def worker_locked(n):
    global counter
    for _ in range(n):
        with lock:                # only one thread inside at a time
            counter += 1

threads = [threading.Thread(target=worker_locked, args=(5_000,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print("with a lock:", f"{counter:,}")
"""),
md("""
Correct, and the locked section is now *serial*, which Amdahl's law will charge
you for.

## Fix 2: no shared state at all
"""),
code("""
def worker_private(n, results, i):
    local = 0
    for _ in range(n):
        local += 1                # nothing shared
    results[i] = local

results = [0] * 4
threads = [threading.Thread(target=worker_private, args=(5_000, results, i)) for i in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print("per-thread counts:", results, "  sum:", f"{sum(results):,}")
"""),
md("""
Each thread keeps its own count; the four are added once at the end. That is
the Map and Reduce of MapReduce, and it is why the framework has no race.

**What we used:** threads sharing memory, interleaving, locks, and why MapReduce
keeps state local (session 12, sections 4, 5, 9 and 11).
"""),
])

# ---------------------------------------------------------------- 12-B
NB["X12-B"] = ("Why is the GPU 50× faster, and 10× slower?", [
md("""
# Same operation on a lot of data, or different operations on different data?

No GPU is needed to see the principle: NumPy applies one operation to a whole
array at once, in the SIMD style, while a Python loop decides element by
element.
"""),
code("""
import numpy as np, time
x = np.random.default_rng(0).normal(size=1_000_000)

t0 = time.perf_counter(); y = [v * 2.0 + 1.0 for v in x];  t_loop = time.perf_counter() - t0
t0 = time.perf_counter(); y = x * 2.0 + 1.0;                t_vec  = time.perf_counter() - t0
print(f"same arithmetic on 1,000,000 numbers:  loop {t_loop:.3f} s   vectorized {t_vec:.4f} s   ({t_loop / t_vec:.0f}x)")
"""),
md("""
## A branch inside the loop

Vectorized code cannot "take a branch" per element; it computes both sides and
selects. That is what a GPU does too, and it is why divergent branches waste
lanes.
"""),
code("""
t0 = time.perf_counter(); y = [v * 2 if v > 0 else -v for v in x];          t_loop = time.perf_counter() - t0
t0 = time.perf_counter(); y = np.where(x > 0, x * 2, -x);                    t_vec  = time.perf_counter() - t0
print(f"with a branch:  loop {t_loop:.3f} s   vectorized {t_vec:.4f} s   ({t_loop / t_vec:.0f}x): both sides computed for every element")
"""),
md("""
## When the work is genuinely different per element

An agent-based step where each agent runs its own small program does not
vectorize, and that is the shape of code that runs *slower* on a GPU than on a
CPU core.
"""),
code("""
def agent_step(state):
    # different agents do different things: no single operation to broadcast
    if state["mood"] > 0.5:
        state["friends"] += 1
    elif state["friends"] > 3:
        state["mood"] += 0.1
    else:
        state["mood"] -= 0.05
    return state

agents = [{"mood": m, "friends": f} for m, f in zip(np.random.default_rng(1).random(200_000), np.random.default_rng(2).integers(0, 6, 200_000))]
t0 = time.perf_counter(); agents = [agent_step(a) for a in agents]; print(f"200,000 branchy agent steps: {time.perf_counter() - t0:.3f} s: CPU work")
"""),
md("""
**What we used:** Flynn's taxonomy, SIMD versus MIMD, and why branches hurt
throughput (session 12, sections 6 to 8). Vectorize before buying hardware.
"""),
])

# ---------------------------------------------------------------- 12-C
NB["X12-C"] = ("Count every word in Wikipedia in two minutes", [
md("""
# Count every word in a big text with MapReduce

Map on chunks with private dictionaries, shuffle by key, reduce by adding. The
text never moves; only the small (word, count) pairs do.
"""),
code("""
import re
from collections import Counter, defaultdict

text = (\"the vote on the budget was close and the party split on the vote \" * 2000).split()
chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)]
print(len(text), "words in", len(chunks), "chunks")
"""),
code("""
def map_chunk(chunk):
    \"\"\"Runs on one machine, on its own chunk, with its own dictionary. No shared state.\"\"\"
    return Counter(chunk)

def shuffle(mapped):
    \"\"\"Route every (word, count) pair to the reducer responsible for that word.\"\"\"
    by_word = defaultdict(list)
    for counts in mapped:
        for word, n in counts.items():
            by_word[word].append(n)
    return by_word

def reduce_word(word, counts):
    return word, sum(counts)

mapped = [map_chunk(c) for c in chunks]               # in real MapReduce: in parallel
shuffled = shuffle(mapped)
result = dict(reduce_word(w, c) for w, c in shuffled.items())
print(sorted(result.items(), key=lambda kv: -kv[1])[:5])
print("same as counting directly:", result == Counter(text))
"""),
md("""
## How much crossed the "network"?
"""),
code("""
pairs_sent = sum(len(c) for c in mapped)
print(f"{len(text):,} words of input;  {pairs_sent} (word, count) pairs sent to reducers")
"""),
md("""
## Run the map phase in parallel for real
"""),
code("""
from multiprocessing import Pool
try:
    with Pool(4) as pool:
        mapped_parallel = pool.map(map_chunk, chunks)
    print("parallel map gives the same result:", dict(reduce_word(w, c) for w, c in shuffle(mapped_parallel).items()) == result)
except Exception as e:
    print("multiprocessing not available here:", e)
"""),
md("""
Why it is not 4× faster: the shuffle and the reduce are serial, and the slowest
worker sets the finish line. This is Amdahl's law with a communication term.

## What does *not* distribute this way

Addition is associative and commutative, so partial counts combine in any order.
A median is not:
"""),
code("""
import statistics
chunk_a, chunk_b = [1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11]        # two machines, unequal chunks
print("median of medians:", statistics.median([statistics.median(chunk_a), statistics.median(chunk_b)]),
      "  true median:", statistics.median(chunk_a + chunk_b))
print("mean of means (weighted): ", (sum(chunk_a) + sum(chunk_b)) / (len(chunk_a) + len(chunk_b)), "  sums and counts combine exactly")
"""),
md("""
**What we used:** MapReduce, which statistics split exactly, and Amdahl's law
(session 12, sections 9 to 11).
"""),
])

# ---------------------------------------------------------------- 13-A
NB["X13-A"] = ("Two point four million ballots, and the wrong president", [
md("""
# 2.4 million ballots, and the wrong president

A simulated electorate where the sampling frame is not the population. Size
reduces variance; it does nothing about bias.
"""),
code("""
import numpy as np
rng = np.random.default_rng(1936)

N = 2_000_000
affluent = rng.random(N) < 0.30                      # owns a phone or a car, or subscribes to the Digest
votes_landon = np.where(affluent, rng.random(N) < 0.60, rng.random(N) < 0.28)
print(f"true share for Landon: {votes_landon.mean():.3f}")
"""),
md("""
## The Literary Digest: a huge sample from the wrong frame
"""),
code("""
frame = np.flatnonzero(affluent)                      # only the affluent are on the mailing list
respondents = rng.choice(frame, 240_000, replace=False)
print(f"Digest estimate ({len(respondents):,} ballots): {votes_landon[respondents].mean():.3f}")
"""),
md("""
## Gallup: a small sample from the right frame
"""),
code("""
for size in [1_000, 5_000, 50_000]:
    sample = rng.choice(N, size, replace=False)
    print(f"random sample of {size:>6,}: {votes_landon[sample].mean():.3f}")
"""),
md("""
The small random samples wobble around the truth; the enormous biased one is
precisely wrong.

## More data from the same frame does not help
"""),
code("""
for size in [10_000, 100_000, 500_000]:
    respondents = rng.choice(frame, size, replace=False)
    print(f"Digest with {size:>7,} ballots: {votes_landon[respondents].mean():.3f}")
"""),
md("""
Every estimate from the affluent frame lands near 0.60, the vote of the
affluent rather than of the electorate. Digital trace data is this situation
every day: a platform is a frame, not a population.

**What we used:** coverage error and non-response, and why a biased sample of a
billion is still biased (session 13, sections 6, 8 and 12).
"""),
])

# ---------------------------------------------------------------- 13-B
NB["X13-B"] = ("Is every segregated city full of racists?", [
md("""
# Schelling's segregation model in 40 lines

Mild individual preferences, strong collective segregation.
"""),
code("""
import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng(11)

N, F, EMPTY = 30, 0.30, 0.10
cells = np.array(["R"] * int(N * N * (1 - EMPTY) / 2) + ["B"] * int(N * N * (1 - EMPTY) / 2))
cells = np.concatenate([cells, np.array(["."] * (N * N - len(cells)))])
rng.shuffle(cells)
grid = cells.reshape(N, N)

def share_like_me(g, r, c):
    me, same, occ = g[r, c], 0, 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (dr or dc) and 0 <= r + dr < N and 0 <= c + dc < N and g[r + dr, c + dc] != ".":
                occ += 1
                same += g[r + dr, c + dc] == me
    return same / occ if occ else 1.0

def unsatisfied(g):
    return [(r, c) for r in range(N) for c in range(N) if g[r, c] != "." and share_like_me(g, r, c) < F]

def mean_share(g):
    return np.mean([share_like_me(g, r, c) for r in range(N) for c in range(N) if g[r, c] != "."])
"""),
code("""
def show(g, title):
    img = np.vectorize({"R": 0, "B": 1, ".": 2}.get)(g)
    plt.imshow(img, cmap=plt.matplotlib.colors.ListedColormap(["#d7301f", "#2166ac", "white"]))
    plt.title(title); plt.axis("off"); plt.show()

show(grid, f"random start: like-me share {mean_share(grid):.0%}")
"""),
code("""
for round_ in range(50):
    movers = unsatisfied(grid)
    if not movers:
        break
    rng.shuffle(movers)
    for r, c in movers:
        empties = list(zip(*np.where(grid == ".")))
        rng.shuffle(empties)
        for er, ec in empties:                       # closest satisfying cell, simplified to: any satisfying cell
            grid[er, ec] = grid[r, c]
            if share_like_me(grid, er, ec) >= F:
                grid[r, c] = "."
                break
            grid[er, ec] = "."
print(f"stable after {round_} rounds")
show(grid, f"F = {F:.0%}: like-me share {mean_share(grid):.0%}")
"""),
md("""
Everyone asked for 30%; the typical neighborhood ends up far above it. Change
`F` and run it again: 0.5 is stark, and 0.25 still segregates.

## Reading the end state backwards is a mistake

The rule of the agents is visible in the code. Given only the final grid, would
you have guessed a 30% threshold?

**What we used:** agent-based modeling, generative sufficiency and Schelling's
model (session 13, sections 13 and 14).
"""),
])

# ---------------------------------------------------------------- 13-C
NB["X13-C"] = ("How many Likes does it take to know you better than your spouse?", [
md("""
# How many Likes to know you?

A simulated version of the study: a personality trait predicted from a
person's Likes, with accuracy rising with the number of Likes available. The
real paper is Youyou, Kosinski and Stillwell (2015).
"""),
code("""
import numpy as np
rng = np.random.default_rng(5)

n_people, n_pages = 3000, 400
page_signal = rng.normal(0, 1, n_pages)                       # each page carries a little information about the trait
trait = rng.normal(0, 1, n_people)
p_like = 1 / (1 + np.exp(-(0.22 * np.outer(trait, page_signal) - 1.6)))
likes = (rng.random((n_people, n_pages)) < p_like).astype(float)   # binary Likes matrix
print(likes.shape, "average Likes per person:", likes.sum(axis=1).mean().round(1))
"""),
md("""
## Learn the trait from Likes (linear regression), evaluate on held-out people
"""),
code("""
train, test = slice(0, 2000), slice(2000, None)

def fit_predict(n_available):
    X = likes[:, :n_available]
    Xb = np.column_stack([X, np.ones(len(X))])
    w = np.linalg.lstsq(Xb[train], trait[train], rcond=None)[0]
    pred = Xb[test] @ w
    return np.corrcoef(pred, trait[test])[0, 1]

for n in [10, 30, 70, 150, 300, 400]:
    print(f"{n:>4} Likes available: r = {fit_predict(n):.2f}")
"""),
md("""
Accuracy rises with the logarithm of the number of Likes, which is the shape
of the curve in the paper, where 10 Likes matched a work colleague, 70 a
friend, 150 a family member and 300 a spouse (human judges averaged
$r \\approx 0.49$).

## The privacy consequence

Each Like says almost nothing; the pattern says a lot. And a model fitted on
*other people* still works on you:
"""),
code("""
print(f"a model that never saw the test people: r = {fit_predict(400):.2f} on them")
"""),
md("""
**What we used:** supervised learning as a measurement instrument (session 10,
section 3) and its privacy consequences, inference and shadow profiles
(session 13, sections 10 and 11).
"""),
])
