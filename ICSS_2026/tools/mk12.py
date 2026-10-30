OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/12-ParallelProgramming/ICSS-2026-12-ParallelProgramming.qmd"
s = ['''---
title: "<span class='course'>Introduction to Computing for the Social Sciences</span><br><span class='session'>Session 12 &ndash; Parallel Programming</span>"
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
    footer: "<span class='fbar-left'>Session 12</span><span class='fbar-mid'>Introduction to Computing for the Social Sciences</span><span class='fbar-right'>Winter Semester 2026-2027</span>"
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
  - Exercise: JQ + Parallelization exercises
- Session 13: Social Science Applications
- Session 14: Exam Review
:::
:::
::::
''']

def sl(t, b): s.append(f"\n## {t}\n\n{b}\n")

ITEMS = ["Parallelization", "Hardware Parallelization", "Software Parallelization",
         "Limitations"]
def outline(cur=None):
    m = [f"[{t}]{{.current}}" if i+1 == cur else t for i, t in enumerate(ITEMS)]
    cls = "{.outline .focus}" if cur else "{.outline}"
    return "::: " + cls + "\n" + "\n".join(f"- {t}" for t in m) + "\n:::"

sl("Install jq for next exercise session", """::: {.center-h .sm}
<https://jqlang.org/>
:::

::: {.center-h}
![](figures/jq-website.png){height="10.4em"}
:::""")

sl("Overview", outline())

sl("Moore's law", """::: {.center-h}
![](figures/moores-law.png){height="12.0em"}
:::""")

sl("Moore's law and its limits", """:::: {.columns}
::: {.column width="76%"}
::: {.sm}
- **Moore's law** predicts that the number of transistors per microchip doubles every two years &ndash; exponential growth in computing power
- While the increase is still exponential, the rate is slower and doubling takes more than two years
- There is a **physical limit**: a transistor cannot be smaller than an atom
- The limit is expected to be reached in this decade unless radically different models of computation become feasible
- **Parallelization is a workaround to this limit:** using several processors
:::
:::

::: {.column width="24%"}
::: {.imgcol}
![](figures/transistor-symbol.png){height="4.4em"}

![](figures/transistor-photo.png){height="4.0em"}
:::
:::
::::

::: {.source}
To learn more about Moore's law: <https://ourworldindata.org/technological-change#advances-in-computational-technology>
:::""")

sl("The brain as an inspiration for parallelization", """:::: {.columns}
::: {.column width="68%"}
::: {.tbl-grid .xs}
| | Operations/sec | Power [Watts] | Cores | sec/cycle |
|---|---|---|---|---|
| **Brain** | $10^{13}$ | 15&ndash;20 | ? | $10^{-3}$ |
| **Intel Terascale** | $10^{12}$ | 85 | 80 | $10^{-9}$ |
| **Supercomputer Blue Gene** | $3.6 \\times 10^{14}$ | $1.2 \\times 10^{6}$ | 130 000 | $10^{-9}$ |
:::

::: {.sm}
- Brains work **slowly** but are **massively parallel**
- Example of various regions active at the same time
:::
:::

::: {.column width="32%"}
![](figures/fmri-brain.png){height="7.4em"}
:::
::::

::: {.source}
<https://psychcentral.com/lib/what-is-functional-magnetic-resonance-imaging-fmri>
:::""")

sl("Parallel computer example: IBM Blue Gene", """::: {.center-h}
![](figures/blue-gene.png){height="11.6em"}
:::

::: {.source}
<https://en.wikipedia.org/wiki/IBM_Blue_Gene>
:::""")

sl("Reasons to parallelize", """::: {.sm}
- **Save time and/or money**
  - throw compute resources at a problem and shorten compute time
  - can use cheap commodity components to build parallel processors
- **Solve larger, more complex problems**
  - some problems are so large they are infeasible to solve using serial computation, especially with limited memory
  - example: web search engines and databases processing millions of transactions every second
- **Provide concurrency**
  - a single compute resource can only do one thing at a time; multiple compute resources can do many things simultaneously
:::""")

