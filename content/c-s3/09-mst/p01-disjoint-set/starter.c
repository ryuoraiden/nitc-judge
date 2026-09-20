#include "problem.h"

void dsuInit(DSU *d, int n) {
    /* TODO: every vertex starts alone - its own parent, rank 0. */
}

int find(DSU *d, int x) {
    /* TODO: follow parent until you reach the representative (parent[x] == x).
       Path compression: on the way back, point x straight at the root.
       The one-liner is:
           if (d->parent[x] != x) d->parent[x] = find(d, d->parent[x]);
           return d->parent[x]; */
    return x;
}

int unite(DSU *d, int a, int b) {
    /* TODO: find both roots; if equal return 0.
       Otherwise attach the SHORTER tree under the taller one (union by rank),
       and if the ranks were equal, bump the new root's rank. Return 1. */
    return 0;
}
