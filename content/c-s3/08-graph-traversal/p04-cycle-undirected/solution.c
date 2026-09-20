#include "problem.h"

static int visited[MAXV];

static int dfs(const Graph *g, int u, int parent) {
    visited[u] = 1;
    for (int i = 0; i < g->deg[u]; i++) {
        int v = g->adj[u][i];
        if (!visited[v]) {
            if (dfs(g, v, u)) return 1;
        } else if (v != parent) {
            return 1;               /* reached a visited vertex another way */
        }
    }
    return 0;
}

int hasCycle(const Graph *g) {
    for (int v = 0; v <= g->n; v++) visited[v] = 0;
    for (int v = 1; v <= g->n; v++)
        if (!visited[v] && dfs(g, v, -1)) return 1;
    return 0;
}
