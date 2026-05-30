# CS-580 Final Project: Karger  vs. Karger-Stein 

## Modules

### `karger.py`

This module implements the classic karger and the karger-stein contraction algorithms using
the UnionFind data structure for supernodes.

**Interface**

 
- `Karger(edges, n)` 
- `karger_run()` -> `int` 
- `karger_repeated(num_runs)` -> `(int, int)` 
- `stein_run()` -> `int` 
- `stein_repeated(num_runs)` -> `(int, int)` 
