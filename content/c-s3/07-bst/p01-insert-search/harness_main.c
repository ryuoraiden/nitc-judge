#include <stdio.h>
#include "problem.h"

static void inorder(Node *r) { if (!r) return; inorder(r->left); printf("%d ", r->key); inorder(r->right); }
static void preorder(Node *r) { if (!r) return; printf("%d ", r->key); preorder(r->left); preorder(r->right); }

int main(void) {
    Node *root = NULL;
    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'i') {
            int v; if (scanf("%d", &v) != 1) break;
            root = insertKey(root, v);
        } else if (cmd == 's') {
            int v; if (scanf("%d", &v) != 1) break;
            printf(searchKey(root, v) ? "PRESENT\n" : "NOT PRESENT\n");
        } else if (cmd == 'p') {
            if (root == NULL) printf("NULL");
            inorder(root); printf("\n");
        } else if (cmd == 't') {
            if (root == NULL) printf("NULL");
            preorder(root); printf("\n");
        }
    }
    return 0;
}
