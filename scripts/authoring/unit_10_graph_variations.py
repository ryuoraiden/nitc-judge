"""Unit 10 - Graph modification questions.  Run: python scripts/authoring/unit_10_graph_variations.py

The NITC lab never asks the textbook algorithm straight; every question is the
algorithm plus a twist.  This unit is those twists, plus the algorithms from the
theory syllabus the lab has not asked yet (Bellman-Ford, Floyd-Warshall, heap Prim).
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report

PACK = "c-s3"
UNIT = "10-graph-variations"
rng = random.Random(1010)
INF = 10 ** 9

write_unit(PACK, UNIT, "Graph modification questions",
           "Standard algorithm plus a twist, the way the lab asks: Dijkstra's shortest-path "
           "tree, Prim with blocked edges, Bellman-Ford, Floyd-Warshall, heap Prim, and "
           "counting shortest paths.")


# ----------------------------------------------------------------- python models
def py_dijkstra(n, w, s):
    """w: dict (u,v)->weight, 1-based.  Returns dist list (INF unreachable)."""
    dist = [INF] * (n + 1)
    done = [False] * (n + 1)
    dist[s] = 0
    for _ in range(n):
        u = -1
        for v in range(1, n + 1):
            if not done[v] and (u == -1 or dist[v] < dist[u]):
                u = v
        if u == -1 or dist[u] >= INF:
            break
        done[u] = True
        for (a, b), c in w.items():
            if a == u and dist[u] + c < dist[b]:
                dist[b] = dist[u] + c
    return dist


def unique_spt(n, w, s):
    """True if every reachable vertex has exactly one shortest-path predecessor."""
    dist = py_dijkstra(n, w, s)
    for v in range(1, n + 1):
        if v == s or dist[v] >= INF:
            continue
        preds = [u for (u, b), c in w.items() if b == v and dist[u] < INF and dist[u] + c == dist[v]]
        if len(preds) != 1:
            return False
    return True


def matrix_input(n, w, extra_lines=()):
    rows = []
    for i in range(1, n + 1):
        rows.append(" ".join(str(0 if i == j else w.get((i, j), 999)) for j in range(1, n + 1)))
    return f"{n}\n" + "\n".join(rows) + "\n" + "".join(f"{x}\n" for x in extra_lines)


def rand_directed(nmin, nmax, density, lo, hi):
    n = rng.randint(nmin, nmax)
    w = {}
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            if u != v and rng.random() < density:
                w[(u, v)] = rng.randint(lo, hi)
    return n, w


# ================================================================= p01 Dijkstra SPT matrix (MQ4)
A1 = r"""
#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

static int w[MAXV][MAXV], tree[MAXV][MAXV];
static int dist[MAXV], parent[MAXV], done_[MAXV], children[MAXV];

int main(void) {
    int n, s;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) scanf("%d", &w[i][j]);
    if (scanf("%d", &s) != 1) return 0;

    for (int i = 1; i <= n; i++) {
        dist[i] = INF; parent[i] = -1; done_[i] = 0; children[i] = 0;
        for (int j = 1; j <= n; j++) tree[i][j] = (i == j) ? 0 : -1;
    }
    dist[s] = 0;

    for (int step = 0; step < n; step++) {
        int u = -1;
        for (int v = 1; v <= n; v++)
            if (!done_[v] && (u == -1 || dist[v] < dist[u])) u = v;
        if (u == -1 || dist[u] == INF) break;
        done_[u] = 1;

        for (int v = 1; v <= n; v++) {
            if (u == v || w[u][v] == NOEDGE) continue;   /* 0 off the diagonal IS a road */
            if (dist[u] + w[u][v] < dist[v]) {
                dist[v] = dist[u] + w[u][v];
                parent[v] = u;              /* the one extra line vs plain Dijkstra */
            }
        }
    }

    /* Each vertex except s contributes exactly one tree edge, parent -> child. */
    for (int v = 1; v <= n; v++)
        if (parent[v] != -1) {
            tree[parent[v]][v] = w[parent[v]][v];
            children[parent[v]]++;
        }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) printf("%d ", tree[i][j]);
        printf("\n");
    }

    /* A leaf is a vertex with no children - but never the depot itself: a root
       with a single child is not a "leaf-end destination". */
    int leaves = 0;
    for (int v = 1; v <= n; v++)
        if (v != s && children[v] == 0) leaves++;
    printf("%d\n", leaves);
    return 0;
}
"""

S1 = r"""
#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

