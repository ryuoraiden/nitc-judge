#include <stdlib.h>
#include "problem.h"

BST init(int key) {
    BST n = malloc(sizeof(BSTNode));
    n->key = key;
    n->left = n->right = n->parent = NULL;
    return n;
}

BST insert(BST T, int k) {
    BST y = NULL, x = T;
    while (x != NULL) {                 /* walk down, remembering the parent */
        y = x;
        x = (k < x->key) ? x->left : x->right;
    }
    BST n = init(k);
    n->parent = y;
    if (y == NULL) return n;            /* tree was empty */
    if (k < y->key) y->left = n; else y->right = n;
    return T;
}

BST search(BST T, int k) {
    while (T != NULL && T->key != k) T = (k < T->key) ? T->left : T->right;
    return T;
}
