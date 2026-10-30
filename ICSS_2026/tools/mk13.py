OUT = "/home/dgarcia/Dropbox/Teaching/Konstanz/ICSS-local/ICSS_2026/Slides/13-SocialScienceApplications/ICSS-2026-13-SocialScienceApplications.qmd"
s = ['''---
title: "<span class='course'>Introduction to Computing for the Social Sciences</span><br><span class='session'>Session 13 &ndash; Social Science Applications</span>"
author: "David Garcia<br><span class='semester'>Winter Semester 2026-2027</span>"
format:
  revealjs:
    theme: [default, ../theme/unikn.scss]
    width: 1280
    height: 720
    margin: 0.06
    center: false
    slide-number: c
    show-slide-number: all
    progress: true
    controls: true
    history: true
    logo: ../theme/unikn-logo.png
    footer: "<span class='fbar-left'>Session 13</span><span class='fbar-mid'>Introduction to Computing for the Social Sciences</span><span class='fbar-right'>Winter Semester 2026-2027</span>"
    highlight-style: github
    link-external-newwindow: true
    fig-align: left
---

## Course Outline

:::: {.columns}
::: {.column width="50%"}
::: {.sm}
- Session 1: Introduction
- Session 2: Information Coding
- Session 3: Data Structures
- Session 4: Software
- Session 5: Algorithms
- Session 6: Recursion
- Session 7: Sorting Algorithms
:::
:::

::: {.column width="50%"}
::: {.sm}
- Session 8: Time Complexity
- Session 9: Theoretical Computer Science
- Session 10: Machine Learning
- Session 11: Databases
- Session 12: Parallel Programming
- Session 13: Social Science Applications
  - Thursday: Exercises & exam recap
- Session 14: Exam Review: Lectures recap
:::
:::
::::
''']

def sl(t, b): s.append(f"\n## {t}\n\n{b}\n")

ITEMS = ["Computational Social Science",
         "Digital Behavioral Data in the Social Sciences",
         "New Methods in the Social Sciences",
         "Computational Analysis of Social Science Theory",
         "Courses Outlook"]
def outline(cur=None, last="Courses Outlook"):
    items = ITEMS[:-1] + [last]
    m = [f"[{t}]{{.current}}" if i+1 == cur else t for i, t in enumerate(items)]
    cls = "{.outline .focus}" if cur else "{.outline}"
    return "::: " + cls + "\n" + "\n".join(f"- {t}" for t in m) + "\n:::"

sl("Overview", outline())

sl("Computational Social Science (CSS)", """::: {.definition}
[Computational Social Science]{.label}
Quantitative testing of theories from the social sciences at unprecedented breadth, depth and scale. (Lazer et al., *Science*, 2009)
:::

:::: {.columns}
::: {.column width="48%"}
::: {.sm}
- Using new, large-scale data to inform social science theory
- Quantitative and empirical, not just theoretical
- Not data-driven studies: **interdisciplinary research**
:::

::: {.source}
[Computational social science. D Lazer, A Pentland, L Adamic, S Aral, AL Barabási… *Science*, 2009](https://www.science.org/doi/10.1126/science.1167742)
:::
:::

::: {.column width="52%"}
![](figures/p04-1.jpg){height="7.4em"}
:::
::::""")

sl("Buzzwords related to Computational Social Science", """::: {.definition}
[Social Data Science]{.label}
Focus on new methods to study human behavior and society rather than on testing or developing social science theory. Almost a synonym of CSS.
:::

::: {.definition}
[Web Science]{.label}
Study of the Web as a socio-technical system. Empirical studies but also computer science methods development.
:::

::: {.definition}
[Digital Sociology]{.label}
Sociology of the digital transformation and social phenomena affected by the new use of Information and Communication Technology.
:::""")

sl("Computational in Computational Social Science", """::: {.sm}
It can have three meanings, all related to computation but different:
:::

::: {.definition}
[Digital]{.label}
Based on large datasets of human behavior, for example produced by the Web and social media.
:::

::: {.definition}
[Computerized]{.label}
The quantitative analysis of data in an automated, tractable, repeatable and extensible fashion.
:::

::: {.definition}
[Generative]{.label}
Application of data and results to the design of agent-based models that explain complex social phenomena and motivate interventions.
:::""")