int main(void) {
    /* TODO
       1. read n, the n x n distance matrix (999 = no road), and s (1-based)
       2. ordinary O(V^2) Dijkstra from s - but whenever you improve dist[v]
          through u, also record parent[v] = u
       3. output matrix: 0 on the diagonal, -1 everywhere else, then
          tree[parent[v]][v] = dist-matrix weight for every v with a parent
       4. print it, then the number of leaves: vertices other than s that are
          nobody's parent */
    return 0;
}
"""


def spt_ok(n, w, s):
    """The sheet guarantees: everything reachable, and a unique shortest path."""
    d = py_dijkstra(n, w, s)
    return all(x < INF for x in d[1:]) and unique_spt(n, w, s)


def symmetric(n, density, lo, hi):
    """Undirected roads, like the official sample: dist[i][j] == dist[j][i]."""
    w = {}
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if rng.random() < density:
                w[(u, v)] = w[(v, u)] = rng.randint(lo, hi)
    return w


MQ4_SAMPLE = "5\n0 4 2 999 999\n4 0 1 5 999\n2 1 0 8 10\n999 5 8 0 2\n999 999 10 2 0\n1\n"

T1 = [MQ4_SAMPLE,
      # star: every other city is its own leaf
      matrix_input(5, {(1, v): v for v in range(2, 6)} | {(v, 1): v for v in range(2, 6)}, [1]),
      # a path: exactly one leaf, even though the depot has degree 1
      matrix_input(4, {(1, 2): 3, (2, 1): 3, (2, 3): 3, (3, 2): 3, (3, 4): 3, (4, 3): 3}, [1]),
      # depot in the middle of a path: two leaves, one on each side
      matrix_input(5, {(1, 2): 1, (2, 1): 1, (2, 3): 1, (3, 2): 1, (3, 4): 1, (4, 3): 1,
                       (4, 5): 1, (5, 4): 1}, [3]),
      # zero-weight roads are real roads, not "the diagonal"
      matrix_input(4, {(1, 2): 0, (2, 1): 0, (2, 3): 5, (3, 2): 5, (1, 4): 2, (4, 1): 2}, [1]),
      # a direct road that loses to a two-hop route
      matrix_input(3, {(1, 2): 10, (2, 1): 10, (1, 3): 1, (3, 1): 1, (3, 2): 2, (2, 3): 2}, [1]),
      matrix_input(2, {(1, 2): 7, (2, 1): 7}, [2])]

# branching random trees, mostly symmetric like the sheet, a few one-way
while len(T1) < 15:
    n = rng.randint(5, 10)
    w = symmetric(n, 0.45, 0, 40) if len(T1) % 4 else rand_directed(n, n, 0.45, 0, 40)[1]
    s = rng.randint(1, n)
    if spt_ok(n, w, s):
        T1.append(matrix_input(n, w, [s]))

# near the sheet's size limits
while len(T1) < 17:
    n = 100 if len(T1) == 15 else 60
    w = symmetric(n, 0.08, 1, 998)
    s = rng.randint(1, n)
    if spt_ok(n, w, s):
        T1.append(matrix_input(n, w, [s]))

write_problem(
    PACK, UNIT, "p01-dijkstra-spt-matrix", title="Week 4 modification (MQ4): shortest-path tree + leaf count",
    mode="program", difficulty="hard", estimated_minutes=30, samples=1,
    topics=["dijkstra", "shortest path tree", "matrix output"],
    prereqs=[f"{PACK}.05-dijkstra.p01-dijkstra-matrix"],
    source="NITC_Lab_S3_DSA Week 4 - SSSP/MQ4.pdf (official statement; test 1 is the official sample)",
    run={"timeout_ms": 3000, "output_cap_kb": 1024},
    hints=[
        "The whole tree is one extra line inside Dijkstra: when dist[u] + w[u][v] "
        "beats dist[v], also set parent[v] = u.",
        "Write each tree edge in ONE direction only, parent -> child: "
        "tree[parent[v]][v]. The official sample's matrix is not symmetric even "
        "though its roads are.",
        "Leaves = vertices other than s that are nobody's parent. Count children "
        "with children[parent[v]]++. Do not count s: in the official sample the "
        "depot has a single child and the answer is still 1.",
    ],
    starter=S1, solution=A1, tests=T1,
    statement=r"""
# Week 4 modification (MQ4): shortest-path tree + leaf count

**Official statement** - `Week 4 - SSSP/MQ4.pdf`. Test 1 is the sheet's sample.

> You are working as a Logistics Coordinator for a central fleet management system. Your
> primary responsibility is to dispatch delivery trucks from a central depot located in
> one city to `n - 1` other regional cities...
>
> To ensure cost efficiency, you need to construct a **Shortest Path Tree (SPT)** rooted
> at the central depot. The road network is structured such that **all cities are
> reachable** from the central depot and there is **exactly one unique shortest path**
> from the central depot to every other reachable city (distance between any two cities
> is less than 999).
>
> Your task is to:
>
> 1. Construct the optimal path tree and represent it as an `n x n` adjacency matrix
>    (where an edge exists with its edge weight only if it forms part of the Shortest
>    Path Tree, and `-1` otherwise).
> 2. Calculate the minimum number of vehicles required to cover all leaf-end
>    destinations simultaneously without overlapping terminal routes, which is **the
>    total number of leaf nodes** in the generated Shortest Path Tree.

## Input format

- first line: `n` (`n >= 2`), cities numbered `1..n`
- next `n` lines: the distance matrix, `0 <= dist[i][j] < 999`; `999` means no direct
  road between distinct cities
- last line: the depot `s`

## Output format

`n` lines: the SPT adjacency matrix (`-1` for edges not in the tree). Then one line:
the minimum number of vehicles needed.

## Sample

```
5
0 4 2 999 999
4 0 1 5 999
2 1 0 8 10
999 5 8 0 2
999 999 10 2 0
1
```

```
0 -1 2 -1 -1
-1 0 -1 5 -1
-1 1 0 -1 -1
-1 -1 -1 0 2
-1 -1 -1 -1 0
1
```

