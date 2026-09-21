#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m, s;
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;
    static WGraph g;
    wgraphInit(&g, n);
    for (int i = 0; i < m; i++) {
        int u, v, c;
        if (scanf("%d %d %d", &u, &v, &c) != 3) return 0;
        wgraphAddEdge(&g, u, v, c);
        wgraphAddEdge(&g, v, u, c);
    }
    printf("%d\n", primHeap(&g, s));
    return 0;
}
