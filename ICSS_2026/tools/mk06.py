#!/usr/bin/env python3
"""Emit the Quarto source of ICSS session 6 (Recursion)."""

OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/06-Recursion/ICSS-2026-06-Recursion.qmd"

HEADER = '''---
title: "<span class='course'>Introduction to Computing for the Social Sciences</span><br><span class='session'>Session 6 &ndash; Recursion</span>"
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
    footer: "<span class='fbar-left'>Session 06</span><span class='fbar-mid'>Introduction to Computing for the Social Sciences</span><span class='fbar-right'>Winter Semester 2026-2027</span>"
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
- Session 10: Machine Learning
- Session 11: Databases
- Session 12: Parallel Programming
- Session 13: Social Science Applications
- Session 14: Exam Review
:::
:::
::::
'''

P = "figures/person-"


def family(rows, height="3.4em"):
    """rows: how many generations to show (1 = P, 2 = + parents, 3 = + grandparents)."""
    out = ['<div class="family">']
    if rows >= 3:
        out.append('<div class="gen gen-grand">'
                   f'<img src="{P}gm1.png"><img src="{P}gf1.png">'
                   '<span class="gap"></span>'
                   f'<img src="{P}gm2.png"><img src="{P}gf2.png"></div>')
    if rows >= 2:
        out.append('<div class="gen gen-parents">'
                   f'<img src="{P}mother.png"><img src="{P}father.png"></div>')
    if rows >= 1:
        out.append(f'<div class="gen gen-p"><img src="{P}p.png"></div>')
    out.append('</div>')
    return "\n".join(out)


MAP = ('<img class="simpleland" src="figures/simpleland-map.png">\n'
       '<div class="simpleland-label">Simpleland</div>')

RULES = ("- P was born in Simpleland\n"
         "- either of P's parents are citizens of Simpleland")


def rules_block(hl=None, extra=None):
    r1 = "P was born in Simpleland"
    r2 = "either of P's parents are citizens of Simpleland"
    if hl == 1:
        r1 = "[" + r1 + "]{.hl}"
    if hl == 2:
        r2 = "[" + r2 + "]{.hl}"
    lines = [f"- {r1}", f"- {r2}"]
    if extra:
        lines.append(f"- [{extra}]{{.hl}}")
    return "\n".join(lines)


s = [HEADER]


def slide(title, body):
    s.append(f"\n## {title}\n\n{body}\n")


# ---------------------------------------------------------------- Simpleland
slide("Recursion example", f"""::: {{.center-h}}
![](figures/simpleland-map.png){{height="11.6em"}}

**Simpleland**
:::""")

intro = ("A person (P) is a citizen of Simpleland if it satisfies any of these "
         "conditions:")

for rows, question, hl, extra, tag in [
        (0, None, None, None, None),
        (1, "bottom", None, None, None),
        (1, "bottom", 1, None, None),
        (2, "bottom", None, None, None),
        (2, "bottom", 2, None, None),
        (3, "centre", None, None, None),
]:
    q = ""
    if question == "centre":
        q = '\n::: {.tag .qcentre}\nIs P a citizen of Simpleland?\n:::\n'
    elif question == "bottom":
        q = "\n::: {.sm}\n**Is P a citizen of Simpleland?**\n:::\n"
    body = (f"::: {{.sm}}\n{intro}\n\n{rules_block(hl, extra)}\n:::\n{q}\n"
            f"{family(rows) if rows else ''}\n\n{MAP}")
    slide("Recursion example", body)

# Components of recursion (base case / recursion case)
slide("Components of Recursion",
      f"""::: {{.sm}}
{intro}

- P was born in Simpleland &nbsp;&nbsp; [**Base case**]{{.hl}}
- either of P's parents are citizens of Simpleland
:::

{family(3)}

{MAP}""")

slide("Components of Recursion",
      f"""::: {{.sm}}
{intro}

- P was born in Simpleland
- either of P's parents are citizens of Simpleland &nbsp;&nbsp; [**Recursion case**]{{.hl}}
:::

::: {{.tag .qcentre}}
Is P a citizen of Simpleland?
:::

{family(3)}

{MAP}""")

