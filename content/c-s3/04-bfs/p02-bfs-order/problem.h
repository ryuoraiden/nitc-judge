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

/* Provided for you. */
void graphInit(Graph *g, int n);
void addEdge(Graph *g, int u, int v);
void sortNeighbours(Graph *g);

/* Yours: write the BFS visit order starting at s into order[],
   and return how many vertices were visited. */
int bfsOrder(const Graph *g, int s, int order[]);

#endif
