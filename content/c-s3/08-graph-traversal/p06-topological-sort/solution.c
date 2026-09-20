#include "problem.h"

int topoSort(const Graph *g, int order[]) {
    int indeg[MAXV] = {0}, used[MAXV] = {0}, count = 0;

    for (int u = 1; u <= g->n; u++)
        for (int i = 0; i < g->deg[u]; i++) indeg[g->adj[u][i]]++;

    for (int step = 0; step < g->n; step++) {
        int pick = -1;
        for (int v = 1; v <= g->n; v++)
            if (!used[v] && indeg[v] == 0) { pick = v; break; }   /* smallest first */

        if (pick == -1) return 0;                                  /* cycle */
        used[pick] = 1;
        order[count++] = pick;
        for (int i = 0; i < g->deg[pick]; i++) indeg[g->adj[pick][i]]--;
    }
    return count;
}
