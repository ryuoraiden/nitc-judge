#include <ctype.h>
#include <stdlib.h>
#include "problem.h"

Node *newNode(int key) {
    Node *n = malloc(sizeof(Node));
    n->key = key;
    n->left = n->right = NULL;
    return n;
}

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    if (s[*i] != '(') return NULL;
    (*i)++;
    skipSpace(s, i);
    if (s[*i] == ')') { (*i)++; return NULL; }
    int sign = 1, v = 0;
    if (s[*i] == '-') { sign = -1; (*i)++; }
    while (isdigit((unsigned char)s[*i])) v = v * 10 + (s[(*i)++] - '0');
    Node *n = newNode(sign * v);
    n->left = buildTree(s, i);
    n->right = buildTree(s, i);
    skipSpace(s, i);
    if (s[*i] == ')') (*i)++;
    return n;
}

void freeTree(Node *r) {
    if (!r) return;
    freeTree(r->left);
    freeTree(r->right);
    free(r);
}
