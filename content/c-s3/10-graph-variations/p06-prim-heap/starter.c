#include "problem.h"

int primHeap(const WGraph *g, int s) {
    static MinHeap h;
    int inTree[MAXV] = {0};
    heapInit(&h);

    /* TODO
       Push (0, s). Then, while the heap is not empty:
         pop the cheapest (key, u)
         if u is already in the tree, skip it (a stale, more expensive entry)
         otherwise put u in the tree, add key to the total, and push
         (edge cost, v) for every neighbour v not yet in the tree
       At the end, if fewer than n vertices joined, return -1. */
    return -1;
}
