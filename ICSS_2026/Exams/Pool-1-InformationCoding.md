# Pool 1: Information Coding

*Exam question pool · session 2 · typically **question 1**, 7–11 points.*
See [README](README.md) for the item format and source tags,
[Blueprint](Blueprint.md) for how to assemble a question from these.

Everything here is done **by hand, without a calculator**. Always print the IEEE
754 reminder in the paper: *"remember that this standard has 8 bits for the
exponent and a bias of 127"*.

---

## IC-01 · Convert to octal · 2–3 pts · [2023-Ex Q1a, 2023-E2 Q1a, 2024-E1 Q1a, 2025-E1 Q1a, 2025-E2 Q1a]

> Convert the following numbers to octal notation.
> - $10111101_2$
> - $20_{16}$
> - $687_{10}$

**Solution.**
- $10111101_2$: group in threes from the right: $010\ 111\ 101$ → $\mathbf{275_8}$.
- $20_{16} = 32_{10}$ → $\mathbf{40_8}$.
- $687_{10}$: repeated division by 8: $687 = 85\cdot 8 + 7$, $85 = 10\cdot 8 + 5$,
  $10 = 1\cdot 8 + 2$, $1 = 0\cdot 8 + 1$ → read the remainders upwards →
  $\mathbf{1257_8}$. Check: $512 + 128 + 40 + 7 = 687$. ✓

**Variants used in other years.**

| Source | Numbers | Answers |
|---|---|---|
| 2023-E2 Q1a | $10111101111010111_2$, $20_{16}$, $687_{10}$ | $275727_8$, $40_8$, $1257_8$ |
| 2024-E1 Q1a | $110000100111100011001_2$, $64_{10}$ | $6047431_8$, $100_8$ |
| 2025-E1 Q1a | $\text{B87}_{16}$, *(see erratum)* | $5607_8$ |
| 2025-E2 Q1a | $\text{ABC}_{16}$, $1025_6$ | $5274_8$, $\;1025_6 = 233_{10} = 351_8$ |

> **Erratum.** 2025-E1 Q1a printed the second number as $1012_8$, already
> octal. A base subscript was presumably lost. Use one of the sets above.

**Notes.** The grouping shortcut only works between bases that are powers of the
same number ($2 \leftrightarrow 8 \leftrightarrow 16$). From base 10, or between
base 6 and base 8, students must go through repeated division or through
decimal. Award the method, not only the digits.

---

## IC-02 · Convert to base 32 · 2 pts · [2025-E1 Q1b, 2025-E2 Q1b]

> Convert the following numbers to base 32. Specify the decimal value of each
> symbol you use for your coding.
> - $1011110100000111_2$
> - $611_{16}$

**Solution.** Base 32 is $2^5$, so group binary digits in **fives** from the
right. Symbols: `0`–`9` for 0–9, then `A`=10, `B`=11, …, `V`=31.

- $1011110100000111_2$ → $1\ |\ 01111\ |\ 01000\ |\ 00111$ → digits
  $1, 15, 8, 7$ → $\mathbf{1F87_{32}}$, with `F` = 15.
  Check: $1\cdot 32768 + 15\cdot 1024 + 8\cdot 32 + 7 = 48391 = \text{BD07}_{16}$. ✓
- $611_{16} = 0110\,0001\,0001_2 = 011000010001_2$ → $01\ |\ 10000\ |\ 10001$ →
  digits $1, 16, 17$ → $\mathbf{1GH_{32}}$, with `G` = 16 and `H` = 17.
  Check: $1024 + 512 + 17 = 1553 = 611_{16}$. ✓

**Notes.** The "specify the decimal value of each symbol" clause is the point of
the question: base 32 needs 32 distinct symbols and there is no universal
convention, so the answer is only well defined once the student states theirs.
Accept any consistent alphabet.

---

## IC-03 · Convert to hexadecimal · 2 pts · [2024-E2 Q1a]

> Convert the following numbers to hexadecimal notation.
> - $110000100111100011001_2$
> - $64_{10}$

