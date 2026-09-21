#include "problem.h"

/* Height in nodes, or -1 if any subtree below is unbalanced. */
static int checkedHeight(Node *r) {
    if (r == NULL) return 0;
    int l = checkedHeight(r->left);
    if (l < 0) return -1;
    int h = checkedHeight(r->right);
    if (h < 0) return -1;
    if (l - h > 1 || h - l > 1) return -1;
    return 1 + (l > h ? l : h);
}

int isBalanced(Node *root) {
    return checkedHeight(root) >= 0;
}

/* Height in nodes; updates *best with the widest bend seen, in edges. */
static int heightAndDiameter(Node *r, int *best) {
    if (r == NULL) return 0;
    int l = heightAndDiameter(r->left, best);
    int h = heightAndDiameter(r->right, best);
    if (l + h > *best) *best = l + h;        /* path bending at r, measured in edges */
    return 1 + (l > h ? l : h);
}

int diameter(Node *root) {
    int best = 0;
    heightAndDiameter(root, &best);
    return best;
}

void mirror(Node *root) {
    if (root == NULL) return;
    Node *t = root->left;
    root->left = root->right;
    root->right = t;
    mirror(root->left);
    mirror(root->right);
}
