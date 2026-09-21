# Floyd-Warshall: all-pairs shortest paths

Shortest distances between **every** pair of vertices, in about six lines.

## Input format

- first line: `n`
- next `n` lines: the adjacency matrix, `999` = no edge (directed; weights may be
  negative)

## Output format

The `n x n` distance matrix, `INF` where no path exists - or `NEGATIVE CYCLE` if the
graph has one.

## Sample

```
4
0 3 999 7
8 0 2 999
5 999 0 1
2 999 999 0
```

```
0 3 5 6
5 0 2 3
3 6 0 1
2 5 7 0
```

## The whole algorithm

```c
for (k = 1; k <= n; k++)
    for (i = 1; i <= n; i++)
        for (j = 1; j <= n; j++)
            if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
```

After iteration `k`, `d[i][j]` is the shortest `i -> j` path that uses **only vertices
`1..k` as stopovers**. Each new `k` asks one question per pair: "is it better to go
through `k`?". That is why `k` has to be the outer loop - by the time you consider
stopover `k`, every `d[i][k]` and `d[k][j]` must already be final for stopovers `1..k-1`.
Put `i` or `j` outermost and it still runs, still prints plausible numbers, and is
wrong.

## Two guards

- skip the update when `d[i][k]` or `d[k][j]` is `INF`, or `INF + negative` sneaks under
  `INF`
- a negative diagonal entry afterwards means a vertex reaches itself at negative cost:
  a negative cycle

## When to use which

| question | algorithm |
|---|---|
| one source, non-negative weights | Dijkstra |
| one source, negative weights | Bellman-Ford |
| every pair, small `n` (`<= 100`) | Floyd-Warshall - `O(n^3)`, tiny code |
