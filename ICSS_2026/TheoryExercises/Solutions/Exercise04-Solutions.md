# Solutions to Exercise Sheet 4: Software

*Introduction to Computing for the Social Sciences · Prof. Dr. David Garcia*

> Solutions to [Exercise Sheet 4](../Exercise04.md). Each solution
> starts with where the material is in the slides and in the handout (the
> lecture transcript). Slide numbers count the title slide as 1 and refer to
> `Slides/04-Software/ICSS-2026-04-Software.qmd`.

---

**Where to look, for all four exercises.** The process: slides 21 to 23 (*From a script to software*, *A typical software engineering flow*, *Vibe coding in the flow*); handout [04 §5 Software engineering](../../Transcripts/04-Software.md#5-software-engineering). Requirements, specifications and design: slides 25 to 32; handout [04 §6](../../Transcripts/04-Software.md#6-requirements-specifications-and-design). Tests: slides 34 to 38 (*What is a test?* to *Test first, then generate*); handout [04 §7 Testing](../../Transcripts/04-Software.md#7-testing). Data structures: session 3, handout [03 §9 Dictionaries](../../Transcripts/03-DataStructures.md#9-dictionaries) and the stacks and queues of [03 §3](../../Transcripts/03-DataStructures.md#3-linked-lists).

These are model answers. Other choices are just as good if they are written
down and the tests follow from them; the questions to the client are the part
that matters most, because each one is a decision that would otherwise be
made silently, by you or by a language model.

## Exercise 1: Counting the answers to a survey question

**a) Requirements.**

Functional:

1. The result gives, for each of the four options, the number of respondents
   who chose it, also when that number is 0.
2. Skipped questions (`None`) are counted separately, as "no answer", and not
   as one of the options.
3. Answers that differ only in upper and lower case or surrounding spaces
   count as the same option: `"Bus"` and `" bus"` are `"bus"`.
4. Any other answer, such as `"train"` or a typo, is counted as "invalid",
   so that all answers are accounted for and the counts add up to the number
   of respondents.

Non-functional: the list of answers is not modified (safety); the result
contains only counts, nothing that identifies a respondent (privacy); the
options always appear in the same order, so that two runs can be compared
(reproducibility).

Questions to the client, with the assumed answer:

| Question | Assumed answer |
|---|---|
| Are the answers always written exactly as the options? | No; compare ignoring case and spaces. |
| What should happen with answers that are not one of the options? | Count them as "invalid" and show the count. |
| Should skipped questions appear in the result? | Yes, as "no answer". |
| Counts or percentages? | Counts; percentages are one division away. |
| In which order should the options appear? | In the order of the questionnaire. |

**b) Specification.**

```python
def count_answers(answers, options=("car", "bus", "bike", "walk")):
    """Count how many respondents chose each option.

    answers: a list; each element is a string or None (question skipped).
             Strings are compared ignoring upper/lower case and surrounding spaces.
    options: the valid options, in the order in which they are reported.
    Returns: a dict with one key per option, in the order of options, followed by
             the keys "no answer" (for None) and "invalid" (for any other string).
             Every key is present, with 0 if no answer falls into it, and the
             counts add up to len(answers).
    The list is not modified. An empty list gives 0 for every key.
    """
```

**c) Design.**

- `normalize(answer)` returns the answer in lower case without surrounding
  spaces, or `None` for a skipped question.
- `count_answers(answers, options)` creates a dictionary with every key set
  to 0, then adds 1 to the right key for each normalized answer.
- `report(counts)` prints one line per key, in order.

A **dictionary** from option to count connects them: each answer is a lookup
by key, and the keys can be created in questionnaire order before counting, so
options nobody chose still appear. A set of the valid options makes the check
"is this answer an option?" a constant-time lookup, although with four options
a tuple is just as good.

**d) Tests.**

