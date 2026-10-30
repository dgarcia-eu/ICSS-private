import numpy as np

def bootstrap_means(task):
    seed, n_resamples = task
    rng = np.random.default_rng(seed)
    data = np.random.default_rng(0).exponential(size=5_000)       # the same sample on every worker
    return [data[rng.integers(0, len(data), len(data))].mean() for _ in range(n_resamples)]
