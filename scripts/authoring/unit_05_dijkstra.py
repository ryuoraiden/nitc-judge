"""Unit 05 - Dijkstra.  Run: python scripts/authoring/unit_05_dijkstra.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report

PACK = "c-s3"
UNIT = "05-dijkstra"

import random
rng = random.Random(505)

write_unit(PACK, UNIT, "Dijkstra and weighted shortest paths",
           "Weighted graphs, where BFS stops working. The O(V^2) version first, then "
           "Week 4 Practice Question 2, then the heap-backed version.")

MATRIX_TYPES = r"""
#define MAXV 105
#define NOEDGE 999          /* the sheet's marker for "no direct road" */
#define INF 1000000000      /* unreachable */
"""

MATRIX_FORMAT = r"""
## Input format

```
n
<n lines of n integers: the adjacency matrix>
k
```

`time[i][j]` is the cost of the one-way edge `i -> j`. A value of **999** means
there is no such edge. The diagonal is 0. `k` is given **1-based**; the harness
converts it before calling you, so your `src` is already 0-based.
"""

DIJKSTRA_IMPL = r"""
#include "problem.h"

void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]) {
    int done[MAXV];
    for (int i = 0; i < n; i++) { dist[i] = INF; done[i] = 0; }
    dist[src] = 0;

    for (int iter = 0; iter < n; iter++) {
        int u = -1;
        for (int i = 0; i < n; i++)
            if (!done[i] && (u == -1 || dist[i] < dist[u])) u = i;

        if (u == -1 || dist[u] == INF) break;
        done[u] = 1;

        for (int v = 0; v < n; v++) {
            if (w[u][v] == NOEDGE || u == v) continue;
            if (dist[u] + w[u][v] < dist[v]) dist[v] = dist[u] + w[u][v];
        }
    }
}
"""

# --------------------------------------------------------------- p01
H1 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
""" + MATRIX_TYPES + r"""
/* dist[v] = cost of the cheapest src->v path, or INF if v is unreachable.
   Vertices are 0-based here, matching the matrix indices. */
void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]);

#endif
"""

M1 = r"""
#include <stdio.h>
#include "problem.h"

static int w[MAXV][MAXV];

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &w[i][j]);

    int k;
    if (scanf("%d", &k) != 1) return 0;

    int dist[MAXV];
    dijkstra(n, w, k - 1, dist);

    for (int v = 0; v < n; v++)
        printf("%d%s", dist[v] >= INF ? -1 : dist[v], v + 1 < n ? " " : "");
    printf("\n");
    return 0;
}
"""

S1 = r"""
#include "problem.h"

void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]) {
    int done[MAXV];

    /* TODO
       1. dist[i] = INF for all i, done[i] = 0, then dist[src] = 0
       2. repeat n times:
            a. pick the unfinished vertex u with the smallest dist
            b. if there is none, or dist[u] is still INF, stop - everything
               reachable has been settled
            c. mark u done
            d. relax every edge out of u: if dist[u] + w[u][v] beats dist[v],
               write the smaller value into dist[v]
       Skip w[u][v] == NOEDGE: 999 means there is no edge, not a cost of 999. */
}
"""

A1 = DIJKSTRA_IMPL

T1 = [
    "5\n0 5 999 999 2\n999 0 1 1 999\n999 999 0 2 9\n999 999 999 0 10\n999 2 7 999 0\n1\n",
    "4\n0 1 999 999\n999 0 1 999\n999 999 0 1\n999 999 999 0\n1\n",
    "4\n0 10 999 999\n999 0 1 999\n999 999 0 1\n999 999 999 0\n1\n",
    "3\n0 999 999\n999 0 999\n999 999 0\n1\n",
    "5\n0 4 2 999 999\n999 0 999 5 999\n999 1 0 8 10\n999 999 999 0 2\n999 999 999 999 0\n1\n",
    "4\n0 999 999 999\n1 0 999 999\n999 1 0 999\n999 999 1 0\n4\n",
    "6\n0 7 9 999 999 14\n7 0 10 15 999 999\n9 10 0 11 999 2\n999 15 11 0 6 999\n999 999 999 6 0 9\n14 999 2 999 9 0\n1\n",
]