```python
def test_typical():
    assert count_answers(["bus", "bike", "bus"]) == \
        {"car": 0, "bus": 2, "bike": 1, "walk": 0, "no answer": 0, "invalid": 0}

def test_case_and_spaces_are_ignored():
    counts = count_answers(["Bus", " bike "])
    assert counts["bus"] == 1 and counts["bike"] == 1

def test_missing_and_invalid():
    counts = count_answers([None, "train", "car"])
    assert counts["no answer"] == 1 and counts["invalid"] == 1 and counts["car"] == 1

def test_empty():
    assert all(n == 0 for n in count_answers([]).values())

def test_counts_add_up():
    answers = ["bus", "Bus", None, "car", "x"]
    assert sum(count_answers(answers).values()) == len(answers)

def test_input_is_not_modified():
    answers = ["Bus", None]
    count_answers(answers)
    assert answers == ["Bus", None]
```

The example from the client's message, `["bus", "bike", None, "car", "bus",
"Bus"]`, gives bus 3, bike 1, car 1, walk 0, no answer 1, invalid 0. The
version a language model writes from the one-line request typically gives bus
2 and a separate key `"Bus"` with 1, and fails on `None` or counts it as a
key: both are caught by the second and third tests.

## Exercise 2: The seminar waiting list

**a) Requirements.**

Functional:

1. The first 20 students who register get a place, in the order in which they
   register.
2. Everyone after that goes to the end of the waiting list.
3. When a student with a place drops out, the first student on the waiting
   list gets the place.
4. A student on the waiting list can also drop out; the others keep their
   order.
5. A student ID can be registered only once, either with a place or on the
   waiting list.
6. Dropping an ID that is not registered is reported as an error and changes
   nothing.

Non-functional: first come, first served is strictly kept, since the
waiting list is a question of fairness and students will complain about any
exception; the list of registrations is never lost when the program stops, for
example by saving it after every change (safety); a list shown to the students
contains only IDs, no names (privacy).

Questions to the client, with the assumed answer:

| Question | Assumed answer |
|---|---|
| What if someone registers twice? | The second registration is refused; their position does not change. |
| Can someone on the waiting list drop out? | Yes. |
| Is the number of places always 20? | For this seminar; the program takes it as a parameter. |
| Does someone who moves up have to confirm the place? | No, they get it directly. |
| Who sees the lists? | The instructor sees everything; students see only IDs. |

**b) Specification.** The state of the seminar is kept in one dictionary,
`seminar = {"capacity": 20, "places": [], "waiting": deque()}`, which both
functions receive.

```python
def register(seminar, student_id):
    """Register a student for the seminar.

    seminar: a dict with "capacity" (int), "places" (list of IDs, in order of
             registration) and "waiting" (deque of IDs, first in line first).
    student_id: a string.
    Result: if fewer than capacity students have a place, student_id is added to
            the end of "places" and "place" is returned; otherwise it is added to
            the end of "waiting" and "waiting" is returned.
    Raises: ValueError if student_id is already in "places" or "waiting";
            nothing is changed in that case.
    Never: more than capacity IDs in "places"; an ID twice in the seminar.
    """

def drop(seminar, student_id):
    """Remove a student from the seminar.

    seminar: as for register; student_id: a string.
    Result: if student_id has a place, it is removed, and the first ID of
            "waiting", if any, is moved to the end of "places". If student_id is
            on the waiting list, it is removed and the order of the others is kept.
    Raises: ValueError if student_id is not registered; nothing is changed.
    """
```

**c) Design.**

- `new_seminar(capacity)` returns the empty dictionary described above.
- `register(seminar, student_id)` and `drop(seminar, student_id)` as
  specified.
- `show(seminar)` prints the places and the waiting list, in order.

The places are a **list**, since their order (order of registration) is kept
and there are at most 20. The waiting list is a **queue** (`collections.deque`),
because it is first in, first out: new students join at the end, the student
who moves up leaves from the front. A stack would give the place to the most
recent student, the unfair outcome of serving the newest request first. With hundreds of registrations a **set** of all registered IDs
would make the duplicate check fast; with a seminar, searching the list and the
queue is fine. Making the capacity a parameter is a design decision for the
tests: they can use a seminar with 2 places instead of 20.

**d) Tests.**

```python
def test_first_come_get_places():
    s = new_seminar(2)
    assert [register(s, x) for x in ["a", "b", "c"]] == ["place", "place", "waiting"]
    assert s["places"] == ["a", "b"] and list(s["waiting"]) == ["c"]

