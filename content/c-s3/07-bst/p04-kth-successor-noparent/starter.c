#include "problem.h"

int kthSmallest(Node *root, int k) {
    /* TODO: inorder is sorted, so the k-th smallest is the k-th node an inorder
       traversal visits. Walk inorder with a counter and stop at k.
       A helper taking a counter by pointer is the easy way:
           static void walk(Node *r, int k, int *count, int *answer)
       Return -1 if the tree has fewer than k nodes. */
    return -1;
}

int maximum(Node *root) {
    /* TODO: rightmost key, -1 if empty. */
    return -1;
}

int successorOf(Node *root, int key) {
    /* TODO - WITHOUT a parent pointer.
       Walk down from the root. Every time you move LEFT, the node you are leaving
       is bigger than key, so remember it as the best candidate so far. Moving
       right can never be the successor. When you fall off the tree (or land on
       key and it has a right subtree), you have the answer. */
    return -1;
}
