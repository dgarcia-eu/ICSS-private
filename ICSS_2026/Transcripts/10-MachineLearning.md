# Session 10: Machine Learning

*Introduction to Computing for the Social Sciences · lecture transcript*

> Companion text for lecture 10. Notation follows
> [the course conventions](00-Conventions.md).
>
> **Reading for this session:** lecture materials; for going deeper, Hastie,
> Tibshirani & Friedman, *The Elements of Statistical Learning* (2009), free at
> <https://hastie.su.domains/ElemStatLearn/>. References at the end.

---

## Contents

<!-- MOTIVATION-TOC:BEGIN -->
0. [Motivating examples](#motivating-examples)
<!-- MOTIVATION-TOC:END -->
1. [A short history of AI](#1-a-short-history-of-ai)
2. [What machine learning is](#2-what-machine-learning-is)
3. [Supervised learning: the setup](#3-supervised-learning-the-setup)
4. [Features](#4-features)
5. [Error, loss and the traps of accuracy](#5-error-loss-and-the-traps-of-accuracy)
6. [Generalization: the train/test split](#6-generalization-the-traintest-split)
7. [A first model: k nearest neighbors](#7-a-first-model-k-nearest-neighbors)
8. [Overfitting, underfitting, bias and variance](#8-overfitting-underfitting-bias-and-variance)
9. [Two more models: Naive Bayes and the MLP](#9-two-more-models-naive-bayes-and-the-mlp)
10. [Unsupervised learning and clustering](#10-unsupervised-learning-and-clustering)
11. [Generative models and LLMs](#11-generative-models-and-llms)
12. [Ethics and responsible AI](#12-ethics-and-responsible-ai)
13. [Check yourself](#13-check-yourself)
14. [References](#14-references)

---

<!-- MOTIVATION-SECTION:BEGIN -->
## Motivating examples

Three candidate openings for this session, each a real situation the
material is the answer to. **One of these will be used in the lecture**;
the others are kept here because they are worth reading anyway.

<!-- MOTIVATION:M10-A:BEGIN -->
### A · Google predicted the flu, until it didn't

In 2009 *Nature* published a paper that looked like the future of social
measurement. Google Flu Trends estimated influenza-like illness in US regions
from the volume of certain search queries, and it tracked the official
figures of the CDC closely while being available two weeks earlier, because
the data of the CDC depends on doctors filing reports. It was selected from
50 million candidate search terms by finding the 45 that best fitted the CDC
series. And then it broke. It missed the 2009 H1N1 pandemic entirely, a
non-seasonal outbreak; it ran persistently high from 2011; and in the
2012–13 season it predicted more than double the actual rate. The service
was quietly retired in 2015.

The post-mortem by Lazer and colleagues in *Science* named two causes, and
both are squarely in this session. The first is overfitting. Searching 50
million terms for the 45 that best match 128 weekly data points is nearly
guaranteed to find terms that fit the past and mean nothing, and some of the
selected terms had no plausible connection to influenza; they were seasonal
for other reasons, such as the high-school basketball season, which peaks in
winter. The model had learned "it is winter" with great accuracy. A model that
fits the training data almost perfectly is reporting a symptom, not an
achievement, and the standard defense, evaluating on data the model has never
seen, is what this session builds. The second cause is algorithmic
confounding. The measuring instrument was not independent of what it
measured: Google changed its search product repeatedly over the period,
adding suggestions and related-search features that themselves increase the
volume of health-related queries, so the model was partly measuring Google's
own interface changes. This is a problem specific to digital trace data and
has no counterpart in survey methodology, because the platform is not a
passive sensor. The episode does not show that search data is useless; later
work found that Google Flu Trends combined with CDC data outperformed either
alone. What it shows is that a predictive instrument needs the same scrutiny
as any other instrument, validation against something external and a check
that it has not simply memorized the past.

Section 6 of this session is about generalization, why the test set must be
held out before training begins, and what information leakage does to a
reported score. Section 8 is about overfitting and the bias-variance
trade-off, which is the formal version of "45 terms out of 50 million".
Section 5 is about error and loss, and why the number you report depends on
which question you are actually asking. Section 12 is about responsible use,
where algorithmic confounding sits alongside the other ways in which a model
can be confidently wrong. The sentence to leave the session with is that
fitting the past well is evidence of nothing until you have shown that the
model works on data it has never seen.
<!-- MOTIVATION:M10-A:END -->
<!-- MOTIVATION:M10-B:BEGIN -->
### B · 93% accurate, and it never finds anyone

A university wants to identify students at risk of dropping out early enough
to offer support. A model is built, evaluated, and reported as 93% accurate,
and the committee approves it. Seven percent of students drop out. A model
that predicts "will not drop out" for every single student, a model
containing no information whatsoever, is correct 93% of the time. If the
reported model is doing anything at all, the report does not show it, and the
report does not distinguish the two cases. This is class imbalance, and it is
the normal condition rather than a special case: fraud is rare, disease is
rare, hate speech is rare, dropping out is rare. Accuracy weights every case
equally, so it is dominated by the majority class, precisely the class nobody
cares about. The metrics that reveal the problem are all computed on the
minority class. Precision asks, of the students we flagged, how many really
were at risk, $TP/(TP+FP)$; recall asks, of the students really at risk, how
many we caught, $TP/(TP+FN)$; and $F_1$ is the harmonic mean of the two,
$2PR/(P+R)$. The always-"no" model has recall 0, so $F_1 = 0$. The metric
collapses to zero the instant the model stops finding anything, which is
exactly the behavior you want from a metric.

The second half of the question is the one that carries the real weight, and
it has no purely technical answer: precision and recall trade off against
each other, and which one you want depends on what happens next. If flagged
students are automatically enrolled in a mandatory program, a false positive
imposes something unwanted on someone who did not need it, so you optimize
precision. If flagged students are offered an appointment they can decline, a
false positive costs an email, while a false negative is a student who needed
help and was never contacted, so you optimize recall. Same model, same data,
opposite thresholds, decided by the intervention and not by the statistics.
That decision belongs to the people designing the program, which is why it
needs to be stated in terms that a committee can actually discuss.

Section 5 of this session covers error, loss, class imbalance, precision,
recall and $F_1$, with this exact arithmetic worked through. Section 3
presents the supervised setup, so that $TP$ and $FN$ refer to something
concrete. Section 12 is about responsible use: whether a prediction should be
made at all, what happens to the person on the receiving end, and who is
accountable when it is wrong. The rule to carry out is never to report
accuracy alone on imbalanced data, and always to state the base rate
alongside it, so that the reader can see the comparison you should have made
yourself.
<!-- MOTIVATION:M10-B:END -->
<!-- MOTIVATION:M10-C:BEGIN -->
### C · A million speeches nobody can read

Content analysis is one of the oldest methods in the social sciences, and it
does not scale. Two trained coders, a codebook, an intercoder reliability
check, and a sample of a few hundred documents: this is rigorous, well
understood, and it caps out at roughly the number of documents two people can
read. Now the corpus is every Bundestag speech since 1949, around a million
documents. At five minutes each, one person needs about 83 000 hours, some
forty working years, and two coders with double coding make it eighty. The
method that is correct is not available. The obvious move is to sample. Two
thousand speeches, coded properly, is a week's work and supports perfectly
good inference about the population, but it forecloses the questions that
made the corpus interesting: how the rhetoric of one party shifted across a
specific decade, what happened in the three months after a particular event,
how a single speaker changed over a career. Those are questions about
subsets, and a sample of 2 000 has too few documents in any of them.

The move this session is about is different. Instead of using the 2 000
coded documents as the data, use them as examples of the judgment you want
made, and train a model to reproduce that judgment on the other 998 000. That
reframing is the whole of supervised learning: the 2 000 hand-coded speeches
are the training data, pairs of an input $x$, the text, and a label $y$, your
judgment; a model $f$ is fitted so that $f(x) \approx y$ on those examples;
and the model is then applied to documents no human has read. It immediately
raises the question that decides whether the study is any good: how do you
know that the model reproduces your judgment rather than something correlated
with it? Hold out part of your coded data, never let the model see it, and
measure the agreement there. That measurement, not the confidence of the
model and not how sensible the output looks, is your evidence. Two warnings
belong in the same breath, and both are developed later in the session. The
model learns what your coders did, including their systematic mistakes; it
industrializes your codebook, biases and all. And agreement can be high
overall and poor exactly where it matters, on rare categories, on the years
you care about, or on the speeches of one party, so check by subgroup and not
only in aggregate.

Section 3 of this session presents the supervised setup, features, labels,
model and prediction. Section 4 is about features, how a speech becomes
something a model can take as input, and why TF-IDF is a better
representation than raw word counts. Section 6 is about the train/test
split, which is how the question of how you know gets an answer. Section 9
presents the models themselves, starting with Naive Bayes, which is a strong
and interpretable baseline for exactly this task. The framing to keep is
that a supervised model here is a measurement instrument, and instruments
have to be validated. The fact that it was fitted rather than designed
changes nothing about that obligation.
<!-- MOTIVATION:M10-C:END -->
---

<!-- MOTIVATION-SECTION:END -->
## 1. A short history of AI

There is no agreed definition of intelligence, and the lecture offers two
that are commonly used: the problem-solving ability of a system, and "you
know it when you see it", which is the Turing test of session 9. The history
of the field fits in six lines. The foundations were laid in the 1950s, in
parallel in the United States, where the 1956 Dartmouth workshop coined the
term artificial intelligence, and in the Soviet Union, under the name of
cybernetics. In the 1970s the limits of the perceptron, the first learning
machine, led to the first AI winter, a collapse of funding and interest when
the methods did not deliver. The 1980s brought expert systems and the return
of neural networks, the 1990s and 2000s a second AI winter, and the 2010s
deep learning, made possible by compute and data rather than by new ideas.
The 2020s are the decade of the AI bubble, whether or not it bursts. The
pattern is worth noticing: the core ideas of neural networks date from the
1950s to the 1980s, and what changed in the 2010s was the availability of
GPUs, which we will see in session 12, and of large datasets. Sometimes an
idea is waiting for a substrate, which is the same argument we made about
Babbage's engine in session 1.

---

## 2. What machine learning is

There are two historical approaches to artificial intelligence. The first is
the expert system, with hand-coded rules to solve one or more problems. The
second is *machine learning*, which automatically learns how to solve a
problem from data. Expert systems dominated before the 1980s and again in the
early 2000s, but machine learning is now the main approach to artificial
intelligence, and historically it has also been called pattern recognition
and statistical learning. Machine learning trains a *model* from data, and
here lies the vocabulary trap of session 5: the word "algorithm" is often
used to refer to the resulting model and not to the procedure that produced
it. In practice, AI systems may contain expert rules, but they mainly depend
on learning from data.

Machine learning has three families. *Supervised learning* is learning with
labeled examples: the model learns from data where the correct answers are
already known, for example predicting election outcomes from historical
voting data and demographics, and its common tasks are classification and
regression. *Unsupervised learning* is finding hidden patterns: the algorithm
explores data without labels to discover structure and relationships, for
example grouping survey respondents into distinct segments based on their
attitudes, and its common tasks are clustering and dimensionality reduction.
*Reinforcement learning*, which we do not cover, is learning through trial
and error: the algorithm learns by receiving rewards or penalties for its
actions in an environment, for example in adaptive language teaching. The key
distinction is what each needs: supervised learning needs labeled data,
unsupervised learning finds patterns on its own, and reinforcement learning
needs access to an environment to learn from feedback.

---

## 3. Supervised learning: the setup

The goal of supervised learning is to learn a function $f: X \rightarrow Y$
that maps inputs to outputs, using a dataset of example input-output pairs.
On the input side, the *features* $X$ are the input variables used to make
predictions, also called predictors, independent variables or covariates,
for example age, income and education level; a *feature vector* $x$ is a
single observation with all its features, such as `x = [35, $50k,
Bachelor's]`; and the *training data* is a collection of $n$ examples $(x_1,
y_1), \dots, (x_n, y_n)$. On the output side, the *target* $Y$ is the
outcome we want to predict, also called label, response or dependent
variable, for example a voting choice or mortality; the *prediction*
$\hat{y} = f(x)$ is the output of the model for a given input; and the
*model* $f$ is the learned function that makes the predictions. The hat in
$\hat{y}$ always means estimated, and keeping $y$ and $\hat{y}$ apart in your
notation is not pedantry, because almost every concept below is about the
difference between them.

Supervised tasks come in two kinds. In *classification*, $Y$ is categorical,
for example true or false, or a label, and an error is binary: you get the
right class or you do not. In *regression*, $Y$ is a continuous number, for
example an income or a probability, and errors can be measured with a
number. That distinction determines which loss function you can use, which
is the subject of [section 5](#5-error-loss-and-the-traps-of-accuracy).

---

## 4. Features

*Features* are the measurable properties or characteristics we use to
describe our data; they are the input variables that the algorithm uses to
learn patterns and make predictions. Think of features as the questions we
ask about each data point. In social science they are things like age,
education and income, and in text analysis word counts, sentence length or
sentiment scores. *Feature engineering* is the process of creating, selecting
and transforming features to improve the performance of a model, that is,
deciding which features to use and how to represent them. Instead of just
word counts, we might create features for word combinations (bigrams), for
the ratio of positive to negative words, or for the presence of exclamation
marks.

TF-IDF is the worked example of the lecture. The problem with simple word
counts is that words like "the", "and" and "is" appear frequently in every
document but tell us nothing about, say, sentiment, while distinctive words
like "amazing" or "terrible" are very informative. TF-IDF, which stands for
term frequency times inverse document frequency, gives each word a score that
balances how often it appears in a document with how rare it is across all
documents:

$$\text{TF} = \frac{\text{count of word}}{\text{total words in document}},
\qquad
\text{IDF} = \log \frac{\text{total documents}}{\text{documents with word}},
\qquad
\text{TF-IDF} = \text{TF} \times \text{IDF}.$$

Read the IDF carefully. If a word appears in every document, the ratio is 1
and the logarithm is 0, so the word gets a score of zero no matter how often
it occurs; if it appears in one document out of a thousand, the logarithm is
large. Words that are frequent in a document but rare overall get high
scores. This is a nice example of feature engineering doing real work: the
same text, represented differently, becomes far more learnable. The exercise
of the lecture is to guess the highest and lowest TF-IDF scores in the review
cards of the previous slide.

---

## 5. Error, loss and the traps of accuracy

The *error* is the difference between what the model predicted and the true
value for a single example, $\hat{y} - y$. The *loss* is a function that
measures the total error across all the examples in the dataset, an average
of the errors with different formulas depending on the task, and the goal of
training is to minimize the loss. The lecture works through five film
reviews:

| Review | True $y$ | Predicted $\hat{y}$ | Correct? | Error |
|---|---|---|---|---|
| "Amazing film!" | 1 | 1 | ✓ | 0 |
| "Terrible movie" | 0 | 1 | ✗ | 1 |
| "Loved it!" | 1 | 1 | ✓ | 0 |
| "Boring film" | 0 | 0 | ✓ | 0 |
| "Not good" | 0 | 1 | ✗ | 1 |

There are 2 errors out of 5, so the error rate, also called the 0-1 loss, is
$2/5 = 40\%$ and the accuracy is 60%. For regression the usual losses are
the mean squared error and the mean absolute error, and for probabilities the
cross-entropy.

*Class imbalance* occurs when one class appears much more frequently than
the others in the dataset, and it is extremely common in real-world
problems: fraud detection has 99% legitimate transactions and 1% fraud, rare
disease diagnosis 95% healthy and 5% sick, hate speech detection 90% normal
posts and 10% hate speech. Accuracy is misleading under class imbalance. Take
1 000 social media posts, 900 normal and 100 hate speech, and a naive model
that always predicts "normal". It is correct on 900 of the 900 normal posts
and on 0 of the 100 hate speech posts, so its accuracy is 90%. It looks great
and it detects zero hate speech. The issue is that accuracy treats all
classes equally, so a model can achieve high accuracy by predicting the
majority class every time, completely ignoring the minority class we actually
care about.

The metrics that reveal the problem are computed on the minority class.
*Precision* asks, of the posts we flagged as hate speech, how many actually
were, and *recall* asks, of all the actual hate speech, how much we caught:

$$\text{precision} = \frac{TP}{TP + FP}, \qquad \text{recall} = \frac{TP}{TP + FN}, \qquad F_1 = \frac{2 \cdot P \cdot R}{P + R},$$

where $TP$, $FP$ and $FN$ are the numbers of true positives, false positives
and false negatives, and the $F_1$ score is the harmonic mean of precision
$P$ and recall $R$. Check the naive model against these: its recall is 0, so
$F_1 = 0$, and the metric catches immediately what accuracy hid. The reason
for the harmonic mean rather than the arithmetic one is that it punishes
imbalance: a model with precision 1.0 and recall 0.0 has an arithmetic mean of
0.5 and a harmonic mean of 0, and 0 is the honest answer. In multi-class
problems, $F_1$ can be computed for each class separately; the
*macro-average* $F_1$ is the mean of the per-class scores, and the
*micro-average* $F_1$ is a single score over all classifications together, so
that larger classes weigh more. Which one you report matters, because the
macro average treats a rare class as equally important and the micro average
does not.

---

## 6. Generalization: the train/test split

The ultimate goal of machine learning is generalization. We do not just want
a model that memorizes the training data; we want a model that performs well
on new, unseen data from the real world, and that is what makes machine
learning valuable. To evaluate generalization we split our data into two
separate sets before training begins. The *training set*, typically 70 to
80% of the data, is used to train the model, and the algorithm learns
patterns from it; it is like the practice exams of a student. The *test
set*, the remaining 20 to 30%, is held back from training and used only to
evaluate the final performance; it is like the final exam, never seen before.
The critical rule is that the test set must remain completely separate and
unseen during training.

*Information leakage* happens when the train/test split is not well
separated. Typical sources are using the test set for feature engineering,
for example by choosing which words to keep by looking at the whole corpus,
and ignoring correlations between samples, for example power users or
high-activity periods in social media data. If the same user appears in both
sets, the model can recognize the user rather than the phenomenon, and the
test score is a fiction. That second source is the trap in social science
data specifically, and it is worth stating as a rule: split by the unit of
dependence, not by row. *Cross-validation* partitions the data into many
train/test splits and reports the average performance; it uses the data more
efficiently and gives a sense of the variance of the estimate.

---

## 7. A first model: k nearest neighbors

To classify a point $x$ in a 0/1 task with $k$ nearest neighbors, look at
the $k$ training points closest to $x$ and take the average of their labels,

$$\hat{Y}(x) = \frac{1}{k} \sum_{x_i \in N_k(x)} y_i,$$

where $N_k(x)$ is the set of the $k$ nearest neighbors of $x$, and predict
the class 1 if the average is above one half. That is the whole model. There
is no training beyond storing the data, which is why kNN is the cleanest
possible illustration of the next section. With $k = 15$ the decision
boundary of the example from Hastie et al. is smooth, because each prediction
averages fifteen neighbors and individual noisy points cannot move it much.
With $k = 1$ the boundary is jagged: every training point is classified
correctly by definition, since its nearest neighbor is itself, and the
boundary wraps around every outlier. The exercise of the lecture is to extend
the model to more than two classes.

---

## 8. Overfitting, underfitting, bias and variance

The lecture shows the misclassification curves of kNN from Hastie et al.,
with a training set of 200 points and a test set of 10 000, plotted against
$k$. Models with a very high $k$, around 100, have high training and test
errors, because the model is too simple to capture the pattern; this is
*underfitting*, and the error is called *bias*. Models with a very low $k$,
around 1, have a very low training error but a high test error, because the
model has memorized the training set, including its noise; this is
*overfitting*, and the error is called *variance*. Stated generally in terms
of *model complexity*, for example the number of parameters, the training
error falls monotonically as complexity rises, because a more flexible model
can always fit the training data better, while the test error falls and then
rises again. Minimizing the training error is therefore a mistake that leads
to high variance, and the *bias-variance tradeoff* is the observation that a
middle range of complexity gives the lowest possible test error. This is the
single most important idea of the lecture, and it is not specific to machine
learning: it is the same reason why a regression with one predictor per
observation fits perfectly and predicts nothing.

---

## 9. Two more models: Naive Bayes and the MLP

Naive Bayes is the example of a linear model. In Bayesian classification, for
a feature vector $x = (x_1, \dots, x_d)$ the predicted class is the one with
the highest posterior probability,

$$\hat{y} = \arg\max_{c \in C} P(Y = c \mid X = x),$$

and applying Bayes' theorem, and dropping the denominator because it does not
depend on $c$,

$$\hat{y} = \arg\max_{c \in C} P(X = x \mid Y = c) \cdot P(Y = c).$$

The *naive independence assumption* is that the features are independent of
each other given the class, which lets us decompose the joint probability
into a product of individual feature probabilities:

$$\hat{y} = \arg\max_{c \in C} P(Y = c) \cdot \prod_{j=1}^{d} P(X_j = x_j \mid Y = c),$$

where $\hat{y}$ is the predicted class, $Y$ the class variable, $C$ the set of
all possible classes, $X = (X_1, \dots, X_d)$ the feature vector with $d$
features, $P(Y = c)$ the prior probability of class $c$, and $P(X_j = x_j \mid
Y = c)$ the likelihood of feature $j$ having the value $x_j$ given the class
$c$. The assumption is obviously false for text, since "New" and "York" are
not independent, and Naive Bayes works well anyway; a model can be wrong in
its assumptions and still be useful for prediction. Naive Bayes is a linear
model because its decision boundary can be written as a hyperplane in the
feature space $X$.

The multi-layer perceptron (MLP) is the example of a nonlinear model. It is
inspired by how neurons work: each unit computes a linear combination of its
inputs followed by a nonlinear activation function. The features are the
inputs of the first layer, the final output is a class or a probability, and
the complexity of the model grows with the number of hidden layers, since
more layers mean more parameters. Fitting the model means finding the
connection weights that minimize the loss, and being nonlinear, the model
can fit more than just a hyperplane separating the classes. Connect this
back to section 8: adding layers adds parameters, which moves you to the
right on the complexity axis, and deep networks are exactly the regime where
overfitting is a constant concern.

---

## 10. Unsupervised learning and clustering

*Unsupervised learning* finds structures or patterns in data without a
target variable that we try to predict. In supervised learning we have pairs
of feature vectors $X$ and target values $Y$, but in unsupervised learning we
only have the feature vectors $X$. Its typical tasks are *clustering*,
partitioning the data into $K$ groups where elements are similar within
groups; *dimensionality reduction*, transforming $X$ into a low-dimensional
space that maintains similarity or variance, as in principal component
analysis; *density estimation*, learning the underlying distribution of the
data values; and *association discovery*, finding correlations or
co-occurrence patterns. The example of the lecture is document topics: given
a large collection of unlabeled documents, such as articles, tweets,
research papers or survey responses, we want to automatically discover the
main topics and group similar documents together, and this is unsupervised
because we do not know in advance what topics exist or which documents
belong to which topic.

The algorithm of the lecture is *K-means*, in the form given by Hastie et
al. (2009, algorithm 14.1). Write $C(i)$ for the cluster assigned to
observation $i$, $N_k$ for the number of observations in cluster $k$, and
$m_k$ for the mean of cluster $k$. The algorithm alternates two steps. For a
given cluster assignment $C$, it minimizes the total cluster variance with
respect to the means $\{m_1, \dots, m_K\}$, which means setting each cluster
mean to the average of its members; then, given the means, it assigns each
observation to the closest current cluster mean,

$$C(i) = \arg\min_{1 \le k \le K} \|x_i - m_k\|^2,$$

and it repeats the two steps until the assignments do not change. The
quantity being minimized is the total cluster variance,

$$\min_{C, \{m_k\}} \sum_{k=1}^{K} N_k \sum_{C(i)=k} \|x_i - m_k\|^2,$$

which weighs each cluster by its size. Each step can only decrease the
objective, so the algorithm always converges, but to a local minimum, which
is why K-means is usually run several times with different starting points.

To choose $K$ we assume that there is a natural number of clusters: too small
a $K$ merges distinct groups and too large a $K$ splits real groups apart.
The *elbow method* plots the within-cluster sum of squares,

$$\text{WSS} = \sum_{k=1}^{K} \sum_{C(i)=k} \| x_i - m_k \|^2,$$

against $K$. Note that WSS is the same sum as the objective above without the
weights $N_k$, which is the version usually plotted. WSS always falls as $K$
grows, and with $K = n$ it is zero, so you cannot simply minimize it; the
elbow is the point after which additional clusters barely reduce the WSS,
because before it each new cluster buys a lot and after it almost nothing.
The elbow method is a heuristic, not a test. It often gives an ambiguous
plot, and that ambiguity is honest information, because sometimes there is
no natural $K$.

---

## 11. Generative models and LLMs

*Predictive* models aim to predict just one variable $Y$, while *generative*
models aim to produce new examples of data points $X$. For text, a
predictive or discriminative model represents the conditional probability of
a label given the text, $P(y \mid x)$, for example $P(\text{sentiment} =
\text{positive} \mid \text{"I loved this movie"})$. A generative model
represents the probability of the text itself, $P(x)$, or the probability of
the next token given the previous ones, $P(x_t \mid x_1, \dots, x_{t-1})$,
for example $P(\text{"movie"} \mid \text{"I loved this"})$; a model that
predicts the next token from the previous ones is called *autoregressive*.

Large language models are trained with exactly this objective, next-word
prediction. Simplified, the process is to collect massive amounts of text, to
create training examples in which, for each position, the previous words are
the input and the next word is the target, to train a neural network by
updating billions of parameters to minimize the prediction error, and to
repeat this trillions of times until the model has learned the patterns of
the language. Notice that this is supervised learning with labels that cost
nothing to produce, because the text supplies its own targets, and that is
the trick that made scale possible. As the lecture notes, some of the slides
of this session were co-created with Claude, which works because the lecturer
already knows what Claude should say.

The person of this session is Geoffrey Hinton (born 1947), a
British-Canadian cognitive psychologist and computer scientist whose
pioneering work on neural networks laid the foundation for modern AI,
including generative models like ChatGPT, DALL-E and Stable Diffusion. He
received the 2018 Turing Award with Bengio and LeCun and the 2024 Nobel Prize
in Physics for neural networks. Hinton describes AI as a kind of intuition
rather than intelligence: our intuition discovers patterns that we cannot
explain and that might not be useful for intervention or design, but it is a
very useful tool for creativity and prediction. That framing is worth taking
seriously for research: a model that predicts well has found a pattern, not
necessarily the mechanism, and only a mechanism lets you intervene.

---

## 12. Ethics and responsible AI

The lecture closes with six questions worth asking before deploying any
model. Can we use a model for this prediction at all? Historical training
data for unemployment benefits, for example, encodes historical decisions,
including discriminatory ones. What features are allowed for the prediction?
It is against human rights to use ethnicity as a predictor of criminality.
Who are we generalizing for? Computer vision models that fail to detect
non-white faces are a direct consequence of their training sets. Under which
conditions was the data gathered? The authors of texts did not express
agreement with their writing being used to train generative text models,
with a loss of labor as consequence. Can we trust an AI model? People have a
right to an explanation of a prediction, and credit scores are the classic
case. And who is responsible for the mistakes of a model? *Responsible AI*
is not just about preventing harm, but about preventing AI from shifting
power to the already powerful; it compels us toward AI development, but
safely.

The appendix of the lecture collects cautionary cases worth knowing: Clever
Hans, a horse that appeared to do arithmetic and was reading the posture of
its trainer, the original example of a model learning the wrong feature; the
double descent phenomenon; "one parameter is always enough", the
demonstration that a single real number with enough digits can fit any
dataset; the adversarial 3D-printed turtle classified as a rifle from every
angle; Microsoft Tay; the prediction of sensitive attributes from Facebook
likes; and shadow profiles.

---

## 13. Check yourself

**1.** Your classifier has 97% accuracy on a dataset where 97% of cases are negative. What do you report instead?

<details><summary>Answer</summary>

Precision, recall and $F_1$ on the positive class, and the confusion matrix.
The 97% is consistent with a model that never predicts positive at all. Also
report the base rate, so that the reader can see the comparison.

</details>

**2.** Why is a train/test split not enough when your data has repeated users?

<details><summary>Answer</summary>

Because random row-wise splitting puts the same user in both sets, so the
model can learn to recognize the user rather than the phenomenon, and the
test performance is then optimistic. Split by user, that is, group-wise, and
not by row.

</details>

**3.** kNN with k = 1 has zero training error. Is it a good model?

<details><summary>Answer</summary>

No. Zero training error is the symptom, not the achievement. Every point is
its own nearest neighbor, so the training error is trivially zero while the
test error is high. This is the purest example of overfitting.

</details>

**4.** You raise K in K-means from 3 to 10 and WSS falls. Is the clustering better?

<details><summary>Answer</summary>

Not necessarily. WSS falls monotonically with $K$ by construction and
reaches zero at $K = n$. The question is whether the fall is steep, which
makes the extra clusters worth it, or gradual, which does not, and that is
what the elbow method looks at. No plot substitutes for asking whether the
clusters mean anything substantively.

</details>

**5.** Naive Bayes assumes features are independent given the class. For text this is clearly false. Why use it?

<details><summary>Answer</summary>

Because the assumption only has to be good enough to get the ranking of the
classes right, not the probabilities. Errors from the false assumption often
affect all classes similarly and cancel in the $\arg\max$. It is fast, needs
little data, and is a strong baseline, so always run it before something
complicated.

</details>

---

## 14. References

- **Hastie, T., Tibshirani, R. & Friedman, J. (2009).** *The Elements of
  Statistical Learning*, 2nd ed. Springer. Free at
  <https://hastie.su.domains/ElemStatLearn/>. Source of the kNN figures
  (chapter 2), the bias-variance curve (chapter 7) and the K-means algorithm
  and formulas (chapter 14).
- **Bishop, C. M. (2006).** *Pattern Recognition and Machine Learning*.
  Springer.
  <https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/>
- **Russell, S. & Norvig, P. (2021).** *Artificial Intelligence: A Modern
  Approach*, 4th ed. Pearson. The standard reference for section 1.
- **Salton, G. & Buckley, C. (1988).** "Term-weighting approaches in
  automatic text retrieval". *Information Processing & Management* 24(5),
  513–523. TF-IDF.
- **Wikipedia, *Precision and recall*:**
  <http://en.wikipedia.org/wiki/Precision_and_recall>. Source of the diagram
  in section 5.
- **Vaswani, A. et al. (2017).** "Attention Is All You Need". *Advances in
  Neural Information Processing Systems* 30. The transformer architecture
  behind current LLMs.
- **Buolamwini, J. & Gebru, T. (2018).** "Gender Shades: Intersectional
  Accuracy Disparities in Commercial Gender Classification". *Proceedings of
  Machine Learning Research* 81, 77–91. The "who are we generalizing for?"
  question of section 12, with data.
- **Kosinski, M., Stillwell, D. & Graepel, T. (2013).** "Private traits and
  attributes are predictable from digital records of human behavior". *PNAS*
  110(15), 5802–5805. The appendix cases; also session 13.
- **Athalye, A., Engstrom, L., Ilyas, A. & Kwok, K. (2018).** "Synthesizing
  Robust Adversarial Examples". *ICML*. The 3D-printed turtle.
- **Belkin, M., Hsu, D., Ma, S. & Mandal, S. (2019).** "Reconciling modern
  machine-learning practice and the classical bias-variance trade-off".
  *PNAS* 116(32), 15849–15854. The double descent of the appendix.
- **Boué, L. (2019).** "Real numbers, data science and chaos: How to fit any
  dataset with a single parameter". *arXiv:1904.12320*.
