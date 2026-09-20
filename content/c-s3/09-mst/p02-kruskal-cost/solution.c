#include <stdlib.h>
#include "problem.h"

static int cmpEdge(const void *a, const void *b) {
    const Edge *x = a, *y = b;
    return (x->w > y->w) - (x->w < y->w);
}

int kruskal(int n, Edge edges[], int m) {
    qsort(edges, m, sizeof(Edge), cmpEdge);

    DSU d;
    dsuInit(&d, n);

    int taken = 0, cost = 0;
    for (int i = 0; i < m && taken < n - 1; i++) {
        if (unite(&d, edges[i].u, edges[i].v)) {   /* no cycle created */
            cost += edges[i].w;
            taken++;
        }
    }
    return (taken == n - 1) ? cost : -1;
}
