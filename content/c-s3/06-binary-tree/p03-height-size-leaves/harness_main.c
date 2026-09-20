#include <stdio.h>
#include "problem.h"

static char line[200005];

static Node *readTree(void) {
    if (fgets(line, sizeof line, stdin) == NULL) return NULL;
    int i = 0;
    return buildTree(line, &i);
}

int main(void) {
    Node *root = readTree();
    printf("%d %d %d\n", height(root), countNodes(root), countLeaves(root));
    freeTree(root);
    return 0;
}
