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
