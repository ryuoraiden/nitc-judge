#include <stdio.h>
#include "problem.h"

void levelOrder(Node *root) {
    static Node *q[MAXQ];
    int head = 0, tail = 0;
    if (root == NULL) return;

    q[tail++] = root;
    while (head < tail) {
        int size = tail - head;          /* nodes on the current level */
        for (int k = 0; k < size; k++) {
            Node *cur = q[head++];
            printf("%d ", cur->data);
            if (cur->left)  q[tail++] = cur->left;
            if (cur->right) q[tail++] = cur->right;
        }
        printf("\n");
    }
}