slide("Recursion",
      """::: {.definition}
[Definition of recursion]{.label}

::: {.sm}
Recursion is a technique in mathematics, logic and computer science to specify a function through itself (a *recursive definition*). The fundamental principle of recursion is to define the value of a function $f$ through previously calculated values of the same function $f(n)$, $f(n-1)$, …
:::
:::

::: {.sm}
- as long as the start value of the function $f$ is known for sufficiently many arguments (**base cases**), any value of $f$ can be calculated
- a recursive call of the function $f$ keeps calling itself until
  - the function converges to a specific target value
  - or a pre-defined **abort condition** has been met
:::""")

slide("Issues with Recursion",
      f"""::: {{.sm}}
{intro}

{rules_block()}
:::

::: {{.tag .qcentre}}
What if we don't know all ancestors of P?
:::

{family(3)}

{MAP}""")

slide("Issues with Recursion",
      f"""::: {{.sm}}
{intro}

- P was born in Simpleland
- either of P's parents are citizens of Simpleland
- if we don't know P's parents, P is not a citizen of Simpleland &nbsp;&nbsp; [**Abort case**]{{.hl}}
:::

{family(3)}

{MAP}""")

slide("Recursion and Fractals",
      """::: {.imgrow .middle}
![](figures/recursive-drawing-1.png){height="6.4em"}
![](figures/recursive-drawing-3.png){height="6.4em"}
![](figures/recursive-drawing-2.png){height="6.4em"}
:::

::: {.source}
<http://recursivedrawing.com/>
:::""")

# ------------------------------------------------------------------ factorial
slide("Factorial: An Example",
      """::: {.sm}
How many different ways exist for arranging the four diners?
:::

:::: {.columns}
::: {.column width="16%"}
::: {.sm}
**Slots**

<br>

**Choices**
:::
:::

::: {.column width="84%"}
![](figures/06-factorial-slots.svg){height="3.4em"}
:::
::::""")

slide("Factorial: An Example",
      """::: {.sm}
How many different ways exist for arranging the four diners?
:::

:::: {.columns}
::: {.column width="16%"}
::: {.sm}
**Slots**

<br>

**Choices**
:::
:::

::: {.column width="84%"}
![](figures/06-factorial-slots-choices.svg){height="6.0em"}
:::
::::""")

slide("Factorial: An Example",
      """::: {.sm}
How many different ways exist for arranging the four diners?
:::

:::: {.columns}
::: {.column width="16%"}
::: {.sm}
**Slots**

<br>

**Choices**
:::
:::

::: {.column width="84%"}
![](figures/06-factorial-slots-choices.svg){height="6.0em"}
:::
::::

::: {.center-h}
$4! = 4 \\cdot 3 \\cdot 2 \\cdot 1 = 24$ arrangements
:::""")

slide("Factorial: A Recursive Definition",
      """::: {.sm}
**Iterative definition:** &nbsp;&nbsp; $n! = n \\, (n-1) \\, (n-2) \\dots (1)$

<br>

**Recursive definition:** &nbsp;&nbsp; $n! = n \\, (n-1)!$
:::""")

slide("Factorial: A Recursive Definition",
      """::: {.sm}
**Iterative definition:** &nbsp;&nbsp; $n! = n \\, (n-1) \\, (n-2) \\dots (1)$

<br>

**Recursive definition:** &nbsp;&nbsp; $n! = n \\, (n-1)!$
:::

::: {.center-h}
$$n! = \\begin{cases} 1 & \\text{if } n = 1 \\quad \\text{\\small (base case)}\\\\
n \\cdot (n-1)! & \\text{if } n > 1 \\quad \\text{\\small (recursion case)} \\end{cases}$$
:::""")

