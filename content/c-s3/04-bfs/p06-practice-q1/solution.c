#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXV 105

static int adj[MAXV][MAXV];
static int deg[MAXV];

static int cmpInt(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    /* Consume the rest of the first line so fgets starts on the adjacency lists. */
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF) { }

    char line[8192];
    for (int read = 0; read < n; ) {
        if (fgets(line, sizeof line, stdin) == NULL) break;

        char *tok = strtok(line, " \t\r\n");
        if (tok == NULL) continue;          /* skip blank lines */

        int u = atoi(tok);
        deg[u] = 0;
        while ((tok = strtok(NULL, " \t\r\n")) != NULL)
            adj[u][deg[u]++] = atoi(tok);
        qsort(adj[u], deg[u], sizeof(int), cmpInt);
        read++;
    }

    int s;
    if (scanf("%d", &s) != 1) return 0;

    int parent[MAXV], seen[MAXV], queue[MAXV];
    for (int v = 0; v <= n; v++) { parent[v] = -1; seen[v] = 0; }

    int head = 0, tail = 0;
    seen[s] = 1;
    queue[tail++] = s;

    while (head < tail) {
        int u = queue[head++];
        for (int i = 0; i < deg[u]; i++) {
            int v = adj[u][i];
            if (!seen[v]) {
                seen[v] = 1;
                parent[v] = u;
                queue[tail++] = v;
            }
        }
    }

    for (int v = 1; v <= n; v++) {
        if (!seen[v]) { printf("-1\n"); continue; }
        int stack[MAXV], len = 0;
        for (int x = v; x != -1; x = parent[x]) stack[len++] = x;
        for (int i = len - 1; i >= 0; i--)
            printf("%d%s", stack[i], i > 0 ? "-" : "");
        printf("\n");
    }
    return 0;
}
