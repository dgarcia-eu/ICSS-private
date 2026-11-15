# Session 12: Parallel Programming

<style>
figure, .figure, .float { margin: 1.4em 0 1.8em 0; }
figure img, .float img { display: block; max-width: 100%; }
figcaption, .figcaption, .figure p.caption { margin-top: 0.3em; font-size: 0.88em; color: #555; }
details { margin: -0.5em 0 2.2em 0; }
</style>

*Introduction to Computing for the Social Sciences · lecture transcript*

**Reading for this session:** section 4.8, "Parallel Computing", of DeNero,
*Composing Programs*, and chapter 5, "Programming with Big Data", of Foster
et al. (eds.), *Big Data and Social Science* (2017). Before the next
exercise session, install `jq` from <https://jqlang.org/>. References at
the end.

---

## Contents

1. [Parallelization](#parallelization)
2. [Hardware parallelization](#hardware)
3. [Software parallelization](#software)
4. [Limitations](#limitations)

---

<!-- MOTIVATION-SECTION:BEGIN -->
## Motivating examples

<!-- MOTIVATION:M12-A:BEGIN -->
### A · Your laptop stopped getting faster in 2005

Between roughly 1975 and 2005 there was a reliable way to make slow code
fast, which was to wait. Processor clock speeds doubled every couple of years
alongside transistor counts, so the same unmodified program ran twice as fast
on the hardware of two years later without anybody doing anything. This
stopped in the mid-2000s, when clock speeds reached about 3 GHz. They have
essentially stayed there for twenty years, because power consumption and heat
rise faster than the clock frequency and the heat cannot be removed from the
chip. Moore's law itself did not stop, since transistor counts kept roughly
doubling. However, the additional transistors were used to build more cores
instead of faster ones. As a consequence, a sequential program does not run
faster on a 128-core machine than on a 4-core one, because it uses one core
while the other 127 are idle. To use them, the program has to be written for
several cores, so getting more speed has become a software problem. Herb
Sutter described this change with the phrase *"the free lunch is over"*,
because now you have to write your program differently if you want it to run
faster on newer hardware.

There are two limits to keep in mind before we start. First, parallelism does
not change complexity. An $O(n^2)$ algorithm on 100 cores is still $O(n^2)$,
because dividing the work by 100 only changes a constant factor. Therefore,
what we learned in the Time Complexity session still holds, i.e. if your
program is too slow, check whether you have an algorithm problem before you
look for more hardware, because more cores cannot compensate for the wrong
growth rate. Second, the speedup is bounded and the bound is lower than you
would guess. The fraction of your program that cannot be parallelized sets a
maximum speedup for the whole program regardless of how many processors you
buy. That fraction is usually larger than people expect, because reading the
input, writing the output and the sequential combination step all count
towards it.

In this session you will learn about Moore's law, its physical limits and why
parallelization is a workaround. We will learn the difference between
multiprocessor, multicore and multithreading, and the distinction between
concurrency, which is a way of structuring a program, and parallelism, which
is a way of executing one. We will also see where parallelism happens in your
machine, namely in instruction pipelines, cores, GPUs and clusters, and we
will learn Amdahl's law, which quantifies the maximum speedup. Your laptop
has had multiple cores for your entire adult life and almost every analysis
script you have written has used only one of them. After this session you
will be able to judge when that is worth changing.

<!-- MOTIVATION:M12-A:END -->
<!-- MOTIVATION:M12-B:BEGIN -->
### B · Sixteen cores, and 2.5× faster

An agent-based model takes 40 hours on your laptop. The department has a
16-core node on the cluster, so you expect the model to run in two and a half
hours there. Instead, it takes 16 hours. You then request a 64-core node and
the model takes 15 hours. Nothing is broken or misconfigured, and these
numbers are what theory predicts. Gene Amdahl wrote down the following
formula in 1967:

$$S = \frac{1}{(1 - P) + \dfrac{P}{N}},$$

where $P$ is the fraction of the computation that can be parallelized and
$N$ is the number of processors. In the denominator, $(1-P)$ is the serial
part, which does not get faster with more processors, while $P/N$ is the
parallel part divided among the $N$ processors. We can fit the formula to the
observation. A speedup of 2.5 on 16 cores means

$$2.5 = \frac{1}{(1-P) + P/16} \;\Longrightarrow\; P \approx 0.64,$$

so 64% of the runtime can be parallelized and 36% cannot. The serial part
includes, for example, reading the input files, seeding the model, collecting
results, writing output and the parts of the simulation that are inherently
sequential. Now we can predict the 64-core run,

$$S = \frac{1}{0.36 + 0.64/64} = \frac{1}{0.37} = 2.70 \;\Longrightarrow\;
40 / 2.70 \approx 15\ \text{hours},$$

which is what happened. The maximum speedup, as $N \to \infty$, is

$$S_{\max} = \frac{1}{1 - P} = \frac{1}{0.36} = 2.8\times.$$

Therefore, forty hours will never become less than fourteen on any machine
until the 36% is reduced. Two consequences follow from this. First,
diminishing returns arrive very early. Going from 1 to 4 cores gives most of
the possible speedup while the 64th core contributes almost nothing. The
efficiency, i.e. the speedup per core, falls from 100% to 4%, so on a shared
cluster you are occupying 64 cores to do the work of three and other people
cannot use them. Second, what you can improve is the serial fraction rather
than the number of cores. Reducing $1-P$ from 36% to 10% would raise the
maximum speedup from 2.8× to 10×. To do this, you need to profile the program
to find where the serial time is spent, which is often in a mundane step like
parsing input files and not in the model itself.

In this session you will learn Amdahl's law with a worked table and its
limit. We will also learn what can and cannot be parallelized, which usually
depends on whether the tasks share data that they modify. For example,
divide-and-conquer algorithms like mergesort are easy to parallelize because
their subproblems work on disjoint data. When you use a cluster for your own
research, measure $P$ before requesting nodes. One profiling run tells you
the maximum speedup, and it is frequently low enough that fixing the serial
part is the better choice.

<!-- MOTIVATION:M12-B:END -->
<!-- MOTIVATION:M12-C:BEGIN -->
### C · Three billion posts, one million rows of memory

Imagine that you have three billion posts and you want the correlation
between likes and reshares. Your machine holds a million rows at a time, so
the data must be processed in about 3,000 chunks. The natural thing to do is
to compute the correlation within each chunk and to average the 3,000
results. This produces a number, but that number is not the correlation of
the whole data. The reason is that Pearson's $\rho$ is a nonlinear function
of the data, and averaging a nonlinear function computed on subsets does not
recover the function of the whole. If you plot the chunk-average estimate
against the true whole-sample value, the points form a cloud instead of a
line. If you do the same with the mean, you get a perfect line, because the
mean is linear and an average of averages with equal chunk sizes is the
average of the whole. Therefore, the question is which quantities can still
be computed exactly after the data is split.

For the correlation, the answer is that $\rho$ can be written entirely in
terms of sums,

$$\rho_{xy} = \frac{n\sum x_i y_i - \sum x_i \sum y_i}
{\sqrt{n\sum x_i^2 - (\sum x_i)^2}\ \sqrt{n\sum y_i^2 - (\sum y_i)^2}},$$

and sums are additive across a partition. Each chunk returns six numbers,
namely $n$, $\sum x$, $\sum y$, $\sum x^2$, $\sum y^2$ and $\sum xy$, and the
coordinator adds them and evaluates the formula once. The result is exactly
the whole-data correlation and not an approximation, while memory never
exceeds one chunk plus six accumulators. Sending six numbers per chunk
instead of a million rows is the main idea behind distributed computing on
data at this scale, i.e. we bring the code to the data and move only the
summaries. In general, we look for quantities that are additive over
partitions and sufficient to determine the statistic we want. Where they
exist, the computation can be distributed exactly. Where they do not exist,
for example for the median, the quantiles or the number of distinct values,
you need several communication rounds or an approximation with a stated
error bound.

In this session you will learn about MapReduce, which has a Map phase that
computes partial results locally, a communication phase and a Reduce phase
that combines them. We will learn about distributed statistical inference,
with the mean as the easy case and the correlation as a case in which we
trade extra communication time against extra variance in the estimate. We
will also see Amdahl's law, because the Reduce step is serial and therefore
limits the speedup. In your own work, keep in mind that you cannot distribute
an estimator just because you can distribute a mean. Medians, quantiles,
variances, regression coefficients and correlations each need to be thought
about separately, because the naive approach of averaging gives a wrong
result for most of them.

<!-- MOTIVATION:M12-C:END -->

---

<!-- MOTIVATION-SECTION:END -->
## 1. Moore's law and why it is running out {#parallelization}
*Moore's law* predicts that the number of transistors per microchip doubles
every two years, which is an exponential growth in computing power. The
increase is still exponential but the rate is slower, so doubling now takes
more than two years. There is also a physical limit, because a transistor
cannot be smaller than an atom. This limit is expected to be reached in this
decade unless radically different models of computation become feasible.
Parallelization, i.e. using several processors, is a workaround to this
limit.

For forty years, the way to make a slow program fast was to wait, because the
same code ran twice as fast on the hardware of two years later. Since roughly
2005, the transistor count still rises but the clock speed does not, and the
extra transistors are used for more cores rather than for faster ones. To
benefit from them, programs have to be written to use several cores, which
makes speed a software problem that you have to solve yourself. Remember from
the Time Complexity session that parallelization changes the constant factor
and not the complexity class, so an $O(n^2)$ algorithm on 100 cores is still
$O(n^2)$. If your program is too slow, first check whether you have an
algorithm problem, because more hardware does not fix that. To learn more
about Moore's law, Our World in Data keeps the transistor counts up to date
at
<https://ourworldindata.org/technological-change#advances-in-computational-technology>.

---

## 2. The brain as an inspiration

We can compare the brain with two machines:

| | Operations/sec | Power (Watts) | Cores | sec/cycle |
|---|---|---|---|---|
| **Brain** | $10^{13}$ | 15–20 | ? | $10^{-3}$ |
| **Intel Terascale** | $10^{12}$ | 85 | 80 | $10^{-9}$ |
| **Supercomputer Blue Gene** | $3.6 \times 10^{14}$ | $1.2 \times 10^{6}$ | 130,000 | $10^{-9}$ |

The table is most informative when we compare the values of each column.
Brains work slowly but are massively parallel. A neuron fires on a
millisecond timescale, which is a million times slower than a transistor
switches. Nevertheless, the brain reaches $10^{13}$ operations per second
because very many neurons are active at the same time. It does so on about 20
watts, which is the power of a light bulb, while Blue Gene needs 1.2
megawatts for 36 times the throughput. Per operation and watt, the brain is
therefore more than three orders of magnitude more efficient. The number of
cores of a brain is a question mark because the analogy does not hold there,
since neurons are not general-purpose processors that execute instructions.
We can see the parallelism in fMRI images, which show various regions of the
brain active at the same time during a single task. IBM Blue Gene is an
example of a parallel computer built in a different way, i.e. from many
conventional processors connected to each other.

---

## 3. Reasons to parallelize

There are three reasons to parallelize:

- **Saving time or money.** We can use more compute resources for a problem
  to shorten the compute time. We can also use cheap commodity components to
  build parallel processors, because a hundred ordinary machines cost far
  less than one machine that is a hundred times as fast, if such a machine
  exists at all. This is the idea behind Beowulf clusters and, later, cloud
  computing.
- **Solving larger and more complex problems.** Some problems are so large
  that they are infeasible to solve with serial computation, especially with
  limited memory. For example, web search engines and databases process
  millions of transactions every second. Sometimes we parallelize because the
  data does not fit in the memory of one machine and not because of speed.
- **Providing concurrency.** A single compute resource can only do one thing
  at a time, while multiple compute resources can do many things
  simultaneously.

---

## 4. Types of parallelization

There are different ways to multiply processing:

- A ***multiprocessor*** system has more than one CPU.
- A ***multicore*** processor is one CPU with several cores.
- ***Multithreading*** lets a single core execute more than one task
  concurrently.

These three are not alternatives. For example, a modern laptop is all three
at once. The unit of software that runs on them is the process. A *process*
owns its code, its data and its file pointers. It can contain several
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

As the diagram shows, the threads of one process share the code, the data and
the open files, but each has its own registers and stack. Sharing makes
threads cheap, because nothing has to be copied and no messages have to be
passed between them. However, sharing also makes threads risky, because two
threads that write the same variable can interleave in ways that the
programmer did not intend. The private stack allows each thread to be in the
middle of its own function calls, i.e. each thread has its own call stack
like the one we saw in the Recursion session.

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
necessarily simultaneously. An application makes progress on more than one
task at the same time, i.e. it does not completely finish one task before it
begins the next. The tasks are on the same CPU and their order is not
completely fixed. *Parallelism* means that an application splits its tasks
into smaller subtasks that can be processed in parallel, so the tasks are on
different CPUs and are executed simultaneously at certain times. In short,
concurrency is about how a program is structured while parallelism is about
how it is executed. A concurrent program is written as several independent
activities, and whether they actually run at the same instant depends on how
many cores you have. Therefore, concurrency is a property of your code and
parallelism is a property of the machine that runs it.

Concurrency has costs and advantages. Switching between tasks takes
computing time, for example to load data or instructions into memory. This
switching is handled by the operating system, which uses compute time to do
it. Therefore, on a single core, concurrency makes the total amount of work
larger. Why should we use it then? Concurrency can save time when a program
uses resources that are slower than the CPU. The CPU can change to another
process when a slow task starts, for example an access to files on the hard
drive, to information over a network, to data from a peripheral device, or
to user input. The difference in speed is large, because a CPU cycle takes
less than a nanosecond while a disk seek takes milliseconds and a network
round trip takes tens of milliseconds. While one task waits for the disk, the
CPU could execute millions of instructions for another task. Concurrency does
not give us more work per second but it avoids idle waiting. As a practical
rule, use concurrency for work that mostly waits for input and output
(I/O-bound work) and parallelism for work that mostly computes (CPU-bound
work). The last part of the practical Python examples shows this difference
with twenty simulated downloads and four computations that run in threads.

---

## 6. Flynn's taxonomy {#hardware}
Flynn's taxonomy classifies multi-processor computer architectures along
two dimensions, namely the instruction stream and the data stream. Each of
them can be single or multiple:

| | **Single data** | **Multiple data** |
|---|---|---|
| **Single instruction** | **SISD**: one CPU | **SIMD**: graphics cards (GPU) |
| **Multiple instruction** | **MISD**: fault-tolerant systems (e.g. airplanes) | **MIMD**: supercomputers, multiple CPUs per chip |

The four combinations are the following:

- **SISD** is the classical von Neumann machine, in which one instruction is
  applied to one datum at a time.
- **SIMD** applies the same operation to many data at once. For example,
  *"add 1 to every element of this vector"* is one instruction over a million
  data items. Graphics and matrix arithmetic need this kind of operation,
  which is why GPUs are SIMD machines.
- **MISD** is the least common type. It runs several different computations
  on the same data so that their results can be compared. For example, flight
  control computers run independent implementations on the same sensor
  readings and vote on the result. The purpose is fault tolerance rather than
  speed.
- **MIMD** covers the general-purpose parallel machines, for example your
  multi-core laptop, a cluster or a supercomputer.

---

## 7. Instruction-level parallelism

CPU architectures divide their instructions into *microinstructions*, each
of which takes a hardware clock cycle. As an example, consider an
architecture with five microinstructions:

1. **IF** (instruction fetch) gets the next instruction code.
2. **ID** (instruction decode) converts the code into hardware activation
   flags.
3. **EX** (execute) performs the calculation based on the register contents.
4. **MEM** (memory access) writes results to main memory if necessary.
5. **WB** (register write back) changes the registers, for example the
   pointer to the next instruction.

Not all instructions need all five cycles and the details depend on the
architecture. What matters for parallelism is that different parts of the
hardware are used for each microinstruction. For example, if IF uses the
fetch unit and EX uses the arithmetic logic unit, then the fetch unit is idle
while instruction 1 is in EX and it could already be fetching instruction 2.
Without parallelism, the instructions run one after the other and a canonical
processor takes five clock cycles per instruction:

```
i │ IF ID EX MEM WB │
  │                 │ IF ID EX MEM WB │
  │                                   │ IF ID EX MEM WB │
  └───────────────── time ────────────────────────────▶
```

With a *pipeline*, each stage starts a new instruction as soon as it is
free. A pipelined processor can therefore execute five instructions
simultaneously and can take as little as one clock cycle per instruction:

```
i │ IF ID EX MEM WB
  │    IF ID EX MEM WB
  │       IF ID EX MEM WB
  │          IF ID EX  MEM WB
  │             IF ID  EX  MEM WB
  └────── time ──────────────────▶
```

The pipeline does not make any single instruction finish faster, because each
one still takes five cycles from start to finish. What changes is the
throughput, because after the pipeline fills, one instruction completes every
cycle. This is the difference between latency, i.e. the time that one task
takes, and throughput, i.e. the number of tasks completed per unit of time.
We find the same difference at every scale of parallel computing.

The pipeline has two caveats:

- ***Speculative execution.*** Future instructions start before the current
  one finishes, but control flow can make the CPU throw them away, for
  example when an `if` statement changes the next instruction and the
  pipeline has to be cleaned. The pipeline has to guess which way a branch
  will go in order to keep filling. If it guesses wrong, the partially
  executed instructions are discarded and the pipeline restarts, which is
  called a pipeline flush and costs several cycles. For this reason,
  unpredictable branches are expensive at the lowest level.
- ***Security risks.*** Speculative execution leaves traces that can be read
  by other programs. The Spectre and Meltdown vulnerabilities make it
  possible to read private data of other programs that speculatively executed
  instructions left in the processor cache. These bugs are not in any program
  but in the optimization strategy of the hardware. They were present in
  nearly every processor made between 1995 and 2018 and the fixes reduce
  performance. In this case, the isolation between programs failed because of
  how the hardware implements the execution of instructions.

---

## 8. Multi-core, GPUs and clusters

Several cores per processor allow the execution of multiple threads in
parallel. Most likely all your laptops and mobile phones are multi-core and
many are even multi-processor. A multi-core processor has several complete
processing units on one chip that share a cache and a memory bus, while a
multi-processor system has several chips, each with its own cache and memory
bus. For software, the difference is mostly noticeable in memory speed.

A *graphics processing unit* (GPU) is specialized to calculate what is
displayed on a screen. GPUs are designed for multiplications of matrices,
which is how 3D models are displayed. They perform the same calculation over
a large set of data, i.e. a vector, which makes them SIMD machines in Flynn's
taxonomy. They also have large memories with very high bandwidth. GPUs cannot
do every operation efficiently because they are designed for matrix
operations, but those operations have applications beyond graphics. For
example, mining cryptocurrencies means solving modular algebra equations for
many possible solutions, and training machine learning models means applying
matrix operations to fit many parameters on large datasets. Training a neural
network like the ones of the Machine Learning session is numerically a long
sequence of matrix multiplications, which is the operation that GPUs were
built for. The deep learning advances of the 2010s started when researchers
noticed that hardware built for video games was also the right hardware for
neural networks.

A *computing cluster* links many computers with very high bandwidth
connections. An example is the Scientific Compute Cluster (SCC) of the
University of Konstanz, which has Infiniband connections of 56 Gbit/s and 0.7
µs latency, Intel Broadwell HPC compute nodes with 28 cores per node and up
to 1,024 GB of RAM, and a large RAID (redundant array of independent disks)
storage. The Department of Politics and Public Administration is an SCC
shareholder with 4 compute nodes, i.e. 112 cores, as part of the larger SCC
infrastructure. It can also use the compute nodes of other shareholders if
they are available, since resources might be idle when other departments do
not need them. The main benefit of Infiniband is its low latency more than
its bandwidth. A latency of 0.7 µs is roughly a hundred times better than
ordinary Ethernet. For distributed algorithms that exchange many small
messages, latency determines whether the parallelization is worth it, as we
will see below with distributed statistical inference.

---

## 9. Software parallelization and MapReduce {#software}
Software parallelization can happen in two settings:

- **Multiple threads or processes in the same computer**, for example running
  mergesort with its recursive calls in separate parts of memory. The issue
  here is coordinating memory access, and the solutions are inter-process
  communication (IPC) and message passing interfaces (MPI), which we do not
  cover. Mergesort is a good example because, as we learned in the Sorting
  Algorithms session, its two recursive calls operate on disjoint halves of
  the array. They cannot interfere with each other and can run on different
  cores, so only the merge step needs coordination. Divide-and-conquer
  algorithms are often easy to parallelize for this reason.
- **Multiple machines connected through a network**, which is called
  *distributed computing*. An example is splitting parts of mergesort to
  different machines and merging the results in more central machines. The
  issue here is that network communication is the bottleneck of the
  computation, and the solution is a distributed paradigm such as
  *MapReduce*.

MapReduce has three phases:

1. In the **Map phase**, each machine computes a part of the solution on its
   partial dataset.
2. In the **communication phase**, the Map results are sent to the reducer
   over the network.
3. In the **Reduce phase**, the Map results are combined into the final
   solution.

Computations can take several Map-Reduce iterations or hierarchies. Apache
Hadoop and Spark are some of the most popular software solutions for
MapReduce.

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

The principle of MapReduce is to bring the code to the data. Moving a
terabyte across a network is slow while moving the twenty lines of code that
process it takes almost no time. Therefore, the computation happens where the
data already is and only the small intermediate results are sent over the
network. For this to work, the Map function must be computable on a partition
of the data without using the rest of it. Next, we will see which statistics
have this property.

---

## 10. Distributed statistical inference

As an example, consider billions of data points distributed over several
thousand data servers. We have three objectives:

- **Saving time** by using a distributed architecture that brings the code to
  the data.
- **Keeping communication time low**, because it matters here in contrast to
  plain parallel processing.
- **Obtaining an inference with desirable statistical properties**, i.e. one
  that minimizes the additional error.

The third objective makes this problem different from ordinary
parallelization. When you split a sorting problem across machines, you get
the same answer faster. However, when you split an estimation problem across
machines, you may get a different answer and possibly a worse one, so speed
is not the only criterion. The total time of a divide-and-conquer inference
is $T_{map} + T_{comm} + T_{reduce}$, i.e. the time of the local computation,
the communication and the combination. The estimate $\hat\theta$ that it
produces should ideally have three properties:

- **Accurate**, with a small mean squared error
  $MSE(\hat\theta) = E[(\hat\theta - \theta)^2]$.
- **Unbiased**, with $E[\hat\theta] = \theta$.
- **Minimum variance**, with
  $Var(\hat\theta) = E[(\hat\theta - E[\hat\theta])^2]$ as small as possible.

When things are easy, we can simply average. In the Map phase each machine
computes the same estimator in its local sample, and in the Reduce phase the
Map results are averaged into the final estimator. For the mean this works
exactly. Each machine $j$ computes the mean $\hat\mu_j$ of its sample $S_j$,
and the reducer computes

$$\hat\mu = \frac{1}{M}\sum_{j=1}^{M} \hat\mu_j.$$

If we plot the distributed estimate against the whole-sample estimate, we get
a perfect straight line. The two agree exactly when the samples are of equal
size, because the mean is a linear function of the data and an average of
averages is then the average of the whole. Now we apply the same approach to
Pearson's correlation, i.e. we compute it in each local sample and average
the results. This time the scatter plot of the distributed estimate against
the whole-sample estimate is a cloud instead of a line, because the average
of the correlations is not the correlation of the pooled data. Pearson's
$\rho$ is a nonlinear function of sums, and averaging nonlinear functions
computed on subsets does not recover the function of the whole. This matters
for social scientists in general, because you cannot distribute an estimator
just because you can distribute a mean. Medians, quantiles, regression
coefficients, variances and correlations all need a specific solution. The
second part of the practical Python examples shows this with data that is
split unevenly over four machines.

A smarter calculation changes what the Map phase returns. Pearson's
correlation can be written entirely in terms of sums,

$$\rho_{xy} = \frac{n\sum_i x_i y_i - \sum_i x_i \sum_i y_i}
{\sqrt{n\sum_i x_i^2 - (\sum_i x_i)^2}\ \sqrt{n\sum_i y_i^2 - (\sum_i y_i)^2}},$$

so each Map returns its sample size $n_j$ and five partial sums over its own
sample, namely $\sum x$, $\sum y$, $\sum x^2$, $\sum y^2$ and $\sum xy$,
instead of a correlation. Sums are additive over partitions, so the reducer
adds them across machines, $\sum_i x_i = \sum_j \sum_{i \in S_j} x_i$ and
likewise for the rest, and then evaluates the formula once. The result is
exactly the whole-sample correlation and the scatter plot becomes a perfect
line again. What we learn from this example is that we accept added
communication time to avoid added variance in the estimate. Each machine now
sends six numbers instead of one, so $T_{comm}$ grows, but the estimate is
exact instead of noisy. Designing a distributed algorithm means deciding how
much communication time to spend for how much accuracy. In general, we look
for a set of quantities that are additive over partitions and that determine
the statistic we want. These are called *sufficient statistics*. If your
estimator has a small set of them, it can be distributed exactly.

---

## 11. Amdahl's law {#limitations}
Can you actually achieve an optimal speedup? Gene Amdahl showed in 1967 that
there is an upper limit. The intuition is that there is always a part of the
code that cannot be parallelized, and with increasing parallelization this
part dominates the overall runtime of the program. The maximal speedup
depends on two variables, namely the fraction $P$ of the computation that can
be parallelized, for example 80%, and the number $N$ of processors or threads
that can be used in parallel. Amdahl's law gives the speedup $S$ of the
execution of the whole task as

$$S = \frac{1}{(1 - P) + \dfrac{P}{N}}.$$

In the denominator, $(1-P)$ is the serial part, which does not get faster
with more processors, and $P/N$ is the parallel part divided among the $N$
processors. For $P = 0.8$ the speedup grows as follows:

| $N$ | $S$ |
|---|---|
| 1 | 1.00 |
| 2 | 1.67 |
| 4 | 2.50 |
| 8 | 3.33 |
| 16 | 4.00 |
| 100 | 4.81 |
| $\infty$ | **5.00** |

For example, for $N = 2$ we get $S = 1/(0.2 + 0.4) = 1.67$. In the limit, as
$N \to \infty$, $P/N \to 0$ and $S \to 1/(1-P) = 1/0.2 = 5$. Two consequences
follow from this:

- **The maximum speedup is $1/(1-P)$** regardless of how many processors you
  buy. With 20% of serial code you can never go faster than 5×, even with a
  million cores.
- **Diminishing returns come fast.** Going from 1 to 4 processors gives a
  speedup of 2.5×, while going from 4 to 100 gives less than 2× more, so the
  eighth processor contributes less than the second.

In practice, you should measure $P$ before parallelizing. For example, if a
profiler says that half of your runtime is in a sequential file-parsing step,
your maximum speedup is 2× and the effort is probably better spent on the
parser. A more optimistic view is Gustafson's law, which observes that people
who buy more processors often use them to solve bigger problems rather than
the same problem faster, and the serial fraction of a bigger problem is often
smaller. The first part of the practical Python examples measures the speedup
of a real job on one to eight workers and compares it with Amdahl's law.

---

## 12. Summary

Parallelization is motivated by the limits of Moore's law. Its paradigms are
multi-core, multi-processor and multi-thread execution, and it should not be
confused with concurrency. Hardware parallelization happens at the
instruction level, in multi-core processors, in GPUs and in clusters.
Software parallelization includes distributed computing with MapReduce.
Finally, the limit of parallelization is given by Amdahl's law.

---

## 13. Why does this matter? Practical Python examples

Check the [practical Python examples in this Jupyter notebook](https://github.com/dgarcia-eu/ICSS/blob/main/PythonExamples/Examples12-ParallelProgramming.ipynb).
There, you will see how much faster a bootstrap runs on two, four and eight
cores and where Amdahl's law limits it, which statistics can be combined
exactly from data that is split over several machines, and why threads speed
up downloads but not computations.

---

## 14. Check yourself

**1.** Your program spends 90% of its time in a parallelizable loop. What is the best possible speedup, and how many cores get you halfway there?

<details><summary>Answer</summary>

The maximum speedup is $1/(1 - 0.9) = 10\times$. Half of that is 5×, which
needs $5 = 1/(0.1 + 0.9/N)$, so $0.1 + 0.9/N = 0.2$ and $N = 9$. Nine cores
get you to 5×, while the remaining 5× would need infinitely many cores. All
Amdahl curves have this shape, with a fast start and a slow approach to the
maximum.

</details>

**2.** A web scraper that fetches 1,000 pages is slow. Threads or processes?

<details><summary>Answer</summary>

Threads or asynchronous I/O are the better choice. The work is I/O-bound,
because almost all the time is spent waiting for network responses, and while
one thread waits, another can send its request. You do not need multiple
cores for this, since concurrency on one core is enough. Multiple processes
would work too but would cost more memory without any benefit.

</details>

**3.** Why can mergesort's two recursive calls run in parallel, but not the two halves of an in-place bubble sort pass?

<details><summary>Answer</summary>

The calls of mergesort operate on disjoint subarrays, so neither call reads
or writes what the other uses and any interleaving gives the same result. A
bubble sort pass compares and swaps adjacent elements along the whole array,
so the regions that each half works on overlap at the boundary. In addition,
the passes depend on each other sequentially. Parallel execution is safe when
the tasks access disjoint parts of memory.

</details>

**4.** You distribute a median calculation by computing the median on each machine and averaging. Is that correct?

<details><summary>Answer</summary>

No, for the same reason as for Pearson's correlation. The median is not
linear, so the average of the medians is not the median of the pooled data.
For example, consider two machines holding [1, 2, 3] and [100, 200, 300].
Their medians are 2 and 200 and the average of these is 101, while the true
median is 51.5. Unlike the correlation, the median has no small set of
additive sufficient statistics. Its exact distributed computation therefore
needs a different algorithm with several communication rounds, or an
approximation with a stated error bound.

</details>

**5.** Why does a pipelined CPU not make a single instruction finish any faster?

<details><summary>Answer</summary>

The instruction still passes through all five stages with one cycle each, so
its latency is unchanged at 5 cycles. The pipeline improves the throughput
instead, because once it is full, five instructions are in progress
simultaneously and one instruction completes per cycle. Latency and
throughput are easy to confuse when we reason about parallel systems.

</details>

---

## 15. References

- **DeNero, J.** *Composing Programs*, section 4.8, "Parallel Computing".
  <https://www.composingprograms.com/pages/48-parallel-computing.html>. The
  reading for this session.
- **Vo, H. & Silva, C. (2017).** "Programming with Big Data", chapter 5 of
  Foster, I., Ghani, R., Jarmin, R. S., Kreuter, F. & Lane, J. (eds.), *Big
  Data and Social Science*. Chapman & Hall/CRC. The second reading for this
  session, with MapReduce and Spark in practice.
- **Moore, G. E. (1965).** "Cramming more components onto integrated
  circuits". *Electronics* 38(8). The original observation of Moore's law.
- **Our World in Data, *Technological Change*:**
  <https://ourworldindata.org/technological-change#advances-in-computational-technology>.
  Transistor-count data behind the Moore's law figure.
- **Amdahl, G. M. (1967).** "Validity of the single processor approach to
  achieving large scale computing capabilities". *AFIPS Conference
  Proceedings* 30, 483–485. The source of Amdahl's law.
- **Gustafson, J. L. (1988).** "Reevaluating Amdahl's Law". *Communications
  of the ACM* 31(5), 532–533.
- **Flynn, M. J. (1972).** "Some Computer Organizations and Their
  Effectiveness". *IEEE Transactions on Computers* C-21(9), 948–960. The
  source of Flynn's taxonomy.
- **Hennessy, J. L. & Patterson, D. A. (2019).** *Computer Architecture: A
  Quantitative Approach*, 6th ed. Morgan Kaufmann. Pipelining and
  instruction-level parallelism.
- **Kocher, P. et al. (2019).** "Spectre Attacks: Exploiting Speculative
  Execution". *IEEE Symposium on Security and Privacy*.
- **Lipp, M. et al.
  (2018).** "Meltdown: Reading Kernel Memory from User Space". *USENIX
  Security Symposium*. <https://meltdownattack.com/>
- **Dean, J. & Ghemawat, S. (2008).** "MapReduce: Simplified Data Processing
  on Large Clusters". *Communications of the ACM* 51(1), 107–113. The
  original MapReduce paper.
- **Zaharia, M. et al. (2016).** "Apache Spark: A Unified Engine for Big Data
  Processing". *Communications of the ACM* 59(11), 56–65.
- **Garcia, D.** *Scalable Algorithms for Statistical Inference from Big
  Data*, lecture slides. Source of the divide-and-conquer figures and the
  correlation example of distributed statistical inference.
- **Jordan, M. I., Lee, J. D. & Yang, Y. (2019).** "Communication-Efficient
  Distributed Statistical Inference". *Journal of the American Statistical
  Association* 114(526), 668–681. The trade-off between communication and
  accuracy in depth.
- **Lawrence Livermore National Laboratory, *Introduction to Parallel
  Computing*:**
  <https://hpc.llnl.gov/documentation/tutorials/introduction-parallel-computing-tutorial>.
  Source of the "reasons to parallelize" framing.
- **jq manual:** <https://jqlang.org/>. For the exercise session.
