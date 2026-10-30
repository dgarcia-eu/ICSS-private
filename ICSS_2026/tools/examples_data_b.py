"""Question/answer examples for sessions 8-13.  See examples_data_a.py."""

X = {}


def ex(xid, title, tagline, open_, close, notes):
    X[xid] = dict(title=title, tagline=tagline, open=open_, close=close,
                  notes=notes.strip("\n"))


# ===========================================================================
#  08  Time Complexity
# ===========================================================================

ex("X08-A", "Tr0ub4dor&3 or correct horse battery staple?",
   "Which password is safer, and why the answer is a growth rate.",
   dict(img="figures/xkcd-936-password-strength.png", imgh=10.6, wide=False,
        credit="XKCD 936, Randall Munroe, CC BY-NC 2.5, xkcd.com/936",
        body=r"""
Two passwords. One is eleven characters with a capital, a digit and a symbol.
The other is four common words.

The comic's claim: the second is **stronger**, and easier to remember.
""",
        ask="Is that true? What does 'strong' even measure, and why does adding *one more word* do more than adding a symbol?"),
   dict(img="figures/08-password-bruteforce.png", imgh=8.8, wide=True, credit="",
        body=r"""
- Guessing is a search with cost $|A|^L$: alphabet size to the power of the
  **length**. Length is the exponent, and that is where the leverage is.
- $26^8 \approx 2 \times 10^{11}$: 21 seconds at $10^{10}$ guesses/s. $2048^4 =
  2^{44}$: 29 minutes. $2048^6 = 2^{66}$: **234 years**. Two more words beat
  every symbol you could add.
- **Exponential** growth: each extra character multiplies the work; each extra
  order of magnitude of hardware only divides it once.
""",
        uses="§3 why it matters: some numbers · §8 asymptotic behavior: polynomial versus exponential · §9 using O-notation"),
   r"""
**Source.** XKCD 936 (CC BY-NC 2.5; used here in an educational context with
attribution). A guess rate of $10^{10}$/s is a realistic offline GPU attack on
a weak hash (Hashcat benchmarks); against a properly slow hash it is $10^4$/s
and every bar moves six orders of magnitude to the right, which is worth saying.

**Facts.** Bars are computed in the figure script: 8 lowercase letters 21 s; 8
from 95 symbols 7.7 days; 4 words 29 min; 12 lowercase 110 days; 12 from 95
symbols 1.7 million years; 6 words 234 years. The comic's own numbers assume
$10^3$/s (online guessing).

**How to present.** Open with the comic and a vote. Close with the bar chart on
a log axis and the formula $|A|^L$; then ask what a 100× faster attacker does to
each bar (shifts it by 2 on the log axis) against what one more word does
(multiplies by 2048). That contrast *is* the session's message about growth
rates.

**Where it plugs in.** With the growth-rate table of the main deck; it gives
the $2^n$ row a face.
""")

ex("X08-B", "The clustering script that ran out of memory at 100 000",
   "It worked on 10 000 respondents. Ten times more data, one hundred times more memory.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
A student clusters survey respondents by computing the **distance between every
pair** and feeding the matrix to a clustering routine. On the 10 000-respondent
pilot it takes a minute. On the full 100 000 it crashes:

```
MemoryError: Unable to allocate 74.5 GiB for an array
with shape (100000, 100000) and data type float64
```
""",
        ask="Ten times the data asked for a hundred times the memory. Which number in the code decides that, and what does the full 1 000 000-respondent panel need?"),
   dict(img="figures/08-quadratic-memory.png", imgh=9.6, wide=True, credit="",
        body=r"""
- $n$ respondents have $n^2$ pairs; at 8 bytes each the matrix is $8n^2$ bytes:
  0.8 GB at $10^4$, **80 GB at $10^5$**, **8 TB at $10^6$**. The data itself is
  linear and stays small.
- This is **memory complexity** $O(n^2)$, and it fails harder than time
  complexity: a slow job finishes late, an oversized allocation never starts.
- Escapes: algorithms that never form the matrix (K-means is $O(nK)$ per step),
  or approximate neighbor search. Check the exponent *before* the pilot.
""",
        uses="§2 three kinds of complexity: time, memory · §8 O-notation · §9 using it: read the $n^2$ off the code before running it"),
   r"""
**Source.** The error message is verbatim NumPy for a $10^5 \times 10^5$
float64 array (74.5 GiB). Hierarchical clustering via `scipy.cluster.hierarchy`
and `sklearn.metrics.pairwise_distances` both materialize this matrix.

**Facts.** $8n^2$ bytes: $n=10^4$ gives 800 MB; $10^5$ gives 80 GB; $10^6$ gives
8 TB. Even a 512 GB cluster node fails at $n \approx 250\,000$. The dashed
lines in the figure are a 16 GB laptop and a 512 GB node.

**How to present.** Open with the error message; it is a real one and students
recognize the genre. Ask what "ten times the data, a hundred times the memory"
implies about the exponent. Close with the log-log plot: two lines, slopes 1 and
2, and the horizontal machine limits. The lesson: a pilot on a subsample cannot
reveal a quadratic term; only reading the code can.

**Where it plugs in.** With the memory-complexity slides of the main deck
(§2 and §8 of the transcript); connects to K-means in session 10, which is the
linear-memory alternative.
""")

ex("X08-C", "Computers got 1 000× faster. Solving got 43 000 000× faster.",
   "Where did the other 43 000× come from? Not from hardware.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
A 2010 report to the US President compared how long a benchmark optimization
problem took to solve in **1988** and in **2003**.

- Processors in 2003 were about **1 000 times faster**.
- The problem was solved about **43 000 000 times faster**.

The same kind of problem, on the same kind of machine, in the same field.
""",
        ask="Where did the missing factor of 43 000 come from, and why is it, not Moore's law, the reason today's models fit at all?"),
   dict(img="figures/08-algorithms-vs-hardware.png", imgh=9.0, wide=True, credit="",
        body=r"""
- The rest came from **algorithms**: better linear-programming solvers, better
  data structures inside them, better numerical methods. Improvements in the
  *growth rate* and its constants, not in the clock speed.
- Hardware improves everything by a constant factor. An algorithmic improvement
  from $O(n^2)$ to $O(n \log n)$ improves *more* the bigger the problem gets.
- The report's conclusion: in many fields, **algorithms have contributed more
  than Moore's law**, and they are the part a researcher can choose.
""",
        uses="§3 why it matters · §8 asymptotic behavior: why a better growth rate beats a faster machine · §10 why this matters for us"),
   r"""
**Source.** PCAST (2010), *Report to the President and Congress: Designing a
Digital Future*, p. 71, quoting Martin Grötschel on a production-planning LP:
1988 solve time about 82 years, 2003 about 1 minute; 43 million× in total, of
which about 1000× hardware and about 43 000× algorithms. Bixby (2002,
*Operations Research*) gives a detailed history for LP.

**Facts.** The numbers are for one benchmark family and should be quoted as
such; the *shape* of the claim, algorithmic gains exceeding hardware gains,
holds across sorting, FFT, linear algebra and SAT solving.

**How to present.** Open with the two numbers and let the room compute the
ratio. Close with the bar chart on a log axis; the point to land is the one in
the third bullet: a constant factor is a one-off gift, a better exponent keeps
giving. Tie back to the sorting speedup of session 7 (25 000× at $n = 10^6$) as
the worked case they have already seen.

**Where it plugs in.** As the closing argument of the session, right before
"why this matters for us".
""")

