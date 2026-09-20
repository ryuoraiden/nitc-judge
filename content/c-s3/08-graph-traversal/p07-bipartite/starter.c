#include "problem.h"

int bipartite(const Graph *g, int colour[]) {
    /* TODO
       - colour[v] = -1 for "uncoloured"
       - for every still-uncoloured vertex (the graph may be disconnected):
           give it colour 0 and BFS/DFS from it
           every neighbour must get the OPPOSITE colour
           if a neighbour already has the SAME colour as the current vertex -> not
           bipartite, return 0
       - return 1 if you get through the whole graph */
    return 0;
}