FULL = [
    (7, "Early data-driven CSS", "11.4em", None),
    (8, "The Gartner Hype Curve of CSS", "10.6em",
     "*Bit by Bit: Social Research in the Digital Age.* Matthew Salganik, 2017"),
    (9, "The Three Ages of CSS", "10.6em", None),
    (10, "Combining Disciplines and Methods in CSS", "11.4em", None),
    (11, "Combining Disciplines and Methods in CSS", "11.4em", None),
]
for page, title, h, src in FULL:
    ext = "jpg" if page in (7, 10, 11) else "png"
    srcline = f"\n\n::: {{.source}}\n{src}\n:::" if src else ""
    sl(title, f"""::: {{.center-h}}
![](figures/p{page:02d}-1.{ext}){{height="{h}"}}
:::{srcline}""")

sl("Digital Behavioral Data in the Social Sciences", outline(2))

sl("Sensors and connectivity are increasingly pervasive", """::: {.center-h}
![](figures/p13-1.jpg){height="11.6em"}
:::""")

sl("Digital Behavioral Data in the Social Sciences", """:::: {.columns}
::: {.column width="58%"}
::: {.sm}
More and more of our actions happen through digital technologies, e.g.:

- Searching for a job online
- Talking with a family member over the phone
- Sharing open source code
- Posting a video on a social networking site
- Paying at the supermarket with a credit card
- Chatting on a company instant messenger
:::
:::

::: {.column width="42%"}
![](figures/p14-1.png){height="7.4em"}
:::
::::

::: {.center-h .sm}
All of these actions generate **digital traces** that can be analyzed in social science research
:::""")

sl("Research example: Earthquakes on Twitter", """::: {.center-h}
![](figures/p15-1.jpg){height="8.4em"}
:::

::: {.source}
XKCD 723, *Seismic Waves*: <https://xkcd.com/723/>
:::""")

sl("Research example: Earthquakes on Twitter", """::: {.center-h}
![](figures/p16-1.png){height="10.4em"}
:::

::: {.source}
Earle PS, Bowden DC, Guy M. Twitter earthquake detection: earthquake monitoring in a social world. *Annals of Geophysics* (2012)
:::""")

sl("Research example: Trading and Google trends", """::: {.center-h}
![](figures/p17-1.jpg){height="10.0em"}
:::

::: {.source}
Quantifying Trading Behavior in Financial Markets Using Google Trends. Tobias Preis, Helen Susannah Moat, H Eugene Stanley. *Scientific Reports* (2013)
:::""")

sl("Research example: Gender Inequality with Facebook", """::: {.center-h}
![](figures/p18-1.jpg){height="9.6em"}
:::

::: {.source}
Garcia, D., Mitike Kassa, Y., Cuevas, A., Cebrian, M., Moro, E., Rahwan, I., & Cuevas, R. Analyzing gender inequality through large-scale Facebook advertising data. *PNAS* (2018)
:::""")

sl("Issues with Digital Behavioral Data: Representation", """:::: {.columns}
::: {.column width="26%"}
![](figures/p19-1.png){height="8.4em"}
:::

::: {.column width="74%"}
![](figures/p19-2.png){height="9.0em"}
:::
::::

::: {.source}
Meaningful measures of human society in the twenty-first century. David Lazer et al., *Nature* (2021)<br>
<https://www.pewresearch.org/internet/2021/04/07/social-media-use-in-2021/>
:::""")

sl("New Methods in the Social Sciences", outline(3))

sl("The Challenge of New Unstructured Data", """::: {.center-h}
![](figures/p21-1.jpg){height="10.4em"}
:::

::: {.source}
<https://twitter.com/mszll/status/1332245497617190913>
:::""")

sl("Heterogenous Data Sources and Methods", """::: {.xs}
- Social science data used to have few formats: e.g. experiment outcome annotations or survey responses
- Now many more formats and data sources:
  - text, social networks, locations and timestamps, likes…
- Sometimes these formats are even related to each other
- Methods have been improving over time:
  - **First generation of methods:** adapting previous social science methods
    - example: dictionaries in text analysis
  - **Second generation of methods:** using Machine Learning models to generalize measurement from many examples of measurements
    - example: sentiment analysis
  - **Third generation of methods:** using large models to analyze highly-dimensional data
    - example: word embeddings &ndash; see the "document analysis" course
:::""")

