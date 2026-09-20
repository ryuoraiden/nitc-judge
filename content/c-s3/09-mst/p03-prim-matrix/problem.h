#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define NOEDGE 0        /* w[u][v] == 0 means there is no edge (weights are >= 1) */

/* ---- Yours: grow an MST outward from src.
        parent[v] = the vertex v was attached from, or -1 for src / unreachable.
        Return the total weight, or -1 if some vertex is unreachable. ---- */
int prim(int n, int w[MAXV][MAXV], int src, int parent[]);

#endif
