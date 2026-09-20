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

#define MAXQ 100005

/* ---- Yours: print each level on its own line, left to right, values
        followed by a space.  Print nothing at all for an empty tree. ---- */
void levelOrder(Node *root);

#endif
