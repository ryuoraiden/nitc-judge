# Topological sort (Kahn), lexicographically smallest

An ordering of the vertices such that every edge `u -> v` has `u` before `v`. Among all
valid orders, print the **lexicographically smallest**.

```c
int topoSort(const Graph *g, int order[]);   /* returns n, or 0 if impossible */
```

## Input format

```
n m
u1 v1
...
```

`m` **directed** edges. Print the order, or `IMPOSSIBLE` if the graph has a cycle.

## Example

```
5 5
1 2
1 3
2 4
3 4
4 5
```

```
1 2 3 4 5
```

## Kahn's algorithm

Count `indeg[v]`, the number of edges pointing into `v`. A vertex with indegree 0 has
no unmet prerequisite, so it can go next. Output it, then decrement the indegree of
everything it points to - as though deleting it from the graph - and repeat.

If a round finds no vertex with indegree 0 while vertices remain, every remaining
vertex depends on another remaining one, which can only happen if there is a **cycle**.
So Kahn's algorithm detects cycles for free.

## Getting the smallest order

Whenever several vertices have indegree 0, any of them is valid - so pick the
**smallest-numbered** one. With `n <= 100` a linear scan for the smallest available
vertex is completely fine and much easier to get right than a heap.
