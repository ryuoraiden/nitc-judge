#include "problem.h"

BST minimum(BST T) {
    if (T == NULL) return NULL;
    while (T->left != NULL) T = T->left;
    return T;
}

BST maximum(BST T) {
    if (T == NULL) return NULL;
    while (T->right != NULL) T = T->right;
    return T;
}

BST successor(BST T, BST x) {
    (void)T;
    if (x == NULL) return NULL;
    if (x->right != NULL) return minimum(x->right);

    BST y = x->parent;
    while (y != NULL && x == y->right) { x = y; y = y->parent; }
    return y;
}

BST predecessor(BST T, BST x) {
    (void)T;
    if (x == NULL) return NULL;
    if (x->left != NULL) return maximum(x->left);

    BST y = x->parent;
    while (y != NULL && x == y->left) { x = y; y = y->parent; }
    return y;
}