The tree is the chain `1 -> 3 -> 2 -> 4 -> 5`, so there is exactly one leaf-end
destination and one vehicle suffices.

## Three details the sample decides for you

**The matrix is directed.** The roads are two-way, yet row 1 has `2` at column 3 while
row 3 has `-1` at column 1. Each tree edge is written once, from parent to child:
`tree[parent[v]][v]`. Filling in both directions, as you would for an MST, turns this
answer wrong.

**The diagonal prints `0`, not `-1`.**

**The depot is never a leaf.** In the sample, city 1 has just one tree neighbour. Count
"vertices that are nobody's parent" and it drops out naturally; count "vertices with
one tree edge" and you get 2 instead of 1.

## Zero is a real distance

`0 <= dist[i][j]`, so a `0` **off** the diagonal is a road of length zero. Skip only
`999` and `i == j`. Test 5 has one, and treating it as "no road" changes the tree.

## Why the tree is just `parent[]`

Every shortest path from `s` is a shortest path to some earlier city plus one road.
So if every city remembers which city it was reached from, those links form a tree
rooted at `s`. Record it at the only moment it can change:

```c
if (dist[u] + w[u][v] < dist[v]) {
    dist[v] = dist[u] + w[u][v];
    parent[v] = u;
}
```

The sheet's uniqueness guarantee means `<` versus `<=` does not matter here. Without
that guarantee, the two produce different (equally valid) trees.

## Not a minimum spanning tree

It looks just like the Week 5 output, but it is a different tree. The SPT minimises each
city's distance from the depot. The MST minimises the total road length. Read which one
a question means.
""",
)

# ================================================================= p02 count shortest paths
WG_H = r"""
#define MAXV 105
#define MAXD 105
#define INF 1000000000

/* Weighted adjacency list over 1..n.  Provided and already built. */
typedef struct {
    int n;
    int deg[MAXV];
    int to[MAXV][MAXD];
    int cost[MAXV][MAXD];
} WGraph;

void wgraphInit(WGraph *g, int n);
void wgraphAddEdge(WGraph *g, int u, int v, int c);
"""

WG_C = r"""
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
"""

H2 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + WG_H + r"""
/* ---- Yours: Dijkstra from s that also counts shortest paths.
        dist[v] = shortest distance (INF if unreachable)
        ways[v] = how many different shortest paths reach v (0 if unreachable).
        All edge weights are >= 1. ---- */
void dijkstraCount(const WGraph *g, int s, int dist[], long long ways[]);

#endif
"""

M2 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    static WGraph g;
    wgraphInit(&g, n);
    for (int i = 0; i < m; i++) {
        int u, v, c;
        if (scanf("%d %d %d", &u, &v, &c) != 3) return 0;
        wgraphAddEdge(&g, u, v, c);
    }
    int s, t;
    if (scanf("%d %d", &s, &t) != 2) return 0;

    int dist[MAXV];
    long long ways[MAXV];
    dijkstraCount(&g, s, dist, ways);

    if (dist[t] >= INF) printf("-1\n0\n");
    else printf("%d\n%lld\n", dist[t], ways[t]);
    return 0;
}
"""

S2 = r"""
#include "problem.h"

void dijkstraCount(const WGraph *g, int s, int dist[], long long ways[]) {
    int done[MAXV];
    /* TODO: O(V^2) Dijkstra, with one extra array.
       ways[s] = 1, everything else 0.
       When relaxing u -> v with new distance nd:
         nd <  dist[v]  -> strictly better: dist[v] = nd, ways[v] = ways[u]
         nd == dist[v]  -> another equally short route: ways[v] += ways[u]
       Only do this from a u that has just been finalised. */
    (void)done;
}
"""

A2 = r"""
#include "problem.h"

void dijkstraCount(const WGraph *g, int s, int dist[], long long ways[]) {
    int done[MAXV];
    for (int v = 0; v <= g->n; v++) { dist[v] = INF; ways[v] = 0; done[v] = 0; }
    dist[s] = 0;
    ways[s] = 1;

    for (int step = 0; step < g->n; step++) {
        int u = -1;
        for (int v = 1; v <= g->n; v++)
            if (!done[v] && (u == -1 || dist[v] < dist[u])) u = v;
        if (u == -1 || dist[u] >= INF) break;
        done[u] = 1;                       /* ways[u] is final from here on */

        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->to[u][i];
            int nd = dist[u] + g->cost[u][i];
            if (nd < dist[v]) {
                dist[v] = nd;
                ways[v] = ways[u];         /* old routes were longer: forget them */
            } else if (nd == dist[v]) {
                ways[v] += ways[u];        /* a tie: add these routes too */
            }
        }
    }
}
"""


def edges_text(n, w, s, t):
    items = list(w.items())
    rng.shuffle(items)
    return f"{n} {len(items)}\n" + "".join(f"{u} {v} {c}\n" for (u, v), c in items) + f"{s} {t}\n"


T2 = [edges_text(4, {(1, 2): 1, (1, 3): 1, (2, 4): 1, (3, 4): 1}, 1, 4),
      edges_text(5, {(1, 2): 1, (1, 3): 2, (2, 3): 1, (2, 4): 2, (3, 4): 1, (4, 5): 1}, 1, 5),
      edges_text(3, {(1, 2): 5}, 1, 3),
      edges_text(3, {(1, 2): 2, (2, 3): 2, (1, 3): 4}, 1, 3),
      edges_text(6, {(1, 2): 1, (1, 3): 1, (2, 4): 1, (3, 4): 1, (4, 5): 1, (4, 6): 1, (5, 6): 0 + 1}, 1, 6),
      edges_text(2, {(1, 2): 3}, 2, 2)]
