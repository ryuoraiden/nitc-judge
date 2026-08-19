#include "problem.h"

int bfsOrder(const Graph *g, int s, int order[]) {
    int visited[MAXV] = {0};
    int queue[MAXV];
    int head = 0, tail = 0;
    int count = 0;

    visited[s] = 1;
    queue[tail++] = s;

    while (head < tail) {
        int u = queue[head++];
        order[count++] = u;

        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->adj[u][i];
            if (!visited[v]) {
                visited[v] = 1;      /* on enqueue, not on dequeue */
                queue[tail++] = v;
            }
        }
    }
    return count;
}
