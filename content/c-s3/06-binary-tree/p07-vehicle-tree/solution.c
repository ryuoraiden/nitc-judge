#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Vehicle {
    int vno;
    char model[32];
    int price;
    struct Vehicle *left, *right;
} Vehicle;

static Vehicle *q[10005];

static Vehicle *newVehicle(int vno, const char *model, int price) {
    Vehicle *v = malloc(sizeof(Vehicle));
    v->vno = vno;
    strncpy(v->model, model, sizeof v->model - 1);
    v->model[sizeof v->model - 1] = '\0';
    v->price = price;
    v->left = v->right = NULL;
    return v;
}

/* Level-order insertion: the new node goes into the first free child slot
   found by a BFS, left before right. */
static Vehicle *insertLevelOrder(Vehicle *root, Vehicle *node) {
    if (root == NULL) return node;
    int head = 0, tail = 0;
    q[tail++] = root;
    while (head < tail) {
        Vehicle *cur = q[head++];
        if (cur->left == NULL) { cur->left = node; return root; }
        q[tail++] = cur->left;
        if (cur->right == NULL) { cur->right = node; return root; }
        q[tail++] = cur->right;
    }
    return root;
}

static void show(Vehicle *v) { printf("%d %s %d\n", v->vno, v->model, v->price); }

static void inorder(Vehicle *r)   { if (!r) return; inorder(r->left); show(r); inorder(r->right); }
static void preorder(Vehicle *r)  { if (!r) return; show(r); preorder(r->left); preorder(r->right); }
static void postorder(Vehicle *r) { if (!r) return; postorder(r->left); postorder(r->right); show(r); }

static void levelOrder(Vehicle *root) {
    if (root == NULL) return;
    int head = 0, tail = 0;
    q[tail++] = root;
    while (head < tail) {
        Vehicle *cur = q[head++];
        show(cur);
        if (cur->left) q[tail++] = cur->left;
        if (cur->right) q[tail++] = cur->right;
    }
}

static Vehicle *search(Vehicle *r, int vno) {
    if (r == NULL || r->vno == vno) return r;
    Vehicle *l = search(r->left, vno);
    return l ? l : search(r->right, vno);
}

static void freeTree(Vehicle *r) {
    if (!r) return;
    freeTree(r->left); freeTree(r->right); free(r);
}

int main(void) {
    Vehicle *root = NULL;
    int opt;
    while (scanf("%d", &opt) == 1) {
        if (opt == 1) {
            int vno, price;
            char model[64];
            if (scanf("%d %63s %d", &vno, model, &price) != 3) break;
            root = insertLevelOrder(root, newVehicle(vno, model, price));
        } else if (opt == 2) inorder(root);
        else if (opt == 3) preorder(root);
        else if (opt == 4) postorder(root);
        else if (opt == 5) levelOrder(root);
        else if (opt == 6) {
            int vno;
            if (scanf("%d", &vno) != 1) break;
            Vehicle *v = search(root, vno);
            if (v) show(v); else printf("-1\n");
        } else if (opt == 7) break;
    }
    freeTree(root);
    return 0;
}