write_problem(
    PACK, UNIT, "p01-dijkstra-matrix", title="Dijkstra on an adjacency matrix",
    mode="function", difficulty="medium", estimated_minutes=15, samples=2,
    topics=["dijkstra", "shortest path", "greedy"],
    prereqs=[f"{PACK}.04-bfs.p03-bfs-distances"],
    source="Core of NITC_Lab_S3_DSA Week 4 Practice Question 2",
    hints=[
        "Two arrays: dist[] for best-known costs and done[] for vertices already "
        "settled. Never revisit a settled vertex.",
        "Finding the minimum is a plain linear scan over unfinished vertices: "
        "if (!done[i] && (u == -1 || dist[i] < dist[u])) u = i;",
        "Guard the relaxation with w[u][v] == NOEDGE. 999 is a marker meaning "
        "'no edge', so treating it as a real cost invents roads that do not exist.",
    ],
    header=H1, harness=M1, starter=S1, solution=A1, tests=T1,
    statement=r"""
# Dijkstra on an adjacency matrix

BFS finds shortest paths by counting edges. The moment edges have different costs,
that stops working: a two-edge route can be cheaper than a one-edge route, and BFS
would happily return the one-edge one.

Dijkstra fixes it with a greedy rule: **repeatedly settle the unfinished vertex
with the smallest known distance, then relax its outgoing edges.**

```c
void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]);
```

`dist[v]` is the cheapest cost from `src` to `v`, or `INF` if unreachable.
""" + MATRIX_FORMAT + r"""
## Output

`dist[0] dist[1] ... dist[n-1]`, space separated. Unreachable prints `-1`.

## Example

```
5
0 5 999 999 2
999 0 1 1 999
999 999 0 2 9
999 999 999 0 10
999 2 7 999 0
1
```

```
0 4 5 5 2
```

Note vertex 2: the direct road `1 -> 2` costs 5, but going `1 -> 5 -> 2` costs
`2 + 2 = 4`. That is precisely the case BFS gets wrong.

## The 999 trap

`999` means **no edge**, not "an edge costing 999". Forget the guard and you invent
roads: paths appear that should not exist, and the answers come out too small on
exactly the sparse graphs where it matters. Test 4 is a graph with no edges at all,
which fails loudly if you got this wrong.

## Why the greedy choice is safe

When you pick the unfinished vertex `u` with the smallest `dist[u]`, that value is
already final. Any other route to `u` would have to leave the settled set through
some unfinished vertex `x`, and `dist[x] >= dist[u]` by choice of `u` - so that
route is already at least as long before it even arrives.

That argument leans on one thing: **edge weights are non-negative**. With a negative
edge, a longer-looking detour could still reduce the total, and the whole guarantee
collapses. That is why the last problem in this unit needs a completely different
algorithm.

## Complexity

This version is `O(V^2)`: `V` rounds, each doing a linear scan for the minimum. For
a dense matrix that is optimal. You will replace the scan with a heap in problem 4.
""",
)

# --------------------------------------------------------------- p02
H2 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
""" + MATRIX_TYPES + r"""
/* Provided for you - the function you just wrote. */
void dijkstra(int n, int w[MAXV][MAXV], int src, int dist[]);

/* Yours: the time until the LAST location has received supplies,
   or -1 if any location cannot be reached at all. */
int minTotalTime(int n, int w[MAXV][MAXV], int src);

#endif
"""

M2 = r"""
#include <stdio.h>
#include "problem.h"

static int w[MAXV][MAXV];

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &w[i][j]);

    int k;
    if (scanf("%d", &k) != 1) return 0;

    printf("%d\n", minTotalTime(n, w, k - 1));
    return 0;
}
"""

S2 = r"""
#include "problem.h"

