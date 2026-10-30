# Session 12: Parallel Programming

*Introduction to Computing for the Social Sciences · lecture transcript*

> Companion text for lecture 12. Notation follows
> [the course conventions](00-Conventions.md).
>
> **Reading for this session:** section 4.8, "Parallel Computing", of DeNero,
> *Composing Programs*, and chapter 5, "Programming with Big Data", of Foster
> et al. (eds.), *Big Data and Social Science* (2017). Before the next
> exercise session, install `jq` from <https://jqlang.org/>. References at
> the end.

---

## Contents

<!-- MOTIVATION-TOC:BEGIN -->
0. [Motivating examples](#motivating-examples)
<!-- MOTIVATION-TOC:END -->
1. [Moore's law and why it is running out](#1-moores-law-and-why-it-is-running-out)
2. [The brain as an inspiration](#2-the-brain-as-an-inspiration)
3. [Reasons to parallelize](#3-reasons-to-parallelize)
4. [Types of parallelization](#4-types-of-parallelization)
5. [Concurrency vs parallelism](#5-concurrency-vs-parallelism)
6. [Flynn's taxonomy](#6-flynns-taxonomy)
7. [Instruction-level parallelism](#7-instruction-level-parallelism)
8. [Multi-core, GPUs and clusters](#8-multi-core-gpus-and-clusters)
9. [Software parallelization and MapReduce](#9-software-parallelization-and-mapreduce)
10. [Distributed statistical inference](#10-distributed-statistical-inference)
11. [Amdahl's law](#11-amdahls-law)
12. [Summary](#12-summary)
13. [Check yourself](#13-check-yourself)
14. [References](#14-references)

---

<!-- MOTIVATION-SECTION:BEGIN -->
## Motivating examples

Three candidate openings for this session, each a real situation the
material is the answer to. **One of these will be used in the lecture**;
the others are kept here because they are worth reading anyway.

<!-- MOTIVATION:M12-A:BEGIN -->
### A · Your laptop stopped getting faster in 2005

Between roughly 1975 and 2005 there was a reliable way to make slow code
fast: wait. Processor clock speeds doubled every couple of years alongside
transistor counts, so the same unmodified program ran twice as fast on the
hardware of two years later, and nobody had to do anything. That stopped.
Clock speeds hit a wall around 3 GHz in the mid-2000s and have essentially
stayed there for twenty years, because power consumption and heat rise faster
than the clock frequency and there is no way to remove the heat. Moore's law
itself did not stop, since transistor counts kept roughly doubling; the
transistors simply went somewhere else, into cores. The consequence is a
genuine break in how performance works. A sequential program gets no faster
on a 128-core machine than on a 4-core one: it uses one core, and the other
127 sit idle. Making use of them requires the program to be written to use
them, which is a software problem, and increasingly the only remaining source
of speedup. This is what Herb Sutter called "the free lunch is over", and it
is why a course like this has a session on parallelism at all: for the first
time in the history of computing, performance is something you have to ask
for.

Two qualifications belong right here, before any enthusiasm sets in. First,
parallelism does not change complexity. An $O(n^2)$ algorithm on 100 cores is
still $O(n^2)$, because you have divided the work by 100, which is a constant
factor. The lesson of session 8 holds: if your program is too slow, check
whether you have an algorithm problem before you reach for hardware, because
no number of cores rescues the wrong growth rate. Second, the speedup is
bounded, and by less than you would guess. Whatever fraction of your program
cannot be parallelized sets a hard ceiling on the whole thing, no matter how
many processors you buy, and that fraction is usually larger than people
expect, since reading the input, writing the output and the sequential
combination step all count. The formula that quantifies it, Amdahl's law, is
the last thing in this session and the most commonly misapplied idea in it.

Section 1 of this session is about Moore's law, its physical limits, and why
parallelization is the workaround. Sections 4 and 5 give the vocabulary,
multiprocessor, multicore and multithreading, and the distinction between
concurrency, a way of structuring a program, and parallelism, a way of
executing one; confusing those two is the most common error in this
material. Sections 7 and 8 show where the parallelism actually lives in your
machine, in instruction pipelines, cores, GPUs and clusters, and section 11
presents Amdahl's law and the ceiling. The practical framing is that your
laptop has had multiple cores for your entire adult life, and almost every
analysis script you have written has used one of them. This session is about
when that is worth changing and when it is not.
<!-- MOTIVATION:M12-A:END -->
<!-- MOTIVATION:M12-B:BEGIN -->
### B · Sixteen cores, and 2.5× faster

An agent-based model takes 40 hours on your laptop. The department has a
16-core node on the cluster. You expect two and a half hours and you get 16.
You request a 64-core node and you get 15. Nothing is broken, nobody
misconfigured anything, and the numbers are exactly what theory predicts.
Gene Amdahl wrote the formula down in 1967:

$$S = \frac{1}{(1 - P) + \dfrac{P}{N}},$$

where $P$ is the fraction of the computation that can be parallelized and
$N$ the number of processors. Read the denominator: $(1-P)$ is the serial
part, which $N$ never touches, and $P/N$ is the parallel part shared out. Fit
it to the observation. A speedup of 2.5 on 16 cores means

$$2.5 = \frac{1}{(1-P) + P/16} \;\Longrightarrow\; P \approx 0.64,$$

so 64% of the runtime parallelizes and 36% does not: reading the input
files, seeding the model, collecting results, writing output, and the parts
of the simulation that are inherently sequential. Now predict the 64-core
run,

$$S = \frac{1}{0.36 + 0.64/64} = \frac{1}{0.37} = 2.70 \;\Longrightarrow\;
40 / 2.70 \approx 15\ \text{hours},$$

which is what happened. And the ceiling, as $N \to \infty$, is

$$S_{\max} = \frac{1}{1 - P} = \frac{1}{0.36} = 2.8\times.$$

Forty hours will never become less than fourteen, on any machine that will
ever exist, until the 36% is reduced. Two things follow, and both are
counterintuitive enough to be worth stating plainly. Diminishing returns
arrive immediately: going from 1 to 4 cores buys most of what there is, the
64th core contributes essentially nothing, and the efficiency, speedup per
core, falls from 100% to 4%, so on a shared cluster you are occupying 64
cores to do the work of three, which is a cost to other people. And the lever
is the serial fraction, not the core count: reducing $1-P$ from 36% to 10%
would raise the ceiling from 2.8× to 10×, which means profiling to find where
the serial time actually goes, and it is usually somewhere dull, like parsing
input files, rather than in the interesting part of the model.

Section 11 of this session presents Amdahl's law itself, with the worked
table and the limit. Sections 4 and 5 are about what can and cannot be
parallelized in the first place, and why the answer usually comes down to
shared mutable state. Section 9 is about software parallelization, including
the observation that divide-and-conquer algorithms like mergesort parallelize
almost for free because their subproblems touch disjoint data. The rule to
take to the cluster is to measure $P$ before requesting nodes. One profiling
run tells you the ceiling, and it is frequently low enough that the right
answer is to fix the serial part instead.
<!-- MOTIVATION:M12-B:END -->
<!-- MOTIVATION:M12-C:BEGIN -->
### C · Three billion posts, one million rows of memory

Three billion posts. You want the correlation between likes and reshares.
Your machine holds a million rows at a time, so the data must be processed in
about 3 000 chunks. The natural thing to do is to compute the correlation
within each chunk and to average the 3 000 results. It produces a number, and
it is not the correlation. The reason is that Pearson's $\rho$ is a nonlinear
function of the data, and averaging a nonlinear function computed on subsets
does not recover the function of the whole. Plotting the chunk-average
estimate against the true whole-sample value gives a cloud, not a line. Do
the same thing with the mean and you get a perfect line, because the mean is
linear, and an average of averages, with equal chunk sizes, is the average.
So the question is not how to split the data, but which quantities survive
being split.

For the correlation, the answer is that $\rho$ can be written entirely in
terms of sums,

$$\rho_{xy} = \frac{n\sum x_i y_i - \sum x_i \sum y_i}
{\sqrt{n\sum x_i^2 - (\sum x_i)^2}\ \sqrt{n\sum y_i^2 - (\sum y_i)^2}},$$

and sums are additive across a partition. So each chunk returns six numbers,
$n$, $\sum x$, $\sum y$, $\sum x^2$, $\sum y^2$ and $\sum xy$, the coordinator
adds them, and evaluates the formula once. The result is exactly the
whole-data correlation, not an approximation, and memory never exceeds one
chunk plus six accumulators. Six numbers per chunk instead of a million rows:
that is the whole idea behind distributed computing on data at this scale,
bring the code to the data and move only the summaries. The general
principle is worth more than the formula. Look for quantities that are
additive over partitions and sufficient to determine the statistic you want.
Where they exist, the computation distributes exactly. Where they do not,
as for the median, the quantiles or the number of distinct values, you need
several communication rounds or an approximation with a stated error bound.
That is a genuine limitation, not an implementation detail, and knowing on
which side of it your estimator falls is the useful skill.

Section 9 of this session presents MapReduce, with the Map phase computing
partial results locally, the communication phase, and the Reduce phase
combining them. Section 10 is about distributed statistical inference
specifically, with the mean as the easy case, the correlation as the
instructive one, and the trade of extra communication time against extra
variance in the estimate. Section 11 presents Amdahl's law, since the Reduce
step is serial and therefore sets the ceiling. The warning to carry into your
own work is that you cannot distribute an estimator just because you can
distribute a mean. Medians, quantiles, variances, regression coefficients and
correlations each need to be thought about separately, and the naive answer
is wrong for most of them.
<!-- MOTIVATION:M12-C:END -->
---

<!-- MOTIVATION-SECTION:END -->
## 1. Moore's law and why it is running out

*Moore's law* predicts that the number of transistors per microchip doubles
every two years, an exponential growth in computing power. While the
increase is still exponential, the rate is slower and doubling now takes more
than two years, and there is a physical limit, because a transistor cannot be
smaller than an atom. The limit is expected to be reached in this decade
unless radically different models of computation become feasible, and
parallelization, that is, using several processors, is a workaround to this
limit. That last observation is the reason why this lecture exists. For
forty years, the way to make a slow program fast was to wait, because the
same code ran twice as fast on the hardware of two years later. That free
lunch is over. Since roughly 2005, the transistor count still rises but the
clock speed does not, and the extra transistors go into more cores rather
than into faster ones. Making use of them is now a software problem, which
means that it is your problem. Connect this to session 8: parallelization
changes the constant factor, not the complexity class, so an $O(n^2)$
algorithm on 100 cores is still $O(n^2)$. If your program is too slow, first
check whether you have an algorithm problem, because no amount of hardware
fixes that. To learn more about Moore's law, Our World in Data keeps the
transistor counts up to date at
<https://ourworldindata.org/technological-change#advances-in-computational-technology>.

---

## 2. The brain as an inspiration

The lecture compares the brain with two machines:

| | Operations/sec | Power (Watts) | Cores | sec/cycle |
|---|---|---|---|---|
| **Brain** | $10^{13}$ | 15–20 | ? | $10^{-3}$ |
| **Intel Terascale** | $10^{12}$ | 85 | 80 | $10^{-9}$ |
| **Supercomputer Blue Gene** | $3.6 \times 10^{14}$ | $1.2 \times 10^{6}$ | 130 000 | $10^{-9}$ |

Read the table by columns rather than by rows. Brains work slowly but are
massively parallel: a neuron fires on a millisecond timescale, a million
times slower than a transistor switches, and the brain nonetheless reaches
$10^{13}$ operations per second because enormously many things happen at
once. And it does so on about 20 watts, the power of a light bulb, while Blue
Gene needs 1.2 megawatts for 36 times the throughput; per operation and
watt, biology wins by more than three orders of magnitude. The number of
cores of a brain is a question mark because the analogy breaks down, since
neurons are not general-purpose processors executing instructions. The
parallelism is visible in fMRI images, which show various regions of the
brain active at the same time during a single task. IBM Blue Gene is the
canonical example of a parallel computer built the other way, from many
conventional processors wired together.

---

## 3. Reasons to parallelize

There are three reasons to parallelize. The first is to save time or money:
we can throw compute resources at a problem and shorten the compute time,
and we can use cheap commodity components to build parallel processors,
which is the insight behind Beowulf clusters and, later, cloud computing,
because a hundred ordinary machines cost far less than one machine a hundred
times as fast, if such a machine even exists. The second is to solve larger
and more complex problems: some problems are so large that they are
infeasible to solve with serial computation, especially with limited memory,
and web search engines and databases processing millions of transactions
every second are the example; note the word memory, because sometimes you
parallelize not for speed but because the data does not fit on one machine.
The third is to provide concurrency: a single compute resource can only do
one thing at a time, while multiple compute resources can do many things
simultaneously.

---

## 4. Types of parallelization

There are different ways to multiply processing. A *multiprocessor* system
has more than one CPU, a *multicore* processor is one CPU with several cores,
and *multithreading* lets a single core execute more than one task
concurrently. The three are not alternatives; a modern laptop is all three
at once. The unit of software that runs on them is the process. A *process*
owns its code, its data and its file pointers, and it can contain several
*threads*, each of which has its own registers and its own stack:

```
┌─────────────────────────────────────────────────┐
│ Process                                         │
│   CODE      DATA      FILE POINTERS             │  ← shared
│ ┌──────────┬──────────┬──────────┐              │
│ │ thread 1 │ thread 2 │ thread 3 │              │
│ │ registers│ registers│ registers│              │  ← private
│ │  stack   │  stack   │  stack   │              │
│ └──────────┴──────────┴──────────┘              │
└─────────────────────────────────────────────────┘
```

This diagram is the key to the whole software half of the lecture. The
threads of one process share the code, the data and the open files, but each
has its own registers and stack. Sharing is why threads are cheap, since
there is no copying and no message passing, and sharing is also why threads
are dangerous, since two threads writing the same variable can interleave in
ways that neither programmer intended. The private stack is what allows each
thread to be in the middle of its own function calls; recall the call stack
of session 6, of which each thread has its own.

---

## 5. Concurrency vs parallelism

In single-thread execution, tasks run one after another on one CPU. In
parallel execution, tasks run on different CPUs at the same time. In
concurrent execution, tasks are interleaved on one CPU:

```
single-thread   CPU 1  │ task 1 │ task 2 │ task 3 │

parallel        CPU 1  │ task 1 │
                CPU 2  │ task 2 │
                CPU 3  │ task 3 │

concurrent      task 1  ██    ██        ██
                task 2      ██    ██
                task 3            ██        ██
```

*Concurrency* means executing multiple tasks at the same time but not
necessarily simultaneously: an application is making progress on more than
one task at the same time, it does not completely finish one task before it
begins the next, the tasks are on the same CPU, and their order is not
completely fixed. *Parallelism* means that an application splits its tasks
into smaller subtasks that can be processed in parallel: the tasks are on
different CPUs and are, at certain times, executed simultaneously. The
one-line version is that concurrency is about structure and parallelism is
about execution. A concurrent program is written as several independent
activities, and whether they actually run at the same instant depends on how
many cores you have; concurrency is a property of your code and parallelism
a property of the machine running it.

Concurrency has costs and advantages. Switching between tasks takes
computing time, for example to load data or instructions into memory, and
this switching is handled by the operating system, which uses compute time
to do it. So on a single core, concurrency makes the total work larger, not
smaller. Why do it at all? Because concurrency can save time when using
resources that are slower than the CPU. The CPU can change to another
process when a slow task starts, for example an access to files on the hard
drive, to information over a network, to data from a peripheral device, or
to user input. The numbers make the case: a CPU cycle is under a
nanosecond, a disk seek takes milliseconds, and a network round trip tens of
milliseconds, so while one task waits for the disk, the CPU could execute
millions of instructions for another task. That is what concurrency buys,
not more work per second but no idle waiting, and the practical rule is
concurrency for I/O-bound work and parallelism for CPU-bound work.

---

## 6. Flynn's taxonomy

Flynn's taxonomy classifies multi-processor computer architectures along
two dimensions, the instruction stream and the data stream, each of which
can be single or multiple:

| | **Single data** | **Multiple data** |
|---|---|---|
| **Single instruction** | **SISD**: one CPU | **SIMD**: graphics cards (GPU) |
| **Multiple instruction** | **MISD**: fault-tolerant systems (e.g. airplanes) | **MIMD**: supercomputers, multiple CPUs per chip |

SISD is the classical von Neumann machine, with one instruction
applied to one datum at a time. SIMD applies the same operation to many data
at once, so that "add 1 to every element of this vector" is one instruction
over a million data items; this is exactly what graphics and matrix
arithmetic need, hence GPUs. MISD is the odd one: several different
computations on the same data, so that their results can be compared. Flight
control computers run independent implementations on the same sensor
readings and vote, and the purpose is not speed but fault tolerance. MIMD is
everything general-purpose and parallel: your multi-core laptop, a cluster,
a supercomputer.

---

## 7. Instruction-level parallelism

CPU architectures divide their instructions into *microinstructions*, each
of which takes a hardware clock cycle. The example of the lecture is an
architecture with five microinstructions: IF, instruction fetch, gets the
next instruction code; ID, instruction decode, converts the code into
hardware activation flags; EX, execute, performs the calculation based on
the register contents; MEM, memory access, writes results to main memory if
necessary; and WB, register write back, changes the registers, for example
the pointer to the next instruction. Not all instructions need all five
cycles, and the details depend on the architecture, but different parts of
the hardware are used for each microinstruction, and that is the whole idea.
If IF uses the fetch unit and EX uses the arithmetic logic unit, then while
instruction 1 is in EX the fetch unit is idle, and it could be fetching
instruction 2. Without parallelism, the instructions run one after the
other and a canonical processor takes five clock cycles per instruction:

```
i │ IF ID EX MEM WB │
  │                 │ IF ID EX MEM WB │
  │                                   │ IF ID EX MEM WB │
  └───────────────── time ────────────────────────────▶
```

With a *pipeline*, each stage starts a new instruction as soon as it is
free, so a pipelined processor can simultaneously execute five instructions
and can take as little as one clock cycle per instruction:

```
i │ IF ID EX MEM WB
  │    IF ID EX MEM WB
  │       IF ID EX MEM WB
  │          IF ID EX  MEM WB
  │             IF ID  EX  MEM WB
  └────── time ──────────────────▶
```

The speedup is not that any single instruction finishes faster, because each
one still takes five cycles from start to finish. What changes is the
throughput: after the pipeline fills, one instruction completes every cycle.
This is exactly the distinction between latency and throughput, and it recurs
at every scale of parallel computing.

The pipeline has two caveats. The first is *speculative execution*: future
instructions start before the current one finishes, but control flow usually
makes the CPU throw away future instructions, for example when an `if`
statement changes the next instruction and the pipeline has to be cleaned.
The pipeline has to guess which way a branch will go in order to keep
filling, and if it guesses wrong, the partially executed instructions are
discarded and the pipeline restarts, a pipeline flush that costs several
cycles; this is why, at the very lowest level, unpredictable branches are
expensive. The second caveat is security: speculative execution leaves
traces that can be read by other programs, and the Spectre and Meltdown
vulnerabilities make it possible to read private data of other programs
left in the processor cache by speculatively executed instructions. These
are worth knowing about as a matter of principle, because they are bugs not
in any program but in the optimization strategy of the hardware, present in
nearly every processor made between 1995 and 2018, and the fixes cost real
performance. An abstraction, that each program is isolated, leaked because
of how it was implemented underneath.

---

## 8. Multi-core, GPUs and clusters

Several cores per processor allow the execution of multiple threads in
parallel, and most likely all the laptops and mobile phones of the students
in this course are multi-core and many are even multi-processor. The
distinction is that a multi-core processor has several complete processing
units on one chip, sharing a cache and a memory bus, while a multi-processor
system has several chips, each with its own; from software, the difference
mostly shows up in memory speed.

A *graphics processing unit* (GPU) is specialized to calculate what is
displayed on a screen. GPUs are designed for multiplications of matrices,
which is how 3D models are displayed, they perform the same calculation over
a large set of data, a vector, which makes them SIMD machines in Flynn's
taxonomy, and they have large memories with very high bandwidth. They cannot
do every operation efficiently, because they are designed for matrix
operations, but those operations have applications beyond graphics: mining
cryptocurrencies means solving modular algebra equations for many possible
solutions, and training machine learning models means applying matrix
operations to fit many parameters on large datasets. The last point closes
the loop with session 10. Training a neural network is, numerically, a long
sequence of matrix multiplications, precisely the operation GPUs were built
for, and the deep learning revolution of the 2010s happened when people
noticed that hardware built for video games was the right hardware for
neural networks.

A *computing cluster* links many computers with very high bandwidth
connections. The example of the lecture is the Scientific Compute Cluster
(SCC) of the University of Konstanz, with Infiniband connections of 56
Gbit/s and 0.7 µs latency, Intel Broadwell HPC compute nodes with 28 cores
per node and up to 1024 GB of RAM, and a large RAID (redundant array of
independent disks) storage. The Department of Politics and Public
Administration is an SCC shareholder with 4 compute nodes, that is, 112
cores, as part of the larger SCC infrastructure, and if they are available
it can use the compute nodes of other shareholders, since resources might be
idle when other departments do not need them. Note what is being bought with
Infiniband: not so much bandwidth as latency. A latency of 0.7 µs is roughly
a hundred times better than ordinary Ethernet, and for distributed
algorithms that exchange many small messages, latency is what determines
whether the parallelization pays off at all, which is the subject of section
10.

---

## 9. Software parallelization and MapReduce

Software parallelization comes in two settings. The first is multiple
threads or processes in the same computer, for example running mergesort
with its recursive calls in separate parts of memory. The issue here is
coordinating memory access, and the solutions are inter-process
communication (IPC) and message passing interfaces (MPI), which we do not
cover. Mergesort is the natural example because of session 7: the two
recursive calls operate on disjoint halves of the array, so they cannot
interfere and can run on different cores, and only the merge step needs
coordination. Divide-and-conquer algorithms are parallel almost by
construction. The second setting is multiple machines connected through a
network, that is, *distributed computing*, for example splitting parts of
mergesort to different machines and merging the results in more central
machines. The issue here is that network communication is the bottleneck of
the computation, and the solution is a distributed paradigm such as
*MapReduce*.

MapReduce has three phases. In the Map phase, each machine computes a part
of the solution on its partial dataset; in the communication phase, the Map
results are sent to the reducer over the network; and in the Reduce phase,
the Map results are combined into the final solution. Computations can take
several Map-Reduce iterations or hierarchies, and Apache Hadoop and Spark
are some of the most popular software solutions for MapReduce.

```
   S₁      S₂      …      S_M        ← data, already on M machines
    │       │              │
  Map     Map     …      Map         ← same function, run locally
    │       │              │
    └───────┴──────┬───────┘         ← communication
                Reduce               ← combine
                   │
              final result
```

The governing principle is to bring the code to the data. Moving a terabyte
across a network is slow, while moving the twenty lines of code that process
it is free, so the computation goes to where the data already sits and only
the small intermediate results travel. For this to work, the Map function
must be computable on a partition of the data with no reference to the rest
of it, and whether your statistic has that property is the question of the
next section.

---

## 10. Distributed statistical inference

The setting of the lecture's example is billions of data points distributed
over several thousand data servers. The objectives are to save time by using
a distributed architecture that brings the code to the data, to keep in mind
that communication time matters, in contrast to plain parallel processing,
and to obtain an inference with desirable statistical properties that
minimizes the additional error. That third objective is what makes this
different from ordinary parallelization. When you split a sorting problem
across machines you get the same answer, faster; when you split an
estimation problem across machines, you may get a different answer, and
possibly a worse one. Speed is not the only currency. The total time of a
divide-and-conquer inference is $T_{map} + T_{comm} + T_{reduce}$, the local
computation, the communication and the combination, and the estimate
$\hat\theta$ it produces should ideally be accurate, with a small mean
squared error $MSE(\hat\theta) = E[(\hat\theta - \theta)^2]$, unbiased, with
$E[\hat\theta] = \theta$, and of minimum variance, with $Var(\hat\theta) =
E[(\hat\theta - E[\hat\theta])^2]$ as small as possible.

When things are easy, the recipe is averaging: in the Map phase each machine
computes the same estimator in its local sample, and in the Reduce phase the
Map results are averaged into the final estimator. For the mean this works
exactly. Each machine $j$ computes the mean $\hat\mu_j$ of its sample $S_j$,
and the reducer computes

$$\hat\mu = \frac{1}{M}\sum_{j=1}^{M} \hat\mu_j.$$

Plotting the distributed estimate against the whole-sample estimate gives a
perfect straight line: the two agree exactly when the samples are of equal
size, because the mean is a linear function of the data and an average of
averages is the average. Now apply the same recipe to Pearson's correlation,
computing it in each local sample and averaging the results. The scatter
plot of the distributed estimate against the whole-sample estimate is a
cloud, not a line, because the average of the correlations is not the
correlation of the pooled data: Pearson's $\rho$ is a nonlinear function of
sums, and averaging nonlinear functions computed on subsets does not recover
the function of the whole. This is a general warning, and it is the reason
why this section is in a social science course: you cannot distribute an
estimator just because you can distribute a mean. Medians, quantiles,
regression coefficients, variances and correlations all need thought.

The smarter calculation changes what the Map phase returns. Pearson's
correlation can be written entirely in terms of sums,

$$\rho_{xy} = \frac{n\sum_i x_i y_i - \sum_i x_i \sum_i y_i}
{\sqrt{n\sum_i x_i^2 - (\sum_i x_i)^2}\ \sqrt{n\sum_i y_i^2 - (\sum_i y_i)^2}},$$

so each Map returns its sample size $n_j$ and five partial sums, $\sum x$,
$\sum y$, $\sum x^2$, $\sum y^2$ and $\sum xy$ over its own sample, instead
of a correlation. Sums are additive over partitions, so the reducer simply
adds them across machines, $\sum_i x_i = \sum_j \sum_{i \in S_j} x_i$ and
likewise for the rest, and then evaluates the formula once. The result is
exactly the whole-sample correlation, and the scatter plot becomes a perfect
line again. The lesson of the lecture is the trade-off: added communication
time to avoid added variance in the estimate. Each machine now sends six
numbers instead of one, so $T_{comm}$ grows, but the estimate is exact
instead of noisy, and designing a distributed algorithm means choosing a
point on that trade-off deliberately. The general recipe is to find a set of
quantities that are additive over partitions and that determine the
statistic you want. These are called *sufficient statistics*, and if your
estimator has small ones, it distributes perfectly.

---

## 11. Amdahl's law

Can you actually achieve an optimal speedup? Gene Amdahl showed in 1967 that
there is an upper limit. The intuition is that there is always a part of the
code that cannot be parallelized, and that with increasing parallelization
this part dominates the overall runtime of the program. The maximal speedup
depends on two variables, the fraction $P$ of the computation that can be
parallelized, for example 80%, and the number $N$ of processors or threads
that can be used in parallel, and Amdahl's law gives the speedup $S$ of the
execution of the whole task as

$$S = \frac{1}{(1 - P) + \dfrac{P}{N}}.$$

Read the denominator: $(1-P)$ is the serial part, which $N$ never touches,
and $P/N$ is the parallel part shared among the $N$ processors. For $P =
0.8$ the speedup grows as follows:

| $N$ | $S$ |
|---|---|
| 1 | 1.00 |
| 2 | 1.67 |
| 4 | 2.50 |
| 8 | 3.33 |
| 16 | 4.00 |
| 100 | 4.81 |
| $\infty$ | **5.00** |

Check $N = 2$: $S = 1/(0.2 + 0.4) = 1.67$. Check the limit: as $N \to
\infty$, $P/N \to 0$ and $S \to 1/(1-P) = 1/0.2 = 5$. Two things follow, and
both are counterintuitive. The ceiling is $1/(1-P)$ no matter how many
processors you buy, so with 20% of serial code you can never go faster than
5×, even with a million cores. And diminishing returns come fast: going
from 1 to 4 processors buys 2.5×, while going from 4 to 100 buys less than
2× more, so the eighth processor contributes less than the second. The
practical consequence is to measure $P$ before parallelizing. If a profiler
says that half of your runtime is in a sequential file-parsing step, your
ceiling is 2× and the effort is probably better spent on the parser. The
optimistic counterpoint, worth knowing though not examined here, is
Gustafson's law: in practice, people who buy more processors use them to
solve bigger problems rather than the same problem faster, and the serial
fraction of a bigger problem is often smaller.

---

## 12. Summary

Parallelization is motivated by the limits of Moore's law; its paradigms are
multi-core, multi-processor and multi-thread execution, and it should not be
confused with concurrency. Hardware parallelization happens at the
instruction level, in multi-core processors, in GPUs and in clusters.
Software parallelization includes distributed computing with MapReduce. And
the limit of parallelization is given by Amdahl's law.

---

## 13. Check yourself

**1.** Your program spends 90% of its time in a parallelizable loop. What is the best possible speedup, and how many cores get you halfway there?

<details><summary>Answer</summary>

The ceiling is $1/(1 - 0.9) = 10\times$. Halfway, that is 5×, needs $5 =
1/(0.1 + 0.9/N)$, so $0.1 + 0.9/N = 0.2$, giving $N = 9$. Nine cores get you
to 5×, and the remaining 5× needs infinitely many. This is the shape of every
Amdahl curve.

</details>

**2.** A web scraper that fetches 1000 pages is slow. Threads or processes?

<details><summary>Answer</summary>

Threads, or asynchronous I/O. The work is I/O-bound: almost all the time is
spent waiting for network responses, and while one thread waits, another
can send its request. You do not need multiple cores for this, since
concurrency on one core is enough. Multiple processes would work too but
cost more memory for no benefit.

</details>

**3.** Why can mergesort's two recursive calls run in parallel, but not the two halves of an in-place bubble sort pass?

<details><summary>Answer</summary>

The calls of mergesort operate on disjoint subarrays, so neither reads or
writes what the other touches, and any interleaving gives the same result. A
bubble sort pass compares and swaps adjacent elements the whole way along,
so the regions that each half touches overlap at the boundary, and the passes
are sequentially dependent besides. Disjointness of memory access is the
condition for safe parallelism.

</details>

**4.** You distribute a median calculation by computing the median on each machine and averaging. Is that correct?

<details><summary>Answer</summary>

No, for the same reason as Pearson's correlation. The median is not linear,
and the average of the medians is not the median of the pooled data:
consider two machines holding [1, 2, 3] and [100, 200, 300], with medians 2
and 200, average 101, and true median 51.5. Unlike the correlation, the
median has no small set of additive sufficient statistics, so its exact
distributed computation needs a genuinely different algorithm, with several
communication rounds, or an approximation with a stated error bound.

</details>

**5.** Why does a pipelined CPU not make a single instruction finish any faster?

<details><summary>Answer</summary>

Because the instruction still passes through all five stages, one cycle
each, so its latency is unchanged at 5 cycles. What the pipeline improves is
the throughput: once it is full, one instruction completes per cycle because
five are in flight simultaneously. Confusing the two is the most common
error in reasoning about parallel systems.

</details>

---

## 14. References

- **DeNero, J.** *Composing Programs*, section 4.8, "Parallel Computing".
  <https://www.composingprograms.com/pages/48-parallel-computing.html>. The
  reading for this session.
- **Vo, H. & Silva, C. (2017).** "Programming with Big Data", chapter 5 of
  Foster, I., Ghani, R., Jarmin, R. S., Kreuter, F. & Lane, J. (eds.), *Big
  Data and Social Science*. Chapman & Hall/CRC. The second reading for this
  session; MapReduce and Spark in practice.
- **Moore, G. E. (1965).** "Cramming more components onto integrated
  circuits". *Electronics* 38(8). The original observation of section 1.
- **Our World in Data, *Technological Change*:**
  <https://ourworldindata.org/technological-change#advances-in-computational-technology>.
  Transistor-count data behind the Moore's law figure.
- **Amdahl, G. M. (1967).** "Validity of the single processor approach to
  achieving large scale computing capabilities". *AFIPS Conference
  Proceedings* 30, 483–485. Section 11.
- **Gustafson, J. L. (1988).** "Reevaluating Amdahl's Law". *Communications
  of the ACM* 31(5), 532–533.
- **Flynn, M. J. (1972).** "Some Computer Organizations and Their
  Effectiveness". *IEEE Transactions on Computers* C-21(9), 948–960. Section
  6.
- **Hennessy, J. L. & Patterson, D. A. (2019).** *Computer Architecture: A
  Quantitative Approach*, 6th ed. Morgan Kaufmann. Pipelining and
  instruction-level parallelism (section 7).
- **Kocher, P. et al. (2019).** "Spectre Attacks: Exploiting Speculative
  Execution". *IEEE Symposium on Security and Privacy*; **Lipp, M. et al.
  (2018).** "Meltdown: Reading Kernel Memory from User Space". *USENIX
  Security Symposium*. <https://meltdownattack.com/>
- **Dean, J. & Ghemawat, S. (2008).** "MapReduce: Simplified Data Processing
  on Large Clusters". *Communications of the ACM* 51(1), 107–113. Section 9.
- **Zaharia, M. et al. (2016).** "Apache Spark: A Unified Engine for Big Data
  Processing". *Communications of the ACM* 59(11), 56–65.
- **Garcia, D.** *Scalable Algorithms for Statistical Inference from Big
  Data*, lecture slides. Source of the divide-and-conquer figures and the
  correlation example of section 10.
- **Jordan, M. I., Lee, J. D. & Yang, Y. (2019).** "Communication-Efficient
  Distributed Statistical Inference". *Journal of the American Statistical
  Association* 114(526), 668–681. The communication/accuracy trade-off of
  section 10, in depth.
- **Lawrence Livermore National Laboratory, *Introduction to Parallel
  Computing*:**
  <https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial>.
  Source of the "reasons to parallelize" framing of section 3.
- **jq manual:** <https://jqlang.org/>. For the exercise session.
