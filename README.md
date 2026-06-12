# CS-580 Final Project: Karger  vs. Karger-Stein 

This is an implementation of the Karger and Karger-Stein min-cut algorithms for our CS-580 final. 

## Setup

**Requires Python 3.10+**

To get up and runing follow these steps:

```bash
# clone the repo
git clone https://github.com/bryc3-psu/cs-580-final-project
cd cs-580-final-project

# create and source venv
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
pip install -e .

# generate the graph dataset
# note: this is computationally expensive and takes some time
python scripts/generate_dataset.py
```

## Scripts

After setup you can run these scripts to reproduce our results.

### `scripts/exp1.py`
For each graph of size $n$, run both algorithms $R=10$ times on each of the $100$ graphs and record the fraction of runs that successfully returned the true min-cut value. Then average the success rate across all $100$ graphs at each size to obtain an empirical per-trial success probability $p$.

### `scripts/exp2.py`
For each graph (sweeping across size $n$), run both algorithms repeatedly until they return the true min-cut value (capped at 1000 attempts). Then record the average across all $100 graphs at each size $n$ to obtain an empirical number of required trials $t$ for a high probability of success.
