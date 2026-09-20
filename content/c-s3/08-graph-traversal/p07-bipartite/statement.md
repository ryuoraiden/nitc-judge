# Bipartite check by 2-colouring

A graph is bipartite when its vertices can be split into two sets with **every edge
going between the sets**, never inside one.

```c
int bipartite(const Graph *g, int colour[]);
```

Return 1 and fill `colour[]` with 0/1, or return 0. In each component the
smallest-numbered vertex must take colour 0, so the answer is unique.

## Input format

```
n m
u1 v1
...
```

`n` vertices numbered `1..n` and `m` **undirected** edges (each one is added in both
directions for you). Adjacency lists are sorted ascending before your function runs.

## Output

The two colour classes, one per line (colour 0 then colour 1), each ascending -
or `-1` if the graph is not bipartite.

## Example

```
4 4
1 2
2 3
3 4
4 1
```

```
1 3
2 4
```

A 4-cycle alternates fine. A 3-cycle does not, and prints `-1`.

## The algorithm

Traverse (BFS or DFS). Give the start vertex colour 0 and every neighbour the opposite
colour, `1 - colour[u]`. If you meet an already-coloured neighbour that has the **same**
colour as the vertex you are standing on, that edge joins two vertices on the same
side - not bipartite.

`colour[v] == -1` doubles as "not visited", so you need only one array.

## Do not forget the disconnected case

The graph need not be connected, so wrap the traversal in the for-every-uncoloured-
vertex loop. A graph is bipartite only if *every* component is.

## The theory fact worth remembering

A graph is bipartite **iff it contains no odd-length cycle**. The colouring is just a
constructive way of checking that.
