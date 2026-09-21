#include <stdio.h>
#include "problem.h"

static char line[200005];

static Node *readTree(void) {
    if (fgets(line, sizeof line, stdin) == NULL) return NULL;
    int i = 0;
    return buildTree(line, &i);
}

static void pre(Node *r) { if (!r) return; printf("%d ", r->key); pre(r->left); pre(r->right); }

int main(void) {
    Node *root = readTree();
    printf("%d\n", isBalanced(root));
    printf("%d\n", diameter(root));
    mirror(root);
    pre(root);
    printf("\n");
    freeTree(root);
    return 0;
}