sl("Research Example: VADER sentiment analysis", """:::: {.columns}
::: {.column width="34%"}
![](figures/p23-2.png){height="9.4em"}
:::

::: {.column width="66%"}
![](figures/p23-1.jpg){height="9.4em"}
:::
::::

::: {.source}
VADER: A Parsimonious Rule-Based Model for Sentiment Analysis of Social Media Text. C. Hutto, E. Gilbert. *ICWSM* (2014)
:::""")

sl("Research Example: Social Media and Emotion Surveys", """::: {.center-h}
![](figures/p24-1.jpg){height="10.6em"}
:::

::: {.source}
Social media emotion macroscopes reflect emotional experiences in society at large. D Garcia et al.
:::""")

sl("Research Example: Personality and Facebook Likes", """::: {.center-h}
![](figures/p25-1.jpg){height="10.6em"}
:::

::: {.source}
Computer-based personality judgments are more accurate than those made by humans. Youyou et al. *PNAS* (2015)
:::""")

sl("Issues with Methods: New Privacy Risks", """:::: {.columns}
::: {.column width="34%"}
![](figures/p26-1.png){height="9.6em"}
:::

::: {.column width="66%"}
![](figures/p26-2.png){height="6.4em"}
:::
::::

::: {.source}
Private traits and attributes are predictable from digital records of human behavior. Kosinski et al. (2013)<br>
Collective aspects of privacy in the Twitter social network. Garcia et al. (2018)
:::""")

sl("Computational Analysis of Social Science Theory", outline(4))

sl("The End of Theory?", """::: {.center-h}
![](figures/p28-1.jpg){height="5.6em"}

![](figures/p28-2.jpg){height="5.4em"}
:::""")

sl("The End of Theory?", """::: {.center-h}
![](figures/p29-3.jpg){height="9.0em"}
:::""")

sl("Agent-Based Modelling: Computing and Social Theory", """::: {.center-h}
![](figures/p30-1.jpg){height="4.2em"}
:::

::: {.sm}
- Model humans as **agents** that symbolize a simplified behavior
- Agents have quantifiable variables and properties
  - all interaction rules are explicitly defined and parametrized
- Simulations and mathematical analysis can be applied to derive system properties that might not be easy to conclude from intuition alone
- Generates hypotheses and proofs of **generative sufficiency**, but not empirical evidence
:::""")

sl("Modelling Segregation: Schelling's Model", """:::: {.columns}
::: {.column width="58%"}
::: {.xs}
**Model properties:**

- Agents of two kinds, similar number
- Low but nonzero fraction of empty cells
- Cells have a neighborhood of 8 cells around the central cell
- Corners and borders have fewer neighbors
- Agents are aware of the fraction of similar agents in their neighborhood: $f$
- Agents are satisfied with $f \\geq F$
- If unsatisfied, they jump to the closest satisfying cell
- $F$ is a parameter that measures **intolerance**
- Example: simulation with $F = 0.2$
:::
:::

::: {.column width="42%"}
![](figures/p31-1.jpg){height="9.4em"}
:::
::::""")

sl("More on Schelling's model", """::: {.center-h}
![](figures/p32-1.jpg){height="10.4em"}
:::

::: {.source}
<https://dgarcia-eu.github.io/CMSS-Konstanz/02_Segregation/Slides/Slides.html#14> &nbsp;&mdash;&nbsp; slides 14&ndash;38
:::""")

sl("Segregation Under Tolerance in Schelling's Model", """:::: {.columns}
::: {.column width="50%"}
![](figures/p33-1.jpg){height="8.6em"}

::: {.center-h .xs}
Example with $F = 0.6$. Strong segregation
:::
:::

::: {.column width="50%"}
![](figures/p33-2.jpg){height="8.6em"}

::: {.center-h .xs}
Example with $F = 0.4$. Also segregated!
:::
:::
::::

::: {.source}
Dynamic Models of Segregation. Thomas Schelling. *Journal of Mathematical Sociology* (1971)
:::""")