def test_first_on_waiting_list_moves_up():
    s = new_seminar(2)
    for x in ["a", "b", "c", "d"]:
        register(s, x)
    drop(s, "a")
    assert s["places"] == ["b", "c"] and list(s["waiting"]) == ["d"]

def test_drop_from_waiting_list_keeps_order():
    s = new_seminar(1)
    for x in ["a", "b", "c", "d"]:
        register(s, x)
    drop(s, "c")
    assert s["places"] == ["a"] and list(s["waiting"]) == ["b", "d"]

def test_register_twice_is_refused():
    s = new_seminar(2)
    register(s, "a")
    with pytest.raises(ValueError):
        register(s, "a")
    assert s["places"] == ["a"] and list(s["waiting"]) == []

def test_drop_unknown_is_refused():
    s = new_seminar(2)
    with pytest.raises(ValueError):
        drop(s, "z")

def test_never_more_places_than_capacity():
    s = new_seminar(2)
    for x in "abcdefg":
        register(s, x)
    assert len(s["places"]) == 2
```

## Exercise 3: Who took part in both waves?

**a) Requirements.**

Functional:

1. The result is the list of respondent IDs that appear in both waves, sorted.
2. The number of respondents in both waves is reported.
3. An ID that appears twice in the same wave is counted once.
4. IDs are compared exactly as written; `"007"` and `"7"` are different IDs.

Non-functional: the email addresses are not needed for this task, so the
result, and any file written from it, contains **no email addresses**
(privacy). This is the requirement that the client did not state and would
certainly agree with: the emails are personal data, and a list of panel
participants with their email addresses is exactly the kind of file that
should never be shared by accident. The two input files are never modified
(safety).

Questions to the client, with the assumed answer:

| Question | Assumed answer |
|---|---|
| Are IDs numbers or text, and can they have leading zeros? | Text; leading zeros are kept. |
| What about someone who submitted a wave twice? | They count once. |
| Should we also match on email, for people who got a new ID? | No; match on ID only, and report the question back. |
| Sorted how? | As text, which for IDs of equal length is numeric order. |
| Is the list of IDs shared with anyone else? | Assume it may be, so it contains IDs only. |

**b) Specification.**

```python
def in_both_waves(wave1, wave2):
    """Return the respondents who took part in both waves.

    wave1, wave2: lists of pairs (respondent_id, email); respondent_id is a
                  string. The same ID may appear more than once in a list.
    Returns: a sorted list of the distinct IDs that appear in both lists; the
             number of respondents in both waves is its length.
    The result contains no email addresses. The input lists are not modified.
    """
```

**c) Design.**

- `ids(wave)` returns the **set** of IDs in a wave; this is the step that
  drops the email addresses and removes duplicates.
- `in_both_waves(wave1, wave2)` returns `sorted(ids(wave1) & ids(wave2))`.
- `report(ids_in_both)` prints the count and writes the IDs to a file.

A set is the right structure because the task is membership: "is this ID also
in the other wave?". With $n$ respondents per wave, the intersection of two
sets takes time proportional to $n$, while checking every ID of one list
against the other list takes time proportional to $n^2$, the difference timed
in the WhyItMatters notebook of session 3. The result is a list, since it has
to be sorted. Dropping the emails in the very first function means that no
later part of the program can leak them.

**d) Tests.**

```python
W1 = [("001", "a@x.de"), ("002", "b@x.de"), ("003", "c@x.de")]
W2 = [("003", "c@x.de"), ("001", "a@y.de"), ("004", "d@x.de")]

def test_typical():
    assert in_both_waves(W1, W2) == ["001", "003"]

def test_duplicates_count_once():
    assert in_both_waves(W1 + [("001", "a@x.de")], W2) == ["001", "003"]

def test_nobody_in_both():
    assert in_both_waves([("001", "a@x.de")], [("002", "b@x.de")]) == []

def test_empty_wave():
    assert in_both_waves([], W2) == []

