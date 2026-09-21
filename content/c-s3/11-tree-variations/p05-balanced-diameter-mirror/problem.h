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

/* ---- Yours. ---- */
int  isBalanced(Node *root);   /* 1 if at EVERY node the subtree heights differ by <= 1 */
int  diameter(Node *root);     /* edges on the longest path between any two nodes; 0 if <= 1 node */
void mirror(Node *root);       /* swap left and right at every node, in place */

#endif
