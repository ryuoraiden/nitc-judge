#include <stdlib.h>
#include "problem.h"

Node *newNode(int value) {
    Node *n = malloc(sizeof(Node));
    n->data = value;
    n->left = n->right = NULL;
    return n;
}

void freeTree(Node *root) {
    if (root == NULL) return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}
