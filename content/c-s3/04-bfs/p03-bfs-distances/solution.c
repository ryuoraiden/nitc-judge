#include "problem.h"

void bfsDistances(const Graph *g, int s, int dist[]) {
    for (int v = 0; v <= g->n; v++) dist[v] = -1;

    int queue[MAXV];
    int head = 0, tail = 0;

    dist[s] = 0;
    queue[tail++] = s;

    while (head < tail) {
        int u = queue[head++];
        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->adj[u][i];
            if (dist[v] == -1) {          /* -1 means undiscovered */
                dist[v] = dist[u] + 1;
                queue[tail++] = v;
            }
        }
    }
}
