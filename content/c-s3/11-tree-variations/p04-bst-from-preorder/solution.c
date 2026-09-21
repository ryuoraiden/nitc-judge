#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    struct Node *left, *right;
} Node;

static Node *insertKey(Node *r, int k) {
    if (r == NULL) {
        r = malloc(sizeof(Node));
        r->key = k; r->left = r->right = NULL;
        return r;
    }
    if (k < r->key) r->left = insertKey(r->left, k);
    else r->right = insertKey(r->right, k);
    return r;
}

static void postorder(Node *r) { if (!r) return; postorder(r->left); postorder(r->right); printf("%d ", r->key); }

static int height(Node *r) {
    if (!r) return 0;
    int a = height(r->left), b = height(r->right);
    return 1 + (a > b ? a : b);
}

static Node *q[100005];

static void levelOrder(Node *root) {
    int h = 0, t = 0;
    if (root) q[t++] = root;
    while (h < t) {
        Node *c = q[h++];
        printf("%d ", c->key);
        if (c->left) q[t++] = c->left;
        if (c->right) q[t++] = c->right;
    }
    printf("\n");
}

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    Node *root = NULL;
    for (int i = 0; i < n; i++) {
        int k;
        if (scanf("%d", &k) != 1) break;
        root = insertKey(root, k);   /* inserting a preorder in order rebuilds the tree */
    }
    postorder(root); printf("\n");
    levelOrder(root);
    printf("%d\n", height(root));
    return 0;
}
