# Worked examples: questions, answers, notebooks

Thirty-six question-and-answer examples, three per session from 2 to 13. Each one exists in
three forms. The first is a **blog-style post** for self-study in `posts/`, with the puzzle,
what is going on, the answer, why it matters for research, and links to the sections of the
lecture transcript it rests on. The second is a **Jupyter notebook** in `notebooks/` that
reproduces the problem and the solution in a few simple cells, using the standard library
plus NumPy, matplotlib, pandas, scikit-learn and SQLite; every notebook is executed and its
outputs are stored, so it reads on GitHub without a kernel. The third is a **pair of slides**,
an opening question and a closing answer, in the example deck of the session under
`../Slides/Examples/`.

Start with the post; open the notebook when it says *try it first*. Notebooks run from this
folder (`jupyter lab Examples/notebooks`); the Titanic one reads `notebooks/data/titanic.csv`.

| Session | Example | Post | Notebook (browser · file) | Slides |
|---|---|---|---|---|
| 2 Information Coding | **The clock that ends on 19 January 2038**: Why one specific second breaks a 32-bit counter, and what it wraps to. | [X02-A](posts/X02-A-the-clock-that-ends-in-2038.md) | [open](notebooks/X02-A.html) · [ipynb](notebooks/X02-A.ipynb) | [deck](../Slides/Examples/02-Examples/ICSS-2026-02-Examples.qmd) |
| 2 Information Coding | **0.1 + 0.2 is not 0.3**: The most famous wrong answer in computing, resolved bit by bit. | [X02-B](posts/X02-B-0.1-plus-0.2.md) | [open](notebooks/X02-B.html) · [ipynb](notebooks/X02-B.ipynb) | [deck](../Slides/Examples/02-Examples/ICSS-2026-02-Examples.qmd) |
| 2 Information Coding | **Why your boarding pass spells you MUELLER**: Passports, airlines and ASCII: what happens to a name when the alphabet has 37 symbols. | [X02-C](posts/X02-C-boarding-pass-mueller.md) | [open](notebooks/X02-C.html) · [ipynb](notebooks/X02-C.ipynb) | [deck](../Slides/Examples/02-Examples/ICSS-2026-02-Examples.qmd) |
| 3 Data Structures | **Where does the Back button keep the pages?**: Visit A, B, C, go back twice, then open D. Where did C go? Two stacks explain every browser. | [X03-A](posts/X03-A-the-back-button.md) | [open](notebooks/X03-A.html) · [ipynb](notebooks/X03-A.ipynb) | [deck](../Slides/Examples/03-Examples/ICSS-2026-03-Examples.qmd) |
| 3 Data Structures | **Count a million words: 49 seconds or 0.01**: The same loop, two containers, a factor of 4 500, measured on this laptop. | [X03-B](posts/X03-B-count-a-million-words.md) | [open](notebooks/X03-B.html) · [ipynb](notebooks/X03-B.ipynb) | [deck](../Slides/Examples/03-Examples/ICSS-2026-03-Examples.qmd) |
| 3 Data Structures | **The waiting room that gets slower the fuller it is**: Calling the next patient costs 1 000 moves in one structure and one in another. | [X03-C](posts/X03-C-the-waiting-room.md) | [open](notebooks/X03-C.html) · [ipynb](notebooks/X03-C.ipynb) | [deck](../Slides/Examples/03-Examples/ICSS-2026-03-Examples.qmd) |
| 4 Software | **The survey whose ages summed to a 40 000-digit number**: One operator, two types, two meanings: the most common bug in beginner data code. | [X04-A](posts/X04-A-the-40000-digit-sum.md) | [open](notebooks/X04-A.html) · [ipynb](notebooks/X04-A.ipynb) | [deck](../Slides/Examples/04-Examples/ICSS-2026-04-Examples.qmd) |
| 4 Software | **The rocket that exploded because a number did not fit**: Ariane 5, 4 June 1996: US$370 million, 37 seconds, one integer conversion. | [X04-B](posts/X04-B-ariane-5.md) | [open](notebooks/X04-B.html) · [ipynb](notebooks/X04-B.ipynb) | [deck](../Slides/Examples/04-Examples/ICSS-2026-04-Examples.qmd) |
| 4 Software | **Was 1900 a leap year? Excel says yes**: A three-line rule, a 120-year-old bug, and why control flow has to be written down exactly. | [X04-C](posts/X04-C-was-1900-a-leap-year.md) | [open](notebooks/X04-C.html) · [ipynb](notebooks/X04-C.ipynb) | [deck](../Slides/Examples/04-Examples/ICSS-2026-04-Examples.qmd) |
| 5 Algorithms | **What is your Erdős number?**: Six degrees, measured: how to compute a distance in a graph of two million authors. | [X05-A](posts/X05-A-erdos-number.md) | [open](notebooks/X05-A.html) · [ipynb](notebooks/X05-A.ipynb) | [deck](../Slides/Examples/05-Examples/ICSS-2026-05-Examples.qmd) |
| 5 Algorithms | **The seven bridges of Königsberg**: Euler, 1736: the first graph problem, and the first proof that something cannot be done. | [X05-B](posts/X05-B-konigsberg.md) | [open](notebooks/X05-B.html) · [ipynb](notebooks/X05-B.ipynb) | [deck](../Slides/Examples/05-Examples/ICSS-2026-05-Examples.qmd) |
| 5 Algorithms | **Solve the maze without luck**: A procedure that finds the shortest way out of any maze, and knows when it has. | [X05-C](posts/X05-C-solve-the-maze.md) | [open](notebooks/X05-C.html) · [ipynb](notebooks/X05-C.ipynb) | [deck](../Slides/Examples/05-Examples/ICSS-2026-05-Examples.qmd) |
| 6 Recursion | **The monks, the 64 disks, and the end of the world**: A legend, a two-line recursive plan, and an exact count of 18 446 744 073 709 551 615 moves. | [X06-A](posts/X06-A-towers-of-hanoi.md) | [open](notebooks/X06-A.html) · [ipynb](notebooks/X06-A.ipynb) | [deck](../Slides/Examples/06-Examples/ICSS-2026-06-Examples.qmd) |
| 6 Recursion | **Draw this tree in five lines**: A picture that is made of smaller copies of itself, and the code that has the same shape. | [X06-B](posts/X06-B-fractal-tree.md) | [open](notebooks/X06-B.html) · [ipynb](notebooks/X06-B.ipynb) | [deck](../Slides/Examples/06-Examples/ICSS-2026-06-Examples.qmd) |
| 6 Recursion | **You have more ancestors than there were people**: Thirty generations back, 2³⁰ ancestors, but the world held 400 million. What gives? | [X06-C](posts/X06-C-more-ancestors-than-people.md) | [open](notebooks/X06-C.html) · [ipynb](notebooks/X06-C.ipynb) | [deck](../Slides/Examples/06-Examples/ICSS-2026-06-Examples.qmd) |
| 7 Sorting Algorithms | **How the post office sorts 20 million letters a night**: No comparisons at all: sorting by postcode, one digit at a time. | [X07-A](posts/X07-A-radix-sort-postcodes.md) | [open](notebooks/X07-A.html) · [ipynb](notebooks/X07-A.ipynb) | [deck](../Slides/Examples/07-Examples/ICSS-2026-07-Examples.qmd) |
| 7 Sorting Algorithms | **Can you sort 8 things in 10 comparisons?**: A colleague claims a sorting algorithm that beats every known one. Prove them wrong without seeing it. | [X07-B](posts/X07-B-sort-8-in-10-comparisons.md) | [open](notebooks/X07-B.html) · [ipynb](notebooks/X07-B.ipynb) | [deck](../Slides/Examples/07-Examples/ICSS-2026-07-Examples.qmd) |
| 7 Sorting Algorithms | **The median of a billion salaries, without sorting**: You only need the middle value; sorting all of them is work you did not ask for. | [X07-C](posts/X07-C-median-without-sorting.md) | [open](notebooks/X07-C.html) · [ipynb](notebooks/X07-C.ipynb) | [deck](../Slides/Examples/07-Examples/ICSS-2026-07-Examples.qmd) |
| 8 Time Complexity | **Tr0ub4dor&3 or correct horse battery staple?**: Which password is safer, and why the answer is a growth rate. | [X08-A](posts/X08-A-password-strength.md) | [open](notebooks/X08-A.html) · [ipynb](notebooks/X08-A.ipynb) | [deck](../Slides/Examples/08-Examples/ICSS-2026-08-Examples.qmd) |
| 8 Time Complexity | **The clustering script that ran out of memory at 100 000**: It worked on 10 000 respondents. Ten times more data, one hundred times more memory. | [X08-B](posts/X08-B-clustering-out-of-memory.md) | [open](notebooks/X08-B.html) · [ipynb](notebooks/X08-B.ipynb) | [deck](../Slides/Examples/08-Examples/ICSS-2026-08-Examples.qmd) |
| 8 Time Complexity | **Computers got 1 000× faster. Solving got 43 000 000× faster.**: Where did the other 43 000× come from? Not from hardware. | [X08-C](posts/X08-C-algorithms-vs-hardware.md) | [open](notebooks/X08-C.html) · [ipynb](notebooks/X08-C.ipynb) | [deck](../Slides/Examples/08-Examples/ICSS-2026-08-Examples.qmd) |
| 9 Theoretical Computer Science | **Design a coffee machine that cannot be cheated**: 10-cent and 20-cent coins, a 50-cent coffee, and the smallest machine that gets it right every time. | [X09-A](posts/X09-A-coffee-machine-automaton.md) | [open](notebooks/X09-A.html) · [ipynb](notebooks/X09-A.ipynb) | [deck](../Slides/Examples/09-Examples/ICSS-2026-09-Examples.qmd) |
| 9 Theoretical Computer Science | **Can a finite machine check your brackets?**: Every editor flags a missing parenthesis. What kind of machine does it take? | [X09-B](posts/X09-B-brackets-and-stacks.md) | [open](notebooks/X09-B.html) · [ipynb](notebooks/X09-B.ipynb) | [deck](../Slides/Examples/09-Examples/ICSS-2026-09-Examples.qmd) |
| 9 Theoretical Computer Science | **Is there a fast way to solve any Sudoku?**: A newspaper puzzle, a million-dollar question, and why they are the same thing. | [X09-C](posts/X09-C-sudoku-np.md) | [open](notebooks/X09-C.html) · [ipynb](notebooks/X09-C.ipynb) | [deck](../Slides/Examples/09-Examples/ICSS-2026-09-Examples.qmd) |
| 10 Machine Learning | **The wolf detector that only saw snow**: Right on eight test images out of ten, useless at the zoo, and how to find out why. | [X10-A](posts/X10-A-wolf-detector-snow.md) | [open](notebooks/X10-A.html) · [ipynb](notebooks/X10-A.ipynb) | [deck](../Slides/Examples/10-Examples/ICSS-2026-10-Examples.qmd) |
| 10 Machine Learning | **Predict who survived the Titanic in five words**: A one-feature rule gets 79%. Every model you build must beat it. | [X10-B](posts/X10-B-titanic-in-five-words.md) | [open](notebooks/X10-B.html) · [ipynb](notebooks/X10-B.ipynb) | [deck](../Slides/Examples/10-Examples/ICSS-2026-10-Examples.qmd) |
| 10 Machine Learning | **How many groups are there?**: 240 survey respondents, two scores, no labels, and the algorithm that finds groups even when there are none. | [X10-C](posts/X10-C-how-many-groups.md) | [open](notebooks/X10-C.html) · [ipynb](notebooks/X10-C.ipynb) | [deck](../Slides/Examples/10-Examples/ICSS-2026-10-Examples.qmd) |
| 11 Databases | **Little Bobby Tables**: A boy's name deletes a school's records. The bug is in one line, and it is a lesson about data versus code. | [X11-A](posts/X11-A-little-bobby-tables.md) | [open](notebooks/X11-A.html) · [ipynb](notebooks/X11-A.ipynb) | [deck](../Slides/Examples/11-Examples/ICSS-2026-11-Examples.qmd) |
| 11 Databases | **The join that returned more rows than the table**: Eight purchases, two products, sixteen rows. Nothing crashed. The report is wrong. | [X11-B](posts/X11-B-join-explosion.md) | [open](notebooks/X11-B.html) · [ipynb](notebooks/X11-B.ipynb) | [deck](../Slides/Examples/11-Examples/ICSS-2026-11-Examples.qmd) |
| 11 Databases | **Find the customers who never ordered**: The query returned zero, but marketing knows there are hundreds. The rows were dropped before you could count them. | [X11-C](posts/X11-C-customers-who-never-ordered.md) | [open](notebooks/X11-C.html) · [ipynb](notebooks/X11-C.ipynb) | [deck](../Slides/Examples/11-Examples/ICSS-2026-11-Examples.qmd) |
| 12 Parallel Programming | **One million increments, and the counter says 712 431**: Four threads, each adding one to a shared counter 250 000 times. No error. A quarter of the additions vanished. | [X12-A](posts/X12-A-lost-increments.md) | [open](notebooks/X12-A.html) · [ipynb](notebooks/X12-A.ipynb) | [deck](../Slides/Examples/12-Examples/ICSS-2026-12-Examples.qmd) |
| 12 Parallel Programming | **Why is the GPU 50× faster, and 10× slower?**: The same graphics card trains the model in an hour and runs your for-loop in a week. | [X12-B](posts/X12-B-gpu-faster-and-slower.md) | [open](notebooks/X12-B.html) · [ipynb](notebooks/X12-B.ipynb) | [deck](../Slides/Examples/12-Examples/ICSS-2026-12-Examples.qmd) |
| 12 Parallel Programming | **Count every word in Wikipedia in two minutes**: 20 GB of text, 100 machines, and the reason it is not 100× faster. | [X12-C](posts/X12-C-mapreduce-word-count.md) | [open](notebooks/X12-C.html) · [ipynb](notebooks/X12-C.ipynb) | [deck](../Slides/Examples/12-Examples/ICSS-2026-12-Examples.qmd) |
| 13 Social Science Applications | **Two point four million ballots, and the wrong president**: The Literary Digest, 1936: the biggest poll in history, and why size did not save it. | [X13-A](posts/X13-A-literary-digest-1936.md) | [open](notebooks/X13-A.html) · [ipynb](notebooks/X13-A.ipynb) | [deck](../Slides/Examples/13-Examples/ICSS-2026-13-Examples.qmd) |
| 13 Social Science Applications | **Is every segregated city full of racists?**: A grid, a rule, and a result that separates outcomes from motives. | [X13-B](posts/X13-B-schelling-segregation.md) | [open](notebooks/X13-B.html) · [ipynb](notebooks/X13-B.ipynb) | [deck](../Slides/Examples/13-Examples/ICSS-2026-13-Examples.qmd) |
| 13 Social Science Applications | **How many Likes does it take to know you better than your spouse?**: A number, a method, and a privacy problem that consent cannot fix. | [X13-C](posts/X13-C-likes-and-personality.md) | [open](notebooks/X13-C.html) · [ipynb](notebooks/X13-C.ipynb) | [deck](../Slides/Examples/13-Examples/ICSS-2026-13-Examples.qmd) |