slide("Factorial: Iterative Implementation",
      """<pre class="pseudocode" style="width:60%;margin:0.4em auto"><i>Procedure</i> IterativeFactorial(<i>n</i>)
<i>Inputs:</i>
  <i>n</i>: positive integer
<i>Result:</i> factorial of the number <i>n</i>
result &larr; 1
<b>While</b> n &gt; 1:
      result &larr; result * n
      n &larr; n - 1
<b>return</b> result</pre>

::: {.center-h .sm}
$n! = n \\, (n-1) \\, (n-2) \\dots (1)$
:::""")

slide("Factorial: Recursive Implementation",
      """<pre class="pseudocode" style="width:64%;margin:0.4em auto"><i>Procedure</i> RecursiveFactorial(<i>n</i>)
<i>Inputs:</i>
  <i>n</i>: positive integer
<i>Result:</i> factorial of the number <i>n</i>
<b>If</b> n = 1
      <b>then return</b> 1
<b>Else</b>
      <b>return</b> n * RecursiveFactorial(n - 1)</pre>

::: {.center-h .sm}
$n! = n \\, (n-1)!$ &nbsp;&nbsp;&nbsp; $1! = 1$
:::""")

slide("Recursive factorial in Python",
      """::: {.center-h}
![](figures/python-recursive-factorial.png){height="6.4em"}
:::

::: {.center-h .sm}
$n! = n \\, (n-1)!$ &nbsp;&nbsp;&nbsp; $1! = 1$
:::""")

# overview of the seven states, then one per slide
grid = "\n".join(
    f'![](figures/06-factorial-tree-{i}.svg){{height="4.0em"}}' for i in range(1, 8))
slide("Factorial: Recursive Execution",
      f"""::: {{.sm}}
- Calculation can be represented as a tree
  - example: `fac(4)`
:::

::: {{.imgrow .middle style="flex-wrap:wrap;gap:0.6em 1.4em"}}
{grid}
:::""")

for i in range(1, 8):
    tail = ""
    if i == 7:
        tail = "\n\n::: {.center-h .sm}\n$\\Rightarrow$ `fac(4)` = 24\n:::"
    slide("Factorial: Recursive Execution",
          f"""::: {{.sm}}
- Calculation can be represented as a tree
  - example: `fac(4)`
:::

::: {{.center-h}}
![](figures/06-factorial-tree-{i}.svg){{height="9.0em"}}
:::{tail}""")

# call-stack screenshots
for n in range(32, 40):
    slide("Factorial: Recursive Execution",
          f"""::: {{.center-h}}
![](figures/callstack-{n}.jpg){{height="12.6em"}}
:::""")

# ------------------------------------------------------------------- memory
MEMFIG = '![](figures/06-process-memory.svg){height="12.6em"}'
mem_intro = ("A program being run in a machine is called a **process**. "
             "Processes require memory to run, which is organized as follows:")
mem_items = [
    ("Code Segment (CS)", "Stack Segment (SS)", "Data Segment or Heap (DS)"),
]
details = [
    None,
    ["contains executable instructions, i.e., a program loaded from hard disc",
     "typically read-only and of fixed size"],
    ["contains local variables, parameters, return address",
     "typically no execute (NX)",
     "limited in size, e.g. 8 MB for Linux, 1 MB for Windows and Java"],
    ["contains global data; Python manages all objects in a (private) heap",
     "typically no execute (NX)",
     "size is limited by main memory (RAM) or by explicit parameter when run"],
]
titles = ["Intermission: Memory of a running program"] + ["Memory of a running program"] * 3
for k in range(4):
    items = []
    for j, name in enumerate(["Code Segment (CS)", "Stack Segment (SS)",
                              "Data Segment or Heap (DS)"]):
        items.append(f"- {name}")
        if details[k] and j == k - 1:
            for d in details[k]:
                items.append(f"  - {d}")
    slide(titles[k], f""":::: {{.columns}}
::: {{.column width="52%"}}
::: {{.sm}}
{mem_intro}

{chr(10).join(items)}
:::
:::

::: {{.column width="48%"}}
{MEMFIG}
:::
::::""")

