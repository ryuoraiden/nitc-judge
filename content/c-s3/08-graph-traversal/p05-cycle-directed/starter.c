#include "problem.h"

/* 0 = untouched, 1 = on the current path, 2 = finished */
static int colour[MAXV];

static int dfs(const Graph *g, int u) {
    /* TODO
       colour[u] = 1;
       for each neighbour v:
           if colour[v] == 1 -> v is on the path we are standing on: cycle
           if colour[v] == 0 and dfs(v) found a cycle -> report it
       colour[u] = 2 before returning 0. */
    return 0;
}

int hasCycleDirected(const Graph *g) {
    return 0;   /* TODO: clear colours, try every untouched vertex */
}
