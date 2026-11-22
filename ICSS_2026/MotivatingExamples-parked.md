# Parked motivating examples

Examples taken out of a session and kept to be used later. Each one is also
stored in `tools/motivation_data.py` (`PARKED`), so it can be put back into a
deck and its handout with the usual markers.

---

## M03-B · The helpline that answered the newest caller first

**Status.** Removed from session 3 (Data Structures) on 2026-10-30. To be used
when stacks, queues and heaps are covered: session 5 defines stacks and queues
(PUSH, POP, ENQUEUE, DEQUEUE), session 6 heaps and priority queues.

### Slide (as it was in the session 3 deck)

```markdown
## The helpline that answered the newest caller first {.fit1}

::: {.motivation}
[Motivating example]{.label}
A support system stores incoming requests in whatever structure the developer
reached for. Under load, callers are answered **most-recent-first**. Someone who
called at 9 a.m. is still waiting at 5 p.m., while a 4:55 p.m. caller is served
immediately.
:::

- No request was lost and the **average** waiting time looks
  reasonable.
- The failure is in *who* waits: early ones wait more and not just a little bit more.

[What was the problem with the structure of the data about calls and what would be the structure to serve people fairly?]{.ask}
```

### Handout text

A public service runs a support line. Requests that cannot be handled
immediately are stored and dealt with when a caseworker frees up, and the
developer, needing somewhere to put the pending ones, used a stack. A stack
is LIFO, last in, first out: whatever went in most recently comes out first.
So under sustained load, precisely when the system matters, the person who
has been waiting longest is at the bottom of the stack, underneath everyone
who arrived after them, and a request that arrives during a busy period can
be buried indefinitely. This has a name, *starvation*. The instructive part is
how well the system hides it. Nothing is lost, since every request is still
there; no error occurs, since the code is correct in the sense of doing what
it says; and the mean waiting time can look perfectly acceptable, because most
people are served instantly. The damage is entirely in the tail, and the tail
is people.

Change one structure and the outcome changes. A queue is FIFO, first in,
first out: requests are appended at the rear and served from the front, so
every request is served after a bounded number of others, and callers are
served in the order they called. Both operations still cost $O(1)$, so the
fair version is not slower. You could also use a priority queue, which serves
the most urgent case first. That is often the right thing, and it
reintroduces the original problem in a new form, because low-priority cases
can starve unless their priority rises with their waiting time. The design
question does not go away; it becomes explicit.

Section 3 of this session covers the linked lists on which stacks and queues
are usually built, and why insertion at one end is cheap in one representation
and expensive in another; the two structures themselves, with their operations
PUSH and POP, ENQUEUE and DEQUEUE, are defined in session 5, where they drive
the two ways of searching a graph. The general point is worth stating plainly,
because it is the reason why this material belongs in a social science course:
a data structure encodes a policy. LIFO and FIFO are not two implementations of
the same thing; they are two different answers to the question of who gets
served first, and that question is not technical. Somebody chose, possibly
without realizing that they were choosing.

---

## M04-B · "Clear the cache", said the developer

**Status.** Removed from session 4 (Software) on 2026-11-08 and replaced by
the Symbian example (M04-D).

### Slide (as it was in the session 4 deck)

```markdown
## "Clear the cache", said the developer {.fit1}

::: {.motivation}
[Motivating example]{.label}
Late 2025, posted on Reddit: a developer asks Google's coding agent
**Antigravity** to clear a project's cache. The agent runs
`rmdir /s /q d:\`, which deletes **the entire D: drive**, past the Recycle Bin.
Its answer: *"I am deeply, deeply sorry. This is a critical failure on my part."*
:::

:::: {.figures}
::: {.fq}
[1]{.big}[command]{.cap}
:::
::: {.fq}
[1 drive]{.big}[deleted instead of 1 folder]{.cap}
:::
::: {.fq}
[0]{.big}[confirmations asked ("Turbo mode")]{.cap}
:::
::::

[What should have been specified, and checked, before a command that deletes files is allowed to run?]{.ask}

::: {.source}
TechRadar, December 2025; AI Incident Database, report 7050
:::
```

### Handout text

