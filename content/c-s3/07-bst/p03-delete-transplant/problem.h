#ifndef PROBLEM_H
#define PROBLEM_H
#include <stddef.h>   /* NULL */

/* The exact node from the Week 2 assignment sheet. */
typedef struct _BSTNode {
    int key;
    struct _BSTNode *left;
    struct _BSTNode *right;
    struct _BSTNode *parent;
} BSTNode;

typedef BSTNode *BST;

/* ---- Provided for you. ---- */
BST init(int key);
BST insert(BST T, int k);
BST search(BST T, int k);
BST minimum(BST T);

/* ---- Yours. ---- */
BST transplant(BST T, BST u, BST v);   /* returns the root */
BST delete(BST T, BST x);              /* returns the root */

#endif
