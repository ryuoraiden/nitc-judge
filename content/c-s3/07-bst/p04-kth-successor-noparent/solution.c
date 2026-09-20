#include "problem.h"

static void walk(Node *r, int k, int *count, int *answer) {
    if (r == NULL || *answer != -1) return;
    walk(r->left, k, count, answer);
    if (*answer != -1) return;
    (*count)++;
    if (*count == k) { *answer = r->key; return; }
    walk(r->right, k, count, answer);
}

int kthSmallest(Node *root, int k) {
    int count = 0, answer = -1;
    if (k <= 0) return -1;
    walk(root, k, &count, &answer);
    return answer;
}

int maximum(Node *root) {
    if (root == NULL) return -1;
    while (root->right != NULL) root = root->right;
    return root->key;
}

int successorOf(Node *root, int key) {
    int best = -1;
    Node *cur = root;
    while (cur != NULL) {
        if (key < cur->key) { best = cur->key; cur = cur->left; }  /* candidate */
        else cur = cur->right;                                     /* too small */
    }
    return best;
}
