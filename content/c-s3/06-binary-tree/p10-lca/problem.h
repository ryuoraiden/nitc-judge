#ifndef PROBLEM_H
#define PROBLEM_H

#include <stddef.h>   /* NULL */

typedef struct Node {
    int data;
    struct Node *left;
    struct Node *right;
} Node;

/* ---- Provided for you. ---- */
Node *newNode(int value);
Node *buildTree(const char *s, int *i);   /* parses either parenthesized notation */
void  freeTree(Node *root);

/* ---- Yours: lowest common ancestor of the nodes holding a and b.
        Both are guaranteed to be in the tree; a node is its own ancestor. ---- */
Node *lca(Node *root, int a, int b);

#endif
