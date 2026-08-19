#include "problem.h"

int minTotalTime(int n, int w[MAXV][MAXV], int src) {
    int dist[MAXV];
    dijkstra(n, w, src, dist);

    /* TODO: the teams travel concurrently, so the answer is not the sum of the
       distances. Work out which single number over dist[0..n-1] it actually is,
       and return -1 if any vertex is unreachable. */
    return 0;
}
