# implementation of the karger and karger-stein contraction algorithms
# using the UnionFind datastructure

import random
from math import ceil, sqrt
from dataclasses import dataclass

class UnionFind:
  def __init__(self, n: int) -> None:
    self.parent: list[int] = list(range(n))
    self.size: list[int] = [1] * n
    self.count: int = n

  def copy(self) -> 'UnionFind':
    uf = UnionFind.__new__(UnionFind)
    uf.parent = self.parent.copy()
    uf.size = self.size.copy()
    uf.count = self.count
    return uf

  def find(self, x: int) -> int:
    root: int = x

    # a root node is just a node that is its own parent
    while self.parent[root] != root:
      root = self.parent[root]

    # optimization: compress paths by pointing nodes directly to root
    while self.parent[x] != root:
      next_node: int = self.parent[x]
      self.parent[x] = root
      x = next_node

    return root

  def merge(self, edge: tuple[int, int]) -> bool:
    root_x, root_y = self.find(edge[0]), self.find(edge[1])

    if root_x == root_y:
      return False

    # union by size: attach the smaller tree under the larger
    # to keep find() efficient
    if self.size[root_x] < self.size[root_y]:
      root_x, root_y = root_y, root_x

    self.parent[root_y] = root_x
    self.size[root_x] += self.size[root_y]
    self.count -= 1
    return True

@dataclass
class GraphState:
  edges: list[tuple[int, int]]
  uf: UnionFind

class Karger:
  def __init__(self, edges: list[tuple[int, int]], n: int) -> None:
    self.edges = edges
    self.n = n

  def _contract(self, state: GraphState, stop_at: int) -> GraphState:
    uf = state.uf.copy()
    remaining = state.edges.copy()

    while uf.count > stop_at:
      # merge supernodes, then remove self looping edges
      uf.merge(random.choice(remaining))
      remaining = [(x, y) for x, y in remaining if uf.find(x) != uf.find(y)]

    return GraphState(edges=remaining, uf=uf)

  def _stein_rec(self, state: GraphState) -> int:
    # base case: two supernodes remain
    if state.uf.count <= 3:
      return len(self._contract(state, stop_at=2).edges)

    next_stop = ceil(state.uf.count / sqrt(2))

    # contract until next_stop, and then do two independent recursive branches
    contracted_state = self._contract(state, stop_at=next_stop)
    first  = self._stein_rec(contracted_state)
    second = self._stein_rec(contracted_state)

    return min(first, second)

  def karger_run(self) -> int:
    initial = GraphState(edges=self.edges, uf=UnionFind(self.n))
    return len(self._contract(initial, stop_at=2).edges)

  def karger_repeated(self, num_runs: int) -> tuple[int, int]:
    min_cut, found_on = min(
      ((self.karger_run(), i) for i in range(num_runs)),
      key=lambda x: x[0]
    )
    return min_cut, found_on + 1

  def stein_run(self) -> int:
    initial = GraphState(edges=self.edges, uf=UnionFind(self.n))
    return self._stein_rec(initial)

  def stein_repeated(self, num_runs: int) -> tuple[int, int]:
    min_cut, found_on = min(
      ((self.stein_run(), i) for i in range(num_runs)),
      key=lambda x: x[0]
    )
    return min_cut, found_on + 1
