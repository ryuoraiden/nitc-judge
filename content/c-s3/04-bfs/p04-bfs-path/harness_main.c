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
    int s, t;
    if (scanf("%d %d", &s, &t) != 2) return 0;

    int path[MAXV];
    int len = bfsPath(&g, s, t, path);

    if (len == 0) {
        printf("NO PATH\n");
    } else {
        for (int i = 0; i < len; i++) printf("%d%s", path[i], i + 1 < len ? "-" : "");
        printf("\n");
    }
    return 0;
}
