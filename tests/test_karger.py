import pytest
import networkx as nx
from karger import UnionFind, Karger

class TestUnion:

  # -------------------------------------------------
  # init tests
  # -------------------------------------------------
  def test_initial_state_multi_node(self):
    # each node is its own root, size 1, count equals n
    uf = UnionFind(5)
    assert uf.count == 5
    for i in range(5):
      assert uf.parent[i] == i
      assert uf.size[i] == 1

  def test_initial_state_single_node(self):
    # edge case check
    uf = UnionFind(1)
    assert uf.count == 1
    assert uf.find(0) == 0

  def test_initial_with_different_count(self):
    # passing count changes only the count var
    uf = UnionFind(10, count=5)
    assert uf.count == 5
    assert len(uf.parent) == 10
    assert len(uf.size) == 10


  # -------------------------------------------------
  # find tests
  # -------------------------------------------------
  def test_find_before_union(self):
    # find reports that every node is its own root
    uf = UnionFind(5)
    for i in range(5):
      assert uf.find(i) == i

  def test_find_after_union(self):
    # merged nodes return the same root, unmerged nodes do not
    uf = UnionFind(5)
    uf.merge((0, 1))
    uf.merge((2, 3))
    assert uf.find(0) == uf.find(1)
    assert uf.find(2) == uf.find(3)
    assert uf.find(4) != uf.find(0)

  def test_find_transitivity(self):
    # indirectly merged nodes share a root
    uf = UnionFind(5)
    uf.merge((0, 1))
    uf.merge((1, 2))
    assert uf.find(0) == uf.find(2)

  def test_find_path_compression(self):
    # all nodes on the path should point directly to root after find()
    uf = UnionFind(4)
    uf.parent = [0, 0, 1, 2]  # chain: 3->2->1->0
    uf.find(3)
    assert uf.parent[3] == 0
    assert uf.parent[2] == 0
    assert uf.parent[1] == 0

  # -------------------------------------------------
  # union tests
  # -------------------------------------------------
  def test_union_distinct_supernodes(self):
    # union merges distinct supernodes and decrements count
    uf = UnionFind(5)
    result = uf.merge((0, 1))
    assert result == True
    assert uf.find(0) == uf.find(1)
    assert uf.count == 4

  def test_union_same_supernode(self):
    # union on already-merged nodes returns False and doesn't change count
    uf = UnionFind(5)
    uf.merge((0, 1))
    result = uf.merge((0, 1))
    assert result == False
    assert uf.count == 4

  def test_union_size_tracking(self):
    # size of tree is accurate
    uf = UnionFind(4)
    uf.merge((0, 1))
    assert uf.size[uf.find(0)] == 2
    uf.merge((2, 3))
    uf.merge((0, 2))
    assert uf.size[uf.find(0)] == 4

  def test_union_by_size_larger_becomes_root(self):
    # larger supernode is the root after union
    uf = UnionFind(5)
    uf.merge((0, 1))
    uf.merge((0, 2))  # size root0 = 3
    uf.merge((3, 4))  # size root3 = 2
    uf.merge((0, 3))
    assert uf.find(3) == uf.find(0)
    assert uf.size[uf.find(0)] == 5

  def test_union_all_nodes(self):
    # merging all nodes leaves one supernode
    uf = UnionFind(5)
    uf.merge((0, 1))
    uf.merge((1, 2))
    uf.merge((2, 3))
    uf.merge((3, 4))
    assert uf.count == 1
    assert len(set(uf.find(i) for i in range(5))) == 1

  def test_union_independent_supernodes(self):
    # unions doesnt effect independent supernodes
    uf = UnionFind(6)
    uf.merge((0, 1))
    uf.merge((2, 3))
    uf.merge((4, 5))
    assert uf.count == 3
    assert uf.find(0) == uf.find(1)
    assert uf.find(2) == uf.find(3)
    assert uf.find(4) == uf.find(5)
    assert uf.find(0) != uf.find(2)
    assert uf.find(0) != uf.find(4)
    assert uf.find(2) != uf.find(4)

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
  def test_contract(self):
    failures = []
    for edges, n, _, name in self.graphs:
      k = Karger(edges, n)
      original = edges.copy()
      remaining, uf = k._contract(edges, num_supernodes=n, stop_at=2)
      if uf.count != 2:
        failures.append(f"{name}: uf.count={uf.count}, expected 2")
      if edges != original:
        failures.append(f"{name}: input edges were mutated")
      if not all(uf.find(u) != uf.find(v) for u, v in remaining):
        failures.append(f"{name}: self loops found in remaining edges")
    assert not failures, "\n".join(failures)

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
