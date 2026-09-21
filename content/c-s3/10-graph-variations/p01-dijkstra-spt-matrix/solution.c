#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

static int w[MAXV][MAXV], tree[MAXV][MAXV];
static int dist[MAXV], parent[MAXV], done_[MAXV];

int main(void) {
    int n, s;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) scanf("%d", &w[i][j]);
    if (scanf("%d", &s) != 1) return 0;

    for (int i = 1; i <= n; i++) {
        dist[i] = INF; parent[i] = -1; done_[i] = 0;
        for (int j = 1; j <= n; j++) tree[i][j] = (i == j) ? 0 : -1;
    }
    dist[s] = 0;

    for (int step = 0; step < n; step++) {
        int u = -1;
        for (int v = 1; v <= n; v++)
            if (!done_[v] && (u == -1 || dist[v] < dist[u])) u = v;
        if (u == -1 || dist[u] == INF) break;
        done_[u] = 1;

        for (int v = 1; v <= n; v++) {
            if (u == v || w[u][v] == NOEDGE) continue;
            if (dist[u] + w[u][v] < dist[v]) {
                dist[v] = dist[u] + w[u][v];
                parent[v] = u;              /* the one extra line vs plain Dijkstra */
            }
        }
    }

    /* Each reachable vertex except s contributes exactly one tree edge. */
    for (int v = 1; v <= n; v++)
        if (parent[v] != -1) tree[parent[v]][v] = w[parent[v]][v];

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) printf("%d ", tree[i][j]);
        printf("\n");
    }
    return 0;
}
