#include <stdio.h>
#include <stdlib.h>

#define MAXV 105
#define MAXE 10005

typedef struct { int u, v, w; } Edge;

static Edge edges[MAXE];
static int tree[MAXV][MAXV];
static int parent[MAXV], rnk[MAXV];
static int n, m;

static int find(int x) {
    if (parent[x] != x) parent[x] = find(parent[x]);
    return parent[x];
}

static int unite(int a, int b) {
    int ra = find(a), rb = find(b);
    if (ra == rb) return 0;
    if (rnk[ra] < rnk[rb]) parent[ra] = rb;
    else if (rnk[rb] < rnk[ra]) parent[rb] = ra;
    else { parent[rb] = ra; rnk[ra]++; }
    return 1;
}

static int cmpEdge(const void *a, const void *b) {
    const Edge *x = a, *y = b;
    return (x->w > y->w) - (x->w < y->w);
}

static void printTree(void) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) printf("%d ", tree[i][j]);
        printf("\n");
    }
}

int main(void) {
    if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int i = 0; i < m; i++)
        if (scanf("%d %d %d", &edges[i].u, &edges[i].v, &edges[i].w) != 3) return 0;

    for (int i = 1; i <= n; i++) {
        parent[i] = i; rnk[i] = 0;
        for (int j = 1; j <= n; j++) tree[i][j] = (i == j) ? 0 : -1;
    }

    qsort(edges, m, sizeof(Edge), cmpEdge);

    /* Pass 1: can the graph be connected at all?  We must know before printing
       anything, because a disconnected graph outputs "-1" and nothing else. */
    int taken = 0;
    for (int i = 0; i < m && taken < n - 1; i++)
        if (unite(edges[i].u, edges[i].v)) taken++;

    if (taken != n - 1) { printf("-1\n"); return 0; }

    /* Pass 2: same walk again, now printing a snapshot per accepted edge. */
    for (int i = 1; i <= n; i++) { parent[i] = i; rnk[i] = 0; }

    int cost = 0;
    taken = 0;
    for (int i = 0; i < m && taken < n - 1; i++) {
        if (unite(edges[i].u, edges[i].v)) {
            tree[edges[i].u][edges[i].v] = edges[i].w;
            tree[edges[i].v][edges[i].u] = edges[i].w;
            cost += edges[i].w;
            taken++;
            printTree();               /* after EACH accepted edge */
        }
    }

    printTree();                       /* the finished tree again */
    printf("%d\n", cost);
    return 0;
}
