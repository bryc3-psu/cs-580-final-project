import random
from math import ceil, sqrt

class UnionFind:
  """
  Union-find data structure to track merged supernodes
  during Karger-style algorithms.

  - find(): returns the root of the supernode a node
    belongs to
  - union(): merges two (super)nodes into one

  Supernodes are represented as trees (represented by their root), 
  implemented by the parent list. Individual nodes are therefore 
  implicitly the indices into the parent (and size) lists. Size and 
  count are bookeeping for the size of the trees and number of 
  unique (super)nodes respectively
  """
  def __init__(self, n: int, count: int = None) -> None:
    """
    Initialize n nodes each as their own supernode.

    Args:
      n (int): number of nodes in the graph
      count (int): number of starting supernodes

    Returns:
      None
    """
    self.parent: list[int] = list(range(n))
    self.size: list[int] = [1] * n
    self.count: int = count if count is not None else n

  def find(self, x: int) -> int:
    """
    Find the root of the supernode that contains x.

    Args:
      x (int): node to search for

    Returns:
      int: root of the supernode containing x
    """
    root: int = x
    
    # a root node is just a node that is its own parent
    while self.parent[root] != root:
      root = self.parent[root]

    # optimization: compress paths by pointing nodes
    # directly to root
    while self.parent[x] != root:
      next_node: int = self.parent[x]
      self.parent[x] = root
      x = next_node

    return root

  def merge(self, edge: tuple[int, int]) -> bool:
    """
    Merge (super)nodes connected by edge into one supernode.

    Args:
      edge (tuple[int, int]): the edge to merge across

    Returns:
      bool: True if the nodes were merged
    """
    root_x, root_y = self.find(edge[0]), self.find(edge[1])

    if root_x == root_y:
      return False

    # size is used as a cheap approximation for height
    # to try and attach the shorter supernode to the 
    # taller as much as possible to keep find() efficient
    if self.size[root_x] < self.size[root_y]:
      root_x, root_y = root_y, root_x

    # attach root_y's tree under root_x's tree
    self.parent[root_y] = root_x
    self.size[root_x] += self.size[root_y]

    self.count -= 1
    return True
 
class Karger:
  def __init__(self, edges: list[tuple[int, int]], n: int) -> None:
    self.edges = edges
    self.n = n

  def _contract(self, edges: list[tuple[int, int]], num_supernodes: int, stop_at: int) -> list[tuple[int, int]]:
    """
    Merge (super)nodes until `stop_at` number of supernodes remain.

    Args:
      edges (list[tuple[int, int]]): list of edges
      num_supernodes (int): current count of supernodes in graph
      stop_at (int): keep merging until this many supernodes remain

    Returns:
      list[tuple[int, int]]: remaining edges after contraction
    """
    uf = UnionFind(self.n, num_supernodes)
    # don't want to corrupt self.edges
    remaining = edges.copy()

    while uf.count > stop_at:
      # merge and remove self loops (edges starting and ending in smae supernode)
      uf.merge(random.choice(remaining))
      remaining = [(x,y) for x, y in remaining if uf.find(x) != uf.find(y)]

    # returning uf for testing, can drop it later
    return remaining, uf

  def _stein_rec(self, edges: list[tuple[int, int]], num_supernodes: int) -> int:
    """
    Recursively implements a single iteration of Karger-Stein:
      - Instead of running contract until two supernodes remain, run unril n/sqrt(2) + 1 remain
      - Then recursively do two recursive trials on the resulting contracted graph, returning the min

    Args:
      edges (list[tuple[int, int]]): list of edges
      num_supernodes (int): current numer of supernodes in the graph

    Returns:
      int: number of remaining edges (i.e. the min-cut value found)
    """
    if num_supernodes <= 3:
      remaining, _ = self._contract(edges, num_supernodes=num_supernodes, stop_at=2)
      return len(remaining)

    next_stop = ceil(num_supernodes / sqrt(2))
    remaining, uf = self._contract(edges, num_supernodes=num_supernodes, stop_at=next_stop)

    actual_supernodes = uf.count
    print(f"num_supernodes={num_supernodes}, next_stop={next_stop}, actual_supernodes={actual_supernodes}, len(remaining)={len(remaining)}")
    first = self._stein_rec(remaining, num_supernodes=actual_supernodes)
    second = self._stein_rec(remaining, num_supernodes=actual_supernodes)

    return min(first, second)
    
  def karger_run(self) -> int:
    """
    Perform a single iteration of the standard Karger contraction to find a min-cut.

    Returns:
      int: number of remaining edges (i.e. the min-cut value found)
    """
    return len(self._contract(self.edges, num_supernodes=self.n, stop_at=2)[0])

  def karger_repeated(self, num_runs: int) -> tuple[int, int]:
    """
    Perform repeated iterations of the standard karger contraction, and choose the smallest min-cut found as the min-cut.

    Args:
      num_runs (int): number of iterations to perform

    Returns:
      int: the smallest min-cut value found for all iterations
      int: number of the iteration the best min-cut was found on
    """
    min_cut, found_on = min(
      ((self.karger_run(), i) for i in range(num_runs)),
      key=lambda x: x[0]
    ) 

    return min_cut, found_on+1

  def stein_run(self) -> int:
    """
    Perform a single iteration of the Karger-Stein contraction to find a min-cut.

    Returns:
      int: number of remaining edges (i.e. the min-cut value found)
    """
    return self._stein_rec(self.edges, num_supernodes=self.n)

  def stein_repeated(self, num_runs: int) -> tuple[int, int]:
    """
    Perform repeated iterations of the Karger-Stein contraction, and choose the smallest min-cut found as the min-cut.

    Args:
      num_runs (int): number of iterations to perform

    Returns:
      int: the smallest min-cut value found for all iterations
      int: number of the iteration the best min-cut was found on
    """
    min_cut, found_on = min(
      ((self.stein_run(), i) for i in range(num_runs)),
      key=lambda x: x[0]
    ) 

    return min_cut, found_on+1