for _ in range(6):
    n, w = rand_directed(4, 8, 0.45, 1, 4)          # small weights => many ties
    T2.append(edges_text(n, w, 1, rng.randint(2, n)))

write_problem(
    PACK, UNIT, "p02-count-shortest-paths", title="Dijkstra: how many shortest paths?",
    mode="function", difficulty="hard", estimated_minutes=18, samples=2, tier="extra",
    topics=["dijkstra", "counting", "dynamic programming"],
    prereqs=[f"{PACK}.05-dijkstra.p01-dijkstra-matrix"],
    source="Common Dijkstra modification",
    hints=[
        "Keep a second array ways[] next to dist[]. ways[s] = 1.",
        "On a strictly better distance, the old routes are all longer and no longer "
        "count: ways[v] = ways[u]. On an equal distance, these routes are extra "
        "shortest routes: ways[v] += ways[u].",
        "It only works because u is finalised when you relax from it, so ways[u] "
        "is already complete. That is also why weights must be positive here.",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"wgraph.c": WG_C},
    statement=r"""
# Dijkstra: how many shortest paths?

A standard way to make Dijkstra "not straightforward": don't just ask for the shortest
distance, ask **how many different paths achieve it**.

```c
void dijkstraCount(const WGraph *g, int s, int dist[], long long ways[]);
```

## Input format

```
n m
u1 v1 w1
...
s t
```

`m` **directed** edges, weights `>= 1`. Print `dist[t]` and `ways[t]` on two lines, or
`-1` and `0` if `t` is unreachable.

## Example

```
4 4
1 2 1
1 3 1
2 4 1
3 4 1
1 4
```

```
2
2
```

Two paths of length 2: `1-2-4` and `1-3-4`.

## The two-line change

Dijkstra already visits vertices in order of final distance. When it relaxes an edge
`u -> v` giving candidate distance `nd`:

| case | meaning | update |
|---|---|---|
| `nd < dist[v]` | a strictly shorter route | `dist[v] = nd; ways[v] = ways[u];` |
| `nd == dist[v]` | another route of the same best length | `ways[v] += ways[u];` |
| `nd > dist[v]` | worse | nothing |

The reset in the first row matters: every route counted so far was longer, so they
stop counting.

## How big can the count get?

Exponentially big. Give vertex `i` an edge to every `j > i` of weight `j - i` and
*every* path from 1 to `n` is a shortest path: `2^(n-2)` of them. At 65 vertices that
no longer fits in a `long long` and the count silently goes negative. These tests keep
the answer well inside `long long`; in an exam, a question that can produce huge counts
will say "print it modulo 10^9+7" - apply `% MOD` at both update lines if it does.

## Why positive weights

The count is right only if `ways[u]` is complete when you relax out of `u` - that is,
every shortest route into `u` has already been counted. Dijkstra guarantees that
because it finalises `u` only after everything closer. A zero-weight edge could let a
vertex at the same distance feed `u` *after* `u` was finalised, so this question
always guarantees weights `>= 1`.

The same pattern answers "minimum number of edges among all shortest paths", or "the
maximum total bonus along a shortest path" - keep a second array and update it with the
same three-way comparison.
""",
)

# ================================================================= p03 Bellman-Ford
A3 = r"""
#include <stdio.h>

#define MAXV 105
#define MAXE 10005
#define INF 1000000000

static int eu[MAXE], ev[MAXE], ew[MAXE];
static long long dist[MAXV];

int main(void) {
    int n, m, s;
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;
    for (int i = 0; i < m; i++)
        if (scanf("%d %d %d", &eu[i], &ev[i], &ew[i]) != 3) return 0;

    for (int v = 1; v <= n; v++) dist[v] = INF;
    dist[s] = 0;

    /* n-1 rounds: every simple path has at most n-1 edges. */
    for (int round = 1; round <= n - 1; round++) {
        int changed = 0;
        for (int i = 0; i < m; i++) {
            if (dist[eu[i]] == INF) continue;          /* never relax from "infinity" */
            if (dist[eu[i]] + ew[i] < dist[ev[i]]) {
                dist[ev[i]] = dist[eu[i]] + ew[i];
                changed = 1;
            }
        }
        if (!changed) break;
    }

    /* One more round: anything that still improves sits on a reachable negative cycle. */
    for (int i = 0; i < m; i++) {
        if (dist[eu[i]] == INF) continue;
        if (dist[eu[i]] + ew[i] < dist[ev[i]]) { printf("NEGATIVE CYCLE\n"); return 0; }
    }

    for (int v = 1; v <= n; v++) {
        if (dist[v] == INF) printf("INF");
        else printf("%lld", dist[v]);
        printf(v < n ? " " : "\n");
    }
    return 0;
}
"""

