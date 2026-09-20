#include <stdio.h>
#include "problem.h"

static void post(Node *r) { if (!r) return; post(r->left); post(r->right); printf("%d ", r->data); }

int main(void) {
    int n;
    static int pre[10005], in[10005];
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) scanf("%d", &pre[i]);
    for (int i = 0; i < n; i++) scanf("%d", &in[i]);
    Node *root = buildFromPreIn(pre, in, n);
    post(root);
    printf("\n");
    freeTree(root);
    return 0;
}
