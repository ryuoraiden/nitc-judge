# Prim: grow the tree from a source

```c
int prim(int n, int w[MAXV][MAXV], int src, int parent[]);
```

Start from `src` and repeatedly attach the cheapest edge that reaches a new vertex.
Return the total weight, or `-1` if some vertex cannot be reached.

## Input format

```
n m s
u1 v1 w1
...
```

Undirected weighted edges; `w[u][v] == 0` means no edge. Print the cost on one line,
then `parent[1..n]` (with `-1` for the source).

## Example

```
5 7 1
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 10
4 5 7
```

```
15
-1 3 1 2 4
```

## Prim vs Dijkstra: one character of difference

The loops are identical - pick the smallest-key unfinished vertex, mark it done, then
update its neighbours. The update is where they diverge:

| | update |
|---|---|
| Dijkstra | `if (dist[u] + w[u][v] < dist[v])` - distance from the source |
| Prim | `if (w[u][v] < key[v])` - weight of one edge |

Dijkstra accumulates a path length; Prim only cares how cheaply `v` can be hooked onto
the tree that exists so far. Writing `key[u] + w[u][v]` by reflex gives you a shortest
path tree, which is a different tree, and often a more expensive one.

## Why greedy is safe here

The **cut property**: for any split of the vertices into "in the tree" and "not in the
tree", the cheapest edge crossing that split belongs to some MST. Prim picks exactly
that edge every round.
