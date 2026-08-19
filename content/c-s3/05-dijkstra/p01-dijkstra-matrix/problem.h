#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define NOEDGE 999          /* the sheet's marker for "no direct road" */
#define INF 1000000000      /* unreachable */

/* dist[v] = cost of the cheapest src->v path, or INF if v is unreachable.
   Vertices are 0-based here, matching the matrix indices. */
void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]);

#endif
