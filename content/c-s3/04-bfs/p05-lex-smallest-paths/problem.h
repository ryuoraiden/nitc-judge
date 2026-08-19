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
void sortNeighbours(Graph *g);   /* already called: adjacency lists are ascending */

/* Yours: fill parent[] so that following it back from any reachable vertex v
   spells out the lexicographically smallest shortest path from s to v.
   parent[s] must be -1.  Leave parent[v] = -1 for unreachable v too. */
void lexShortestPaths(const Graph *g, int s, int parent[]);

#endif
