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

/* ---- Yours. ---- */
int height(Node *root);        /* nodes on the longest root-to-leaf path; empty = 0 */
int countNodes(Node *root);
int countLeaves(Node *root);   /* nodes with no children */

#endif
