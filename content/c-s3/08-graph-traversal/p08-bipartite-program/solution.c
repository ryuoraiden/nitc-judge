#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXV 105

static int adj[MAXV][MAXV], deg[MAXV];
static int colour[MAXV];
static int stack_[MAXV * MAXV];
static char line[8192];

static int cmpInt(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF) { }   /* eat the rest of line 1 */

    for (int read = 0; read < n; ) {
        if (fgets(line, sizeof line, stdin) == NULL) break;
        char *tok = strtok(line, " \t\r\n");
        if (tok == NULL) continue;                       /* blank line: skip */
        int u = atoi(tok);
        deg[u] = 0;
        while ((tok = strtok(NULL, " \t\r\n")) != NULL) adj[u][deg[u]++] = atoi(tok);
        qsort(adj[u], deg[u], sizeof(int), cmpInt);
        read++;
    }

    for (int v = 1; v <= n; v++) colour[v] = -1;

    for (int s = 1; s <= n; s++) {
        if (colour[s] != -1) continue;
        int top = -1;
        colour[s] = 0;
        stack_[++top] = s;

        while (top >= 0) {
            int u = stack_[top--];
            for (int i = 0; i < deg[u]; i++) {
                int v = adj[u][i];
                if (colour[v] == -1) {
                    colour[v] = 1 - colour[u];
                    stack_[++top] = v;
                } else if (colour[v] == colour[u]) {
                    printf("-1\n");
                    return 0;
                }
            }
        }
    }

    for (int c = 0; c <= 1; c++) {
        int first = 1;
        for (int v = 1; v <= n; v++)
            if (colour[v] == c) { printf(first ? "%d" : " %d", v); first = 0; }
        printf("\n");
    }
    return 0;
}
