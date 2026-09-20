#ifndef PROBLEM_H
#define PROBLEM_H
#include <stddef.h>   /* NULL */

/* Note: NO parent pointer - PD Lab 12 Q2 forbids it. */
typedef struct Node {
    int key;
    struct Node *left;
    struct Node *right;
} Node;

/* ---- Provided. ---- */
Node *insertKey(Node *root, int key);
Node *searchKey(Node *root, int key);

/* ---- Yours. ---- */
int kthSmallest(Node *root, int k);   /* the k-th smallest key, or -1 if k is too big */
int maximum(Node *root);              /* -1 if the tree is empty */
int successorOf(Node *root, int key); /* next key in inorder after `key`, or -1 */

#endif
