#include "problem.h"

static int visited[MAXV];

static int dfs(const Graph *g, int u, int parent) {
    /* TODO
       mark u; for each neighbour v:
         - if v is not visited, recurse with parent = u; if that finds a cycle, report it
         - else if v != parent, you have reached an already-visited vertex by a
           different route -> cycle
       Skipping the parent is what stops the edge you just came along from
       counting as a cycle. */
    return 0;
}

int hasCycle(const Graph *g) {
    /* TODO: clear visited, then try every unvisited vertex (the graph may be
       disconnected) and report 1 if any DFS finds a cycle. */
    return 0;
}