S3 = r"""
#include <stdio.h>

#define MAXV 105
#define MAXE 10005
#define INF 1000000000

int main(void) {
    /* TODO
       Store the edges as three arrays (or a struct): from, to, weight.
       dist[s] = 0, everything else INF.
       Repeat n-1 times: for every edge u->v, if dist[u] != INF and
       dist[u] + w < dist[v], lower dist[v].
       Then one extra pass: if any edge can STILL be relaxed, print
       NEGATIVE CYCLE. Otherwise print the distances, INF for unreachable. */
    return 0;
}
"""


def bf_text(n, edges, s):
    return f"{n} {len(edges)} {s}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges)


def rand_bf(allow_cycle):
    n = rng.randint(3, 7)
    # a random DAG over a random order has no cycles at all, so negative weights are safe
    order = list(range(1, n + 1))
    rng.shuffle(order)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.45:
                edges.append((order[i], order[j], rng.randint(-8, 15)))
    if allow_cycle and len(edges) > 1:
        # a backward edge with a weight that may or may not close a negative cycle
        i, j = sorted(rng.sample(range(n), 2))
        edges.append((order[j], order[i], rng.randint(-5, 25)))
    rng.shuffle(edges)
    return n, edges


T3 = [bf_text(5, [(1, 2, 6), (1, 3, 7), (2, 3, 8), (2, 4, 5), (2, 5, -4), (3, 4, -3),
                  (3, 5, 9), (4, 2, -2), (5, 4, 7), (5, 1, 2)], 1),
      bf_text(3, [(1, 2, 1), (2, 3, -1), (3, 2, -1)], 1),
      bf_text(4, [(1, 2, 4), (3, 4, -1), (4, 3, -1)], 1),        # negative cycle NOT reachable
      bf_text(4, [(1, 2, 2), (2, 3, -5), (1, 3, 1)], 1),
      bf_text(1, [], 1),
      bf_text(3, [(2, 1, -3), (3, 2, 4)], 3)]
for k in range(6):
    T3.append(bf_text(*rand_bf(allow_cycle=(k % 2 == 1)), s=1))

write_problem(
    PACK, UNIT, "p03-bellman-ford", title="Bellman-Ford: distances with negative edges",
    mode="program", difficulty="hard", estimated_minutes=20, samples=1,
    topics=["bellman-ford", "shortest path", "negative weights"],
    prereqs=[f"{PACK}.05-dijkstra.p05-negative-cycle"],
    source="DSA theory syllabus; Week 4 Q3 is the same algorithm on a grid",
    hints=[
        "Store the graph as an edge list - Bellman-Ford loops over edges, never over "
        "vertices' neighbours.",
        "Skip any edge whose tail is still INF. INF + (-3) is a smaller number than "
        "INF, so without the check 'unreachable' vertices slowly start looking "
        "reachable.",
        "A negative cycle that s cannot reach does not affect any distance from s, "
        "and the INF check is exactly what stops it from being reported. Test 3 has "
        "that case.",
    ],
    starter=S3, solution=A3, tests=T3,
    statement=r"""
# Bellman-Ford: distances with negative edges

The Week 4 sheet only asked you to *detect* a negative cycle. This is the algorithm
doing its actual job: distances from a source when some edges are negative.

## Input format

```
n m s
u1 v1 w1
...
```

`m` **directed** edges; weights may be negative.

## Output format

If a negative cycle is **reachable from `s`**, print `NEGATIVE CYCLE`. Otherwise print
`dist[1] ... dist[n]` on one line, with `INF` for unreachable vertices.

(Not `-1`: with negative weights, `-1` is a perfectly real distance. A question with
negative edges that asks for `-1` on unreachable is ambiguous, and worth pointing out.)

## Sample

```
5 10 1
1 2 6
1 3 7
2 3 8
2 4 5
2 5 -4
3 4 -3
3 5 9
4 2 -2
5 4 7
5 1 2
```

```
0 2 7 4 -2
```

## The algorithm

Relax **every edge**, `n-1` times over. A shortest simple path has at most `n-1` edges,
and each full pass extends the set of correct distances by at least one more edge
along every path - so after `n-1` passes, everything is final.

If a further pass can still improve something, there is no final answer: a negative
cycle lets you keep going round. That is the detection step.

## The INF guard

```c
if (dist[u] == INF) continue;
```

Without it, an edge out of an unreachable vertex with weight `-3` "improves" its target
to `INF - 3`, and unreachable vertices start printing as enormous numbers. Worse, a
negative cycle that `s` **cannot reach** gets reported, though it has no effect on any
distance from `s`. Test 3 is exactly that graph.

## Dijkstra vs Bellman-Ford, for the viva

| | Dijkstra (O(V^2) array) | Bellman-Ford |
|---|---|---|
| time | `O(V^2)` | `O(VE)` |
| negative edges | wrong answers | correct |
| negative cycles | cannot detect | detects |
| idea | finalise the closest vertex greedily | relax everything, repeatedly |
""",
)

# ================================================================= p04 Floyd-Warshall
A4 = r"""
#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

static long long d[MAXV][MAXV];

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) {
            int x;
            scanf("%d", &x);
            d[i][j] = (i == j) ? 0 : (x == NOEDGE ? INF : x);
        }

    /* k is the OUTER loop: "shortest paths using only 1..k as intermediates". */
    for (int k = 1; k <= n; k++)
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++) {
                if (d[i][k] == INF || d[k][j] == INF) continue;
                if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
            }

    for (int i = 1; i <= n; i++)
        if (d[i][i] < 0) { printf("NEGATIVE CYCLE\n"); return 0; }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (d[i][j] == INF) printf("INF");
            else printf("%lld", d[i][j]);
            printf(j < n ? " " : "\n");
        }
    }
    return 0;
}
"""

