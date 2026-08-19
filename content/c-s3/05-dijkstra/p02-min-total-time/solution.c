#include "problem.h"

int minTotalTime(int n, int w[MAXV][MAXV], int src) {
    int dist[MAXV];
    dijkstra(n, w, src, dist);

    int worst = 0;
    for (int v = 0; v < n; v++) {
        if (dist[v] >= INF) return -1;   /* somewhere never gets supplies */
        if (dist[v] > worst) worst = dist[v];
    }
    return worst;
}
