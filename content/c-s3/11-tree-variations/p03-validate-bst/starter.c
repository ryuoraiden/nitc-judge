#include <limits.h>
#include "problem.h"

int isBST(Node *root) {
    /* TODO
       Checking only root->left->key < root->key < root->right->key at every node
       is NOT enough (see the statement). Pass down the allowed range instead:
           static int check(Node *r, long long lo, long long hi)
       every key must satisfy lo < key < hi; going left tightens hi to the
       parent's key, going right tightens lo. */
    return 0;
}
