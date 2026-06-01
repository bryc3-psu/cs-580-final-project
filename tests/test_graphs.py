import os
import pickle
import pytest
import networkx
import random
from collections import defaultdict, Counter
from graphgen import GraphInstance
 
VALID_PREFIXES = {"er", "ba", "pp", "rr", "bb", "roc"}
ALLOWED_SIZES  = range(10, 101)
DATA_DIRS      = ["./data/graphs/by_size"]
 
 
class TestGraphs:
  @classmethod
  def setup_class(cls):
    graphs = []
    for d in DATA_DIRS:
      if not os.path.exists(d):
        continue
      for fname in os.listdir(d):
        if fname.endswith(".pkl"):
          with open(os.path.join(d, fname), "rb") as f:
            graphs.extend(pickle.load(f))

    cls.graphs = graphs
    if not cls.graphs:
      pytest.fail(f"No graphs found. Did you run generate_datasets.py?")

  def test_graph_structure(self):
    failures = []
    for g in self.graphs:
      nodes = set(n for e in g.edges for n in e)
      G = networkx.Graph(g.edges)

      if len(nodes) < 2:
        failures.append(f"{g.label}: less than 2 nodes")
      if len(g.edges) == 0:
        failures.append(f"{g.label}: no edges")
      if not all(0 <= n < g.n for n in nodes):
        failures.append(f"{g.label}: edge(s) to non-existant node(s)")
      if not networkx.is_connected(G):
        failures.append(f"{g.label}: graph is not connected")
 
    assert not failures, "\n".join(failures)
 
  def test_graph_metadata(self):
    failures = []
    for g in self.graphs:
      nodes = set(n for e in g.edges for n in e)

      if g.true_cut < 1:
        failures.append(f"{g.label}: true_cut={g.true_cut} (non-positive)")
      if len(nodes) != g.n:
        failures.append(f"{g.label}: n={g.n} but the edge list uses {len(nodes)} distinct nodes")
      if not g.label or g.label.split("-")[0] not in VALID_PREFIXES:
        failures.append(f"{g.label}: unrecognized label")
 
    assert not failures, "\n".join(failures)

  def test_true_cuts(self):
    failures = []
    graph_by_types = defaultdict(list)
    sample = []
    for g in self.graphs:
      graph_by_types[g.label.split("-")[0]].append(g)
    for graphs in graph_by_types.values():
      sample.extend(random.sample(graphs, min(50, len(graphs))))
 
    for g in sample:
      try:
        G = networkx.Graph(g.edges)
        expected, _ = networkx.stoer_wagner(G)
        if expected != g.true_cut:
          failures.append(f"{g.label}: true_cut={g.true_cut} but stoer_wagner gives {expected}")
      except Exception as e:
        failures.append(f"{g.label}: stoer_wagner raised exception: {e}")

    assert not failures, "\n".join(failures)

  def test_ratio(self):
    failures = []
    expected = {"rr": 0.75, "bb": 0.25}
    type_counts = Counter(g.label.split("-")[0] for g in self.graphs)
    total = len(self.graphs)
    for type, exp_ratio in expected.items():
      actual_ratio = type_counts.get(type, 0) / total
      if abs(actual_ratio - exp_ratio) > 0.05:
        failures.append(f"'{type}' ratio={actual_ratio:.2f}, expected ~{exp_ratio} (+=0.05)")
