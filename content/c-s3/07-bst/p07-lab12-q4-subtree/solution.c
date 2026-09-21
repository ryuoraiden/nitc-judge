#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    struct Node *left, *right;
} Node;

static Node *newNode(int key) {
    Node *n = malloc(sizeof(Node));
    n->key = key;
    n->left = n->right = NULL;
    return n;
}

static Node *insert(Node *root, int key) {
    if (root == NULL) return newNode(key);
    if (key < root->key) root->left = insert(root->left, key);
    else root->right = insert(root->right, key);
    return root;
}

/* Same shape and same keys, node for node. */
static int identical(Node *a, Node *b) {
    if (a == NULL || b == NULL) return a == b;
    return a->key == b->key && identical(a->left, b->left) && identical(a->right, b->right);
}

/* Keys are unique, so the only candidate is the node holding BST1's root key.
   Find it in O(h), then compare. */
static int isSubtree(Node *t1, Node *t2) {
    if (t1 == NULL) return 1;
    while (t2 != NULL && t2->key != t1->key) t2 = (t1->key < t2->key) ? t2->left : t2->right;
    return t2 != NULL && identical(t1, t2);
}

static Node *readBST(void) {
    int n, k;
    Node *root = NULL;
    if (scanf("%d", &n) != 1) return NULL;
    for (int i = 0; i < n; i++)
        if (scanf("%d", &k) == 1) root = insert(root, k);
    return root;
}

int main(void) {
    Node *t1 = readBST();
    Node *t2 = readBST();
    printf(isSubtree(t1, t2) ? "BST1 is a subtree of BST2\n" : "BST1 is NOT a subtree of BST2\n");
    return 0;
}
