#include <stdlib.h>
#include "problem.h"

Node *newNode(int key) {
    Node *n = malloc(sizeof(Node));
    n->key = key;
    n->left = n->right = NULL;
    return n;
}

Node *insertKey(Node *root, int key) {
    if (root == NULL) return newNode(key);
    if (key < root->key) root->left = insertKey(root->left, key);
    else if (key > root->key) root->right = insertKey(root->right, key);
    return root;
}
