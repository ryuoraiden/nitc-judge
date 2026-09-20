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

/* ---- Yours: a topological order of the DIRECTED graph into order[].
        Among all valid orders, produce the lexicographically smallest one.
        Return 0 (and write nothing) if the graph has a cycle. ---- */
int topoSort(const Graph *g, int order[]);   /* returns n, or 0 if impossible */

#endif
