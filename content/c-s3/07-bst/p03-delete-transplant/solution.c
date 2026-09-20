#include <stdlib.h>
#include "problem.h"

BST transplant(BST T, BST u, BST v) {
    if (u->parent == NULL) T = v;                    /* u was the root */
    else if (u == u->parent->left) u->parent->left = v;
    else u->parent->right = v;
    if (v != NULL) v->parent = u->parent;
    return T;
}

BST delete(BST T, BST x) {
    if (x->left == NULL) {
        T = transplant(T, x, x->right);
    } else if (x->right == NULL) {
        T = transplant(T, x, x->left);
    } else {
        BST y = minimum(x->right);                   /* x's successor */
        if (y->parent != x) {
            T = transplant(T, y, y->right);          /* detach y, keep its right child */
            y->right = x->right;
            y->right->parent = y;
        }
        T = transplant(T, x, y);
        y->left = x->left;
        y->left->parent = y;
    }
    free(x);
    return T;
}
