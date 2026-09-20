#include <stdlib.h>
#include "problem.h"

Node *insertKey(Node *root, int key) {
    if (root == NULL) {
        Node *n = malloc(sizeof(Node));
        n->key = key;
        n->left = n->right = NULL;
        return n;
    }
    if (key < root->key) root->left = insertKey(root->left, key);
    else if (key > root->key) root->right = insertKey(root->right, key);
    return root;
}

Node *searchKey(Node *root, int key) {
    if (root == NULL || root->key == key) return root;
    return key < root->key ? searchKey(root->left, key) : searchKey(root->right, key);
}
