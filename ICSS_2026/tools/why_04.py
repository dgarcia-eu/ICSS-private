"""Why it matters, session 4: Software."""

TITLE = "Hundred times slower, quietly wrong, and fixed by its tests"
HOOK = ("A Python loop against compiled NumPy, a wrong mean that a one-line test catches, "
        "and a generated function whose silent error is corrected because a test suite "
        "tells the language model what is wrong.")

CELLS = [
("md", r"""# Hundred times slower, quietly wrong, and fixed by its tests

The lecture went from what a program is to how software is specified and
tested. This notebook shows three practical sides of that: the same
computation at two levels of language, a function that returns a wrong number
until a test asks it a question it cannot dodge, and a vibe-coded function
whose silent error is found and corrected because a test suite was written
first."""),

("md", r"""## 1. Interpreted loop, compiled library

Python is interpreted: every iteration of a loop is translated as it runs.
NumPy is written in C and compiled: `np.sum` runs one machine-code loop with no
interpreter in between. We compute the same sum of squares of ten million
numbers both ways."""),

("code", r"""import time
import numpy as np

x = np.random.default_rng(4).normal(size=10_000_000)

t0 = time.perf_counter()
total = 0.0
for value in x:                     # interpreted: Python executes each step
    total += value * value
t_loop = time.perf_counter() - t0

t0 = time.perf_counter()
total_np = np.sum(x * x)            # compiled: one call into C
t_np = time.perf_counter() - t0

print(f"loop  {t_loop:6.2f} s   result {total:.4f}")
print(f"numpy {t_np:6.4f} s   result {total_np:.4f}")
print(f"ratio {t_loop / t_np:.0f}x")"""),

("md", r"""The results agree to many digits and the loop is on the order of a hundred
times slower. Nothing about Python is wrong; the loop pays the price of being
interpreted ten million times, and the library pays it once. This is why data
code in Python leans on NumPy and pandas, and why the choice between "a loop
over rows" and "an operation on a column" is the choice between the two levels
of language of the lecture.

## 2. A bug that only a test can see

A function to compute the mean age of respondents, skipping the ones who did
not answer. It runs, it returns a plausible number, and it is wrong."""),

("code", r"""def mean_age(ages):
    total = 0
    for age in ages:
        if age is not None:
            total += age
    return total / len(ages)          # divides by all respondents, including the missing ones

print(mean_age([30, 40, None, 50]))"""),

("md", r"""The answer, 30, is a valid age, so nothing looks wrong on a dataset of ten
thousand rows. A test is a tiny input whose correct answer you know. Here it
is one line."""),

("code", r"""try:
    assert mean_age([30, 40, None, 50]) == 40, "missing answers must not count in the denominator"
except AssertionError as e:
    print("AssertionError:", e)"""),

("md", r"""The assertion fails and names the problem (we catch it here so that the
notebook keeps running; in a script it would stop right there, which is the
point). The fix is to count the answers that were used."""),

("code", r"""def mean_age(ages):
    total, count = 0, 0
    for age in ages:
        if age is not None:
            total += age
            count += 1
    return total / count

assert mean_age([30, 40, None, 50]) == 40
assert mean_age([25]) == 25
print("all tests pass")"""),

("md", r"""This is the lecture's advice in one line: a bug that does not crash is found
by a check you wrote, not by the interpreter.

## 3. Vibe coding with a test suite

Now the same lesson with a language model writing the code. Our survey was
run in Germany, so the interview dates are written day first: `05/03/2024` is
the 5th of March. We ask for a function that counts the interviews per month,
and we accept the first answer without reading it, as vibe coding does."""),

("code", r"""from collections import Counter
from datetime import datetime

interview_dates = ["04/03/2024", "05/03/2024", "05/03/2024", "11/03/2024",
                   "02/04/2024", "08/04/2024", "09/04/2024", "12/04/2024"]

# Generated for the prompt "write a function that counts the interviews per month"
def interviews_per_month(dates):
    months = Counter()
    for d in dates:
        months[datetime.strptime(d, "%m/%d/%Y").strftime("%Y-%m")] += 1
    return dict(sorted(months.items()))

interviews_per_month(interview_dates)"""),

("md", r"""No error, and a tidy table. It is also wrong: the format `"%m/%d/%Y"` reads
the month first, the convention in the United States, so `05/03/2024` became
the 3rd of May. Our fieldwork ran in March and April, and the table spreads it
over seven months. Because every day in these dates is 12 or less, every date
is also a valid date month first, and nothing crashes. Here someone might
notice that November looks odd; with a slightly different question, say the
mean number of days between interviews, there would be nothing odd to notice
at all.

The lecture's order of work is to write the specification and the tests before
asking for code. Here is the specification, four tests written from it, and a
small helper that runs them and reports failures the way `pytest` does, so
that the notebook runs anywhere."""),

("code", r"""SPEC = '''interviews_per_month(dates)
dates: a list of strings "DD/MM/YYYY", day first (German convention).
Returns: a dict from "YYYY-MM" to the number of interviews in that month,
         sorted by month; months without interviews do not appear.
An empty list gives {}. The list itself is not modified.'''

def test_day_comes_first():
    got = interviews_per_month(["05/03/2024"])
    assert got == {"2024-03": 1}, f"got {got}"

def test_counts_per_month():
    got = interviews_per_month(["04/03/2024", "11/03/2024", "02/04/2024"])
    assert got == {"2024-03": 2, "2024-04": 1}, f"got {got}"

def test_day_after_the_12th():
    got = interviews_per_month(["25/03/2024"])
    assert got == {"2024-03": 1}, f"got {got}"

def test_empty():
    got = interviews_per_month([])
    assert got == {}, f"got {got}"

TESTS = [test_day_comes_first, test_counts_per_month, test_day_after_the_12th, test_empty]

def run_tests(tests):
    report = []
    for t in tests:
        try:
            t()
        except Exception as e:
            report.append(f"FAILED {t.__name__}: {type(e).__name__} {e}")
    print("\n".join(report) or "all tests pass")
    print(f"{len(tests) - len(report)} passed, {len(report)} failed")
    return "\n".join(report)

failures = run_tests(TESTS)"""),

("md", r"""Three of the four tests fail, and each failure is specific: the 5th of March
was not counted in March, and `25/03/2024` is not even a valid date for this
function. This is where a test suite changes what working with a language
model is like. Instead of "it seems wrong somehow", we can give the model the
specification and the exact failures."""),

("code", r"""prompt = ("Here is the specification of interviews_per_month:\n" + SPEC +
          "\n\nYour implementation fails these tests:\n" + failures +
          "\n\nCorrect the function.")
print(prompt)"""),

("md", r"""Given this prompt, a language model answers with a corrected function. We
write its answer here rather than calling a model, so that the notebook runs
offline and gives the same result every time; the correction is a single
format string."""),

("code", r"""# The model's corrected version: the day comes first in the format
def interviews_per_month(dates):
    months = Counter()
    for d in dates:
        months[datetime.strptime(d, "%d/%m/%Y").strftime("%Y-%m")] += 1
    return dict(sorted(months.items()))

run_tests(TESTS)
interviews_per_month(interview_dates)"""),

("md", r"""All tests pass, and the fieldwork is back in March and April. Nothing in the
first version would have told us it was wrong; the tests did, and they also
told the model what to fix. Writing them took a few minutes and needed only
the specification, not the code. That is the division of labor of the
lecture: a language model can write the implementation, and the
specification and the tests remain your job.

**What we used:** [interpreters and compilers](../Transcripts/04-Software.md#1-what-programming-is),
[vibe coding](../Transcripts/04-Software.md#5-software-engineering),
[specifications](../Transcripts/04-Software.md#6-requirements-specifications-and-design) and
[testing](../Transcripts/04-Software.md#7-testing) from session 4."""),
]
