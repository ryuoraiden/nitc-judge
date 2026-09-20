#include <stdio.h>
#include "problem.h"

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    DSU d;
    dsuInit(&d, n);

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'u') {
            int a, b;
            if (scanf("%d %d", &a, &b) != 2) break;
            printf(unite(&d, a, b) ? "MERGED\n" : "ALREADY\n");
        } else if (cmd == 'f') {
            int a, b;
            if (scanf("%d %d", &a, &b) != 2) break;
            printf(find(&d, a) == find(&d, b) ? "SAME\n" : "DIFFERENT\n");
        } else if (cmd == 'c') {
            int count = 0;
            for (int v = 1; v <= n; v++) if (find(&d, v) == v) count++;
            printf("%d\n", count);
        }
    }
    return 0;
}
