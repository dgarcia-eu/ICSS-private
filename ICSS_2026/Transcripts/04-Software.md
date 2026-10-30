# Session 4: Software

*Introduction to Computing for the Social Sciences · lecture transcript*

> Companion text for lecture 4. Notation follows
> [the course conventions](00-Conventions.md).
>
> **Reading for this session:** Chapters 2 and 6–8 of Zelle, *Python
> Programming: An Introduction to Computer Science* (2016), and chapter 6,
> "Testing and Debugging", of Guttag, *Introduction to Computation and
> Programming Using Python* (2016). References at the end.

---

## Contents

<!-- MOTIVATION-TOC:BEGIN -->
0. [Motivating examples](#motivating-examples)
<!-- MOTIVATION-TOC:END -->
1. [What programming is](#1-what-programming-is)
2. [Programming paradigms](#2-programming-paradigms)
3. [Imperative programming](#3-imperative-programming)
4. [Object-oriented programming](#4-object-oriented-programming)
5. [Software engineering](#5-software-engineering)
6. [Requirements, specifications, and design](#6-requirements-specifications-and-design)
7. [Testing](#7-testing)
8. [Check yourself](#8-check-yourself)
9. [References](#9-references)

---

<!-- MOTIVATION-SECTION:BEGIN -->
## Motivating examples

Three real cases from 2025, each a version of the same story: software built
quickly, accepted because it seemed to work, and missing something nobody had
written down or checked. None of them would have been prevented by more code.
Each would have been prevented by a requirement stated, a specification that
included what must never happen, or a test.

<!-- MOTIVATION:M04-A:BEGIN -->
### A · The app that leaked 13,000 photo IDs

Tea is a US app on which women share warnings about men they have dated. To
keep men out, it asked every new user to upload a selfie and, for many, a
photo of an identity document, which moderators used to verify the account.
In July 2025 a user of the forum 4chan posted the address of the online
storage, a Firebase bucket, where these images were kept. The storage had no
login and no access rule: anyone who knew the address could list and download
everything in it. About 72,000 images were copied and spread, among them
around 13,000 selfies and photo IDs, and the rest from posts, comments and
direct messages. Days later, a second problem exposed more than a million
private messages, and the company disabled its messaging feature.

Many people blamed vibe coding, the practice of building software by
prompting an AI tool and accepting what it produces; the person who first
leaked the data said so too. The company says the exposed data came from a
system built before February 2024. How the code was written does not change
the lesson, which is about requirements and tests rather than about who typed
the code. "Only moderators may see the identity photos, and only while they
verify an account" is a requirement that anyone at the company would have
agreed with if asked. Nobody wrote it down as part of what the system had to
do, so nothing in the system enforced it. And a single test, "try to download
an ID photo without logging in", would have failed on the first day.

Section 6 of this session is about requirements, including the ones that are
not about what the program computes but about how it must behave: security,
privacy, safety. Section 7 is about the tests that check them. For research
software the analogue is a script that produces the right table and also
writes the respondents' names into a file that ends up public.
<!-- MOTIVATION:M04-A:END -->
<!-- MOTIVATION:M04-B:BEGIN -->
### B · "Clear the cache", said the developer

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
<!-- MOTIVATION:M04-B:END -->
<!-- MOTIVATION:M04-C:BEGIN -->
### C · The code freeze that was only a sentence

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
<!-- MOTIVATION:M04-C:END -->
---

<!-- MOTIVATION-SECTION:END -->
## 1. What programming is

*Programming* is the process of creating a set of instructions that tell a
computer how to perform a task, and a *programming language* is a formal
language for writing those instructions, either directly as machine code or
as human-readable *source code* that is translated to machine code
automatically. Two words carry the weight. The language is formal: unlike
natural language, it has a precise grammar, and a text either is a program in
the language or is not. And the translation is automatic: we write for humans,
and the machine executes something else.

Programming languages sit on a ladder from close to the machine to close to
the human. The same small computation, the area of a triangle, looks very
different on each rung:

| Level | Examples | What it is | The same computation |
|---|---|---|---|
| High-level | Python, R, Java, C | written for humans, portable; one line becomes many machine instructions | `area = b * h / 2` |
| Low-level | assembly language | readable names for machine instructions | `LOAD r1,b` `LOAD r2,h` `MUL r1,r2` `DIV r1,#2` |
| | machine code | the binary instructions the processor executes | `0001001001000101 0010010011101100 …` |

At the bottom, *machine code* is what the processor executes, and each
processor family has its own instruction set. *Assembly language* gives
readable names to machine instructions, so `MUL r1,r2` stands for one
multiplication, and each assembly instruction becomes exactly one machine
instruction. The *high-level languages* at the top are written for humans,
are portable across machines, and one of their lines becomes many machine
instructions.

The translation from high-level code to machine code happens in one of two
ways. An *interpreter* translates and runs the code one line at a time, on
every run: it reads `x = 3`, translates and executes it, then the next line,
and so on until the output appears. Errors appear when the line that contains
them runs. Python, R and JavaScript, the languages of interactive data
analysis, are interpreted. A *compiler* translates the whole program once,
before it runs, into a file of machine code, which can then run many times,
fast. Many errors are found before anything runs. C and C++ are compiled, and
Java compiles to an intermediate code that is then interpreted. Either way,
the machine executes exactly what is written, not what you meant, and that is
the reason for the second half of this session.

---

## 2. Programming paradigms

*Programming paradigms* classify languages and programs by how they express a
computation. The basic split is between *imperative* programming, which
consists of statements that change the state of the program step by step and
so describes how to compute a result, and *declarative* programming, which
describes what the result should be and leaves the how to the system. Within
the imperative family, *object-oriented* programming groups data and the
instructions that operate on it into objects. Within the declarative family,
*functional* programming expresses the result as the value of functions
applied to other functions. You will meet the declarative style in SQL in
session 11, and the functional style through recursion in session 6. Python
supports all of these paradigms, and which one you are using depends on how
you write, not on the language. The rest of this part covers the two you use
in almost every Python program: imperative and object-oriented.

---

## 3. Imperative programming

The name comes from the Latin *imperare*, to order or to command, and it
describes what the programmer does: an imperative program is a sequence of
orders, carried out one after the other. The program has a *state*, the
current values of all its variables, and it runs by changing that state one
statement at a time. Four ingredients are enough to write any imperative
program. *Assignments* change the state, as in `total = 0`. *Control
structures* decide which statement runs next: conditions run a block only if a
test is true, and loops repeat a block. *Functions* give a name to a block of
steps, so that it can be reused and, just as important, checked on its own:

```python
total = 0             # assignment
for age in [34, 41]:  # loop
    if age >= 18:     # condition
        total += age

def mean(xs):         # function
    return sum(xs) / len(xs)
```

This is also how the hardware works, since a processor holds data in memory
and executes one instruction after another, which is why imperative
programming feels natural and why most courses start with it. Its weakness
shows as programs grow: when any statement can change any variable, it becomes
hard to know which part of a long program is responsible for a value, and that
is the problem object-oriented programming addresses.

---

## 4. Object-oriented programming

An *object* bundles data, its *attributes*, with the operations on that data,
its *methods*. A *class* is the blueprint for objects, and every object is an
*instance* of a class. A class `Respondent` might say that every respondent
has the attributes `name` and `age` and the methods `is_adult()` and
`describe()`; the objects `ana` and `ben` are two respondents, each with its
own name and age, and both able to do what the class says. You query or change
an object by calling one of its methods, with the notation
`object.method(arguments)`. The motivation is manageability: in a large
program, each piece of data travels with the only code that is allowed to
change it, so that when something goes wrong there is one place to look.

### You already use objects

Every value in Python is an object, including the strings and dictionaries of
the Python block course:

```python
s = "Konstanz"
s.upper()     # 'KONSTANZ'
s.count("n")  # 2

votes = {"yes": 12, "no": 7}
votes.get("no")        # 7
votes.get("maybe", 0)  # 0
list(votes.keys())     # ['yes', 'no']
```

`s` is an object of the class `str` and `votes` an object of the class
`dict`; `upper`, `count`, `get` and `keys` are their methods. Lists, sets and
pandas data frames work the same way: `ages.append(34)` and
`df.groupby("country")` are method calls on objects.

### Your own class and objects

A class definition says which attributes every object of the class has and
which methods it offers:

```python
class Respondent:
    def __init__(self, name, age):      # runs when an object is created
        self.name = name                # attributes
        self.age = age

    def is_adult(self):                 # methods; self is the object
        return self.age >= 18

    def describe(self):
        return f"{self.name}, {self.age} years"
```

```python
ana = Respondent("Ana", 34)
ben = Respondent("Ben", 16)
ana.describe()     # 'Ana, 34 years'
ben.is_adult()     # False
```

`Respondent("Ana", 34)` creates a new object and runs the special method
`__init__` on it, which stores the name and age as attributes. Inside a
method, `self` is the object the method was called on, so `ana.describe()`
reads Ana's attributes and `ben.is_adult()` reads Ben's.

### The four concepts

*Encapsulation* means that the data and the methods that use it live together
in one object. The object `ana` holds her name and age together with the
methods that use them, and other code asks the object, as in `ana.is_adult()`,
instead of working on the data directly.

*Abstraction* means that you use an object through its methods without knowing
how it works inside. `s.upper()` returns `'KONSTANZ'`, and you never need to
know how Python stores the characters of a string, which is also what lets
Python change that storage between versions without breaking your code.

*Inheritance* lets a new class extend an existing one and reuse its methods. A
student is a respondent who also has a study program:

```python
class Student(Respondent):
    def __init__(self, name, age, program):
        super().__init__(name, age)     # set name and age as a Respondent does
        self.program = program

bea = Student("Bea", 21, "Politics")
bea.is_adult()     # True: inherited from Respondent
```

`Student` repeats none of the code of `Respondent`, yet every student has a
name, an age, and the methods `is_adult()` and `describe()`. The test for
whether inheritance fits is the "is a" test: a student is a respondent, so it
fits; a survey has respondents, which is a different relation.

*Polymorphism* means that the same name does the right thing for each class.
`len("data")` counts characters and gives 4, `len([3, 1, 2])` counts elements
and gives 3, and `len({"yes": 12, "no": 7})` counts keys and gives 2. The
operator `+` is another example: it adds numbers and joins strings, which
explains a classic bug of data analysis, where ages read from a file as text
are "added" by joining them into one long string.

---

## 5. Software engineering

*Software engineering* is the application of a systematic, disciplined
approach to the development, operation and maintenance of software. A script
written for one analysis is one file, used by one person, run once. Software
is the same code grown into small parts, with requirements, tests,
documentation and a history of versions, used by other people on other data
for years. Research code becomes software more often than its authors
expect: it outlives the paper it was written for, other people build on it,
and published results depend on it.

A typical software engineering process has six stages. *Requirements* state
what problem is solved and for whom. The *specification* states precisely what
the program must do. The *design* decides how to split the work into parts,
such as functions, classes or modules, and which data structures connect them.
*Implementation* is writing the code. *Testing* checks that the code does what
the specification says. And *maintenance* covers using, fixing, extending and
handing over the program. The stages are connected by feedback: a failing test
sends you back to the code, a test that reveals a gap sends you back to the
specification, and new needs or new data start the cycle again from the
requirements. Real projects go around this loop many times in small steps,
which is called *iterative* development.

*Vibe coding*, a term coined by Andrej Karpathy in February 2025, describes
programming by describing what you want, accepting the generated code without
reading it, and seeing whether the result seems to work. In terms of the
software engineering process, a language model can take over much of one
stage, implementation. The others remain with people. Requirements belong to
you and your client, whoever needs the software, because only they know what
it is for. Specification, design, testing and maintenance remain yours: a
check written by the same system that wrote the code shares its blind spots,
and the design decides whether the generated pieces fit together. The three
opening examples all failed outside the implementation stage. With AI tools,
writing code has become the cheapest step, and everything around it is the
part you cannot delegate.

---

## 6. Requirements, specifications, and design

### Requirements

*Requirements* describe what the software must achieve, for whom, and under
which constraints, in the words of the people who need it. They come from the
*client*: a research team, a colleague, or yourself in three months. They
describe the need, not the program: "I need the mean age of each survey wave,
without the people who did not answer" is a requirement; a function with a
loop is not. Four questions find most requirements: who uses the software,
with which data, what must never happen, and when is it done? A
misunderstanding found while collecting requirements costs a conversation;
found after the code is written, it costs the code.

*Functional requirements* state what output the program gives for which
input: the mean skips missing answers, an empty survey raises an error.
*Non-functional requirements* state how the program must behave beyond its
outputs. In research software the important ones are *security* (users see
only their own data), *privacy* (no names or identifiers in the output),
*safety* (never delete or change the original data), *performance* (it must
finish on the full data set) and *reproducibility* (the same input gives the
same result on another machine). Tea, Antigravity and Replit all met their
functional requirements: the app stored photos, the agent deleted files, the
database answered queries. The non-functional requirements were never written
down, so nothing enforced them.

### Specifications

A *specification* is a precise description of what a program must do,
without saying how. It states the *inputs* and what may be assumed about them,
called the *preconditions*; the *outputs* and what is guaranteed about them,
called the *postconditions*; what happens in edge cases and errors; and what
the program must never do. You already know the format: every procedure in
this course starts with `Inputs:` and `Result:`, which is a specification in
miniature.

Consider a request that sounds complete: "write a function that computes the
mean age of the respondents". A human colleague would come back with
questions, and a language model will silently answer them for you. How are
missing answers stored, and do they count? What if nobody answered? Are ages
integers, or can they be text like `"34"`? Should the result be rounded? May
the function change the list it was given? Each question has several
defensible answers, and different answers give different numbers. The
specification is where you choose:

```python
def mean_age(ages):
    """Return the mean of the ages that were answered.

    ages: a list of ages in years (int); None marks a missing answer.
    Returns: the mean of the ages that are not None, as a float.
    Raises: ValueError if no age was answered.
    The list itself is not modified.
    """
```

Each line of the docstring answers one of the questions, and none of them says
how to compute the mean. That separation is the point: the specification can
be checked against any implementation, whether you wrote it, a colleague did,
or a language model generated it.

When you ask a language model for code, the prompt is a specification,
whether you write it carefully or not. Compare "write a function for the mean
age" with "write `mean_age(ages)`; `ages` is a list of ints, `None` marks a
missing answer and is skipped; return a float; raise `ValueError` if no age
was answered; do not modify the list; use only the standard library". The
second prompt gets better code and gives you something to check the code
against. One kind of rule does not belong in a prompt at all: a rule that must
never be broken, such as "never touch the production data" or "never delete
anything outside this folder". A prompt is a request. Such rules have to be
enforced by the system itself, through permissions, backups and separate test
and production data, so that breaking them is impossible rather than
discouraged.

### Design

The *design* decides how the program is split into parts and how the parts
are connected. For the survey example, a good design has four small
functions: `load_responses(path)` reads the file into a list of dictionaries,
one per respondent; `clean_ages(rows)` turns the age column into a list of
integers, with `None` for missing answers; `mean_age(ages)` computes the mean
of the answered ages, as specified above; and `report(mean, n)` writes one
line of text for the report. Each part has one job and its own specification,
and the design states what data flows between them: a list of dictionaries,
then a list of integers or `None`, then a number.

Small parts are easier to test, because each can be checked on its own with a
few cases; easier to replace, because a new data format only changes
`load_responses`; and easier to ask a language model for, one specified
function at a time, rather than a whole program at once. Choosing the data
structures is part of the design, and session 3 gave you the choices. Keep
items in order: a list, such as answers in the order they arrived. Look
something up by a key: a dictionary, such as `counts["yes"]` or a codebook.
Check membership fast: a set, such as the IDs already registered. Serve first
come, first served: a queue, such as a waiting list for a seminar. The design
is yours to decide; a language model writes better code inside a structure you
chose than when it invents one.

---

## 7. Testing

A *test* is a small program that runs your code on an input whose correct
output you know, and checks that the code produces it. The specification says
what should happen; a test checks that it does. The simplest test in Python is
an `assert` statement, which does nothing if its condition is true and stops
the program with an error if it is false:

```python
assert mean_age([30, 40, 50]) == 40
assert mean_age([30, None, 50]) == 40
```

The value of a failing `assert` is that it turns a quiet wrong number into a
loud failure. A wrong mean that looks plausible can travel all the way into a
paper; a stopped program cannot.

### Tests with pytest

For more than a few checks, a test framework keeps them organized. With
*pytest*, the standard tool in Python, you write each test as a function whose
name starts with `test_`, in a file whose name starts with `test_`, and run the
command `pytest` in that folder. It finds every test, runs it, and reports
which ones failed and why:

```python
# test_survey.py
import pytest
from survey import mean_age

def test_typical():
    assert mean_age([30, 40, 50]) == 40

def test_missing_answers_are_skipped():
    assert mean_age([30, None, 50]) == 40

def test_no_answers_raises():
    with pytest.raises(ValueError):
        mean_age([None, None])

def test_input_is_not_modified():
    ages = [30, None, 50]
    mean_age(ages)
    assert ages == [30, None, 50]
```

Each test corresponds to a line of the specification. The third checks that
an error is raised, with `pytest.raises`, and the fourth checks a property,
that the input is left unchanged, rather than an output.

### A generated function meets the tests

Here is a plausible implementation, of the kind a language model or a hurried
programmer produces:

```python
def mean_age(ages):
    answered = [a for a in ages if a is not None]
    return sum(answered) / len(ages)
```

It is short, it runs, and on a list without missing values it is correct.
Running the tests gives:

```
$ pytest -q
.FF.
FAILED test_missing_answers_are_skipped
  assert 26.666666666666668 == 40
FAILED test_no_answers_raises
  DID NOT RAISE ValueError
2 failed, 2 passed
```

Two of the four tests fail. The function divides by the number of all
respondents instead of the number who answered, so the mean of 30 and 50 with
one missing answer comes out as 26.7 instead of 40, a quiet wrong number of
exactly the kind that survives into tables. And when nobody answered it
returns 0 instead of raising an error, which would report a mean age of zero.
The fix is to divide by `len(answered)` and to raise `ValueError` when
`answered` is empty, after which all four tests pass. A quick look at the
output on one list without missing values would have shown nothing wrong.

### Choosing test cases

Good tests sit where the specification draws a line. A *typical* case checks
the ordinary behavior, `[30, 40, 50]` gives 40. Cases with *missing values*
check the rule for them, `[30, None, 50]` gives 40. *Boundary* cases check the
smallest inputs, `[25]` gives 25. *Empty* cases check the error rule, both
`[None, None]` and `[]` raise `ValueError`. And *must-not-happen* cases check
the prohibitions, the list is unchanged afterwards. The general heuristic is to
test missing, empty, single, largest and smallest inputs, because bugs gather
at the edges of what the programmer imagined.

### Test first, then generate

The order of work that makes AI tools safe to use is the order of the software
engineering process. First write the specification, as a docstring. Second,
write the tests from the specification, before any code exists, so that they
encode what you meant rather than what the code happens to do. Third, ask the
language model, or yourself, for an implementation. Fourth, run the tests and
read the code that passes them. Fifth, every bug you find later becomes a new
test, a *regression test*, so that the same bug can never come back unnoticed.
The tests are your measurement: they replace the feeling that the code works
with evidence that it does.

### What tests cannot do

Edsger Dijkstra put the limit of testing in one sentence in 1970: "Program
testing can be used to show the presence of bugs, but never to show their
absence." Tests check only the cases someone thought of, so a specification
that misses a requirement produces tests that miss it too, as the Tea app
shows. *Software verification* goes further: it proves, with mathematical
methods, that a program meets its specification for every possible input, not
only for the inputs that were tried. Verification is expensive and needs a
specification written in a formal language, so it is used where failure is
unacceptable: flight control software, railway signaling, the cores of
operating systems. For research code, the practical combination is a clear
specification, tests derived from it, and reading the code you did not write
before running it on real data. Within those limits, tests are the cheapest
form of quality control available to you: keep them small and fast, and run
them after every change.

---

## 8. Check yourself

**1.** Is Python compiled or interpreted, and what does that mean for when you see an error?

<details><summary>Answer</summary>

Python is interpreted: the code is translated and run line by line, each time
the program runs. Errors appear when the line that contains them runs, so a
mistake in a branch that your test data never reaches can stay hidden until
someone else runs the program on other data. (Strictly, Python first compiles
the source to an intermediate code and then interprets that, but the practical
consequence is the same.)

</details>

**2.** In `votes = {"yes": 12}; votes.get("no", 0)`, what is an object, what is a class and what is a method?

<details><summary>Answer</summary>

`votes` is an object of the class `dict`, and `get` is a method of that class,
called on `votes`. It returns 0, the default, because the key `"no"` is not in
the dictionary.

</details>

**3.** A colleague asks: "Can you write something that tells me how many people answered each option of question 5?" Write two functional and one non-functional requirement.

<details><summary>Answer</summary>

Functional: the result gives, for every option of question 5, the number of
respondents who chose it; respondents who did not answer are counted
separately, not as an option. Non-functional: the original data file is never
changed (safety), or the result contains no respondent identifiers (privacy).
Other reasonable answers: options nobody chose appear with 0; the count runs
in a few seconds on the full survey.

</details>

**4.** Write a specification, as a docstring, for a function `share_yes(answers)` that returns the share of "yes" answers, and three pytest tests for it.

<details><summary>Answer</summary>

```python
def share_yes(answers):
    """Return the share of "yes" among the valid answers.

    answers: a list of strings, each "yes", "no" or None (no answer).
    Returns: (number of "yes") / (number of "yes" or "no"), a float in [0, 1].
    Raises: ValueError if there is no "yes" or "no" answer.
    The list is not modified.
    """

def test_typical():
    assert share_yes(["yes", "no", "yes", "no"]) == 0.5

def test_missing_are_ignored():
    assert share_yes(["yes", None, "no", None]) == 0.5

def test_no_valid_answer_raises():
    with pytest.raises(ValueError):
        share_yes([None, None])
```

Counting missing answers as "no" would also be defensible, as long as it is
written down.

</details>

**5.** Your program must remember which participants have already registered for a study and tell, quickly, whether a new registration is a duplicate. Which data structure belongs in the design, and why?

<details><summary>Answer</summary>

A set of participant IDs: checking membership in a set takes constant time on
average, whatever its size, while a list would have to be scanned. If the
program also needs data about each participant, a dictionary from ID to that
data does both jobs.

</details>

**6.** A colleague says: "the generated code passed all my tests, so it is correct". What would you ask?

<details><summary>Answer</summary>

Which requirements the tests cover, since tests only check the cases someone
wrote; and whether the tests were written from the specification before the
code, or adapted to what the code produced, since tests written after the
fact tend to confirm the code rather than check it. Passing tests show the
absence of the bugs that were looked for, not of all bugs; only verification
proves correctness for every input.

</details>

---

## 9. References

- **Zelle, J. M. (2016).** *Python Programming: An Introduction to Computer
  Science*, 3rd ed. Franklin, Beedle & Associates. Chapters 2 and 6–8 are the
  reading for this session.
- **Guttag, J. V. (2016).** *Introduction to Computation and Programming Using
  Python*, 2nd ed. MIT Press. Chapter 6, "Testing and Debugging", covers
  section 7 in more depth.
- **IEEE (1990).** *Standard Glossary of Software Engineering Terminology*,
  IEEE Std 610.12-1990. The source of the definition of software engineering
  in section 5.
- **Dijkstra, E. W. (1970).** *Notes on Structured Programming* (EWD249). The
  source of the quotation in section 7.
- **pytest documentation.** <https://docs.pytest.org/>. "Get started" is enough
  for this course.
- **PEP 257, Docstring Conventions.** <https://peps.python.org/pep-0257/>.
  How to write the docstrings that serve as specifications.
- **Karpathy, A. (2025).** The post that introduced the term "vibe coding",
  2 February 2025, on X.
- **Tea data leaks.** *TechCrunch* and *CNN*, 26 July 2025, and the reporting
  of *404 Media* on the second leak of private messages. Motivating example A.
- **Antigravity deletes a drive.** *TechRadar*, December 2025, and the AI
  Incident Database, report 7050, with the developer's post on Reddit.
  Motivating example B.
- **Replit deletes a production database.** *Fortune*, 23 July 2025, and the
  AI Incident Database. Motivating example C.
