#include "problem.h"

int bfsPath(const Graph *g, int s, int t, int path[]) {
    int parent[MAXV];
    int seen[MAXV];
    for (int v = 0; v <= g->n; v++) { parent[v] = -1; seen[v] = 0; }

    int queue[MAXV];
    int head = 0, tail = 0;
    seen[s] = 1;
    queue[tail++] = s;

    while (head < tail) {
        int u = queue[head++];
        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->adj[u][i];
            if (!seen[v]) {
                seen[v] = 1;
                parent[v] = u;
                queue[tail++] = v;
            }
        }
    }

    if (!seen[t]) return 0;

    /* Collect t -> s, which comes out reversed. */
    int stack[MAXV], len = 0;
    for (int x = t; x != -1; x = parent[x]) stack[len++] = x;

    for (int i = 0; i < len; i++) path[i] = stack[len - 1 - i];
    return len;
}
