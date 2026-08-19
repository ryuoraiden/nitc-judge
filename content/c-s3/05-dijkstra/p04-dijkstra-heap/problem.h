#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define MAXD 105
#define INF 1000000000

/* ---- Weighted adjacency list. Provided, already built. ---- */
typedef struct {
    int n;
    int deg[MAXV];
    int to[MAXV][MAXD];
    int cost[MAXV][MAXD];
} WGraph;

void wgraphInit(WGraph *g, int n);
void wgraphAddEdge(WGraph *g, int u, int v, int c);

/* ---- Min-heap priority queue. Provided - the one you built in unit 03. ---- */
typedef struct { int key; int id; } Item;
typedef struct { Item a[MAXV * MAXD]; int size; } MinHeap;

void heapInit(MinHeap *h);
int  heapEmpty(const MinHeap *h);
void heapInsert(MinHeap *h, int key, int id);
Item heapExtractMin(MinHeap *h);

/* ---- Yours. ---- */
void dijkstraHeap(const WGraph *g, int src, int dist[]);

#endif
