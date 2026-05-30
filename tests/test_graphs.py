import pickle
import pytest
import networkx
from graphgen import GraphInstance
 
VALID_PREFIXES = {"er", "ba", "pp"}
ALLOWED_SIZES  = range(10, 101)
FILE_PATH       = "./data/graphs.pkl"
 
 
class TestGraphs:
  @classmethod
  def setup_class(cls):
    try:
      with open(FILE_PATH, "rb") as file:
        cls.graphs = pickle.load(file)
    except FileNotFoundError:
      pytest.fail(f"Dataset at '{FILE_PATH}' is missing. Did you run `graphgen.py`?")

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
      try:
        G = networkx.Graph(g.edges)
        expected_cut, _ = networkx.stoer_wagner(G)
        if expected_cut != g.true_cut:
          failures.append(f"{g.label}: true_cut={g.true_cut} while stoer_wagner gives {expected_cut}")
      except Exception as e:
        failures.append(f"{g.label}: stoer_wagner raised excpetion: {e}")
 
    assert not failures, "\n".join(failures)
 
  def test_dataset(self):
    graph_types_present = set(g.label.split("-")[0] for g in self.graphs)

    failures = []
    for prefix in VALID_PREFIXES:
      if prefix not in graph_types_present:
        failures.append(f"'{prefix}' graphs types missing")
 
    for g in self.graphs:
      if g.n not in ALLOWED_SIZES:
        failures.append(f"{g.label}: n={g.n} outside allowed_sizes range")
 
    assert not failures, "\n".join(failures)
