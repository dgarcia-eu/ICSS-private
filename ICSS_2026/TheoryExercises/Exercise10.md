# Exercise Sheet 10: Machine Learning

*Introduction to Computing for the Social Sciences · Prof. Dr. David Garcia*

> Exercises 1–3 are worked through in the exercise session. The *Additional
> practice* section is for self-study. Worked solutions to every exercise, with
> pointers to the slides and the handout sections that cover the material, are
> in [`Solutions/Exercise10-Solutions.md`](Solutions/Exercise10-Solutions.md); try before you open them.
> Notation: [course conventions](../Transcripts/00-Conventions.md).

---

## Exercise 1: Evaluating a classifier

A research group builds a classifier to detect hate speech in social media posts.
They evaluate it on a test set of 1000 posts, of which 100 are actually hate
speech. The results are:

|  | Predicted: hate speech | Predicted: normal |
|---|---|---|
| **Actually hate speech** | 60 | 40 |
| **Actually normal** | 30 | 870 |

a) Compute the **accuracy**, **precision**, **recall** and **F1 score** of the
   classifier. Show your calculations.

b) A colleague proposes a much simpler classifier that always predicts "normal".
   Compute the same four metrics for it; if one of them is not defined, say so
   and explain why. Which classifier looks better under which metric, and why?

c) The group wants to use the classifier to automatically delete posts. Would you
   advise them to optimize for precision or for recall? What if instead they want
   to use it to flag posts for a human moderator to review? Justify both answers.

d) The group reports that "the model is 93% accurate". Write two sentences
   explaining to a non-technical reader why that number alone is not informative
   here.

---

## Exercise 2: Training, testing and overfitting

A team has a dataset of 5000 tweets, each labeled by a human as positive or
negative. They want to train a classifier and report how well it performs.

a) Describe how they should split the data, and explain **why** the test set must
   not be touched during training.

b) The team builds their feature set by looking at which words are most strongly
   associated with the labels **across the whole dataset**, and then trains and
   tests with a 80/20 split. What is wrong with this procedure, and what would
   the consequence be for the reported performance?

c) The dataset contains tweets from 300 users, and some users contributed more
   than 100 tweets each. The team splits the tweets at random. Explain the
   problem and describe a better splitting strategy.

d) The team tries a $k$ nearest neighbors classifier and finds that with $k = 1$
   the training error is 0% while the test error is 31%. With $k = 50$ the
   training error is 24% and the test error is 26%. Explain both results in terms
   of **bias** and **variance**, and say which model you would choose.

---

## Exercise 3: Clustering

A researcher has survey responses from 2000 people on 12 attitude items and wants
to identify groups of respondents with similar attitude profiles. They decide to
use K-means.

a) Is this supervised or unsupervised learning? Justify your answer by saying
   what plays the role of $X$ and of $Y$.

b) Write the pseudocode of the K-means algorithm, following the course
   conventions for pseudocode.

c) The researcher computes the within-cluster sum of squares for
   $K = 1, 2, \dots, 10$ and obtains:

   | $K$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
   |---|---|---|---|---|---|---|---|---|---|---|
   | WSS | 8400 | 5100 | 3200 | 2900 | 2700 | 2560 | 2440 | 2340 | 2250 | 2170 |

   Which $K$ would you choose, and why? Explain why simply choosing the $K$ with
   the lowest WSS is not an option.

d) The researcher runs K-means twice with $K = 4$ and gets two different
   clusterings. Explain why this can happen and what to do about it.

> For (b), remember that K-means alternates two steps until nothing changes. Be
> explicit about the stopping condition, an algorithm that does not say when it
> stops is not an algorithm (session 5).

---

## Additional practice

### A1. Features and TF-IDF

A small corpus has 4 documents. The word *crisis* appears 3 times in document 1,
which has 100 words in total, and appears in 2 of the 4 documents. The word *the*
appears 6 times in document 1 and in all 4 documents.

a) Compute the TF, IDF and TF-IDF of *crisis* and of *the* in document 1 (use the
   natural logarithm).
b) Explain in one sentence why the result is what feature engineering is for.
c) Give two examples of engineered features for a task of detecting sarcasm in
   tweets, and say what each one is meant to capture.

### A2. Naive Bayes by hand

