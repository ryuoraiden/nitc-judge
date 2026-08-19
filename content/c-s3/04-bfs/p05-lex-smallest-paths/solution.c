#include "problem.h"

void lexShortestPaths(const Graph *g, int s, int parent[]) {
    int seen[MAXV];
    for (int v = 0; v <= g->n; v++) seen[v] = 0;

    int queue[MAXV];
    int head = 0, tail = 0;

    seen[s] = 1;
    parent[s] = -1;
    queue[tail++] = s;

    while (head < tail) {
        int u = queue[head++];
        /* g->adj[u] is ascending, so neighbours are offered smallest-first. */
        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->adj[u][i];
            if (!seen[v]) {
                seen[v] = 1;
                parent[v] = u;   /* first discovery wins, and it is the best one */
                queue[tail++] = v;
            }
        }
    }
}
