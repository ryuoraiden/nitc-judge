#include <limits.h>
#include "problem.h"

static int check(Node *r, long long lo, long long hi) {
    if (r == NULL) return 1;
    if (r->key <= lo || r->key >= hi) return 0;
    return check(r->left, lo, r->key) && check(r->right, r->key, hi);
}

int isBST(Node *root) {
    return check(root, (long long)INT_MIN - 1, (long long)INT_MAX + 1);
}