A spam filter is trained on 100 emails: 40 spam, 60 not spam. In the spam emails
the word *free* appears in 24 of them and the word *meeting* in 2. In the
non-spam emails *free* appears in 6 and *meeting* in 30.

a) Estimate $P(Y = \text{spam})$, $P(\text{free} \mid \text{spam})$ and the other
   three conditional probabilities.
b) Using Naive Bayes, classify an email that contains both *free* and *meeting*.
   Show the two scores.
c) Which assumption did you use in (b), and why is it questionable here?
d) What would happen if the word *free* had never appeared in a non-spam email,
   and how is that usually fixed?

### A3. Bias and variance

For each situation, say whether the model is more likely to be **underfitting**
or **overfitting**, and what you would change.

a) Training error 2%, test error 30%.
b) Training error 28%, test error 30%.
c) A decision tree grown until every leaf contains a single training example.
d) A linear regression fitted to data that clearly follows a U-shape.
e) A neural network with 10 million parameters trained on 500 examples.

### A4. kNN by hand

Six labeled points in one dimension:

| $x$ | 1 | 2 | 4 | 7 | 8 | 10 |
|---|---|---|---|---|---|---|
| $y$ | A | A | B | A | B | B |

a) Classify $x = 5$ with $k = 1$, $k = 3$ and $k = 5$.
b) Which value of $k$ gives the smoothest decision boundary, and why?
c) What is the training error of the $k = 1$ classifier on these six points?
d) kNN requires no training. What is the cost of that?

### A5. Macro vs micro F1

A classifier assigns news articles to three topics. On the test set:

| Topic | Support | Precision | Recall |
|---|---|---|---|
| Politics | 800 | 0.90 | 0.95 |
| Economy | 150 | 0.70 | 0.60 |
| Culture | 50 | 0.40 | 0.30 |

a) Compute the F1 score of each topic.
b) Compute the macro-average F1.
c) Explain why a micro-average would be considerably higher, and which one you
   would report if all three topics matter equally.

### A6. Supervised, unsupervised, or neither

For each research task, say which family of machine learning it belongs to, and
name the specific task type (classification, regression, clustering,
dimensionality reduction).

a) Predicting a country's GDP next year from this year's indicators.
b) Grouping parliamentary speeches into themes without a predefined list.
c) Deciding whether a tweet is about climate change, given 5000 labeled tweets.
d) Reducing 40 survey items to a small number of underlying attitude dimensions.
e) Training a robot to walk by rewarding forward movement.

### A7. Ethics of prediction

For each proposed system, name the main ethical problem from the lecture's list
and say what you would ask the developers.

a) A model predicting recidivism, trained on historical arrest records.
b) A face recognition system for university entrance, trained on a public
   photo dataset.
c) A model that predicts students' final grades in week 2 and routes low
   predictions to a "support track".
d) An LLM trained on the full text of a newspaper archive without asking the
   journalists.

---

## Sources

- There was no 2024 theory sheet for this session; this sheet is new, built from
  the lecture slides and the references below.
- **Hastie, T., Tibshirani, R. & Friedman, J. (2009).** *The Elements of
  Statistical Learning*, 2nd ed. Springer. Free at
  <https://hastie.su.domains/ElemStatLearn/>, ch. 2 (kNN and the bias–variance
  tradeoff: exercise 2d, A3, A4), ch. 7 (model assessment: exercise 2), ch. 14.3
  (K-means: exercise 3).
- **Bishop, C. M. (2006).** *Pattern Recognition and Machine Learning*. Springer.
  Naive Bayes and smoothing (A2).
- **Manning, C. D., Raghavan, P. & Schütze, H. (2008).** *Introduction to
  Information Retrieval*. Cambridge University Press.
  <https://nlp.stanford.edu/IR-book/>: TF-IDF (A1) and the evaluation measures
  of exercise 1.
- **Wikipedia, *Precision and recall*:**
  <http://en.wikipedia.org/wiki/Precision_and_recall>, used in the lecture and
  in exercise 1.
- **Buolamwini, J. & Gebru, T. (2018).** "Gender Shades". *FAccT*.: A7(b).
- **Angwin, J. et al. (2016).** "Machine Bias". *ProPublica*.: A7(a).
