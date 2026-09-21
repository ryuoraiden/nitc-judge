#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    static WGraph g;
    wgraphInit(&g, n);
    for (int i = 0; i < m; i++) {
        int u, v, c;
        if (scanf("%d %d %d", &u, &v, &c) != 3) return 0;
        wgraphAddEdge(&g, u, v, c);
    }
    int s, t;
    if (scanf("%d %d", &s, &t) != 2) return 0;

    int dist[MAXV];
    long long ways[MAXV];
    dijkstraCount(&g, s, dist, ways);

    if (dist[t] >= INF) printf("-1\n0\n");
    else printf("%d\n%lld\n", dist[t], ways[t]);
    return 0;
}
