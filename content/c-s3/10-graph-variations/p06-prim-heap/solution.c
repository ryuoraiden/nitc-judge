#include "problem.h"

int primHeap(const WGraph *g, int s) {
    static MinHeap h;
    int inTree[MAXV] = {0};
    int joined = 0, total = 0;
    heapInit(&h);

    heapInsert(&h, 0, s);
    while (!heapEmpty(&h)) {
        Item it = heapExtractMin(&h);
        int u = it.id;
        if (inTree[u]) continue;           /* lazy deletion: already attached cheaper */

        inTree[u] = 1;
        total += it.key;
        joined++;

        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->to[u][i];
            if (!inTree[v]) heapInsert(&h, g->cost[u][i], v);   /* key = ONE edge */
        }
    }
    return (joined == g->n) ? total : -1;
}
