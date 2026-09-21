#include "problem.h"

void dijkstraCount(const WGraph *g, int s, int dist[], long long ways[]) {
    int done[MAXV];
    /* TODO: O(V^2) Dijkstra, with one extra array.
       ways[s] = 1, everything else 0.
       When relaxing u -> v with new distance nd:
         nd <  dist[v]  -> strictly better: dist[v] = nd, ways[v] = ways[u]
         nd == dist[v]  -> another equally short route: ways[v] += ways[u]
       Only do this from a u that has just been finalised. */
    (void)done;
}