slide("Recursion: Implementation in memory",
      """::: {.sm}
- Recursion uses the **program stack**:
  - parameters
  - return address
  - local variables
  - return values
- stack grows and shrinks automatically with every method call
  - BUT has a maximum size: **stack overflows** are possible!
  - Warning: recursion in functions easily leads to stack overflow
:::""")

slide("Memes warned you about recursion",
      """:::: {.columns}
::: {.column width="44%"}
::: {.sm}
**3 Steps to being a good Programmer**

1. Avoid recursion
2. Repeat steps 1 and 2
3. Always have an exit condition
4. Beware of being off by one
:::

![](figures/meme-stack-overflow.png){height="5.6em"}
:::

::: {.column width="56%"}
![](figures/meme-distracted-boyfriend.jpg){height="8.6em"}
:::
::::""")

# --------------------------------------------------------- recursive algorithms
OUTLINE = """::: {{.outline{focus}}}
1. {a}
2. {b}
3. {c}
:::"""


def outline(cur):
    items = ["Recursion", "Recursive Algorithms", "Dynamic Programming"]
    marked = [f"[{t}]{{.current}}" if i + 1 == cur else t for i, t in enumerate(items)]
    return OUTLINE.format(focus=" .focus" if cur else "", a=marked[0], b=marked[1], c=marked[2])


slide("Outline", outline(2))

slide("The Greatest Common Divisor",
      """::: {.center-h}
![](figures/06-gcd.svg){height="12.0em"}
:::""")

GCD_PSEUDO = """<pre class="pseudocode"><i>Procedure</i> GCD(<i>a</i>, <i>b</i>)
<i>Inputs:</i>
      <i>a</i>, <i>b</i>: natural numbers (a, b &isin; &#8469;); a &ge; b
<i>Result:</i> one value with the greatest common divisor (gcd) of a and b
<b>If</b> b = 0,
       <b>then</b> t &larr; a
<b>Else</b>
       t &larr; GCD(b, mod(a,b))
<b>return</b> t</pre>"""

slide("Euclid's algorithm",
      f"""::: {{.sm}}
Uses the mathematical property: $\\gcd(a,b) = \\gcd(b,\\ a \\bmod b)$
:::

{GCD_PSEUDO}""")

slide("Euclid's algorithm",
      f"""::: {{.sm}}
Uses the mathematical property: $\\gcd(a,b) = \\gcd(b,\\ a \\bmod b)$
:::

:::: {{.columns}}
::: {{.column width="62%"}}
{GCD_PSEUDO}
:::

::: {{.column width="38%"}}
::: {{.xs}}
- $\\gcd(270, 192)$
  - $270 \\bmod 192 = 78$
  - $\\gcd(192, 78)$
    - $192 \\bmod 78 = 36$
    - $\\gcd(78, 36)$
      - $78 \\bmod 36 = 6$
      - $\\gcd(36, 6)$
        - $36 \\bmod 6 = 0$
        - $\\gcd(6, 0)$
          - **return 6**
:::
:::
::::""")

slide("Euclid and the GCD",
      """:::: {.columns}
::: {.column width="70%"}
::: {.sm}
- Euclid (~300 BC) Greek mathematician
- "Euclid of Alexandria" but little is actually known about his life, neither birth year nor place
- Commonly known as the father of geometry
- Euclid's most influential book is *Elements*, which includes the algorithm to calculate the gcd
- The original version of the algorithm did subtractions on the terms instead of modulo operations but it was recursive. However, it required more steps
- One of his lesser known books is titled *Data* (Δεδομένα), on how to study given information geometrically
:::
:::

::: {.column width="30%"}
![](figures/euclid.jpg){height="8.6em"}

::: {.xs}
Imagination of how Euclid could have looked like
:::
:::
::::""")

slide("Depth-First Search in Directed Graphs",
      """::: {.center-h}
![](figures/directed-graph.png){height="8.4em"}
:::

::: {.sm}
Several problems can be solved with depth-first search, such as:

- Is node $x$ included in the graph?
- Does a graph have a cycle?
- Does the graph have a strongly connected component?
:::""")

