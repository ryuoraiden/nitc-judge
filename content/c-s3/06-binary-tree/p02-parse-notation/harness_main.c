#include <stdio.h>
#include "problem.h"

static char line[200005];

static void pre(Node *r) { if (!r) return; printf("%d ", r->data); pre(r->left); pre(r->right); }
static void in(Node *r)  { if (!r) return; in(r->left); printf("%d ", r->data); in(r->right); }

int main(void) {
    if (fgets(line, sizeof line, stdin) == NULL) return 0;
    int i = 0;
    Node *root = buildTree(line, &i);
    if (root == NULL) { printf("EMPTY\n"); return 0; }
    /* preorder + inorder together pin down the exact shape you built */
    pre(root); printf("\n");
    in(root);  printf("\n");
    freeTree(root);
    return 0;
}
