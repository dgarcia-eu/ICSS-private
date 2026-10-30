# Exercise Sheet 4: Software

*Introduction to Computing for the Social Sciences · Prof. Dr. David Garcia*

> Exercises 1 and 2 are worked through in the exercise session; Exercises 3 and
> 4 follow the same steps and are for self-study, as is the *Additional
> practice* section. Worked solutions to every exercise, with pointers to the
> slides and the handout sections that cover the material, are in
> [`Solutions/Exercise04-Solutions.md`](Solutions/Exercise04-Solutions.md); try before you open them.
> Notation: [course conventions](../Transcripts/00-Conventions.md).

---

## How to work on these exercises

Each exercise is a small request from a client, the kind of message a
colleague might send you. You do not write the program. You do the four steps
of the software engineering process that remain yours when a language model
can write the code:

a) **Requirements.** Write down what the software must achieve: at least
   three functional requirements and at least one non-functional requirement.
   List the questions you would ask the client before starting, and for each,
   the answer you will assume if the client is not available.

b) **Specification.** Write the specification of the main function as a
   docstring: inputs and what may be assumed about them, the result, what
   happens in edge cases and errors, and what the function must never do.

c) **Design.** Split the work into two to four small functions, with one line
   each on what it does, and say which data structure from session 3 (list,
   dictionary, set, queue, stack) connects them, and why.

d) **Tests.** Write at least four test cases for the main function: a
   typical case, a boundary or empty case, a case with missing or invalid
   data, and a case for something that must never happen. Write each as a
   pytest test, or as a table with input and expected result.

Keep the design simple: these are programs of 20 to 40 lines. There is more
than one good answer to every step; what matters is that each choice is
written down and that the tests follow from the specification.

---

## Exercise 1: Counting the answers to a survey question

> *"Hi! Our survey has a question about how people get to work, with the
> options 'car', 'bus', 'bike' and 'walk'. Could you write something that tells
> me how many people chose each option? I'll send you the answers as a list.
> Thanks, Lea"*

The answers arrive as a Python list, for example
`["bus", "bike", None, "car", "bus", "Bus"]`, with `None` where a respondent
skipped the question.

Work through steps a) to d). In step a), think in particular about the last
two entries of the example list.

---

## Exercise 2: The seminar waiting list

> *"Our seminar has 20 places and always more people who want in. Could you
> write a small program for the sign-ups? People register with their student
> ID. The first 20 get a place, the others go on a waiting list, and when
> someone drops out, the next person from the waiting list moves up. Best,
> Tom"*

The program must support three operations: register a student ID, drop a
student ID, and show who has a place and who is waiting, in order.

Work through steps a) to d). Write a specification for each of the two
functions `register(student_id)` and `drop(student_id)`, and tests for both. In
step c), say which data structure holds the participants and which holds the
waiting list.

---

## Exercise 3: Who took part in both waves?

> *"We ran our panel survey twice, in spring and in autumn. I have two files of
> respondent IDs, one per wave. I need to know how many people answered both
> times, and the list of their IDs, sorted, so I can merge their answers. The
> files also have the respondents' email addresses, by the way. Cheers, Ana"*

Each file can be read into a list of pairs `(respondent_id, email)`. The same
ID can appear twice in a file if someone submitted the survey twice.

Work through steps a) to d). In step a), decide what the email addresses
have to do with the requirements.

---

## Exercise 4: Grades from exercise points

> *"For my course I have the exercise points of every student: up to 10 points
> for each of the 12 sheets. Students pass the exercise part if they have at
> least 50% of the points. Could you write something that gives me, for every
> student, the total and whether they passed? The points are in a table that
> the teaching assistants keep updating. Thanks, David"*

The table can be read into a dictionary from student ID to a list of points,
for example `{"01/123": [10, 8, None, 7, ...], ...}`, with `None` for a sheet
that was not handed in.

Work through steps a) to d). In step a), think about what "at least 50% of
the points" means when a student has not handed in every sheet, and about the
table that "the teaching assistants keep updating".

---

## Additional practice

### A1. Functional or non-functional?

For each requirement, say whether it is functional or non-functional, and for
the non-functional ones, which kind (security, privacy, safety, performance,
reproducibility).

a) The mean is computed only over the answered questions.
b) The program finishes in under a minute on the full survey of 50,000
   respondents.
c) The output file contains no names or email addresses.
d) An empty input list raises a `ValueError`.
e) The original data file is never overwritten.
f) Running the analysis twice on the same data gives the same result, also on
   a colleague's computer.
g) Only the course instructors can see the grades of all students.

### A2. The questions a model will not ask

A colleague sends a language model the prompt *"write a function that
computes the age of each respondent from their birth date"*. Write five
questions whose answers the prompt leaves open, and rewrite the prompt so that
it answers them.

### A3. Which test is missing?

The specification of `share_yes(answers)` says: *"answers is a list of "yes",
"no" or None. Returns the share of "yes" among the "yes" and "no" answers.
Raises ValueError if there is no "yes" or "no" answer. The list is not
modified."* These are the tests:

```python
def test_typical():
    assert share_yes(["yes", "no", "yes", "yes"]) == 0.75

def test_all_yes():
    assert share_yes(["yes", "yes"]) == 1.0
```

Which lines of the specification are not tested? Write the missing tests.
Then write an implementation that passes both tests above and is still wrong.

### A4. Choosing a data structure

For each task, which data structure belongs in the design, and why?

a) The answers of one respondent, in the order of the questions.
b) A codebook that translates answer codes such as `3` into labels such as
   `"agree"`.
c) The email addresses that have already received an invitation, so that
   nobody is invited twice.
d) Help requests in a chat service, answered in the order they arrived.
e) The steps a user took in an editor, so that "undo" reverses the most
   recent one first.

### A5. Compilers, interpreters and research code

a) You have a Python script that takes 6 hours on your data. A colleague says
   "rewrite it in C, it will be 50 times faster". Give two reasons why that
   may be bad advice.
b) Python is interpreted. Why can an error in a part of the script that your
   test data never reaches stay hidden, and what does that mean for the test
   cases you choose?

### A6. Rules that do not belong in a prompt

For each rule, say whether it is enough to state it in the prompt to a coding
agent, and if not, how the system should enforce it.

a) Use only the standard library.
b) Never delete files outside the project folder.
c) Name the functions in English.
d) Do not change the production database during the code freeze.

---

## Sources

- The exercises are new in 2026/27; the earlier sheet 4 (object-oriented
  programming, debugging, problem-solving) is no longer used.
- **Zelle, J. M. (2016).** *Python Programming: An Introduction to Computer
  Science*, 3rd ed., ch. 2, 6–8: reading for this session.
- **Guttag, J. V. (2016).** *Introduction to Computation and Programming Using
  Python*, 2nd ed., MIT Press, ch. 6 (testing and debugging).
- **pytest documentation.** <https://docs.pytest.org/>
- **PEP 257, Docstring Conventions.** <https://peps.python.org/pep-0257/>
