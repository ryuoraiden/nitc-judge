#include "problem.h"

int prim(int n, int w[MAXV][MAXV], int src, int parent[]) {
    int key[MAXV], done[MAXV];
    const int INF = 1000000000;

    for (int v = 0; v <= n; v++) { key[v] = INF; done[v] = 0; parent[v] = -1; }
    key[src] = 0;

    int total = 0;
    for (int step = 0; step < n; step++) {
        int u = -1;
        for (int v = 1; v <= n; v++)
            if (!done[v] && (u == -1 || key[v] < key[u])) u = v;

        if (u == -1 || key[u] == INF) return -1;   /* unreachable vertex left */
        done[u] = 1;
        total += key[u];

        for (int v = 1; v <= n; v++) {
            if (done[v] || w[u][v] == NOEDGE) continue;
            if (w[u][v] < key[v]) {                /* one edge, not a distance */
                key[v] = w[u][v];
                parent[v] = u;
            }
        }
    }
    return total;
}