# ===========================================================================
#  09  Theoretical Computer Science
# ===========================================================================

ex("X09-A", "Design a coffee machine that cannot be cheated",
   "10-cent and 20-cent coins, a 50-cent coffee, and the smallest machine that gets it right every time.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
A coffee machine accepts **10-cent and 20-cent coins**. A coffee costs exactly
**50 cents**; overpaying is not allowed and there is no change. The machine
must accept `10 20 20`, `20 20 10`, `10 10 10 10 10`, and reject `20 20 20`
the moment the third coin lands.

It has no memory of what you did, other than *what state it is in*.
""",
        ask="How many states does the machine need? Draw it. Is there any sequence of coins your drawing gets wrong?"),
   dict(img="figures/09-vending-dfa.svg", imgh=8.8, wide=True, credit="",
        body=r"""
- A **deterministic finite automaton** with one state per amount paid so far,
  0, 10, 20, 30, 40, **50** (accepting), plus a reject state for any coin that
  would exceed 50. Each coin is a transition.
- The 5-tuple: $Q = \{0,10,20,30,40,50,\text{reject}\}$, $\Sigma = \{10, 20\}$,
  $\delta$ the arrows, $q_0 = 0$, $X = \{50\}$. The transition table is the program.
- The machine is *complete*: every state has an arrow for every coin. That, plus
  determinism, is what makes "cannot be cheated" a theorem rather than a hope.
""",
        uses="§2 finite-state automata: the 5-tuple and transition diagrams · §3 why determinism matters · §5 regular languages"),
   r"""
**Source.** Standard introductory automaton; Sipser ch. 1 opens with an
automatic-door controller built the same way. The diagram is generated; a
20-cent coin from state 40 goes to reject.

**Facts.** Seven states is minimal for a complete machine: any two amounts paid
so far are distinguishable by some future coin sequence, so no two can be
merged, and the reject state accepts nothing. Adding a 5-cent coin roughly
doubles the states; adding *change* needs an output, a Mealy machine, which is
a good stretch question.

**How to present.** Open with the spec and give the room five minutes in pairs
to draw it; collect two drawings on the board. Most forget the reject arrows
(incomplete automaton) or add a "memory". Close with the figure and write the
5-tuple next to it explicitly; the exam asks for exactly this. Then ask: what
if coffee cost *any* multiple of 10? (Still finite.) What if the machine had to
accept "as many 10s as 20s"? (Not finite; see X09-B.)

**Where it plugs in.** Right after the definition of a DFA, before the z0–z3
automaton of the main deck.
""")

ex("X09-B", "Can a finite machine check your brackets?",
   "Every editor flags a missing parenthesis. What kind of machine does it take?",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
Your editor knows instantly that `((a + b) * (c − d)` is missing a bracket, and
that `(()(()))` is fine. A JSON file with 40 000 nested objects is validated in
milliseconds.

Session 9 has just given you a machine with finitely many states.
""",
        ask="Can a finite-state automaton decide whether the brackets in a string are balanced? If not, what is the *smallest* addition that makes it possible?"),
   dict(img="figures/09-brackets-pda.svg", imgh=8.6, wide=True, credit="",
        body=r"""
- **No.** Balanced strings can be nested arbitrarily deep, so the machine must
  *count* open brackets without bound, and a finite automaton with $k$ states
  cannot distinguish depth $k$ from depth $k+1$. (The formal version: $a^n b^n$
  is not regular.)
- **A stack** is the smallest addition: push on `(`, pop on `)`, accept if the
  stack is empty at the end and never underflows. That is a **push-down automaton**,
  and balanced brackets are a **context-free** language.
- Nested structures, JSON, HTML, arithmetic and code, all live one level up the
  Chomsky hierarchy from what a regex can handle. That is why "parse HTML with a
  regex" is a famous mistake.
""",
        uses="§2 finite-state automata and their limit · §4 formal languages and grammars · §5 regular languages: what they cannot express · the Chomsky hierarchy"),
   r"""
**Source.** Sipser ch. 1–2; the pumping lemma gives the formal proof that
$a^n b^n$ is not regular. The trace in the figure runs the stack on
`(()(()))`.

**Facts.** The grammar is $S \to (S)S \mid \varepsilon$. A PDA with one stack
suffices; two stacks give a Turing machine. Real parsers (for JSON, Python)
are push-down machines in disguise, since recursive descent uses the *call* stack.

**How to present.** Open by asking for a DFA; let the room try for three
minutes and fail. The failure is instructive because every attempt has a
fixed maximum depth. Close with the stack trace and the one-line grammar. Then
name the hierarchy explicitly, regular ⊂ context-free ⊂ …, and place the coffee
machine (X09-A) and the brackets side by side as the boundary.

**Where it plugs in.** Between the DFA material and the push-down automaton of
the exercise sheet; sets up the Chomsky-hierarchy slide of the main deck.
""")

