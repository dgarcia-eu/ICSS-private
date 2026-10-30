#!/usr/bin/env python3
"""Build, execute and knit the "why it matters" notebooks in WhyItMatters/.

One notebook per lecture from 2 to 13. The cells of notebook NN live in
tools/why_NN.py, which defines

    TITLE = "..."          # notebook title (also the first heading)
    HOOK  = "..."          # one sentence for the README table
    CELLS = [("md", "..."), ("code", "..."), ...]

    python3 tools/genwhy.py            # build + execute + knit all
    python3 tools/genwhy.py 05 12      # only these
    python3 tools/genwhy.py --readme   # regenerate WhyItMatters/README.md only

Executed outputs are stored in the .ipynb, so the notebooks read on GitHub
without a kernel; nbconvert writes an .html next to each one. A failing cell
aborts that notebook and is reported.
"""
import glob
import importlib
import os
import subprocess
import sys
import time

import nbformat
from nbclient import NotebookClient

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "WhyItMatters")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE)

SESSIONS = {
    "02": "InformationCoding", "03": "DataStructures", "04": "Software",
    "05": "Algorithms", "06": "Recursion", "07": "SortingAlgorithms",
    "08": "TimeComplexity", "09": "TheoreticalCS", "10": "MachineLearning",
    "11": "Databases", "12": "ParallelProgramming", "13": "SocialScienceApplications",
}
NAMES = {
    "02": "Information Coding", "03": "Data Structures", "04": "Software",
    "05": "Algorithms", "06": "Recursion", "07": "Sorting Algorithms",
    "08": "Time Complexity", "09": "Theoretical Computer Science",
    "10": "Machine Learning", "11": "Databases", "12": "Parallel Programming",
    "13": "Social Science Applications",
}


def spec(nn):
    return importlib.import_module(f"why_{nn}")


def fname(nn):
    return f"W{nn}-{SESSIONS[nn]}"


def build(nn):
    m = spec(nn)
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["language_info"] = {"name": "python"}
    for kind, src in m.CELLS:
        nb.cells.append(nbformat.v4.new_markdown_cell(src) if kind == "md"
                        else nbformat.v4.new_code_cell(src))
    return nb


def run(nn):
    nb = build(nn)
    path = os.path.join(OUT, fname(nn) + ".ipynb")
    t0 = time.time()
    client = NotebookClient(nb, timeout=600, kernel_name="python3",
                            resources={"metadata": {"path": OUT}}, allow_errors=False)
    try:
        client.execute()
        status = "ok"
    except Exception as e:                       # noqa: BLE001
        status = "FAILED: " + str(e).strip().splitlines()[-1][:160]
    nbformat.write(nb, path)
    if status == "ok":
        subprocess.run([sys.executable, "-m", "jupyter", "nbconvert", "--to", "html",
                        "--log-level", "ERROR", path], check=True)
    return status, time.time() - t0


def readme():
    rows = []
    for nn in sorted(SESSIONS):
        try:
            m = spec(nn)
        except ModuleNotFoundError:
            continue
        f = fname(nn)
        rows.append(f"| {int(nn)} {NAMES[nn]} | **{m.TITLE}**: {m.HOOK} | "
                    f"[open]({f}.html) · [ipynb]({f}.ipynb) | "
                    f"[handout](../Transcripts/{nn}-{SESSIONS[nn]}.md) |")
    text = open(os.path.join(HERE, "why_readme_head.md")).read().rstrip() + "\n\n"
    text += "| Session | Notebook | Open | Lecture |\n|---|---|---|---|\n" + "\n".join(rows) + "\n"
    open(os.path.join(OUT, "README.md"), "w").write(text)
    return len(rows)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--readme"]:
        print("readme rows:", readme()); sys.exit()
    ids = args or [nn for nn in sorted(SESSIONS)
                   if os.path.exists(os.path.join(HERE, f"why_{nn}.py"))]
    bad = 0
    for nn in ids:
        status, dt = run(nn)
        bad += not status.startswith("ok")
        print(f"W{nn}  {dt:5.1f}s  {spec(nn).TITLE[:50]:52} {status}")
    if not args and os.path.exists(os.path.join(HERE, "why_readme_head.md")):
        print("readme rows:", readme())
    sys.exit(1 if bad else 0)
