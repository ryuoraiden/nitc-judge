#include <stdio.h>
#include <stdlib.h>
#include "problem.h"

void graphInit(Graph *g, int n) {
    g->n = n;
    for (int i = 0; i <= n; i++) g->deg[i] = 0;
}

void addEdge(Graph *g, int u, int v) {
    g->adj[u][g->deg[u]++] = v;
}

static int cmpInt(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);   /* no overflow, unlike x - y */
}

void sortNeighbours(Graph *g) {
    for (int u = 1; u <= g->n; u++)
        qsort(g->adj[u], g->deg[u], sizeof(int), cmpInt);
}

void printAdj(const Graph *g) {
    for (int u = 1; u <= g->n; u++) {
        printf("%d:", u);
        for (int i = 0; i < g->deg[u]; i++) printf(" %d", g->adj[u][i]);
        printf("\n");
    }
}
