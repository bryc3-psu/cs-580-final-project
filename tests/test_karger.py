import pytest
from karger import UnionFind

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
    uf.union(0, 1)
    uf.union(2, 3)
    assert uf.find(0) == uf.find(1)
    assert uf.find(2) == uf.find(3)
    assert uf.find(4) != uf.find(0)

  def test_find_transitivity(self):
    # indirectly merged nodes share a root
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
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
    result = uf.union(0, 1)
    assert result == True
    assert uf.find(0) == uf.find(1)
    assert uf.count == 4

  def test_union_same_supernode(self):
    # union on already-merged nodes returns False and doesn't change count
    uf = UnionFind(5)
    uf.union(0, 1)
    result = uf.union(0, 1)
    assert result == False
    assert uf.count == 4

  def test_union_size_tracking(self):
    # size of tree is accurate
    uf = UnionFind(4)
    uf.union(0, 1)
    assert uf.size[uf.find(0)] == 2
    uf.union(2, 3)
    uf.union(0, 2)
    assert uf.size[uf.find(0)] == 4

  def test_union_by_size_larger_becomes_root(self):
    # larger supernode is the root after union
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(0, 2)  # size root0 = 3
    uf.union(3, 4)  # size root3 = 2
    uf.union(0, 3)
    assert uf.find(3) == uf.find(0)
    assert uf.size[uf.find(0)] == 5

  def test_union_all_nodes(self):
    # merging all nodes leaves one supernode
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(2, 3)
    uf.union(3, 4)
    assert uf.count == 1
    assert len(set(uf.find(i) for i in range(5))) == 1

  def test_union_independent_supernodes(self):
    # unions doesnt effect independent supernodes
    uf = UnionFind(6)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(4, 5)
    assert uf.count == 3
    assert uf.find(0) == uf.find(1)
    assert uf.find(2) == uf.find(3)
    assert uf.find(4) == uf.find(5)
    assert uf.find(0) != uf.find(2)
    assert uf.find(0) != uf.find(4)
    assert uf.find(2) != uf.find(4)