sl("Simulating Effects of Anti-COVID Policies", """:::: {.columns}
::: {.column width="50%"}
![](figures/p34-1.jpg){height="8.6em"}
:::

::: {.column width="50%"}
![](figures/p34-2.png){height="7.6em"}
:::
::::

::: {.source}
Assessment of the Effectiveness of Omicron Transmission Mitigation Strategies for European Universities Using an Agent-Based Network Model. J. Lasser, T. Hell, D. Garcia. *Clinical Infectious Diseases* (2022)
:::""")

sl("Courses Outlook", outline(5))

sl("Deep Learning for the Social Sciences", """:::: {.columns}
::: {.column width="56%"}
::: {.sm}
- 9 ECTS (2+2 SWS)
- Taught next SS by Giordano De Marzo
- Machine Learning concepts
- Multilayer perceptrons and their limitations
- Convolutional Neural Networks
- RNN, LSTM, RL
- Applications to time series, graphs, generative modelling and NLP
- Exercises in PyTorch
:::
:::

::: {.column width="44%"}
![](figures/p36-1.jpg){height="9.0em"}
:::
::::""")

sl("2027: Social Media Data Analysis", """:::: {.columns}
::: {.column width="60%"}
::: {.xs}
- 9 ECTS (2+2 SWS)
- To be taught in 2027 by David Garcia
- Course contents:
  - Analysis of search data to measure information seeking
  - Popularity and social impact in social media
  - Application and evaluation of sentiment analysis techniques for social media text
  - Methods and applications of social network analysis in online media
- Practical assignments where you get and analyze your own data
- <https://github.com/dgarcia-eu/SocialMediaDataAnalysis>
:::
:::

::: {.column width="40%"}
![](figures/p37-1.jpg){height="8.0em"}
:::
::::""")

sl("2027: Computational Modelling of Social Systems", """:::: {.columns}
::: {.column width="60%"}
::: {.sm}
- Seminar with exercises: 6 ECTS (2 + 2 SWS)
- To be taught in 2027 by David Garcia
- <https://github.com/dgarcia-eu/CMSS-Konstanz>
- Lectures and exercises on Agent-Based Modelling and Complexity Science
- Topics:
  - Modelling segregation: Schelling's model
  - Modelling cultures: Axelrod's model
  - Spreading of behavior
  - Opinion dynamics
  - Network growth models
  - Social resilience
- Python exercises with Mesa
:::
:::

::: {.column width="40%"}
![](figures/p38-1.png){height="4.6em"}
:::
::::""")

sl("Path to Master Thesis", """:::: {.columns}
::: {.column width="58%"}
::: {.sm}
- **Recommendation:** take *Colloquium in Social Data Science* the semester before your master thesis
- Preparation by joining group research updates (Tuesdays 13:30-15:00)
- Students prepare their thesis plan during the semester and present it for input at the end
- Manual registration by me &ndash; contact me before to discuss coursework and potential topics
- **Second recommendation:** take my group's courses and read our papers
:::
:::

::: {.column width="42%"}
![](figures/p39-1.png){height="4.4em"}
:::
::::""")

sl("Summary", """::: {.sm}
- **Computational Social Science**
  - Using new sources of data and computational methods in the social sciences: the three meanings of the word *computational*
- **Digital Behavioral Data in the Social Sciences**
  - Social media, search, mobile phones… Risks: representation problems
- **New Methods in the Social Sciences**
  - Text analysis as an example. Risks: privacy
- **Computational Analysis of Social Science Theory**
  - Agent-Based Modelling to analyze models of social systems
- **Next Sessions:** Exam review and Q&A
:::""")

sl("Next sessions: Q&A and exam review", """:::: {.columns}
::: {.column width="60%"}
::: {.sm}
- An exam example can be found in the theory exercises folder on Ilias
- In the upcoming sessions we can discuss any previous exercise, the exam example, or go back to any slides from the lectures
- Extra time will be used for Q&A about practical projects
- 24 hours before each session I will collect questions and requests from the form:
:::

::: {.center-h .sm}
<https://forms.gle/MXTtQw6FUNpw2qrW9>
:::
:::

::: {.column width="40%"}
![](figures/p41-1.png){height="8.0em"}
:::
::::""")

open(OUT, "w").write("".join(s))
print("slides:", "".join(s).count("\n## "))