ex("X09-C", "Is there a fast way to solve any Sudoku?",
   "A newspaper puzzle, a million-dollar question, and why they are the same thing.",
   dict(img="figures/sudoku-example.svg", imgh=9.6, wide=False,
        credit="Puzzle: Wikimedia Commons (public domain)",
        body=r"""
You can check a finished Sudoku in seconds: every row, column and box has 1–9.
**Solving** one is another matter, and a $9 \times 9$ grid is only the newspaper
size. On an $n^2 \times n^2$ grid, does the solving time stay reasonable?
""",
        ask="Is there an algorithm that solves *any* Sudoku in time polynomial in the grid size? What would it mean if you found one, and why has nobody?"),
   dict(img="figures/sudoku-example.svg", imgh=7.4, wide=False,
        credit="Puzzle: Wikimedia Commons (public domain)",
        body=r"""
- **Checking** a filled grid is polynomial: that puts Sudoku in **NP**.
- Yato & Seta (2003) showed generalized Sudoku is **NP-complete**: every problem
  in NP can be translated into a Sudoku in polynomial time.
- So a polynomial-time Sudoku solver would give one for satisfiability,
  timetabling, protein folding and the rest: **P = NP**, and a million-dollar
  Clay prize. Nobody has one; the working assumption is that none exists.
- Newspaper Sudokus are solved by **backtracking search**, exponential in the
  worst case and fine at $9 \times 9$.
""",
        uses="§7 computability versus complexity · §9 complexity classes: P, NP, NP-completeness and reduction"),
   r"""
**Source.** Yato, T. & Seta, T. (2003), "Complexity and completeness of finding
another solution and its application to puzzles", *IEICE Trans. Fundamentals*
E86-A(5). The puzzle image is public domain (Wikimedia Commons). The Clay
Millennium Prize for P vs NP: claymath.org.

**Facts.** NP-completeness is for the $n^2 \times n^2$ generalization; the
$9 \times 9$ case is a fixed finite problem and technically $O(1)$. The
hardest known 9×9 puzzles still fall to backtracking in milliseconds. A 17-clue
minimum for a unique solution was proved in 2012 by exhaustive computation.

**How to present.** Open with the puzzle and the check/solve asymmetry;
"verify fast, find slow" is the whole of NP in one sentence. Close with the
chain: in NP (verifier), NP-complete (reduction), a fast solver collapses
everything. The exam's `TC-10` and `TC-11` ask exactly this; the
seminar-assignment candidate (M09-B) is the same story with a scheduling face.

**Where it plugs in.** With the P/NP Venn diagrams at the end of the main deck.
""")

# ===========================================================================
#  10  Machine Learning
# ===========================================================================