DFS_MAIN = """<pre class="pseudocode"><i>Procedure</i> DFS(<i>G</i>)
<i>Inputs:</i>
  <i>G</i>: a graph
<i>Result:</i> A graph with information
<b>For</b> each vertex u in G.V
      color [u] &larr; WHITE
      &pi; [u] &larr; NIL              # parent
time = 0                       # global count
<b>For</b> each vertex u in G.V
      <b>if</b> color [u] = WHITE
             <b>then</b> DFSVisit(G, u)</pre>"""

DFS_VISIT = """<pre class="pseudocode"><i>Procedure</i> DFSVisit(<i>G</i>, <i>u</i>)
<i>Inputs:</i>
  <i>G</i>: a graph
  <i>u</i>: the node to be processed
<i>Result:</i> A graph with information
time = time + 1
d [u] = time                   # discovered
color [u] = GRAY
<b>For</b> each vertex v in neighbors(u):
      <b>if</b> color [v] = WHITE
             <b>then</b> &pi; [v] &larr; u
                    DFSVisit(G, v)
color [u] &larr; BLACK
time = time + 1
f [u] = time                   # finished</pre>"""

DFS_SLIDES = [
    ("00", DFS_MAIN, "Example: Starting vertex $u = c$<br>if next node is unclear go alphabetically",
     "time = 0<br>Enter For-Loop:<br>call `DFSVisit(G, c)`"),
    ("01", DFS_VISIT, "call `DFSVisit(G, c)`<br>time = 1",
     "Enter For-Loop:<br>next adjacent white node: b<br>add parent of b<br>call `DFSVisit(G, b)`"),
    ("02", DFS_VISIT, "call `DFSVisit(G, b)`<br>time = 2",
     "Enter For-Loop:<br>next adjacent white node: e<br>add parent of e<br>call `DFSVisit(G, e)`"),
    ("03", DFS_VISIT, "call `DFSVisit(G, e)`<br>time = 3",
     "Enter For-Loop:<br>next adjacent white node: a<br>add parent of a<br>call `DFSVisit(G, a)`"),
    ("04", DFS_VISIT, "call `DFSVisit(G, a)`<br>time = 4",
     "Enter For-Loop:<br>no adjacent white nodes<br>finish `DFSVisit(G, a)`"),
    ("05", DFS_VISIT, "finish `DFSVisit(G, a)`<br>time = 5",
     "return to For-Loop of `DFSVisit(G, e)`"),
    ("06", DFS_VISIT, "return to For-Loop of `DFSVisit(G, e)`<br>time = 5",
     "Back in the For-Loop:<br>next adjacent white node: f<br>add parent of f<br>call `DFSVisit(G, f)`"),
    ("07", DFS_VISIT, "call `DFSVisit(G, f)`<br>time = 6",
     "Enter the For-Loop:<br>no adjacent white nodes<br>finish `DFSVisit(G, f)`"),
    ("08", DFS_VISIT, "finish `DFSVisit(G, f)`<br>time = 7",
     "return to For-Loop of `DFSVisit(G, e)`"),
    ("09", DFS_VISIT, "return to For-Loop of `DFSVisit(G, e)`<br>time = 7",
     "Back in the For-Loop:<br>no adjacent white nodes<br>finish `DFSVisit(G, e)`"),
    ("10", DFS_VISIT, "finish `DFSVisit(G, e)`<br>time = 8",
     "return to For-Loop of `DFSVisit(G, b)`"),
    ("11", DFS_VISIT, "return to For-Loop of `DFSVisit(G, b)`<br>time = 8",
     "Back in the For-Loop:<br>no adjacent white nodes<br>finish `DFSVisit(G, b)`"),
    ("12", DFS_VISIT, "finish `DFSVisit(G, b)`<br>time = 9",
     "return to For-Loop of `DFSVisit(G, c)`"),
    ("13", DFS_VISIT, "return to For-Loop of `DFSVisit(G, c)`<br>time = 9",
     "Back in the For-Loop:<br>next adjacent white node: g<br>add parent of g<br>call `DFSVisit(G, g)`"),
    ("14", DFS_VISIT, "call `DFSVisit(G, g)`<br>time = 10",
     "Enter the For-Loop:<br>next adjacent white node: d<br>add parent of d<br>call `DFSVisit(G, d)`"),
    ("15", DFS_VISIT, "call `DFSVisit(G, d)`<br>time = 11",
     "Enter the For-Loop:<br>no adjacent white nodes<br>finish `DFSVisit(G, d)`"),
    ("16", DFS_VISIT, "finish `DFSVisit(G, d)`<br>time = 12",
     "return to For-Loop of `DFSVisit(G, g)`"),
    ("17", DFS_VISIT, "return to For-Loop of `DFSVisit(G, g)`<br>time = 12",
     "Back in the For-Loop:<br>no adjacent white nodes<br>finish `DFSVisit(G, g)`"),
    ("18", DFS_VISIT, "finish `DFSVisit(G, g)`<br>time = 13",
     "return to For-Loop of `DFSVisit(G, c)`"),
    ("19", DFS_VISIT, "return to For-Loop of `DFSVisit(G, c)`<br>time = 13",
     "Back in the For-Loop:<br>no adjacent white nodes<br>finish `DFSVisit(G, c)`"),
    ("20", DFS_VISIT, "finish `DFSVisit(G, c)`<br>time = 14",
     "All nodes finished<br>&rarr; **FINISHED**"),
]