S4 = r"""
#include <stdio.h>

#define MAXV 105
#define NOEDGE 999
#define INF 1000000000

int main(void) {
    /* TODO
       d[i][j] = the matrix, with 999 turned into INF (and 0 on the diagonal).
       for k: for i: for j:   (k OUTERMOST - see the statement)
           if both halves are finite and d[i][k] + d[k][j] < d[i][j], take it
       If any d[i][i] ends up negative -> NEGATIVE CYCLE.
       Otherwise print the matrix, INF where unreachable. */
    return 0;
}
"""


def fw_matrix(n, w):
    return matrix_input(n, w)


T4 = [fw_matrix(4, {(1, 2): 3, (1, 4): 7, (2, 1): 8, (2, 3): 2, (3, 1): 5, (3, 4): 1, (4, 1): 2}),
      fw_matrix(3, {(1, 2): 4, (2, 3): -2, (1, 3): 5}),
      fw_matrix(3, {(1, 2): 1, (2, 3): -1, (3, 1): -1}),
      fw_matrix(4, {(1, 2): 2, (3, 4): 1}),
      fw_matrix(1, {})]
for k in range(6):
    n, edges = rand_bf(allow_cycle=(k % 3 == 2))
    T4.append(fw_matrix(n, {(u, v): w for u, v, w in edges}))

write_problem(
    PACK, UNIT, "p04-floyd-warshall", title="Floyd-Warshall: all-pairs shortest paths",
    mode="program", difficulty="medium", estimated_minutes=15, samples=1,
    topics=["floyd-warshall", "all pairs shortest path", "dynamic programming"],
    prereqs=[f"{PACK}.05-dijkstra.p01-dijkstra-matrix"],
    source="DSA theory syllabus (not yet asked in lab)",
    hints=[
        "Three nested loops, and k must be the OUTERMOST. That order is the entire "
        "algorithm - swap it and it compiles, runs and gives wrong answers.",
        "Convert 999 to a large INF when reading, and skip the update when either "
        "d[i][k] or d[k][j] is INF so you never add to infinity.",
        "After the loops, a negative number on the diagonal means some vertex can "
        "reach itself with negative total cost - a negative cycle.",
    ],
    starter=S4, solution=A4, tests=T4,
    statement=r"""
# Floyd-Warshall: all-pairs shortest paths

Shortest distances between **every** pair of vertices, in about six lines.

## Input format

- first line: `n`
- next `n` lines: the adjacency matrix, `999` = no edge (directed; weights may be
  negative)

## Output format

The `n x n` distance matrix, `INF` where no path exists - or `NEGATIVE CYCLE` if the
graph has one.

## Sample

```
4
0 3 999 7
8 0 2 999
5 999 0 1
2 999 999 0
```

```
0 3 5 6
5 0 2 3
3 6 0 1
2 5 7 0
```

## The whole algorithm

```c
for (k = 1; k <= n; k++)
    for (i = 1; i <= n; i++)
        for (j = 1; j <= n; j++)
            if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
```

After iteration `k`, `d[i][j]` is the shortest `i -> j` path that uses **only vertices
`1..k` as stopovers**. Each new `k` asks one question per pair: "is it better to go
through `k`?". That is why `k` has to be the outer loop - by the time you consider
stopover `k`, every `d[i][k]` and `d[k][j]` must already be final for stopovers `1..k-1`.
Put `i` or `j` outermost and it still runs, still prints plausible numbers, and is
wrong.

## The diagonal

As on the Week 4 sheet, the diagonal is always `0` and `999` only ever marks a missing
edge between **distinct** vertices, so there are no self-loops. A negative cycle must
therefore pass through at least two vertices. (If a question did allow a negative
self-loop on the diagonal, you would have to read it instead of overwriting it with 0.)

## Two guards

- skip the update when `d[i][k]` or `d[k][j]` is `INF`, or `INF + negative` sneaks under
  `INF`
- a negative diagonal entry afterwards means a vertex reaches itself at negative cost:
  a negative cycle

## When to use which

| question | algorithm |
|---|---|
| one source, non-negative weights | Dijkstra |
| one source, negative weights | Bellman-Ford |
| every pair, small `n` (`<= 100`) | Floyd-Warshall - `O(n^3)`, tiny code |
""",
)

# ================================================================= p05 Prim with blocked edges
A5 = r"""
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
"""

S5 = r"""
#include <stdio.h>

#define MAXV 105
#define INF 1000000000

int main(void) {
    /* TODO
       Read n m s, the m edges, then b and the b blocked pairs.
       A blocked edge simply does not exist - delete it from the matrix.
       Run Prim from s. Every time a vertex joins the tree (except s), put its
       edge in the output matrix and print the whole matrix.
       Then print the final matrix once more and the total cost.
       If the blocked edges disconnect the graph, print -1 and NOTHING else. */
    return 0;
}
"""


def prim_blocked_text(n, edges, s, blocked):
    return (f"{n} {len(edges)} {s}\n" + "".join(f"{u} {v} {x}\n" for u, v, x in edges)
            + f"{len(blocked)}\n" + "".join(f"{u} {v}\n" for u, v in blocked))


