#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left, *right;
} Node;

static char s[200005];

static Node *buildTree(const char *str, int *i) {
    if (str[*i] != '(') return NULL;
    (*i)++;
    if (str[*i] == ')') { (*i)++; return NULL; }
    int value = 0;
    while (isdigit((unsigned char)str[*i])) value = value * 10 + (str[(*i)++] - '0');
    Node *n = malloc(sizeof(Node));
    n->data = value;
    n->left = buildTree(str, i);
    n->right = buildTree(str, i);
    if (str[*i] == ')') (*i)++;
    return n;
}

static void postorder(Node *r, int *first) {
    if (r == NULL) return;
    postorder(r->left, first);
    postorder(r->right, first);
    printf(*first ? "%d" : " %d", r->data);
    *first = 0;
}

static void freeTree(Node *r) {
    if (!r) return;
    freeTree(r->left); freeTree(r->right); free(r);
}

int main(void) {
    int i = 0, first = 1;
    if (scanf("%200000s", s) != 1) return 0;
    Node *root = buildTree(s, &i);
    postorder(root, &first);
    printf("\n");
    freeTree(root);
    return 0;
}