sl("Types of parallelization", """:::: {.columns}
::: {.column width="56%"}
::: {.sm}
Different ways to "multiply" processing:

- **multiprocessor:** more than one CPU
- **multicore:** one CPU with several cores
- **multithreading:** a single core executes more than one task concurrently
:::

::: {.example .xs style="margin-top:0.6em"}
[Process]{.label}

**CODE** &nbsp;&nbsp; **DATA** &nbsp;&nbsp; **FILE POINTERS**

| thread 1 | thread 2 | thread 3 |
|---|---|---|
| registers · stack | registers · stack | registers · stack |
:::
:::

::: {.column width="44%"}
::: {.imgcol}
![](figures/blue-gene.png){height="4.4em"}

![](figures/cpu-die.jpg){height="5.4em"}
:::
:::
::::""")

sl("Single-thread vs Parallel", """::: {.center-h}
![](figures/12-single-vs-parallel.svg){height="10.4em"}
:::""")

sl("Concurrent vs Parallel", """::: {.center-h}
![](figures/12-concurrent-vs-parallel.svg){height="12.0em"}
:::""")

sl("Concurrent vs Parallel", """::: {.sm}
**Concurrency**

- Concurrency means executing multiple tasks **at the same time but not necessarily simultaneously**
- An application is making progress on more than one task at the same time (concurrently). It does not completely finish one task before it begins the next
- Tasks on the **same CPU**, order not completely fixed

**Parallelism**

- Parallelism means that an application splits its tasks into smaller subtasks which can be processed in parallel
- Tasks on **different CPUs**, tasks are at certain times executed in parallel
:::""")

sl("Concurrency costs and advantages", """::: {.center-h}
![](figures/12-concurrency-switch.svg){height="2.6em"}
:::

::: {.sm}
- **Switching between tasks takes computing time**
  - e.g. loading data or instructions into memory
  - this is handled by the operating system, using that compute time
- **Concurrency can save time** when using resources that are slower than the CPU. The CPU can change to another process when a slow task starts. For example:
  - access to files on the hard drive
  - access to information over a network
  - access to data from a peripheral device
  - user input
:::""")

sl("Hardware Parallelization", outline(2))

sl("Flynn's Taxonomy", """::: {.sm}
Multi-processor computer architecture (hardware) classification along two dimensions: **instruction stream** and **data stream**. Both can be single or multiple.
:::

::: {.center-h}
![](figures/12-flynn.svg){height="9.6em"}
:::""")

sl("Flynn's Taxonomy", """::: {.center-h}
![](figures/12-flynn.svg){height="12.0em"}
:::""")

ILP = [
    None,
    "**IF:** instruction fetch &ndash; get next instruction code",
    "**ID:** instruction decode &ndash; convert code into hardware activation flags",
    "**EX:** execute &ndash; perform calculation based on registry information",
    "**MEM:** memory access &ndash; write results to main memory if necessary",
    "**WB:** register write back &ndash; change registers (e.g. next instruction pointer)",
]
for k in range(7):
    subs = [x for x in ILP[1:k+1] if x]
    sub = "".join(f"\n    - {x}" for x in subs)
    tail = ""
    if k == 6:
        tail = ("\n- Not all instructions need all five cycles. Details depend on the architecture"
                "\n- Different parts of the hardware are used for each microinstruction")
    sl("Instruction-level parallelism", f"""::: {{.center-h}}
![](figures/12-pipeline-stages.svg){{height="2.0em"}}
:::

::: {{.sm}}
- CPU architectures have instructions that are divided into **microinstructions**
- Each microinstruction takes a hardware clock cycle
- The example is an architecture with five microinstructions{sub}{tail}
:::""")

sl("Instruction-level parallelism", """::: {.center-h}
![](figures/12-pipeline-none.svg){height="4.0em"}
:::

::: {.sm}
- A canonical processor **without** parallelism: takes 5 clock cycles per instruction
:::

:::: {.columns}
::: {.column width="60%"}
![](figures/12-pipeline-full.svg){height="6.4em"}
:::

::: {.column width="40%"}
::: {.sm}
- A **pipelined** processor can simultaneously execute five instructions
- It can take up to only **one clock cycle per instruction**
:::
:::
::::""")

