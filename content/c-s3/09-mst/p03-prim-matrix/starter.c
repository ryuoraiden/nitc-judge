#include "problem.h"

int prim(int n, int w[MAXV][MAXV], int src, int parent[]) {
    int key[MAXV], done[MAXV];
    const int INF = 1000000000;

    /* TODO
       1. key[v] = INF, done[v] = 0, parent[v] = -1 for all v; key[src] = 0
       2. repeat n times:
            pick the unfinished vertex u with the smallest key
            if none is reachable (key is still INF) -> return -1
            mark u done, add key[u] to the total
            for every neighbour v with an edge: if !done[v] and w[u][v] < key[v],
                key[v] = w[u][v]; parent[v] = u;
       3. return the total
       Note the difference from Dijkstra: key[v] is the weight of ONE edge, not
       the distance from the source. */
    return -1;
}
