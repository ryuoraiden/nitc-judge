#include "problem.h"

void dijkstraHeap(const WGraph *g, int src, int dist[]) {
    MinHeap h;
    heapInit(&h);

    /* TODO
       1. dist[v] = INF for v in 0..n, then dist[src] = 0
       2. insert (0, src) into the heap
       3. while the heap is not empty:
            - extract the smallest item (key, u)
            - if key > dist[u], this entry is STALE - skip it and continue
            - otherwise relax every edge u->v: if dist[u] + cost < dist[v],
              update dist[v] and insert (dist[v], v)
       There is no decrease-key here. You insert a second, better entry and
       let the stale one be skipped when it surfaces. See the statement. */
}
