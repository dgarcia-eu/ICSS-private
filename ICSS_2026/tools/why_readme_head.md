# Why it matters: one notebook per lecture

One short, standalone Jupyter notebook for each lecture from 2 to 13. Each one
runs a small experiment that shows why the content of that lecture matters in
practice for someone who computes with data: a rounding error that changes a
result, an algorithm that becomes unusable when the data grows, a query that
takes a second instead of a minute, a model that looks accurate and is not.
The notebooks are minimal on purpose. Run them, change the numbers, and watch
what happens.

They need only Python with NumPy, matplotlib, pandas, scikit-learn and SQLite
(everything in an Anaconda installation). Every notebook is executed and its
outputs are stored, so it also reads on GitHub without a kernel; the *open*
link is the rendered page. Run them from this folder
(`jupyter lab WhyItMatters`). They are built from `tools/why_NN.py` by
`tools/genwhy.py`.
