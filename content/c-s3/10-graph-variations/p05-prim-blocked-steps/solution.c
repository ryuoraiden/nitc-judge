#include <stdio.h>

#define MAXV 105
#define INF 1000000000

static int w[MAXV][MAXV], tree[MAXV][MAXV];
static int key[MAXV], parent[MAXV], done_[MAXV];
static int n;

static void printTree(void) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) printf("%d ", tree[i][j]);
        printf("\n");
    }
}

/* Runs Prim.  With print != 0, prints the matrix after each added edge.
   Returns the total cost, or -1 if some vertex could not be reached. */
static int prim(int s, int print) {
    for (int i = 1; i <= n; i++) {
        key[i] = INF; parent[i] = -1; done_[i] = 0;
        for (int j = 1; j <= n; j++) tree[i][j] = (i == j) ? 0 : -1;
    }
    key[s] = 0;
    int cost = 0;

    for (int step = 0; step < n; step++) {
        int u = -1;
        for (int v = 1; v <= n; v++)
            if (!done_[v] && (u == -1 || key[v] < key[u])) u = v;
        if (u == -1 || key[u] == INF) return -1;
        done_[u] = 1;

        if (parent[u] != -1) {                  /* s itself adds no edge */
            tree[u][parent[u]] = tree[parent[u]][u] = key[u];
            cost += key[u];
            if (print) printTree();
        }
        for (int v = 1; v <= n; v++) {
            if (done_[v] || w[u][v] == 0) continue;
            if (w[u][v] < key[v]) { key[v] = w[u][v]; parent[v] = u; }
        }
    }
    return cost;
}

int main(void) {
    int m, s, b;
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;
    for (int i = 0; i < m; i++) {
        int u, v, x;
        if (scanf("%d %d %d", &u, &v, &x) != 3) return 0;
        w[u][v] = w[v][u] = x;
    }
    if (scanf("%d", &b) != 1) b = 0;
    for (int i = 0; i < b; i++) {
        int u, v;
        if (scanf("%d %d", &u, &v) != 2) break;
        w[u][v] = w[v][u] = 0;                  /* blocked == the edge does not exist */
    }

    if (prim(s, 0) == -1) { printf("-1\n"); return 0; }   /* check before printing */

    int cost = prim(s, 1);
    printTree();
    printf("%d\n", cost);
    return 0;
}
