"""Unit 09 - Minimum spanning trees.  Run: python scripts/authoring/unit_09_mst.py"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report

PACK = "c-s3"
UNIT = "09-mst"
rng = random.Random(909)

write_unit(PACK, UNIT, "Minimum spanning trees",
           "Disjoint sets, then Kruskal and Prim, then the two Week 5 questions verbatim - "
           "the wording of each one tells you which algorithm it wants.")


def rand_weighted(nmin=3, nmax=7, density=0.5, connected=True, wmax=60, distinct=True):
    n = rng.randint(nmin, nmax)
    pairs = set()
    if connected:
        for v in range(2, n + 1):
            pairs.add((rng.randint(1, v - 1), v))
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if rng.random() < density:
                pairs.add((u, v))
    pairs = sorted(pairs)
    weights = rng.sample(range(1, wmax), len(pairs)) if distinct else \
        [rng.randint(1, wmax) for _ in pairs]
    edges = [(u, v, w) for (u, v), w in zip(pairs, weights)]
    rng.shuffle(edges)
    return n, edges


def edges_input(n, edges, source=None):
    head = f"{n}\n{len(edges)}\n" + (f"{source}\n" if source is not None else "")
    return head + "".join(f"{u} {v} {w}\n" for u, v, w in edges)


# ------------------------------------------------------------------ p01
H1 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105

/* Disjoint-set forest over 1..n. */
typedef struct {
    int parent[MAXV];
    int rank[MAXV];
} DSU;

void dsuInit(DSU *d, int n);
int  find(DSU *d, int x);            /* representative of x's set, with path compression */
int  unite(DSU *d, int a, int b);    /* 1 if they were separate and got merged, 0 if already together */

#endif
"""

M1 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    DSU d;
    dsuInit(&d, n);

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'u') {
            int a, b;
            if (scanf("%d %d", &a, &b) != 2) break;
            printf(unite(&d, a, b) ? "MERGED\n" : "ALREADY\n");
        } else if (cmd == 'f') {
            int a, b;
            if (scanf("%d %d", &a, &b) != 2) break;
            printf(find(&d, a) == find(&d, b) ? "SAME\n" : "DIFFERENT\n");
        } else if (cmd == 'c') {
            int count = 0;
            for (int v = 1; v <= n; v++) if (find(&d, v) == v) count++;
            printf("%d\n", count);
        }
    }
    return 0;
}
"""

S1 = r"""
#include "problem.h"

void dsuInit(DSU *d, int n) {
    /* TODO: every vertex starts alone - its own parent, rank 0. */
}

int find(DSU *d, int x) {
    /* TODO: follow parent until you reach the representative (parent[x] == x).
       Path compression: on the way back, point x straight at the root.
       The one-liner is:
           if (d->parent[x] != x) d->parent[x] = find(d, d->parent[x]);
           return d->parent[x]; */
    return x;
}

int unite(DSU *d, int a, int b) {
    /* TODO: find both roots; if equal return 0.
       Otherwise attach the SHORTER tree under the taller one (union by rank),
       and if the ranks were equal, bump the new root's rank. Return 1. */
    return 0;
}
"""

A1 = r"""
#include "problem.h"

void dsuInit(DSU *d, int n) {
    for (int v = 0; v <= n; v++) {
        d->parent[v] = v;
        d->rank[v] = 0;
    }
}

int find(DSU *d, int x) {
    if (d->parent[x] != x) d->parent[x] = find(d, d->parent[x]);   /* compress */
    return d->parent[x];
}

