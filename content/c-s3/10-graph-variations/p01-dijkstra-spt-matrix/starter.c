#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

int main(void) {
    /* TODO
       1. read n, the n x n distance matrix (999 = no road), and s (1-based)
       2. ordinary O(V^2) Dijkstra from s - but whenever you improve dist[v]
          through u, also record parent[v] = u
       3. output matrix: 0 on the diagonal, -1 everywhere else, then
          tree[parent[v]][v] = dist-matrix weight for every v with a parent
       4. print it, then the number of leaves: vertices other than s that are
          nobody's parent */
    return 0;
}
