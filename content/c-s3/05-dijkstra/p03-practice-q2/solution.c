#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

static int w[MAXV][MAXV];
static int dist[MAXV];
static int done[MAXV];

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &w[i][j]);

    int k;
    if (scanf("%d", &k) != 1) return 0;
    k--;                                  /* the sheet numbers locations from 1 */

    for (int i = 0; i < n; i++) { dist[i] = INF; done[i] = 0; }
    dist[k] = 0;

    for (int iter = 0; iter < n; iter++) {
        int u = -1;
        for (int i = 0; i < n; i++)
            if (!done[i] && (u == -1 || dist[i] < dist[u])) u = i;
        if (u == -1 || dist[u] == INF) break;
        done[u] = 1;

        for (int v = 0; v < n; v++) {
            if (u == v || w[u][v] == NOEDGE) continue;
            if (dist[u] + w[u][v] < dist[v]) dist[v] = dist[u] + w[u][v];
        }
    }

    int worst = 0;
    for (int v = 0; v < n; v++) {
        if (dist[v] >= INF) { printf("-1\n"); return 0; }
        if (dist[v] > worst) worst = dist[v];
    }
    printf("%d\n", worst);
    return 0;
}
