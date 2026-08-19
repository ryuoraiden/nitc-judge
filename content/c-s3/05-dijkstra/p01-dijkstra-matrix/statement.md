# Dijkstra on an adjacency matrix

BFS finds shortest paths by counting edges. The moment edges have different costs,
that stops working: a two-edge route can be cheaper than a one-edge route, and BFS
would happily return the one-edge one.

Dijkstra fixes it with a greedy rule: **repeatedly settle the unfinished vertex
with the smallest known distance, then relax its outgoing edges.**

```c
void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]);
```

`dist[v]` is the cheapest cost from `src` to `v`, or `INF` if unreachable.

## Input format

```
n
<n lines of n integers: the adjacency matrix>
k
```

`time[i][j]` is the cost of the one-way edge `i -> j`. A value of **999** means
there is no such edge. The diagonal is 0. `k` is given **1-based**; the harness
converts it before calling you, so your `src` is already 0-based.

## Output

`dist[0] dist[1] ... dist[n-1]`, space separated. Unreachable prints `-1`.

## Example

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
0 4 5 5 2
```

Note vertex 2: the direct road `1 -> 2` costs 5, but going `1 -> 5 -> 2` costs
`2 + 2 = 4`. That is precisely the case BFS gets wrong.

## The 999 trap

`999` means **no edge**, not "an edge costing 999". Forget the guard and you invent
roads: paths appear that should not exist, and the answers come out too small on
exactly the sparse graphs where it matters. Test 4 is a graph with no edges at all,
which fails loudly if you got this wrong.

## Why the greedy choice is safe

When you pick the unfinished vertex `u` with the smallest `dist[u]`, that value is
already final. Any other route to `u` would have to leave the settled set through
some unfinished vertex `x`, and `dist[x] >= dist[u]` by choice of `u` - so that
route is already at least as long before it even arrives.

That argument leans on one thing: **edge weights are non-negative**. With a negative
edge, a longer-looking detour could still reduce the total, and the whole guarantee
collapses. That is why the last problem in this unit needs a completely different
algorithm.

## Complexity

This version is `O(V^2)`: `V` rounds, each doing a linear scan for the minimum. For
a dense matrix that is optimal. You will replace the scan with a heap in problem 4.
