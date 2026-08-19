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
    int s;
    if (scanf("%d", &s) != 1) return 0;

    int parent[MAXV];
    for (int v = 0; v <= g.n; v++) parent[v] = -1;

    lexShortestPaths(&g, s, parent);

    for (int v = 1; v <= g.n; v++) {
        if (v != s && parent[v] == -1) { printf("-1\n"); continue; }
        int stack[MAXV], len = 0;
        for (int x = v; x != -1; x = parent[x]) stack[len++] = x;
        for (int i = len - 1; i >= 0; i--)
            printf("%d%s", stack[i], i > 0 ? "-" : "");
        printf("\n");
    }
    return 0;
}
