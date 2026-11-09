# Motivating examples: selector

Each deck from session 2 to session 12 currently carries **three** candidate
opening examples, inserted right after the Overview slide, and each is developed
at length in the matching transcript under *Why this matters*.

## How to choose

Put an `x` in the brackets of the ones you want to **keep**. Leave the rest
empty. You can keep more than one per session, or none.

```
- [x] M05-A ...     keep this one
- [ ] M05-B ...     delete this one
```

Then run:

```bash
python3 tools/pickmotivation.py          # show what would change
python3 tools/pickmotivation.py --apply  # delete the unselected ones and rebuild
```

The script deletes the unchosen candidates from **both** the deck and the
transcript, re-renders every affected deck, and reports the new page counts. It
only ever removes text between the `<!-- MOTIVATION:... -->` markers, so nothing
else can be touched.

If you change your mind afterwards, `python3 tools/genmotivation.py` puts all
three back and you can start again.

## A note on page counts

Until you choose, each deck from 2 to 12 has **3 more slides** than its 2025
original, so the page-parity check in `PROGRESS.md` is off by three for those
decks. After selection it will be off by however many you kept, usually one.

---


## Session 2: Information Coding

<small>Deck: `Slides/02-InformationCoding/ICSS-2026-02-InformationCoding.qmd` · Transcript: `Transcripts/02-InformationCoding.md`</small>

- [ ] **M02-A**: *Excel renamed one gene in five*  
  <small>Spreadsheet autoformatting silently corrupted gene names in 20% of published genetics papers. What is the software actually storing?</small>
- [ ] **M02-B**: *Müller became MÃ¼ller*  
  <small>A survey exported from one system and read in another silently splits categories. What is a text file, if the same bytes mean two things?</small>
- [ ] **M02-C**: *The index that lost half its value*  
  <small>The Vancouver Stock Exchange index drifted from 1000 to 525 in 22 months through truncation alone. Why can't a computer store 0.1?</small>


## Session 3: Data Structures

<small>Deck: `Slides/03-DataStructures/ICSS-2026-03-DataStructures.qmd` · Transcript: `Transcripts/03-DataStructures.md`</small>

- [ ] **M03-A**: *Two million respondents, and one duplicate*  
  <small>Finding duplicates in a panel: 2 × 10¹² comparisons the obvious way, two seconds with the right structure.</small>
- [ ] **M03-C**: *Six thousand rows, and the answer in thirteen steps*  
  <small>Codebook lookups: 6,000 comparisons scanning, 13 with binary search, and what you have to give up to get it.</small>


## Session 4: Software

<small>Deck: `Slides/04-Software/ICSS-2026-04-Software.qmd` · Transcript: `Transcripts/04-Software.md`</small>

- [ ] **M04-A**: *The app that leaked 13,000 photo IDs*  
  <small>Tea stored 13,000 selfies and photo IDs where anyone could download them: an obvious requirement that nobody wrote down or tested.</small>
- [ ] **M04-D**: *The 5 millimeters nobody could move*  
  <small>Nokia's Symbian grew to 20 million lines in one phone, and nobody could find the code to move a screen element by 5 mm.</small>


## Session 5: Algorithms

<small>Deck: `Slides/05-Algorithms/ICSS-2026-05-Algorithms.qmd` · Transcript: `Transcripts/05-Algorithms.md`</small>

- [ ] **M05-A**: *Six handshakes, and how you would check*  
  <small>Milgram needed volunteers and postage; Facebook measured the same thing over 1.59 billion people. What is the procedure?</small>
- [ ] **M05-B**: *Whose contacts, within two steps?*  
  <small>Contact tracing as a graph search: thousands of people, answered in seconds, and every step of the recipe has to be pinned down.</small>
- [ ] **M05-C**: *The network that would not fit*  
  <small>84 million people: 7 × 10¹⁵ cells one way, a laptop's worth the other. Representation decides whether the study is possible.</small>


## Session 6: Recursion

<small>Deck: `Slides/06-Recursion/ICSS-2026-06-Recursion.qmd` · Transcript: `Transcripts/06-Recursion.md`</small>

- [ ] **M06-A**: *How many people report to her?*  
  <small>An org chart of unknown depth: a loop needs to know how many levels there are, and you don't.</small>
- [ ] **M06-B**: *The comment thread with no bottom*  
  <small>Replies to replies to replies: when the data is defined in terms of itself, what should the procedure look like?</small>
- [ ] **M06-C**: *The algorithm that is 2 300 years old*  
  <small>Euclid's gcd, c. 300 BC, still the one your computer uses, and the cleanest illustration of what makes a recursion stop.</small>


## Session 7: Sorting Algorithms

<small>Deck: `Slides/07-SortingAlgorithms/ICSS-2026-07-SortingAlgorithms.qmd` · Transcript: `Transcripts/07-SortingAlgorithms.md`</small>

