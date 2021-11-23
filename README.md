# Sliding-block puzzle solver

We explore the speed and optimality of algorithms to solve the sliding-puzzle game. We compare A*, BFS, greedy best-first search, and a custom human-based algorithm. In the 24-puzzle game, finding the optimal solution using BFS is infeasible, finding the optimal solution using A* can take hours or days, but finding a **sub-optimal** solution using our human-based algorithm takes a few seconds or minutes.

To run our human-based algorithm, clone or download the repo and run:

```
python solver.py
```

To run the A\* search algorithm run:

```
python solver.py --astar
```
