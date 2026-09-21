#include <stdio.h>
#include "problem.h"

static char line[200005];

static Node *readTree(void) {
    if (fgets(line, sizeof line, stdin) == NULL) return NULL;
    int i = 0;
    return buildTree(line, &i);
}

int main(void) {
    int q;
    if (scanf("%d", &q) != 1) return 0;
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF) { }
    while (q--) {
        Node *root = readTree();
        printf("%s\n", isBST(root) ? "YES" : "NO");
        freeTree(root);
    }
    return 0;
}
