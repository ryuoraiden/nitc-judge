#include <stdio.h>
#include "problem.h"

int main(void) {
    BST T = NULL;
    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'i') {
            int v; if (scanf("%d", &v) != 1) break;
            T = insert(T, v);
        } else if (cmd == 'm') {
            BST r = minimum(T);
            printf(r ? "%d\n" : "-1\n", r ? r->key : 0);
        } else if (cmd == 'x') {
            BST r = maximum(T);
            printf(r ? "%d\n" : "-1\n", r ? r->key : 0);
        } else if (cmd == 'n' || cmd == 'r') {
            int v; if (scanf("%d", &v) != 1) break;
            BST x = search(T, v);
            BST r = (x == NULL) ? NULL : (cmd == 'n' ? successor(T, x) : predecessor(T, x));
            printf(r ? "%d\n" : "-1\n", r ? r->key : 0);
        }
    }
    return 0;
}
