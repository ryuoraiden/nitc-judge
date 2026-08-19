#include <stdio.h>
#include "problem.h"

static int w[MAXV][MAXV];

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &w[i][j]);

    int k;
    if (scanf("%d", &k) != 1) return 0;

    printf("%d\n", minTotalTime(n, w, k - 1));
    return 0;
}
