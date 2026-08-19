#include <stdio.h>
#include "problem.h"

#define MAXN 1000

int main(void) {
    int n, i;
    if (scanf("%d", &n) != 1) return 0;
    int a[MAXN];
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    if (scanf("%d", &i) != 1) return 0;

    maxHeapify(a, n, i);

    for (int k = 0; k < n; k++) printf("%d%s", a[k], k + 1 < n ? " " : "");
    printf("\n");
    return 0;
}
