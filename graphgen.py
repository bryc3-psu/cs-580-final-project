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
  allowed_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
  weights = {"er": 0.4, "ba": 0.4, "pp": 0.2}

  def _er_generator(self) -> list[GraphInstance]:
    pass

  def _ba_generator(self) -> list[GraphInstance]:
    pass

  def _pp_generator(self) -> list[GraphInstance]:
    pass

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
    for gen_func in [self._er_generator(), self._ba_generator(), self._pp_generator()]:
      results.extend(gen_func())

    return results

