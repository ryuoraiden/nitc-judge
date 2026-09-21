#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

int main(void) {
    /* TODO
       d[i][j] = the matrix, with 999 turned into INF (and 0 on the diagonal).
       for k: for i: for j:   (k OUTERMOST - see the statement)
           if both halves are finite and d[i][k] + d[k][j] < d[i][j], take it
       If any d[i][i] ends up negative -> NEGATIVE CYCLE.
       Otherwise print the matrix, INF where unreachable. */
    return 0;
}
