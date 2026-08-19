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
void addEdge(Graph *g, int u, int v);   /* directed edge u -> v */
void sortNeighbours(Graph *g);          /* each adjacency list ascending */
void printAdj(const Graph *g);

#endif