sl("Instruction-level parallelism: caveats", """::: {.center-h}
![](figures/12-pipeline-caveat.svg){height="6.4em"}
:::

::: {.xs}
- **Speculative execution:** future instructions start before we finish one
  - control flow usually makes the CPU throw away future instructions
  - e.g. an `if` statement changes the next instruction &rarr; need to clean the pipeline
- **Security risks:** speculative execution leaves traces that can be read by other programs
  - the **Spectre** and **Meltdown** vulnerabilities make it possible to read private data of other programs left in the registers of speculated execution
:::""")

sl("Multi-core processors: your laptop", """::: {.center-h}
![](figures/cpu-die.jpg){height="8.4em"}
:::

::: {.sm}
- Several cores per processor allow executing multiple threads in parallel
- Most likely in this course, all student laptops and mobile phones are multi-core and many even multi-processor
:::

::: {.source}
<https://superuser.com/questions/584900/how-distinguish-between-multicore-and-multiprocessor-systems>
:::""")

sl("Graphics Processing Unit (GPU)", """:::: {.columns}
::: {.column width="58%"}
::: {.xs}
- Graphics Processing Units are specialized to calculate what is displayed on a screen
- Designed for **multiplications of matrices** to calculate how to display 3D models
- Performs the same calculation over a large set of data (a vector)
- GPUs have large memories and high clock speeds
- **Cannot do any operation efficiently!** Designed for matrix operations
- Applications beyond graphics:
  - mining cryptocurrencies: solving modular algebra equations for many possible solutions
  - training machine learning models: applying matrix operations to fit many parameters on large datasets
:::
:::

::: {.column width="42%"}
![](figures/gpu-card.png){height="5.4em"}
:::
::::""")

sl("Computing clusters", """::: {.sm}
- **Computing cluster:** linking many computers with very high bandwidth connections
- Example: the Scientific Compute Cluster (SCC) of Uni Konstanz
  - Infiniband: 56 Gbit/s, 0.7 µs latency
  - Intel Broadwell HPC compute nodes
    - 28 cores per node
    - up to 1024 GB RAM
  - large RAID (redundant array of independent disks) memory
- The Politics & Public Administration department is an SCC **shareholder** with 4 compute nodes, i.e. 112 cores
  - part of the larger SCC infrastructure
  - if available, can use compute nodes of other shareholders. Resources might be idle when other departments do not need them
:::""")

sl("Software Parallelization", outline(3))

sl("Types of Software Parallelization", """::: {.sm}
- **Multiple threads or processes in the same computer**
  - e.g. running mergesort with calls in separate parts of memory
  - *Issues:* coordinating memory access
  - *Solutions:* Inter-Process Communication (IPC) and Message Passing Interfaces (MPI) &ndash; not covered here
- **Multiple machines connected through a network: distributed computing**
  - e.g. splitting parts of mergesort to different machines and merging results in more central machines
  - *Issues:* network communication is the bottleneck for computation
  - *Solutions:* distributed paradigms like **MapReduce**
:::""")

sl("MapReduce", """::: {.center-h}
![](figures/mapreduce-slide.jpg){height="11.6em"}
:::""")

sl("MapReduce", """:::: {.columns}
::: {.column width="52%"}
::: {.sm}
- **Map phase:** compute parts of the solution on partial datasets in each machine
- **Communication phase:** send Map results to the Reducer over the network
- **Reduce phase:** combine Map results into the final solution
- Computations can take several Map-Reduce iterations or hierarchies
- Apache Hadoop and Spark are some of the most popular software solutions for MapReduce
:::
:::

::: {.column width="48%"}
![](figures/mapreduce-slide.jpg){height="5.6em"}

::: {.imgrow .middle}
![](figures/logo-hadoop.png){height="2.2em"}
![](figures/logo-spark.png){height="2.6em"}
:::
:::
::::""")

sl("Distributed statistical inference example", """::: {.center-h}
![](figures/inference-problem.jpg){height="6.6em"}
:::

::: {.sm}
- Billions of data points distributed over several thousand data servers
- Objectives:
  - Save time by using a distributed architecture: **bring the code to the data**
  - Warning! Communication time matters (vs. plain parallel processing)
  - Inference should have desirable statistical properties and minimize additional error
:::""")

sl("Distributed statistical inference: desired properties", """::: {.center-h}
![](figures/mapreduce-slide.jpg){height="11.0em"}
:::""")

