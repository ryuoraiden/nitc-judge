#include <stdio.h>
#include <stdlib.h>
#include "problem.h"

void graphInit(Graph *g, int n) {
    /* TODO: record n, and set every degree to zero.
       Vertices run 1..n, so do not forget index n itself. */
}

void addEdge(Graph *g, int u, int v) {
    /* TODO: append v to u's list and grow deg[u]. One line. */
}

static int cmpInt(const void *a, const void *b) {
    /* TODO: qsort comparator for ints - negative, zero or positive. */
    return 0;
}

void sortNeighbours(Graph *g) {
    /* TODO: qsort each vertex's list.
       qsort(g->adj[u], g->deg[u], sizeof(int), cmpInt); */
}

void printAdj(const Graph *g) {
    /* TODO: one line per vertex 1..n:
         "u:" followed by " v" for each neighbour, then a newline.
       A vertex with no out-edges prints just "u:". */
}
