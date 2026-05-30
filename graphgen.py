import os
import pickle 
import random
import networkx
from dataclasses import dataclass

# this will be the object used in experiments
@dataclass
class GraphInstance:
  edges: list[tuple[int, int]]
  n: int
  true_cut: int
  label: str

class GraphGenerator:
  # default params
  k = 100
  allowed_sizes = range(10, 101)
  weights = {"er": 0.4, "ba": 0.4, "pp": 0.2}

  def _real_k(self, graph_type: str) -> int:
    total = sum(self.weights.values())
    return round(self.k * self.weights.get(graph_type, 0) / total)
 
  def _validate(self, G: networkx.Graph) -> bool:
    if G.number_of_nodes() < 2:
      return False
    if G.number_of_edges() == 0:
      return False
    if not networkx.is_connected(G):
      return False
    return True

  def _make_instance(self, G: networkx.Graph, label: str) -> GraphInstance | None:
    try:
      true_cut, _ = networkx.stoer_wagner(G)
    except Exception:
      return None

    return GraphInstance(
            edges=list(G.edges()), 
            n=G.number_of_nodes(), 
            true_cut=true_cut, 
            label=label
           )

  def _er_generator(self) -> list[GraphInstance]:
    """
    Erdos-Renyi graph generator.

    Gen Method:
      - Start with n nodes
      - For every possible pair of nodes, with probability p: add an edge
    """
    probs  = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 
              0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
    params = [(n, p) for n in self.allowed_sizes for p in probs]

    results = []
    while len(results) < self._real_k("er"):
      n, p = random.choice(params)
      G = networkx.erdos_renyi_graph(n, p)
      if self._validate(G):
        instance = self._make_instance(G, label=f"er-{n}-{p}")
        if instance is not None:
          results.append(instance)

    return results


  def _ba_generator(self) -> list[GraphInstance]:
    """
    Barabasi-Ablert graph generator.

    Gen Method:
      - Start with small initial graph
      - Keep adding nodes until n nodes total using the following strategy:
      - With probability proportional to each nodes degree: create m edges
    """
    m_values = range(1, 6)
    params   = [(n, m) for n in self.allowed_sizes for m in m_values if m < n]

    results  = []
    while len(results) < self._real_k("ba"):
      n, m = random.choice(params)
      G = networkx.barabasi_albert_graph(n, m)
      if self._validate(G):
        instance = self._make_instance(G, label=f"ba-{n}-{m}")
        if instance is not None:
          results.append(instance)
    return results

  def _pp_generator(self) -> list[GraphInstance]:
    """
    Planted Partition graph generator.

    Gen Method:
      - Start with l groups of size k
      - For nodes in the same group: add en edge with probability p_in
      - For nodes in a different group: add en edge with probability p_out
      - Note: p_in >> p_out creates dense, well seperated clusters
    """
    p_in_values  = [0.5, 0.6, 0.7, 0.8, 0.9]
    p_out_values = [0.01, 0.05, 0.07, 0.1]
    params = [
      (l, k, p_in, p_out)
      for n in self.allowed_sizes
      for l in [2, 3, 4, 5]
      for k in [n // l] if k >= 2
      for p_in in p_in_values
      for p_out in p_out_values
    ]

    results = []
    while len(results) < self._real_k("pp"):
      l, k, p_in, p_out = random.choice(params)
      G = networkx.planted_partition_graph(l, k, p_in, p_out)
      if self._validate(G):
        instance = self._make_instance(G, label=f"pp-{l}-{k}-{p_in}-{p_out}")
        if instance is not None:
          results.append(instance)

    return results

  def generate(
    self, 
    k: int = None, 
    n_values: list[int] = None, 
    weights: dict = None
  ) -> list[GraphInstance]:
    if k is not None: self.k = k
    if n_values is not None: self.allowed_sizes = n_values
    if weights is not None: self.weights = weights

    results = []
    for name, gen_func in [("ER", self._er_generator), ("BA", self._ba_generator), ("PP", self._pp_generator)]:
      print(f"Generating {name} graphs...")
      results.extend(gen_func())

    return results

def main():
  path = "./data/graphs.pkl"
  if os.path.exists(path):
    print(f"'{path}' already exists, either move/rename/delete it before generating.")
    return

  graphs = GraphGenerator().generate()
  with open(path, "wb") as file:
    pickle.dump(graphs, file)

  print()
  print(f"Done! Saved {len(graphs)} generated graphs to '{path}'.")
 
 
if __name__ == "__main__":
  main()