sl("When things are easy: averaging", """:::: {.columns}
::: {.column width="52%"}
![](figures/inference-averaging.jpg){height="10.4em"}
:::

::: {.column width="48%"}
::: {.sm}
- **Map:** compute the same estimator in each local sample
- **Reduce:** aggregate to the final estimator by averaging each Map result
:::
:::
::::""")

sl("Averaging: computing a mean", """::: {.center-h}
![](figures/inference-mean.jpg){height="11.4em"}
:::""")

sl("Averaging: computing a mean", """::: {.center-h}
![](figures/inference-mean.jpg){height="11.4em"}
:::""")

sl("Problems with averaging: Pearson's correlation", """:::: {.columns}
::: {.column width="50%"}
![](figures/inference-correlation-1.jpg){height="9.6em"}
:::

::: {.column width="50%"}
::: {.sm}
- **Map:** compute Pearson's correlation in each local sample
- **Reduce:** aggregate to the final estimator by averaging each Map result
:::

![](figures/pearson-formula.png){width="94%"}
:::
::::""")

sl("Problems with averaging: Pearson's correlation", """::: {.center-h}
![](figures/inference-correlation-2.jpg){height="11.4em"}
:::""")

sl("Smarter distributed calculation of correlations", """::: {.center-h}
![](figures/inference-smarter-1.jpg){height="11.4em"}
:::""")

sl("Smarter distributed calculation of correlations", """::: {.center-h}
![](figures/inference-smarter-2.jpg){height="11.4em"}
:::""")

sl("Smarter distributed calculation of correlations", """::: {.center-h}
![](figures/inference-smarter-2.jpg){height="10.0em"}
:::

::: {.tag .xs}
Added communication time tradeoff to avoid added variance in the estimate
:::""")

sl("Limitations", outline(4))

sl("Limits to Parallelization", """::: {.sm}
- Can you actually achieve an optimal speedup?
- **Gene Amdahl (1967): there is an upper limit**
- Intuition:
  - there is always a part of the code that **cannot** be parallelized
  - with increasing parallelization, this part dominates the overall runtime of the program
- Maximal speedup depends on two variables:
  - $P$: fraction of the computation that can be parallelized, e.g. 80%
  - $N$: number of processors / threads that can be used in parallel
:::""")

sl("Limits to Parallelization: Amdahl's law", """:::: {.columns}
::: {.column width="42%"}
![](figures/amdahl-formula.png){width="92%"}

::: {.sm}
- $S$: speed-up of the execution of the whole task, e.g. 2×
- $P$: fraction of the computation that can be parallelized, e.g. 80%
- $N$: number of processors / threads that can be used in parallel
:::
:::

::: {.column width="58%"}
![](figures/amdahl-plot.png){height="10.0em"}
:::
::::""")

sl("Summary", """:::: {.columns}
::: {.column width="72%"}
::: {.sm}
- **Parallelization**
  - Motivation with Moore's law
  - Example paradigms: multi-core, multi-processor, multi-thread
  - Parallelization vs concurrency
- **Hardware Parallelization**
  - Instruction-level parallelization
  - Multi-core processors, GPUs and clusters
- **Software Parallelization**
  - Distributed computing: MapReduce
- **Limitations:** Amdahl's law
:::
:::

::: {.column width="28%"}
::: {.tag .sm}
Now: course surveys!
:::
:::
::::""")

for part, pswd, img in [("Theory", "ATEVY", "qr-survey-theory"),
                        ("Practice", "XZ7GC", "qr-survey-practice")]:
    sl("Please help us to improve the course!", f""":::: {{.columns}}
::: {{.column width="58%"}}
::: {{.sm}}
- Survey only for the **{part}** part of ICSS
- <https://evasys.uni-konstanz.de/evasys/online.php?pswd={pswd}>
- It takes about 5-10 minutes
- Completely anonymous
:::

![](figures/evasys-laptop.jpg){{height="4.4em"}}
:::

::: {{.column width="42%"}}
![](figures/{img}.png){{height="8.4em"}}
:::
::::""")

open(OUT, "w").write("".join(s))
print("slides:", "".join(s).count("\n## "))
