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
Node *insertKey(Node *root, int key);

/* ---- Yours.  All O(h): each walks ONE root-to-leaf path. ---- */
int  lcaBST(Node *root, int a, int b);    /* both keys are present */
int  floorKey(Node *root, int x);         /* largest key <= x, or -1 */
int  ceilKey(Node *root, int x);          /* smallest key >= x, or -1 */
void printRange(Node *root, int lo, int hi);  /* keys in [lo, hi] ascending, each + ' ' */

#endif
