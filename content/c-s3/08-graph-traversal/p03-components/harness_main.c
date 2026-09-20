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

    int comp[MAXV];
    int k = components(&g, comp);
    printf("%d\n", k);
    for (int c = 1; c <= k; c++) {
        int first = 1;
        for (int v = 1; v <= g.n; v++)
            if (comp[v] == c) { printf(first ? "%d" : " %d", v); first = 0; }
        printf("\n");
    }
    return 0;
}
