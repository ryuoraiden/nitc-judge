#include <ctype.h>
#include <stdlib.h>
#include "problem.h"

Node *newNode(int value) {
    Node *n = malloc(sizeof(Node));
    n->data = value;
    n->left = n->right = NULL;
    return n;
}

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    if (s[*i] != '(') return NULL;          /* no subtree here at all */
    (*i)++;
    skipSpace(s, i);
    if (s[*i] == ')') { (*i)++; return NULL; }   /* "( )" is an empty child */

    int sign = 1, value = 0;
    if (s[*i] == '-') { sign = -1; (*i)++; }
    while (isdigit((unsigned char)s[*i])) value = value * 10 + (s[(*i)++] - '0');

    Node *n = newNode(sign * value);
    n->left = buildTree(s, i);              /* each returns NULL without consuming */
    n->right = buildTree(s, i);             /* anything if the next char is not '(' */
    skipSpace(s, i);
    if (s[*i] == ')') (*i)++;
    return n;
}

void freeTree(Node *root) {
    if (root == NULL) return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}
