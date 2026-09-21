# Week 4 modification (MQ4): shortest-path tree + leaf count

**Official statement** - `Week 4 - SSSP/MQ4.pdf`. Test 1 is the sheet's sample.

> You are working as a Logistics Coordinator for a central fleet management system. Your
> primary responsibility is to dispatch delivery trucks from a central depot located in
> one city to `n - 1` other regional cities...
>
> To ensure cost efficiency, you need to construct a **Shortest Path Tree (SPT)** rooted
> at the central depot. The road network is structured such that **all cities are
> reachable** from the central depot and there is **exactly one unique shortest path**
> from the central depot to every other reachable city (distance between any two cities
> is less than 999).
>
> Your task is to:
>
> 1. Construct the optimal path tree and represent it as an `n x n` adjacency matrix
>    (where an edge exists with its edge weight only if it forms part of the Shortest
>    Path Tree, and `-1` otherwise).
> 2. Calculate the minimum number of vehicles required to cover all leaf-end
>    destinations simultaneously without overlapping terminal routes, which is **the
>    total number of leaf nodes** in the generated Shortest Path Tree.

## Input format

- first line: `n` (`n >= 2`), cities numbered `1..n`
- next `n` lines: the distance matrix, `0 <= dist[i][j] < 999`; `999` means no direct
  road between distinct cities
- last line: the depot `s`

## Output format

`n` lines: the SPT adjacency matrix (`-1` for edges not in the tree). Then one line:
the minimum number of vehicles needed.

## Sample

```
5
0 4 2 999 999
4 0 1 5 999
2 1 0 8 10
999 5 8 0 2
999 999 10 2 0
1
```

```
0 -1 2 -1 -1
-1 0 -1 5 -1
-1 1 0 -1 -1
-1 -1 -1 0 2
-1 -1 -1 -1 0
1
```

The tree is the chain `1 -> 3 -> 2 -> 4 -> 5`, so there is exactly one leaf-end
destination and one vehicle suffices.

## Three details the sample decides for you

**The matrix is directed.** The roads are two-way, yet row 1 has `2` at column 3 while
row 3 has `-1` at column 1. Each tree edge is written once, from parent to child:
`tree[parent[v]][v]`. Filling in both directions, as you would for an MST, turns this
answer wrong.

**The diagonal prints `0`, not `-1`.**

**The depot is never a leaf.** In the sample, city 1 has just one tree neighbour. Count
"vertices that are nobody's parent" and it drops out naturally; count "vertices with
one tree edge" and you get 2 instead of 1.

## Zero is a real distance

`0 <= dist[i][j]`, so a `0` **off** the diagonal is a road of length zero. Skip only
`999` and `i == j`. Test 5 has one, and treating it as "no road" changes the tree.

## Why the tree is just `parent[]`

Every shortest path from `s` is a shortest path to some earlier city plus one road.
So if every city remembers which city it was reached from, those links form a tree
rooted at `s`. Record it at the only moment it can change:

```c
if (dist[u] + w[u][v] < dist[v]) {
    dist[v] = dist[u] + w[u][v];
    parent[v] = u;
}
```

The sheet's uniqueness guarantee means `<` versus `<=` does not matter here. Without
that guarantee, the two produce different (equally valid) trees.

## Not a minimum spanning tree

It looks just like the Week 5 output, but it is a different tree. The SPT minimises each
city's distance from the depot. The MST minimises the total road length. Read which one
a question means.
