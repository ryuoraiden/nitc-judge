# DFS, recursive

Go as deep as possible before backtracking.

```c
int dfsOrder(const Graph *g, int s, int order[]);
```

Write the visit order starting at `s` into `order[]` and return the count. Only
vertices reachable from `s` appear.

## Input format

```
n m
u1 v1
...
```

`n` vertices numbered `1..n` and `m` **undirected** edges (each one is added in both
directions for you). Adjacency lists are sorted ascending before your function runs.

Then a final line with the source `s`.

## Example

```
5 5
1 2
1 3
2 4
3 4
4 5
1
```

```
1 2 4 3 5
```

From 1 we take the smallest neighbour 2, from 2 we reach 4, from 4 we take 3 (smaller
than 5), 3 has nothing new, back to 4, then 5.

Compare that with BFS on the same graph (`1 2 3 4 5`): DFS commits to a branch, BFS
spreads out level by level.

## Where the marking goes

Mark `u` as visited at the **top of `dfs(u)`**, not only before calling it. If `u` has
two unvisited neighbours that both link onward to `w`, checking only at the call site
can enter `w` twice.