int minTotalTime(int n, int w[MAXV][MAXV], int src) {
    int dist[MAXV];
    dijkstra(n, w, src, dist);

    /* TODO: the teams travel concurrently, so the answer is not the sum of the
       distances. Work out which single number over dist[0..n-1] it actually is,
       and return -1 if any vertex is unreachable. */
    return 0;
}
"""

A2 = r"""
#include "problem.h"

int minTotalTime(int n, int w[MAXV][MAXV], int src) {
    int dist[MAXV];
    dijkstra(n, w, src, dist);

    int worst = 0;
    for (int v = 0; v < n; v++) {
        if (dist[v] >= INF) return -1;   /* somewhere never gets supplies */
        if (dist[v] > worst) worst = dist[v];
    }
    return worst;
}
"""

T2 = [
    "5\n0 5 999 999 2\n999 0 1 1 999\n999 999 0 2 9\n999 999 999 0 10\n999 2 7 999 0\n1\n",
    "4\n0 1 999 999\n999 0 1 999\n999 999 0 1\n999 999 999 0\n1\n",
    "3\n0 1 999\n999 0 999\n999 999 0\n1\n",
    "2\n0 7\n7 0\n1\n",
    "5\n0 4 2 999 999\n999 0 999 5 999\n999 1 0 8 10\n999 999 999 0 2\n999 999 999 999 0\n1\n",
    "1\n0\n1\n",
    "6\n0 7 9 999 999 14\n7 0 10 15 999 999\n9 10 0 11 999 2\n999 15 11 0 6 999\n999 999 999 6 0 9\n14 999 2 999 9 0\n1\n",
]

write_problem(
    PACK, UNIT, "p02-min-total-time", title="Minimum total time (the Q2 rule)",
    mode="function", difficulty="easy", estimated_minutes=6, samples=2,
    topics=["dijkstra", "shortest path"],
    prereqs=[f"{PACK}.{UNIT}.p01-dijkstra-matrix"],
    source="Core of NITC_Lab_S3_DSA Week 4 Practice Question 2",
    hints=[
        "The teams all leave at once and travel in parallel. Nobody waits for "
        "anybody else, so the total elapsed time is decided by one location only.",
        "Everything is supplied once the SLOWEST location has been reached - so "
        "the answer is the maximum of dist[], not the sum.",
        "Check reachability before taking the maximum, or an INF entry becomes "
        "your answer. Any unreachable vertex means the whole thing returns -1.",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"dijkstra.c": DIJKSTRA_IMPL},
    statement=r"""
# Minimum total time (the Q2 rule)

Dijkstra is provided. This rung is one short function - and one modelling decision
that is easy to get backwards.

> `n` emergency teams start from location `k` and begin delivering emergency
> supplies to all other locations **concurrently**. Find the minimum total time
> required for all `n` locations to receive supplies. If any location cannot be
> reached, return `-1`.

```c
int minTotalTime(int n, int w[MAXV][MAXV], int src);
```
""" + MATRIX_FORMAT + r"""
## Output

A single integer, or `-1`.

## Example

```
5
0 5 999 999 2
999 0 1 1 999
999 999 0 2 9
999 999 999 0 10
999 2 7 999 0
1
```

```
5
```

The distances are `0 4 5 5 2`.

## The modelling decision

"Total time" sounds like a sum. It is not.

The teams travel **concurrently** - all of them set out at the same moment and none
waits for another. So the job is finished the instant the *last* location receives
its supplies, and the elapsed time is the **largest** of the shortest distances, not
their total.

In the sample, the sum would be 16 and the answer is 5.

## The order of the two checks

Take the maximum of `dist[]` and you will happily return `INF` when some location is
cut off. Test the reachability of every vertex first, return `-1` the moment one
fails, and only then take the maximum over what remains.
""",
)

# --------------------------------------------------------------- p03
A3 = r"""
#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

