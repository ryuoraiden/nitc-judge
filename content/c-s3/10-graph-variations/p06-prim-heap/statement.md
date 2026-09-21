# Prim with a priority queue

The theory syllabus asks for "implementation of Prim's and Dijkstra's algorithms using
priority queues". You wrote the heap Dijkstra in unit 05; this is its twin.

```c
int primHeap(const WGraph *g, int s);   /* MST cost, or -1 if disconnected */
```

The min-heap (`heapInsert`, `heapExtractMin` over `Item {key, id}`) is provided.

## Input format

```
n m s
u1 v1 w1
...
```

Undirected edges (added in both directions for you). Print the MST cost or `-1`.

## Example

```
5 7 1
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 10
4 5 7
```

```
15
```

## Side by side with heap Dijkstra

```c
/* Dijkstra */                              /* Prim */
Item it = heapExtractMin(&h);               Item it = heapExtractMin(&h);
if (it.key > dist[u]) continue;             if (inTree[u]) continue;
                                            inTree[u] = 1; total += it.key;
for each edge u -> v:                       for each edge u -> v:
  if (dist[u] + c < dist[v])                  if (!inTree[v])
    { dist[v] = dist[u] + c;                    heapInsert(&h, c, v);
      heapInsert(&h, dist[v], v); }
```

The key pushed is **the edge cost alone**. Push `total + c` or `dist[u] + c` out of habit
and you are computing shortest paths, and the "MST" comes out too expensive.

Complexity: `O(E log E)` - better than the `O(V^2)` array version on sparse graphs, worse
on dense ones, which is why the lab's `n <= 100` matrix questions happily use the array
version.
