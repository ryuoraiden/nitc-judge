# Dijkstra with a priority queue

Same algorithm, better bookkeeping. The `O(V^2)` version spends every round doing a
linear scan to find the closest unfinished vertex. A min-heap answers that question
in `O(log V)`.

```c
void dijkstraHeap(const WGraph *g, int src, int dist[]);
```

The weighted adjacency list and the min-heap from unit 03 are both provided.
Vertices are **1-based** here.

## Input format

```
n m
u1 v1 c1
...
s
```

`m` directed edges `u -> v` of cost `c`. Print `dist[1..n]`, with `-1` for
unreachable.

## Example

```
5 8
1 2 5
1 5 2
5 2 2
5 3 7
2 3 1
2 4 1
3 4 2
4 5 10
1
```

```
0 4 5 5 2
```

Same graph as problem 1, same answers - now via the heap.

## Lazy deletion: the part worth understanding

Textbook Dijkstra calls `decrease-key` when it finds a better route to a vertex
already in the queue. Implementing that needs the heap to track where each vertex
lives, and to fix up those positions on every swap. It is a real amount of code.

The standard trick avoids it entirely. When you improve `dist[v]`, just **insert
another entry** for `v` with the new smaller key, and leave the old one alone. The
heap now holds two entries for `v`; the better one is closer to the top and comes
out first.

When the worse one eventually surfaces, you detect it and throw it away:

```c
if (it.key > dist[u]) continue;   /* stale - a better route was already settled */
```

That single line is what makes the whole approach correct. Without it you re-expand
vertices you already finished, and the running time degrades badly.

The heap can hold up to `E` entries rather than `V`, which is why the complexity is
`O(E log E)` - conventionally written `O(E log V)`, since `E < V^2` makes
`log E < 2 log V`.

## Which version should you actually use

`O(V^2)` wins on dense graphs, where `E` approaches `V^2` and the heap's bookkeeping
is pure overhead. The heap wins on sparse graphs, which is most real ones. Knowing
*why* you would pick either is a standard viva question, and now you have written
both.
