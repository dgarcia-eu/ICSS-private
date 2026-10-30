# Exercise Sheet 13: Social Science Applications

*Introduction to Computing for the Social Sciences · Prof. Dr. David Garcia*

> Exercises 1–3 are worked through in the exercise session. The *Additional
> practice* section is for self-study. Worked solutions to every exercise, with
> pointers to the slides and the handout sections that cover the material, are
> in [`Solutions/Exercise13-Solutions.md`](Solutions/Exercise13-Solutions.md); try before you open them.
> Notation: [course conventions](../Transcripts/00-Conventions.md).
>
> This session's exercises are more discursive than the earlier ones. Answers are
> expected in complete sentences, and there is usually more than one defensible
> position, what is graded is the reasoning.

---

## Exercise 1: Designing a study with digital traces

A research group wants to study whether public attention to climate change
increased after a major flood in Germany. They propose to count the number of
posts on a social media platform mentioning "Klimawandel" in the four weeks
before and the four weeks after the flood.

a) Which of the **three meanings of "computational"** from the lecture does this
   study use? Could it be extended to use the other two? Say how.

b) Name three distinct threats to the validity of this design, drawn from the
   lecture's discussion of digital behavioral data. For each one, say concretely
   how it could produce a spurious increase.

c) The group finds a 40% increase and concludes that "public attention to climate
   change rose by 40%". Rewrite that conclusion so that it says only what the
   data supports.

d) Propose one additional data source and one validation strategy that would
   strengthen the study. Refer to the methodological cycle from the lecture
   (traces, surveys, models, experiments).

---

## Exercise 2: Schelling's model

Consider Schelling's segregation model as presented in the lecture: a grid with
agents of two kinds, a small fraction of empty cells, neighborhoods of the 8
surrounding cells, and a satisfaction threshold $F$.

a) Write the pseudocode of the model's update loop, following the course
   conventions. Be explicit about the stopping condition.

b) Consider the following $3 \times 3$ neighborhood, with the agent under
   consideration in the center. `R` and `B` are the two kinds and `·` is an empty
   cell.

   ```
   R B B
   B R ·
   R B B
   ```

   Compute $f$ for the central agent. Is it satisfied if $F = 0.4$? If $F = 0.2$?
   State clearly whether empty cells count in the denominator, and justify your
   choice.

c) The lecture reports that the grid segregates even for $F = 0.4$, i.e. when
   agents actively prefer to be in the minority. Explain the mechanism in your own
   words: why does a preference that no individual would call intolerant produce a
   segregated outcome?

d) A politician reads about the result and concludes that "residential
   segregation proves that people are prejudiced". Explain, using the model, why
   the inference is invalid. Name the general methodological error.

> Part (d) is the exam-relevant one. The model is a *counterexample*: it shows
> that segregated outcomes are compatible with tolerant preferences, and
> therefore that you cannot read the preferences off the outcome.

---

## Exercise 3: Methods and their risks

a) The lecture distinguishes **three generations** of methods for measuring
   social science constructs from text. Name them, give one example of each, and
   say what is gained and what is lost when moving from one generation to the
   next.

b) A study uses a dictionary of positive and negative words to measure the
   sentiment of parliamentary speeches. Give two concrete reasons why this could
   go wrong for this particular text type, and one thing the researchers should do
   before trusting the measure.

c) Explain the finding of Kosinski et al. (2013) in two sentences, and then
   explain why it is a problem that cannot be solved by asking users for consent.

d) You are designing a study that predicts individuals' political attitudes from
   their public social media activity. Write down three questions from the
   lecture's responsible-AI list that you would have to answer before proceeding,
   and answer them for this specific study.

---

## Additional practice

### A1. Representation

Using the Pew data from the lecture (share of U.S. adults using each platform, by
age group):

| Platform | 18–29 | 65+ |
|---|---|---|
| Snapchat | 65% | 2% |
| Instagram | 71% | 13% |
| YouTube | 95% | 49% |
| TikTok | 48% | 4% |
| Twitter | 42% | 7% |
| Facebook | 70% | 50% |

a) Which platform would you choose to study attitudes of the general adult
   population, and why? What would still be wrong with it?
b) A study of TikTok concludes that "the public is increasingly concerned about
   housing costs". Restate the conclusion so it is defensible.
c) Explain why increasing the sample from 10 000 to 10 million posts does not fix
   the problem.
d) Name the three failure modes of digital trace data from the lecture and give
   one example of each.

### A2. Agent-based modeling

