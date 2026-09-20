#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define MAXE 10005

typedef struct { int u, v, w; } Edge;

/* ---- Provided: the DSU you just wrote. ---- */
typedef struct { int parent[MAXV]; int rank[MAXV]; } DSU;
void dsuInit(DSU *d, int n);
int  find(DSU *d, int x);
int  unite(DSU *d, int a, int b);

/* ---- Yours: total weight of a minimum spanning tree, or -1 if the graph
        cannot be connected.  edges[] may be reordered. ---- */
int kruskal(int n, Edge edges[], int m);

#endif
