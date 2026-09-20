# Cycle detection (undirected)

```c
int hasCycle(const Graph *g);   /* 1 or 0 */
```

The graph may be disconnected.

## Input format

```
n m
u1 v1
...
```

`n` vertices numbered `1..n` and `m` **undirected** edges (each one is added in both
directions for you). Adjacency lists are sorted ascending before your function runs.

## Example

```
4 4
1 2
2 3
3 4
4 1
```

```
1
```

## Why you must pass the parent

In an undirected graph every edge appears twice - `1 2` puts 2 in 1's list *and* 1 in
2's. So when the DFS is at 2 and looks at its neighbours, it sees 1, which is already
visited. That is not a cycle; it is the edge you just arrived on.

Passing `parent` and skipping exactly that one vertex fixes it. Any other edge into an
already-visited vertex genuinely closes a loop.

## The directed case is different

For a directed graph this parent trick is wrong - there you need to know whether the
visited vertex is still **on the current recursion path** (grey) or already finished
(black). Same traversal, different bookkeeping; that is the next problem.
