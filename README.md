# CS-580 Final Project: Karger  vs. Karger-Stein 

This is an implementation of the Karger and Karger-Stein min-cut algorithms for our CS-580 final. 

---

## Scripts

You can run these scripts to reproduce out results (after generating graphs wit `scripts/generate_dataset.py`)

### `scripts/exp1.py`
For each graph of size $n$, run both algorithms $R=10$ times on each of the $100$ graphs and record the fraction of runs that successfully returned the true min-cut value. Then average the success rate across all $100$ graphs at each size to obtain an empirical per-trial success probability $p$.

### `scripts/exp2.py`
For each graph (sweeping across size $n$), run both algorithms repeatedly until they return the true min-cut value (capped at 1000 attempts). Then record the average across all $100 graphs at each size $n$ to obtain an empirical number of required trials $t$ for a high probability of success.