ex("X10-A", "The wolf detector that only saw snow",
   "Right on eight test images out of ten, useless at the zoo, and how to find out why.",
   dict(img="figures/10-husky-wolf-q.svg", imgh=7.6, wide=True, credit="",
        body=r"""
Researchers trained a classifier to tell **wolves from huskies** from photos. On
the held-out test images it got eight out of ten right. Then it failed on the
obvious ones: a husky in a snowy garden was a wolf, a wolf on grass was a husky.
""",
        ask="The model passed its test. What did it actually learn, and what question would have caught it before deployment?"),
   dict(img="figures/10-husky-wolf.svg", imgh=7.0, wide=True, credit="",
        body=r"""
- In the training photos, wolves were mostly **in snow** and huskies mostly not.
  Snow was a cheaper feature than fur or ears, so the model learned **snow**.
- An explanation method (LIME) that highlights the pixels driving each decision
  showed the **background**, never the animal.
- The test set had the same bias, so the test score was honest *and* useless. The
  question to ask: **does the feature the model uses exist in the world where the
  model will be used?** Otherwise the model has learned a correlation, not the concept.
""",
        uses="§4 features and what the model can see · §6 generalization and why a test set can lie · §8 overfitting to spurious structure · §12 trust and explanation"),
   r"""
**Source.** Ribeiro, Singh & Guestrin (2016), "Why Should I Trust You?
Explaining the Predictions of Any Classifier", *KDD*; the husky/wolf experiment
is §6.4, with the figure of LIME highlighting snow. The diagram here is
schematic; the paper's actual images are copyrighted.

**Facts.** 20 wolf and husky images, hand-picked so that the wolves had snow
behind them, a logistic regression on image features; 10 test images, of which
one husky in snow and one wolf without snow were misclassified. Shown to
graduate students, 10 of 27 trusted the model before seeing the explanations
and 3 of 27 after.

**How to present.** Open with the four-panel figure but *without* the dashed
box, and ask what the model learned. Close with the box: the explanation looks
at the background. Then the generalization, which is the real content: the
Clever Hans horse, Google Flu's basketball season (M10-A), a dropout model that
learned the campus wifi log. The check is always the same: interrogate the
feature, not the score.

**Where it plugs in.** Between the features slides and the train/test material;
it motivates §12's "right to an explanation" concretely.
""")

ex("X10-B", "Predict who survived the Titanic in five words",
   "A one-feature rule gets 79%. Every model you build must beat it.",
   dict(img="figures/10-titanic-rates.png", imgh=8.6, wide=True, credit="",
        body=r"""
The Titanic passenger list is the standard first dataset in machine learning:
891 passengers, with sex, age, class, fare, and whether they survived.

Before any model: the survival rates by sex and by class, above.
""",
        ask="State a prediction rule in **five words**. What accuracy does it get, and how would you know whether a neural network with 10 000 parameters is actually better?"),
   dict(img="figures/10-titanic-confusion.svg", imgh=7.2, wide=True, credit="",
        body=r"""
- "**Women survive, men do not.**" Accuracy $(233 + 468)/891 = \mathbf{78.7\%}$,
  precision 0.74, recall 0.68 on the survivors.
- That is the **baseline**. A model that reports 80% has added one point over a
  rule anyone could state; a model that reports 78% has learned nothing.
- Always compute the trivial rule first: majority class, one feature, a domain
  fact. Then the confusion matrix, so that the errors have names.
""",
        uses="§3 the supervised setup: features, target, prediction · §5 error, loss, precision and recall · §6 test performance means nothing without a baseline"),
   r"""
**Source.** Kaggle "Titanic: Machine Learning from Disaster" training set,
891 rows; counts by sex: women 314 (233 survived), men 577 (109 survived); by
class: 1st 136/216, 2nd 87/184, 3rd 119/491. Confusion matrix and metrics are
computed in the figure script from those counts.

**Facts.** The rule "survived iff female" has accuracy 0.787. Adding
"or a child in 1st or 2nd class" reaches about 0.80. Good published models
reach about 0.82 to 0.84; the ceiling is low because the outcome is genuinely
noisy.

**How to present.** Open with the two bar charts and ask for a five-word rule.
Close by filling the confusion matrix on the board from the counts (they are on
the slide) and computing accuracy, precision and recall live: three exam
formulas, one dataset. Then the framing: this number is what the models of the
practical part have to beat, and most first attempts will not.

**Where it plugs in.** With the error/loss slides; use again in session 13 when
representation and base rates return.
""")

ex("X10-C", "How many groups are there?",
   "240 survey respondents, two scores, no labels, and the algorithm that finds groups even when there are none.",
   dict(img="figures/10-kmeans-data.png", imgh=10.0, wide=False, credit="",
        body=r"""
Two attitude scores for 240 respondents. No labels: nobody has said how many
"types" of respondent there are, or which respondent is which.

Look at it. Now imagine it had 12 dimensions instead of 2, and 24 000 points.
""",
        ask="Write the procedure that finds the groups. How do you choose how many? And what does it do when the data has no groups at all?"),
   dict(img="figures/10-kmeans-k3.png", imgh=10.0, wide=False, credit="",
        body=r"""
- **K-means**: pick $K$ centers; assign each point to the nearest; move each
  center to the mean of its points; repeat until nothing changes. Unsupervised:
  there is no $Y$.
- **Choosing $K$**: the within-cluster sum of squares falls with every extra
  cluster, to zero at $K = n$. The **elbow** is where it stops falling steeply:
  here $K = 3$.
- **The warning**: K-means always returns $K$ clusters. On two concentric rings
  it confidently splits them in half. A clustering is a *hypothesis*, not a finding.
""",
        uses="§2 the three families: unsupervised learning · §10 clustering, K-means and the elbow method · §12 what a model's output is evidence of"),
   r"""
**Source.** Synthetic data generated in the figure script (three Gaussian
blobs; two rings), K-means implemented there so that the elbow values are real
(WSS: 3489, 1503, 299, 256, …). MacQueen (1967) for K-means; Hastie et al.
§14.3.

**Facts.** The elbow at $K = 3$ is unambiguous on this data by design; on real
survey data it rarely is, and that ambiguity is honest information. K-means
assumes spherical clusters of similar size; the ring figure shows the failure.

**How to present.** Open with the unlabeled scatter; ask for a number of
groups and a procedure. Close with the colored result and the elbow plot
(both on the extra slide of this deck), then the rings as a final beat. The
sentence to land: the algorithm never says "there are no groups". That is the
researcher's job.

**Where it plugs in.** With the K-means slides of the main deck; the elbow and
ring figures are supplementary and can be dropped into the main deck directly.
""")

