#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

int main(void) {
    /* TODO
       1. read n, the n x n matrix (999 = no edge), and s (1-based)
       2. ordinary O(V^2) Dijkstra from s - BUT whenever you improve dist[v]
          through u, also record parent[v] = u
       3. build the output matrix: 0 on the diagonal, -1 everywhere else,
          then tree[parent[v]][v] = w[parent[v]][v] for every v that has a parent
       4. print it */
    return 0;
}
