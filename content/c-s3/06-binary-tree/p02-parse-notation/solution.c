#include <ctype.h>
#include "problem.h"

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    if (s[*i] != '(') return NULL;
    (*i)++;
    skipSpace(s, i);
    if (s[*i] == ')') { (*i)++; return NULL; }

    int sign = 1, value = 0;
    if (s[*i] == '-') { sign = -1; (*i)++; }
    while (isdigit((unsigned char)s[*i])) value = value * 10 + (s[(*i)++] - '0');

    Node *n = newNode(sign * value);
    n->left = buildTree(s, i);
    n->right = buildTree(s, i);
    skipSpace(s, i);
    if (s[*i] == ')') (*i)++;
    return n;
}
