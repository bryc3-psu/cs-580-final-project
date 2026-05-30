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
  allowed_sizes = range(10, 101)

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
      true_cut, _ = networkx.edge_connectivity(G)
    except Exception:
      return None

    return GraphInstance(
            edges=list(G.edges()), 
            n=G.number_of_nodes(), 
            true_cut=true_cut, 
            label=label
           )

  # Erdos-Renyi
  def generate_er (
    self,
    k: int,
    n_values: list[int] = None,
    p_values: list[float] = None,
  ) -> list[GraphInstance]:
    if n_values is None: n_values = self.allowed_sizes
    if p_values is None: p_values = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 
                                     0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]

    results = []
    params = [(n, p) for n in n_values for p in p_values]
    while len(results) < k:
      n, p = random.choice(params)
      G = networkx.erdos_renyi_graph(n, p)
      if self._validate(G):
        instance = self._make_instance(G, label=f"er-{n}-{p}")
        if instance is not None:
          results.append(instance)

    return results

  # Random Regular
  def generate_rr(
    self,
    k: int,
    n_values: list[int] = None,
    d_values: list[int] = None,
  ) -> list[GraphInstance]:
    if n_values is None: n_values = self.allowed_sizes
    if d_values is None: d_values = [3, 4, 5, 6, 8, 10]

    results = []
    params  = [(n, d) for n in n_values for d in d_values if n > d and (n * d) % 2 == 0]
    while len(results) < k:
      n, d = random.choice(params)
      G = networkx.random_regular_graph(d, n)
      if self._validate(G):
        instance = self._make_instance(G, label=f"rr-{n}-{d}")
        if instance is not None:
          results.append(instance)

    return results
 
  # Barbell
  def generate_barbell(
    self,
    k: int,
    m1_values: list[int] = None,
    m2_values: list[int] = None,
  ) -> list[GraphInstance]:
    if m1_values is None: m1_values = list(range(3, 21))
    if m2_values is None: m2_values = list(range(0, 4))

    results = []
    params  = [(m1, m2) for m1 in m1_values for m2 in m2_values]
    while len(results) < k:
      m1, m2 = random.choice(params)
      G = networkx.barbell_graph(m1, m2)
      if self._validate(G):
        results.append(self._make_instance_known(G, label=f"bb-{m1}", true_cut=1))

    return results
 
  # Ring of Cliques
  def generate_ring_of_cliques(
    self,
    k: int,
    num_cliques_values: list[int] = None,
    clique_size_values: list[int] = None,
  ) -> list[GraphInstance]:
    if num_cliques_values is None: num_cliques_values = list(range(3, 11))
    if clique_size_values is None: clique_size_values = list(range(3, 11))

    results = []
    params  = [(nc, cs) for nc in num_cliques_values for cs in clique_size_values]
    while len(results) < k:
      nc, cs = random.choice(params)
      G = networkx.ring_of_cliques(nc, cs)
      if self._validate(G):
        results.append(self._make_instance_known(G, label=f"roc-{nc}-{cs}", true_cut=2))

    return results
 
