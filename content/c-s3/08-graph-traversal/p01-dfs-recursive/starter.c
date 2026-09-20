#include "problem.h"

static int visited[MAXV];

static void dfs(const Graph *g, int u, int order[], int *count) {
    /* TODO
       - mark u visited, append it to order[] (use (*count)++)
       - for each neighbour v of u in ascending order:
             if v is not visited, recurse into it */
}

int dfsOrder(const Graph *g, int s, int order[]) {
    int count = 0;
    for (int v = 0; v <= g->n; v++) visited[v] = 0;
    dfs(g, s, order, &count);
    return count;
}
