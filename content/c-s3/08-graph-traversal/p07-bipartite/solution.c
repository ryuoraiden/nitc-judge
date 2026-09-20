#include "problem.h"

int bipartite(const Graph *g, int colour[]) {
    int queue[MAXV];

    for (int v = 0; v <= g->n; v++) colour[v] = -1;

    for (int s = 1; s <= g->n; s++) {
        if (colour[s] != -1) continue;
        int head = 0, tail = 0;
        colour[s] = 0;                    /* smallest vertex of the component */
        queue[tail++] = s;

        while (head < tail) {
            int u = queue[head++];
            for (int i = 0; i < g->deg[u]; i++) {
                int v = g->adj[u][i];
                if (colour[v] == -1) {
                    colour[v] = 1 - colour[u];
                    queue[tail++] = v;
                } else if (colour[v] == colour[u]) {
                    return 0;             /* an edge inside one side */
                }
            }
        }
    }
    return 1;
}
