#include "problem.h"

void dijkstraCount(const WGraph *g, int s, int dist[], long long ways[]) {
    int done[MAXV];
    for (int v = 0; v <= g->n; v++) { dist[v] = INF; ways[v] = 0; done[v] = 0; }
    dist[s] = 0;
    ways[s] = 1;

    for (int step = 0; step < g->n; step++) {
        int u = -1;
        for (int v = 1; v <= g->n; v++)
            if (!done[v] && (u == -1 || dist[v] < dist[u])) u = v;
        if (u == -1 || dist[u] >= INF) break;
        done[u] = 1;                       /* ways[u] is final from here on */

        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->to[u][i];
            int nd = dist[u] + g->cost[u][i];
            if (nd < dist[v]) {
                dist[v] = nd;
                ways[v] = ways[u];         /* old routes were longer: forget them */
            } else if (nd == dist[v]) {
                ways[v] += ways[u];        /* a tie: add these routes too */
            }
        }
    }
}
