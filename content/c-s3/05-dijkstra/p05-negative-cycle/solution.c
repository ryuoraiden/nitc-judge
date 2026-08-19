#include <stdio.h>

#define MAXV 105
#define NOEDGE 999

static int w[MAXV][MAXV];
static long long dist[MAXV];

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &w[i][j]);

    /* Every vertex starts at 0, which is equivalent to adding a virtual source
       with a zero-cost edge to each one. That way a negative cycle anywhere in
       the graph is detected, not only ones reachable from a chosen start. */
    for (int i = 0; i < n; i++) dist[i] = 0;

    for (int pass = 0; pass < n - 1; pass++) {
        int changed = 0;
        for (int u = 0; u < n; u++)
            for (int v = 0; v < n; v++) {
                if (u == v || w[u][v] == NOEDGE) continue;
                if (dist[u] + w[u][v] < dist[v]) {
                    dist[v] = dist[u] + w[u][v];
                    changed = 1;
                }
            }
        if (!changed) break;   /* settled early: no negative cycle */
    }

    /* One extra pass: any further improvement proves a negative cycle. */
    for (int u = 0; u < n; u++)
        for (int v = 0; v < n; v++) {
            if (u == v || w[u][v] == NOEDGE) continue;
            if (dist[u] + w[u][v] < dist[v]) {
                printf("1\n");
                return 0;
            }
        }

    printf("-1\n");
    return 0;
}
