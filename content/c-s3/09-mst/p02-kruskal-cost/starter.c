#include <stdlib.h>
#include "problem.h"

static int cmpEdge(const void *a, const void *b) {
    /* TODO: order by weight, ascending. Return negative / zero / positive -
       NOT a true/false comparison like C++ needs. */
    return 0;
}

int kruskal(int n, Edge edges[], int m) {
    /* TODO
       1. qsort the edges by weight
       2. dsuInit
       3. for each edge in order: if unite(u, v) succeeds it does not close a
          cycle - add its weight and count it
       4. a spanning tree needs exactly n-1 edges; if you took fewer, the graph
          was disconnected -> return -1 */
    return -1;
}