# ===========================================================================
#  11  Databases
# ===========================================================================

ex("X11-A", "Little Bobby Tables",
   "A boy's name deletes a school's records. The bug is in one line, and it is a lesson about data versus code.",
   dict(img="figures/xkcd-327-exploits-of-a-mom.png", imgh=6.0, wide=True,
        credit="XKCD 327, Randall Munroe, CC BY-NC 2.5, xkcd.com/327",
        body=r"""
A school enrolls a child whose registered name is
`Robert'); DROP TABLE Students;--`. Shortly afterwards, the school has no
student records.
""",
        ask="What did the school's software do with that name? Which single line was wrong, and what is the correct version?"),
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
The school built its query by pasting the name into a string:

```python
query = "INSERT INTO Students (name) VALUES ('" + name + "')"
```

With the boy's name that string becomes **two statements**:

```sql
INSERT INTO Students (name) VALUES ('Robert'); DROP TABLE Students;--')
```

- The name was **data**; concatenation turned it into **code**. This is SQL
  injection, and it is still in the top three web vulnerabilities.
- The fix is to keep data and code separate: a **parameterized query**
  `cursor.execute("INSERT INTO Students (name) VALUES (?)", (name,))`.
  The database never parses the value as SQL, whatever it contains.
""",
        uses="§8 SQL is a language: text can be executed · §10 data manipulation: INSERT, DROP · §13 SQL injection and parameterized queries"),
   r"""
**Source.** XKCD 327, "Exploits of a Mom" (CC BY-NC 2.5, attribution on the
slide). The OWASP Top 10 lists injection in every edition. The comic's own
line, "I hope you've learned to sanitize your database inputs", is slightly
wrong advice: the robust answer is parameterization, not sanitization.

**Facts.** `--` starts a comment in SQL, which swallows the trailing `')`.
Whether two statements execute in one call depends on the driver (SQLite's
`execute` refuses; `executescript` and many web stacks allow it). Exercise A5
of the exercise sheet has the `' OR '1'='1` variant that needs no `DROP`.

**How to present.** Open with the comic; it is the best-known joke in
computing and half the room has seen it, which does not matter. Ask what the
code must have looked like. Close by writing the concatenation line and the
resulting SQL on the board, then the `?` version. Connect to sessions 2 and 4:
the same "data interpreted as instructions" failure as encoding bugs and
`eval`.

**Where it plugs in.** The SQL-injection slide of the main deck already uses
the comic; this deck supplies the question-then-code structure around it.
""")

ex("X11-B", "The join that returned more rows than the table",
   "Eight purchases, two products, sixteen rows. Nothing crashed. The report is wrong.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
An analyst joins the `purchase` table (8 rows) with the `product` table (2 rows)
to add product names to the report. The result has **16 rows**, and total sales
in the report have **doubled**.

```sql
SELECT * FROM purchase, product;
```

The query ran without error. The numbers went to the board meeting.
""",
        ask="Where did the extra rows come from? Why is this *correct* behavior for the query as written, and what did the analyst forget?"),
   dict(img="figures/11-join-explosion.svg", imgh=9.0, wide=True, credit="",
        body=r"""
- Two tables in `FROM` with no condition is the **Cartesian product**: every row
  of one paired with every row of the other, $8 \times 2 = 16$.
- The missing piece is the **join condition**: `WHERE purchase.product_id =
  product.id`, or better `INNER JOIN product ON …`, which keeps only matching pairs.
- Prefer the explicit `JOIN … ON` syntax: a forgotten `WHERE` silently multiplies,
  a forgotten `ON` is a syntax error. **Check the row count of every join** against
  what it should be; a join can never *silently* be wrong if you do that.
""",
        uses="§9 tables as sets of tuples · §11 selection · §12 joins: manual joins, INNER JOIN, and what happens without a condition"),
   r"""
**Source.** The `purchase`/`product` tables are the ones in the main deck; the
exam's `DB-03` and `DB-04` restructure a similar purchases table. The figure
enumerates the product. The doubled total is what happens when you `SUM` a
column after a two-row Cartesian join.

**Facts.** $|A \times B| = |A| \cdot |B|$; two million-row tables give
$10^{12}$ rows, which is how a forgotten join condition takes down a database
server. The other direction, *fewer* rows than expected, is the inner join
dropping unmatched rows (X11-C).

**How to present.** Open with the query, the 16, and the doubled total; the
"went to the board meeting" line is the hook. Close with the figure, then the
`ON` syntax, then the habit: print the row count before and after every join.
That habit is worth more than any SQL feature.

**Where it plugs in.** At the manual-join slide of the main deck, whose three
questions ("why four rows? why new column names? how many with no WHERE?") this
answers.
""")

