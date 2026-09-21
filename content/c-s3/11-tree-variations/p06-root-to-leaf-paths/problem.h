#ifndef PROBLEM_H
#define PROBLEM_H

#include <stddef.h>   /* NULL */

typedef struct Node {
    int key;
    struct Node *left;
    struct Node *right;
} Node;

#define MAXDEPTH 100005

/* ---- Provided. ---- */
Node *newNode(int key);
Node *buildTree(const char *s, int *i);
void  freeTree(Node *root);

/* ---- Yours: print every root-to-leaf path on its own line, left to right,
        keys joined by "->".  Then print how many of those paths have a key sum
        equal to target. ---- */
void rootToLeaf(Node *root, int target);

#endif
