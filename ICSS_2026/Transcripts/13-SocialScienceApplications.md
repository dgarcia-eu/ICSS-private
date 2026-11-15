# Session 13: Social Science Applications

<style>
figure, .figure, .float { margin: 1.4em 0 1.8em 0; }
figure img, .float img { display: block; max-width: 100%; }
figcaption, .figcaption, .figure p.caption { margin-top: 0.3em; font-size: 0.88em; color: #555; }
details { margin: -0.5em 0 2.2em 0; }
</style>

*Introduction to Computing for the Social Sciences · lecture transcript*

This is the closing session of the course. In it we put what we learned in
the previous sessions to work on actual research. It is also the session with
the most references, because every claim here points to a paper that you can
read. You can find the full references at the end.

---

## Contents

1. [Computational social science](#css)
2. [Digital behavioral data](#digital-data)
3. [New methods in the social sciences](#new-methods)
4. [Computational analysis of social science theory](#theory)
5. [Courses outlook](#outlook)

---

## 1. What Computational Social Science is {#css}
*Computational Social Science* (CSS) is the quantitative testing of theories
from the social sciences at unprecedented breadth, depth and scale, in the
words of the manifesto by Lazer et al. (2009) in *Science*. That definition
commits to three things. First, CSS uses new, large-scale data to inform
social science theory. Second, it is quantitative and empirical and not just
theoretical. Third, it is interdisciplinary research rather than a collection
of data-driven studies. The third point is the one that students most often
understand backwards, because CSS is not social science done with big data.
Instead, the theory comes first and the data and the computation are used to
test it. For example, a study that finds a striking pattern in a billion
tweets and stops there is not CSS, because it describes the data without
asking a question about society.

The word "unprecedented" in the definition is nevertheless justified. Three
properties of the data changed by orders of magnitude between 2000 and 2010:

- **Breadth**, i.e. how many people are observed.
- **Depth**, i.e. how finely their behavior is recorded.
- **Scale**, i.e. how long a period and how many contexts are covered.

The methods of the social sciences had to change with them.

---

## 2. Neighboring labels

Several neighboring fields have their own names and it helps to know which is
which when you read the literature.

- ***Social Data Science*** focuses on new methods to study human behavior and
  society rather than on testing or developing social science theory. It is
  almost a synonym of CSS.
- ***Web Science*** is the study of the Web as a socio-technical system, with
  empirical studies but also the development of computer science methods.
- ***Digital Sociology*** is the sociology of the digital transformation and
  of the social phenomena affected by the new uses of information and
  communication technology.

These fields differ in emphasis and not in substance. CSS emphasizes theory
and Social Data Science emphasizes methods, while Web Science takes the Web as
its object and Digital Sociology studies digitalization as a social
phenomenon.

---

## 3. The three meanings of "computational"

The word "computational" in Computational Social Science can have three
meanings, which are all related to computation but different.

- ***Digital*** means based on large datasets of human behavior, for example
  produced by the Web and social media.
- ***Computerized*** means the quantitative analysis of data in an automated,
  tractable, repeatable and extensible fashion.
- ***Generative*** means the application of data and results to the design of
  agent-based models that explain complex social phenomena and motivate
  interventions.

These three meanings organize the rest of this session. We will first look at
digital behavioral data, then at the new computerized methods, and finally at
agent-based modeling as the generative meaning.

The definition of "computerized" makes four demands on an analysis:

- **Automated** means that there is no manual step that you cannot describe.
- **Tractable** means that the analysis finishes in reasonable time, as we
  learned in the Time Complexity session.
- **Repeatable** means that someone else who runs your code gets your numbers.
- **Extensible** means that the next study can build on it.

These four are properties of your code and not of your data, which is why a
social scientist needs the computing concepts of this course.

Before the field matured, there was a phase of pure enthusiasm about data. A
satirical Urban Dictionary entry for "data piñata" describes it as a big data
method that consists of whacking data with a stick in the hope that some
insights will come out. The cover of Simon Lindgren's book *Data Theory* uses
the same image to make a serious point. The warning is worth taking seriously,
because without a question more data just means more patterns, and most
patterns in a large enough dataset are noise.

---

## 4. The three ages of CSS

Salganik's *Bit by Bit* places CSS on the Gartner hype curve, which is the
typical shape of the reputation of a technology over time. The curve has a
peak of inflated expectations, then a trough of disillusionment, and then a
slope of enlightenment that leads to a plateau of productivity. We can label
the phases of CSS by what people were excited about:

- The **age of data** is the peak. There was enthusiasm about the digital
  traces themselves and their sheer volume, and many believed that they would
  answer every question.
- The **age of theory** is the trough. The field discovered that data without
  a question produces nothing and turned back to social theory to say what it
  is actually measuring.
- The **age of methods** is the recovery. Progress is sustained because it is
  built on developing and validating measurement instruments rather than on
  acquiring more data.

According to this account we are in the third phase, which is an optimistic
reason to take a methods course like this one.

```
hype │      ╱‾╲
     │     ╱   ╲          ╱‾‾‾‾‾▶
     │    ╱     ╲       ╱
     │  ╱         ╲___╱
     └──[ data ]─[theory]─[ methods ]───▶ time
```

---

## 5. Combining disciplines and methods

CSS sits at the intersection of three fields, namely computer science,
mathematics and statistics, and the behavioral and social sciences. A useful
way to remember how two of these approaches differ is that statistics is about
making sound inferences from too little data, while data science is about
making meaningful inferences from too much data. Classical statistics was
built for a situation in which data is expensive and scarce, which is why it
developed significance testing, power analysis and sampling theory. Digital
traces put us in the opposite situation, in which almost every difference is
statistically significant because $n$ is a hundred million, and the hard
problem is to decide what any of it means.

The methods of CSS reinforce each other rather than compete:

- **Large-scale digital traces** give breadth but no ground truth.
- **Survey validation** supplies the ground truth. For example, it answers
  whether a Twitter-based measure of sentiment tracks what people report
  feeling.
- **Computational modeling** turns a verbal theory into something that
  generates predictions.
- **Controlled experiments** establish causality, which observational traces
  cannot do.

None of them is enough on its own and the strongest CSS papers combine at
least two of them, for example digital traces that are validated with a
survey. The third part of the practical Python examples shows this cycle in a
small simulation, in which traces show a pattern, two models state possible
mechanisms and an experiment decides between them.

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

## 6. Digital behavioral data {#digital-data}
Sensors and connectivity are increasingly pervasive and more and more of our
actions happen through digital technologies. For example, we search for a job
online, talk with a family member over the phone, share open source code,
post a video on a social networking site, pay at the supermarket with a
credit card, or chat on a company instant messenger. All of these actions
generate *digital traces* that can be analyzed in social science research.
The key property of such traces is that they are found data and not designed
data, i.e. nobody paid respondents, wrote a questionnaire or drew a sample.
This gives three advantages, because the traces are cheap, they are
longitudinal by default, and they record behavior rather than self-reported
behavior. It also brings one large disadvantage, namely that the people who
leave traces do not represent the population, as we will see after the
research examples.

---

## 7. Four research examples

Let's look at four research examples that use digital traces.

The first example is the detection of earthquakes on Twitter. The comic XKCD
723, *Seismic Waves*, had the idea first. In it, a character can tell that an
earthquake happened elsewhere because the tweets about it arrive before the
seismic wave does. The comic is a joke about messages that travel at the
speed of light while seismic waves travel through rock, but it is also a
research design, which Earle, Bowden and Guy (2012) built. Their Twitter
earthquake detection can produce alerts within a couple of minutes of an
event, which in some cases is faster than the instrumental networks in
regions with sparse sensor coverage. The signal is a sudden spike in the rate
of tweets containing "earthquake" from a geographic region. This works
because humans act as the sensors and there are a lot of them. For the same
reason, the method fails in regions with few users, which is an example of
the representation problem that we discuss below.

The second example is trading and Google Trends. Preis, Moat and Stanley
(2013) studied whether the search volume for finance-related words on Google
Trends relates to stock market movements. They found that the search volume
for terms such as "debt" rose ahead of market falls, and that a trading
strategy based on this signal outperformed a buy-and-hold benchmark in
backtesting. The general idea is that aggregate search behavior measures
collective attention and information seeking before a decision is made, and
it has become a standard instrument of CSS.

The third example is gender inequality with Facebook. Garcia et al. (2018)
used the advertising interface of Facebook, which reports the size of
audiences by gender, age and country. With it they constructed a worldwide
indicator of the gender gap in Facebook use and validated it against
established offline indices of gender inequality in the economy, health and
education. The method is worth noting because the data is not scraped from
users at all. Instead, it is read from a public marketing tool as aggregate
counts. This is a cheap and privacy-preserving way to obtain population-level
measures, and it can be updated monthly while a census is updated every ten
years.

The fourth example uses social media to measure emotions in society, and we
will see it among the method examples below.

---

## 8. Issues with digital data: representation {#digital-data-issues}

The central problem of digital trace data is that the people who produce
them are not the population. Data of the Pew Research Center on the social
media use of US adults by age group shows the size of the gap in the table
below.

| Platform | 18–29 | 65+ | Youngest − oldest |
|---|---|---|---|
| Snapchat | 65% | 2% | **+63** |
| Instagram | 71% | 13% | **+58** |
| YouTube | 95% | 49% | **+46** |
| TikTok | 48% | 4% | **+44** |
| Twitter | 42% | 7% | **+35** |
| Facebook | 70% | 50% | **+20** |

A study of Snapchat is demographically a study of the young. A 63-point gap
cannot be corrected with weights, because the users are a different
population. In addition, the gaps differ by platform, so "social media users"
are not one group either. Lazer et al. (2021), in *Meaningful measures of
human society in the twenty-first century*, argue that this is the central
methodological challenge of the field. They also argue that it needs a
scientific data infrastructure with known coverage properties rather than
clever solutions in each study. We should keep three failure modes separate:

- **Coverage error** means that whole groups are absent from the platform,
  for example most adults over 65 on Snapchat.
- **Behavioral distortion** means that what people do on a platform is shaped
  by the affordances and the audience of the platform, so it is not their
  behavior in general.
- **Algorithmic confounding** means that what you observe is partly the
  product of the ranking algorithm of the platform, which changes without
  notice. A trend in your data may therefore be a trend in the software of
  the company.

The first part of the practical Python examples simulates algorithmic
confounding, with a ranking change that almost doubles the share of posts
about a topic while the users behave the same as before.

---

## 9. New methods: three generations {#new-methods}
Social science data used to have few formats, such as the annotations of
experiment outcomes or survey responses. Now there are many more formats and
data sources, such as text, social networks, locations and timestamps, and
likes, and sometimes these formats are even related to each other. The
methods to handle them have improved over time in three generations:

- The **first generation** adapted previous social science methods. An example
  is the use of dictionaries in text analysis, where you take a hand-built
  list of words scored for a construct and count them. This is transparent
  and cheap, but the measure is only as good as the list.
- The **second generation** uses machine learning models to generalize
  measurement from many examples of measurements. An example is sentiment
  analysis, where you label a few thousand texts and train a classifier to
  reproduce your labeling on millions more, as we learned in the Machine
  Learning session.
- The **third generation** uses large models to analyze highly dimensional
  data. An example is word embeddings, which are treated in the document
  analysis course.

Across the three generations, the methods move from rules that you write to
patterns learned from data. This gains coverage and nuance but loses
transparency, so you have to validate the instrument because you can no
longer read it.

---

## 10. Method examples {#method-examples}

The first example is VADER sentiment analysis. Hutto and Gilbert (2014) built
VADER, which stands for Valence Aware Dictionary and sEntiment Reasoner. It
is a rule-based model tuned specifically for social media text. VADER is a
first-generation method because it has a lexicon at its core, but it adds
rules for the features of social media text:

- **Negation**, because "not good" does not mean "good".
- **Intensifiers**, because "very good" is more than "good".
- **Punctuation**, because "good!!!" is more than "good".
- **Capitalization**, because "GOOD" is more than "good".
- **Emoticons and slang**, which are frequent in social media text.

The lexicon itself was built by asking crowdworkers to rate each term, so the
scores are empirical and do not depend on the intuition of one author. VADER
demonstrates that a well-designed simple method can match a machine-learned
one on the domain it was built for, with the large advantage that you can
read its rules.

The second example is social media emotion macroscopes. Garcia, Pellert,
Lasser and Metzler (2021), in *Social media emotion macroscopes reflect
emotional experiences in society at large*, address the main objection to the
examples above. Does aggregated social media sentiment measure anything real?
They answered this question with validation against surveys, by comparing
time series of text-derived emotion with population surveys of self-reported
affect. The finding is that aggregate signals do track the emotional
experience of society, while individual-level inferences are far weaker. This
asymmetry is a general lesson. An instrument can be reliable at the
population level and useless at the person level, because the errors average
out over many people but not for a single person.

The third example is personality and Facebook likes. Youyou, Kosinski and
Stillwell (2015) showed in *Computer-based personality judgments are more
accurate than those made by humans* that, using only the Facebook likes of a
person, a model predicted their self-reported Big Five personality traits
more accurately than the friends of the person could, and, with about 300
likes, more accurately than their spouse. This result is a methodological
success and a privacy problem at the same time, which is the topic we turn to
next.

---

## 11. Issues with methods: privacy

Kosinski, Stillwell and Graepel (2013), in *Private traits and attributes are
predictable from digital records of human behavior*, showed that Facebook
likes, which are individually innocuous, predict sensitive attributes with
high accuracy. These attributes include sexual orientation, ethnicity,
religious and political views, personality traits, intelligence, substance
use and parental separation. Nobody had to disclose those attributes for the
model to infer them. Aggregations of innocuous data are therefore not
innocuous, and no individual consent decision can anticipate this, because
the inference is based on the pattern across thousands of people.

Garcia et al. (2018), in *Collective aspects of privacy in the Twitter social
network*, go one step further. They show that the data of your friends
predicts your attributes even if you are not on the platform at all, which is
called the shadow profile problem. Privacy is therefore not an individual
property that you can protect by your own choices. Instead, it is collective,
because the decision of someone else to share leaks information about you.
For research practice this means that the consent framework inherited from
survey methodology is not sufficient, and that you should consider what your
model can infer in addition to what your data contains.

---

## 12. The end of theory? {#theory}
In 2008 *Wired* published Chris Anderson's essay "The End of Theory: The Data
Deluge Makes the Scientific Method Obsolete", which argued that with enough
data, correlation supersedes causation and models become unnecessary, because
the numbers speak for themselves. The essay is wrong, and we can state the
reasons in the terms of this course:

- **Data does not interpret itself.** Without a theory, you cannot say which
  of the millions of correlations in a large dataset is meaningful.
- **Prediction is not explanation.** Recall Hinton's framing in the Machine
  Learning session, i.e. a model that predicts well has found a pattern but
  not the mechanism. Only a mechanism licenses intervention, so a social
  scientist who wants to change something needs more than a good predictor.
- **Measurement requires theory.** To claim that your variable measures
  polarization you need a theory of what polarization is, so there is no
  theory-free measurement.
- **Sampling bias does not go away with size.** A biased sample of a billion
  is still biased, as we saw with the representation problem, because volume
  reduces variance but not bias.

The version of the same argument in the 2020s is that large language models
make theory unnecessary, and the same counterarguments apply to it.

---

## 13. Agent-based modeling {#agent-based-modeling}

Agent-based modeling is the generative meaning of "computational". It models
humans as agents that symbolize a simplified behavior. The agents have
quantifiable variables and properties, and all the interaction rules are
explicitly defined and parametrized. Simulations and mathematical analysis
can then be applied to derive properties of the system that might not be easy
to conclude from intuition alone.

An agent-based model generates hypotheses and proofs of *generative
sufficiency*, but it does not generate empirical evidence. This means that
the model shows that a proposed micro-mechanism is sufficient to produce an
observed macro-pattern, i.e. that these rules can generate this outcome. It
does not show that this is what happens in the world, because other rules
might generate the same outcome. In Epstein's phrase, if you did not grow it,
you did not explain it. However, growing it is a necessary condition for an
explanation and not a sufficient one. The second part of the practical Python
examples shows this with two different mechanisms that generate the same
unequal popularity of songs.

The requirement that the rules be explicit has a benefit of its own. Writing
a model as code forces you to be explicit, because a verbal theory can hide
an ambiguity indefinitely while a program with an ambiguous rule cannot be
written. This benefit of computational modeling does not depend on any
simulation result.

---

## 14. Schelling's segregation model

The classic example is the segregation model of Thomas Schelling (1971),
*Dynamic Models of Segregation*. The model has agents of two kinds in
similar numbers on a grid with a low but nonzero fraction of empty cells.
Each cell has a neighborhood of the 8 cells around it, while cells at corners
and borders have fewer neighbors. Agents are aware of the fraction $f$ of
similar agents in their neighborhood. They are satisfied when $f \ge F$ and
if they are unsatisfied they jump to the closest satisfying cell. The
parameter $F$ measures intolerance. We can write the model as an algorithm in
the pseudocode of the course:

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

Let's look at a simulation with $F = 0.2$. Here agents are content as long as
one in five of their neighbors is like them, i.e. they are happy in a
neighborhood where they are outnumbered four to one. This is an extremely
tolerant population by any reasonable reading, but the grid still segregates
into large single-color blocks. With $F = 0.6$ the segregation is very
strong. With $F = 0.4$, where agents are satisfied even when they are in the
minority, the grid is also clearly segregated. The point of the model is that
strongly segregated macro-outcomes do not require intolerant
micro-preferences. A mild individual preference not to be completely isolated
is sufficient when it is iterated over many small moves.

The methodological lesson applies far beyond segregation. You cannot infer
individual motives from an aggregate pattern, so observing a segregated city
does not allow you to conclude that its residents are intolerant. This is the
computational counterpart of the ecological fallacy, and it is the idea of
this session that transfers best to other research problems. You can find
more on Schelling's model in the slides of the CMSS course,
<https://dgarcia-eu.github.io/CMSS-Konstanz/02_Segregation/Slides/Slides.html#14>
(slides 14 to 38).

---

## 15. Simulating anti-COVID policies

Lasser, Hell and Garcia (2022), in *Assessment of the Effectiveness of
Omicron Transmission Mitigation Strategies for European Universities Using
an Agent-Based Network Model*, use agent-based modeling for a policy question
that was open at the time. The agents are students and staff. The contact
network comes from actual course enrollment data, i.e. who shares a room with
whom and when, and the disease process is calibrated to the parameters of the
Omicron variant. Then policies such as masking, ventilation, testing
frequency, vaccination coverage and class size caps are simulated and the
sizes of the resulting outbreaks are compared. The value of this approach is
that these interventions cannot be randomized, because you cannot run a
controlled trial of university-wide mask policies during a wave. The model
gives a way to compare counterfactuals with its assumptions written down, so
that other researchers can argue with them. This is the generative
contribution of computational methods. For the same reason, the output of the
model is a hypothesis about mechanisms and not evidence in the sense of a
trial.

---

## 16. Courses outlook {#outlook}
Several courses continue from here:

- ***Deep Learning for the Social Sciences*** has 9 ECTS (2+2 SWS) and is
  taught next summer semester by Giordano De Marzo. It covers machine
  learning concepts, multilayer perceptrons and their limitations,
  convolutional neural networks, recurrent networks, LSTMs and reinforcement
  learning, and applications to time series, graphs, generative modeling and
  natural language processing, with exercises in PyTorch.
- ***Social Media Data Analysis*** has 9 ECTS (2+2 SWS) and will be taught in
  2027 by David Garcia
  (<https://github.com/dgarcia-eu/SocialMediaDataAnalysis>). It covers the
  analysis of search data to measure information seeking, popularity and
  social impact in social media, the application and evaluation of sentiment
  analysis techniques for social media text, and methods and applications of
  social network analysis in online media. It has practical assignments in
  which you get and analyze your own data.
- ***Computational Modelling of Social Systems*** is a seminar with exercises
  of 6 ECTS (2+2 SWS) that will be taught in 2027 by David Garcia
  (<https://github.com/dgarcia-eu/CMSS-Konstanz>). It has lectures and
  exercises on agent-based modeling and complexity science, such as
  Schelling's model of segregation, Axelrod's model of cultures, the
  spreading of behavior, opinion dynamics, network growth models and social
  resilience, with Python exercises in Mesa.

For the path to the master thesis, there are two recommendations. The first
is to take the *Colloquium in Social Data Science* the semester before your
master thesis and to prepare by joining the research updates of the group
(Tuesdays 13:30–15:00). Students prepare their thesis plan during the
semester and present it for input at the end. Registration is manual, so
contact David Garcia beforehand to discuss coursework and potential topics.
The second recommendation is to take the courses of the group and to read its
papers.

---

## 17. Summary

Computational Social Science uses new sources of data and computational
methods in the social sciences, and the word computational has three
meanings, namely digital, computerized and generative. Digital behavioral
data comes from social media, search, mobile phones and more, and its main
risk is representation. The new methods of the social sciences, with text
analysis as the example, bring privacy risks. Finally, the computational
analysis of social science theory uses agent-based modeling to analyze models
of social systems.

The next sessions are the exam review and a Q&A. In them we can discuss any
previous exercise or go back to any slides of the course, and the extra time
will be used for questions about the practical projects. Questions and
requests are collected 24 hours before each session from the form
<https://forms.gle/MXTtQw6FUNpw2qrW9>.

---

## 18. Why does this matter? Practical Python examples

Check the [practical Python examples in this Jupyter notebook](https://github.com/dgarcia-eu/ICSS/blob/main/PythonExamples/Examples13-SocialScienceApplications.ipynb).
There, you will see a trend in platform data that comes from a change in the
ranking algorithm and not from the users, two different mechanisms that
produce the same unequal popularity of songs, and a simulated experiment that
tells the two mechanisms apart.

---

## 19. Check yourself

**1.** A study analyzes 500 million tweets about an election and concludes that the public favors candidate A. Name three separate problems.

<details><summary>Answer</summary>

- **Coverage.** Twitter users are younger, more urban and more politically
  engaged than the electorate. The sample is therefore not the population and
  a larger $n$ does not fix that.
- **Behavioral distortion.** Tweeting about a candidate is not the same as
  voting for them, and posting is dominated by a small hyperactive minority.
  The unit of analysis is the tweet, while the unit of interest is the person.
- **Algorithmic confounding.** What is visible and collectable depends on the
  ranking and the API of the platform, which the researcher does not control.

A fourth problem is that inferring support from text requires a validated
instrument and not just keyword counting.

</details>

**2.** In Schelling's model with F = 0.4, agents prefer to be in the minority. Why does segregation still emerge?

<details><summary>Answer</summary>

Segregation emerges because satisfaction is evaluated locally and
iteratively. An agent that happens to fall below the threshold moves and its
departure changes the composition of its old neighborhood, which can push a
neighbor below the threshold, and so on. These small local adjustments add up
to large-scale sorting. The rule of an agent does not mention the global
pattern, i.e. the pattern is emergent, and this is why you cannot infer
preferences from outcomes.

</details>

**3.** Your agent-based model reproduces an observed macro-pattern. What have you shown, and what have you not?

<details><summary>Answer</summary>

You have shown generative sufficiency, i.e. this set of micro-rules is enough
to produce the pattern. You have not shown that these are the rules that
operate in the world, because other mechanisms may produce the same pattern,
which is called equifinality. You have not produced empirical evidence
either. The model generates a hypothesis that then needs independent testing
with data.

</details>

**4.** Why does the shadow-profile result mean that individual consent is not sufficient for privacy protection?

<details><summary>Answer</summary>

Individual consent is not sufficient because the information about you is
carried by the data of other people. If the likes and connections of your
friends predict your attributes, then your own decision to stay off the
platform does not protect you, and their consent decisions affect your
privacy without your involvement. Privacy is a collective property, so it
needs collective protections such as regulation and institutions in addition
to individual opt-outs.

</details>

**5.** Anderson claimed that with enough data, we no longer need models. Give the strongest version of his argument, then say why it fails.

<details><summary>Answer</summary>

The strongest version is that for many practical purposes, such as
recommending, translating and forecasting, a model that predicts accurately
is all that anyone needs, and modern systems achieve that without any theory
of the domain. This is true in those domains, for example machine translation
works without linguistics. The argument fails for social science because the
goal is usually explanation and intervention rather than prediction. A
predictor tells you what will happen if nothing changes, while a policy is a
change. Moreover, deciding what to measure and claiming that a variable
measures a social construct are theoretical work that data cannot do for you,
and correlations found in a biased sample remain biased at any $n$.

</details>

---

## 20. References

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
  4, and the best single book on the material of this session.
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
