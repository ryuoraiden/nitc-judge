#include <stdio.h>
#include "problem.h"

int main(void) {
    Node *root = NULL;
    char c;
    while (scanf(" %c", &c) == 1) {
        if (c == 'e') break;
        int a, b;
        if (c == 'i') { if (scanf("%d", &a) != 1) break; root = insertKey(root, a); }
        else if (c == 'l') { if (scanf("%d %d", &a, &b) != 2) break; printf("%d\n", lcaBST(root, a, b)); }
        else if (c == 'f') { if (scanf("%d", &a) != 1) break; printf("%d\n", floorKey(root, a)); }
        else if (c == 'c') { if (scanf("%d", &a) != 1) break; printf("%d\n", ceilKey(root, a)); }
        else if (c == 'r') { if (scanf("%d %d", &a, &b) != 2) break; printRange(root, a, b); printf("\n"); }
    }
    return 0;
}
