#include "problem.h"

void wgraphInit(WGraph *g, int n) {
    g->n = n;
    for (int i = 0; i <= n; i++) g->deg[i] = 0;
}

void wgraphAddEdge(WGraph *g, int u, int v, int c) {
    int d = g->deg[u]++;
    g->to[u][d] = v;
    g->cost[u][d] = c;
}

static int before(Item x, Item y) {
    if (x.key != y.key) return x.key < y.key;
    return x.id < y.id;
}

static void swapItems(Item *x, Item *y) { Item t = *x; *x = *y; *y = t; }

void heapInit(MinHeap *h) { h->size = 0; }
int  heapEmpty(const MinHeap *h) { return h->size == 0; }

void heapInsert(MinHeap *h, int key, int id) {
    int i = h->size++;
    h->a[i].key = key;
    h->a[i].id = id;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (!before(h->a[i], h->a[p])) break;
        swapItems(&h->a[i], &h->a[p]);
        i = p;
    }
}

Item heapExtractMin(MinHeap *h) {
    Item root = h->a[0];
    h->a[0] = h->a[--(h->size)];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = 2 * i + 2, best = i;
        if (l < h->size && before(h->a[l], h->a[best])) best = l;
        if (r < h->size && before(h->a[r], h->a[best])) best = r;
        if (best == i) break;
        swapItems(&h->a[i], &h->a[best]);
        i = best;
    }
    return root;
}
