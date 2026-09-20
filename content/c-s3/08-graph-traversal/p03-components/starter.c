#include "problem.h"

int components(const Graph *g, int comp[]) {
    /* TODO
       - comp[v] = 0 means "not assigned yet"
       - for v from 1 to n: if comp[v] is still 0, start a new component number
         and flood-fill from v (DFS or BFS - either is fine) marking every vertex
         you reach with that number
       - return how many components you started
       Scanning v in ascending order is what numbers the components by their
       smallest vertex. */
    return 0;
}
