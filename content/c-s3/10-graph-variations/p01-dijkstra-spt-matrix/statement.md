# Dijkstra: print the shortest-path tree as a matrix

**This is a reconstruction** of your Week 4 modification question from memory - the
exact wording is lost, but the twist was printing the shortest-path tree as a matrix.

> Given a directed weighted graph as an adjacency matrix (`999` = no direct edge) and a
> source `s`, run Dijkstra from `s` and print the **shortest-path tree** as an `n x n`
> matrix.

## Input format

- first line: `n`
- next `n` lines: the adjacency matrix (`0` on the diagonal, `999` = no edge, weights
  otherwise, all non-negative)
- last line: the source `s` (1-based)

## Output format

An `n x n` matrix: `0` on the diagonal, `w` at `[u][v]` when the edge `u -> v` is in the
shortest-path tree, `-1` everywhere else. In every test the shortest path to each vertex
is unique, so the tree is unique.

## Sample

```
5
0 5 999 999 2
999 0 1 1 999
999 999 0 2 9
999 999 999 0 10
999 2 7 999 0
1
```

```
0 -1 -1 -1 2
-1 0 1 1 -1
-1 -1 0 -1 -1
-1 -1 -1 0 -1
-1 2 -1 -1 0
```

Vertex 2 is reached `1 -> 5 -> 2` (cost 4, beating the direct 5), so its tree edge is
`5 -> 2`. Vertices 3 and 4 hang off 2.

## What a shortest-path tree is

Every shortest path from `s` is "shortest path to some earlier vertex, plus one edge".
So if every vertex remembers just **which vertex it was reached from**, those links
together form a tree rooted at `s`, and walking them backwards gives every shortest
path. That is the `parent[]` array - the same idea as BFS path reconstruction, now with
weights.

Record it at the only moment it can change:

```c
if (dist[u] + w[u][v] < dist[v]) {
    dist[v] = dist[u] + w[u][v];
    parent[v] = u;
}
```

## Shortest-path tree is not a minimum spanning tree

Same kind of output as Week 5, different tree. The SPT minimises each vertex's
**distance from `s`**; the MST minimises the **total edge weight**. On the sample, the
MST would not necessarily contain `5 -> 2`. If a question says "tree" and "source",
read carefully which one it means.

## If ties were allowed

With two equally short routes to `v`, strict `<` keeps whichever parent found it first,
while `<=` keeps the last. Both are valid trees. The tests avoid ties so that either is
accepted - but in an exam, say which rule you used.
