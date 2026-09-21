#include <stdio.h>
#include "problem.h"

int lcaBST(Node *root, int a, int b) {
    /* TODO: both smaller than root -> go left; both larger -> go right;
       otherwise they split here (or one of them IS here): root is the LCA. */
    return -1;
}

int floorKey(Node *root, int x) {
    /* TODO: walk down. Equal -> done. Root bigger than x -> go left.
       Root smaller -> it is a candidate; remember it and go right. */
    return -1;
}

int ceilKey(Node *root, int x) {
    return -1;   /* TODO: mirror of floor */
}

void printRange(Node *root, int lo, int hi) {
    /* TODO: inorder, but skip subtrees that cannot contain anything in range:
       only go left if root->key > lo, only go right if root->key < hi. */
}
