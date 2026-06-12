import os
import pickle
import csv
import numpy as np
from multiprocessing import Pool

from karger import Karger
from plots import line_plot

R = 10
STEP = 10
SIZES = range(10, 501, STEP)
DATA_DIR    = "./data/graphs/by_size"
RESULTS_DIR = "./data/exp1_attempt2"
os.makedirs(RESULTS_DIR, exist_ok=True)

def plot_results(avg_rows):
  n_values = np.array([r["n"] for r in avg_rows])
  n_values_smooth = list(np.linspace(n_values.min(), n_values.max(), 300))
  karger_avgs = np.array([r["karger_avg_success"] for r in avg_rows])
  stein_avgs = np.array([r["stein_avg_success"]  for r in avg_rows])

  def karger_model(n): return 1 / n**2
  def stein_model(n):  return 1 / np.log(n)

  datapoints = {
    "Karger (empirical)":       list(zip(n_values, karger_avgs)),
    "Karger-Stein (empirical)": list(zip(n_values, stein_avgs)),
    "Theoretical: 1/n^2":     list(zip(n_values_smooth, karger_model(np.array(n_values_smooth)))),
    "Theoretical: 1/log(n)": list(zip(n_values_smooth, stein_model(np.array(n_values_smooth)))),
  }

  styles = {
    "Karger (empirical)":       {"marker": "o"},
    "Karger-Stein (empirical)": {"marker": "o"},
    "Theoretical: 1/n^2":     {"linestyle": ":", "color": "gray"},
    "Theoretical: 1/log(n)": {"linestyle": ":", "color": "black"},
  }

  fig = line_plot(
    datapoints=datapoints,
    styles=styles,
    xlabel="Graph size (n)",
    ylabel="Per-run success probability",
    title="Per-run Success Probability vs Graph Size",
  )
  #fig.axes[0].set_yscale("log")

  path = f"{RESULTS_DIR}/success_rate_vs_n.png"
  fig.savefig(path, dpi=150, bbox_inches="tight")
  print(f"Saved {path}")

def save_csv(rows, filename):
  path = f"{RESULTS_DIR}/{filename}"
  with open(path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
  print(f"Saved {path}")

def process_graph(g):
  k = Karger(g.edges, g.n)
  karger_rate = sum(1 for _ in range(R) if k.karger_run() == g.true_cut) / R
  stein_rate = sum(1 for _ in range(R) if k.stein_run()  == g.true_cut) / R
  return {
    "label":               g.label,
    "n":                   g.n,
    "karger_success_rate": karger_rate,
    "stein_success_rate":  stein_rate,
  }

def run_experiment():
  raw_rows = []
  avg_rows = []

  for n in SIZES:
    path = f"{DATA_DIR}/graphs_er_{n}.pkl"
    with open(path, "rb") as f:
      graphs = pickle.load(f)

    print(f"n={n}: {len(graphs)} graphs, {R} runs each...")
    with Pool() as pool:
      rows = pool.map(process_graph, graphs)

    raw_rows.extend(rows)
    karger_rates = [r["karger_success_rate"] for r in rows]
    stein_rates  = [r["stein_success_rate"]  for r in rows]
    avg_rows.append({
      "n":                  n,
      "karger_avg_success": np.mean(karger_rates),
      "stein_avg_success":  np.mean(stein_rates),
    })

  return raw_rows, avg_rows

if __name__ == "__main__":
  #raw_rows, avg_rows = run_experiment()
  #save_csv(raw_rows, "results.csv")
  #save_csv(avg_rows, "results_avg.csv")
  #plot_results(avg_rows)
  with open(f"{RESULTS_DIR}/results_avg.csv") as f:
    avg_rows = [
      {"n": float(r["n"]), "karger_avg_success": float(r["karger_avg_success"]), "stein_avg_success": float(r["stein_avg_success"])}
      for r in csv.DictReader(f)
    ]
  plot_results(avg_rows)
