# Connected components

```c
int components(const Graph *g, int comp[]);
```

Fill `comp[v]` with the component number of `v` and return how many there are.
Components are numbered `1, 2, 3, ...` **in order of their smallest vertex**.

## Input format

```
n m
u1 v1
...
```

`n` vertices numbered `1..n` and `m` **undirected** edges (each one is added in both
directions for you). Adjacency lists are sorted ascending before your function runs.

## Output

The number of components, then one line per component listing its vertices ascending.

## Example

```
6 3
1 2
2 3
4 5
```

```
3
1 2 3
4 5
6
```

## The outer loop is the whole trick

A single DFS explores exactly one component. To cover the graph you need a loop
*around* the traversal:

```c
for (int v = 1; v <= n; v++)
    if (comp[v] == 0) flood(g, v, comp, ++label);
```

That pattern - "for every unvisited vertex, start a new traversal" - is the basis of
counting components, checking bipartiteness on a disconnected graph, and finding
cycles anywhere in a graph. Every one of those questions is a plain traversal plus
this loop.

Note the reuse: `comp[]` doubles as the visited array, since `0` can mean "not yet
assigned".
