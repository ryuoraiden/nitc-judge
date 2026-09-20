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

/* ---- Yours: print the node values in order, each followed by a space. ---- */
void preorder(Node *root);
void inorder(Node *root);
void postorder(Node *root);

#endif