def test_leading_zeros_are_kept():
    assert in_both_waves([("007", "a@x.de")], [("7", "a@x.de")]) == []

def test_no_email_in_result():
    assert all("@" not in x for x in in_both_waves(W1, W2))
```

## Exercise 4: Grades from exercise points

**a) Requirements.**

Functional:

1. For every student in the table, the result gives the total points and
   whether they passed.
2. A sheet that was not handed in (`None`) counts as 0 points.
3. A student passes if the total is at least half of the points possible; a
   total of exactly 50% passes ("at least").
4. Points outside 0 to 10 are an error in the table and are reported, not
   silently used.

Non-functional: the table that the teaching assistants keep updating is only
read, never written (safety); the grades of all students are seen only by the
instructor (security and privacy); the same table gives the same result
(reproducibility).

The central question is what "50% of the points" means while the course is
still running. Possible answers: 50% of all 120 points of the course, which
nobody passes before the end of the semester; or 50% of the points of the
sheets graded so far, which lets the instructor see who is at risk during the
semester. The solution below takes the second, because the table "keeps being
updated", and states it in the specification so the client can disagree.

| Question | Assumed answer |
|---|---|
| 50% of all 12 sheets, or of the sheets graded so far? | Of the sheets graded so far: 10 points times the number of entries. |
| Does exactly 50% pass? | Yes. |
| Do missing sheets count as 0, or are they left out? | As 0. |
| Can there be half points? | Yes; points are numbers from 0 to 10. |
| What if two students have lists of different length? | That is an error in the table and is reported. |

**b) Specification.**

```python
def exercise_results(points):
    """Return the total points and the pass decision of every student.

    points: a dict from student ID (str) to a list of points, one entry per
            sheet graded so far, all lists of the same length; each entry is a
            number from 0 to 10, or None for a sheet not handed in.
    Returns: a dict from student ID to a pair (total, passed): total is the sum
             of the points, with None counting as 0; passed is True if total is
             at least half of 10 times the number of entries.
    Raises: ValueError if an entry is outside 0 to 10, or if the lists differ in
            length.
    The dict and its lists are not modified. An empty dict gives {}.
    """
```

**c) Design.**

- `read_table(path)` reads the file into the dictionary above; it opens the
  file only for reading.
- `total(sheet_points)` returns the sum of one student's points, with `None`
  as 0, and raises `ValueError` for an entry outside 0 to 10.
- `passed(total_points, n_sheets)` returns whether `total_points` is at least
  half of `10 * n_sheets`.
- `exercise_results(points)` checks the lengths and builds the result with
  the two functions above.

A **dictionary** from student ID to a **list** of points: the instructor looks
students up by ID, and each student's points keep the order of the sheets. The
result is again a dictionary keyed by student ID. Keeping `passed` as its own
function puts the pass rule in one place, which is the line the client is most
likely to change.

**d) Tests.**

```python
def test_typical_pass_and_fail():
    r = exercise_results({"A": [10, 8, 7], "B": [2, 3, 4]})
    assert r == {"A": (25, True), "B": (9, False)}

def test_exactly_half_passes():
    assert exercise_results({"A": [5, 5]}) == {"A": (10, True)}

def test_just_below_half_fails():
    assert exercise_results({"A": [5, 4.5]}) == {"A": (9.5, False)}

def test_missing_sheet_counts_as_zero():
    assert exercise_results({"A": [10, None]}) == {"A": (10, True)}

def test_points_out_of_range_raise():
    with pytest.raises(ValueError):
        exercise_results({"A": [11, 5]})

def test_lists_of_different_length_raise():
    with pytest.raises(ValueError):
        exercise_results({"A": [10, 10], "B": [10]})

def test_empty():
    assert exercise_results({}) == {}

def test_input_is_not_modified():
    points = {"A": [10, None]}
    exercise_results(points)
    assert points == {"A": [10, None]}
