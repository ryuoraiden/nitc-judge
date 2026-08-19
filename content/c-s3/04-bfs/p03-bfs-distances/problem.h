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

/* Yours: dist[v] = number of edges on a shortest s->v path, or -1 if
   v cannot be reached.  dist[s] is 0. */
void bfsDistances(const Graph *g, int s, int dist[]);

#endif