**Solution.** Group in **fours** from the right, padding on the left:
$0001\ 1000\ 0100\ 1111\ 0001\ 1001$ → $\mathbf{0x184F19}$.
$64_{10} = \mathbf{0x40}$.

---

## IC-04 · IEEE 754 multiplication · 4 pts · [2023-E2 Q1d, 2024-Ex Q1a, 2024-E2 Q1b, 2025-Ex Q1a, 2025-E1 Q1c]

> The following two numbers are encoded in IEEE 754 single-precision
> floating-point standard, shown in hexadecimal notation.
> ```
> 0x40000000
> 0x42400000
> ```
> Multiply the numbers and show the result in the same standard using
> hexadecimal notation. *(Note: remember that this standard has 8 bits for the
> exponent and a bias of 127.)*

**Solution.** Decode both.

`0x40000000` = `0 10000000 00000000000000000000000`
sign $+$, exponent $128 - 127 = 1$, significand $1.0$ → $1.0 \times 2^1 = \mathbf{2.0}$

`0x42400000` = `0 10000100 10000000000000000000000`
sign $+$, exponent $132 - 127 = 5$, significand $1.5$ → $1.5 \times 2^5 = \mathbf{48.0}$

Multiply: significands $1.0 \times 1.5 = 1.5$, exponents $1 + 5 = 6$ →
$1.5 \times 2^6 = 96.0$.

Encode: sign `0`; exponent $6 + 127 = 133 = 10000101_2$; significand fraction
$0.5 = 1000\ldots_2$.

`0 10000101 10000000000000000000000` = `0100 0010 1100 0000 …` = **`0x42C00000`**

**Variant.** 2025-E1 Q1c uses `0x40800000` (= 4.0) and `0x42000000` (= 32.0);
product $128.0 = 1.0 \times 2^7$ → **`0x43000000`**.

**Notes.** Marking: 1 point per decoded operand, 1 for the multiplication rule
(multiply significands, **add** exponents), 1 for re-encoding with the bias
added back. The most common error is adding the *biased* exponents (getting
$128+132$) instead of the unbiased ones.

---

## IC-05 · IEEE 754 addition · 4 pts · [2023-E1 Q1a]

> The following two numbers are encoded in IEEE 754 single-precision
> floating-point standard, shown in hexadecimal notation.
> ```
> 0x41800000
> 0x41F80000
> ```
> Add the numbers and show the result in the same standard using hexadecimal
> notation.

**Solution.**
`0x41800000` → exponent $131-127 = 4$, significand $1.0$ → $16.0$
`0x41F80000` → exponent $131-127 = 4$, significand $1.9375$ → $31.0$
Sum $= 47.0 = 1.46875 \times 2^5$.
Exponent $5 + 127 = 132 = 10000100_2$; fraction $0.46875 = 0111100\ldots_2$.
→ **`0x423C0000`**

**Notes.** Addition is the harder operation to do by hand because the exponents
must be aligned first. Here they already match, which is why this pair was
chosen, a pair with different exponents would not fit in 4 points.

---

## IC-06 · Add 0.125 and check exactness · 2–3 pts · [2023-E1 Q1b, 2024-Ex Q1b, 2024-E2 Q1c, 2025-Ex Q1b]

> Add $0.125_{10}$ to the result of the previous question and show the result in
> IEEE 754 floating-point standard with hexadecimal notation. Is the exact value
> of the result the same as the encoded one?

**Solution** (following `IC-04`, result 96.0):
$96.125 = 1.501953125 \times 2^6$. Exponent $133$; fraction
$0.501953125 \times 2^{23} = 4210688 = \text{0x404000}$.
→ **`0x42C04000`**

**Yes, exact.** $0.125 = 2^{-3}$ is a power of two, so $96.125 = 769/8$ is a
dyadic rational; it needs only 9 significand bits and 23 are available. No
rounding occurs.

**Variants.** After `IC-05` (47.0): $47.125$ → **`0x423C8000`**, exact.
After the `IC-04` variant (128.0): $128.125$ → **`0x43002000`**, exact.

**Notes.** The "is it exact?" half is worth insisting on, because it is the
conceptual point: floats are exact for dyadic rationals and inexact for
everything else. Contrast with `IC-07`, where the answer is *no*.

