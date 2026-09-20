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

/* ---- Yours: label every vertex with its component number.
        Components are numbered 1, 2, 3, ... in order of their smallest vertex. ---- */
int components(const Graph *g, int comp[]);   /* returns how many components */

#endif
