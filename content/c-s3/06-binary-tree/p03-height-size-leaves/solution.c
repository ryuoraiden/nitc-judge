#include "problem.h"

int height(Node *root) {
    if (root == NULL) return 0;
    int l = height(root->left), r = height(root->right);
    return 1 + (l > r ? l : r);
}

int countNodes(Node *root) {
    if (root == NULL) return 0;
    return 1 + countNodes(root->left) + countNodes(root->right);
}

int countLeaves(Node *root) {
    if (root == NULL) return 0;
    if (root->left == NULL && root->right == NULL) return 1;
    return countLeaves(root->left) + countLeaves(root->right);
}
