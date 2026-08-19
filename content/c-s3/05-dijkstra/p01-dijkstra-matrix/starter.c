#include "problem.h"

void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]) {
    int done[MAXV];

    /* TODO
       1. dist[i] = INF for all i, done[i] = 0, then dist[src] = 0
       2. repeat n times:
            a. pick the unfinished vertex u with the smallest dist
            b. if there is none, or dist[u] is still INF, stop - everything
               reachable has been settled
            c. mark u done
            d. relax every edge out of u: if dist[u] + w[u][v] beats dist[v],
               write the smaller value into dist[v]
       Skip w[u][v] == NOEDGE: 999 means there is no edge, not a cost of 999. */
}
