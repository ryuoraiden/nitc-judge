#include <stdio.h>
#include <stdlib.h>

typedef struct _BSTNode {
    int key;
    struct _BSTNode *left, *right, *parent;
} BSTNode;
typedef BSTNode *BST;

int main(void) {
    /* TODO - it is two things you already have, glued together:
         1. find the k-th smallest node (inorder with a shared counter)
         2. delete THAT NODE with the Week 2 transplant delete
       Print the deleted key, or -1 if the tree has fewer than k nodes. */
    return 0;
}
