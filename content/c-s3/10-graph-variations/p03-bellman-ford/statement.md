# Bellman-Ford: distances with negative edges

The Week 4 sheet only asked you to *detect* a negative cycle. This is the algorithm
doing its actual job: distances from a source when some edges are negative.

## Input format

```
n m s
u1 v1 w1
...
```

`m` **directed** edges; weights may be negative.

## Output format

If a negative cycle is **reachable from `s`**, print `NEGATIVE CYCLE`. Otherwise print
`dist[1] ... dist[n]` on one line, with `INF` for unreachable vertices.

(Not `-1`: with negative weights, `-1` is a perfectly real distance. A question with
negative edges that asks for `-1` on unreachable is ambiguous, and worth pointing out.)

## Sample

```
5 10 1
1 2 6
1 3 7
2 3 8
2 4 5
2 5 -4
3 4 -3
3 5 9
4 2 -2
5 4 7
5 1 2
```

```
0 2 7 4 -2
```

## The algorithm

Relax **every edge**, `n-1` times over. A shortest simple path has at most `n-1` edges,
and each full pass extends the set of correct distances by at least one more edge
along every path - so after `n-1` passes, everything is final.

If a further pass can still improve something, there is no final answer: a negative
cycle lets you keep going round. That is the detection step.

## The INF guard

```c
if (dist[u] == INF) continue;
```

Without it, an edge out of an unreachable vertex with weight `-3` "improves" its target
to `INF - 3`, and unreachable vertices start printing as enormous numbers. Worse, a
negative cycle that `s` **cannot reach** gets reported, though it has no effect on any
distance from `s`. Test 3 is exactly that graph.

## Dijkstra vs Bellman-Ford, for the viva

| | Dijkstra (O(V^2) array) | Bellman-Ford |
|---|---|---|
| time | `O(V^2)` | `O(VE)` |
| negative edges | wrong answers | correct |
| negative cycles | cannot detect | detects |
| idea | finalise the closest vertex greedily | relax everything, repeatedly |
