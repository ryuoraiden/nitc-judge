#ifndef PROBLEM_H
#define PROBLEM_H

#include <stddef.h>   /* NULL */

typedef struct Node {
    int data;
    struct Node *left;
    struct Node *right;
} Node;

/* ---- Provided. ---- */
Node *newNode(int value);
void  freeTree(Node *root);

/* ---- Yours: rebuild the tree from its preorder and inorder sequences
        (all values distinct), and return the root. ---- */
Node *buildFromPreIn(int pre[], int in[], int n);

#endif