```

The boundary tests, exactly half and just below, are where an implementation
most often goes wrong: writing `>` instead of `>=` fails the second test, and
leaving `None` out of the count of sheets would let a student pass with half
the points of only the sheets they handed in.

## Additional practice

### A1. Functional or non-functional?

**Where to look.** Slide 26 (*Functional and non-functional requirements*). Handout: [04 §6](../../Transcripts/04-Software.md#6-requirements-specifications-and-design).

a) functional. b) non-functional, performance. c) non-functional, privacy.
d) functional: it says what output (an error) the program gives for an input.
e) non-functional, safety. f) non-functional, reproducibility.
g) non-functional, security.

### A2. The questions a model will not ask

**Where to look.** Slides 28 to 30 (*An ambiguous request*, *Writing the specification*, *The specification is your prompt*).

Open questions: in which format are the birth dates written (`"1990-03-05"`,
`"05.03.1990"`, or date objects)? Age at which date: today, or the date of the
interview? Age in completed years, or with decimals? What happens with a
missing birth date? What with an impossible one, in the future or giving an
age over 120? Is the data modified, or is a new list returned?

A rewritten prompt: *"Write `ages(birth_dates, interview_dates)`. Both are
lists of strings `"DD.MM.YYYY"` of the same length. Return a list of ints: the
age in completed years on the interview date. Return None for a missing birth
date and raise ValueError for a birth date after the interview date. Do not
modify the input lists; use only the standard library."*

### A3. Which test is missing?

**Where to look.** Slides 34 to 37 (*What is a test?* to *Choosing test cases*).

Not tested: that `None` answers are ignored, that the `ValueError` is raised,
and that the list is not modified. Missing tests:

```python
def test_missing_answers_are_ignored():
    assert share_yes(["yes", None, "no", None]) == 0.5

def test_no_valid_answer_raises():
    with pytest.raises(ValueError):
        share_yes([None, None])

def test_input_is_not_modified():
    answers = ["yes", None]
    share_yes(answers)
    assert answers == ["yes", None]
```

A wrong implementation that passes the two given tests:
`return answers.count("yes") / len(answers)`. It gives 0.75 and 1.0 on the
given cases, but 0.25 instead of 0.5 on the first missing test, because it
divides by all answers including `None`; it returns 0.0 instead of raising
`ValueError` for `[None, None]`, and raises `ZeroDivisionError` for `[]`. Two passing tests said nothing about
the lines of the specification they did not cover.

### A4. Choosing a data structure

**Where to look.** Slide 32 (*Design: choosing the data structures*); session 3.

a) A list: the order of the questions matters. b) A dictionary from code to
label: lookup by key. c) A set: the only question is membership, and a set
answers it in constant time. d) A queue: first in, first out. e) A stack: last
in, first out, so the most recent step is undone first.

### A5. Compilers, interpreters and research code

**Where to look.** Slides 9 and 10 (*Levels of programming languages*, *Interpreter vs. compiler*). Handout: [04 §1 What programming is](../../Transcripts/04-Software.md#1-what-programming-is).

a) (i) The 50× may be irrelevant if the bottleneck is reading data, or if the
slow part already runs in a compiled library like NumPy: you would rewrite the
part that is already fast. (ii) Your time is a cost: six hours of computer
time once is cheaper than two weeks of your time plus a new class of bugs, and
the C version would need its own tests. Measure first which part is slow,
then improve that part (session 8).

b) An interpreter translates each line only when it runs, so an error in a
branch that never runs, say the `else` for a rare answer code, is never
reported. Test cases should therefore make every branch run at least once:
the rare codes, the missing values, the empty input.

### A6. Rules that do not belong in a prompt

**Where to look.** Slides 23 and 30 (*Vibe coding in the flow*, *The specification is your prompt*); motivating examples on slides 5 and 6.

a) and c) can go in the prompt. They are wishes about the code, and you can
check them by reading the code or with a test; if the model ignores them, the
result is inconvenient, not harmful. b) and d) must be enforced by the system,
because breaking them once does damage that cannot be undone. b): run the
agent with permission to change only the project folder, ask for confirmation
before any delete command, and keep backups. d): give the agent no access to
the production database at all, with separate development and production
data, which is what Replit did after its agent deleted a production database
during a code freeze.