def rand_undirected_distinct(nmin, nmax, density):
    n = rng.randint(nmin, nmax)
    pairs = {(rng.randint(1, v - 1), v) for v in range(2, n + 1)}
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if rng.random() < density:
                pairs.add((u, v))
    pairs = sorted(pairs)
    weights = rng.sample(range(1, 100), len(pairs))
    edges = [(u, v, x) for (u, v), x in zip(pairs, weights)]
    rng.shuffle(edges)
    return n, edges


SAMPLE_EDGES = [(1, 2, 4), (1, 3, 2), (2, 3, 1), (2, 4, 5), (3, 4, 8), (3, 5, 10), (4, 5, 7)]
T5 = [prim_blocked_text(5, SAMPLE_EDGES, 1, [(2, 3)]),
      prim_blocked_text(5, SAMPLE_EDGES, 1, []),
      prim_blocked_text(5, SAMPLE_EDGES, 1, [(3, 5), (5, 4)]),
      prim_blocked_text(4, [(1, 2, 3), (2, 3, 4), (3, 4, 5), (1, 4, 9)], 2, [(2, 1)]),
      prim_blocked_text(3, [(1, 2, 5)], 1, [])]
for _ in range(6):
    n, edges = rand_undirected_distinct(4, 7, 0.45)
    blocked = [(u, v) for u, v, _ in rng.sample(edges, rng.randint(0, min(3, len(edges))))]
    T5.append(prim_blocked_text(n, edges, rng.randint(1, n), blocked))

write_problem(
    PACK, UNIT, "p05-prim-blocked-steps", title="Prim with blocked edges, printing every step",
    mode="program", difficulty="hard", estimated_minutes=30, samples=1,
    topics=["mst", "prim", "matrix output"],
    prereqs=[f"{PACK}.09-mst.p04-week5-q1-prim"],
    source="Reconstruction of the DSA Lab Week 5 modification question",
    hints=[
        "Blocked edges need no special handling in the algorithm. Read them and "
        "delete them from the weight matrix; after that it is ordinary Prim.",
        "Print a snapshot at the moment a vertex joins the tree with a real edge - "
        "that is, when you mark u done and parent[u] != -1. The source itself joins "
        "with no edge and prints nothing.",
        "Blocking can disconnect the graph, and then the answer is -1 alone. Run "
        "Prim once silently to check, then again to print.",
    ],
    starter=S5, solution=A5, tests=T5,
    statement=r"""
# Prim with blocked edges, printing every step

**This is a reconstruction** of your Week 5 modification question: Prim's algorithm,
printing the MST after every step, with some edges blocked. The official format is lost,
so this follows Week 5 Q1/Q2's conventions.

## Input format

```
n m s
u1 v1 w1          (m undirected edges, positive distinct weights)
...
b
x1 y1             (b blocked edges - they may not be used)
...
```

## Output format

Run Prim from `s`. After **each vertex joins the tree** (with its edge), print the
current tree as an `n x n` matrix (`0` diagonal, weight for a chosen edge in both
directions, `-1` otherwise). Then print the final tree once more, then the total cost.
If the blocked edges leave some vertex unreachable, print `-1` and nothing else.

## Sample

```
5 7 1
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
3 5 10
4 5 7
1
2 3
```

```
0 -1 2 -1 -1
-1 0 -1 -1 -1
2 -1 0 -1 -1
-1 -1 -1 0 -1
-1 -1 -1 -1 0
0 4 2 -1 -1
4 0 -1 -1 -1
2 -1 0 -1 -1
-1 -1 -1 0 -1
-1 -1 -1 -1 0
0 4 2 -1 -1
4 0 -1 5 -1
2 -1 0 -1 -1
-1 5 -1 0 -1
-1 -1 -1 -1 0
0 4 2 -1 -1
4 0 -1 5 -1
2 -1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
0 4 2 -1 -1
4 0 -1 5 -1
2 -1 0 -1 -1
-1 5 -1 0 7
-1 -1 -1 7 0
18
```

Blocking `2-3` (the cheapest edge, weight 1) forces 2 to attach through `1-2` instead,
and the cost rises from 15 to 18.

## The twist is not in the algorithm

A blocked edge is simply an edge that does not exist. Read the blocked pairs and zero
them out of the weight matrix (both directions), and what remains is exactly Week 5
Q1. Modification questions are often like this: the twist changes the *input*, and
recognising that saves you from rewriting the algorithm.

## Prim vs Kruskal snapshots

Prim's snapshots grow **one connected tree** outward from `s`. Kruskal's (Week 5 Q2)
can show several disconnected fragments that merge later. If an exam shows you a
sequence of partial trees, that is the quickest way to tell which algorithm produced
them.
""",
)

# ================================================================= p06 Prim with a heap
H6 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + WG_H + r"""
/* ---- Provided: min-heap priority queue from unit 03. ---- */
typedef struct { int key; int id; } Item;
typedef struct { Item a[MAXV * MAXD]; int size; } MinHeap;

void heapInit(MinHeap *h);
int  heapEmpty(const MinHeap *h);
void heapInsert(MinHeap *h, int key, int id);
Item heapExtractMin(MinHeap *h);

/* ---- Yours: MST cost by Prim from s using the heap, or -1 if disconnected.
        The graph is undirected: every edge was added in both directions. ---- */
int primHeap(const WGraph *g, int s);

#endif
"""

