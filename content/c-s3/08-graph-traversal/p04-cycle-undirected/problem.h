#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define MAXE 20005

/* Vertices are 1..n.  adj[u][0..deg[u]-1] is kept in ascending order. */
typedef struct {
    int n;
    int deg[MAXV];
    int adj[MAXV][MAXV];
} Graph;

/* ---- Provided: the graph is built and its lists sorted before you are called. ---- */
void graphInit(Graph *g, int n);
void addEdge(Graph *g, int u, int v);
void sortNeighbours(Graph *g);

/* ---- Yours: 1 if the UNDIRECTED graph contains a cycle, else 0.
        The graph may be disconnected. ---- */
int hasCycle(const Graph *g);

#endif