static int w[MAXV][MAXV];
static int dist[MAXV];
static int done[MAXV];

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &w[i][j]);

    int k;
    if (scanf("%d", &k) != 1) return 0;
    k--;                                  /* the sheet numbers locations from 1 */

    for (int i = 0; i < n; i++) { dist[i] = INF; done[i] = 0; }
    dist[k] = 0;

    for (int iter = 0; iter < n; iter++) {
        int u = -1;
        for (int i = 0; i < n; i++)
            if (!done[i] && (u == -1 || dist[i] < dist[u])) u = i;
        if (u == -1 || dist[u] == INF) break;
        done[u] = 1;

        for (int v = 0; v < n; v++) {
            if (u == v || w[u][v] == NOEDGE) continue;
            if (dist[u] + w[u][v] < dist[v]) dist[v] = dist[u] + w[u][v];
        }
    }

    int worst = 0;
    for (int v = 0; v < n; v++) {
        if (dist[v] >= INF) { printf("-1\n"); return 0; }
        if (dist[v] > worst) worst = dist[v];
    }
    printf("%d\n", worst);
    return 0;
}
"""

S3 = r"""
#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

int main(void) {
    /* TODO: the whole program.
       Read n, the n x n matrix, and k. Remember k is 1-based.
       Run Dijkstra from k-1, then print the largest distance, or -1 if some
       location is unreachable. */
    return 0;
}
"""

T3 = [
    "5\n0 5 999 999 2\n999 0 1 1 999\n999 999 0 2 9\n999 999 999 0 10\n999 2 7 999 0\n1\n",
    "4\n0 1 999 999\n999 0 1 999\n999 999 0 1\n999 999 999 0\n1\n",
    "3\n0 1 999\n999 0 999\n999 999 0\n1\n",
    "5\n0 4 2 999 999\n999 0 999 5 999\n999 1 0 8 10\n999 999 999 0 2\n999 999 999 999 0\n1\n",
    "4\n0 999 999 999\n1 0 999 999\n999 1 0 999\n999 999 1 0\n4\n",
    "1\n0\n1\n",
    "6\n0 7 9 999 999 14\n7 0 10 15 999 999\n9 10 0 11 999 2\n999 15 11 0 6 999\n999 999 999 6 0 9\n14 999 2 999 9 0\n3\n",
    "5\n0 3 999 7 999\n8 0 2 999 999\n5 999 0 1 999\n2 999 999 0 999\n999 999 999 999 0\n1\n",
]

# Near the size limit: n = 100, sparse one-way roads, one connected and one not.
def _big_q2(n, density, connected):
    w = [[0 if i == j else 999 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and rng.random() < density:
                w[i][j] = rng.randint(0, 998)
    if connected:                        # a ring guarantees every city is reachable
        for i in range(n):
            w[i][(i + 1) % n] = rng.randint(1, 998)
    rows = "\n".join(" ".join(map(str, r)) for r in w)
    return f"{n}\n{rows}\n{rng.randint(1, n)}\n"


T3 += [_big_q2(100, 0.06, True), _big_q2(100, 0.02, False)]

write_problem(
    PACK, UNIT, "p03-practice-q2", title="Practice Question 2 (full)",
    mode="program", difficulty="medium", estimated_minutes=20, samples=1,
    topics=["dijkstra", "shortest path"],
    prereqs=[f"{PACK}.{UNIT}.p02-min-total-time"],
    source="NITC_Lab_S3_DSA Week 4 - SSSP, Practice Question 2 (verbatim)",
    hints=[
        "You already wrote both halves in the last two problems. This is assembling "
        "them into one main() plus the input reading.",
        "k arrives 1-based. Decrement it once, right after reading, and then think "
        "purely 0-based for the rest of the program.",
        "Test 5 has a source with no outgoing edges at all except backwards - "
        "make sure your loop terminates cleanly when nothing is reachable.",
    ],
    starter=S3, solution=A3, tests=T3,
    statement=r"""
# Practice Question 2 (full)

Verbatim from the Week 4 sheet.

