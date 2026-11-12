"""Why it matters, session 2: Information Coding."""

TITLE = "The numbers your computer cannot store"
HOOK = ("Rounding errors that add up to a wrong variance, an integer that silently "
        "turns negative, and a name that becomes two names because of one byte.")

CELLS = [
("md", r"""# The numbers your computer cannot store

Every number and every character in your data is a pattern of bits, and the
lecture explained the agreements behind those patterns: two's complement for
integers, IEEE 754 for real numbers, UTF-8 for text. This notebook shows what
happens in ordinary data work when those agreements are ignored. Three small
experiments: rounding errors that accumulate, an integer that overflows without
a word of warning, and a text file read with the wrong encoding."""),

("md", r"""## 1. Rounding errors add up

$0.1$ has no finite binary expansion, so the computer stores a number that is
very slightly off. One such error is harmless. A million of them are not. We
add $0.1$ a million times, once in the usual way and once with `math.fsum`,
which keeps track of the lost digits."""),

("code", r"""import math

total = 0.0
for _ in range(1_000_000):
    total += 0.1
print("plain loop:", total)
print("math.fsum: ", math.fsum([0.1] * 1_000_000))
print("error of the loop:", total - 100_000)"""),

("md", r"""The loop is off by about $10^{-6}$. That is tiny, and it is the mechanism of
the Patriot missile failure described in the lecture: a clock that counts
tenths of a second in 24-bit arithmetic drifts a little with every tick. We
can watch that happen with 32-bit floats, which have 24 significant bits, by
adding 0.1 for every tenth of a second of 100 hours of operation."""),

("code", r"""import numpy as np
import matplotlib.pyplot as plt

ticks = 100 * 3600 * 10                               # tenths of a second in 100 hours
clock = np.cumsum(np.full(ticks, 0.1, dtype=np.float32))   # the clock, tick by tick
true_time = np.arange(1, ticks + 1) / 10
drift = clock - true_time

plt.plot(true_time / 3600, drift)
plt.xlabel("hours of operation"); plt.ylabel("clock error in seconds")
plt.title("A 32-bit clock that adds 0.1 s per tick")
plt.show()
print(f"error after 100 hours: {drift[-1]:.3f} s")"""),

("md", r"""The clock ends more than three hours wrong. With 24 significant bits, once
the count passes 32 768 seconds the representable numbers are spaced 0.004 or
more apart, so "add 0.1" becomes "add the nearest representable step", which
is too much (0.1015625) up to 131 072 seconds and too little (0.09375) beyond
it. Nothing ever brings the clock back. The Patriot's fixed-point clock lost only a
third of a second in 100 hours, and a missile at 1.7 km/s moves half a
kilometer in that time.

The same mechanism hides in a formula you may use every week. The variance can
be computed in one pass as the mean of the squares minus the square of the mean.
On paper that is exact. In floating point it subtracts two huge, nearly equal
numbers, and the digits that survive are the ones that were already wrong. Here
the data are Unix timestamps (about $1.7 \cdot 10^9$ seconds) of events that
happened within a couple of seconds of each other, so the true variance is
about 1."""),

("code", r"""rng = np.random.default_rng(1)
timestamps = 1_700_000_000 + rng.normal(0, 1.0, size=10_000)   # seconds since 1970

naive = np.mean(timestamps ** 2) - np.mean(timestamps) ** 2       # one pass
two_pass = np.mean((timestamps - np.mean(timestamps)) ** 2)      # subtract the mean first
print("one-pass formula:", naive)
print("two-pass formula:", two_pass)
print("numpy.var:       ", np.var(timestamps))"""),

("md", r"""The one-pass formula returns exactly 0: the spread of the data lived in
digits that a 64-bit float does not have once the numbers are squared, and
with another seed the same formula comes out negative, which a variance cannot
be. The two-pass formula and `numpy.var` agree. The values are ordinary: timestamps, account
balances in cents and population counts all have this shape, a large mean with
small variation around it. Subtract the mean before you square."""),

("md", r"""## 2. An integer that becomes negative

Python integers grow without bound, but the arrays of NumPy and pandas store
numbers in fixed-width types, exactly the `byte`, `short`, `int` and `long` of
the lecture's table. A 32-bit integer stops at $2^{31} - 1 = 2\,147\,483\,647$.
Timestamps in seconds fit, but converting them to milliseconds does not, and
NumPy does not stop to tell you."""),

("code", r"""seconds = np.array([1_700_000_000, 1_700_000_001], dtype=np.int32)   # seconds since 1970
millis = seconds * 1000                                                # still int32
print("as int32:     ", millis)
print("Python ints:  ", [int(s) * 1000 for s in seconds])
print("as int64:     ", seconds.astype(np.int64) * 1000)"""),

("md", r"""The products wrap around and land on large negative numbers, without an error
and without a warning, because the operation is done element by element in
32-bit two's complement. Anything you compute from that column afterwards is
quietly wrong. Check the `dtype` of a column when its values are near a power of
two, and convert to a wider type before you multiply."""),

("md", r"""## 3. One byte, two names

Text is bits too, and the map from characters to bytes is not unique. `ß` and
`ü` are one byte each in Latin-1 (ISO-8859-1) and two bytes each in UTF-8, so
the same file means different things under the two encodings."""),

("code", r"""for ch in "ß", "ü", "a":
    print(f"{ch}: UTF-8 {ch.encode('utf-8').hex(' ')!s:8}  Latin-1 {ch.encode('latin-1').hex(' ')}")"""),

("md", r"""Now the everyday version of the problem. A colleague saves a survey as a
UTF-8 file, which is what nearly every program does today. We read it with
`encoding="latin-1"`, which is what many older tools and some spreadsheets
still assume."""),

("code", r"""import io
import pandas as pd

csv_bytes = "name,age\nMüller,34\nMueller,41\nMüller,29\nGroß,52\n".encode("utf-8")

right = pd.read_csv(io.BytesIO(csv_bytes), encoding="utf-8")
wrong = pd.read_csv(io.BytesIO(csv_bytes), encoding="latin-1")
print(wrong)
print("\nrows named Müller:", (right["name"] == "Müller").sum(), "read correctly,",
      (wrong["name"] == "Müller").sum(), "with the wrong encoding")
print("mean age of the Müllers:", right.loc[right["name"] == "Müller", "age"].mean(),
      " and with the wrong encoding:", wrong.loc[wrong["name"] == "Müller", "age"].mean())"""),

("md", r"""Each two-byte UTF-8 character has become two Latin-1 characters: `Ã¼` for
`ü`, and for `ß` an `Ã` followed by an invisible control character. Nothing
crashed. The file still has the right number of
rows and columns; only every name with a non-ASCII letter is now a different
string, so a group of respondents disappears from every filter and every group
mean that names it. The fix is one argument, `encoding="utf-8"`, but you have
to know that the question exists.

**What we used:** [floating-point numbers](https://dgarcia-eu.github.io/ICSS/Transcripts/02-InformationCoding.html#floating-point-numbers-ieee-754),
[when rounding errors matter](https://dgarcia-eu.github.io/ICSS/Transcripts/02-InformationCoding.html#rounding-errors),
[data types](https://dgarcia-eu.github.io/ICSS/Transcripts/02-InformationCoding.html#data-types) and
[character coding](https://dgarcia-eu.github.io/ICSS/Transcripts/02-InformationCoding.html#character-coding) from session 2."""),
]
