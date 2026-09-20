#include "problem.h"

int dfsIterative(const Graph *g, int s, int order[]) {
    int visited[MAXV] = {0};
    int stack[MAXE];
    int top = -1, count = 0;

    stack[++top] = s;
    while (top >= 0) {
        int u = stack[top--];
        if (visited[u]) continue;      /* a duplicate push from another neighbour */
        visited[u] = 1;
        order[count++] = u;

        /* push descending so the smallest neighbour is popped first */
        for (int i = g->deg[u] - 1; i >= 0; i--) {
            int v = g->adj[u][i];
            if (!visited[v]) stack[++top] = v;
        }
    }
    return count;
}
