import pytest
import networkx as nx
from karger import Karger

class TestKarger:
  @classmethod
  def setup_class(cls):
    G_complete = nx.complete_graph(6)
    G_ladder   = nx.circular_ladder_graph(5)
    G_dgm      = nx.dorogovtsev_goltsev_mendes_graph(3)
    G_bridge   = nx.Graph()
    G_bridge.add_edges_from([
      # group 1
      (0,1), (0,2), (0,3), (0,4), (0,5),
      (1,2), (1,3), (1,4), (1,5),
      (2,3), (2,4), (2,5),
      (3,4), (3,5),
      (4,5),
      # group 2
      (6,7),  (6,8),  (6,9),  (6,10), (6,11),
      (7,8),  (7,9),  (7,10), (7,11),
      (8,9),  (8,10), (8,11),
      (9,10), (9,11),
      (10,11),
      # bridge
      (0,6)
    ])

    cls.graphs = [
      (list(G_bridge.edges()),   G_bridge.number_of_nodes(),   1,                              "two_cliques_bridge"),
      (list(G_complete.edges()), G_complete.number_of_nodes(), nx.stoer_wagner(G_complete)[0], "complete_k6"),
      (list(G_ladder.edges()),   G_ladder.number_of_nodes(),   nx.stoer_wagner(G_ladder)[0],   "circular_ladder"),
      (list(G_dgm.edges()),      G_dgm.number_of_nodes(),      nx.stoer_wagner(G_dgm)[0],      "dorogovtsev_goltsev_mendes"),
    ]

  def test_karger_run(self):
    failures = []
    for edges, n, true_cut, name in self.graphs:
      k = Karger(edges, n)
      original = edges.copy()
      result = k.karger_run()
      if not isinstance(result, int):
        failures.append(f"{name}: result is not int")
      if result < 1:
        failures.append(f"{name}: result={result} < 1")
      if k.edges != original:
        failures.append(f"{name}: self.edges were mutated")
      if result < true_cut:
        failures.append(f"{name}: result={result} < true_cut={true_cut}")
    assert not failures, "\n".join(failures)

  def test_stein_run(self):
    failures = []
    for edges, n, true_cut, name in self.graphs:
      k = Karger(edges, n)
      original = edges.copy()
      result = k.stein_run()
      if not isinstance(result, int):
        failures.append(f"{name}: result is not int")
      if result < 1:
        failures.append(f"{name}: result={result} < 1")
      if k.edges != original:
        failures.append(f"{name}: self.edges were mutated")
      if result < true_cut:
        failures.append(f"{name}: result={result} < true_cut={true_cut}")
    assert not failures, "\n".join(failures)

  def test_karger_repeated(self):
    failures = []
    for edges, n, true_cut, name in self.graphs:
      k = Karger(edges, n)
      best_cut, found_on = k.karger_repeated(num_runs=100)
      if best_cut != true_cut:
        failures.append(f"{name}: got {best_cut}, expected {true_cut}")
      if found_on < 1 or found_on > 1000:
        failures.append(f"{name}: found_on={found_on} out of range")
    assert not failures, "\n".join(failures)

  def test_stein_repeated(self):
    failures = []
    for edges, n, true_cut, name in self.graphs:
      k = Karger(edges, n)
      best_cut, found_on = k.stein_repeated(num_runs=100)
      if best_cut != true_cut:
        failures.append(f"{name}: got {best_cut}, expected {true_cut}")
      if found_on < 1 or found_on > 1000:
        failures.append(f"{name}: found_on={found_on} out of range")
    assert not failures, "\n".join(failures)
