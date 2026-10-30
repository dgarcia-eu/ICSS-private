# Why it matters: one notebook per lecture

One short, standalone Jupyter notebook for each lecture from 2 to 13. Each one
runs a small experiment that shows why the content of that lecture matters in
practice for someone who computes with data: a rounding error that changes a
result, an algorithm that becomes unusable when the data grows, a query that
takes a second instead of a minute, a model that looks accurate and is not.
The notebooks are minimal on purpose. Run them, change the numbers, and watch
what happens.

They need only Python with NumPy, matplotlib, pandas, scikit-learn and SQLite
(everything in an Anaconda installation). Every notebook is executed and its
outputs are stored, so it also reads on GitHub without a kernel; the *open*
link is the rendered page. Run them from this folder
(`jupyter lab WhyItMatters`). They are built from `tools/why_NN.py` by
`tools/genwhy.py`.

| Session | Notebook | Open | Lecture |
|---|---|---|---|
| 2 Information Coding | **The numbers your computer cannot store**: Rounding errors that add up to a wrong variance, an integer that silently turns negative, and a name that becomes two names because of one byte. | [open](W02-InformationCoding.html) · [ipynb](W02-InformationCoding.ipynb) | [handout](../Transcripts/02-InformationCoding.md) |
| 3 Data Structures | **Matching two surveys: minutes or milliseconds**: The same matching task on a list and on a set, timed as the surveys grow, and a search that halves the problem at every step. | [open](W03-DataStructures.html) · [ipynb](W03-DataStructures.ipynb) | [handout](../Transcripts/03-DataStructures.md) |
| 4 Software | **Hundred times slower, quietly wrong, and fixed by its tests**: A Python loop against compiled NumPy, a wrong mean that a one-line test catches, and a generated function whose silent error is corrected because a test suite tells the language model what is wrong. | [open](W04-Software.html) · [ipynb](W04-Software.ipynb) | [handout](../Transcripts/04-Software.md) |
| 5 Algorithms | **A network of 100 000 people: 80 gigabytes or 8 megabytes**: Two ways to store the same social network, breadth-first search giving the six degrees, and what goes wrong when the queue becomes a stack. | [open](W05-Algorithms.html) · [ipynb](W05-Algorithms.ipynb) | [handout](../Transcripts/05-Algorithms.md) |
| 6 Recursion | **The same function, 1.6 million calls or 31**: A recursive definition can be run as written or with its results saved, and the difference between the two is the difference between a second and a century. | [open](W06-Recursion.html) · [ipynb](W06-Recursion.ipynb) | [handout](../Transcripts/06-Recursion.md) |
| 7 Sorting Algorithms | **Sort it once, and sort it stably**: Three sorting algorithms on the same data, a tie order that an unstable sort scrambles, and what a sorted list buys you afterwards. | [open](W07-SortingAlgorithms.html) · [ipynb](W07-SortingAlgorithms.ipynb) | [handout](../Transcripts/07-SortingAlgorithms.md) |
| 8 Time Complexity | **Measure the slope, predict the wall**: Three ways to find duplicate ids, the growth exponent read off a log-log plot, and what each one would cost on a billion rows. | [open](W08-TimeComplexity.html) · [ipynb](W08-TimeComplexity.ipynb) | [handout](../Transcripts/08-TimeComplexity.md) |
| 9 Theoretical Computer Science | **What a machine cannot do, and what it cannot do in time**: A regular expression that takes exponential time, a group-splitting problem that no computer solves for 60 people, and a question no program can answer. | [open](W09-TheoreticalCS.html) · [ipynb](W09-TheoreticalCS.ipynb) | [handout](../Transcripts/09-TheoreticalCS.md) |
| 10 Machine Learning | **The model that learned nothing and scored 91%**: A test score that goes up when the model gets worse, and a classifier that reaches 91% on pure noise: why the train/test split has to be respected to the letter. | [open](W10-MachineLearning.html) · [ipynb](W10-MachineLearning.ipynb) | [handout](../Transcripts/10-MachineLearning.md) |
| 11 Databases | **Half a million rows, one lookup, a thousand times faster**: An index turns a scan of the whole table into a jump, the database filters before the data moves, and a transaction keeps the money from vanishing when the program crashes halfway. | [open](W11-Databases.html) · [ipynb](W11-Databases.ipynb) | [handout](../Transcripts/11-Databases.md) |
| 12 Parallel Programming | **Eight cores are not eight times faster**: A bootstrap on eight workers, the serial fraction that caps it, statistics that survive being split across machines and ones that do not, and why threads help you wait but not compute. | [open](W12-ParallelProgramming.html) · [ipynb](W12-ParallelProgramming.ipynb) | [handout](../Transcripts/12-ParallelProgramming.md) |
| 13 Social Science Applications | **Same pattern, different story**: A rise in engagement that came from the ranking algorithm, and two mechanisms that produce the same heavy tail: what a digital trace can tell you, what it cannot, and how to tell the stories apart. | [open](W13-SocialScienceApplications.html) · [ipynb](W13-SocialScienceApplications.ipynb) | [handout](../Transcripts/13-SocialScienceApplications.md) |
