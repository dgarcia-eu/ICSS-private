# Session 13: Social Science Applications

*Introduction to Computing for the Social Sciences · lecture transcript*

> Companion text for lecture 13. Notation follows
> [the course conventions](00-Conventions.md).
>
> This is the closing lecture: it puts everything from sessions 1 to 12 to
> work on actual research. It is also the most heavily referenced session,
> since every claim here points to a paper you can read. Full references at
> the end.

---

## Contents

1. [What Computational Social Science is](#1-what-computational-social-science-is)
2. [Neighboring labels](#2-neighboring-labels)
3. [The three meanings of "computational"](#3-the-three-meanings-of-computational)
4. [The three ages of CSS](#4-the-three-ages-of-css)
5. [Combining disciplines and methods](#5-combining-disciplines-and-methods)
6. [Digital behavioral data](#6-digital-behavioral-data)
7. [Four research examples](#7-four-research-examples)
8. [Issues with digital data: representation](#8-issues-with-digital-data-representation)
9. [New methods: three generations](#9-new-methods-three-generations)
10. [Method examples](#10-method-examples)
11. [Issues with methods: privacy](#11-issues-with-methods-privacy)
12. [The end of theory?](#12-the-end-of-theory)
13. [Agent-based modeling](#13-agent-based-modeling)
14. [Schelling's segregation model](#14-schellings-segregation-model)
15. [Simulating anti-COVID policies](#15-simulating-anti-covid-policies)
16. [Courses outlook](#16-courses-outlook)
17. [Summary](#17-summary)
18. [Check yourself](#18-check-yourself)
19. [References](#19-references)

---

## 1. What Computational Social Science is

*Computational Social Science* (CSS) is the quantitative testing of theories
from the social sciences at unprecedented breadth, depth and scale, in the
words of the manifesto by Lazer et al. (2009) in *Science*. That definition
commits to three things: using new, large-scale data to inform social science
theory; being quantitative and empirical, and not just theoretical; and being
interdisciplinary research rather than data-driven studies. Read the last
point carefully, because it is the one students most often get backwards.
CSS is not social science done with big data. The theory comes first, and the
data and the computation are in service of testing it; a study that finds a
striking pattern in a billion tweets and stops there is not CSS but a
description in search of a question. The word "unprecedented" in the
definition is nevertheless doing honest work. Breadth, that is, how many
people, depth, that is, how finely their behavior is recorded, and scale,
that is, how long a period and how many contexts, really did change by orders
of magnitude between 2000 and 2010, and the methods had to change with them.

---

## 2. Neighboring labels

Several adjacent fields have their own names, and knowing which is which saves
confusion when reading. *Social Data Science* focuses on new methods to study
human behavior and society rather than on testing or developing social
science theory, and it is almost a synonym of CSS. *Web Science* is the study
of the Web as a socio-technical system, with empirical studies but also the
development of computer science methods. *Digital Sociology* is the sociology
of the digital transformation and of the social phenomena affected by the new
uses of information and communication technology. The distinctions are of
emphasis and not of substance: CSS emphasizes theory, Social Data Science
emphasizes methods, Web Science takes the Web as its object, and Digital
Sociology studies digitalization as a social phenomenon.

---

## 3. The three meanings of "computational"

The word "computational" in Computational Social Science can have three
meanings, all related to computation but different. *Digital* means based on
large datasets of human behavior, for example produced by the Web and social
media. *Computerized* means the quantitative analysis of data in an
automated, tractable, repeatable and extensible fashion. *Generative* means
the application of data and results to the design of agent-based models that
explain complex social phenomena and motivate interventions. This
tripartition organizes the rest of the lecture: the digital meaning is the
subject of [section 6](#6-digital-behavioral-data), the computerized meaning
of [section 9](#9-new-methods-three-generations), and the generative meaning
of [section 13](#13-agent-based-modeling). It is worth noticing what
"computerized" demands. Automated means that there is no manual step you
cannot describe, tractable that the analysis finishes in reasonable time, as
in session 8, repeatable that someone else running your code gets your
numbers, and extensible that the next study can build on it. Those four words
are why this whole course exists: they are properties of your code, not of
your data.

Before this maturity there was a phase of pure enthusiasm, which the lecture
illustrates with early data-driven CSS. The satirical Urban Dictionary entry
for "data piñata", a big data method that consists of whacking data with a
stick in the hope that some insights will come out, captures it, and the
cover of Simon Lindgren's book *Data Theory* makes the same joke seriously.
The warning is worth taking: without a question, more data just means more
patterns, and most patterns in a large enough dataset are noise.

---

## 4. The three ages of CSS

Salganik's *Bit by Bit* places CSS on the Gartner hype curve, the standard
shape of the reputation of a technology, with a peak of inflated
expectations, a trough of disillusionment, and a slope of enlightenment
leading to a plateau of productivity. The lecture's version labels the phases
by what people got excited about. The age of data is the peak: enthusiasm
about the digital traces themselves, their sheer volume, and the belief that
they would answer everything. The age of theory is the trough: the field
discovers that data without a question produces nothing, and turns back to
social theory to say what it is actually measuring. The age of methods is the
recovery: sustained progress, built on developing and validating measurement
instruments rather than on acquiring more data. We are, on this account, in
the third phase, which is the optimistic reading of why a methods course like
this one is worth taking.

```
hype │      ╱‾╲
     │     ╱   ╲          ╱‾‾‾‾‾▶
     │    ╱     ╲       ╱
     │  ╱         ╲___╱
     └──[ data ]─[theory]─[ methods ]───▶ time
```

---

## 5. Combining disciplines and methods

CSS sits at the intersection of three fields, computer science, mathematics
and statistics, and the behavioral and social sciences, and the slide of the
lecture carries a caption worth memorizing: statistics is about making sound
inferences from too little data, and data science about making meaningful
inferences from too much data. That contrast is exact. Classical statistics
was built for the regime where data is expensive and scarce, hence
significance testing, power analysis and sampling theory. Digital traces put
us in the opposite regime, where everything is significant because $n$ is a
hundred million, and the hard problem is deciding what any of it means.

The methods of CSS reinforce each other rather than compete. Large-scale
digital traces give breadth but no ground truth. Survey validation supplies
the ground truth, answering whether a Twitter-based measure of sentiment
tracks what people report feeling. Computational modeling turns a verbal
theory into something that generates predictions. And controlled experiments
establish causality, which observational traces cannot. No single one of them
is enough on its own, and the strongest CSS papers close a loop between at
least two of them.

```
   Large-scale Digital Traces
        ↕            ↕
        ↕      Survey Validation
        ↕            ↕
   Computational Modeling
        ↕
   Controlled Experiments
```

---

## 6. Digital behavioral data

Sensors and connectivity are increasingly pervasive, and more and more of our
actions happen through digital technologies: searching for a job online,
talking with a family member over the phone, sharing open source code,
posting a video on a social networking site, paying at the supermarket with a
credit card, or chatting on a company instant messenger. All of these
actions generate *digital traces* that can be analyzed in social science
research. The key property of such traces is that they are found data and not
designed data. Nobody paid respondents, wrote a questionnaire or drew a
sample. That gives three advantages, since the traces are cheap, they are
longitudinal by default, and they record behavior rather than self-reported
behavior, and one large disadvantage, which is the subject of [section
8](#8-issues-with-digital-data-representation).

---

## 7. Four research examples

The first example is earthquakes on Twitter. XKCD 723, *Seismic Waves*, gets
there first: a character notices that they can tell that an earthquake
happened elsewhere because the tweets about it arrive faster than the seismic
wave. That is a joke about the speed of light versus the speed of rock, and it
is also a research design. Earle, Bowden and Guy (2012) built it: Twitter
earthquake detection can produce alerts within a couple of minutes of an
event, in some cases faster than the instrumental networks in regions with
sparse sensor coverage, and the signal is a sudden spike in the rate of tweets
containing "earthquake" from a geographic region. Note what makes this work:
humans are the sensors, and there are a lot of them. The method fails exactly
where there are few users, which is section 8 again.

The second example is trading and Google Trends. Preis, Moat and Stanley
(2013) studied whether the search volume for finance-related words on Google
Trends relates to stock market movements. The search volume for terms such as
"debt" rose ahead of market falls, and a trading strategy based on the signal
outperformed a buy-and-hold benchmark in backtesting. The general idea, that
aggregate search behavior measures collective attention and information
seeking before a decision is made, has become a standard CSS instrument.

The third example is gender inequality with Facebook. Garcia et al. (2018)
used the advertising interface of Facebook, which reports the size of
audiences by gender, age and country, to construct a worldwide indicator of
the gender gap in Facebook use, and validated it against established offline
indices of gender inequality in the economy, health and education. The
methodological trick is worth noting: the data is not scraped from users at
all, but read off a public marketing tool as aggregate counts. This is a
cheap, privacy-preserving way to obtain population-level measures, and it
updates monthly rather than every ten years like a census. The fourth
example, social media as an emotion macroscope, is covered in [section
10](#10-method-examples).

---

## 8. Issues with digital data: representation

The central problem of digital trace data is that the people who produce
them are not the population. Data of the Pew Research Center on the social
media use of US adults by age group makes the size of the gap concrete:

| Platform | 18–29 | 65+ | Youngest − oldest |
|---|---|---|---|
| Snapchat | 65% | 2% | **+63** |
| Instagram | 71% | 13% | **+58** |
| YouTube | 95% | 49% | **+46** |
| TikTok | 48% | 4% | **+44** |
| Twitter | 42% | 7% | **+35** |
| Facebook | 70% | 50% | **+20** |

A study of Snapchat is, demographically, a study of the young; a 63-point gap
is not a nuisance to be weighted away but a different population. And the
gaps differ by platform, so "social media users" is not one group either.
Lazer et al. (2021), in *Meaningful measures of human society in the
twenty-first century*, argue that this is the central methodological
challenge of the field, and that it needs infrastructure, a scientific data
infrastructure with known coverage properties, rather than cleverness on a
per-study basis. Three failure modes should be kept separate. Coverage
error means that whole groups are absent from the platform. Behavioral
distortion means that what people do on a platform is shaped by the
affordances and the audience of the platform, and is not their behavior in
general. And algorithmic confounding means that what you observe is partly
the product of the ranking algorithm of the platform, which changes without
notice, so that a trend in your data may be a trend in the software of the
company.

---

## 9. New methods: three generations

Social science data used to have few formats, such as the annotations of
experiment outcomes or survey responses. Now there are many more formats and
data sources, such as text, social networks, locations and timestamps, and
likes, and sometimes these formats are even related to each other. The
methods to handle them have been improving over time in three generations.
The first generation adapted previous social science methods; the example
is the use of dictionaries in text analysis, where you take a hand-built
list of words scored for a construct and count them, which is transparent,
cheap, and exactly as good as the list. The second generation uses machine
learning models to generalize measurement from many examples of
measurements; the example is sentiment analysis, where you label a few
thousand texts and train a classifier, as in session 10, to reproduce your
labeling on millions more. The third generation uses large models to analyze
highly dimensional data; the example is word embeddings, which are treated in
the document analysis course. The trajectory is a steady move from rules you
write to patterns learned from data, buying coverage and nuance at the cost
of transparency, which matters because you then have to validate the
instrument rather than read it.

---

## 10. Method examples

The first example is VADER sentiment analysis. Hutto and Gilbert (2014) built
VADER, the Valence Aware Dictionary and sEntiment Reasoner, a rule-based
model tuned specifically for social media text. It is first-generation in
the sense of section 9, with a lexicon at its core, but with rules that
handle the things social media text actually does: negation, since "not good"
is not "good"; intensifiers, since "very good" is more than "good";
punctuation, since "good!!!" is more than "good"; capitalization, since
"GOOD" is more than "good"; and emoticons and slang. The lexicon itself was
built by having crowdworkers rate each term, so the scores are empirical
rather than an author's intuition. VADER is a good demonstration that a
well-designed simple method can match a machine-learned one on the domain it
was built for, and it has the enormous advantage that you can read it.

The second example is social media emotion macroscopes. Garcia, Pellert,
Lasser and Metzler (2021), in *Social media emotion macroscopes reflect
emotional experiences in society at large*, address the obvious objection to
all of the above: does aggregated social media sentiment measure anything
real? The answer comes from validation against surveys, comparing time series
of text-derived emotion with population surveys of self-reported affect. The
finding is that aggregate signals do track the emotional experience of
society, while individual-level inferences are far weaker. That asymmetry is
a general lesson: an instrument can be reliable at the population level and
useless at the person level, because the errors average out in one case and
not in the other.

The third example is personality and Facebook likes. Youyou, Kosinski and
Stillwell (2015) showed in *Computer-based personality judgments are more
accurate than those made by humans* that, using only the Facebook likes of a
person, a model predicted their self-reported Big Five personality traits
more accurately than the friends of the person could, and, with about 300
likes, more accurately than their spouse. Take this as the transition to the
next section: the same result is a methodological triumph and a privacy
catastrophe.

---

## 11. Issues with methods: privacy

Kosinski, Stillwell and Graepel (2013), in *Private traits and attributes are
predictable from digital records of human behavior*, showed that Facebook
likes, each of them individually innocuous, predict sensitive attributes
with high accuracy: sexual orientation, ethnicity, religious and political
views, personality traits, intelligence, substance use and parental
separation. The point is not that anyone disclosed those attributes. It is
that they did not have to. Aggregations of innocuous data are not innocuous,
and no individual consent decision can anticipate this, because the
inference lives in the pattern across thousands of people. Garcia et al.
(2018), in *Collective aspects of privacy in the Twitter social network*,
push this further: the data of your friends predicts your attributes even if
you are not on the platform at all, which is the shadow profile problem.
Privacy is therefore not an individual property that you can protect by your
own choices; it is collective, and someone else's decision to share leaks
information about you. For research practice this means that the consent
framework inherited from survey methodology is not sufficient. Consider what
your model can infer, not just what your data contains.

---

## 12. The end of theory?

In 2008 *Wired* published Chris Anderson's essay "The End of Theory: The Data
Deluge Makes the Scientific Method Obsolete", which argued that with enough
data, correlation supersedes causation and models become unnecessary,
because the numbers speak for themselves. The response of the lecture is a
large red cross drawn over it, and the reasons why the essay is wrong can be
stated in the terms of this course. Data does not interpret itself: without a
theory, you cannot say which of the millions of correlations in a large
dataset is meaningful. Prediction is not explanation: recall Hinton's framing
in session 10, that a model that predicts well has found a pattern, not the
mechanism, and only a mechanism licenses intervention, so a social scientist
who wants to change something needs more than a good predictor. Measurement
requires theory: to claim that your variable measures polarization you need a
theory of what polarization is, and there is no theory-free measurement. And
sampling bias does not go away with size: a biased sample of a billion is
still biased, as section 8 showed, because volume reduces variance and not
bias. The version of the same argument in the 2020s is that large language
models make theory unnecessary, and the counterarguments are the same ones.

---

## 13. Agent-based modeling

Agent-based modeling is the generative meaning of "computational" from
section 3. It models humans as agents that symbolize a simplified behavior;
the agents have quantifiable variables and properties, and all the
interaction rules are explicitly defined and parametrized. Simulations and
mathematical analysis can then be applied to derive properties of the system
that might not be easy to conclude from intuition alone. An agent-based model
generates hypotheses and proofs of generative sufficiency, but not empirical
evidence, and that last point is the one to underline. The model shows that
a proposed micro-mechanism is sufficient to produce an observed macro-pattern,
that is, that these rules can generate this outcome. It does not show that
this is what happens in the world, because other rules might generate the
same outcome. In Epstein's phrase, if you did not grow it, you did not
explain it, but growing it is a necessary and not a sufficient condition.
Note also the real content of the requirement that the rules be explicit:
writing a model as code forces you to be explicit, because a verbal theory can
hide ambiguity indefinitely while a program cannot compile it. That is a
benefit of computational modeling independent of any simulation result.

---

## 14. Schelling's segregation model

The classic example is the segregation model of Thomas Schelling (1971),
*Dynamic Models of Segregation*. The model has agents of two kinds in
similar numbers on a grid with a low but nonzero fraction of empty cells.
Each cell has a neighborhood of the 8 cells around it, and corners and
borders have fewer neighbors. Agents are aware of the fraction $f$ of
similar agents in their neighborhood, they are satisfied when $f \ge F$, and
if they are unsatisfied they jump to the closest satisfying cell. The
parameter $F$ measures intolerance. As an algorithm, in the course's
pseudocode:

```
Procedure SCHELLING(grid, F)
Inputs:
      grid: a grid with agents of two kinds and some empty cells
      F: the satisfaction threshold
Result: the grid evolved until no agent is unsatisfied
moved ← TRUE
While moved:
      moved ← FALSE
      For each agent a in random order:
            f ← fraction of the occupied neighbors of a that are of the kind of a
            If f < F
                  then move a to the closest empty cell where its f would be ≥ F
                       moved ← TRUE
```

The lecture runs the simulation with $F = 0.2$, where agents are content as
long as one in five of their neighbors is like them, that is, they are happy
in a neighborhood where they are outnumbered four to one, an extremely
tolerant population by any reasonable reading. The grid still segregates into
large single-color blocks. With $F = 0.6$ the segregation is very strong, and
with $F = 0.4$, where agents actively prefer to be in the minority, the grid
is also clearly segregated. This is the point of the model: strongly
segregated macro-outcomes do not require intolerant micro-preferences, and a
mild individual preference not to be completely isolated, iterated over many
small moves, is sufficient. The methodological lesson generalizes far beyond
segregation. You cannot read individual motives off an aggregate pattern, so
observing a segregated city does not license the inference that its
residents are intolerant. This is the computational counterpart of the
ecological fallacy, and it is the single most transferable idea of this
lecture. There is more on Schelling's model in the slides of the CMSS course,
<https://dgarcia-eu.github.io/CMSS-Konstanz/02_Segregation/Slides/Slides.html#14>
(slides 14 to 38).

---

## 15. Simulating anti-COVID policies

Lasser, Hell and Garcia (2022), in *Assessment of the Effectiveness of
Omicron Transmission Mitigation Strategies for European Universities Using
an Agent-Based Network Model*, use agent-based modeling for a live policy
question. The agents are students and staff, the contact network comes from
actual course enrollment data, that is, who shares a room with whom and when,
and the disease process is calibrated to the parameters of the Omicron
variant. Then policies are simulated, such as masking, ventilation, testing
frequency, vaccination coverage and class size caps, and the sizes of the
outbreaks are compared. The value of doing it this way is that these
interventions cannot be randomized: you cannot run a controlled trial of
university-wide mask policies during a wave. The model gives a way to
compare counterfactuals, with its assumptions written down where they can be
argued with, which is exactly the generative contribution of section 3, and
exactly why its output is a hypothesis about mechanisms and not evidence in
the sense of a trial.

---

## 16. Courses outlook

The lecture closes with the courses that continue from here. *Deep Learning
for the Social Sciences*, 9 ECTS (2+2 SWS), taught next summer semester by
Giordano De Marzo, covers machine learning concepts, multilayer perceptrons
and their limitations, convolutional neural networks, recurrent networks,
LSTMs and reinforcement learning, and applications to time series, graphs,
generative modeling and natural language processing, with exercises in
PyTorch. *Social Media Data Analysis*, 9 ECTS (2+2 SWS), to be taught in 2027
by David Garcia (<https://github.com/dgarcia-eu/SocialMediaDataAnalysis>),
covers the analysis of search data to measure information seeking,
popularity and social impact in social media, the application and evaluation
of sentiment analysis techniques for social media text, and methods and
applications of social network analysis in online media, with practical
assignments in which you get and analyze your own data. *Computational
Modelling of Social Systems*, a seminar with exercises of 6 ECTS (2+2 SWS),
to be taught in 2027 by David Garcia
(<https://github.com/dgarcia-eu/CMSS-Konstanz>), has lectures and exercises
on agent-based modeling and complexity science: Schelling's model of
segregation, Axelrod's model of cultures, the spreading of behavior, opinion
dynamics, network growth models and social resilience, with Python exercises
in Mesa.

For the path to the master thesis, the recommendation is to take the
*Colloquium in Social Data Science* the semester before your master thesis,
and to prepare by joining the research updates of the group (Tuesdays
13:30–15:00). Students prepare their thesis plan during the semester and
present it for input at the end; registration is manual, so contact David
Garcia beforehand to discuss coursework and potential topics. The second
recommendation is to take the courses of the group and to read its papers.

---

## 17. Summary

Computational Social Science uses new sources of data and computational
methods in the social sciences, and the word computational has three
meanings, digital, computerized and generative. Digital behavioral data
comes from social media, search, mobile phones and more, and its main risk is
representation. The new methods of the social sciences, with text analysis
as the example, bring privacy risks. And the computational analysis of social
science theory uses agent-based modeling to analyze models of social
systems. The next sessions are the exam review and a Q&A. An exam example
can be found in the folder of theory exercises on Ilias; in the upcoming
sessions we can discuss any previous exercise, the exam example, or go back
to any slides from the lectures, and the extra time will be used for
questions about the practical projects. Questions and requests are
collected 24 hours before each session from the form
<https://forms.gle/MXTtQw6FUNpw2qrW9>.

---

## 18. Check yourself

**1.** A study analyzes 500 million tweets about an election and concludes that the public favors candidate A. Name three separate problems.

<details><summary>Answer</summary>

Coverage: Twitter users are younger, more urban and more politically engaged
than the electorate, so the sample is not the population and no amount of
$n$ fixes that. Behavioral distortion: tweeting about a candidate is not
voting for them, and posting is dominated by a small hyperactive minority, so
the unit of analysis, tweets, is not the unit of interest, people.
Algorithmic confounding: what is visible and collectable depends on the
ranking and the API of the platform, which the researcher does not control.
A fourth problem, if you like, is that inferring support from text requires a
validated instrument, not just keyword counting.

</details>

**2.** In Schelling's model with F = 0.4, agents prefer to be in the minority. Why does segregation still emerge?

<details><summary>Answer</summary>

Because satisfaction is evaluated locally and iteratively. An agent that
happens to fall below the threshold moves; its departure changes the
composition of its old neighborhood, which can push a neighbor below the
threshold, and so on. Small local adjustments compound into large-scale
sorting. Nothing in the rule of any agent mentions the global pattern; the
pattern is emergent, and this is why you cannot infer preferences from
outcomes.

</details>

**3.** Your agent-based model reproduces an observed macro-pattern. What have you shown, and what have you not?

<details><summary>Answer</summary>

You have shown generative sufficiency: this set of micro-rules is enough to
produce the pattern. You have not shown that these are the operating rules,
since other mechanisms may produce the same pattern, which is called
equifinality, nor have you produced empirical evidence. The model generates a
hypothesis that then needs independent testing with data.

</details>

**4.** Why does the shadow-profile result mean that individual consent is not sufficient for privacy protection?

<details><summary>Answer</summary>

Because the information about you is carried by other people's data. If the
likes and connections of your friends predict your attributes, then your own
decision to stay off the platform does not protect you, and their consent
decisions affect your privacy without your involvement. Privacy is a
collective property, so it needs collective, that is, regulatory and
institutional, protections, not just individual opt-outs.

</details>

**5.** Anderson claimed that with enough data, we no longer need models. Give the strongest version of his argument, then say why it fails.

<details><summary>Answer</summary>

The strongest version is that for many practical purposes, such as
recommending, translating and forecasting, a model that predicts accurately
is all anyone needs, and modern systems achieve that without any theory of
the domain. That is genuinely true, and it is why machine translation works
without linguistics. It fails for social science because the goal is usually
not prediction but explanation and intervention: a predictor tells you what
will happen if nothing changes, while a policy is precisely a change.
Moreover, deciding what to measure, and claiming that a variable measures a
social construct, is theoretical work that no amount of data performs for
you, and correlations found in a biased sample remain biased at any $n$.

</details>

---

## 19. References

- **Lazer, D., Pentland, A., Adamic, L., Aral, S., Barabási, A.-L. et al.
  (2009).** "Computational Social Science". *Science* 323(5915), 721–723.
  The definition of section 1.
- **Lazer, D. et al. (2021).** "Meaningful measures of human society in the
  twenty-first century". *Nature* 595, 189–196. Section 8.
- **Pew Research Center (2021).** *Social Media Use in 2021.*
  <https://www.pewresearch.org/internet/2021/04/07/social-media-use-in-2021/>.
  Source of the platform/age table of section 8.
- **Salganik, M. J. (2017).** *Bit by Bit: Social Research in the Digital
  Age.* Princeton University Press. Free online at
  <https://www.bitbybitbook.com/>. Source of the hype-curve figure of section
  4, and the best single book on the material of this lecture.
- **Lindgren, S. (2020).** *Data Theory: Interpretive Sociology and
  Computational Methods.* Polity. Section 3.
- **Earle, P. S., Bowden, D. C. & Guy, M. (2012).** "Twitter earthquake
  detection: earthquake monitoring in a social world". *Annals of Geophysics*
  54(6), 708–715. <https://doi.org/10.4401/ag-5364>. Section 7.
- **Munroe, R.** *Seismic Waves*, XKCD 723: <https://xkcd.com/723/>
- **Preis, T., Moat, H. S. & Stanley, H. E. (2013).** "Quantifying Trading
  Behavior in Financial Markets Using Google Trends". *Scientific Reports* 3,
  1684. Section 7.
- **Garcia, D., Mitike Kassa, Y., Cuevas, A., Cebrian, M., Moro, E., Rahwan,
  I. & Cuevas, R. (2018).** "Analyzing gender inequality through large-scale
  Facebook advertising data". *PNAS* 115(27), 6958–6963. Section 7.
- **Hutto, C. J. & Gilbert, E. (2014).** "VADER: A Parsimonious Rule-Based
  Model for Sentiment Analysis of Social Media Text". *Proceedings of the
  International AAAI Conference on Web and Social Media* 8(1), 216–225.
  Section 10.
- **Garcia, D., Pellert, M., Lasser, J. & Metzler, H. (2021).** "Social media
  emotion macroscopes reflect emotional experiences in society at large".
  *arXiv:2107.13236*. Section 10.
- **Youyou, W., Kosinski, M. & Stillwell, D. (2015).** "Computer-based
  personality judgments are more accurate than those made by humans". *PNAS*
  112(4), 1036–1040. Section 10.
- **Kosinski, M., Stillwell, D. & Graepel, T. (2013).** "Private traits and
  attributes are predictable from digital records of human behavior". *PNAS*
  110(15), 5802–5805. Section 11.
- **Garcia, D., Goel, M., Agrawal, A. K. & Kumaraguru, P. (2018).**
  "Collective aspects of privacy in the Twitter social network". *EPJ Data
  Science* 7, 3. Section 11, shadow profiles.
- **Anderson, C. (2008).** "The End of Theory: The Data Deluge Makes the
  Scientific Method Obsolete". *Wired*, 23 June 2008.
  <https://www.wired.com/2008/06/pb-theory/>. Section 12.
- **Schelling, T. C. (1971).** "Dynamic Models of Segregation". *Journal of
  Mathematical Sociology* 1(2), 143–186. Section 14.
- **Epstein, J. M. (2006).** *Generative Social Science: Studies in
  Agent-Based Computational Modeling.* Princeton University Press. Section
  13, "if you didn't grow it, you didn't explain it".
- **Lasser, J., Hell, T. & Garcia, D. (2022).** "Assessment of the
  Effectiveness of Omicron Transmission Mitigation Strategies for European
  Universities Using an Agent-Based Network Model". *Clinical Infectious
  Diseases* 75(1), e293–e300. Section 15.
- **CMSS Konstanz course materials:**
  <https://github.com/dgarcia-eu/CMSS-Konstanz>. Schelling's model in depth.
- **Social Media Data Analysis course materials:**
  <https://github.com/dgarcia-eu/SocialMediaDataAnalysis>