> There is a network of `n` locations, labeled from 1 to `n`. You are given an
> adjacency matrix `time[n][n]`, where `time[i][j]` represents the time in minutes
> it takes for an emergency rescue team to travel directly from location `i` to
> location `j` along a **one-way** road (`0 <= time[i][j] < 999`). If there is **no
> direct road** from `i` to `j`, `time[i][j]` is equal to 999.
>
> `n` emergency teams start from location `k` and begin delivering emergency
> supplies to all other locations concurrently. Write a program to find the
> **minimum total time** required for all `n` locations to receive supplies from
> location `k`. If any location cannot be reached from `k`, return `-1`.

## Input format

- first line: the number of vertices `n`
- next `n` lines: the adjacency matrix `time[n][n]`
- last line: `k`

## Output format

A single integer: the minimum total time, or `-1`.

## Sample

```
5
0 5 999 999 2
999 0 1 1 999
999 999 0 2 9
999 999 999 0 10
999 2 7 999 0
1
```

```
5
```

## What is actually new here

Very little - and that is the point of having climbed the ladder. You wrote the
Dijkstra in problem 1 and the max-vs-sum rule in problem 2. What remains is reading
the input and remembering that `k` is 1-based while your arrays are not.

Decrement `k` exactly once, immediately after reading it. Doing it later, or twice,
is the classic way to get an answer that is right for a different source vertex.
""",
)

# --------------------------------------------------------------- p04
H4 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define MAXD 105
#define INF 1000000000

/* ---- Weighted adjacency list. Provided, already built. ---- */
typedef struct {
    int n;
    int deg[MAXV];
    int to[MAXV][MAXD];
    int cost[MAXV][MAXD];
} WGraph;

void wgraphInit(WGraph *g, int n);
void wgraphAddEdge(WGraph *g, int u, int v, int c);

/* ---- Min-heap priority queue. Provided - the one you built in unit 03. ---- */
typedef struct { int key; int id; } Item;
typedef struct { Item a[MAXV * MAXD]; int size; } MinHeap;

void heapInit(MinHeap *h);
int  heapEmpty(const MinHeap *h);
void heapInsert(MinHeap *h, int key, int id);
Item heapExtractMin(MinHeap *h);

/* ---- Yours. ---- */
void dijkstraHeap(const WGraph *g, int src, int dist[]);

#endif
"""

E4 = r"""
#include "problem.h"

void wgraphInit(WGraph *g, int n) {
    g->n = n;
    for (int i = 0; i <= n; i++) g->deg[i] = 0;
}

void wgraphAddEdge(WGraph *g, int u, int v, int c) {
    int d = g->deg[u]++;
    g->to[u][d] = v;
    g->cost[u][d] = c;
}

static int before(Item x, Item y) {
    if (x.key != y.key) return x.key < y.key;
    return x.id < y.id;
}

static void swapItems(Item *x, Item *y) { Item t = *x; *x = *y; *y = t; }

void heapInit(MinHeap *h) { h->size = 0; }
int  heapEmpty(const MinHeap *h) { return h->size == 0; }

void heapInsert(MinHeap *h, int key, int id) {
    int i = h->size++;
    h->a[i].key = key;
    h->a[i].id = id;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (!before(h->a[i], h->a[p])) break;
        swapItems(&h->a[i], &h->a[p]);
        i = p;
    }
}

Item heapExtractMin(MinHeap *h) {
    Item root = h->a[0];
    h->a[0] = h->a[--(h->size)];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = 2 * i + 2, best = i;
        if (l < h->size && before(h->a[l], h->a[best])) best = l;
        if (r < h->size && before(h->a[r], h->a[best])) best = r;
        if (best == i) break;
        swapItems(&h->a[i], &h->a[best]);
        i = best;
    }
    return root;
}
"""

M4 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;

    WGraph g;
    wgraphInit(&g, n);
    for (int i = 0; i < m; i++) {
        int u, v, c;
        if (scanf("%d %d %d", &u, &v, &c) != 3) return 0;
        wgraphAddEdge(&g, u, v, c);
    }

    int s;
    if (scanf("%d", &s) != 1) return 0;

    int dist[MAXV];
    dijkstraHeap(&g, s, dist);

    for (int v = 1; v <= n; v++)
        printf("%d%s", dist[v] >= INF ? -1 : dist[v], v < n ? " " : "");
    printf("\n");
    return 0;
}
"""

S4 = r"""
#include "problem.h"

