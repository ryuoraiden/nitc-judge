# BFS distances (and why BFS gives shortest paths)

```c
void bfsDistances(const Graph *g, int s, int dist[]);
```

`dist[v]` is the number of edges on a shortest path from `s` to `v`, `0` for `s`
itself, and `-1` if `v` is unreachable.

## Input format

```
n m
u1 v1
u2 v2
...
s
```

`n` vertices numbered `1..n`, `m` directed edges `u -> v`, then the source `s`.
The graph is built and its adjacency lists sorted ascending before your function
is called.

## Output

`dist[1] dist[2] ... dist[n]` on one line, space separated.

## Example

```
5 8
1 3
1 4
2 4
2 5
3 1
3 4
4 1
4 2
1
```

```
0 2 1 1 3
```

## One array, two jobs

You do not need a `visited[]` array here. `dist[v] == -1` already means "not
discovered yet". Initialise everything to `-1`, set `dist[s] = 0`, and the check
`if (dist[v] == -1)` does exactly the work `if (!visited[v])` would have.

## Why the first time you reach a vertex is the shortest time

BFS pulls vertices out of the queue in non-decreasing order of distance: everything
at distance `d` comes out before anything at distance `d+1`. So the first time `v`
is discovered, it is discovered from some `u` at the smallest possible distance, and
`dist[u] + 1` is genuinely minimal.

That guarantee is exactly what breaks once edges have different weights - a
two-edge path can be cheaper than a one-edge path - and that is the reason
Dijkstra has to exist at all. You will meet it in the next unit.
