#include "problem.h"

void dijkstraHeap(const WGraph *g, int src, int dist[]) {
    MinHeap h;
    heapInit(&h);

    for (int v = 0; v <= g->n; v++) dist[v] = INF;
    dist[src] = 0;
    heapInsert(&h, 0, src);

    while (!heapEmpty(&h)) {
        Item it = heapExtractMin(&h);
        int u = it.id;

        /* A better route to u was found after this entry was queued. */
        if (it.key > dist[u]) continue;

        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->to[u][i];
            int nd = dist[u] + g->cost[u][i];
            if (nd < dist[v]) {
                dist[v] = nd;
                heapInsert(&h, nd, v);
            }
        }
    }
}
