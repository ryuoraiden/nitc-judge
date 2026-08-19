# Practice Question 4: detect a negative cycle

From the Week 4 sheet, marked optional there. It is here because it is the cleanest
possible demonstration of where Dijkstra's guarantee actually comes from.

> Write a program that takes a weighted directed graph in the form of an adjacency
> matrix, and determines whether the graph contains any negative weight cycles.
> `999` is used to represent the absence of a direct edge between two distinct
> vertices (weight of any edge is always less than 999).

## Input format

- first line: the number of vertices `n`
- next `n` lines: the adjacency matrix

## Output format

Print `1` if there is a negative cycle, `-1` otherwise.

## Sample

```
3
0 -1 999
999 0 -2
-2 999 0
```

```
1
```

That cycle `1 -> 2 -> 3 -> 1` costs `-1 + -2 + -2 = -5`. Go round it again and the
total drops another 5. There is no shortest path at all, because there is no bottom.

## Why not Dijkstra

Dijkstra settles a vertex and never reconsiders it, justified by the argument that
no later route could come back cheaper. With a negative edge that argument fails
outright - a detour through a negative edge really can beat the direct route.

**Bellman-Ford** makes no such commitment. It relaxes *every* edge, `n-1` times over.
Since any simple path uses at most `n-1` edges, that is enough passes for every real
shortest path to settle.

## The detection trick

After `n-1` passes, everything that can settle has settled. So run **one more pass**.
If any edge can still be relaxed, the only explanation is a cycle you can keep going
round to lower the total - a negative cycle.

## Why every distance starts at 0

Ordinarily Bellman-Ford starts with `dist[src] = 0` and everything else at infinity.
Here there is no source, and a negative cycle sitting in a component unreachable from
any particular start would be missed.

Setting **every** `dist[v] = 0` is equivalent to adding an imaginary vertex with a
zero-cost edge to every real one. Now every component is reachable, and a negative
cycle anywhere will be found. It costs one line and is the whole reason this version
works on disconnected input.
