from typing import List

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
  def __init__(self, n: int) -> None:
    """
    Initialize n nodes each as their own supernode.

    Args:
      n: number of nodes in the graph
    Returns:
      None
    """
    self.parent: List[int] = list(range(n))
    self.size: List[int] = [1] * n
    self.count: int = n

  def find(self, x: int) -> int:
    """
    Find the root of the supernode that contains x.

    Args:
      x: node to search for
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

  def union(self, x: int, y: int) -> bool:
    """
    Merge (super)nodes x and y into one supernode.

    Args:
      x: first node
      y: second node
    Returns:
      bool: True if the nodes were merged
    """
    root_x, root_y = self.find(x), self.find(y)

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
 