---

## IC-07 · Decimal to IEEE 754, with rounding direction · 3 pts · [2025-E1 Q1d, 2025-E2 Q1c, 2023-Ex Q1c+d]

> Convert $0.225_{10}$ to IEEE 754 floating-point standard and write it with
> hexadecimal notation. Is the exact value of the result the same, higher, or
> lower than the encoded one?

**Solution.**
$0.225 = 1.8 \times 2^{-3}$. Exponent $-3 + 127 = 124 = 01111100_2$.
Fraction $0.8$ in binary is $0.110011001100\ldots$, infinitely repeating.
$0.8 \times 2^{23} = 6710886.4$, which rounds **down** to $6710886 =
\text{0x666666}$.
→ **`0x3E666666`**

The encoded value is $0.224999994\ldots$, so the **exact value 0.225 is higher
than the encoded one**. There is a loss of precision because $0.225 = 9/40$ and
40 has a factor of 5, so the number is not a dyadic rational and its binary
expansion never terminates.

**Variants.**

| Source | Number | Encoding | Direction |
|---|---|---|---|
| 2025-E2 Q1c | $0.2_{10}$ | `0x3E4CCCCD` | rounds **up**; exact value is **lower** |
| 2023-Ex Q1c | $-42.1_{10}$ | `0xC2286666` | magnitude rounds down; encoded $= -42.099998\ldots$ |

**Notes.** The direction half separates students who converted mechanically from
those who understand rounding. Both directions occur in the pool deliberately,
do not let students learn "the answer is always lower".

---

## IC-08 · Hexadecimal subtraction · 2 pts · [2023-E1 Q1c, 2024-Ex Q1c, 2025-Ex Q1c]

> Which hexadecimal number should you subtract from `0xC0FFEE` to get `0xC0C0A`
> as a result?

**Solution.** $\text{0xC0FFEE} - \text{0x0C0C0A}$. Aligning the second number
(it has one digit fewer) is the whole trick:

```
   C 0 F F E E
 - 0 C 0 C 0 A
   -----------
   B 4 F 3 E 4
```

→ **`0xB4F3E4`**. Check in decimal: $12648430 - 789514 = 11858916 =
\text{0xB4F3E4}$. ✓

**Notes.** Most lost points come from not aligning the digits, students read
`0xC0C0A` as if it had six digits. Borrowing in base 16 (borrow = 16, not 10) is
the second source of errors.

---

## IC-09 · One's and two's complement · 2 pts · [2023-Ex Q1b]

> Show how the number $-42$ is encoded in one's complement and two's complement
> as an 8-bit representation. What is the advantage of two's complement over
> one's complement?

**Solution.**
$42_{10} = 00101010_2$.
- **One's complement:** invert every bit → $\mathbf{11010101}$.
- **Two's complement:** invert and add 1 → $11010101 + 1 = \mathbf{11010110}$.

**Advantage:** two's complement has a **single representation of zero** (one's
complement has $00000000$ and $11111111$), and addition and subtraction work
with the ordinary binary adder without an end-around carry correction. It also
represents one extra negative value ($-128$ to $+127$ instead of $-127$ to
$+127$).

---

## IC-10 · Biasing a die to two bits · 2 pts · [2024-E1 Q1c+d, 2025-Ex Q1d]

> a) You are tasked to store the result of one million rolls of a **fair**
> 16-sided die. Explain how you would encode that information with four bits per
> result.
> b) You are able to **bias** a 16-sided die, which means that you can change the
> probabilities of its results. Can you do that in a way that makes it possible
> to store its results with only **two bits per result**? Reason your answer.

**Solution.**
a) There are 16 equally likely outcomes and $\log_2 16 = 4$, so a fixed 4-bit
code assigning each face a distinct pattern $0000$–$1111$ is both sufficient and
optimal. Four million bits = 500 kB. No shorter fixed code exists, because 3
bits distinguish only 8 outcomes.

