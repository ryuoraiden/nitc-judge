#include <stdio.h>
#include <stdlib.h>

typedef struct _BSTNode {
    int key;
    struct _BSTNode *left, *right, *parent;
} BSTNode;
typedef BSTNode *BST;

static BST insert(BST T, int k) {
    BST y = NULL, x = T;
    while (x) { y = x; x = (k < x->key) ? x->left : x->right; }
    BST n = malloc(sizeof(BSTNode));
    n->key = k; n->left = n->right = NULL; n->parent = y;
    if (!y) return n;
    if (k < y->key) y->left = n; else y->right = n;
    return T;
}

static BST minimum(BST T) {
    while (T && T->left) T = T->left;
    return T;
}

/* The k-th node in inorder, or NULL.  *count is shared across the recursion. */
static BST kth(BST T, int k, int *count) {
    if (T == NULL) return NULL;
    BST found = kth(T->left, k, count);
    if (found) return found;
    if (++(*count) == k) return T;
    return kth(T->right, k, count);
}

static BST transplant(BST T, BST u, BST v) {
    if (u->parent == NULL) T = v;
    else if (u == u->parent->left) u->parent->left = v;
    else u->parent->right = v;
    if (v) v->parent = u->parent;
    return T;
}

static BST delete(BST T, BST x) {
    if (x->left == NULL) T = transplant(T, x, x->right);
    else if (x->right == NULL) T = transplant(T, x, x->left);
    else {
        BST y = minimum(x->right);
        if (y->parent != x) {
            T = transplant(T, y, y->right);
            y->right = x->right;
            y->right->parent = y;
        }
        T = transplant(T, x, y);
        y->left = x->left;
        y->left->parent = y;
    }
    free(x);
    return T;
}

static void inorder(BST r)  { if (!r) return; inorder(r->left); printf("%d ", r->key); inorder(r->right); }
static void preorder(BST r) { if (!r) return; printf("%d ", r->key); preorder(r->left); preorder(r->right); }

int main(void) {
    BST T = NULL;
    char c;
    while (scanf(" %c", &c) == 1) {
        if (c == 'e') break;
        if (c == 'i') {
            int k; if (scanf("%d", &k) != 1) break;
            T = insert(T, k);
        } else if (c == 'r') {
            int k, count = 0;
            if (scanf("%d", &k) != 1) break;
            BST x = (k >= 1) ? kth(T, k, &count) : NULL;
            if (x == NULL) { printf("-1\n"); continue; }
            printf("%d\n", x->key);
            T = delete(T, x);
        } else if (c == 'p') {
            if (!T) printf("NULL");
            inorder(T); printf("\n");
        } else if (c == 't') {
            if (!T) printf("NULL");
            preorder(T); printf("\n");
        }
    }
    return 0;
}
