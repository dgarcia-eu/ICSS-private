# Exercise Sheet 12: Parallel Programming

*Introduction to Computing for the Social Sciences · Prof. Dr. David Garcia*

> Exercises 1–3 are worked through in the exercise session. The *Additional
> practice* section is for self-study. Worked solutions to every exercise, with
> pointers to the slides and the handout sections that cover the material, are
> in [`Solutions/Exercise12-Solutions.md`](Solutions/Exercise12-Solutions.md); try before you open them.
> Notation: [course conventions](../Transcripts/00-Conventions.md).

---

## Exercise 1: Parallelization

You are working on parallelizing a program in which 80% of the computation is
parallelizable. Explain how you calculate your answers to the following
questions:

a) What speedup factor will you get using 4 processors instead of 1?

b) How many processors do you need to get a speedup factor of 10?

---

## Exercise 2: Distributed computation

The following is one of the versions of the formula to calculate Pearson's
correlation coefficient:

$$\rho_{xy} = \frac{n\sum_i x_i y_i - \sum_i x_i \sum_i y_i}
{\sqrt{n\sum_i x_i^2 - \left(\sum_i x_i\right)^2}\
 \sqrt{n\sum_i y_i^2 - \left(\sum_i y_i\right)^2}}$$

a) Write the pseudocode to calculate Pearson's correlation in one machine as
   above.

b) Within the framework of MapReduce, write the pseudocode of:

   - a `map()` function that receives as input a random subset of the data.
     Within this pseudocode, call the function `yield()` to send the result of
     the map operation to the reducer.
   - a `reduce()` function to calculate Pearson's correlation based on the
     results of the executions of `map()`, which are received as a list.

> The whole exercise turns on one question: **what should `map()` send?** If it
> sends a correlation, the reducer cannot recover the right answer. Look at the
> formula and find the quantities that are additive across subsets.

---

## Exercise 3: Conceptual questions

a) What is predicted by Moore's law? What is its limit and a workaround?

b) What is the difference between **concurrency** and **parallelism**? List two
   advantages and one disadvantage of concurrency in comparison to running tasks
   sequentially.

c) In your own words, explain **speculative execution** and one of its security
   risks.

d) You work for Melon Usk, who asks you to calculate the **mean** number of likes
   of 3 billion X posts. Your servers only have memory for analyzing at most one
   million posts. Describe in your own words how you would approach this problem.
   How would it differ if he asks you to calculate the **standard deviation**
   instead?

---

## Additional practice

### A1. Amdahl's law

a) A program is 95% parallelizable. What is the maximum speedup with infinitely
   many processors?
b) With 8 processors, what speedup do you achieve for $P = 0.5$, $P = 0.9$ and
   $P = 0.99$?
c) You measure a speedup of 3× on 4 processors. What fraction of the program is
   parallelizable?
d) Your manager proposes buying 64 processors instead of 16 for a program with
   $P = 0.9$. Is it worth it? Give numbers.

### A2. Which distributes exactly?

For each statistic, say whether it can be computed **exactly** by a single
MapReduce round in which each machine sends a fixed number of summary values.
If yes, give the values; if no, explain what fails.

a) The sum of $x$.
b) The mean of $x$.
c) The variance of $x$.
d) The maximum of $x$.
e) The median of $x$.
f) The number of distinct values of $x$.

### A3. Threads, processes and shared state

Two threads run this code on a shared variable `counter`, initially 0. Each
executes the loop 1000 times.

```
For i = 1 to 1000:
      counter ← counter + 1
```

a) What is the value of `counter` at the end? Give the range of possible values
   and explain.
b) Where exactly is the problem, given that `counter ← counter + 1` is one line?
c) Name the mechanism that fixes it, and say what it costs.
d) Why does this problem not arise if the two threads each increment their *own*
   counter and add the two at the end?

### A4. Concurrency or parallelism?

For each task, say whether concurrency, parallelism, both, or neither would help,
and why.

a) Downloading 500 web pages.
b) Multiplying two 5000×5000 matrices.
c) Reading one 4 GB file line by line and counting words.
d) A text editor that autosaves while you type.
e) Computing Fibonacci numbers with the naive recursion (session 6).

### A5. Flynn's taxonomy

Classify each system and justify in one sentence.

a) A pocket calculator.
b) A GPU applying the same shading formula to two million pixels.
c) A 32-core server running 32 unrelated user sessions.
d) Three independent flight-control computers checking each other's output on the
   same sensor readings.

### A6. Pipelining

A processor has the five-stage pipeline `IF ID EX MEM WB`, one cycle per stage.

a) How many cycles does one instruction take from start to finish?
b) How many cycles do 100 instructions take without pipelining?
c) How many cycles do 100 instructions take with a full pipeline?
d) A branch misprediction occurs every 20 instructions and costs 4 cycles.
   Recompute (c).
e) State in one sentence what pipelining improves and what it does not.

### A7. Designing a distributed analysis

You have 10 billion social media posts spread over 200 machines and want to
compute, for each of 50 topics, the average sentiment score of posts mentioning
it.

a) Sketch the Map and Reduce functions.
b) How much data does each machine send to the reducer? Why does this matter more
   than the size of the input?
c) The topic "election" appears in 60% of all posts while the other 49 topics
   share the rest. What problem does this create, and how would you address it?
d) You are then asked for the *median* sentiment per topic instead of the mean.
   What changes?

---

## Sources

- Exercises 1 and 2 are taken from the 2024 sheet 12 of this course; exercise 3
  is taken from its V2 variant.
- **Amdahl, G. M. (1967).** "Validity of the single processor approach to
  achieving large scale computing capabilities". *AFIPS* 30, 483–485.,
  Exercise 1 and A1.
- **Flynn, M. J. (1972).** "Some Computer Organizations and Their
  Effectiveness". *IEEE Transactions on Computers* C-21(9), 948–960.: A5.
- **Dean, J. & Ghemawat, S. (2008).** "MapReduce: Simplified Data Processing on
  Large Clusters". *Communications of the ACM* 51(1), 107–113.: Exercise 2, A7;
  the combiner and straggler discussion in A7 follows this paper.
- **Hennessy, J. L. & Patterson, D. A. (2019).** *Computer Architecture: A
  Quantitative Approach*, 6th ed. Morgan Kaufmann.: Pipelining numbers in A6.
- **Chan, T. F., Golub, G. H. & LeVeque, R. J. (1983).** "Algorithms for
  Computing the Sample Variance". *The American Statistician* 37(3), 242–247.,
  The numerical caveat in A2c.
- **Flajolet, P. et al. (2007).** "HyperLogLog: the analysis of a near-optimal
  cardinality estimation algorithm". *AofA '07*.: A2f.
- **Lawrence Livermore National Laboratory, *Introduction to Parallel
  Computing*:** <https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial>
  Race conditions and the thread/process distinction in A3, A4.
