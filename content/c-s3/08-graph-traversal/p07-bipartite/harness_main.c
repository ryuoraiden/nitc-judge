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
        addEdge(g, v, u);
    }
    sortNeighbours(g);
}

int main(void) {
    Graph g;
    readGraph(&g);

    int colour[MAXV];
    if (!bipartite(&g, colour)) { printf("-1\n"); return 0; }
    for (int c = 0; c <= 1; c++) {
        int first = 1;
        for (int v = 1; v <= g.n; v++)
            if (colour[v] == c) { printf(first ? "%d" : " %d", v); first = 0; }
        printf("\n");
    }
    return 0;
}
