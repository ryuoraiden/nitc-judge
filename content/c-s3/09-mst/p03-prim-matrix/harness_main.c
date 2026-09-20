#include <stdio.h>
#include "problem.h"

static int w[MAXV][MAXV];

int main(void) {
    int n, m, s;
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;
    for (int i = 0; i < m; i++) {
        int u, v, x;
        if (scanf("%d %d %d", &u, &v, &x) != 3) return 0;
        w[u][v] = w[v][u] = x;
    }

    int parent[MAXV];
    int cost = prim(n, w, s, parent);
    printf("%d\n", cost);
    if (cost >= 0)
        for (int v = 1; v <= n; v++) printf("%d%s", parent[v], v < n ? " " : "");
    printf("\n");
    return 0;
}