b) **Yes, on average, with a variable-length code.** The lower bound on the
average number of bits per result is the Shannon entropy
$H = -\sum_i p_i \log_2 p_i$. For a fair die $H = 4$ bits, but bias lowers it.
For example, with $p_1 = 3/4$ and the other fifteen faces at $1/60$ each,
$$H = 0.75\log_2\tfrac{4}{3} + 15 \cdot \tfrac{1}{60}\log_2 60 \approx 0.31 + 1.48 = 1.79 \text{ bits},$$
and Shannon's source coding theorem says a code with average length arbitrarily
close to $H$ exists (Huffman coding gets within one bit).

**The essential qualification:** two bits *on average*, not two bits per result.
A *fixed* 2-bit code can only distinguish 4 outcomes and could never encode 16,
however biased the die. The frequent face gets a short codeword and the rare
faces get long ones.

**Notes.** Part (b) is the discriminating question of this pool. A student who
answers "no, you need 4 bits for 16 outcomes" has missed variable-length coding;
a student who answers "yes" without distinguishing average from per-result
length has missed the point in the other direction. Full marks need both.

---

## IC-11 · Yes/no questions for a biased die · 4 pts · [2023-E2 Q1b+c]

> Consider a tricked 8-sided die such that the probability of results is the
> following:
> $$1: \tfrac{1}{10},\ 2: \tfrac{1}{10},\ 3: \tfrac{1}{10},\ 4: \tfrac{1}{10},\ 5: \tfrac{1}{10},\ 6: \tfrac{1}{10},\ 7: \tfrac{1}{5},\ 8: \tfrac{1}{5}$$
> a) Write a diagram with yes/no questions to determine the result of the roll.
> b) Based on your diagram, how many questions on average will you need to ask to
> know the result of the roll? You do not need to calculate the exact number but
> to show how you would calculate it.

**Solution.**
a) Build the tree by Huffman's rule: repeatedly join the two least probable
nodes. Combining the six $1/10$ faces in pairs gives three $1/5$ nodes, so we
have five nodes of probability $1/5$ (three pairs plus faces 7 and 8). Joining
them gives a tree in which

- faces 7 and 8 are at **depth 2**,
- one pair of $1/10$ faces is at depth 2, so those faces are at **depth 3**,
- the remaining four $1/10$ faces are at **depth 4**.

A valid tree, written as questions:

```
Is the result in {7, 8}?           yes → Is it 7?                 (2 questions)
                                   no  → Is it in {1,2,3,4}?
                                          yes → Is it in {1,2}?
                                                 yes → Is it 1?   (4 questions)
                                                 no  → Is it 3?   (4 questions)
                                          no  → Is it 5?          (3 questions)
```
*(Any tree with the same depth profile is correct; the assignment of faces to
leaves is arbitrary.)*

b) The average is $\sum_i p_i \cdot d_i$, the probability of each result times
the number of questions needed for it:
$$2\cdot\left(\tfrac{1}{5}\cdot 2\right) + 2\cdot\left(\tfrac{1}{10}\cdot 3\right) + 4\cdot\left(\tfrac{1}{10}\cdot 4\right) = 0.8 + 0.6 + 1.6 = \mathbf{3.0 \text{ questions}}$$

**Notes.** The entropy of this distribution is
$H = 6\cdot\tfrac{1}{10}\log_2 10 + 2\cdot\tfrac{1}{5}\log_2 5 \approx 2.92$
bits, so 3.0 is close to optimal, a good remark to make in the exam review, but
not required for full marks. Award (b) for the *formula* $\sum p_i d_i$ even if
the arithmetic is not finished, as the question says.

---

## IC-12 · Base-4 conversion with bitwise operations · 3 pts · [2023-E1 Q1d, 2024-Ex Q1d]

> Write the pseudocode of an algorithm called `decimal_int_to_base4_bitwise()`
> that converts a non-negative integer to a string with its base 4
> representation using **bitwise operations**.

**Solution.** Base 4 is $2^2$, so each base-4 digit is exactly two bits. Mask off
the low two bits, then shift right by two.

```
Procedure DECIMAL-INT-TO-BASE4-BITWISE(n)
Inputs:
      n: a non-negative integer
Result: a string with the base-4 representation of n
If n = 0
      then return "0"
s ← ""                            # the empty string
While n > 0:
      d ← n AND 3                 # 3 = 11 in binary: keeps the two low bits
      s ← DIGIT(d) + s            # prepend, because the digits come out low to high
      n ← n >> 2                  # shift right by two bits
return s
```

