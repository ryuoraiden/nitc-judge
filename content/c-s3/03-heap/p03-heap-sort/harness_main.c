#include <stdio.h>
#include "problem.h"

#define MAXN 2000

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int a[MAXN];
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);

    heapSort(a, n);

    for (int k = 0; k < n; k++) printf("%d%s", a[k], k + 1 < n ? " " : "");
    printf("\n");
    return 0;
}
