#include <stdio.h>
#include "problem.h"

int lcaBST(Node *root, int a, int b) {
    while (root != NULL) {
        if (a < root->key && b < root->key) root = root->left;
        else if (a > root->key && b > root->key) root = root->right;
        else return root->key;            /* they split here */
    }
    return -1;
}

int floorKey(Node *root, int x) {
    int best = -1;
    while (root != NULL) {
        if (root->key == x) return x;
        if (root->key > x) root = root->left;
        else { best = root->key; root = root->right; }   /* candidate, look for bigger */
    }
    return best;
}

int ceilKey(Node *root, int x) {
    int best = -1;
    while (root != NULL) {
        if (root->key == x) return x;
        if (root->key < x) root = root->right;
        else { best = root->key; root = root->left; }
    }
    return best;
}

void printRange(Node *root, int lo, int hi) {
    if (root == NULL) return;
    if (root->key > lo) printRange(root->left, lo, hi);     /* smaller keys may qualify */
    if (root->key >= lo && root->key <= hi) printf("%d ", root->key);
    if (root->key < hi) printRange(root->right, lo, hi);    /* larger keys may qualify */
}
