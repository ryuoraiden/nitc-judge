#include "problem.h"

Node *buildFromPreIn(int pre[], int in[], int n) {
    if (n <= 0) return NULL;
    Node *root = newNode(pre[0]);
    int k = 0;
    while (in[k] != pre[0]) k++;          /* root's position in inorder */
    root->left = buildFromPreIn(pre + 1, in, k);
    root->right = buildFromPreIn(pre + 1 + k, in + k + 1, n - k - 1);
    return root;
}
