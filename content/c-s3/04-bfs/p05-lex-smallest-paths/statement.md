# Lexicographically smallest shortest paths

This is the rule at the heart of Week 4 Practice Question 1.

When several shortest paths tie, you must report the **lexicographically smallest**
one: compare the two vertex sequences position by position, and the one with the
smaller vertex at the first difference wins.

```c
void lexShortestPaths(const Graph *g, int s, int parent[]);
```

Fill `parent[]` so that walking it back from any reachable `v` spells the
lexicographically smallest shortest path. `parent[s] = -1`, and `-1` for
unreachable vertices too.

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

One line per vertex `1..n`: the path from `s`, joined by `-`. Unreachable prints
`-1`.

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
1
1-4-2
1-3
1-4
1-4-2-5
```

## Now stop and think before you code

The instinct is to compare candidate paths whenever a vertex could be reached from
two different parents. **Do not.** Plain BFS with `parent[v] = u` on first discovery
already produces the lexicographically smallest path - provided each adjacency list
is ascending, which the builder guarantees.

Here is the argument, and it is worth following rather than taking on trust.

All shortest paths to a level-`d` vertex have the same length, so comparing them
lexicographically means comparing them position by position over equal lengths.

*Base:* level 1 vertices are the neighbours of `s`, and they enter the queue in
ascending order. Their paths are `s-v`, so queue order is lexicographic order.

*Step:* suppose every vertex at level `d` entered the queue in lexicographic order
of its path. BFS expands them in exactly that order. When we expand `u`, we offer
its neighbours in ascending order. A level-`d+1` vertex `w` discovered from `u` gets
the path `path(u) + w`. If `u1` was queued before `u2` then `path(u1) < path(u2)`,
and since both have the same length, appending anything preserves that order. Within
a single `u`, smaller `w` comes first. So level `d+1` also enters the queue in
lexicographic order - and the first parent to claim each vertex is the best one.

The rule you actually implement: **sort the adjacency lists, and let first discovery
win.** No path comparison anywhere.