HEAP_C = WG_C + r"""
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

M6 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m, s;
    if (scanf("%d %d %d", &n, &m, &s) != 3) return 0;
    static WGraph g;
    wgraphInit(&g, n);
    for (int i = 0; i < m; i++) {
        int u, v, c;
        if (scanf("%d %d %d", &u, &v, &c) != 3) return 0;
        wgraphAddEdge(&g, u, v, c);
        wgraphAddEdge(&g, v, u, c);
    }
    printf("%d\n", primHeap(&g, s));
    return 0;
}
"""

S6 = r"""
#include "problem.h"

int primHeap(const WGraph *g, int s) {
    static MinHeap h;
    int inTree[MAXV] = {0};
    heapInit(&h);

    /* TODO
       Push (0, s). Then, while the heap is not empty:
         pop the cheapest (key, u)
         if u is already in the tree, skip it (a stale, more expensive entry)
         otherwise put u in the tree, add key to the total, and push
         (edge cost, v) for every neighbour v not yet in the tree
       At the end, if fewer than n vertices joined, return -1. */
    return -1;
}
"""

A6 = r"""
#include "problem.h"

int primHeap(const WGraph *g, int s) {
    static MinHeap h;
    int inTree[MAXV] = {0};
    int joined = 0, total = 0;
    heapInit(&h);

    heapInsert(&h, 0, s);
    while (!heapEmpty(&h)) {
        Item it = heapExtractMin(&h);
        int u = it.id;
        if (inTree[u]) continue;           /* lazy deletion: already attached cheaper */

        inTree[u] = 1;
        total += it.key;
        joined++;

        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->to[u][i];
            if (!inTree[v]) heapInsert(&h, g->cost[u][i], v);   /* key = ONE edge */
        }
    }
    return (joined == g->n) ? total : -1;
}
"""


def prim_heap_text(n, edges, s):
    return f"{n} {len(edges)} {s}\n" + "".join(f"{u} {v} {x}\n" for u, v, x in edges)


T6 = [prim_heap_text(5, SAMPLE_EDGES, 1),
      prim_heap_text(5, SAMPLE_EDGES, 4),
      prim_heap_text(4, [(1, 2, 3), (3, 4, 5)], 1),
      prim_heap_text(1, [], 1),
      prim_heap_text(4, [(1, 2, 1), (2, 3, 1), (3, 4, 1), (1, 4, 1), (1, 3, 1)], 2)]
for _ in range(6):
    n, edges = rand_undirected_distinct(4, 10, 0.4)
    if rng.random() < 0.25:
        edges = edges[: max(0, len(edges) - rng.randint(2, 5))]
    T6.append(prim_heap_text(n, edges, rng.randint(1, n)))

write_problem(
    PACK, UNIT, "p06-prim-heap", title="Prim with a priority queue",
    mode="function", difficulty="hard", estimated_minutes=15, samples=2,
    topics=["mst", "prim", "heap", "priority queue"],
    prereqs=[f"{PACK}.09-mst.p03-prim-matrix", f"{PACK}.05-dijkstra.p04-dijkstra-heap"],
    source="DSA theory: 'implementation of Prim's and Dijkstra's algorithms using priority queues'",
    hints=[
        "It is the heap Dijkstra from unit 05 with one change: the key you push is "
        "the edge cost alone, not dist[u] + cost.",
        "Lazy deletion again: a vertex may be in the heap several times with "
        "different keys. The first time it comes out is the cheapest; skip it on "
        "every later pop with 'if (inTree[u]) continue;'.",
        "Count how many vertices actually joined. Fewer than n means disconnected.",
    ],
    header=H6, harness=M6, starter=S6, solution=A6, tests=T6,
    extra={"support.c": HEAP_C},
    statement=r"""
# Prim with a priority queue

The theory syllabus asks for "implementation of Prim's and Dijkstra's algorithms using
priority queues". You wrote the heap Dijkstra in unit 05; this is its twin.

```c
int primHeap(const WGraph *g, int s);   /* MST cost, or -1 if disconnected */
```

The min-heap (`heapInsert`, `heapExtractMin` over `Item {key, id}`) is provided.

## Input format

```
n m s
u1 v1 w1
...
```

Undirected edges (added in both directions for you). Print the MST cost or `-1`.

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
```

## Side by side with heap Dijkstra

```c
/* Dijkstra */                              /* Prim */
Item it = heapExtractMin(&h);               Item it = heapExtractMin(&h);
if (it.key > dist[u]) continue;             if (inTree[u]) continue;
                                            inTree[u] = 1; total += it.key;
for each edge u -> v:                       for each edge u -> v:
  if (dist[u] + c < dist[v])                  if (!inTree[v])
    { dist[v] = dist[u] + c;                    heapInsert(&h, c, v);
      heapInsert(&h, dist[v], v); }
```

The key pushed is **the edge cost alone**. Push `total + c` or `dist[u] + c` out of habit
and you are computing shortest paths, and the "MST" comes out too expensive.

Complexity: `O(E log E)` - better than the `O(V^2)` array version on sparse graphs, worse
on dense ones, which is why the lab's `n <= 100` matrix questions happily use the array
version.
""",
)

report(UNIT, 6)
