# Dijkstra: how many shortest paths?

A standard way to make Dijkstra "not straightforward": don't just ask for the shortest
distance, ask **how many different paths achieve it**.

```c
void dijkstraCount(const WGraph *g, int s, int dist[], long long ways[]);
```

## Input format

```
n m
u1 v1 w1
...
s t
```

`m` **directed** edges, weights `>= 1`. Print `dist[t]` and `ways[t]` on two lines, or
`-1` and `0` if `t` is unreachable.

## Example

```
4 4
1 2 1
1 3 1
2 4 1
3 4 1
1 4
```

```
2
2
```

Two paths of length 2: `1-2-4` and `1-3-4`.

## The two-line change

Dijkstra already visits vertices in order of final distance. When it relaxes an edge
`u -> v` giving candidate distance `nd`:

| case | meaning | update |
|---|---|---|
| `nd < dist[v]` | a strictly shorter route | `dist[v] = nd; ways[v] = ways[u];` |
| `nd == dist[v]` | another route of the same best length | `ways[v] += ways[u];` |
| `nd > dist[v]` | worse | nothing |

The reset in the first row matters: every route counted so far was longer, so they
stop counting.

## How big can the count get?

Exponentially big. Give vertex `i` an edge to every `j > i` of weight `j - i` and
*every* path from 1 to `n` is a shortest path: `2^(n-2)` of them. At 65 vertices that
no longer fits in a `long long` and the count silently goes negative. These tests keep
the answer well inside `long long`; in an exam, a question that can produce huge counts
will say "print it modulo 10^9+7" - apply `% MOD` at both update lines if it does.

## Why positive weights

The count is right only if `ways[u]` is complete when you relax out of `u` - that is,
every shortest route into `u` has already been counted. Dijkstra guarantees that
because it finalises `u` only after everything closer. A zero-weight edge could let a
vertex at the same distance feed `u` *after* `u` was finalised, so this question
always guarantees weights `>= 1`.

The same pattern answers "minimum number of edges among all shortest paths", or "the
maximum total bonus along a shortest path" - keep a second array and update it with the
same three-way comparison.
