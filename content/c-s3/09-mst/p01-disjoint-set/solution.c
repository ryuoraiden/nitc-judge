#include "problem.h"

void dsuInit(DSU *d, int n) {
    for (int v = 0; v <= n; v++) {
        d->parent[v] = v;
        d->rank[v] = 0;
    }
}

int find(DSU *d, int x) {
    if (d->parent[x] != x) d->parent[x] = find(d, d->parent[x]);   /* compress */
    return d->parent[x];
}

int unite(DSU *d, int a, int b) {
    int ra = find(d, a), rb = find(d, b);
    if (ra == rb) return 0;

    if (d->rank[ra] < d->rank[rb]) {
        d->parent[ra] = rb;
    } else if (d->rank[rb] < d->rank[ra]) {
        d->parent[rb] = ra;
    } else {
        d->parent[rb] = ra;
        d->rank[ra]++;
    }
    return 1;
}