ex("X11-C", "Find the customers who never ordered",
   "The query returned zero, but marketing knows there are hundreds. The rows were dropped before you could count them.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
```sql
SELECT c.name
FROM customers c JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;
```

"Customers with no orders": the query is short, reads correctly, and returns
**zero rows**. The marketing team is certain there are hundreds of inactive
customers.
""",
        ask="Why can this query *never* return a row, no matter what the data contains? What kind of join does the question actually need?"),
   dict(img="figures/11-left-join-null.svg", imgh=9.0, wide=True, credit="",
        body=r"""
- An `INNER JOIN` keeps only rows that **match** in both tables. A customer with
  no orders has nothing to match, so the row is gone before `WHERE` ever sees it.
  `o.id IS NULL` is then checked on a set that cannot contain such rows.
- A **`LEFT JOIN`** keeps every customer and fills the order columns with **NULL**
  where there is no match. Now `WHERE o.id IS NULL` selects exactly the inactive ones.
- `NULL` is not a value; it means *absent*. It matches nothing, not even itself,
  which is why `= NULL` is always false and `IS NULL` exists.
""",
        uses="§12 joins: INNER versus LEFT, and NULL for missing matches · §11 selection happens *after* the join · exam item DB-09a (COUNT with a LEFT JOIN)"),
   r"""
**Source.** Standard SQL semantics (SQL-92 onward); the "anti-join" pattern
`LEFT JOIN … WHERE right.key IS NULL` is the idiomatic answer, with `NOT EXISTS`
as the alternative. The tables in the figure are illustrative.

**Facts.** Evaluation order: `FROM`/`JOIN` first, then `WHERE`, then `SELECT`.
`COUNT(*)` after a left join counts the NULL row as 1; `COUNT(o.id)` counts it
as 0, which is the trap in the exam's `DB-09a`.

**How to present.** Open with the query and "zero rows"; ask why. Many students
will say "there must be no such customers". Close with the two result tables of
the figure side by side; the highlighted NULL rows are the answer. Then state
the evaluation order; it explains both this bug and X11-B.

**Where it plugs in.** With the join-types slide of the main deck ("if values
are missing, they are set to NULL"); this is that sentence turned into a bug.
""")

# ===========================================================================
#  12  Parallel Programming
# ===========================================================================

ex("X12-A", "One million increments, and the counter says 712 431",
   "Four threads, each adding one to a shared counter 250 000 times. No error. A quarter of the additions vanished.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
A program counts events in a stream. To make it faster, four threads each
process a quarter of the stream, adding one to a **shared counter** for each
event. One million events go in.

The counter reads **712 431**. Run it again: **698 202**. Every run is different;
every run is too low.
""",
        ask="No thread has a bug. Where did 288 000 increments go, and why does the answer change every time?"),
   dict(img="figures/12-race-condition.svg", imgh=8.6, wide=True, credit="",
        body=r"""
- `counter ← counter + 1` is **three machine steps**: read, add, write. If thread
  B reads between A's read and A's write, both write the same value and one
  increment is **lost**. This is a **race condition**.
- The bug lives in the **interleaving**: no single thread's code shows it, and
  the interleaving differs each run, so the result does too.
- Fixes: a **lock** around the three steps (which serializes them, so Amdahl's
  law applies), or **no shared state**: each thread keeps its own count and the
  four are added at the end. The second is why MapReduce works.
""",
        uses="§4 types of parallelization: threads share memory · §5 concurrency: interleaving is not under your control · §9 software parallelization: why Map keeps state local · §11 Amdahl's law"),
   r"""
**Source.** Textbook race condition; the numbers are illustrative (in CPython
the GIL hides it for pure-Python `+=` but not for C extensions or other
languages). A demonstration in Java, Go or C shows losses of 20 to 40% on a
4-core laptop.

**Facts.** The three-step decomposition is what the hardware does; on some
architectures even a 64-bit write is not atomic. Locks make the increment
correct and make that section serial; the atomic-counter instruction
(`fetch-and-add`) is the hardware fix. Per-thread counters combined at the end
is the pattern with *no* shared mutable state, and it is exactly Map + Reduce.

**How to present.** Open with the two runs and the question; let the room
argue. Close with the timeline figure, then the two fixes, and make the second
one the bridge to MapReduce: the entire design of that framework is "avoid
this figure". Connects back to the two-seats booking example (M11-B), which is
the same race at the database level.

**Where it plugs in.** With the multithreading slides; before MapReduce.
""")

