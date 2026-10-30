#!/usr/bin/env python3
"""Insert figures into the self-study posts (examples and history).

Each entry is (marker, figure): the figure is inserted just before the first
line containing `marker` -- or just after it when the marker is a heading -- so
that a floated figure sits beside the paragraph it illustrates.  Inserted
blocks are wrapped in <!-- FIG --> ... <!-- /FIG --> and are stripped before
re-insertion, so the script is idempotent.

    python3 tools/figposts.py          # insert, report missing markers
    python3 tools/figposts.py --strip  # remove all inserted figures
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "Examples", "posts")
CREDITS = json.load(open(os.path.join(POSTS, "img", "credits.json")))
EXDIR = os.path.join(ROOT, "Slides", "Examples")


def deckfig(name):
    """Path, relative to a post, of a figure in the figures/ folder of the example deck that uses it."""
    import glob
    hits = glob.glob(os.path.join(EXDIR, "*-Examples", "figures", name))
    assert hits, f"figure not found in any Slides/Examples/NN-Examples/figures/: {name}"
    return os.path.relpath(hits[0], POSTS)


def _clean_artist(a):
    a = (a or "").replace("Unknown authorUnknown author", "unknown author").strip()
    a = re.sub(r"\s+", " ", a)
    return a[:48].rstrip(" ,;") if a else "unknown author"


def P(key, caption, wide=False):
    """Portrait or context photo from img/, with licence credit."""
    c = CREDITS[key]
    credit = f'Photo: {_clean_artist(c["artist"])}, {c["license"]}, via <a href="{c["page"]}">Wikimedia Commons</a>.'
    cls = "side wide" if wide else "side"
    return (f'<figure class="{cls}"><img src="img/{c["file"]}" alt="{c["title"]}">'
            f'<figcaption><b>{caption}</b> {credit}</figcaption></figure>')


def F(name, caption, full=True):
    """A figure from the example decks."""
    cls = "full" if full else "side wide"
    return (f'<figure class="{cls}"><img src="{deckfig(name)}" alt="{caption}">'
            f'<figcaption>{caption}</figcaption></figure>')


def D(name, caption, credit, full=False):
    """An outside image used in an example deck (already credited there)."""
    cls = "full" if full else "side wide"
    return (f'<figure class="{cls}"><img src="{deckfig(name)}" alt="{caption}">'
            f'<figcaption>{caption} {credit}</figcaption></figure>')


FIGS = {
# ======================================================================= examples
"X02-A": [
    ("## The puzzle", F("02-y2038-q.svg", "The counter one second before it overflows: a 0 followed by 31 ones.")),
    ("The second fact is that two's complement", F("02-y2038.svg", "Adding one carries into the sign bit; the same 32 bits now mean 13 December 1901.")),
    ("## Why this matters", P("y2038", "How the 32-bit Unix time counter wraps in 2038", wide=True)),
],
"X02-B": [
    ("## What is going on", F("02-float-sum.svg", "The four numbers as IEEE 754 doubles: none is the decimal you typed, and the sum differs from 0.3 in the last bit.")),
    ("## Why this matters", P("excel", "Spreadsheets store numbers as the same IEEE 754 doubles and hide the last digits when displaying them.")),
],
"X02-C": [
    ("## The puzzle", P("passport", "A German passport: the two lines at the bottom are the machine-readable zone.", wide=True)),
    ("## What is going on", F("02-mrz.svg", "The MRZ transliterates the name into a 37-symbol alphabet; every reader in the world decodes it identically.")),
],
"X03-A": [
    ("## What is going on", F("03-browser-stacks.svg", "Three states of the two-stack history: after C, after two Backs, and after opening D, which clears the forward stack.")),
],
"X03-B": [
    ("## The puzzle", F("03-wordcount.svg", "The two containers: a list of pairs that must be searched, and a hash table that is addressed directly.")),
    ("## What is going on", F("03-wordcount-timing.png", "Measured time for both versions; on log axes the list has slope 2 and the dictionary slope 1.")),
],
"X03-C": [
    ("## The puzzle", F("03-queue-shift-q.svg", "Removing the front of an array shifts everyone behind it.")),
    ("## What is going on", F("03-queue-shift.svg", "A queue moves one pointer instead; the cost no longer depends on the length.")),
],
"X04-A": [
    ("## The puzzle", F("04-string-sum-q.svg", "The loop as written, and the output it produced.")),
    ("## What is going on", F("04-string-sum.svg", "Same operator, same code: on strings + concatenates, on integers it adds.")),
],
"X04-B": [
    ("## The puzzle", P("ariane", "An Ariane 5 on the pad at Kourou. Flight 501 in 1996 was the type's maiden flight.", wide=True)),
    ("## What is going on", F("04-ariane-overflow.svg", "A 64-bit float squeezed into a 16-bit integer: the Ariane 5 value did not fit.")),
],
"X04-C": [
    ("## What is going on", F("04-leap-year.svg", "The rule as a flowchart: three nested conditions, and where 1900, 2000 and 2024 come out.")),
    ("## Why this matters", P("excel", "Excel keeps 1900 as a leap year for compatibility with Lotus 1-2-3 files.")),
],
"X05-A": [
    ("## The puzzle", F("05-erdos-q.svg", "A small co-authorship graph. What is the distance from Erdős to You?")),
    ("## What is going on", F("05-erdos-bfs.svg", "Breadth-first search assigns distances layer by layer; the first discovery is the shortest.")),
    ("## Why this matters", P("erdos", "Paul Erdős (1913–1996), with more co-authors than any mathematician in history.")),
],
"X05-B": [
    ("## The puzzle", D("konigsberg-bridges.png", "Königsberg's seven bridges, on a map of the time.", "Map: Bogdan Giuşcă, CC BY-SA 3.0, via Wikimedia Commons.")),
    ("## What is going on", F("05-konigsberg-graph.svg", "The city as a graph: four vertices, seven edges, and every degree odd.")),
    ("## Why this matters", P("euler", "Leonhard Euler (1707–1783), whose 1736 paper on the bridges founded graph theory.")),
],
"X05-C": [
    ("## The puzzle", F("05-maze.svg", "The maze. Green in, red out.")),
    ("## What is going on", F("05-maze-solved.svg", "BFS distances from the entrance, shaded, and the shortest path found by following parent pointers back from the exit.")),
],
"X06-A": [
    ("## The puzzle", D("tower-of-hanoi.jpg", "The puzzle as sold: three pegs, a stack of disks.", "Photo: CC BY-SA 3.0, via Wikimedia Commons.")),
    ("## What is going on", F("06-hanoi.svg", "The recursive plan: move n−1 aside, move the largest, move n−1 back.")),
    ("## Why this matters", P("lucas", "Édouard Lucas (1842–1891), who invented the puzzle and its legend in 1883.")),
],
"X06-B": [
    ("## The puzzle", F("06-fractal-tree.svg", "The same five-line procedure at depths 1, 2, 4 and 10.")),
],
"X06-C": [
    ("## The puzzle", F("06-ancestors.svg", "Ancestor slots double every generation; the population does not.")),
],
"X07-A": [
    ("## The puzzle", P("post-sorting", "A postal sorting center: letters routed by postcode, no two ever compared.", wide=True)),
    ("## What is going on", F("07-radix-postcodes.svg", "The first pass of radix sort: bin by the last digit, collect the bins in order, repeat.")),
    ("## Why this matters", P("card-sorter", "A punched-card sorter, the same algorithm in hardware from the 1890s to the 1960s.")),
],
"X07-B": [
    ("## What is going on", F("07-decision-tree.svg", "The full decision tree for sorting three elements: six leaves, so depth at least three.")),
    ("## Why this matters", P("knuth", "Donald Knuth, whose Art of Computer Programming vol. 3 settles the small cases exactly.")),
],
"X07-C": [
    ("## What is going on", F("07-quickselect.svg", "Quickselect on nine numbers: each partition narrows the active region until the pivot lands on the median.")),
    ("## Why this matters", P("hoare", "Tony Hoare, who published Find (quickselect) in 1961 alongside quicksort.")),
],
"X08-A": [
    ("## The puzzle", D("xkcd-936-password-strength.png", "XKCD 936, the comic that started the argument.", "Randall Munroe, CC BY-NC 2.5, xkcd.com/936.", full=True)),
    ("## What is going on", F("08-password-bruteforce.png", "Time to try every possibility at ten billion guesses per second, on a log axis.")),
],
"X08-B": [
    ("## What is going on", F("08-quadratic-memory.png", "Memory of an n × n distance matrix against the data itself, with a laptop and a cluster node marked.")),
],
"X08-C": [
    ("## What is going on", F("08-algorithms-vs-hardware.png", "Where the 1988–2003 speed-up came from, according to the PCAST report.")),
    ("## Why this matters", P("gordon-moore", "Gordon Moore (1929–2023). His law gave the constant factor; algorithms gave the rest.")),
],
"X09-A": [
    ("## What is going on", F("09-vending-dfa.svg", "The six-state automaton: coins move between amounts, and any coin past 50 goes to reject.")),
    ("## Why this matters", P("rabin", "Michael Rabin, who with Dana Scott gave finite automata their modern definition in 1959.")),
],
"X09-B": [
    ("## What is going on", F("09-brackets-pda.svg", "A stack reading (()(())): depth rises and falls, and ends at zero.")),
    ("## Why this matters", P("chomsky", "Noam Chomsky, whose hierarchy of grammars places brackets one level above what finite automata can do.")),
],
"X09-C": [
    ("## The puzzle", D("sudoku-example.svg", "A newspaper Sudoku.", "Public domain, via Wikimedia Commons.")),
    ("## Why this matters", P("cook", "Stephen Cook, who proved the first problem NP-complete in 1971.")),
],
"X10-A": [
    ("## The puzzle", F("10-husky-wolf-q.svg", "The four cases: two the model saw in training, two it met later.")),
    ("## What is going on", F("10-husky-wolf.svg", "What the explanation highlights: the background.")),
    ("## Why this matters", P("husky", "A Siberian husky on snow, which is the problem.")),
],
"X10-B": [
    ("## The puzzle", P("titanic", "RMS Titanic leaving Southampton, 10 April 1912.", wide=True)),
    ("## What is going on", F("10-titanic-confusion.svg", "The confusion matrix of the five-word rule on 891 passengers.")),
    ("## Why this matters", F("10-titanic-rates.png", "Survival by sex and by ticket class in the training set.")),
],
"X10-C": [
    ("## The puzzle", F("10-kmeans-data.png", "240 respondents, two scores, no labels.", full=False)),
    ("## What is going on", F("10-kmeans-k3.png", "K-means with K = 3; the crosses are the centers.", full=False)),
    ("The next question is how to choose $K$", F("10-kmeans-elbow.png", "Within-cluster sum of squares against K: the elbow at 3.", full=False)),
    ("The rings are the warning", F("10-kmeans-rings.png", "Two rings, K = 2: the algorithm splits them down the middle.", full=False)),
],
"X11-A": [
    ("## The puzzle", D("xkcd-327-exploits-of-a-mom.png", "XKCD 327, Exploits of a Mom.", "Randall Munroe, CC BY-NC 2.5, xkcd.com/327.", full=True)),
    ("## Why this matters", P("bobby", "SQL injection is still in the OWASP top three, twenty years after the comic.")),
],
"X11-B": [
    ("## What is going on", F("11-join-explosion.svg", "Eight purchases × two products = sixteen rows: the Cartesian product.")),
    ("## Why this matters", P("selinger", "Patricia Selinger, whose 1979 optimizer is why a correct join is also a fast one.")),
],
"X11-C": [
    ("## What is going on", F("11-left-join-null.svg", "What INNER JOIN and LEFT JOIN each produce; the NULL rows are the customers you were looking for.")),
    ("## Why this matters", P("chamberlin", "Donald Chamberlin, co-designer of SQL in 1974.")),
],
"X12-A": [
    ("## What is going on", F("12-race-condition.svg", "Two threads interleaving read, add and write: one increment is lost.")),
    ("## Why this matters", P("dean", "Jeff Dean, co-author of MapReduce, a framework designed so that this figure cannot happen.")),
],
"X12-B": [
    ("## What is going on", F("12-simd-vs-cpu.svg", "One flexible core against thousands of lanes that must all do the same thing.")),
    ("## Why this matters", P("gpu", "A graphics processing unit: thousands of simple lanes on one card.", wide=True)),
],
"X12-C": [
    ("## What is going on", F("12-mapreduce.svg", "Map on chunks, shuffle by word, reduce by adding; only the small pairs travel.")),
    ("## Why this matters", P("wikipedia", "Wikipedia's article text is about 20 GB, the input of the example.")),
],
"X13-A": [
    ("## The puzzle", P("literary-digest", "The Literary Digest in its heyday.", wide=True)),
    ("## What is going on", F("13-literary-digest.png", "The Digest's 2.4 million ballots, Gallup's 50 000 interviews, and the result.")),
    ("## The answer", P("gallup", "George Gallup (1901–1984), whose small designed sample was right.")),
],
"X13-B": [
    ("## The puzzle", F("13-schelling-before.svg", "Random start: about half of every agent's neighbors are like it.", full=False)),
    ("## What is going on", F("13-schelling-after.svg", "Everyone satisfied at F = 0.3: three quarters of neighbors are now like them.", full=False)),
    ("## Why this matters", P("schelling", "Thomas Schelling (1921–2016), who ran the first version with coins on a chessboard.")),
],
"X13-C": [
    ("## What is going on", F("13-likes-accuracy.png", "Accuracy against the number of Likes available, with the human judges' thresholds from the paper.")),
    ("## Why this matters", P("gebru", "Timnit Gebru: the questions this raises about inference and consent are the ones session 10's ethics list asks.")),
],
# ======================================================================= history
"H01": [
    ("## Computing as a job", P("harvard-computers", "The Harvard Observatory computers at work, around 1890.", wide=True)),
    ("Katherine Johnson, the best known", P("katherine-johnson", "Katherine Johnson (1918–2020) at NASA Langley in 1966.")),
    ("## Mechanizing the work", P("difference-engine", "Babbage's Difference Engine No. 2, built to his drawings in 1991.", wide=True)),
    ("What survives of the Analytical Engine", P("lovelace", "Ada Lovelace (1815–1852), in a portrait of 1840.")),
    ("The mechanization that actually happened", P("punched-card", "An 80-column punched card: one record, one attribute per column.", wide=True)),
    ("## Machines that hold their own instructions", P("eniac", "ENIAC being programmed, by rewiring, in 1946.", wide=True)),
],
"H02": [
    ("## Measuring information", P("shannon", "Claude Shannon (1916–2001).")),
    ("## The number that behaves the same everywhere", P("kahan", "William Kahan, the author of IEEE 754.")),
    ("## Grace Hopper and the decimal point", P("hopper", "Grace Hopper (1906–1992), photographed in 1984.")),
],
"H03": [
    ("## Structures the hardware gave us", P("punched-card", "An 80-column punched card, the fixed-width record that preceded the array.", wide=True)),
    ("## Structures a problem demanded", P("simon", "Herbert Simon (1916–2001), for whom the linked list was a means to prove theorems.")),
    ("## Structures as promises", P("liskov", "Barbara Liskov, who defined the abstract data type; Turing Award 2008.")),
    ("## The encyclopedia", P("knuth", "Donald Knuth, author of The Art of Computer Programming since 1962.")),
],
"H04": [
    ("## Before there was anything to run it on", P("lovelace", "Ada Lovelace (1815–1852), in a portrait of 1840.")),
    ("## Machines that could be told things", P("z3", "A reconstruction of Zuse's Z3 of 1941 in the Deutsches Museum.", wide=True)),
    ("The reinvention was largely one woman", P("hopper", "Grace Hopper, who named the compiler.")),
],
"H05": [
    ("## Al-Khwarizmi and the general method", P("khwarizmi", "A statue of al-Khwarizmi in Khiva, Uzbekistan.")),
    ("## Graphs, and the search", P("euler", "Leonhard Euler (1707–1783).")),
    ("Breadth-first search, the algorithm", P("konigsberg", "Königsberg in 1652, with its seven bridges.", wide=True)),
],
"H06": [
    ("## Foundations", P("dedekind", "Richard Dedekind (1831–1916), who defined arithmetic by recursion.")),
    ("For the next forty years recursion was a tool", P("godel", "Kurt Gödel (1906–1978).")),
    ("## Rózsa Péter", P("peter", "Rózsa Péter (1905–1977), founder of recursive function theory.")),
    ("Two further ideas in the session", P("hanoi", "A Tower of Hanoi puzzle, sold with its legend since 1883.")),
],
"H07": [
    ("## Machines before programs", P("card-sorter", "A punched-card sorter: one column per pass, least significant first.", wide=True)),
    ("## The first programs", P("von-neumann", "John von Neumann (1903–1957).")),
    ("Six years later the first program that", P("holberton", "Betty Holberton (1917–2001), ENIAC programmer and author of the first sort generator.")),
    ("## Quicksort, and the limit", P("hoare", "Tony Hoare, in 2011.")),
],
"H08": [
    ("## A notation from number theory", F("08-algorithms-vs-hardware.png", "Algorithms against hardware, 1988–2003: the growth rate, not the clock speed, is what the notation measures.")),
    ("Between 1971 and 1973 the class NP", P("cook", "Stephen Cook, Turing Award 1982.")),
    ("## Widening the question", P("goldwasser", "Shafi Goldwasser, Turing Award 2012.")),
    ("## Two undergraduates", P("agrawal", "Manindra Agrawal of IIT Kanpur, first author of 'PRIMES is in P'.")),
],
"H09": [
    ("## Hilbert's question", P("hilbert", "David Hilbert (1862–1943).")),
    ("## 1936", P("turing", "Alan Turing (1912–1954).")),
    ("The smaller machines of the lecture", P("bletchley", "Bletchley Park, where Turing worked from 1939.", wide=True)),
    ("## The tenth problem", P("robinson", "Julia Robinson (1919–1985).")),
],
"H10": [
    ("What one layer could not do, several could", P("hinton", "Geoffrey Hinton, Turing Award 2018, Nobel Prize 2024.")),
    ("## The dataset", P("fei-fei-li", "Fei-Fei Li, who built ImageNet.")),
    ("## Who the models fail", P("buolamwini", "Joy Buolamwini, first author of Gender Shades.")),
],
"H11": [
    ("## Files, then models", P("punched-card", "Before databases: one record per card, filed in drawers.", wide=True)),
    ("## Codd's tables", F("11-left-join-null.svg", "Codd's proposal in one picture: tables related by matching values, not by pointers.", full=False)),
    ("## Making \"what\" fast", P("selinger", "Patricia Selinger, whose 1979 paper made declarative queries fast.")),
],
"H12": [
    ("## The law, and the argument it came from", P("amdahl", "Gene Amdahl (1922–2015).")),
    ("The rebuttal came in 1988", P("illiac", "ILLIAC IV, the sixty-four-processor machine Amdahl argued against.", wide=True)),
    ("## The kinds of machine", P("cray-1", "A Cray-1 in the Deutsches Museum; the bench around the base hides the power supplies.", wide=True)),
    ("## Making programs parallel", P("fran-allen", "Frances Allen (1932–2020), first woman to receive the Turing Award.")),
    ("The other route was to change", P("connection-machine", "A Connection Machine CM-2: many small processors, each with its own instruction stream.", wide=True)),
],
"H13": [
    ("## Simon and the artificial", P("simon", "Herbert Simon (1916–2001): political scientist, AI founder, Nobel and Turing laureate.")),
    ("## Schelling and the model", P("schelling", "Thomas Schelling (1921–2016).")),
    ("The digital half of the field", F("13-schelling-after.svg", "The lecture's Schelling grid after settling: macro segregation from mild micro preference.", full=False)),
    ("## The critics who arrived early", P("noble", "Safiya Umoja Noble, author of Algorithms of Oppression.")),
],
}

BLOCK = re.compile(r"[ \t]*<!-- FIG -->.*?<!-- /FIG -->[ \t]*\n?", re.S)


def strip(text):
    return BLOCK.sub("", text)


def post_file(prefix):
    for f in os.listdir(POSTS):
        if f.startswith(prefix + "-") and f.endswith(".md"):
            return os.path.join(POSTS, f)
    raise SystemExit(f"no post for {prefix}")


def insert(prefix, figs):
    path = post_file(prefix)
    text = strip(open(path).read())
    missing = []
    for marker, fig in figs:
        m = marker.replace("\n", " ")
        # match ignoring line breaks inside the marker
        pat = re.compile(re.escape(m).replace(r"\ ", r"\s+"))
        hit = pat.search(text)
        if not hit:
            missing.append(marker)
            continue
        line_start = text.rfind("\n", 0, hit.start()) + 1
        block = f"<!-- FIG -->\n{fig}\n<!-- /FIG -->\n"
        if text[line_start:line_start + 1] == "#":            # heading: put the figure after it
            line_end = text.find("\n", hit.end())
            text = text[:line_end + 1] + "\n" + block + text[line_end + 1:].lstrip("\n")
        else:
            text = text[:line_start] + block + text[line_start:]
    open(path, "w").write(text)
    return missing


if __name__ == "__main__":
    if "--strip" in sys.argv:
        for f in os.listdir(POSTS):
            if f.endswith(".md"):
                p = os.path.join(POSTS, f); t = strip(open(p).read()); open(p, "w").write(t)
        print("stripped"); sys.exit()
    total, bad = 0, []
    for prefix, figs in FIGS.items():
        miss = insert(prefix, figs)
        total += len(figs) - len(miss)
        bad += [(prefix, m) for m in miss]
    print(f"{total} figures inserted into {len(FIGS)} posts")
    for prefix, m in bad:
        print("  MISSING", prefix, repr(m[:50]))
