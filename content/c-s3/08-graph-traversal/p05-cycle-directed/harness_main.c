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
    printf("%d\n", hasCycleDirected(&g));
    return 0;
}
