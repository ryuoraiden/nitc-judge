#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

static long long d[MAXV][MAXV];

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) {
            int x;
            scanf("%d", &x);
            d[i][j] = (i == j) ? 0 : (x == NOEDGE ? INF : x);
        }

    /* k is the OUTER loop: "shortest paths using only 1..k as intermediates". */
    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++) {
                if (d[i][k] == INF || d[k][j] == INF) continue;
                if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
            }

    for (int i = 1; i <= n; i++)
        if (d[i][i] < 0) { printf("NEGATIVE CYCLE\n"); return 0; }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (d[i][j] == INF) printf("INF");
            else printf("%lld", d[i][j]);
            printf(j < n ? " " : "\n");
        }
    }
    return 0;
}
