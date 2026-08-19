#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105

/* Vertices are numbered 1..n.  adj[u][0..deg[u]-1] holds u's out-neighbours,
   kept in ascending order by sortNeighbours(). */
typedef struct {
    int n;
    int deg[MAXV];
    int adj[MAXV][MAXV];
} Graph;

void graphInit(Graph *g, int n);
void addEdge(Graph *g, int u, int v);
void sortNeighbours(Graph *g);

/* Yours: write a shortest s->t path into path[] (from s to t, in that order)
   and return its length in vertices.  Return 0 if t is unreachable.
   If s == t the path is just s, length 1. */
int bfsPath(const Graph *g, int s, int t, int path[]);

#endif
