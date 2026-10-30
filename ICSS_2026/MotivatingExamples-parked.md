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