ex("X12-B", "Why is the GPU 50× faster, and 10× slower?",
   "The same graphics card trains the model in an hour and runs your for-loop in a week.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
A colleague moves a model-training script to the department's GPU: **50 times
faster**. Encouraged, they move their agent-based simulation, a loop over
agents with an `if` inside, to the same GPU. It runs **10 times slower** than
on the laptop.

Same card, same afternoon.
""",
        ask="What is a GPU actually good at, and what is the property of the second program that makes it a bad fit?"),
   dict(img="figures/12-simd-vs-cpu.svg", imgh=8.2, wide=True, credit="",
        body=r"""
- A GPU is **SIMD** in Flynn's taxonomy: one instruction stream applied to
  thousands of data items at once. Matrix multiplication, the whole of model
  training, is exactly that: every cell does the same multiply-add.
- A loop with a branch is **MIMD** work: different agents take different paths.
  On a GPU the lanes that took the other branch **wait**, and a 3 GHz core with
  branch prediction beats a 1.5 GHz lane every time.
- The rule: GPUs for *the same operation on a lot of data*; CPUs for *different
  operations on different data*. Most social-science code is the second kind.
""",
        uses="§6 Flynn's taxonomy: SISD, SIMD, MIMD · §7 instruction-level parallelism and why branches hurt · §8 multi-core, GPUs and clusters"),
   r"""
**Source.** GPU architecture basics (Hennessy & Patterson, *Computer
Architecture: A Quantitative Approach*, ch. 4). The 50× and 10× numbers are
typical rather than measured; the sign is what matters. Branch divergence
within a "warp" of 32 lanes is documented in every CUDA guide.

**Facts.** A modern GPU has thousands of lanes at about 1.5 GHz with a shared
instruction stream per warp; a CPU core has 3 to 5 GHz, deep pipelines and
speculative execution (session 12 §7). Memory transfer to and from the GPU is
another fixed cost that small tasks never amortize.

**How to present.** Open with the two results; the paradox is real and students
who have used Colab have met it. Close with the Flynn quadrant of the main deck
and place each program in its cell. Then the practical advice: vectorize
(NumPy, array operations) *before* buying hardware; vectorized code is SIMD
code even on a CPU.

**Where it plugs in.** With the Flynn's-taxonomy and GPU slides.
""")

ex("X12-C", "Count every word in Wikipedia in two minutes",
   "20 GB of text, 100 machines, and the reason it is not 100× faster.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
English Wikipedia is about **20 GB** of text. Counting how often every word
occurs takes a laptop around **three hours**: one pass, one dictionary (session
3). A cluster of **100 machines** does it in about **two minutes**.

Three hours divided by 100 is under two minutes, but not by much, and adding
100 more machines barely helps.
""",
        ask="How do 100 machines share one counting job without a shared dictionary? And where does the missing time go?"),
   dict(img="figures/12-mapreduce.svg", imgh=8.6, wide=True, credit="",
        body=r"""
- **MapReduce.** *Map*: each machine counts words in its own chunk, locally, with
  its own dictionary; no shared state, no race. *Shuffle*: pairs for the same
  word are sent to the same reducer. *Reduce*: add the partial counts.
- Only the small `(word, count)` pairs cross the network; the text never moves.
  **Bring the code to the data.**
- The missing time: the shuffle is network communication, the reduce is partly
  serial, and the slowest machine sets the finish line. **Amdahl's law** with a
  communication term: more machines shrink the map phase and nothing else.
""",
        uses="§9 software parallelization and MapReduce · §10 distributed inference: which computations split cleanly · §11 Amdahl's law and the serial fraction"),
   r"""
**Source.** Dean & Ghemawat (2008), whose worked example is exactly word count.
Wikipedia size: about 20 GB of article text uncompressed (dumps.wikimedia.org).
Timings are order-of-magnitude estimates, not measurements; say so.

**Facts.** Word count is the canonical MapReduce program because its Reduce
(addition) is associative and commutative, so partial counts combine in any
order. The same property is what makes the mean distribute exactly and the
median not (session 12 §10, exam `GP-17`).

**How to present.** Open with the numbers and the "not by much" remark. Close
with the figure, following one word ("the") from two chunks to one reducer.
Then the connection to X12-A: Map keeps state private *precisely* to avoid the
race; and to Amdahl: shuffle + reduce are the serial fraction, so the ceiling is
real. Ask what would break if the task were "find the median word length".

**Where it plugs in.** The MapReduce slides of the main deck; the word-count
example is a callback to the dictionary of session 3.
""")

# ===========================================================================
#  13  Social Science Applications
# ===========================================================================

ex("X13-A", "Two point four million ballots, and the wrong president",
   "The Literary Digest, 1936: the biggest poll in history, and why size did not save it.",
   dict(img="figures/13-literary-digest.png", imgh=8.4, wide=True, credit="",
        body=r"""
In 1936 the *Literary Digest* mailed 10 million ballots and received **2.4
million** back, the largest poll ever taken. It predicted **Landon 57%,
Roosevelt 43%**. A young pollster named George Gallup, with about **50 000**
interviews, predicted Roosevelt.

Roosevelt won with **61%**. The *Digest* folded within two years.
""",
        ask="How can 2.4 million responses be wrong by 18 points while 50 000 are right? And what does that say about a study of 500 million tweets?"),
   dict(img="figures/13-literary-digest.png", imgh=7.6, wide=True, credit="",
        body=r"""
- The *Digest* mailed to **its subscribers, telephone owners and car owners**,
  in 1936 the affluent. **Coverage error**: the sampling frame was not the
  electorate. The 24% who answered were also the most motivated: **non-response bias**.
- Gallup's sample was small but **designed to represent** the population.
- Size reduces **variance**, never **bias**. Digital trace data is the *Digest*
  again: a huge, self-selected, platform-shaped sample. The question is always
  *who is in the frame*, not *how many*.
""",
        uses="§6 digital behavioral data · §8 issues with representation: coverage, behavioral distortion, algorithmic confounding · §12 why data does not replace theory"),
   r"""
**Source.** Squire, P. (1988), "Why the 1936 Literary Digest Poll Failed",
*Public Opinion Quarterly* 52(1), which shows that non-response mattered at
least as much as the frame. Actual result: Roosevelt 60.8%, Landon 36.5%.
Gallup's sample size varies by account (50 000 is the commonly cited figure).

**Facts.** 10 million ballots mailed, about 2.4 million returned (24%). The
*Digest* had correctly predicted every election since 1916. Squire's
re-analysis: even among the mailed frame, respondents leaned Landon more than
non-respondents.

**How to present.** Open with the three bars and "which do you believe?"; the
room will pick the big one. Close with the two mechanisms named and separated
(frame against response), then the transfer to platforms: the Pew age-gap
table from the main deck is the modern coverage error. The line to land: **a
biased sample of a billion is a biased sample**.

**Where it plugs in.** Before the "Issues with digital behavioral data:
representation" slide of the main deck.
""")

