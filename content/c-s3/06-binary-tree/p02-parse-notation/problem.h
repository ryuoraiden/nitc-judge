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
void  freeTree(Node *root);

/* ---- Yours: parse a tree starting at s[*i], advancing *i past it.
        Return NULL for an empty subtree "( )" / "()", and also return NULL
        WITHOUT consuming anything if s[*i] (after spaces) is not '('. ---- */
Node *buildTree(const char *s, int *i);

#endif
