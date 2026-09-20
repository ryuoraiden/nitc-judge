#include <ctype.h>
#include "problem.h"

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    /* TODO
       1. if s[*i] is not '(' -> return NULL, consuming nothing
       2. consume '(' and skip spaces
       3. if s[*i] is ')' -> consume it, return NULL (empty child)
       4. read the number digit by digit, make a node
       5. node->left  = buildTree(s, i);
          node->right = buildTree(s, i);
          (step 1 makes these return NULL safely when a child is missing)
       6. skip spaces, consume the closing ')', return the node */
    return NULL;
}
