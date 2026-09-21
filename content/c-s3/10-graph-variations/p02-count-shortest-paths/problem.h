#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define MAXD 105
#define INF 1000000000

/* Weighted adjacency list over 1..n.  Provided and already built. */
typedef struct {
    int n;
    int deg[MAXV];
    int to[MAXV][MAXD];
    int cost[MAXV][MAXD];
} WGraph;

void wgraphInit(WGraph *g, int n);
void wgraphAddEdge(WGraph *g, int u, int v, int c);

/* ---- Yours: Dijkstra from s that also counts shortest paths.
        dist[v] = shortest distance (INF if unreachable)
        ways[v] = how many different shortest paths reach v (0 if unreachable).
        All edge weights are >= 1. ---- */
void dijkstraCount(const WGraph *g, int s, int dist[], long long ways[]);

#endif
