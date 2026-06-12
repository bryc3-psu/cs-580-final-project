import os
import pickle
import random
from multiprocessing import Pool
from graphgen import GraphGenerator

DATA_DIR = "./data/graphs/by_size"
os.makedirs(DATA_DIR, exist_ok=True)
gen = GraphGenerator()
k = 100

def _save(graphs, path):
  if os.path.exists(path):
    print(f"'{os.path.basename(path)}' already exists, skipping...")
    return
  with open(path, "wb") as file:
    pickle.dump(graphs, file)

  print(f"Saved {len(graphs)} graphs to '{path}'.")

def generate_and_save(n):
  graphs = gen.generate_er(k, n_values=[n])
  _save(graphs, f"{DATA_DIR}/graphs_er_{n}.pkl")

if __name__ == "__main__":
  with Pool() as pool:
    pool.map(generate_and_save, range(10, 60, 10))
