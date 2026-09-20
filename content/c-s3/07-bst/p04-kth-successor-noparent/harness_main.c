#include <stdio.h>
#include "problem.h"

int main(void) {
    Node *root = NULL;
    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'i') {
            int v; if (scanf("%d", &v) != 1) break;
            root = insertKey(root, v);
        } else if (cmd == 'k') {
            int k; if (scanf("%d", &k) != 1) break;
            printf("%d\n", kthSmallest(root, k));
        } else if (cmd == 'm') {
            printf("%d\n", maximum(root));
        } else if (cmd == 'n') {
            int v; if (scanf("%d", &v) != 1) break;
            printf("%d\n", successorOf(root, v));
        }
    }
    return 0;
}
