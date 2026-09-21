#ifndef PROBLEM_H
#define PROBLEM_H

#include <stddef.h>   /* NULL */

typedef struct Node {
    int key;
    struct Node *left;
    struct Node *right;
} Node;

/* ---- Provided. ---- */
Node *newNode(int key);
Node *buildTree(const char *s, int *i);
void  freeTree(Node *root);

/* ---- Yours: 1 if this binary tree is a valid BST (strict: no duplicates), else 0. ---- */
int isBST(Node *root);

#endif