`DIGIT(d)` turns the number `d`, between 0 and 3, into the character `"0"` to
`"3"`.

**Notes.** Three things earn the points: (i) masking with `AND 3` rather than
`mod 4`, (ii) shifting by **2**, not 1, (iii) *prepending* the digit, since the
loop produces the least significant digit first. The `n = 0` special case is
worth mentioning but not worth a point.

---

## IC-13 · Why 0.1 loses precision · 2 pts · [2024-E1 Q1b]

> Explain why there is a loss of precision when encoding the number 0.1 in the
> single-precision IEEE 754 floating-point standard.

**Solution.** A binary floating-point number represents
$\pm\, m \times 2^{e}$ with a finite significand, so it can represent exactly
only **dyadic rationals**, fractions whose denominator is a power of two.
$0.1 = 1/10$ and $10 = 2 \times 5$; the factor 5 means the binary expansion is
infinite and periodic, $0.1_{10} = 0.0\overline{0011}_2$. With only 23
significand bits the expansion is cut off and rounded, so the stored value is
$0.100000001490116\ldots$, not $0.1$.

**The risk:** these errors accumulate. `0.1 + 0.2 == 0.3` is false; a loop that
adds $0.1$ ten thousand times does not reach $1000$; and comparing floats with
`==` is unreliable. Compare with a tolerance instead, and use exact types
(integers, or a decimal type) for money and counts.

---

## IC-14 · Fixed vs variable-length codes · 3 pts · `new`

> A social media dataset stores, for each of 500 million posts, the language of
> the post. There are 100 possible languages, but English accounts for 55% of
> posts, the next four languages for 8% each, and the remaining 95 languages
> share the rest.
>
> a) How many bits per post does a fixed-length code need?
> b) Would a variable-length code save space? Estimate the saving, showing how
>    you would calculate it.
> c) Give one practical disadvantage of the variable-length code.

**Solution.**
a) $\lceil \log_2 100 \rceil = \mathbf{7}$ bits per post ($2^6 = 64 < 100 \le
128 = 2^7$), so $3.5\times 10^9$ bits ≈ 437 MB.

b) Yes. The entropy is
$$H = -0.55\log_2 0.55 - 4\,(0.08 \log_2 0.08) - 95\left(\tfrac{0.13}{95}\right)\log_2\tfrac{0.13}{95}$$
$\approx 0.474 + 1.166 + 0.13 \times \log_2(731) \approx 0.474 + 1.166 + 1.238
\approx \mathbf{2.9}$ bits per post. A Huffman code would use roughly 3 bits per
post, under half the fixed-length cost, saving on the order of 250 MB.
*(Students need the formula and the reasoning, not the arithmetic.)*

c) Random access is lost: with a fixed 7-bit code, post $k$'s language is at bit
$7k$ and can be read directly; with a variable-length code you must decode from
the beginning, or store an index that eats back part of the saving. A single
corrupted bit also desynchronizes everything that follows.

**Notes.** This item generalizes `IC-10` to a realistic setting and adds the
engineering trade-off, which no past exam has asked for. Good anchor for a
10-point question 1 combined with `IC-01` and `IC-04`.

---

## Also available from the 2026 exercise sheets

Every exercise in [`../TheoryExercises/Exercise02.md`](../TheoryExercises/Exercise02.md)
is exam-shaped and comes with a worked answer. No cohort has seen the
*Additional practice* items.

| Where | Topic | Suitable as |
|---|---|---|
| TE-02 Ex. 1–3 | Ported from the 2023/24 sheet | Already close to exam questions |
| TE-02 A-items | Base conversion, signed integers, IEEE 754, text encodings, entropy | Fresh 2–4 point subquestions |

Also note that **character encoding** (ASCII, ISO-8859-1, UTF-8, code pages) is
taught in session 2 and covered in the exercise sheet but has **never been
examined**. It would make a good 2-point conceptual subquestion.
