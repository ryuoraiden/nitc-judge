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

static Node *InsertKey(Node *root, int num) {
    if (root == NULL) return newNode(num);
    if (num < root->key) root->left = InsertKey(root->left, num);
    else if (num > root->key) root->right = InsertKey(root->right, num);
    return root;
}

static Node *SearchKey(Node *root, int num) {
    while (root != NULL && root->key != num) root = (num < root->key) ? root->left : root->right;
    return root;
}

/* Two children: replace with the inorder SUCCESSOR (smallest key on the right). */
static Node *DeleteKey(Node *root, int num) {
    if (root == NULL) return NULL;
    if (num < root->key) root->left = DeleteKey(root->left, num);
    else if (num > root->key) root->right = DeleteKey(root->right, num);
    else {
        if (root->left == NULL) { Node *r = root->right; free(root); return r; }
        if (root->right == NULL) { Node *l = root->left; free(root); return l; }
        Node *succ = root->right;
        while (succ->left != NULL) succ = succ->left;
        root->key = succ->key;                        /* copy the successor up... */
        root->right = DeleteKey(root->right, succ->key);  /* ...then delete it below */
    }
    return root;
}

static void Inorder(Node *r)   { if (!r) return; Inorder(r->left); printf("%d ", r->key); Inorder(r->right); }
static void Preorder(Node *r)  { if (!r) return; printf("%d ", r->key); Preorder(r->left); Preorder(r->right); }
static void Postorder(Node *r) { if (!r) return; Postorder(r->left); Postorder(r->right); printf("%d ", r->key); }

int main(void) {
    Node *root = NULL;
    char c;
    while (scanf(" %c", &c) == 1) {
        int num;
        if (c == 'e') break;
        else if (c == 'i') { if (scanf("%d", &num) != 1) break; root = InsertKey(root, num); }
        else if (c == 's') {
            if (scanf("%d", &num) != 1) break;
            printf(SearchKey(root, num) ? "PRESENT\n" : "NOT PRESENT\n");
        }
        else if (c == 'd') {
            if (scanf("%d", &num) != 1) break;
            if (SearchKey(root, num) == NULL) printf("NOT PRESENT\n");
            else root = DeleteKey(root, num);
        }
        else if (c == 'p') { if (!root) printf("NULL"); Inorder(root);   printf("\n"); }
        else if (c == 't') { if (!root) printf("NULL"); Preorder(root);  printf("\n"); }
        else if (c == 'b') { if (!root) printf("NULL"); Postorder(root); printf("\n"); }
    }
    return 0;
}
