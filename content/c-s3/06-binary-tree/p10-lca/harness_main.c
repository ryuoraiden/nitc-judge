#include <stdio.h>
#include "problem.h"

static char line[200005];

static Node *readTree(void) {
    if (fgets(line, sizeof line, stdin) == NULL) return NULL;
    int i = 0;
    return buildTree(line, &i);
}

int main(void) {
    Node *root = readTree();
    int q;
    if (scanf("%d", &q) != 1) return 0;
    while (q--) {
        int a, b;
        if (scanf("%d %d", &a, &b) != 2) break;
        Node *r = lca(root, a, b);
        printf("%d\n", r ? r->data : -1);
    }
    freeTree(root);
    return 0;
}
