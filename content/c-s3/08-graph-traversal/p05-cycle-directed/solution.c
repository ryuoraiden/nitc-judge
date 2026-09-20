#include "problem.h"

static int colour[MAXV];

static int dfs(const Graph *g, int u) {
    colour[u] = 1;                       /* on the current path */
    for (int i = 0; i < g->deg[u]; i++) {
        int v = g->adj[u][i];
        if (colour[v] == 1) return 1;    /* back edge to the current path */
        if (colour[v] == 0 && dfs(g, v)) return 1;
    }
    colour[u] = 2;                       /* finished */
    return 0;
}

int hasCycleDirected(const Graph *g) {
    for (int v = 0; v <= g->n; v++) colour[v] = 0;
    for (int v = 1; v <= g->n; v++)
        if (colour[v] == 0 && dfs(g, v)) return 1;
    return 0;
}