ex("X13-B", "Is every segregated city full of racists?",
   "A grid, a rule, and a result that separates outcomes from motives.",
   dict(img="figures/13-schelling-before.svg", imgh=10.2, wide=False, credit="simulated with `tools/genexamples_figs.py`",
        body=r"""
1 440 agents of two kinds, placed at random on a 40×40 grid with 10% of cells
empty. Each agent wants **at least 30% of its neighbors** to be like itself;
it is content to be in a **70% minority**.

Unsatisfied agents move to a free cell where they would be satisfied.
""",
        ask="What does the grid look like when everyone is satisfied? And if you saw only the end state, what would you conclude about the agents' preferences?"),
   dict(img="figures/13-schelling-after.svg", imgh=10.2, wide=False, credit="simulated with `tools/genexamples_figs.py`",
        body=r"""
- After **8 rounds** and 384 moves everyone is satisfied, and the grid is
  strongly segregated: the neighborhood of the average agent went from **50%**
  to **74%** like itself, far above the 30% anyone asked for.
- Each move changes the neighborhoods of the cells left and joined, tipping
  others below threshold. Mild local preferences **compound** into global sorting.
- **Generative sufficiency**: a segregated outcome does not imply intolerant
  preferences. You cannot read motives off aggregates. This is the model's point,
  and the reason agent-based modeling belongs in the toolkit.
""",
        uses="§13 agent-based modeling and generative sufficiency · §14 Schelling's segregation model · §3 the 'generative' meaning of computational"),
   r"""
**Source.** Schelling, T. C. (1971), "Dynamic Models of Segregation", *J. Math.
Sociology* 1(2). The two grids are produced by a real run of the model in the
figure script (seed 11, $F = 0.3$, 10% empty, 40×40); the 50% to 74% and "8
rounds" figures are read from that run and change together if regenerated.

**Facts.** Schelling's original threshold examples are 1/3 and 1/2; the CMSS
course slides run the full sweep. At $F = 0.3$ the result is already clear; at
$F = 0.5$ it is stark. The measure shown is the mean share of same-kind
neighbors among occupied neighboring cells.

**How to present.** Open with the random grid and the rule; ask for a sketch of
the end state (most draw it *less* clustered than it turns out). Close with the
after-grid and the two numbers; then the inference question. The exam item
`DB-14` asks about the same model, with $F = 0.5$ in its part (e). Add: this is
also the answer to *"why simulate?"*; the result is not derivable from the rule
by inspection.

**Where it plugs in.** With the Schelling slides of the main deck (properties,
F = 0.2 simulation, tolerance results).
""")

ex("X13-C", "How many Likes does it take to know you better than your spouse?",
   "A number, a method, and a privacy problem that consent cannot fix.",
   dict(img="", imgh=0, wide=False, credit="",
        body=r"""
Personality, the Big Five, is normally measured with a 100-item questionnaire.
In 2015 researchers built a model that predicts it from a person's **Facebook
Likes** alone, and compared its accuracy to that of the person's friends,
family and spouse, who each rated the same person.

The judges knew the person for years. The model had a list of Likes.
""",
        ask="How many Likes did the model need to be as accurate as a work colleague? A friend? A spouse? And what follows for privacy, even for people who post nothing?"),
   dict(img="figures/13-likes-accuracy.png", imgh=8.4, wide=True, credit="schematic after Youyou, Kosinski & Stillwell (2015)",
        body=r"""
- **10 Likes** to match a work colleague, **70** a friend, **150** a family member,
  **300** to match the spouse. The average user then had about 227.
- Each Like is innocuous; the **pattern** is not. Kosinski et al. (2013) predicted
  sexual orientation, religion, politics and substance use from Likes at high accuracy.
- **Shadow profiles**: your friends' Likes predict *you*. Privacy is **collective**;
  no individual opt-out removes the information others' data carries about you.
""",
        uses="§10 method examples: personality from Likes · §11 issues with methods: privacy and shadow profiles · §7 digital traces as measurement · session 10 §3 supervised learning"),
   r"""
**Source.** Youyou, W., Kosinski, M. & Stillwell, D. (2015), "Computer-based
personality judgments are more accurate than those made by humans", *PNAS*
112(4): 86 220 participants; thresholds 10/70/150/300 from the paper. Kosinski,
Stillwell & Graepel (2013), *PNAS* 110(15). Garcia et al. (2018), *EPJ Data
Science* 7:3, for shadow profiles. The curve in the figure is **schematic**:
the anchors are from the paper, the line between them is drawn, and the slide
says so.

**Facts.** Human judges: self-other agreement $r \approx 0.49$; computer with
the average number of Likes $r \approx 0.56$. The model was a linear regression
on the Like matrix, nothing exotic.

**How to present.** Open with the setup and ask for the four numbers; guesses
are usually far too high for the colleague and too low for the spouse. Close
with the anchored curve, then the two implications in the last two bullets;
the second is the one students have not thought about. Connect to session 10
(this is plain supervised learning) and to the ethics list of session 10.

**Where it plugs in.** With the "Personality and Facebook likes" and "New
privacy risks" slides of the main deck.
""")
