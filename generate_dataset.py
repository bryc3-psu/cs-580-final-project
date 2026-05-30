import os
import pickle
from graphgen import GraphGenerator

DATA_DIR = "./data/graphs"
os.makedirs(DATA_DIR, exist_ok=True)
gen = GraphGenerator()

def _save(graphs, filename):
  path = f"{DATA_DIR}/{filename}"
  with open(path, "wb") as file:
    pickle.dump(graphs, file)
  print(f"Saved {len(graphs)} graphs to '{path}'.")


for n in range(10, 101, 5):
  _save(gen.generate(k=100, weights={"er": 1.0, "ba": 0, "pp": 0}, n_values=[n]), f"graphs_size_{n}.pkl")

print("\nDone!")