int unite(DSU *d, int a, int b) {
    int ra = find(d, a), rb = find(d, b);
    if (ra == rb) return 0;

    if (d->rank[ra] < d->rank[rb]) {
        d->parent[ra] = rb;
    } else if (d->rank[rb] < d->rank[ra]) {
        d->parent[rb] = ra;
    } else {
        d->parent[rb] = ra;
        d->rank[ra]++;
    }
    return 1;
}
"""

T1 = ["6\nf 1 2\nu 1 2\nf 1 2\nu 2 3\nf 1 3\nc\nu 1 3\nu 4 5\nc\nf 4 6\nu 5 6\nf 4 6\nc\ne\n",
      "4\nc\nf 1 1\nu 1 1\nc\ne\n",
      "5\nu 1 2\nu 3 4\nu 2 3\nc\nf 1 4\nf 1 5\nu 4 5\nc\ne\n"]
for _ in range(5):
    n = rng.randint(4, 9)
    lines = [str(n)]
    for _ in range(rng.randint(6, 14)):
        a, b = rng.randint(1, n), rng.randint(1, n)
        lines.append(rng.choice([f"u {a} {b}", f"f {a} {b}", "c"]))
    lines.append("e")
    T1.append("\n".join(lines) + "\n")

write_problem(
    PACK, UNIT, "p01-disjoint-set", title="Disjoint set union (find, unite)",
    mode="function", difficulty="medium", estimated_minutes=12, samples=1,
    topics=["dsu", "union find"],
    source="DSA theory: Kruskal's analysis and implementation using disjoint sets",
    hints=[
        "find walks up parent[] until it reaches a vertex that is its own parent. "
        "That vertex is the set's representative.",
        "Path compression is one line inside find: reassign parent[x] to the root "
        "you just found, so the next lookup is immediate.",
        "unite must compare ROOTS, not the vertices themselves. Attaching "
        "parent[b] = a instead of parent[find(b)] = find(a) silently loses whole sets.",
    ],
    header=H1, harness=M1, starter=S1, solution=A1, tests=T1,
    statement=r"""
# Disjoint set union (find, unite)

The structure that makes Kruskal's algorithm possible: it answers "are these two
vertices already connected?" in almost constant time.

```c
void dsuInit(DSU *d, int n);
int  find(DSU *d, int x);           /* representative of x's set */
int  unite(DSU *d, int a, int b);   /* 1 if merged, 0 if already together */
```

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `u a b` | union | `MERGED` or `ALREADY` |
| `f a b` | same set? | `SAME` or `DIFFERENT` |
| `c` | how many sets remain | a number |
| `e` | exit | nothing |

The first line of input is `n`.

## Example

```
6
f 1 2
u 1 2
f 1 2
u 2 3
f 1 3
c
e
```

```
DIFFERENT
MERGED
SAME
MERGED
SAME
4
```

After merging {1,2,3}, the remaining sets are {1,2,3}, {4}, {5}, {6} - four of them.

## The two optimisations

**Path compression** (in `find`): after finding the root, point `x` directly at it.
Trees stay almost flat.

```c
if (d->parent[x] != x) d->parent[x] = find(d, d->parent[x]);
return d->parent[x];
```

**Union by rank** (in `unite`): hang the shorter tree under the taller one, so the
result never gets deeper than necessary. `rank` is an upper bound on height; it only
increases when you join two trees of equal rank.

Together they give near-`O(1)` amortised operations. With `n <= 100` you would survive
without either, but they are three lines each and they are what the theory syllabus
means by "implementation using disjoint set data structure".

## The mistake to avoid

`unite` must work on the **roots**:

```c
int ra = find(d, a), rb = find(d, b);   /* then join ra and rb */
```

Writing `d->parent[b] = a` joins two individual vertices and orphans everything else
that was in their sets. It passes small tests and fails the moment three things merge.
""",
)

# ------------------------------------------------------------------ p02
H2 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define MAXE 10005

typedef struct { int u, v, w; } Edge;

/* ---- Provided: the DSU you just wrote. ---- */
typedef struct { int parent[MAXV]; int rank[MAXV]; } DSU;
void dsuInit(DSU *d, int n);
int  find(DSU *d, int x);
int  unite(DSU *d, int a, int b);

/* ---- Yours: total weight of a minimum spanning tree, or -1 if the graph
        cannot be connected.  edges[] may be reordered. ---- */
int kruskal(int n, Edge edges[], int m);

#endif
"""

DSU_IMPL = r"""
#include "problem.h"

void dsuInit(DSU *d, int n) {
    for (int v = 0; v <= n; v++) { d->parent[v] = v; d->rank[v] = 0; }
}

int find(DSU *d, int x) {
    if (d->parent[x] != x) d->parent[x] = find(d, d->parent[x]);
    return d->parent[x];
}

int unite(DSU *d, int a, int b) {
    int ra = find(d, a), rb = find(d, b);
    if (ra == rb) return 0;
    if (d->rank[ra] < d->rank[rb]) d->parent[ra] = rb;
    else if (d->rank[rb] < d->rank[ra]) d->parent[rb] = ra;
    else { d->parent[rb] = ra; d->rank[ra]++; }
    return 1;
}
"""