void dijkstraHeap(const WGraph *g, int src, int dist[]) {
    MinHeap h;
    heapInit(&h);

    /* TODO
       1. dist[v] = INF for v in 0..n, then dist[src] = 0
       2. insert (0, src) into the heap
       3. while the heap is not empty:
            - extract the smallest item (key, u)
            - if key > dist[u], this entry is STALE - skip it and continue
            - otherwise relax every edge u->v: if dist[u] + cost < dist[v],
              update dist[v] and insert (dist[v], v)
       There is no decrease-key here. You insert a second, better entry and
       let the stale one be skipped when it surfaces. See the statement. */
}
"""

A4 = r"""
#include "problem.h"

void dijkstraHeap(const WGraph *g, int src, int dist[]) {
    MinHeap h;
    heapInit(&h);

    for (int v = 0; v <= g->n; v++) dist[v] = INF;
    dist[src] = 0;
    heapInsert(&h, 0, src);

    while (!heapEmpty(&h)) {
        Item it = heapExtractMin(&h);
        int u = it.id;

        /* A better route to u was found after this entry was queued. */
        if (it.key > dist[u]) continue;

        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->to[u][i];
            int nd = dist[u] + g->cost[u][i];
            if (nd < dist[v]) {
                dist[v] = nd;
                heapInsert(&h, nd, v);
            }
        }
    }
}
"""

T4 = [
    "5 8\n1 2 5\n1 5 2\n5 2 2\n5 3 7\n2 3 1\n2 4 1\n3 4 2\n4 5 10\n1\n",
    "4 3\n1 2 1\n2 3 1\n3 4 1\n1\n",
    "4 4\n1 2 10\n1 3 1\n3 2 1\n2 4 1\n1\n",
    "5 4\n1 2 3\n2 3 4\n4 5 1\n5 4 1\n1\n",
    "6 9\n1 2 7\n1 3 9\n1 6 14\n2 3 10\n2 4 15\n3 4 11\n3 6 2\n4 5 6\n6 5 9\n1\n",
    "3 3\n1 2 0\n2 3 0\n1 3 5\n1\n",
    "7 10\n1 2 2\n1 3 4\n2 3 1\n2 4 7\n3 5 3\n5 4 2\n4 6 1\n5 6 5\n6 7 2\n3 7 20\n1\n",
]

write_problem(
    PACK, UNIT, "p04-dijkstra-heap", title="Dijkstra with a priority queue",
    mode="function", difficulty="hard", estimated_minutes=18, samples=2,
    topics=["dijkstra", "heap", "priority queue"],
    prereqs=[f"{PACK}.{UNIT}.p01-dijkstra-matrix",
             f"{PACK}.03-heap.p04-min-heap-pq"],
    source="Combines Week 4 SSSP with the Lab 11 priority queue",
    hints=[
        "The structure is the same as the matrix version. The only change is how "
        "you choose the next vertex: extract from the heap instead of scanning.",
        "Whenever you improve dist[v], insert a fresh (dist[v], v) entry. Do not "
        "try to find and modify the old one - just leave it there.",
        "The stale check is one line at the top of the loop: if (it.key > dist[u]) "
        "continue; Without it you re-expand vertices and the work blows up.",
    ],
    header=H4, harness=M4, starter=S4, solution=A4, tests=T4,
    extra={"support.c": E4},
    statement=r"""
# Dijkstra with a priority queue

Same algorithm, better bookkeeping. The `O(V^2)` version spends every round doing a
linear scan to find the closest unfinished vertex. A min-heap answers that question
in `O(log V)`.

```c
void dijkstraHeap(const WGraph *g, int src, int dist[]);
```

The weighted adjacency list and the min-heap from unit 03 are both provided.
Vertices are **1-based** here.

