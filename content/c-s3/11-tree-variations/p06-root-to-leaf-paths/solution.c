#include <stdio.h>
#include "problem.h"

static int path[MAXDEPTH];

static void walk(Node *r, int depth, int sum, int target, int *count) {
    if (r == NULL) return;
    path[depth] = r->key;                /* overwritten on backtrack: no pop needed */
    sum += r->key;

    if (r->left == NULL && r->right == NULL) {
        for (int i = 0; i <= depth; i++) printf(i ? "->%d" : "%d", path[i]);
        printf("\n");
        if (sum == target) (*count)++;
        return;
    }
    walk(r->left, depth + 1, sum, target, count);
    walk(r->right, depth + 1, sum, target, count);
}

void rootToLeaf(Node *root, int target) {
    int count = 0;
    walk(root, 0, 0, target, &count);
    printf("%d\n", count);
}
