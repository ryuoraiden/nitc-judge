#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    static Edge edges[MAXE];
    for (int i = 0; i < m; i++)
        if (scanf("%d %d %d", &edges[i].u, &edges[i].v, &edges[i].w) != 3) return 0;

    printf("%d\n", kruskal(n, edges, m));
    return 0;
}
