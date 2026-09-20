#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left, *right;
} Node;

static char line[2000005];

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

static Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    if (s[*i] != '(') return NULL;
    (*i)++;
    skipSpace(s, i);
    if (s[*i] == ')') { (*i)++; return NULL; }
    int value = 0;
    while (isdigit((unsigned char)s[*i])) value = value * 10 + (s[(*i)++] - '0');
    Node *n = malloc(sizeof(Node));
    n->data = value;
    n->left = buildTree(s, i);
    n->right = buildTree(s, i);
    skipSpace(s, i);
    if (s[*i] == ')') (*i)++;
    return n;
}

static Node *findNode(Node *root, int x) {
    if (root == NULL || root->data == x) return root;
    Node *l = findNode(root->left, x);
    return l ? l : findNode(root->right, x);
}

static void printAtDepth(Node *root, int k, int *first) {
    if (root == NULL) return;
    if (k == 0) {
        printf(*first ? "%d" : " %d", root->data);
        *first = 0;
        return;
    }
    printAtDepth(root->left, k - 1, first);
    printAtDepth(root->right, k - 1, first);
}

static void freeTree(Node *r) {
    if (!r) return;
    freeTree(r->left); freeTree(r->right); free(r);
}

int main(void) {
    int x, k, i = 0, first = 1;
    if (fgets(line, sizeof line, stdin) == NULL) return 0;
    if (scanf("%d %d", &x, &k) != 2) return 0;

    Node *root = buildTree(line, &i);
    printAtDepth(findNode(root, x), k, &first);
    printf("\n");
    freeTree(root);
    return 0;
}
