#include "problem.h"

void wgraphInit(WGraph *g, int n) {
    g->n = n;
    for (int i = 0; i <= n; i++) g->deg[i] = 0;
}

void wgraphAddEdge(WGraph *g, int u, int v, int c) {
    int d = g->deg[u]++;
    g->to[u][d] = v;
    g->cost[u][d] = c;
}