for key, code, head, foot in DFS_SLIDES:
    slide("Depth-First Search", f""":::: {{.columns}}
::: {{.column width="50%"}}
{code}
:::

::: {{.column width="50%"}}
::: {{.sm}}
{head}
:::

![](figures/06-dfs-{key}.svg){{height="9.6em"}}

::: {{.sm}}
{foot}
:::
:::
::::""")

slide("Depth-First Search",
      """::: {.sm}
More on Depth-First Search: See Cormen (2009)
:::

::: {.imgrow .middle}
![](figures/cormen-dfs-pseudocode.png){height="9.6em"}
![](figures/cormen-dfs-figure.jpg){height="9.6em"}
:::

::: {.source}
From *Introduction to Algorithms* by Thomas Cormen (2009)
:::""")

slide("Types of recursive algorithms",
      """:::: {.columns}
::: {.column width="64%"}
::: {.sm}
- **linear** recursion
  - method calls itself once recursively<br>e.g., factorial, gcd
- **tree** or **cascade** recursion
  - method calls itself multiple times recursively<br>e.g., DFS, fibonacci numbers (next section)
- **tail-end** recursion
  - return value of a function is calculated as a call to itself and nothing else
    - gcd is tail-recursive
  - result of the last recursive call is the final return value
- other types: **nested** recursion
  - parameters of the method contain recursive calls<br>e.g., Ackermann function:
:::
:::

::: {.column width="36%"}
![](figures/ackermann.png){height="4.0em"}
:::
::::""")

# --------------------------------------------------------- dynamic programming
slide("Outline", outline(3))

slide("Optimization Problems (Motivation)",
      """::: {.sm}
- An **optimization problem** consists of maximizing or minimizing a real function by systematically choosing input values from within an allowed set and computing the value of the function
- finding "best available" values of some objective function given a defined domain or input
- many problems in applied social science research actually have this structure
  - optimizing a statistical model
  - optimizing the parameters of a simulation model
  - calculating the shortest geographical path
:::""")

slide("Dynamic Programming",
      """::: {.definition}
[Definition of dynamic programming]{.label}

::: {.sm}
Dynamic programming refers to simplifying a complicated problem by breaking it down into simpler sub-problems and **saving the result** for the future so that we will not have to compute that same problem again.
:::
:::

::: {.sm}
While some problems cannot be taken apart this way, problems that span several points in time often do break apart recursively.

- both a mathematical optimization method and an algorithm design principle
- common technique used in engineering and economics; goes back to the idea of Richard Bellman in the 1950s
- **optimal substructure**: if a problem can be solved optimally by breaking it into sub-problems and recursively finding optimal solutions to sub-problems
:::""")

