#include <stdlib.h>
#include "problem.h"

/* Replace the subtree rooted at u with the subtree rooted at v.
   Returns the new root of the whole tree. */
BST transplant(BST T, BST u, BST v) {
    /* TODO
       - if u is the root (u->parent == NULL), v becomes the new root
       - else if u is its parent's left child, set that left pointer to v
       - else set the right pointer to v
       - if v is not NULL, fix v->parent
       Return the root: T normally, v when u was the root. */
    return T;
}

BST delete(BST T, BST x) {
    /* TODO - three cases:
       1. no left child  -> transplant x with x->right
       2. no right child -> transplant x with x->left
       3. two children   -> y = minimum(x->right)   (x's successor)
            if y is not x's direct child:
                transplant y with y->right
                y->right = x->right; y->right->parent = y;
            transplant x with y
            y->left = x->left; y->left->parent = y;
       free(x) at the end. */
    return T;
}