a) What does an agent-based model demonstrate when it reproduces an observed
   macro-pattern? What does it *not* demonstrate?
b) Give two reasons to build a model even if you never run a simulation.
c) The COVID university model of the lecture compares mitigation policies. Why
   was a model used instead of a randomized experiment?
d) Two different agent-based models, with different rules, both reproduce the
   same observed pattern. What is this called and what does it imply for how you
   should report your model?

### A3. The end of theory

a) Reconstruct Anderson's (2008) argument in three sentences, as strongly as you
   can.
b) Give three distinct objections to it, each drawn from a different session of
   this course.
c) In what domain is Anderson closest to right? Why does that domain differ from
   social science?

### A4. Reading a CSS paper

Pick one of the studies from the lecture: Earle et al. (2012) on earthquake
detection, Preis et al. (2013) on Google Trends and trading, or Garcia et al.
(2018) on Facebook advertising data, and answer:

a) What is the theoretical question, and what is the digital trace used to answer
   it?
b) What is the measurement claim, that is, what is the trace assumed to measure?
c) How is that assumption validated, if at all?
d) Which population does the result generalize to?

### A5. Privacy

a) Explain the difference between disclosing an attribute and having it inferred.
b) What is a shadow profile, and why does it make privacy a collective rather than
   an individual property?
c) You delete your account. Which of the risks in (a) and (b) does that remove?
d) Give one research-practice rule and one policy rule that follow from all this.

### A6. Vocabulary

Match each term to its definition and give one example not used in the lecture.

Terms: Computational Social Science, Social Data Science, Web Science, Digital
Sociology, generative modeling, generative sufficiency.

---

## Sources

- There was no 2024 theory sheet for this session; this sheet is new, built from
  the lecture slides and the references below.
- **Lazer, D. et al. (2009).** "Computational Social Science". *Science*
  323(5915), 721–723.: Exercise 1a, A6.
- **Lazer, D. et al. (2021).** "Meaningful measures of human society in the
  twenty-first century". *Nature* 595, 189–196.: Exercise 1b, A1.
- **Pew Research Center (2021).** *Social Media Use in 2021.*
  <https://www.pewresearch.org/internet/2021/04/07/social-media-use-in-2021/>,
  The table in A1.
- **Salganik, M. J. (2017).** *Bit by Bit: Social Research in the Digital Age.*
  Princeton University Press. <https://www.bitbybitbook.com/>: Ch. 2 on
  observing behavior (exercise 1, A1) and ch. 3 on asking questions; the best
  companion for this sheet.
- **Schelling, T. C. (1971).** "Dynamic Models of Segregation". *Journal of
  Mathematical Sociology* 1(2), 143–186.: Exercise 2.
- **Epstein, J. M. (2006).** *Generative Social Science.* Princeton University
  Press.: Generative sufficiency, exercise 2d and A2.
- **Hutto, C. J. & Gilbert, E. (2014).** "VADER". *ICWSM*.: Exercise 3a, 3b.
- **Kosinski, M., Stillwell, D. & Graepel, T. (2013).** "Private traits and
  attributes are predictable from digital records of human behavior". *PNAS*
  110(15), 5802–5805.: Exercise 3c, A5.
- **Garcia, D. et al. (2018).** "Collective aspects of privacy in the Twitter
  social network". *EPJ Data Science* 7, 3.: A5(b).
- **Garcia, D. et al. (2018).** "Analyzing gender inequality through large-scale
  Facebook advertising data". *PNAS* 115(27), 6958–6963.: A4.
- **Earle, P. S., Bowden, D. C. & Guy, M. (2012).** "Twitter earthquake
  detection". *Annals of Geophysics* 54(6).: A4.
- **Preis, T., Moat, H. S. & Stanley, H. E. (2013).** "Quantifying Trading
  Behavior in Financial Markets Using Google Trends". *Scientific Reports* 3,
  1684.: A4.
- **Anderson, C. (2008).** "The End of Theory". *Wired*.
  <https://www.wired.com/2008/06/pb-theory/>: A3.
- **Lasser, J., Hell, T. & Garcia, D. (2022).** "Assessment of the Effectiveness
  of Omicron Transmission Mitigation Strategies for European Universities Using
  an Agent-Based Network Model". *Clinical Infectious Diseases* 75(1),
  e293–e300.: A2(c).
- **Squire, P. (1988).** "Why the 1936 *Literary Digest* Poll Failed". *Public
  Opinion Quarterly* 52(1), 125–133.: The example in A1(c).