In late 2025 a developer posted on Reddit what had happened while using
Antigravity, a new programming environment by Google in which an AI agent can
edit files and run commands on the developer's computer. The developer asked
the agent to clear the cache of a project, a folder of temporary files that
can safely be deleted. The agent ran the Windows command `rmdir /s /q d:\`,
which removes a folder and everything in it, silently and without using the
Recycle Bin. The folder it named was not the cache folder but the root of the
whole D: drive. The agent's reply, once it noticed, was "I am deeply, deeply
sorry. This is a critical failure on my part." The developer had enabled a
mode in which the agent runs commands without asking for confirmation. Most of
the data had been backed up elsewhere; the rest was lost.

The story spread because the apology is funny, but the failure is the most
common one in software: a command whose effect was never checked before it
ran. What the developer wanted was specified only as "clear the cache". A
specification of the task would have said which folder and nothing else, and a
system that takes the specification seriously checks, before deleting
anything, that the target is that folder. That is what tests do for code, and
what confirmations and permissions do for commands: they compare what is about
to happen with what was meant.

Section 6 treats "what the program must never do" as part of every
specification, and section 7 shows how tests turn a specification into
something that is checked rather than hoped for.

---

## M04-C · The code freeze that was only a sentence

**Status.** Removed from session 4 (Software) on 2026-11-08 and replaced by
the Symbian example (M04-D).

### Slide (as it was in the session 4 deck)

```markdown
## The code freeze that was only a sentence {.fit1}

::: {.motivation}
[Motivating example]{.label}
July 2025: the founder of SaaStr spends twelve days vibe coding an app with
Replit's AI agent. On day nine, during a code freeze he had declared in the
chat, the agent **deletes the production database**, then reports that a
rollback is impossible. It was not; the data came back.
:::

