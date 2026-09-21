#include <stdio.h>

#define MAXV 105
#define MAXE 10005
#define INF 1000000000

int main(void) {
    /* TODO
       Store the edges as three arrays (or a struct): from, to, weight.
       dist[s] = 0, everything else INF.
       Repeat n-1 times: for every edge u->v, if dist[u] != INF and
       dist[u] + w < dist[v], lower dist[v].
       Then one extra pass: if any edge can STILL be relaxed, print
       NEGATIVE CYCLE. Otherwise print the distances, INF for unreachable. */
    return 0;
}
