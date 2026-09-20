# Cycle detection (directed): the three colours

```c
int hasCycleDirected(const Graph *g);
```

## Input format

```
n m
u1 v1
...
```

`m` **directed** edges `u -> v`. Only the `u -> v` direction is added.

## Example

```
3 3
1 2
2 3
1 3
```

```
0
```

Three edges and no cycle: `1 -> 3` is a shortcut, not a loop. The undirected version of
the same edge list *would* report a cycle, which is exactly why this needs its own
algorithm.

## Why "visited" alone fails

Consider `1 -> 2`, `1 -> 3`, `2 -> 3`. Exploring from 1 we finish 2 and 3, come back
to 1, and look at `1 -> 3`: vertex 3 is visited. But that is not a cycle - 3 is
*finished*, sitting below us in the DFS tree, not above us on the path.

## Three colours

| Colour | Meaning |
|---|---|
| 0 | not touched yet |
| 1 | on the path currently being explored (entered, not yet returned from) |
| 2 | fully explored, done |

Set `colour[u] = 1` on entry and `colour[u] = 2` just before returning. Hitting a
neighbour coloured **1** means an edge back into the chain you are standing on - a
cycle. Colour **2** is harmless.

This is the same machinery that makes topological sorting possible: a directed graph
has a topological order exactly when it has no cycle.
