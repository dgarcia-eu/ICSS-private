#!/usr/bin/env python3
"""Write Exams/Solutions/Pool-N-*-Solutions.md from the pool files.

Each pool item keeps its worked solution and marking notes in the pool file
(the question bank is the master copy). This script extracts them into one
solutions file per pool and adds, for every item, where the material is in the
slides and in the handouts (the lecture transcripts). Re-run after editing a
pool or the reference table below:

    python3 tools/gensolutions.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
POOLS = os.path.join(ROOT, "Exams")
OUT = os.path.join(POOLS, "Solutions")
os.makedirs(OUT, exist_ok=True)

DECK = {
    "01": "ICSS-2026-01-Introduction", "02": "ICSS-2026-02-InformationCoding",
    "03": "ICSS-2026-03-DataStructures", "04": "ICSS-2026-04-Software",
    "05": "ICSS-2026-05-Algorithms", "06": "ICSS-2026-06-Recursion",
    "07": "ICSS-2026-07-SortingAlgorithms", "08": "ICSS-2026-08-TimeComplexity",
    "09": "ICSS-2026-09-TheoreticalCS", "10": "ICSS-2026-10-MachineLearning",
    "11": "ICSS-2026-11-Databases", "12": "ICSS-2026-12-ParallelProgramming",
    "13": "ICSS-2026-13-SocialScienceApplications",
}
TRANSCRIPT = {
    "01": "01-Introduction.md", "02": "02-InformationCoding.md", "03": "03-DataStructures.md",
    "04": "04-Software.md", "05": "05-Algorithms.md", "06": "06-Recursion.md",
    "07": "07-SortingAlgorithms.md", "08": "08-TimeComplexity.md", "09": "09-TheoreticalCS.md",
    "10": "10-MachineLearning.md", "11": "11-Databases.md", "12": "12-ParallelProgramming.md",
    "13": "13-SocialScienceApplications.md",
}


def anchor(title):
    """GitHub/pandoc-style anchor of a heading."""
    t = title.lower()
    t = re.sub(r"[^\w\s-]", "", t)
    return re.sub(r"\s+", "-", t.strip())


def headings():
    """{session: {number: (title, anchor)}} from the numbered transcript sections."""
    H = {}
    for sess, fname in TRANSCRIPT.items():
        H[sess] = {}
        for line in open(os.path.join(ROOT, "Transcripts", fname)):
            m = re.match(r"^## (\d+)\. (.+?)\s*$", line)
            if m:
                title = m.group(2)
                custom = re.search(r"\s*\{#([\w-]+)\}$", title)   # an explicit id, as in "## 4. Title {#id}"
                if custom:
                    title = title[:custom.start()]
                    H[sess][m.group(1)] = (title, custom.group(1))
                else:
                    H[sess][m.group(1)] = (title, anchor(f"{m.group(1)}. {title}"))
    return H


HEAD = headings()


def where(spec):
    """spec: list of ("slides", sess, "a-b", "titles") or ("handout", sess, "n") entries."""
    slides, hand = [], []
    for kind, sess, rng, *rest in spec:
        if kind == "slides":
            slides.append(f"session {int(sess)}, slides {rng.replace('-', ' to ')} (*{rest[0]}*), in `Slides/{DECK[sess][10:]}/{DECK[sess]}.qmd`")
        else:
            title, anc = HEAD[sess][rng]
            hand.append(f"[{int(sess):02d} §{rng} {title}](../../Transcripts/{TRANSCRIPT[sess]}#{anc})")
    parts = []
    if slides:
        parts.append("Slides: " + "; ".join(slides) + ".")
    if hand:
        parts.append("Handout: " + ", ".join(hand) + ".")
    return "**Where to look.** " + " ".join(parts)


S, H = "slides", "handout"
# --------------------------------------------------------------------- references
REFS = {
 # Pool 1
 "IC-01": [(S, "02", "17-30", "Positional number systems; Conversions between number systems"), (H, "02", "4"), (H, "02", "5")],
 "IC-02": [(S, "02", "17-30", "Positional number systems; Conversions between number systems"), (H, "02", "4"), (H, "02", "5")],
 "IC-03": [(S, "02", "17-30", "Conversions between number systems"), (H, "02", "5")],
 "IC-04": [(S, "02", "34-38", "Floating-point numbers: IEEE 754"), (H, "02", "7")],
 "IC-05": [(S, "02", "34-38", "Floating-point numbers: IEEE 754"), (H, "02", "7")],
 "IC-06": [(S, "02", "34-41", "Floating-point numbers: IEEE 754; Rounding errors"), (H, "02", "7"), (H, "02", "8")],
 "IC-07": [(S, "02", "34-41", "Floating-point numbers: IEEE 754; Rounding errors"), (H, "02", "7"), (H, "02", "8")],
 "IC-08": [(S, "02", "17-30", "Conversions between number systems"), (H, "02", "5")],
 "IC-09": [(S, "02", "31-33", "Negative numbers; Overflow"), (H, "02", "6")],
 "IC-10": [(S, "02", "9-13", "Measuring information in bits; Encoding information more efficiently"), (H, "02", "1"), (H, "02", "2")],
 "IC-11": [(S, "02", "9-13", "Measuring information in bits; Encoding information more efficiently; Decoding information"), (H, "02", "2")],
 "IC-12": [(S, "02", "17-30", "Conversions between number systems"), (S, "02", "50-55", "Python data types and binary operations; Operators"), (H, "02", "5"), (H, "02", "10")],
 "IC-13": [(S, "02", "34-41", "Floating-point numbers: IEEE 754; Rounding errors"), (H, "02", "7"), (H, "02", "8")],
 "IC-14": [(S, "02", "9-13", "Measuring information in bits; Encoding information more efficiently"), (H, "02", "2")],
 # Pool 2
 "DS-01": [(S, "05", "26-29", "Abstract data structures; Queues; Stacks"), (H, "05", "6"), (H, "03", "1")],
 "DS-02": [(S, "03", "8-12", "Arrays; Linked lists"), (H, "03", "2"), (H, "03", "3"), (H, "03", "4")],
 "DS-03": [(S, "03", "8-9", "Arrays"), (S, "03", "33-45", "Hash tables; Dictionaries"), (H, "03", "2"), (H, "03", "8"), (H, "03", "9")],
 "DS-04": [(S, "03", "34-43", "Hashing; Hash functions; Hash collisions; Linear and random probing"), (H, "03", "8")],
 "DS-05": [(S, "03", "34-43", "Hashing; Hash functions; Hash collisions; Linear and random probing"), (H, "03", "8")],
 "DS-06": [(S, "03", "49-51", "Appendix: binary search"), (H, "03", "5")],
 "DS-07": [(S, "03", "15-32", "Binary trees; Binary search trees"), (H, "03", "6"), (H, "03", "7")],
 "DS-08": [(S, "07", "41-46", "Data structures for sorting; Heaps; Min-heaps"), (S, "07", "79", "Heapsort: pseudocode"), (H, "07", "8")],
 "DS-09": [(S, "07", "41-46", "Heaps; Min-heaps"), (S, "07", "47-79", "Heapsort: example and pseudocode"), (H, "07", "8")],
 "DS-10": [(S, "07", "41-46", "Heaps; Min-heaps"), (H, "07", "8"), (H, "06", "2")],
 "DS-11": [(S, "03", "15-32", "Binary search trees"), (S, "06", "13-15", "Components of recursion"), (S, "06", "77", "Types of recursive algorithms"), (H, "03", "6"), (H, "06", "2"), (H, "06", "7")],
 "DS-12": [(S, "06", "24-25", "Factorial: iterative and recursive implementation"), (S, "06", "43-48", "Memory of a running program"), (H, "06", "3"), (H, "06", "4")],
 "DS-13": [(S, "03", "11-12", "Linked lists"), (S, "06", "13-15", "Components of recursion"), (S, "06", "77", "Types of recursive algorithms"), (H, "03", "3"), (H, "06", "2"), (H, "06", "7")],
 "DS-14": [(S, "03", "33-45", "Hash tables; Dictionaries in Python"), (H, "03", "8"), (H, "03", "9"), (H, "08", "9")],
 "DS-15": [(S, "03", "7-14", "Data structures; Arrays; Linked lists; The question of editing vs search"), (S, "03", "33-45", "Hash tables; Dictionaries"), (S, "05", "26-29", "Queues; Stacks"), (S, "05", "35-37", "Adjacency matrix; Adjacency list"), (S, "07", "41-46", "Heaps"), (H, "03", "4"), (H, "03", "8"), (H, "05", "6"), (H, "05", "8"), (H, "07", "8")],
 # Pool 3
 "AC-01": [(S, "05", "16-20", "Representation of algorithms; Pseudocode"), (S, "07", "6-12", "Why sort at all?; Sorting"), (H, "05", "4"), (H, "07", "1"), (H, "07", "9")],
 "AC-02": [(S, "08", "13-17", "Runtime analysis"), (S, "08", "36-40", "O-notation; Common use of O-notation"), (H, "08", "4"), (H, "08", "9")],
 "AC-03": [(S, "08", "9-12", "Complexity; A more general meaning of complexity"), (H, "08", "2")],
 "AC-04": [(S, "08", "30-38", "O-notation; Asymptotic behavior of functions; Upper bound; Growth of functions"), (H, "08", "8"), (H, "08", "9")],
 "AC-05": [(S, "07", "14-20", "Iterative sorting; Repeated minimum search; Selection sort"), (H, "07", "4")],
 "AC-06": [(S, "07", "14-20", "Repeated minimum search vs selection sort"), (S, "07", "13", "Stable vs unstable sorting"), (H, "07", "3"), (H, "07", "4")],
 "AC-07": [(S, "08", "7-8", "Recap: selection sort"), (S, "08", "13-17", "Runtime analysis example: selection sort"), (H, "08", "4"), (H, "08", "5")],
 "AC-08": [(S, "07", "22-35", "Divide and conquer; Mergesort; The MERGE function"), (S, "08", "23-24", "Complexity of mergesort"), (H, "07", "5"), (H, "07", "6"), (H, "08", "6")],
 "AC-09": [(S, "07", "13", "Stable vs unstable sorting"), (S, "07", "80", "To learn more about sorting"), (H, "07", "3"), (H, "07", "9")],
 "AC-10": [(S, "07", "37-40", "Quicksort; The PARTITION function; Quicksort: properties"), (S, "07", "80", "To learn more about sorting"), (H, "07", "7"), (H, "07", "9"), (H, "08", "9")],
 "AC-11": [(S, "07", "37-40", "Quicksort; The PARTITION function"), (H, "07", "7")],
 "AC-12": [(S, "07", "37-40", "Quicksort: properties"), (S, "08", "18-24", "Average, best and worst running time; Complexity of mergesort"), (H, "07", "7"), (H, "08", "5")],
 "AC-13": [(S, "07", "37-40", "Quicksort; The PARTITION function"), (H, "07", "7")],
 "AC-14": [(S, "05", "16-20", "Representation of algorithms; Pseudocode"), (S, "07", "14-16", "Repeated minimum search"), (S, "08", "30-38", "O-notation; Upper bound"), (H, "05", "4"), (H, "07", "4"), (H, "08", "8"), (H, "08", "9")],
 "AC-15": [(S, "03", "33-45", "Hash tables; Dictionaries"), (S, "03", "49-51", "Appendix: binary search"), (S, "08", "30-40", "O-notation and its use"), (H, "03", "8"), (H, "03", "5"), (H, "07", "9"), (H, "08", "8"), (H, "08", "9")],
 "AC-16": [(S, "03", "33-45", "Hash tables; Dictionaries"), (S, "05", "34-37", "Graphs: formalization; Adjacency matrix; Adjacency list"), (H, "03", "8"), (H, "05", "8"), (H, "08", "9")],
 "AC-17": [(S, "08", "36-40", "O-notation; Growth of functions; Common use of O-notation"), (H, "08", "9"), (H, "08", "10")],
 # Pool 4
 "GP-01": [(S, "05", "32-37", "Graphs; Graphs: formalization; Adjacency matrix"), (H, "05", "7"), (H, "05", "8")],
 "GP-02": [(S, "05", "35-37", "Adjacency matrix; Adjacency list; Adjacency matrix vs adjacency list"), (H, "05", "8")],
 "GP-03": [(S, "05", "39-50", "Example: finding distances; Algorithm: breadth-first search"), (H, "05", "9")],
 "GP-04": [(S, "06", "54-76", "Depth-first search"), (H, "06", "6")],
 "GP-05": [(S, "08", "25-28", "Complexity of BFS"), (S, "06", "54-76", "Depth-first search"), (H, "08", "7"), (H, "06", "6")],
 "GP-06": [(S, "05", "35-37", "Adjacency matrix vs adjacency list"), (H, "05", "8"), (H, "05", "10")],
 "GP-07": [(S, "08", "25-28", "Complexity of BFS"), (S, "08", "30-36", "O-notation; Upper bound"), (H, "08", "7"), (H, "08", "8")],
 "GP-08": [(S, "05", "34-37", "Graphs: formalization; Adjacency matrix"), (S, "05", "39-50", "Finding distances; Breadth-first search"), (H, "05", "8"), (H, "05", "9")],
 "GP-09": [(S, "08", "13-17", "Runtime analysis"), (S, "08", "25-28", "Complexity of BFS"), (H, "08", "4"), (H, "08", "7")],
 "GP-10": [(S, "05", "38-39", "Examples of graph problems; Example: finding distances"), (H, "05", "9")],
 "GP-11": [(S, "05", "38-39", "Examples of graph problems; Example: finding distances"), (S, "07", "41-46", "Heaps; Min-heaps"), (H, "05", "9"), (H, "07", "8")],
 "GP-12": [(S, "07", "41-46", "Heaps; Min-heaps"), (S, "08", "25-28", "Complexity of BFS"), (H, "07", "8"), (H, "08", "7")],
 "GP-13": [(S, "12", "48-49", "Limits to parallelization; Amdahl's law"), (H, "12", "11")],
 "GP-14": [(S, "12", "33-36", "Software parallelization; MapReduce"), (S, "12", "47-49", "Limitations; Limits to parallelization; Amdahl's law"), (H, "12", "9"), (H, "12", "11")],
 "GP-15": [(S, "12", "13-17", "Types of parallelization; Concurrent vs parallel; Concurrency costs and advantages"), (H, "12", "4"), (H, "12", "5")],
 "GP-16": [(S, "12", "21-29", "Instruction-level parallelism and its caveats"), (H, "12", "7")],
 "GP-17": [(S, "12", "37-47", "Distributed statistical inference; Averaging; Pearson's correlation; Limitations"), (H, "12", "10")],
 # Pool 5
 "TC-01": [(S, "09", "10-20", "Finite-state automaton and examples"), (H, "09", "2")],
 "TC-02": [(S, "09", "10-20", "Finite-state automaton and examples"), (H, "09", "2")],
 "TC-03": [(S, "09", "21-22", "Nondeterministic finite-state automata"), (H, "09", "3")],
 "TC-04": [(S, "09", "10-20", "Finite-state automaton and examples"), (S, "09", "33", "Pac-Man ghosts DFA"), (H, "09", "2")],
 "TC-05": [(S, "09", "10-20", "Finite-state automaton and examples"), (H, "09", "2")],
 "TC-06": [(S, "09", "23-32", "Formal languages and grammars; Grammar ≡ automaton; Regular languages"), (S, "09", "40", "The problem with DFA and the Chomsky hierarchy"), (H, "09", "4"), (H, "09", "5"), (H, "09", "6")],
 "TC-07": [(S, "09", "21-22", "Nondeterministic finite-state automata"), (S, "09", "31-32", "Formal languages; Regular languages"), (S, "09", "40", "The Chomsky hierarchy"), (H, "09", "3"), (H, "09", "5")],
 "TC-08": [(S, "09", "21-22", "Nondeterministic finite-state automata"), (S, "09", "10-20", "Finite-state automaton"), (H, "09", "3"), (H, "09", "2")],
 "TC-09": [(S, "09", "31-32", "Formal languages; Regular languages"), (S, "09", "40", "The Chomsky hierarchy"), (H, "09", "5"), (H, "09", "6")],
 "TC-10": [(S, "09", "69-81", "Complexity classes; P; NP; P vs NP; Reducing problems; NP-complete problems"), (H, "09", "9")],
 "TC-11": [(S, "09", "69-81", "Complexity classes; NP-complete problems; SAT"), (H, "09", "9")],
 "TC-12": [(S, "09", "80", "NP-complete example: boolean satisfiability (SAT)"), (S, "09", "73-74", "Problem verifiers; The NP class"), (H, "09", "9")],
 "TC-13": [(S, "09", "41-56", "Turing machines; Formalization; Functioning; Tape trace example"), (H, "09", "6")],
 "TC-14": [(S, "09", "71-76", "Decision problems; The P class; Problem verifiers; The NP class; Hamiltonian path"), (H, "09", "9")],
 # Pool 6
 "DB-01": [(S, "11", "22-29", "Relational databases; Database models; Building a relational database; Normal form example"), (S, "11", "33-40", "Tables in SQL; SQL schema"), (H, "11", "6"), (H, "11", "7"), (H, "11", "9")],
 "DB-02": [(S, "11", "45-47", "SQL queries: selection and projection"), (H, "11", "11")],
 "DB-03": [(S, "11", "26-29", "Building a relational database; Normal form example"), (H, "11", "6"), (H, "11", "7")],
 "DB-04": [(S, "11", "50-54", "SQL manual join; INNER JOIN; Other JOIN operations"), (H, "11", "12")],
 "DB-05": [(S, "11", "22-29", "Relational databases; Building a relational database"), (S, "11", "33-40", "Tables in SQL; SQL schema"), (H, "11", "6"), (H, "11", "7"), (H, "11", "9")],
 "DB-06": [(S, "11", "50-54", "SQL joins"), (H, "11", "12")],
 "DB-07": [(S, "05", "16-20", "Representation of algorithms; Pseudocode"), (S, "04", "11", "Imperative programming"), (H, "05", "4"), (H, "04", "3"), (H, "08", "4")],
 "DB-08": [(S, "11", "45-54", "SQL queries; Aggregation; Joins"), (S, "11", "26-29", "Building a relational database"), (H, "11", "11"), (H, "11", "12"), (H, "11", "7")],
 "DB-09": [(S, "11", "48-54", "Aggregation; Grouping; Joins"), (H, "11", "11"), (H, "11", "12")],
 "DB-10": [(S, "10", "16-18", "Error and loss; Class imbalance; The F1 score"), (H, "10", "5")],
 "DB-11": [(S, "10", "19", "Training/test split: bias and variance"), (S, "10", "22-23", "Overfitting and underfitting; The bias-variance tradeoff"), (H, "10", "6"), (H, "10", "8")],
 "DB-12": [(S, "10", "26-31", "Unsupervised machine learning; Clustering with K-means; The elbow method"), (H, "10", "10")],
 "DB-13": [(S, "10", "10-13", "Machine learning approaches; Supervised learning; Classification and regression"), (S, "10", "26-27", "Unsupervised machine learning"), (H, "10", "2"), (H, "10", "3"), (H, "10", "10")],
 "DB-14": [(S, "13", "30-33", "Agent-based modeling; Modeling segregation: Schelling's model; Segregation under tolerance"), (H, "13", "13"), (H, "13", "14")],
 "DB-15": [(S, "13", "12-19", "Digital behavioral data; Research examples; Issues with digital behavioral data: representation"), (S, "13", "28-29", "The end of theory?"), (H, "13", "6"), (H, "13", "8"), (H, "13", "12")],
 "DB-16": [(S, "13", "27-34", "Computational analysis of social science theory; Agent-based modeling; Simulating anti-COVID policies"), (H, "13", "13"), (H, "13", "15")],
}

ITEM = re.compile(r"^## ([A-Z]{2}-\d\d) · (.+?) · (.+?) · (.*)$")


def split_items(text):
    """Return (preface, [(id, title, pts, tags, question, rest)], tail)."""
    lines = text.split("\n")
    items, cur, preface, tail = [], None, [], []
    for line in lines:
        m = ITEM.match(line)
        if m:
            if cur: items.append(cur)
            cur = {"id": m.group(1), "title": m.group(2), "pts": m.group(3), "tags": m.group(4), "body": []}
            continue
        if line.startswith("## Also available"):
            if cur: items.append(cur); cur = None
            tail.append(line); continue
        if tail:
            tail.append(line)
        elif cur is None:
            preface.append(line)
        else:
            cur["body"].append(line)
    if cur: items.append(cur)
    for it in items:
        body = it["body"]
        q, rest, in_q = [], [], True
        for line in body:
            if in_q and (line.startswith(">") or line.strip() == ""):
                q.append(line); continue
            in_q = False
            rest.append(line)
        # trailing rule
        while rest and rest[-1].strip() in ("", "---"):
            rest.pop()
        text = "\n".join(rest)
        text = re.sub(r"<details><summary>Solution</summary>\s*", "**Solution.**\n\n", text)
        text = text.replace("</details>", "")
        it["question"] = "\n".join(q).strip("\n")
        it["solution"] = text.strip("\n")
    return "\n".join(preface), items


def main():
    pools = sorted(f for f in os.listdir(POOLS) if f.startswith("Pool-") and f.endswith(".md"))
    index = []
    missing = []
    for f in pools:
        text = open(os.path.join(POOLS, f)).read()
        preface, items = split_items(text)
        title = text.split("\n", 1)[0].lstrip("# ").strip()
        out = [f"# Solutions: {title}", "",
               f"*Solutions with references for [`{f}`]({os.path.join('..', f)}). Every item*",
               "*keeps its question in the pool file; here each solution starts with where the*",
               "*material is in the slides and in the handout (the lecture transcript). Slide*",
               "*numbers count the title slide as 1.*",
               "", "*Generated by `tools/gensolutions.py` from the pool file; edit the pool, not this file.*", "",
               "---", ""]
        if "recurring automaton" in preface:
            m = re.search(r"## The recurring automaton.*?(?=\n---)", preface, re.S)
            if m:
                out += [m.group(0).replace("](figures/", "](../figures/"), "", "---", ""]
        for it in items:
            out.append(f"## {it['id']} · {it['title']} · {it['pts']} · {it['tags']}")
            out.append("")
            refs = REFS.get(it["id"])
            if refs is None:
                missing.append(it["id"])
            else:
                out.append(where(refs)); out.append("")
            out.append(it["solution"].replace("](figures/", "](../figures/"))
            out += ["", "---", ""]
        path = os.path.join(OUT, f.replace(".md", "-Solutions.md"))
        open(path, "w").write("\n".join(out).rstrip("\n") + "\n")
        index.append((f, path, len(items)))
        print(f"{path}: {len(items)} items")
    readme = ["# Solutions to the exam question pools", "",
              "One file per pool. Each item's worked solution and marking notes are copied",
              "from the pool file and preceded by a **Where to look** line naming the slides",
              "(deck and slide numbers) and the handout sections (lecture transcripts, with",
              "links) that contain the material needed to develop the solution.", "",
              "These files are generated by `tools/gensolutions.py`; edit the pool files and",
              "re-run the script rather than editing them by hand.", "",
              "| Pool | Solutions | Items |", "|---|---|---|"]
    for f, path, n in index:
        readme.append(f"| [`{f}`](../{f}) | [`{os.path.basename(path)}`]({os.path.basename(path)}) | {n} |")
    readme += ["", "The example exam's marking key ([`ExamExample-2026.md`](../ExamExample-2026.md))",
               "names the pool item behind every subquestion, so its solutions are the",
               "corresponding entries in these files."]
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(readme) + "\n")
    if missing:
        print("MISSING REFS:", missing)


if __name__ == "__main__":
    main()
