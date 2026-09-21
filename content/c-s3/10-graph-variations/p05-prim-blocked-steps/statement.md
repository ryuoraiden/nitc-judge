# Prim with blocked edges, printing every step

**This is a reconstruction** of your Week 5 modification question: Prim's algorithm,
printing the MST after every step, with some edges blocked. The official format is lost,
so this follows Week 5 Q1/Q2's conventions.

## Input format

```
n m s
u1 v1 w1          (m undirected edges, positive distinct weights)
...
b
x1 y1             (b blocked edges - they may not be used)
...
```

## Output format

Run Prim from `s`. After **each vertex joins the tree** (with its edge), print the
current tree as an `n x n` matrix (`0` diagonal, weight for a chosen edge in both
directions, `-1` otherwise). Then print the final tree once more, then the total cost.
If the blocked edges leave some vertex unreachable, print `-1` and nothing else.

## Sample

```
5 7 1
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 10
4 5 7
1
2 3
```

```
0 -1 2 -1 -1
-1 0 -1 -1 -1
2 -1 0 -1 -1
-1 -1 -1 0 -1
-1 -1 -1 -1 0
0 4 2 -1 -1
4 0 -1 -1 -1
2 -1 0 -1 -1
-1 -1 -1 0 -1
-1 -1 -1 -1 0
0 4 2 -1 -1
4 0 -1 5 -1
2 -1 0 -1 -1
-1 5 -1 0 -1
-1 -1 -1 -1 0
0 4 2 -1 -1
4 0 -1 5 -1
2 -1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
0 4 2 -1 -1
4 0 -1 5 -1
2 -1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
18
```

Blocking `2-3` (the cheapest edge, weight 1) forces 2 to attach through `1-2` instead,
and the cost rises from 15 to 18.

## The twist is not in the algorithm

A blocked edge is simply an edge that does not exist. Read the blocked pairs and zero
them out of the weight matrix (both directions), and what remains is exactly Week 5
Q1. Modification questions are often like this: the twist changes the *input*, and
recognising that saves you from rewriting the algorithm.

## Prim vs Kruskal snapshots

Prim's snapshots grow **one connected tree** outward from `s`. Kruskal's (Week 5 Q2)
can show several disconnected fragments that merge later. If an exam shows you a
sequence of partial trees, that is the quickest way to tell which algorithm produced
them.