slide("Dynamic Programming for Recursion",
      """::: {.sm}
- Idea behind dynamic programming
  - use recursion but also save and re-use intermediate solutions:
    - breaking down an optimization problem into simpler sub-problems, and storing the solution to each sub-problem (called **memoization**) so that each sub-problem is only solved once
  - step-by-step put overlapping partial solutions together to form the overall solutions
  - requires checking global values at intermediate steps using all partial solutions
  - typical implementation through iteratively "filling up" an array or a matrix
  - makes code faster by reducing time complexity (reduced compute cycles) by efficient use of space
:::""")

FIB1 = """<pre class="pseudocode" style="width:66%;margin:0.4em auto"><i>Algorithm for</i> fibonacci(n) <i>- recursive version</i>
<i>Input:</i> n &isin; &#8469;
<i>Output:</i> The nth entry in the Fibonacci sequence
fib(n)
     <b>if</b> n = 0:
           <b>return</b> 0
     <b>if</b> n = 1:
           <b>return</b> 1
     <b>return</b> fib(n - 1) + fib(n - 2)</pre>"""

FIB2 = """<pre class="pseudocode" style="width:70%;margin:0.4em auto"><i>Algorithm for</i> fibonacci(n) <i>- recursive but more efficient</i>
<i>Input:</i> n &isin; &#8469;
<i>Output:</i> The nth entry in the Fibonacci sequence
<i>Data:</i> memo array initially all set to NIL
fib(n)
     <b>if</b> n = 0:
           <b>return</b> 0
     <b>if</b> n = 1:
           <b>return</b> 1
     <b>if</b> memo[n] &ne; NIL:
           <b>return</b> memo[n]
     memo[n] = fib(n-1) + fib(n-2)
     <b>return</b> memo[n]</pre>"""

FIB3 = """<pre class="pseudocode" style="width:66%;margin:0.4em auto"><i>Algorithm for</i> fibonacci(n) <i>- fully iterative</i>
<i>Input:</i> n &isin; &#8469;
<i>Output:</i> The nth entry in the Fibonacci sequence
<i>Data:</i> memo array
fib(n):
     memo[0] = 0
     memo[1] = 1
     <b>for</b> i <b>from</b> 2 <b>to</b> n+1:
           memo[i] = memo[i-1] + memo[i-2]
     <b>return</b> memo[n]</pre>"""

slide("Example: Fibonacci numbers", FIB1 + """

::: {.center-h .sm}
The number of calls to `fib(n)` grows **exponentially** with $n$
:::""")
slide("Example: Fibonacci numbers", FIB2)
slide("Example: Fibonacci numbers", FIB2 + """

::: {.center-h .sm}
Previously calculated results are saved in `memo`
:::""")
slide("Example: Fibonacci numbers", FIB3)

slide("Outtake &ndash; Types of algorithms",
      """::: {.sm}
The most prevalent problem-solving heuristics you will encounter

- **Recursion**
  - optimization through recursive function call, e.g. DFS
  - requires specifying sensible abort conditions
- **Greedy**
  - successive extension of partial solutions, e.g. BFS
  - determines locally optimal choice at each step, then moves on
  - only correct if local optimum also leads to globally optimal solutions
- **Divide and Conquer**
  - separate the problem into decoupled/non-overlapping smaller sub-problems. More next session!
  - solve sub-problems independently
  - if necessary, collapse all sub-results to global results
:::""")

slide("Next Session",
      """- Sorting Algorithms
- Divide and Conquer Algorithms""")

slide("Evaluation for Introduction to Programming with Python",
      """::: {.center-h}
![](figures/evaluation-qr.png){height="9.0em"}

<https://evasys.uni-konstanz.de/evasys/online.php?pswd=DPQ9D>
:::""")

open(OUT, "w").write("".join(s))
print("slides:", "".join(s).count("\n## "))