M2 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    static Edge edges[MAXE];
    for (int i = 0; i < m; i++)
        if (scanf("%d %d %d", &edges[i].u, &edges[i].v, &edges[i].w) != 3) return 0;

    printf("%d\n", kruskal(n, edges, m));
    return 0;
}
"""

S2 = r"""
#include <stdlib.h>
#include "problem.h"

static int cmpEdge(const void *a, const void *b) {
    /* TODO: order by weight, ascending. Return negative / zero / positive -
       NOT a true/false comparison like C++ needs. */
    return 0;
}

int kruskal(int n, Edge edges[], int m) {
    /* TODO
       1. qsort the edges by weight
       2. dsuInit
       3. for each edge in order: if unite(u, v) succeeds it does not close a
          cycle - add its weight and count it
       4. a spanning tree needs exactly n-1 edges; if you took fewer, the graph
          was disconnected -> return -1 */
    return -1;
}
"""

A2 = r"""
#include <stdlib.h>
#include "problem.h"

static int cmpEdge(const void *a, const void *b) {
    const Edge *x = a, *y = b;
    return (x->w > y->w) - (x->w < y->w);
}

int kruskal(int n, Edge edges[], int m) {
    qsort(edges, m, sizeof(Edge), cmpEdge);

    DSU d;
    dsuInit(&d, n);

    int taken = 0, cost = 0;
    for (int i = 0; i < m && taken < n - 1; i++) {
        if (unite(&d, edges[i].u, edges[i].v)) {   /* no cycle created */
            cost += edges[i].w;
            taken++;
        }
    }
    return (taken == n - 1) ? cost : -1;
}
"""

T2 = ["5 7\n1 2 4\n1 3 2\n2 3 1\n2 4 5\n3 4 8\n3 5 11\n4 5 7\n",
      "4 2\n1 2 3\n3 4 5\n",
      "1 0\n",
      "3 3\n1 2 1\n2 3 1\n1 3 1\n",
      "6 9\n1 2 3\n1 3 1\n2 3 7\n2 4 5\n3 4 4\n3 5 6\n4 5 2\n4 6 8\n5 6 9\n"]
T2 += [edges_input(*rand_weighted(3, 8)).replace("\n", " ", 1).replace(" ", "\n", 0) for _ in range(0)]
for _ in range(5):
    n, edges = rand_weighted(3, 8, connected=rng.random() < 0.75)
    T2.append(f"{n} {len(edges)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))

write_problem(
    PACK, UNIT, "p02-kruskal-cost", title="Kruskal: total MST cost",
    mode="function", difficulty="medium", estimated_minutes=12, samples=2,
    topics=["mst", "kruskal", "dsu", "greedy"],
    prereqs=[f"{PACK}.{UNIT}.p01-disjoint-set"],
    source="DSA theory: Kruskal's algorithm",
    hints=[
        "Sort the edges by weight, then walk them in order taking any edge whose "
        "endpoints are in different sets.",
        "unite() already returns whether the edge was safe to take - 1 means it "
        "joined two different components, 0 means it would have closed a cycle.",
        "Count the edges you take. A connected graph on n vertices needs exactly "
        "n-1; anything less means the graph was disconnected, so return -1.",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"dsu.c": DSU_IMPL},
    statement=r"""
# Kruskal: total MST cost

```c
int kruskal(int n, Edge edges[], int m);   /* total weight, or -1 */
```

## Input format

```
n m
u1 v1 w1
...
```

`m` undirected weighted edges. Print the MST's total weight, or `-1` if the graph
cannot be connected.

## Example

```
5 7
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 11
4 5 7
```

```
15
```

## The algorithm in four lines

1. Sort the edges by weight.
2. Walk them cheapest-first.
3. Take an edge if its two endpoints are in **different** components (that is exactly
   what `unite` returning 1 means); skip it otherwise, because it would close a cycle.
4. Stop at `n-1` edges.

## The `-1` test

A spanning tree on `n` vertices has exactly `n-1` edges. If you run out of edges with
fewer than that, some vertices were never reachable. So the disconnection test is just
`taken == n - 1` - no separate connectivity check needed.

## The qsort comparator