:::: {.figures}
::: {.fq}
[1,206]{.big}[executives' records deleted]{.cap}
:::
::: {.fq}
[1,196]{.big}[companies' records deleted]{.cap}
:::
::: {.fq}
[0]{.big}[barriers between the agent and production]{.cap}
:::
::::

[A rule in a chat message is a wish. What would have made "never touch production" impossible to break?]{.ask}

::: {.source}
Fortune, 23 July 2025; AI Incident Database. Replit then separated development and production databases.
:::
```

### Handout text

In July 2025 Jason Lemkin, the founder of the software community SaaStr,
documented a twelve-day experiment in building an application by vibe coding
with the AI agent of the platform Replit. On day nine he had declared a code
freeze, a period in which nothing may be changed, and told the agent in the
chat to make no changes without his permission. The agent then deleted the
live production database, which held records on 1,206 executives and
1,196 companies. Asked about it, the agent admitted that it had ignored the
instruction, and it told Lemkin that a rollback was impossible, which turned
out to be wrong: the data could be restored. Replit's chief executive called
the deletion unacceptable, and the company separated development databases
from production databases so that an agent working on the code cannot reach
the real data.

The code freeze existed only as a sentence in a chat. Nothing in the system
enforced it: the agent had the permissions to delete the database, and the
development and the production data were the same data. A rule that matters
has to be part of the requirements of the system, and a rule that must never
be broken has to be enforced by the system itself, through permissions,
backups and separate environments, not requested in a prompt. Replit's fix is
exactly that: it turned a wish into a property of the system.

Section 5 places writing code inside the larger process of software
engineering, and section 6 explains why a prompt is a specification and why
some rules do not belong in a prompt at all.

---

## M05-A · Six handshakes, and how you would check

*Parked on 2026-11-15 (David: removed from the Algorithms session). Kept for later use.*

### Slide

```markdown
## Six handshakes, and how you would check {.fit1}

::: {.motivation}
[Motivating example]{.label}
Milgram's 1967 experiment asked people in Nebraska to get a letter to a stranger
in Boston by passing it only to someone they knew personally. The chains that
arrived had a median of **five intermediaries**. Fifty years later the same
question was answered directly over **1.59 billion people**, giving **3.57**.
:::

:::: {.figures}
::: {.fq}
[5.2]{.big}[Milgram, 1967: mean over the 64 letters that arrived]{.cap}
:::
::: {.fq}
[3.57]{.big}[Facebook, 2016: 1.59 × 10⁹ people]{.cap}
:::
::::

[Milgram needed volunteers and postage. What *procedure* answers the same question from the network itself?]{.ask}

::: {.source}
Milgram, *Psychology Today* (1967); Edunov, Diuk, Filiz, Bhagat & Burke, Facebook Research (2016)
:::
```

### Handout text

### A · Six handshakes, and how you would check

In 1967 Stanley Milgram gave letters to volunteers in Nebraska and Kansas. Each letter was addressed to a stockbroker in Boston and came with one rule, namely that you may only forward it to someone you know personally on a first-name basis. Of 296 chains started, 64 arrived, with a mean length of 5.2 intermediaries and a median of about five. The phrase "six degrees of separation" comes from this experiment by way of a later play. The experiment is famous, but it is a slow and expensive way to measure a graph. It also observes only the chains that were completed, which is a severe selection problem because a chain is more likely to arrive when the path is short. In 2016 the question was answered in a different way. Researchers took the Facebook friendship graph, with 1.59 billion people and hundreds of billions of edges, and computed the average distance between two randomly chosen people directly. The result was 3.57.

The second study is not conceptually harder than the first. The difference is that the researchers did not ask people to pass something through the network. Instead, a program explored the network itself. We start at a person and look at all their friends, who are at distance 1. Then we look at all of their friends who have not been seen yet, who are at distance 2, and we continue until everyone reachable has been seen. This procedure is called breadth-first search. Before it becomes an algorithm, we have to answer four questions:

1. **What exactly is a step?** A step is to look at all the friends of the current person.
2. **Which person do we look at next?** The answer is given by a queue, and choosing a stack instead gives a different algorithm with a different answer.
3. **How do we avoid going round in circles?** We mark every person who has already been seen.
4. **When do we stop?** We stop when nobody is left to look at, and we also need to know that this happens at all.

Without these four answers we only have a good idea, while with them we have a procedure that a machine can execute.

In this session you will learn which properties an algorithm must have, for example finiteness and definiteness, and how each of them rules out a specific way of writing something that looks like a procedure but is not one. You will also learn to write a procedure down as pseudocode or as a flowchart, so that another person and eventually a machine can execute it identically. Finally, we will learn about graphs, how to represent them, and breadth-first search, which is the computation described above. A research question of your own becomes computable when you can say without ambiguity what to do next, and most of the work is usually in getting to that point.

---

## M06-A · How many people report to her?

*Parked on 2026-11-22 (David: removed from the Recursion session). Kept for later use.*

### Slide

```markdown
## How many people report to her?

::: {.motivation}
[Motivating example]{.label}
An organizational chart has a chief executive, division heads, department heads,
team leads and staff, and **nobody knows how deep it goes**, because it differs
by division. You are asked how many people, in total, work below any given
manager.
:::

- A loop over levels needs to know **how many levels** to go through.
- You do not know that number, and it can change next month.

[How do you write a procedure that works without knowing in advance how deep the structure is?]{.ask}
```

### Transcript

````markdown
### A · How many people report to her?

An ordinary organizational chart has a chief executive, division heads below
her, and departments, teams and staff below them. Some
divisions have four levels, others have seven, and the number can change with
the next reorganization. How many people in total work below a given manager?
With what we learned in the Software session, the first idea is a loop that
adds up the direct reports, then their reports, then the reports of those.
Written out, the loop becomes:

```
total ← direct reports
For each direct report:
      total ← total + their direct reports
      For each of those:
            total ← total + their direct reports
                  ...
```

The problem is the `...` at the end. The nesting depth of the code has to
match the depth of the chart, but you do not know that depth when you write
the code and it is not even the same across the organization. You could write
ten levels of nesting, but the code would be wrong for a chart with eleven
levels and it would already be hard to read at the third. The solution comes
from looking at the structure of the data instead of the code. The subtree of
a manager is the manager plus the subtree of each direct report, so the
description of the whole chart refers to the same kind of thing as its parts.
We can write a procedure that follows that description:

```
Procedure HEADCOUNT-BELOW(person)
Inputs:
      person: a node of the organizational chart
Result: the number of people below person
total ← 0
For each direct report r of person:
      total ← total + 1 + HEADCOUNT-BELOW(r)
return total
```

The procedure has four lines and makes no assumption about the depth of the
chart. You can check that it is correct by reading it as a sentence, namely
that the number of people below me is, for each of my direct reports, that
person plus the number of people below them. The procedure also stops without
an explicit test, because a person with no direct reports never enters the
loop and returns 0.

In this session you will learn about the parts of a recursive definition,
namely a base case that returns without recursing and a recursion case that
moves closer to the base case. If either of them is wrong, the procedure never
stops. We will also learn about the call stack, i.e. what the machine keeps in
memory while those nested calls are waiting, and why "recursion depth
exceeded" is a limit that you can reach in practice. Finally, we will learn
about the types of recursion, including tree recursion, which is the type of
the procedure above because it makes one call per direct report. Recursion is
useful when the data is defined in terms of itself, which is the case for
organizations, family trees, file systems, comment threads and grammatical
sentences. If you work with data like these, a recursive procedure is often
the shortest correct way to process them.
````

---

## M06-C · The algorithm that is 2,300 years old

*Parked on 2026-11-22 (David: removed from the Recursion session). Kept for later use.*

### Slide

```markdown
## The algorithm that is 2,300 years old {.fit1}

::: {.motivation}
[Motivating example]{.label}
Euclid's *Elements*, Book VII, around 300 BC, gives a procedure for the greatest
common divisor, namely to **replace the larger number by its remainder against
the smaller and repeat.** It is still the algorithm your computer uses today.
:::

::: {.example}
[gcd(270, 192)]{.label}
gcd(270, 192) → gcd(192, 78) → gcd(78, 36) → gcd(36, 6) → gcd(6, 0) = **6**
:::

[What makes this procedure *stop*, and what happens to a procedure that calls itself and never stops?]{.ask}

::: {.source}
Euclid, *Elements*, Book VII, Propositions 1–2
:::
```

### Transcript

````markdown
### C · The algorithm that is 2,300 years old

The oldest algorithm still in everyday use is about 2,300 years old. Euclid
gives it in Book VII of the *Elements* in geometric language. To find the
greatest common measure of two magnitudes, you repeatedly subtract the smaller
from the larger. In modern form, using remainders instead of repeated
subtraction, the algorithm is written as follows:

$$\gcd(a, b) = \gcd(b,\ a \bmod b), \qquad \gcd(a, 0) = a.$$

These two equations find the largest number that divides both $a$ and $b$
without factoring either of them, which is not obvious at first sight. Let's
run the algorithm on 270 and 192.

| Call | $a$ | $b$ | $a \bmod b$ |
|---|---|---|---|
| 1 | 270 | 192 | 78 |
| 2 | 192 | 78 | 36 |
| 3 | 78 | 36 | 6 |
| 4 | 36 | 6 | 0 |
| 5 | 6 | 0 | base case, return 6 |

The algorithm needs only five calls because the numbers decrease fast, from
270 to 192, 78, 36 and 6. This speed has an explanation, namely that taking a
remainder against $b$ produces a number strictly less than $b$. It can be
shown that two steps at least halve the larger number, so the number of calls
is logarithmic in the input instead of linear. The table also shows the two
things that a recursion needs:

1. **A base case.** In line 5 of the table, $b = 0$ and the procedure returns
   without calling itself. Without the base case the recursion would never
   end.
2. **Progress towards the base case.** Each call replaces $(a, b)$ with
   $(b, a \bmod b)$ and $a \bmod b < b$, so the second argument strictly
   decreases and is never negative. A strictly decreasing sequence of
   non-negative integers cannot go on forever, so the base case is eventually
   reached.

The second point is a proof of termination, and you should be able to make an
argument like it for any recursion you write. If the base case is missing or
the recursive call does not shrink the problem, the calls never stop. Each
call pushes a frame onto the call stack until the stack is full, and the
program stops with the error `RecursionError: maximum recursion depth
exceeded`, which in Python happens after about 1,000 frames.

In this session you will learn about the base case and the recursion case as
the two requirements of a recursive definition, with termination arguments
like the one above. We will also learn about the call stack, what a stack
frame contains, and why Python stops at about 1,000 frames. Finally, we will
learn about linear recursion, of which Euclid's algorithm is the standard
example, and how it can be converted into a loop. After this session you
should be able to run Euclid's algorithm with pen and paper and to explain why
it stops.
````
