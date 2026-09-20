#include <stdlib.h>
#include "problem.h"

Node *insertKey(Node *root, int key) {
    /* TODO
       - empty tree: malloc a node, set key, left = right = NULL, return it
       - key < root->key : root->left  = insertKey(root->left, key)
       - key > root->key : root->right = insertKey(root->right, key)
       - equal: the tests never insert a duplicate; just return root
       Always return root at the end - that is what re-links the parent. */
    return root;
}

Node *searchKey(Node *root, int key) {
    /* TODO: NULL or a match ends it; otherwise go left or right. O(h), never both. */
    return NULL;
}