C++ comparators return "is a before b?". `qsort` wants negative / zero / positive:

```c
return (x->w > y->w) - (x->w < y->w);
```

`return x->w - y->w;` also works for small weights but overflows for large ones - get
into the habit of the safe form.
""",
)

# ------------------------------------------------------------------ p03
H3 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105
#define NOEDGE 0        /* w[u][v] == 0 means there is no edge (weights are >= 1) */

/* ---- Yours: grow an MST outward from src.
        parent[v] = the vertex v was attached from, or -1 for src / unreachable.
        Return the total weight, or -1 if some vertex is unreachable. ---- */
int prim(int n, int w[MAXV][MAXV], int src, int parent[]);

#endif
"""

M3 = r"""
#include <stdio.h>
#include "problem.h"

static int w[MAXV][MAXV];

int main(void) {
    int n, m, s;
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;
    for (int i = 0; i < m; i++) {
        int u, v, x;
        if (scanf("%d %d %d", &u, &v, &x) != 3) return 0;
        w[u][v] = w[v][u] = x;
    }

    int parent[MAXV];
    int cost = prim(n, w, s, parent);
    printf("%d\n", cost);
    if (cost >= 0)
        for (int v = 1; v <= n; v++) printf("%d%s", parent[v], v < n ? " " : "");
    printf("\n");
    return 0;
}
"""

S3 = r"""
#include "problem.h"

int prim(int n, int w[MAXV][MAXV], int src, int parent[]) {
    int key[MAXV], done[MAXV];
    const int INF = 1000000000;

    /* TODO
       1. key[v] = INF, done[v] = 0, parent[v] = -1 for all v; key[src] = 0
       2. repeat n times:
            pick the unfinished vertex u with the smallest key
            if none is reachable (key is still INF) -> return -1
            mark u done, add key[u] to the total
            for every neighbour v with an edge: if !done[v] and w[u][v] < key[v],
                key[v] = w[u][v]; parent[v] = u;
       3. return the total
       Note the difference from Dijkstra: key[v] is the weight of ONE edge, not
       the distance from the source. */
    return -1;
}
"""

A3 = r"""
#include "problem.h"

int prim(int n, int w[MAXV][MAXV], int src, int parent[]) {
    int key[MAXV], done[MAXV];
    const int INF = 1000000000;

    for (int v = 0; v <= n; v++) { key[v] = INF; done[v] = 0; parent[v] = -1; }
    key[src] = 0;

    int total = 0;
    for (int step = 0; step < n; step++) {
        int u = -1;
        for (int v = 1; v <= n; v++)
            if (!done[v] && (u == -1 || key[v] < key[u])) u = v;

        if (u == -1 || key[u] == INF) return -1;   /* unreachable vertex left */
        done[u] = 1;
        total += key[u];

        for (int v = 1; v <= n; v++) {
            if (done[v] || w[u][v] == NOEDGE) continue;
            if (w[u][v] < key[v]) {                /* one edge, not a distance */
                key[v] = w[u][v];
                parent[v] = u;
            }
        }
    }
    return total;
}
"""

T3 = ["5 7 1\n1 2 4\n1 3 2\n2 3 1\n2 4 5\n3 4 8\n3 5 10\n4 5 7\n",
      "4 2 1\n1 2 3\n3 4 5\n",
      "1 0 1\n",
      "5 7 3\n1 2 4\n1 3 2\n2 3 1\n2 4 5\n3 4 8\n3 5 10\n4 5 7\n",
      "3 3 2\n1 2 5\n2 3 3\n1 3 4\n"]
