#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;

    WGraph g;
    wgraphInit(&g, n);
    for (int i = 0; i < m; i++) {
        int u, v, c;
        if (scanf("%d %d %d", &u, &v, &c) != 3) return 0;
        wgraphAddEdge(&g, u, v, c);
    }

    int s;
    if (scanf("%d", &s) != 1) return 0;

    int dist[MAXV];
    dijkstraHeap(&g, s, dist);

    for (int v = 1; v <= n; v++)
        printf("%d%s", dist[v] >= INF ? -1 : dist[v], v < n ? " " : "");
    printf("\n");
    return 0;
}