## Historical background

One post per session on the developments behind the topic, not technical, and starting
where the person slide of the lecture starts (Hopper, Lovelace, al-Khwarizmi, von Neumann,
Hinton). Each post features **at most three people**, at least one of them a woman or a
person of color whose contribution the usual telling leaves out, and otherwise tells the
story as an arc of the field rather than as a gallery of individuals.

| Session | Post |
|---|---|
| 1 Introduction | [When computers were people](posts/H01-when-computers-were-people.md) |
| 2 Information Coding | [A mathematical theory of communication](posts/H02-a-mathematical-theory-of-communication.md) |
| 3 Data Structures | [Shapes for data](posts/H03-shapes-for-data.md) |
| 4 Software | [Telling the machine what to do](posts/H04-telling-the-machine-what-to-do.md) |
| 5 Algorithms | [The namesake, and the first programs](posts/H05-the-namesake-and-the-first-programs.md) |
| 6 Recursion | [Defined in terms of itself](posts/H06-defined-in-terms-of-itself.md) |
| 7 Sorting Algorithms | [Putting things in order](posts/H07-putting-things-in-order.md) |
| 8 Time Complexity | [How long will it take?](posts/H08-how-long-will-it-take.md) |
| 9 Theoretical Computer Science | [What can be computed?](posts/H09-what-can-be-computed.md) |
| 10 Machine Learning | [Learning from examples](posts/H10-learning-from-examples.md) |
| 11 Databases | [One copy of every fact](posts/H11-one-copy-of-every-fact.md) |
| 12 Parallel Programming | [Many hands](posts/H12-many-hands.md) |
| 13 Social Science Applications | [Society as computation](posts/H13-society-as-computation.md) |

## Figures in the posts

Every post carries figures every two or three paragraphs: the example posts reuse the slide
figures from `../Slides/Examples/figures/`, and the history posts use portraits and
photographs from Wikimedia Commons, stored in `posts/img/` with license and author in
`posts/img/credits.json` and repeated in every caption. `tools/fetchportraits.py` fetched
them (free licenses only); `tools/figposts.py` places them.

## Rebuilding

- `python3 tools/genexnotebooks.py` builds and executes every notebook from `tools/exnb_a.py`
  and `tools/exnb_b.py`; pass ids to rebuild a subset.
- `python3 tools/knitexamples.py` knits posts, this index, the transcripts and the notebooks to
  HTML next to the sources (`index.html`, `posts/*.html`, `notebooks/*.html`), with every link
  rewritten so that it opens in a browser.
- The posts are plain Markdown, written by hand; their figures are the slide figures in
  `../Slides/Examples/figures/`.
- Notebook outputs on timing cells (word counts, queues, brute force) are from the machine that
  ran them last; the shape of the result is what matters, not the seconds.