## Input format

```
n m
u1 v1 c1
...
s
```

`m` directed edges `u -> v` of cost `c`. Print `dist[1..n]`, with `-1` for
unreachable.

## Example

```
5 8
1 2 5
1 5 2
5 2 2
5 3 7
2 3 1
2 4 1
3 4 2
4 5 10
1
```

```
0 4 5 5 2
```

Same graph as problem 1, same answers - now via the heap.

## Lazy deletion: the part worth understanding

Textbook Dijkstra calls `decrease-key` when it finds a better route to a vertex
already in the queue. Implementing that needs the heap to track where each vertex
lives, and to fix up those positions on every swap. It is a real amount of code.

The standard trick avoids it entirely. When you improve `dist[v]`, just **insert
another entry** for `v` with the new smaller key, and leave the old one alone. The
heap now holds two entries for `v`; the better one is closer to the top and comes
out first.

When the worse one eventually surfaces, you detect it and throw it away:

```c
if (it.key > dist[u]) continue;   /* stale - a better route was already settled */
```

That single line is what makes the whole approach correct. Without it you re-expand
vertices you already finished, and the running time degrades badly.

The heap can hold up to `E` entries rather than `V`, which is why the complexity is
`O(E log E)` - conventionally written `O(E log V)`, since `E < V^2` makes
`log E < 2 log V`.

## Which version should you actually use

`O(V^2)` wins on dense graphs, where `E` approaches `V^2` and the heap's bookkeeping
is pure overhead. The heap wins on sparse graphs, which is most real ones. Knowing
*why* you would pick either is a standard viva question, and now you have written
both.
""",
)

# --------------------------------------------------------------- p05
A5 = r"""
#include <stdio.h>

#define MAXV 105
#define NOEDGE 999

static int w[MAXV][MAXV];
static long long dist[MAXV];

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            scanf("%d", &w[i][j]);

    /* Every vertex starts at 0, which is equivalent to adding a virtual source
       with a zero-cost edge to each one. That way a negative cycle anywhere in
       the graph is detected, not only ones reachable from a chosen start. */
    for (int i = 0; i < n; i++) dist[i] = 0;

    for (int pass = 0; pass < n - 1; pass++) {
        int changed = 0;
        for (int u = 0; u < n; u++)
            for (int v = 0; v < n; v++) {
                if (u == v || w[u][v] == NOEDGE) continue;
                if (dist[u] + w[u][v] < dist[v]) {
                    dist[v] = dist[u] + w[u][v];
                    changed = 1;
                }
            }
        if (!changed) break;   /* settled early: no negative cycle */
    }

    /* One extra pass: any further improvement proves a negative cycle. */
    for (int u = 0; u < n; u++)
        for (int v = 0; v < n; v++) {
            if (u == v || w[u][v] == NOEDGE) continue;
            if (dist[u] + w[u][v] < dist[v]) {
                printf("1\n");
                return 0;
            }
        }

    printf("-1\n");
    return 0;
}
"""

S5 = r"""
#include <stdio.h>

#define MAXV 105
#define NOEDGE 999

