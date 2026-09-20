# Week 5 Q2: Rural Power Distribution (Kruskal, step by step)

Verbatim from the Week 5 sheet.

> ...Construct the minimum-cost spanning tree by **repeatedly selecting the available
> edge with the smallest weight that does not create a cycle** with the already
> selected edges. **After adding each selected edge, display the current partial tree
> as a weighted adjacency matrix.** Continue until all `n` vertices are connected.
> After constructing the complete minimum-cost spanning tree, display the final tree
> and its total cost. If all vertices cannot be connected, print `-1`.

## Input format

```
n
m
u1 v1 w1
...
```

Note there is **no source vertex** here - that absence, plus "repeatedly selecting the
smallest available edge", is what tells you this one is Kruskal.

## Output format

After each accepted edge, the full `n x n` matrix (`0` diagonal, weight for a selected
edge, `-1` otherwise). Then the final matrix again, then the total cost. `-1` alone if
the graph cannot be connected.

## Sample

```
5
7
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 11
4 5 7
```

```
0 -1 -1 -1 -1
-1 0 1 -1 -1
-1 1 0 -1 -1
-1 -1 -1 0 -1
-1 -1 -1 -1 0
0 -1 2 -1 -1
-1 0 1 -1 -1
2 1 0 -1 -1
-1 -1 -1 0 -1
-1 -1 -1 -1 0
0 -1 2 -1 -1
-1 0 1 5 -1
2 1 0 -1 -1
-1 5 -1 0 -1
-1 -1 -1 -1 0
0 -1 2 -1 -1
-1 0 1 5 -1
2 1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
0 -1 2 -1 -1
-1 0 1 5 -1
2 1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
15
```

Four accepted edges produce four matrices, then the final tree is printed a fifth time
before the cost. **No blank lines between matrices** - that is how the official sample
prints it.

> Note: the hand-written expected outputs sitting in your `Week 5 - MST/tests/` folder
> separate the matrices with blank lines. The assignment sheet does not. The tests here
> follow the sheet.

## Rejected edges print nothing

Edge `3 4 8` closes a cycle, so it is skipped silently - no matrix for it. Only the
`n-1` accepted edges produce output.

## Watch the disconnected case

If the graph cannot be connected the expected output here is a single `-1` with **no
matrices before it**. But you only discover the failure *after* processing every edge,
by which time a naive loop has already printed several snapshots.

So either run Kruskal twice (once silently to check that you can take `n-1` edges, then
again to print), or buffer the snapshots and flush them only on success. The reference
does the two-pass version.

> This is a genuine ambiguity in the sheet, and worth knowing you have a choice to
> defend. Your own Week 5 program prints the snapshots and *then* `-1`; the
> `q2_disconnected.out` file sitting next to it contains only `-1`. The sheet says
> "If all vertices cannot be connected, print -1", so these tests follow the sheet and
> your stored expected output, not your program. If your evaluator wanted the other
> behaviour, the only change is dropping the first pass.
