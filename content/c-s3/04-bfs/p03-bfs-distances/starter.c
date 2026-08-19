#include "problem.h"

void bfsDistances(const Graph *g, int s, int dist[]) {
    /* TODO
       1. set every dist[v] to -1 (meaning "not reached yet")
       2. dist[s] = 0, enqueue s
       3. when you discover an unvisited neighbour v of u:
              dist[v] = dist[u] + 1
          and enqueue it
       dist[v] != -1 doubles as your visited flag - no separate array needed. */
}
