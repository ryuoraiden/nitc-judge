#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;

    Graph g;
    graphInit(&g, n);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (scanf("%d %d", &u, &v) != 2) return 0;
        addEdge(&g, u, v);
    }
    sortNeighbours(&g);
    printAdj(&g);
    return 0;
}
