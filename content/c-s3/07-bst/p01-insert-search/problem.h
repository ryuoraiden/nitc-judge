#ifndef PROBLEM_H
#define PROBLEM_H
#include <stddef.h>   /* NULL */

typedef struct Node {
    int key;
    struct Node *left;
    struct Node *right;
} Node;

/* ---- Yours. ---- */
Node *insertKey(Node *root, int key);   /* returns the (possibly new) root */
Node *searchKey(Node *root, int key);   /* NULL if absent */

#endif
