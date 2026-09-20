#include "problem.h"

static void flood(const Graph *g, int u, int comp[], int label) {
    comp[u] = label;
    for (int i = 0; i < g->deg[u]; i++) {
        int v = g->adj[u][i];
        if (comp[v] == 0) flood(g, v, comp, label);
    }
}

int components(const Graph *g, int comp[]) {
    for (int v = 0; v <= g->n; v++) comp[v] = 0;

    int label = 0;
    for (int v = 1; v <= g->n; v++)
        if (comp[v] == 0) flood(g, v, comp, ++label);
    return label;
}
