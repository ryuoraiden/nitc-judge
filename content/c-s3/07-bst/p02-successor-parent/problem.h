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

/* ---- Yours. ---- */
BST minimum(BST T);
BST maximum(BST T);
BST successor(BST T, BST x);     /* NULL if x holds the largest key */
BST predecessor(BST T, BST x);   /* NULL if x holds the smallest key */

#endif
