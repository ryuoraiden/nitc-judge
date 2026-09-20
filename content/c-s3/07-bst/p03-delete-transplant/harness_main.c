#include <stdio.h>
#include "problem.h"

static void inorder(BST r) { if (!r) return; inorder(r->left); printf("%d ", r->key); inorder(r->right); }
static void preorder(BST r) { if (!r) return; printf("%d ", r->key); preorder(r->left); preorder(r->right); }

int main(void) {
    BST T = NULL;
    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'i') {
            int v; if (scanf("%d", &v) != 1) break;
            T = insert(T, v);
        } else if (cmd == 'd') {
            int v; if (scanf("%d", &v) != 1) break;
            BST x = search(T, v);
            if (x == NULL) printf("NOT PRESENT\n");
            else T = delete(T, x);
        } else if (cmd == 'p') {
            if (T == NULL) printf("NULL");
            inorder(T); printf("\n");
        } else if (cmd == 't') {
            if (T == NULL) printf("NULL");
            preorder(T); printf("\n");
        }
    }
    return 0;
}
