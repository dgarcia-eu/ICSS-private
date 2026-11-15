# Session 11: Machine Learning

<style>
figure, .figure, .float { margin: 1.4em 0 1.8em 0; }
figure img, .float img { display: block; max-width: 100%; }
figcaption, .figcaption, .figure p.caption { margin-top: 0.3em; font-size: 0.88em; color: #555; }
details { margin: -0.5em 0 2.2em 0; }
</style>

*Introduction to Computing for the Social Sciences · lecture transcript*

**Reading for this session:** lecture materials. For going deeper, Hastie,
Tibshirani & Friedman, *The Elements of Statistical Learning* (2009), free at
<https://hastie.su.domains/ElemStatLearn/>. References at the end.

---

## Contents

1. [A brief history of AI and machine learning](#history)
2. [Supervised machine learning](#supervised)
3. [Unsupervised machine learning](#unsupervised)
4. [Generative AI and ML nowadays](#generative)

---

<!-- MOTIVATION-SECTION:BEGIN -->
## Motivating examples

<!-- MOTIVATION:M11-A:BEGIN -->
### A · Google predicted the flu, until it didn't

In 2009 *Nature* published a paper that looked like the future of social
measurement. Google Flu Trends estimated influenza-like illness in US regions
from the volume of certain search queries. It tracked the official figures of
the CDC closely while being available two weeks earlier, because the data of
the CDC depends on doctors filing reports. The model was built by searching
50 million candidate search terms for the 45 that best fitted the CDC series.
However, the model stopped working after a few years. First, it missed the
2009 H1N1 pandemic, which was a non-seasonal outbreak. Then its estimates
were persistently too high from 2011 on, and in the 2012–13 season it
predicted more than double the actual rate. The service was retired in 2015.

Lazer and colleagues analyzed the failure in *Science* and named two causes.
The first cause is overfitting. If you search 50 million terms for the 45
that best match 128 weekly data points, you are nearly guaranteed to find
terms that fit the past by chance. Some of the selected terms had no
plausible connection to influenza and were seasonal for other reasons, for
example searches about high-school basketball, whose season peaks in winter.
The model had therefore learned to detect winter rather than flu. A model
that fits the training data almost perfectly should make you suspicious, and
the standard defense is to evaluate the model on data that it has never seen.
The second cause is algorithmic confounding, i.e. the measuring instrument
was not independent of what it measured. Google changed its search product
repeatedly over the period by adding suggestions and related-search features
that increase the volume of health-related queries, so the model was partly
measuring the changes of Google's own interface. This problem is specific to
digital trace data and has no counterpart in survey methodology, because a
platform changes the behavior that it records. The episode does not show that
search data is useless, because later work found that Google Flu Trends
combined with CDC data outperformed either of them alone. Rather, it shows
that a predictive model needs the same scrutiny as any other measuring
instrument, namely validation against something external and a check that it
has not simply memorized the past.

In this session you will learn about generalization, i.e. why the test set
must be held out before training begins and what information leakage does to
a reported score. We will also learn about overfitting and the bias-variance
tradeoff, which explain what goes wrong when 45 terms are chosen out of 50
million. If you fit a model to your own data, a good fit to the past is not
evidence that the model works until you have tested it on data that it has
never seen.

<!-- MOTIVATION:M11-A:END -->
<!-- MOTIVATION:M11-B:BEGIN -->
### B · 93% accurate, and it never finds anyone

A university wants to identify students at risk of dropping out early enough
to offer them support. A model is built and evaluated, the report says that
it is 93% accurate, and the committee approves it. However, only seven
percent of the students drop out. This means that a model that predicts "will
not drop out" for every single student is also correct 93% of the time,
although it contains no information at all. The report does not let us
distinguish the approved model from this useless one. This problem is called
class imbalance and it is the normal condition in many applications, because
fraud, disease, hate speech and dropping out are all rare. Accuracy weights
every case equally, so it is dominated by the majority class, which is
usually the class that we are less interested in. The metrics that reveal the
problem are computed on the minority class:

- **Precision** is the fraction of the students we flagged who really were at
  risk, i.e. $TP/(TP+FP)$.
- **Recall** is the fraction of the students really at risk that we flagged,
  i.e. $TP/(TP+FN)$.
- **$F_1$** is the harmonic mean of the two, i.e. $2PR/(P+R)$.

The model that always answers "no" has a recall of 0, so its $F_1$ is also 0.
The metric drops to zero as soon as the model stops finding anyone, and this
is the behavior that we want from a metric in this case.

Which metric should have been on the report? This question has no purely
technical answer, because precision and recall trade off against each other
and which one you want depends on what happens after a student is flagged. If
flagged students are automatically enrolled in a mandatory program, a false
positive imposes something unwanted on someone who did not need it, so you
optimize precision. If flagged students are offered an appointment that they
can decline, a false positive costs only an email, while a false negative is
a student who needed help and was never contacted, so you optimize recall.
The same model and the same data lead to opposite thresholds, and the choice
is decided by the intervention rather than by the statistics. That decision
belongs to the people who design the program, so the report has to state it
in terms that a committee can discuss.

In this session you will learn about error, loss, class imbalance, precision,
recall and $F_1$, and we will work through this arithmetic with an example.
We will also learn about the responsible use of models, i.e. whether a
prediction should be made at all, what happens to the person who receives it
and who is accountable when it is wrong. When you evaluate a model on
imbalanced data yourself, do not report accuracy alone and state the base
rate next to it, so that the reader can make the comparison.

<!-- MOTIVATION:M11-B:END -->
<!-- MOTIVATION:M11-C:BEGIN -->
### C · A million speeches nobody can read

Content analysis is one of the oldest methods in the social sciences, but it
does not scale. A typical study has two trained coders, a codebook, an
intercoder reliability check and a sample of a few hundred documents. This
method is rigorous and well understood, but it is limited to roughly the
number of documents that two people can read. Now imagine that the corpus is
every Bundestag speech since 1949, which is around a million documents. At
five minutes per speech, one person needs about 83,000 hours, i.e. some forty
working years, and two coders with double coding need eighty. The correct
method is therefore not feasible. The obvious alternative is to take a
sample. Coding two thousand speeches properly is a week of work and it
supports good inference about the whole population of speeches. However, a
sample cannot answer the questions that made the corpus interesting, for
example how the rhetoric of one party shifted across a specific decade, what
happened in the three months after a particular event, or how a single
speaker changed over a career. Those are questions about subsets, and a
sample of 2,000 has too few documents in each of them.

Machine learning offers a different approach. Instead of using the 2,000
coded documents as the data, we can use them as examples of the judgment that
we want and train a model to reproduce that judgment on the other 998,000.
This is the idea of supervised learning. The 2,000 hand-coded speeches are
the training data, i.e. pairs of an input $x$, which is the text, and a label
$y$, which is your judgment. A model $f$ is fitted so that $f(x) \approx y$
on those examples, and the model is then applied to documents that no human
has read. How do you know that the model reproduces your judgment rather than
something correlated with it? You hold out part of your coded data, never let
the model see it, and measure the agreement between the model and the coders
there. Your evidence is that measurement and neither the confidence of the
model nor how sensible its output looks. There are two warnings to keep in
mind. First, the model learns what your coders did, including their
systematic mistakes, so it applies your codebook with its biases to a million
documents. Second, the agreement can be high overall and poor where it
matters, for example on rare categories, on the years you are interested in
or on the speeches of one party. Therefore, you should check the agreement by
subgroup and not only in aggregate.

In this session you will learn about the supervised setup with its features,
labels, model and predictions, and how a speech becomes something that a
model can take as input. We will also learn about the train/test split, which
answers the question of how you know, and about models such as Naive Bayes,
which is a strong and interpretable baseline for this task. If you use a
supervised model in your research, treat it as a measurement instrument that
has to be validated like any other, even though it was fitted rather than
designed.

<!-- MOTIVATION:M11-C:END -->

---

<!-- MOTIVATION-SECTION:END -->
## 1. A short history of AI {#history}
There is no agreed definition of intelligence, but two definitions are
commonly used. The first is the problem-solving ability of a system. The
second is "you know it when you see it", which is the idea of the Turing test
that we saw in the Theoretical Computer Science session. The history of the
field can be summarized in six periods:

- In the **1950s**, the foundations were laid in parallel in the United
  States, where the 1956 Dartmouth workshop coined the term artificial
  intelligence, and in the Soviet Union under the name of cybernetics.
- In the **1970s**, the limits of the perceptron, which was the first
  learning machine, led to the first AI winter, i.e. a collapse of funding
  and interest when the methods did not deliver what was expected.
- In the **1980s**, expert systems became popular and neural networks
  returned.
- The **1990s and 2000s** were a second AI winter.
- In the **2010s**, deep learning became possible thanks to compute and data
  rather than to new ideas.
- The **2020s** are the decade of the AI bubble, and we do not know yet
  whether it will burst.

The core ideas of neural networks date from the 1950s to the 1980s. What
changed in the 2010s was the availability of large datasets and of GPUs,
which we will learn about in the Parallel Programming session. An idea
sometimes has to wait until the hardware that it needs exists, as happened
with Babbage's engine in the Introduction session.

---

## 2. What machine learning is

There are two historical approaches to artificial intelligence. The first is
the expert system, which has hand-coded rules to solve one or more problems.
The second is *machine learning*, which automatically learns how to solve a
problem from data. Expert systems dominated before the 1980s and again in the
early 2000s, but machine learning is now the main approach to artificial
intelligence. Historically, it has also been called pattern recognition and
statistical learning. Machine learning trains a *model* from data. Be careful
with the vocabulary here, because the word "algorithm" is often used to refer
to the resulting model and not to the procedure that produced it, which is
the meaning that we used in the Algorithms session. In practice, AI systems
may contain expert rules, but they mainly depend on learning from data.

Machine learning has three families:

- *Supervised learning* is learning with labeled examples, which means that
  the model learns from data where the correct answers are already known. An
  example is predicting election outcomes from historical voting data and
  demographics. Its common tasks are classification and regression.
- *Unsupervised learning* is finding hidden patterns, i.e. the algorithm
  explores data without labels to discover structure and relationships. An
  example is grouping survey respondents into distinct segments based on
  their attitudes. Its common tasks are clustering and dimensionality
  reduction.
- *Reinforcement learning* is learning through trial and error, i.e. the
  algorithm learns by receiving rewards or penalties for its actions in an
  environment, for example in adaptive language teaching. We do not cover it
  in this session.

The key distinction between the three families is what each one needs.
Supervised learning needs labeled data, unsupervised learning finds patterns
on its own, and reinforcement learning needs access to an environment to
learn from feedback.

---

## 3. Supervised learning: the setup {#supervised}
The goal of supervised learning is to learn a function $f: X \rightarrow Y$
that maps inputs to outputs, using a dataset of example input-output pairs.
The input side has three terms:

- The *features* $X$ are the input variables used to make predictions, for
  example age, income and education level. They are also called predictors,
  independent variables or covariates.
- A *feature vector* $x$ is a single observation with all its features, such
  as `x = [35, $50k, Bachelor's]`.
- The *training data* is a collection of $n$ examples $(x_1, y_1), \dots,
  (x_n, y_n)$.

The output side has three more terms:

- The *target* $Y$ is the outcome we want to predict, for example a voting
  choice or mortality. It is also called label, response or dependent
  variable.
- The *prediction* $\hat{y} = f(x)$ is the output of the model for a given
  input.
- The *model* $f$ is the learned function that makes the predictions.

The hat in $\hat{y}$ always means estimated. It is important to keep $y$ and
$\hat{y}$ apart in your notation, because almost every concept below is about
the difference between them.

Supervised tasks come in two kinds. In *classification*, $Y$ is categorical,
for example true or false or a label, and an error is binary, i.e. you either
get the right class or you do not. In *regression*, $Y$ is a continuous
number, for example an income or a probability, and errors can be measured
with a number. This distinction determines which loss function you can use,
as we will see when we define error and loss.

---

## 4. Features

*Features* are the measurable properties or characteristics that we use to
describe our data. They are the input variables that the algorithm uses to
learn patterns and make predictions. You can think of features as the
questions that we ask about each data point. In social science they are
things like age, education and income, while in text analysis they are word
counts, sentence length or sentiment scores. *Feature engineering* is the
process of creating, selecting and transforming features to improve the
performance of a model, i.e. deciding which features to use and how to
represent them. For example, instead of using just word counts we might
create features for word combinations (bigrams), for the ratio of positive to
negative words or for the presence of exclamation marks.

Let's see how this works with TF-IDF, which is a common way to build features
from text. The problem with simple word counts is that words like "the",
"and" and "is" appear frequently in every document but tell us nothing about
its sentiment, while distinctive words like "amazing" or "terrible" are very
informative. TF-IDF stands for term frequency times inverse document
frequency. It gives each word a score that balances how often the word
appears in a document with how rare it is across all documents:

$$\text{TF} = \frac{\text{count of word}}{\text{total words in document}},
\qquad
\text{IDF} = \log \frac{\text{total documents}}{\text{documents with word}},
\qquad
\text{TF-IDF} = \text{TF} \times \text{IDF}.$$

To understand the IDF, consider two cases. If a word appears in every
document, the ratio is 1 and the logarithm is 0, so the word gets a score of
zero no matter how often it occurs. If a word appears in one document out of
a thousand, the logarithm is large. Therefore, words that are frequent in a
document but rare overall get high scores. TF-IDF shows what feature
engineering is for, because the same text becomes much easier to learn from
when it is represented differently. As an exercise, take a few short film
reviews and guess which words have the highest and the lowest TF-IDF scores.

---

## 5. Error, loss and the traps of accuracy {#error-and-loss}

The *error* is the difference between what the model predicted and the true
value for a single example, i.e. $\hat{y} - y$. The *loss* is a function that
measures the total error across all the examples in the dataset. It is an
average of the errors, with different formulas depending on the task, and the
goal of training is to minimize the loss. Let's calculate it for an example
of five film reviews:

| Review | True $y$ | Predicted $\hat{y}$ | Correct? | Error |
|---|---|---|---|---|
| "Amazing film!" | 1 | 1 | ✓ | 0 |
| "Terrible movie" | 0 | 1 | ✗ | 1 |
| "Loved it!" | 1 | 1 | ✓ | 0 |
| "Boring film" | 0 | 0 | ✓ | 0 |
| "Not good" | 0 | 1 | ✗ | 1 |

There are 2 errors out of 5, so the error rate, which is also called the 0-1
loss, is $2/5 = 40\%$ and the accuracy is 60%. For regression the usual
losses are the mean squared error and the mean absolute error, while for
probabilities the usual loss is the cross-entropy.

*Class imbalance* occurs when one class appears much more frequently than
the others in the dataset, and it is extremely common in real-world
problems. For example, fraud detection has 99% legitimate transactions and
1% fraud, rare disease diagnosis has 95% healthy and 5% sick people, and hate
speech detection has 90% normal posts and 10% hate speech. Accuracy is
misleading under class imbalance. Take 1,000 social media posts, of which 900
are normal and 100 are hate speech, and a naive model that always predicts
"normal". This model is correct on 900 of the 900 normal posts and on 0 of
the 100 hate speech posts, so its accuracy is 90%. The number looks great,
but the model detects zero hate speech. The issue is that accuracy treats all
classes equally, so a model can achieve high accuracy by predicting the
majority class every time while it completely ignores the minority class that
we actually care about.

The metrics that reveal the problem are computed on the minority class.
*Precision* is the fraction of the posts we flagged as hate speech that
actually were hate speech, and *recall* is the fraction of all the actual
hate speech that we caught:

$$\text{precision} = \frac{TP}{TP + FP}, \qquad \text{recall} = \frac{TP}{TP + FN}, \qquad F_1 = \frac{2 \cdot P \cdot R}{P + R},$$

where $TP$, $FP$ and $FN$ are the numbers of true positives, false positives
and false negatives, and the $F_1$ score is the harmonic mean of precision
$P$ and recall $R$. We can check the naive model against these metrics. Its
recall is 0, so $F_1 = 0$, which shows immediately what accuracy hid. $F_1$
uses the harmonic mean rather than the arithmetic one because the harmonic
mean penalizes an imbalance between precision and recall. For example, a
model with precision 1.0 and recall 0.0 has an arithmetic mean of 0.5 and a
harmonic mean of 0, and 0 is the better description of a model that finds
nothing. In multi-class problems, $F_1$ can be computed for each class
separately. The *macro-average* $F_1$ is the mean of the per-class scores,
while the *micro-average* $F_1$ is a single score over all classifications
together, so that larger classes weigh more. It matters which one you report,
because the macro average treats a rare class as equally important as a
frequent one and the micro average does not. The third part of the practical
Python examples shows a model that is about 95% accurate and still misses
most of the positive cases.

---

## 6. Generalization: the train/test split

The ultimate goal of machine learning is generalization. We do not just want
a model that memorizes the training data. Instead, we want a model that
performs well on new, unseen data from the real world, because this is what
makes machine learning valuable. To evaluate generalization we split our data
into two separate sets before training begins:

- The *training set* is typically 70 to 80% of the data and it is used to
  train the model, i.e. the algorithm learns patterns from it. It is like the
  practice exams of a student.
- The *test set* is the remaining 20 to 30%. It is held back from training
  and used only to evaluate the final performance, so it is like the final
  exam that the student has never seen before.

The critical rule is that the test set must remain completely separate and
unseen during training.

*Information leakage* happens when the train/test split is not well
separated. There are two typical sources of leakage. The first is using the
test set for feature engineering, for example by choosing which words to keep
by looking at the whole corpus. The second is ignoring correlations between
samples, for example power users or high-activity periods in social media
data. If the same user appears in both sets, the model can recognize the user
rather than the phenomenon, and then the test score overestimates how well
the model works on new users. This second source is especially common in
social science data, so a good rule is to split by the unit of dependence,
for example by user, instead of by row. The second part of the practical
Python examples shows how leakage through feature selection produces an
accuracy of 91% on data that contains no information.

*Cross-validation* partitions the data into many train/test splits and
reports the average performance. It uses the data more efficiently and gives
a sense of the variance of the estimate.

---

## 7. A first model: k nearest neighbors

To classify a point $x$ in a 0/1 task with $k$ nearest neighbors (kNN), we
look at the $k$ training points closest to $x$ and take the average of their
labels,

$$\hat{Y}(x) = \frac{1}{k} \sum_{x_i \in N_k(x)} y_i,$$

where $N_k(x)$ is the set of the $k$ nearest neighbors of $x$. We predict the
class 1 if the average is above one half. This is the whole model and it
needs no training beyond storing the data, which makes kNN a simple model to
illustrate overfitting and underfitting. With $k = 15$ the decision boundary
of the example from Hastie et al. is smooth, because each prediction averages
fifteen neighbors and individual noisy points cannot move it much. With
$k = 1$ the boundary is jagged. Every training point is classified correctly
by definition, since its nearest neighbor is itself, and so the boundary goes
around every outlier. As an exercise, think about how to extend the model to
more than two classes.

---

## 8. Overfitting, underfitting, bias and variance

Let's look at the misclassification curves of kNN from Hastie et al., which
plot the error against $k$ for a training set of 200 points and a test set of
10,000. Models with a very high $k$, around 100, have high training and test
errors, because the model is too simple to capture the pattern. This is
called *underfitting*, and the error is called *bias*. Models with a very low
$k$, around 1, have a very low training error but a high test error, because
the model has memorized the training set including its noise. This is called
*overfitting*, and the error is called *variance*.

We can state this more generally in terms of *model complexity*, for example
the number of parameters. The training error falls monotonically as
complexity rises, because a more flexible model can always fit the training
data better, while the test error first falls and then rises again.
Minimizing the training error is therefore a mistake that leads to high
variance. The *bias-variance tradeoff* is the observation that a middle range
of complexity gives the lowest possible test error. This is the most
important idea of this session and it is not specific to machine learning.
For example, a regression with one predictor per observation fits its data
perfectly but predicts new observations badly for the same reason. The first
part of the practical Python examples reproduces these curves with kNN on
simulated data.

---

## 9. Two more models: Naive Bayes and the MLP

Naive Bayes is our example of a linear model. In Bayesian classification, for
a feature vector $x = (x_1, \dots, x_d)$ the predicted class is the one with
the highest posterior probability,

$$\hat{y} = \arg\max_{c \in C} P(Y = c \mid X = x),$$

and then, by applying Bayes' theorem and dropping the denominator because it
does not depend on $c$,

$$\hat{y} = \arg\max_{c \in C} P(X = x \mid Y = c) \cdot P(Y = c).$$

The *naive independence assumption* is that the features are independent of
each other given the class, which lets us decompose the joint probability
into a product of individual feature probabilities:

$$\hat{y} = \arg\max_{c \in C} P(Y = c) \cdot \prod_{j=1}^{d} P(X_j = x_j \mid Y = c),$$

where $\hat{y}$ is the predicted class, $Y$ the class variable, $C$ the set of
all possible classes, $X = (X_1, \dots, X_d)$ the feature vector with $d$
features, $P(Y = c)$ the prior probability of class $c$, and $P(X_j = x_j \mid
Y = c)$ the likelihood of feature $j$ having the value $x_j$ given the class
$c$. The assumption is clearly false for text, for example because "New" and
"York" are not independent, but Naive Bayes often works well anyway. This
shows that a model can be wrong in its assumptions and still be useful for
prediction. Naive Bayes is a linear model because its decision boundary can
be written as a hyperplane in the feature space $X$.

The multi-layer perceptron (MLP) is our example of a nonlinear model. It is
inspired by how neurons work, because each unit computes a linear combination
of its inputs followed by a nonlinear activation function. The features are
the inputs of the first layer and the final output is a class or a
probability. The complexity of the model grows with the number of hidden
layers, since more layers mean more parameters. Fitting the model means
finding the connection weights that minimize the loss. Because the model is
nonlinear, it can fit more than just a hyperplane separating the classes.
This connects to the bias-variance tradeoff, because adding layers adds
parameters and therefore increases the complexity of the model, so
overfitting is a constant concern in deep networks.

---

## 10. Unsupervised learning and clustering {#unsupervised}
*Unsupervised learning* finds structures or patterns in data without a
target variable that we try to predict. In supervised learning we have pairs
of feature vectors $X$ and target values $Y$, but in unsupervised learning we
only have the feature vectors $X$. Its typical tasks are the following:

- *Clustering* is partitioning the data into $K$ groups where elements are
  similar within groups.
- *Dimensionality reduction* is transforming $X$ into a low-dimensional space
  that maintains similarity or variance, as in principal component analysis.
- *Density estimation* is learning the underlying distribution of the data
  values.
- *Association discovery* is finding correlations or co-occurrence patterns.

An example of clustering is finding the topics of documents. Given a large
collection of unlabeled documents, such as articles, tweets, research papers
or survey responses, we want to automatically discover the main topics and
group similar documents together. This task is unsupervised because we do not
know in advance what topics exist or which documents belong to which topic.

A common clustering algorithm is *K-means*, which we present in the form
given by Hastie et al. (2009, algorithm 14.1). We write $C(i)$ for the
cluster assigned to observation $i$, $N_k$ for the number of observations in
cluster $k$, and $m_k$ for the mean of cluster $k$. The algorithm alternates
two steps. First, for a given cluster assignment $C$, it minimizes the total
cluster variance with respect to the means $\{m_1, \dots, m_K\}$, which means
setting each cluster mean to the average of its members. Then, given the
means, it assigns each observation to the closest current cluster mean,

$$C(i) = \arg\min_{1 \le k \le K} \|x_i - m_k\|^2,$$

and it repeats the two steps until the assignments do not change. The
quantity being minimized is the total cluster variance,

$$\min_{C, \{m_k\}} \sum_{k=1}^{K} N_k \sum_{C(i)=k} \|x_i - m_k\|^2,$$

which weighs each cluster by its size. Each step can only decrease this
quantity, so the algorithm always converges. However, it converges to a local
minimum, so K-means is usually run several times with different starting
points.

To choose $K$ we assume that there is a natural number of clusters, because
too small a $K$ merges distinct groups and too large a $K$ splits real groups
apart. The *elbow method* plots the within-cluster sum of squares,

$$\text{WSS} = \sum_{k=1}^{K} \sum_{C(i)=k} \| x_i - m_k \|^2,$$

against $K$. Note that WSS is the same sum as the objective above without the
weights $N_k$, and it is the version that is usually plotted. WSS always
falls as $K$ grows and it is zero with $K = n$, so you cannot simply minimize
it. The elbow is the point after which additional clusters barely reduce the
WSS, i.e. each new cluster before the elbow reduces the WSS a lot and each
new cluster after it reduces the WSS very little. The elbow method is a
heuristic and not a statistical test. The plot is often ambiguous, which can
mean that the data has no natural $K$.

---

## 11. Generative models and LLMs {#generative}
*Predictive* models aim to predict just one variable $Y$, while *generative*
models aim to produce new examples of data points $X$. For text, a
predictive or discriminative model represents the conditional probability of
a label given the text, $P(y \mid x)$, for example $P(\text{sentiment} =
\text{positive} \mid \text{"I loved this movie"})$. A generative model
represents the probability of the text itself, $P(x)$, or the probability of
the next token given the previous ones, $P(x_t \mid x_1, \dots, x_{t-1})$,
for example $P(\text{"movie"} \mid \text{"I loved this"})$. A model that
predicts the next token from the previous ones is called *autoregressive*.

Large language models are trained with this objective, i.e. predicting the
next word. In a simplified way, the training process has four steps:

1. **Collect text.** Massive amounts of text are gathered.
2. **Create training examples.** For each position in the text, the previous
   words are the input and the next word is the target.
3. **Train a neural network.** Billions of parameters are updated to minimize
   the prediction error.
4. **Repeat.** This is done trillions of times until the model has learned
   the patterns of the language.

Notice that this is supervised learning with labels that cost nothing to
produce, because the text supplies its own targets. This is what made
training at such a scale possible. Some of the slides of this session were
co-created with Claude, which only works when you already know what Claude
should say.

An important person in this field is Geoffrey Hinton (born 1947), a
British-Canadian cognitive psychologist and computer scientist whose
pioneering work on neural networks laid the foundation for modern AI,
including generative models like ChatGPT, DALL-E and Stable Diffusion. He
received the 2018 Turing Award with Bengio and LeCun and the 2024 Nobel Prize
in Physics for neural networks. Hinton describes AI as a kind of intuition
rather than intelligence. Our intuition discovers patterns that we cannot
explain and that might not be useful for intervention or design, but it is a
very useful tool for creativity and prediction. This view is useful for
research, because a model that predicts well has found a pattern but not
necessarily the mechanism behind it, and you need the mechanism to know what
an intervention will do.

---

## 12. Ethics and responsible AI

There are six questions that we should ask before deploying any model:

- **Can we use a model for this prediction at all?** For example, historical
  training data for unemployment benefits encodes historical decisions,
  including discriminatory ones.
- **What features are allowed for the prediction?** For example, it is
  against human rights to use ethnicity as a predictor of criminality.
- **Who are we generalizing for?** Computer vision models that fail to detect
  non-white faces are a direct consequence of their training sets.
- **Under which conditions was the data gathered?** The authors of texts did
  not agree to their writing being used to train generative text models,
  which can lead to a loss of their labor.
- **Can we trust an AI model?** People have a right to an explanation of a
  prediction, for example of their credit score.
- **Who is responsible for the mistakes of a model?** Someone has to be
  accountable when a prediction is wrong.

*Responsible AI* is not just about preventing harm but also about preventing
AI from shifting power to the already powerful. It asks us to keep developing
AI but to do it safely.

There are several cautionary cases worth knowing, which you can find in the
appendix of the slides. The first is Clever Hans, a horse that appeared to do
arithmetic but was actually reading the posture of its trainer, which is the
original example of a model learning the wrong feature. Two more are the
double descent phenomenon and "one parameter is always enough", i.e. the
demonstration that a single real number with enough digits can fit any
dataset. The remaining ones are the adversarial 3D-printed turtle that was
classified as a rifle from every angle, Microsoft Tay, the prediction of
sensitive attributes from Facebook likes, and shadow profiles.

---

## 13. Why does this matter? Practical Python examples

Check the [practical Python examples in this Jupyter notebook](https://github.com/dgarcia-eu/ICSS/blob/main/PythonExamples/Examples11-MachineLearning.ipynb).
There, you will see a kNN model that fits its training data perfectly and
predicts badly, a classifier that scores 91% on random data because its
feature selection used the test set, and a model that is 95% accurate and
misses most of the cases we care about.

---

## 14. Check yourself

**1.** Your classifier has 97% accuracy on a dataset where 97% of cases are negative. What do you report instead?

<details><summary>Answer</summary>

You report precision, recall and $F_1$ on the positive class together with
the confusion matrix, because the 97% is consistent with a model that never
predicts positive at all. You should also report the base rate, so that the
reader can make the comparison.

</details>

**2.** Why is a train/test split not enough when your data has repeated users?

<details><summary>Answer</summary>

A random split by rows puts the same user in both sets, so the model can
learn to recognize the user rather than the phenomenon and the test
performance is then too optimistic. Instead, you should split by user, i.e.
group-wise.

</details>

**3.** kNN with k = 1 has zero training error. Is it a good model?

<details><summary>Answer</summary>

No, because zero training error is a symptom of overfitting in this case.
Every point is its own nearest neighbor, so the training error is trivially
zero while the test error is high.

</details>

**4.** You raise K in K-means from 3 to 10 and WSS falls. Is the clustering better?

<details><summary>Answer</summary>

Not necessarily, because WSS falls monotonically with $K$ by construction and
reaches zero at $K = n$. The elbow method looks at whether the fall is steep,
which makes the extra clusters worthwhile, or gradual, which does not. In
addition, you should always ask whether the clusters mean anything
substantively, because no plot can answer that.

</details>

**5.** Naive Bayes assumes features are independent given the class. For text this is clearly false. Why use it?

<details><summary>Answer</summary>

The assumption only has to be good enough to rank the classes correctly,
while the probabilities themselves can be wrong. Errors from the false
assumption often affect all classes similarly and cancel in the $\arg\max$.
Naive Bayes is also fast, needs little data and is a strong baseline, so it
is a good idea to run it before trying a more complicated model.

</details>

---

## 15. References

- **Hastie, T., Tibshirani, R. & Friedman, J. (2009).** *The Elements of
  Statistical Learning*, 2nd ed. Springer. Free at
  <https://hastie.su.domains/ElemStatLearn/>. Source of the kNN figures
  (chapter 2), the bias-variance curve (chapter 7) and the K-means algorithm
  and formulas (chapter 14).
- **Bishop, C. M. (2006).** *Pattern Recognition and Machine Learning*.
  Springer.
  <https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/>
- **Russell, S. & Norvig, P. (2021).** *Artificial Intelligence: A Modern
  Approach*, 4th ed. Pearson. The standard reference for the history of AI.
- **Salton, G. & Buckley, C. (1988).** "Term-weighting approaches in
  automatic text retrieval". *Information Processing & Management* 24(5),
  513–523. TF-IDF.
- **Wikipedia, *Precision and recall*:**
  <http://en.wikipedia.org/wiki/Precision_and_recall>. Source of the
  precision and recall diagram in the slides.
- **Vaswani, A. et al. (2017).** "Attention Is All You Need". *Advances in
  Neural Information Processing Systems* 30. The transformer architecture
  behind current LLMs.
- **Buolamwini, J. & Gebru, T. (2018).** "Gender Shades: Intersectional
  Accuracy Disparities in Commercial Gender Classification". *Proceedings of
  Machine Learning Research* 81, 77–91. The "who are we generalizing for?"
  question of the ethics section, with data.
- **Kosinski, M., Stillwell, D. & Graepel, T. (2013).** "Private traits and
  attributes are predictable from digital records of human behavior". *PNAS*
  110(15), 5802–5805. The prediction of sensitive attributes from Facebook
  likes, also covered in the Social Science Applications session.
- **Athalye, A., Engstrom, L., Ilyas, A. & Kwok, K. (2018).** "Synthesizing
  Robust Adversarial Examples". *ICML*. The 3D-printed turtle.
- **Belkin, M., Hsu, D., Ma, S. & Mandal, S. (2019).** "Reconciling modern
  machine-learning practice and the classical bias-variance trade-off".
  *PNAS* 116(32), 15849–15854. The double descent of the appendix.
- **Boué, L. (2019).** "Real numbers, data science and chaos: How to fit any
  dataset with a single parameter". *arXiv:1904.12320*.