int main(void) {
    /* TODO: Bellman-Ford, used as a detector rather than a distance finder.
       Read n and the matrix, initialise every dist to 0, relax all edges
       n-1 times, then do one more pass. If anything still improves on that
       last pass, print 1. Otherwise print -1. */
    return 0;
}
"""

T5 = [
    "3\n0 -1 999\n999 0 -2\n-2 999 0\n",
    "3\n0 1 999\n999 0 1\n999 999 0\n",
    "4\n0 1 999 999\n999 0 -1 999\n999 999 0 -1\n999 -1 999 0\n",
    "2\n0 5\n5 0\n",
    "4\n0 2 999 999\n999 0 3 999\n999 999 0 4\n999 999 999 0\n",
    "5\n0 1 999 999 999\n999 0 1 999 999\n999 999 0 1 999\n999 999 999 0 1\n999 999 999 999 0\n",
    "3\n0 -1 999\n999 0 -1\n999 999 0\n",
]

# Found by mutation testing.  A chain listed "backwards" (5->4->3->2->1, all -1)
# only settles one edge per pass, so it needs all n-1 passes - stopping one pass
# early makes the check pass report a cycle that is not there.
T5 += ["5\n0 999 999 999 999\n-1 0 999 999 999\n999 -1 0 999 999\n999 999 -1 0 999\n999 999 999 -1 0\n",
       "8\n" + "\n".join(" ".join("0" if i == j else ("-2" if j == i - 1 else "999")
                                  for j in range(8)) for i in range(8)) + "\n",
       # a negative cycle 3 <-> 4 that vertex 1 can never reach
       "4\n0 5 999 999\n999 0 999 999\n999 999 0 -2\n999 999 -2 0\n"]

write_problem(
    PACK, UNIT, "p05-negative-cycle", title="Practice Question 4: detect a negative cycle",
    mode="program", difficulty="hard", estimated_minutes=20, samples=2,
    topics=["bellman-ford", "negative cycle", "shortest path"],
    prereqs=[f"{PACK}.{UNIT}.p01-dijkstra-matrix"],
    source="NITC_Lab_S3_DSA Week 4 - SSSP, Practice Question 4 (optional on the sheet)",
    hints=[
        "Dijkstra cannot be rescued here. Its correctness depends on non-negative "
        "weights, so you need Bellman-Ford, which relaxes every edge repeatedly "
        "instead of committing to a vertex.",
        "Initialise every dist to 0 rather than picking a source. That is the same "
        "as adding an imaginary vertex with a free edge to everywhere, and it makes "
        "cycles in ANY component detectable.",
        "After n-1 full passes all genuine shortest paths have settled. Run one "
        "more pass: if any edge can still be relaxed, a negative cycle exists.",
    ],
    starter=S5, solution=A5, tests=T5,
    statement=r"""
# Practice Question 4: detect a negative cycle

From the Week 4 sheet, marked optional there. It is here because it is the cleanest
possible demonstration of where Dijkstra's guarantee actually comes from.

> Write a program that takes a weighted directed graph in the form of an adjacency
> matrix, and determines whether the graph contains any negative weight cycles.
> `999` is used to represent the absence of a direct edge between two distinct
> vertices (weight of any edge is always less than 999).

## Input format

- first line: the number of vertices `n`
- next `n` lines: the adjacency matrix

## Output format

Print `1` if there is a negative cycle, `-1` otherwise.

## Sample

```
3
0 -1 999
999 0 -2
-2 999 0
```

```
1
```

That cycle `1 -> 2 -> 3 -> 1` costs `-1 + -2 + -2 = -5`. Go round it again and the
total drops another 5. There is no shortest path at all, because there is no bottom.

The diagonal is always `0`: `999` marks a missing edge between two **distinct** vertices, so
there are no self-loops, and any negative cycle passes through at least two vertices.

## Why not Dijkstra

Dijkstra settles a vertex and never reconsiders it, justified by the argument that
no later route could come back cheaper. With a negative edge that argument fails
outright - a detour through a negative edge really can beat the direct route.

**Bellman-Ford** makes no such commitment. It relaxes *every* edge, `n-1` times over.
Since any simple path uses at most `n-1` edges, that is enough passes for every real
shortest path to settle.

## The detection trick

After `n-1` passes, everything that can settle has settled. So run **one more pass**.
If any edge can still be relaxed, the only explanation is a cycle you can keep going
round to lower the total - a negative cycle.

## Why every distance starts at 0

Ordinarily Bellman-Ford starts with `dist[src] = 0` and everything else at infinity.
Here there is no source, and a negative cycle sitting in a component unreachable from
any particular start would be missed.

Setting **every** `dist[v] = 0` is equivalent to adding an imaginary vertex with a
zero-cost edge to every real one. Now every component is reachable, and a negative
cycle anywhere will be found. It costs one line and is the whole reason this version
works on disconnected input.
""",
)

report(UNIT, 5)
