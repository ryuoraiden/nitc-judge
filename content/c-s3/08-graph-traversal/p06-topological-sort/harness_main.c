#include <stdio.h>
#include "problem.h"

static void readGraph(Graph *g) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return;
    graphInit(g, n);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (scanf("%d %d", &u, &v) != 2) return;
        addEdge(g, u, v);
    }
    sortNeighbours(g);
}

int main(void) {
    Graph g;
    readGraph(&g);

    int order[MAXV];
    int k = topoSort(&g, order);
    if (k == 0) { printf("IMPOSSIBLE\n"); return 0; }
    for (int i = 0; i < k; i++) printf("%d%s", order[i], i + 1 < k ? " " : "");
    printf("\n");
    return 0;
}
