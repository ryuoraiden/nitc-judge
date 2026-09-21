#include <stdio.h>

#define MAXV 105
#define MAXE 10005
#define INF 1000000000

static int eu[MAXE], ev[MAXE], ew[MAXE];
static long long dist[MAXV];

int main(void) {
    int n, m, s;
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;
    for (int i = 0; i < m; i++)
        if (scanf("%d %d %d", &eu[i], &ev[i], &ew[i]) != 3) return 0;

    for (int v = 1; v <= n; v++) dist[v] = INF;
    dist[s] = 0;

    /* n-1 rounds: every simple path has at most n-1 edges. */
    for (int round = 1; round <= n - 1; round++) {
        int changed = 0;
        for (int i = 0; i < m; i++) {
            if (dist[eu[i]] == INF) continue;          /* never relax from "infinity" */
            if (dist[eu[i]] + ew[i] < dist[ev[i]]) {
                dist[ev[i]] = dist[eu[i]] + ew[i];
                changed = 1;
            }
        }
        if (!changed) break;
    }

    /* One more round: anything that still improves sits on a reachable negative cycle. */
    for (int i = 0; i < m; i++) {
        if (dist[eu[i]] == INF) continue;
        if (dist[eu[i]] + ew[i] < dist[ev[i]]) { printf("NEGATIVE CYCLE\n"); return 0; }
    }

    for (int v = 1; v <= n; v++) {
        if (dist[v] == INF) printf("INF");
        else printf("%lld", dist[v]);
        printf(v < n ? " " : "\n");
    }
    return 0;
}
