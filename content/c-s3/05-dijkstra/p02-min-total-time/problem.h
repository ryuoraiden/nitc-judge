#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define NOEDGE 999          /* the sheet's marker for "no direct road" */
#define INF 1000000000      /* unreachable */

/* Provided for you - the function you just wrote. */
void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]);

/* Yours: the time until the LAST location has received supplies,
   or -1 if any location cannot be reached at all. */
int minTotalTime(int n, int w[MAXV][MAXV], int src);

#endif