- [ ] **M07-A**: *Sorted by region, then by age, and the regions came apart*  
  <small>Two sorting algorithms give the same sorted order and different results. The property that separates them is stability.</small>
- [ ] **M07-B**: *Two seconds, or fourteen hours*  
  <small>A million records: 5 × 10¹¹ comparisons one way, 2 × 10⁷ the other. Both algorithms are correct.</small>
- [ ] **M07-C**: *Why sort at all?*  
  <small>Sorting is an investment: worthless for one lookup, essential for forty million. How do you work out whether it pays?</small>


## Session 8: Time Complexity

<small>Deck: `Slides/08-TimeComplexity/ICSS-2026-08-TimeComplexity.qmd` · Transcript: `Transcripts/08-TimeComplexity.md`</small>

- [ ] **M08-A**: *It ran fine on the pilot*  
  <small>Four seconds on 1 000 rows. On a million: one hour, or forty-six days, and nothing about the code changed.</small>
- [ ] **M08-B**: *Two students, the same answer, 20 000× apart*  
  <small>Both correct, both hand in the same numbers. One finishes in 90 minutes, the other in under a second.</small>
- [ ] **M08-C**: *Ten billion pages in a third of a second*  
  <small>No machine can look at 10¹⁰ pages in 0.3 s. What class of procedure makes it possible, and what did it cost up front?</small>


## Session 9: Theoretical Computer Science

<small>Deck: `Slides/09-TheoreticalCS/ICSS-2026-09-TheoreticalCS.qmd` · Transcript: `Transcripts/09-TheoreticalCS.md`</small>

- [ ] **M09-A**: *The regular expression that took down a large part of the web*  
  <small>One line of pattern, 27 minutes of global outage. A pattern matcher is a machine with a precise definition, and precise limits.</small>
- [ ] **M09-B**: *300 students, 40 seminars, and no schedule*  
  <small>The assignment problem the department does by hand. There is a mathematical reason why no clever program makes it easy.</small>
- [ ] **M09-C**: *Can a program check your program?*  
  <small>A marking system that rejects submissions which loop forever. Turing proved in 1936 that no such program can exist.</small>


## Session 10: Machine Learning

<small>Deck: `Slides/10-MachineLearning/ICSS-2026-10-MachineLearning.qmd` · Transcript: `Transcripts/10-MachineLearning.md`</small>

- [ ] **M10-A**: *Google predicted the flu, until it didn't*  
  <small>Google Flu Trends beat the CDC in 2009 and predicted more than double the real rate in 2013. It fitted the past almost perfectly.</small>
- [ ] **M10-B**: *93% accurate, and it never finds anyone*  
  <small>A dropout-risk model with 93% accuracy that identifies nobody. Which number should have been on the report?</small>
- [ ] **M10-C**: *A million speeches nobody can read*  
  <small>Every Bundestag speech since 1949: forty person-years to hand-code. You can code 2 000. Now what?</small>


## Session 11: Databases

<small>Deck: `Slides/11-Databases/ICSS-2026-11-Databases.qmd` · Transcript: `Transcripts/11-Databases.md`</small>

- [ ] **M11-A**: *The 15 841 cases that fell off the end of a spreadsheet*  
  <small>Public Health England lost 16 000 COVID results to a 65 536-row limit. No error appeared. 50 000 contacts were never traced.</small>
- [ ] **M11-B**: *Two seats, one airplane*  
  <small>Two agents book the last seat in the same second. Each program checked availability and found one. Neither has a bug.</small>
- [ ] **M11-C**: *Whose number is right?*  
  <small>Three copies of the participant list, three people doing their jobs, and three different answers to 'how many participants'.</small>


## Session 12: Parallel Programming

<small>Deck: `Slides/12-ParallelProgramming/ICSS-2026-12-ParallelProgramming.qmd` · Transcript: `Transcripts/12-ParallelProgramming.md`</small>

- [ ] **M12-A**: *Your laptop stopped getting faster in 2005*  
  <small>Clock speeds flat at about 3 GHz for twenty years while transistor counts kept doubling. The extra transistors became cores, not speed.</small>
- [ ] **M12-B**: *Sixteen cores, and 2.5× faster*  
  <small>40 hours becomes 16 on 16 cores, and 15 on 64. Where did the other thirteen cores go? There is an exact formula, from 1967.</small>
- [ ] **M12-C**: *Three billion posts, one million rows of memory*  
  <small>Correlating likes and reshares across data that does not fit. Averaging the chunk correlations gives a number, and it is the wrong number.</small>


---

## If none of the three works

Say what the session should open with and I will write it. The ones that tend to
work best are: a **specific number** that is surprising, a **decision someone
actually had to make**, or a **failure with a named cause**, rather than a
general statement that the topic is important.