for _ in range(5):
    n, edges = rand_weighted(3, 8, connected=rng.random() < 0.75)
    T3.append(f"{n} {len(edges)} {rng.randint(1, n)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))

write_problem(
    PACK, UNIT, "p03-prim-matrix", title="Prim: grow the tree from a source",
    mode="function", difficulty="medium", estimated_minutes=15, samples=2,
    topics=["mst", "prim", "greedy"],
    prereqs=[f"{PACK}.05-dijkstra.p01-dijkstra-matrix"],
    source="DSA theory: Prim's algorithm; Week 5 Q1",
    hints=[
        "The skeleton is Dijkstra's: pick the closest unfinished vertex, mark it "
        "done, relax its neighbours. Only the relaxation changes.",
        "key[v] holds the weight of the single cheapest edge connecting v to the "
        "tree so far - NOT the distance from the source. So the update is "
        "'if (w[u][v] < key[v])', with no key[u] + ... in it.",
        "Record parent[v] = u whenever you improve key[v]; those n-1 parent links "
        "are the tree.",
    ],
    header=H3, harness=M3, starter=S3, solution=A3, tests=T3,
    statement=r"""
# Prim: grow the tree from a source

```c
int prim(int n, int w[MAXV][MAXV], int src, int parent[]);
```

Start from `src` and repeatedly attach the cheapest edge that reaches a new vertex.
Return the total weight, or `-1` if some vertex cannot be reached.

## Input format

```
n m s
u1 v1 w1
...
```

Undirected weighted edges; `w[u][v] == 0` means no edge. Print the cost on one line,
then `parent[1..n]` (with `-1` for the source).

## Example

```
5 7 1
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 10
4 5 7
```

```
15
-1 3 1 2 4
```

## Prim vs Dijkstra: one character of difference

The loops are identical - pick the smallest-key unfinished vertex, mark it done, then
update its neighbours. The update is where they diverge:

| | update |
|---|---|
| Dijkstra | `if (dist[u] + w[u][v] < dist[v])` - distance from the source |
| Prim | `if (w[u][v] < key[v])` - weight of one edge |

Dijkstra accumulates a path length; Prim only cares how cheaply `v` can be hooked onto
the tree that exists so far. Writing `key[u] + w[u][v]` by reflex gives you a shortest
path tree, which is a different tree, and often a more expensive one.

## Why greedy is safe here

The **cut property**: for any split of the vertices into "in the tree" and "not in the
tree", the cheapest edge crossing that split belongs to some MST. Prim picks exactly
that edge every round.
""",
)

# ------------------------------------------------------------------ p04 (Week 5 Q1)
A4 = r"""
#include <stdio.h>

#define MAXV 105
#define INF 1000000000

static int w[MAXV][MAXV];
static int tree[MAXV][MAXV];
static int key[MAXV], parent[MAXV], done_[MAXV];

int main(void) {
    int n, m, s;
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;

    for (int i = 1; i <= n; i++) {
        key[i] = INF; parent[i] = -1; done_[i] = 0;
        for (int j = 1; j <= n; j++) tree[i][j] = (i == j) ? 0 : -1;
    }
    for (int i = 0; i < m; i++) {
        int u, v, x;
        if (scanf("%d %d %d", &u, &v, &x) != 3) return 0;
        w[u][v] = w[v][u] = x;
    }

    key[s] = 0;
    for (int step = 0; step < n; step++) {
        int u = -1;
        for (int v = 1; v <= n; v++)
            if (!done_[v] && (u == -1 || key[v] < key[u])) u = v;

        if (u == -1 || key[u] == INF) { printf("-1\n"); return 0; }
        done_[u] = 1;

        for (int v = 1; v <= n; v++) {
            if (done_[v] || w[u][v] == 0) continue;
            if (w[u][v] < key[v]) { key[v] = w[u][v]; parent[v] = u; }
        }
    }

    int cost = 0;
    for (int v = 1; v <= n; v++) {
        if (v == s) continue;
        int u = parent[v];
        if (u == -1) { printf("-1\n"); return 0; }
        tree[u][v] = tree[v][u] = w[u][v];
        cost += w[u][v];
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) printf("%d ", tree[i][j]);
        printf("\n");
    }
    printf("%d\n", cost);
    return 0;
}
"""

S4 = r"""
#include <stdio.h>

#define MAXV 105
#define INF 1000000000

int main(void) {
    /* TODO: read n, m, s then the m edges.
       Run Prim from s. Print the MST as an n x n adjacency matrix where
       tree[i][i] = 0, tree[u][v] = w for a chosen edge, and -1 otherwise.
       Then print the total cost. Print -1 alone if some vertex is unreachable. */
    return 0;
}
"""

T4 = ["5\n7\n1\n1 2 4\n1 3 2\n2 3 1\n2 4 5\n3 4 8\n3 5 10\n4 5 7\n",
      "4\n2\n1\n1 2 3\n3 4 5\n",
      "1\n0\n1\n",
      "5\n7\n4\n1 2 4\n1 3 2\n2 3 1\n2 4 5\n3 4 8\n3 5 10\n4 5 7\n",
      "3\n3\n2\n1 2 5\n2 3 3\n1 3 4\n",
      "6\n9\n1\n1 2 3\n1 3 1\n2 3 7\n2 4 5\n3 4 4\n3 5 6\n4 5 2\n4 6 8\n5 6 9\n"]
for _ in range(4):
    n, edges = rand_weighted(3, 7, connected=rng.random() < 0.8)
    T4.append(edges_input(n, edges, source=rng.randint(1, n)))

write_problem(
    PACK, UNIT, "p04-week5-q1-prim", title="Week 5 Q1: Emergency Communication Network (Prim)",
    mode="program", difficulty="hard", estimated_minutes=30, samples=1,
    topics=["mst", "prim", "matrix output"],
    prereqs=[f"{PACK}.{UNIT}.p03-prim-matrix"],
    source="NITC_Lab_S3_DSA Week 5 - MST, Q1 (verbatim; test 1 is the official sample)",
    hints=[
        "The phrase 'must be built starting from this center s' is what forces Prim "
        "rather than Kruskal.",
        "Keep two matrices: the input weights, and a separate output matrix "
        "initialised to 0 on the diagonal and -1 everywhere else.",
        "Fill the output matrix from parent[]: for every v except s, "
        "tree[parent[v]][v] = tree[v][parent[v]] = w. If any parent is still -1, "
        "that vertex was unreachable - print -1 and nothing else.",
    ],
    starter=S4, solution=A4, tests=T4,
    statement=r"""
# Week 5 Q1: Emergency Communication Network (Prim)

Verbatim from the Week 5 sheet.

> A disaster-management authority needs to establish a temporary communication network
> among `n` emergency response centers... The authority wants to connect all response
> centers with the minimum possible total cost, without creating unnecessary cycles. A
> fixed starting center `s` is given. **The network must be built starting from this
> center.** All link costs are positive and distinct.
>
> After constructing the complete minimum-cost spanning tree, display the final tree and
> its total cost. If all vertices cannot be reached from the given source, print `-1`.

## Input format

```
n
m
s
u1 v1 w1
...
```

Constraints: `1 <= n <= 100`, `1 <= w <= 1000`, `u != v`.

## Output format

The MST as an `n x n` adjacency matrix - `0` on the diagonal, the weight for a chosen
edge, `-1` where there is none - then the total cost. If the graph is not connected,
print `-1` and nothing else.

## Sample

```
5
7
1
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 10
4 5 7
```

```
0 -1 2 -1 -1
-1 0 1 5 -1
2 1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
15
```

## Which algorithm, and does it matter?

"Must be built starting from this center" is Prim's wording, and Q2 is the Kruskal
one - the pair is deliberate, so use the one each question describes.

A useful thing to notice: **all weights are positive and distinct, so the MST is
unique.** That means Prim-from-`s` and Kruskal produce the *same* tree here, and since
this question prints no intermediate states, `s` only really affects the reachability
test. If you run out of time, a Kruskal you remember beats a Prim you half-remember.

Also, because the graph is undirected, "reachable from `s`" is the same as "the graph
is connected", so both questions' `-1` cases reduce to the same check: did you manage
to add exactly `n-1` edges?

## The output matrix is separate

Do not overwrite the input weights. Keep `tree[][]` initialised to `0` on the diagonal
and `-1` elsewhere, and fill in only the `n-1` chosen edges, in **both** directions.
""",
)

# ------------------------------------------------------------------ p05 (Week 5 Q2)
A5 = r"""
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
"""

S5 = r"""
#include <stdio.h>
#include <stdlib.h>

#define MAXV 105
#define MAXE 10005

typedef struct { int u, v, w; } Edge;

int main(void) {
    /* TODO: Kruskal, printing the whole n x n matrix after every ACCEPTED edge,
       then the finished matrix once more, then the cost.
       Rejected edges (the ones that would make a cycle) print nothing. */
    return 0;
}
"""

T5 = ["5 7\n1 2 4\n1 3 2\n2 3 1\n2 4 5\n3 4 8\n3 5 11\n4 5 7\n",
      "4 5\n1 2 1\n2 3 2\n3 4 3\n1 4 10\n1 3 4\n",
      "4 2\n1 2 3\n3 4 5\n",
      "1 0\n",
      "3 3\n1 2 5\n2 3 3\n1 3 4\n"]
for _ in range(4):
    n, edges = rand_weighted(3, 6, connected=rng.random() < 0.8)
    T5.append(f"{n} {len(edges)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges))

write_problem(
    PACK, UNIT, "p05-week5-q2-kruskal", title="Week 5 Q2: Rural Power Distribution (Kruskal, step by step)",
    mode="program", difficulty="hard", estimated_minutes=30, samples=1,
    topics=["mst", "kruskal", "dsu", "matrix output"],
    prereqs=[f"{PACK}.{UNIT}.p02-kruskal-cost"],
    source="NITC_Lab_S3_DSA Week 5 - MST, Q2 (verbatim; test 1 is the official sample)",
    hints=[
        "Print the matrix only after an edge is ACCEPTED. An edge you reject for "
        "making a cycle produces no output at all.",
        "The finished tree is printed twice: once as the last accepted-edge "
        "snapshot, and once more at the end before the cost. That is what the "
        "official sample shows.",
        "Disconnected input prints a single -1 and no matrices at all - so decide "
        "connectivity before printing anything, or buffer the snapshots.",
    ],
    starter=S5, solution=A5, tests=T5,
    statement=r"""
# Week 5 Q2: Rural Power Distribution (Kruskal, step by step)

Verbatim from the Week 5 sheet.

> ...Construct the minimum-cost spanning tree by **repeatedly selecting the available
> edge with the smallest weight that does not create a cycle** with the already
> selected edges. **After adding each selected edge, display the current partial tree
> as a weighted adjacency matrix.** Continue until all `n` vertices are connected.
> After constructing the complete minimum-cost spanning tree, display the final tree
> and its total cost. If all vertices cannot be connected, print `-1`.

## Input format

```
n
m
u1 v1 w1
...
```

Note there is **no source vertex** here - that absence, plus "repeatedly selecting the
smallest available edge", is what tells you this one is Kruskal.

## Output format

After each accepted edge, the full `n x n` matrix (`0` diagonal, weight for a selected
edge, `-1` otherwise). Then the final matrix again, then the total cost. `-1` alone if
the graph cannot be connected.

## Sample

```
5
7
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 11
4 5 7
```

```
0 -1 -1 -1 -1
-1 0 1 -1 -1
-1 1 0 -1 -1
-1 -1 -1 0 -1
-1 -1 -1 -1 0
0 -1 2 -1 -1
-1 0 1 -1 -1
2 1 0 -1 -1
-1 -1 -1 0 -1
-1 -1 -1 -1 0
0 -1 2 -1 -1
-1 0 1 5 -1
2 1 0 -1 -1
-1 5 -1 0 -1
-1 -1 -1 -1 0
0 -1 2 -1 -1
-1 0 1 5 -1
2 1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
0 -1 2 -1 -1
-1 0 1 5 -1
2 1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
15
```

Four accepted edges produce four matrices, then the final tree is printed a fifth time
before the cost. **No blank lines between matrices** - that is how the official sample
prints it.

> Note: the hand-written expected outputs sitting in your `Week 5 - MST/tests/` folder
> separate the matrices with blank lines. The assignment sheet does not. The tests here
> follow the sheet.

## Rejected edges print nothing

Edge `3 4 8` closes a cycle, so it is skipped silently - no matrix for it. Only the
`n-1` accepted edges produce output.

## Watch the disconnected case

If the graph cannot be connected the expected output here is a single `-1` with **no
matrices before it**. But you only discover the failure *after* processing every edge,
by which time a naive loop has already printed several snapshots.

So either run Kruskal twice (once silently to check that you can take `n-1` edges, then
again to print), or buffer the snapshots and flush them only on success. The reference
does the two-pass version.

> This is a genuine ambiguity in the sheet, and worth knowing you have a choice to
> defend. Your own Week 5 program prints the snapshots and *then* `-1`; the
> `q2_disconnected.out` file sitting next to it contains only `-1`. The sheet says
> "If all vertices cannot be connected, print -1", so these tests follow the sheet and
> your stored expected output, not your program. If your evaluator wanted the other
> behaviour, the only change is dropping the first pass.
""",
)

report(UNIT, 5)
