#!/usr/bin/env python3
"""Build and execute the example notebooks in Examples/notebooks/.

    python3 tools/genexnotebooks.py            # build + execute all
    python3 tools/genexnotebooks.py X05-B ...  # only these

Executed outputs are stored in the .ipynb, so the notebooks read correctly on
GitHub without a kernel. A failing cell aborts that notebook and is reported.
"""
import os
import sys
import time

import nbformat
from nbclient import NotebookClient

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from exnb_a import NB as NA  # noqa: E402
from exnb_b import NB as NB_  # noqa: E402

NB = {**NA, **NB_}
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "Examples", "notebooks")
os.makedirs(OUT, exist_ok=True)


def build(xid):
    title, cells = NB[xid]
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.metadata["language_info"] = {"name": "python"}
    for kind, src in cells:
        nb.cells.append(nbformat.v4.new_markdown_cell(src) if kind == "md"
                        else nbformat.v4.new_code_cell(src))
    return nb


def run(xid):
    nb = build(xid)
    path = os.path.join(OUT, f"{xid}.ipynb")
    t0 = time.time()
    client = NotebookClient(nb, timeout=300, kernel_name="python3",
                            resources={"metadata": {"path": OUT}}, allow_errors=False)
    try:
        client.execute()
        status = "ok"
    except Exception as e:                       # noqa: BLE001
        status = "FAILED: " + str(e).strip().splitlines()[-1][:160]
    nbformat.write(nb, path)
    return status, time.time() - t0


if __name__ == "__main__":
    ids = sys.argv[1:] or sorted(NB)
    bad = 0
    for xid in ids:
        status, dt = run(xid)
        bad += not status.startswith("ok")
        print(f"{xid}  {dt:5.1f}s  {NB[xid][0][:50]:52} {status}")
    print(f"\n{len(ids) - bad}/{len(ids)} notebooks executed cleanly")
