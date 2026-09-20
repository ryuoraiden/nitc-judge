#include <stdio.h>

#define MAXV 105
#define INF 1000000000

static int w[MAXV][MAXV];
static int tree[MAXV][MAXV];
static int key[MAXV], parent[MAXV], done_[MAXV];

int main(void) {
    int n, m, s;
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;

    for (int i = 1; i <= n; i++) {
        key[i] = INF; parent[i] = -1; done_[i] = 0;
        for (int j = 1; j <= n; j++) tree[i][j] = (i == j) ? 0 : -1;
    }
    for (int i = 0; i < m; i++) {
        int u, v, x;
        if (scanf("%d %d %d", &u, &v, &x) != 3) return 0;
        w[u][v] = w[v][u] = x;
    }

    key[s] = 0;
    for (int step = 0; step < n; step++) {
        int u = -1;
        for (int v = 1; v <= n; v++)
            if (!done_[v] && (u == -1 || key[v] < key[u])) u = v;

        if (u == -1 || key[u] == INF) { printf("-1\n"); return 0; }
        done_[u] = 1;

        for (int v = 1; v <= n; v++) {
            if (done_[v] || w[u][v] == 0) continue;
            if (w[u][v] < key[v]) { key[v] = w[u][v]; parent[v] = u; }
        }
    }

    int cost = 0;
    for (int v = 1; v <= n; v++) {
        if (v == s) continue;
        int u = parent[v];
        if (u == -1) { printf("-1\n"); return 0; }
        tree[u][v] = tree[v][u] = w[u][v];
        cost += w[u][v];
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) printf("%d ", tree[i][j]);
        printf("\n");
    }
    printf("%d\n", cost);
    return 0;
}
