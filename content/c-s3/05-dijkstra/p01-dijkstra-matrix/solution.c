#include "problem.h"

void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]) {
    int done[MAXV];
    for (int i = 0; i < n; i++) { dist[i] = INF; done[i] = 0; }
    dist[src] = 0;

    for (int iter = 0; iter < n; iter++) {
        int u = -1;
        for (int i = 0; i < n; i++)
            if (!done[i] && (u == -1 || dist[i] < dist[u])) u = i;

        if (u == -1 || dist[u] == INF) break;
        done[u] = 1;

        for (int v = 0; v < n; v++) {
            if (w[u][v] == NOEDGE || u == v) continue;
            if (dist[u] + w[u][v] < dist[v]) dist[v] = dist[u] + w[u][v];
        }
    }
}
