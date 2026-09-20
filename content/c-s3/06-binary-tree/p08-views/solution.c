#include <stdio.h>
#include "problem.h"

static Node *q[MAXQ];
static int hdq[MAXQ];

static void view(Node *root, int wantLast) {
    int head = 0, tail = 0;
    if (root) q[tail++] = root;
    while (head < tail) {
        int size = tail - head;
        for (int k = 0; k < size; k++) {
            Node *cur = q[head++];
            if ((!wantLast && k == 0) || (wantLast && k == size - 1)) printf("%d ", cur->data);
            if (cur->left) q[tail++] = cur->left;
            if (cur->right) q[tail++] = cur->right;
        }
    }
    printf("\n");
}

void leftView(Node *root)  { view(root, 0); }
void rightView(Node *root) { view(root, 1); }

void topView(Node *root) {
    static int seen[2 * MAXQ + 1], val[2 * MAXQ + 1];
    int head = 0, tail = 0, lo = 0, hi = 0;
    if (root == NULL) { printf("\n"); return; }

    /* horizontal distances fit in [-tail, tail]; offset them to be array indices */
    const int OFF = MAXQ;
    for (int i = 0; i < 2 * MAXQ + 1; i++) seen[i] = 0;

    q[tail] = root; hdq[tail] = 0; tail++;
    while (head < tail) {
        Node *cur = q[head];
        int hd = hdq[head];
        head++;
        if (!seen[hd + OFF]) { seen[hd + OFF] = 1; val[hd + OFF] = cur->data; }
        if (hd < lo) lo = hd;
        if (hd > hi) hi = hd;
        if (cur->left)  { q[tail] = cur->left;  hdq[tail] = hd - 1; tail++; }
        if (cur->right) { q[tail] = cur->right; hdq[tail] = hd + 1; tail++; }
    }
    for (int hd = lo; hd <= hi; hd++) printf("%d ", val[hd + OFF]);
    printf("\n");
}
