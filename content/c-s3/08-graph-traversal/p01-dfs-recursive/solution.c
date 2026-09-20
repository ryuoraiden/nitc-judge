#include "problem.h"

static int visited[MAXV];

static void dfs(const Graph *g, int u, int order[], int *count) {
    visited[u] = 1;
    order[(*count)++] = u;
    for (int i = 0; i < g->deg[u]; i++) {
        int v = g->adj[u][i];
        if (!visited[v]) dfs(g, v, order, count);
    }
}

int dfsOrder(const Graph *g, int s, int order[]) {
    int count = 0;
    for (int v = 0; v <= g->n; v++) visited[v] = 0;
    dfs(g, s, order, &count);
    return count;
}
