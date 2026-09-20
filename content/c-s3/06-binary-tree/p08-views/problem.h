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

/* ---- Yours: each prints one line (values followed by a space, then '\n'). ---- */
void leftView(Node *root);    /* first node of every level */
void rightView(Node *root);   /* last node of every level */
void topView(Node *root);     /* first node seen at each horizontal distance,
                                 printed from leftmost column to rightmost */

#endif
