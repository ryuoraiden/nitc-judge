# Kruskal: total MST cost

```c
int kruskal(int n, Edge edges[], int m);   /* total weight, or -1 */
```

## Input format

```
n m
u1 v1 w1
...
```

`m` undirected weighted edges. Print the MST's total weight, or `-1` if the graph
cannot be connected.

## Example

```
5 7
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 11
4 5 7
```

```
15
```

## The algorithm in four lines

1. Sort the edges by weight.
2. Walk them cheapest-first.
3. Take an edge if its two endpoints are in **different** components (that is exactly
   what `unite` returning 1 means); skip it otherwise, because it would close a cycle.
4. Stop at `n-1` edges.

## The `-1` test

A spanning tree on `n` vertices has exactly `n-1` edges. If you run out of edges with
fewer than that, some vertices were never reachable. So the disconnection test is just
`taken == n - 1` - no separate connectivity check needed.

## The qsort comparator

C++ comparators return "is a before b?". `qsort` wants negative / zero / positive:

```c
return (x->w > y->w) - (x->w < y->w);
```

`return x->w - y->w;` also works for small weights but overflows for large ones - get
into the habit of the safe form.
