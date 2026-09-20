"""Unit 08 - DFS and graph traversal.  Run: python scripts/authoring/unit_08_graph_traversal.py"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report

PACK = "c-s3"
UNIT = "08-graph-traversal"
rng = random.Random(808)

write_unit(PACK, UNIT, "DFS, components and bipartiteness",
           "DFS recursively and with an explicit stack (the Week 3 ADT way), then the "
           "classic applications: components, cycles, topological order, bipartite test.")

GRAPH_TYPES = r"""
#define MAXV 105
#define MAXE 20005

/* Vertices are 1..n.  adj[u][0..deg[u]-1] is kept in ascending order. */
typedef struct {
    int n;
    int deg[MAXV];
    int adj[MAXV][MAXV];
} Graph;
"""

GRAPH_BUILD = r"""
#include <stdlib.h>
#include "problem.h"

void graphInit(Graph *g, int n) {
    g->n = n;
    for (int i = 0; i <= n; i++) g->deg[i] = 0;
}

void addEdge(Graph *g, int u, int v) {
    g->adj[u][g->deg[u]++] = v;
}

static int cmpInt(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}

void sortNeighbours(Graph *g) {
    for (int u = 1; u <= g->n; u++)
        qsort(g->adj[u], g->deg[u], sizeof(int), cmpInt);
}
"""

PROVIDED = r"""
/* ---- Provided: the graph is built and its lists sorted before you are called. ---- */
void graphInit(Graph *g, int n);
void addEdge(Graph *g, int u, int v);
void sortNeighbours(Graph *g);
"""


def read_graph(undirected=True, with_source=True):
    both = "        addEdge(g, v, u);\n" if undirected else ""
    src = ""
    if with_source:
        src = ""
    return r"""
static void readGraph(Graph *g) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return;
    graphInit(g, n);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (scanf("%d %d", &u, &v) != 2) return;
        addEdge(g, u, v);
""" + both + r"""    }
    sortNeighbours(g);
}
""" + src


def rand_graph(nmin=3, nmax=8, density=0.35, undirected=True, connected=False):
    n = rng.randint(nmin, nmax)
    edges = set()
    if connected:
        for v in range(2, n + 1):
            u = rng.randint(1, v - 1)
            edges.add((u, v) if undirected else (u, v))
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            if u == v:
                continue
            if undirected and v < u:
                continue
            if rng.random() < density:
                edges.add((u, v))
    e = sorted(edges)
    rng.shuffle(e)
    return n, e


def graph_input(n, edges, source=None):
    s = f"{n} {len(edges)}\n" + "".join(f"{u} {v}\n" for u, v in edges)
    if source is not None:
        s += f"{source}\n"
    return s


EDGE_FMT_UNDIR = r"""
## Input format

```
n m
u1 v1
...
```

`n` vertices numbered `1..n` and `m` **undirected** edges (each one is added in both
directions for you). Adjacency lists are sorted ascending before your function runs.
"""

# ------------------------------------------------------------------ p01
H1 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + GRAPH_TYPES + PROVIDED + r"""
/* ---- Yours: recursive DFS from s.  Write the visit order into order[]
        and return how many vertices were visited. ---- */
int dfsOrder(const Graph *g, int s, int order[]);

#endif
"""

M1 = r"""
#include <stdio.h>
#include "problem.h"
""" + read_graph() + r"""
int main(void) {
    Graph g;
    readGraph(&g);
    int s;
    if (scanf("%d", &s) != 1) return 0;

    int order[MAXV];
    int count = dfsOrder(&g, s, order);
    for (int i = 0; i < count; i++) printf("%d%s", order[i], i + 1 < count ? " " : "");
    printf("\n");
    return 0;
}
"""

S1 = r"""
#include "problem.h"

static int visited[MAXV];

static void dfs(const Graph *g, int u, int order[], int *count) {
    /* TODO
       - mark u visited, append it to order[] (use (*count)++)
       - for each neighbour v of u in ascending order:
             if v is not visited, recurse into it */
}

int dfsOrder(const Graph *g, int s, int order[]) {
    int count = 0;
    for (int v = 0; v <= g->n; v++) visited[v] = 0;
    dfs(g, s, order, &count);
    return count;
}
"""

A1 = r"""
#include "problem.h"

static int visited[MAXV];

static void dfs(const Graph *g, int u, int order[], int *count) {
    visited[u] = 1;
    order[(*count)++] = u;
    for (int i = 0; i < g->deg[u]; i++) {
        int v = g->adj[u][i];
        if (!visited[v]) dfs(g, v, order, count);
    }
}

int dfsOrder(const Graph *g, int s, int order[]) {
    int count = 0;
    for (int v = 0; v <= g->n; v++) visited[v] = 0;
    dfs(g, s, order, &count);
    return count;
}
"""

T1 = [graph_input(5, [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)], 1),
      graph_input(6, [(1, 2), (1, 3), (2, 4), (3, 5), (5, 6)], 1),
      graph_input(4, [(1, 2), (3, 4)], 1)]
T1 += [graph_input(*rand_graph(4, 9, connected=True), source=1) for _ in range(5)]

write_problem(
    PACK, UNIT, "p01-dfs-recursive", title="DFS, recursive",
    mode="function", difficulty="easy", estimated_minutes=8, samples=1,
    topics=["dfs", "graph", "recursion"],
    prereqs=[f"{PACK}.04-bfs.p02-bfs-order"],
    source="DSA Lab Week 3 - Graphs, DFSTraversal",
    hints=[
        "Three lines in the body: mark visited, record the vertex, then loop over "
        "the neighbours recursing into the unvisited ones.",
        "Pass the counter as int *count so every recursive call shares it.",
        "Mark u visited at the TOP of dfs(u), before the loop. Checking only at the "
        "call site lets a vertex be entered twice from two different neighbours.",
    ],
    header=H1, harness=M1, starter=S1, solution=A1, tests=T1,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# DFS, recursive

Go as deep as possible before backtracking.

```c
int dfsOrder(const Graph *g, int s, int order[]);
```

Write the visit order starting at `s` into `order[]` and return the count. Only
vertices reachable from `s` appear.
""" + EDGE_FMT_UNDIR + r"""
Then a final line with the source `s`.

## Example

```
5 5
1 2
1 3
2 4
3 4
4 5
1
```

```
1 2 4 3 5
```

From 1 we take the smallest neighbour 2, from 2 we reach 4, from 4 we take 3 (smaller
than 5), 3 has nothing new, back to 4, then 5.

Compare that with BFS on the same graph (`1 2 3 4 5`): DFS commits to a branch, BFS
spreads out level by level.

## Where the marking goes

Mark `u` as visited at the **top of `dfs(u)`**, not only before calling it. If `u` has
two unvisited neighbours that both link onward to `w`, checking only at the call site
can enter `w` twice.
""",
)

# ------------------------------------------------------------------ p02
H2 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + GRAPH_TYPES + PROVIDED + r"""
/* ---- Yours: the SAME order as recursive DFS, but using an explicit stack
        and no recursion (the Week 3 STACK-ADT way). ---- */
int dfsIterative(const Graph *g, int s, int order[]);

#endif
"""

M2 = M1.replace("dfsOrder(&g, s, order)", "dfsIterative(&g, s, order)")

S2 = r"""
#include "problem.h"

int dfsIterative(const Graph *g, int s, int order[]) {
    int visited[MAXV] = {0};
    int stack[MAXE];      /* NOT MAXV - see the statement */
    int top = -1, count = 0;

    /* TODO
       - push s
       - while the stack is not empty:
           pop u
           if u is already visited, skip it (it was pushed more than once)
           mark it, append it to order[]
           push its unvisited neighbours in DESCENDING order
       Descending, so the smallest one ends up on top and is popped first. */

    return count;
}
"""

A2 = r"""
#include "problem.h"

int dfsIterative(const Graph *g, int s, int order[]) {
    int visited[MAXV] = {0};
    int stack[MAXE];
    int top = -1, count = 0;

    stack[++top] = s;
    while (top >= 0) {
        int u = stack[top--];
        if (visited[u]) continue;      /* a duplicate push from another neighbour */
        visited[u] = 1;
        order[count++] = u;

        /* push descending so the smallest neighbour is popped first */
        for (int i = g->deg[u] - 1; i >= 0; i--) {
            int v = g->adj[u][i];
            if (!visited[v]) stack[++top] = v;
        }
    }
    return count;
}
"""

T2 = list(T1)

write_problem(
    PACK, UNIT, "p02-dfs-iterative", title="DFS with an explicit stack",
    mode="function", difficulty="medium", estimated_minutes=14, samples=1,
    topics=["dfs", "stack", "graph"],
    prereqs=[f"{PACK}.{UNIT}.p01-dfs-recursive", f"{PACK}.01-stack.p01-array-stack"],
    source="DSA Lab Week 3 - Graphs requires DFS to be ITERATIVE using the STACK ADT",
    hints=[
        "Mark a vertex visited when you POP it, not when you push it - a vertex can "
        "sit in the stack several times and only the first pop counts.",
        "Because of that, check 'if (visited[u]) continue;' right after popping.",
        "To match recursive order, push neighbours in DESCENDING order so the "
        "smallest is on top and comes off first.",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# DFS with an explicit stack

Your Week 3 assignment requires DFS to be **iterative, using the STACK ADT** - not
recursive. This is that version, and it must produce **exactly the same order** as the
recursive one.

```c
int dfsIterative(const Graph *g, int s, int order[]);
```
""" + EDGE_FMT_UNDIR + r"""
Then a final line with the source `s`.

## Three things that are different from BFS

**1. Mark on pop, not on push.** In BFS you mark when enqueuing. Here a vertex may be
pushed by several neighbours before it is ever popped, so you mark it when it comes
off, and skip it if it was already marked:

```c
int u = stack[top--];
if (visited[u]) continue;
```

**2. Push in descending order.** The stack reverses things. To visit the smallest
neighbour first - matching the recursive version, which loops ascending - push the
neighbours from largest to smallest so the smallest lands on top.

Push ascending instead and you get a *valid* DFS in a different order, which fails
every test here. That mismatch is exactly what the recursive-vs-iterative comparison
is for.

**3. The stack must hold up to `m` entries, not `n`.** Since a vertex can be pushed
once per incoming edge before it is popped, `int stack[MAXV]` overflows on dense
graphs. Size it `MAXE`.

## Example

```
5 5
1 2
1 3
2 4
3 4
4 5
1
```

```
1 2 4 3 5
```

Identical to the recursive output on the same input - that is the point.
""",
)

# ------------------------------------------------------------------ p03
H3 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + GRAPH_TYPES + PROVIDED + r"""
/* ---- Yours: label every vertex with its component number.
        Components are numbered 1, 2, 3, ... in order of their smallest vertex. ---- */
int components(const Graph *g, int comp[]);   /* returns how many components */

#endif
"""

M3 = r"""
#include <stdio.h>
#include "problem.h"
""" + read_graph() + r"""
int main(void) {
    Graph g;
    readGraph(&g);

    int comp[MAXV];
    int k = components(&g, comp);
    printf("%d\n", k);
    for (int c = 1; c <= k; c++) {
        int first = 1;
        for (int v = 1; v <= g.n; v++)
            if (comp[v] == c) { printf(first ? "%d" : " %d", v); first = 0; }
        printf("\n");
    }
    return 0;
}
"""

S3 = r"""
#include "problem.h"

int components(const Graph *g, int comp[]) {
    /* TODO
       - comp[v] = 0 means "not assigned yet"
       - for v from 1 to n: if comp[v] is still 0, start a new component number
         and flood-fill from v (DFS or BFS - either is fine) marking every vertex
         you reach with that number
       - return how many components you started
       Scanning v in ascending order is what numbers the components by their
       smallest vertex. */
    return 0;
}
"""

A3 = r"""
#include "problem.h"

static void flood(const Graph *g, int u, int comp[], int label) {
    comp[u] = label;
    for (int i = 0; i < g->deg[u]; i++) {
        int v = g->adj[u][i];
        if (comp[v] == 0) flood(g, v, comp, label);
    }
}

int components(const Graph *g, int comp[]) {
    for (int v = 0; v <= g->n; v++) comp[v] = 0;

    int label = 0;
    for (int v = 1; v <= g->n; v++)
        if (comp[v] == 0) flood(g, v, comp, ++label);
    return label;
}
"""

T3 = [graph_input(6, [(1, 2), (2, 3), (4, 5)]),
      graph_input(5, []),
      graph_input(4, [(1, 2), (2, 3), (3, 4), (4, 1)]),
      graph_input(7, [(1, 4), (4, 7), (2, 5), (3, 6), (6, 3)])]
T3 += [graph_input(*rand_graph(4, 10, density=0.18)) for _ in range(5)]

write_problem(
    PACK, UNIT, "p03-components", title="Connected components",
    mode="function", difficulty="easy", estimated_minutes=10, samples=2,
    topics=["dfs", "graph", "components"],
    prereqs=[f"{PACK}.{UNIT}.p01-dfs-recursive"],
    source="Standard DFS application (DSA theory: DFS and its applications)",
    hints=[
        "One DFS is not enough: DFS only reaches one component. Loop over every "
        "vertex and start a fresh traversal from each unvisited one.",
        "Use comp[] as both the visited array and the answer: 0 means unvisited, "
        "and a positive number is the component it belongs to.",
        "Scanning vertices 1..n in order automatically numbers components by their "
        "smallest member, which is what the output format wants.",
    ],
    header=H3, harness=M3, starter=S3, solution=A3, tests=T3,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# Connected components

```c
int components(const Graph *g, int comp[]);
```

Fill `comp[v]` with the component number of `v` and return how many there are.
Components are numbered `1, 2, 3, ...` **in order of their smallest vertex**.
""" + EDGE_FMT_UNDIR + r"""
## Output

The number of components, then one line per component listing its vertices ascending.

## Example

```
6 3
1 2
2 3
4 5
```

```
3
1 2 3
4 5
6
```

## The outer loop is the whole trick

A single DFS explores exactly one component. To cover the graph you need a loop
*around* the traversal:

```c
for (int v = 1; v <= n; v++)
    if (comp[v] == 0) flood(g, v, comp, ++label);
```

That pattern - "for every unvisited vertex, start a new traversal" - is the basis of
counting components, checking bipartiteness on a disconnected graph, and finding
cycles anywhere in a graph. Every one of those questions is a plain traversal plus
this loop.

Note the reuse: `comp[]` doubles as the visited array, since `0` can mean "not yet
assigned".
""",
)

# ------------------------------------------------------------------ p04
H4 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + GRAPH_TYPES + PROVIDED + r"""
/* ---- Yours: 1 if the UNDIRECTED graph contains a cycle, else 0.
        The graph may be disconnected. ---- */
int hasCycle(const Graph *g);

#endif
"""

M4 = r"""
#include <stdio.h>
#include "problem.h"
""" + read_graph() + r"""
int main(void) {
    Graph g;
    readGraph(&g);
    printf("%d\n", hasCycle(&g));
    return 0;
}
"""

S4 = r"""
#include "problem.h"

static int visited[MAXV];

static int dfs(const Graph *g, int u, int parent) {
    /* TODO
       mark u; for each neighbour v:
         - if v is not visited, recurse with parent = u; if that finds a cycle, report it
         - else if v != parent, you have reached an already-visited vertex by a
           different route -> cycle
       Skipping the parent is what stops the edge you just came along from
       counting as a cycle. */
    return 0;
}

int hasCycle(const Graph *g) {
    /* TODO: clear visited, then try every unvisited vertex (the graph may be
       disconnected) and report 1 if any DFS finds a cycle. */
    return 0;
}
"""

A4 = r"""
#include "problem.h"

static int visited[MAXV];

static int dfs(const Graph *g, int u, int parent) {
    visited[u] = 1;
    for (int i = 0; i < g->deg[u]; i++) {
        int v = g->adj[u][i];
        if (!visited[v]) {
            if (dfs(g, v, u)) return 1;
        } else if (v != parent) {
            return 1;               /* reached a visited vertex another way */
        }
    }
    return 0;
}

int hasCycle(const Graph *g) {
    for (int v = 0; v <= g->n; v++) visited[v] = 0;
    for (int v = 1; v <= g->n; v++)
        if (!visited[v] && dfs(g, v, -1)) return 1;
    return 0;
}
"""

T4 = [graph_input(4, [(1, 2), (2, 3), (3, 4)]),
      graph_input(4, [(1, 2), (2, 3), (3, 4), (4, 1)]),
      graph_input(6, [(1, 2), (2, 3), (4, 5), (5, 6), (6, 4)]),
      graph_input(3, []),
      graph_input(2, [(1, 2)])]
T4 += [graph_input(*rand_graph(4, 9, density=0.2)) for _ in range(5)]

write_problem(
    PACK, UNIT, "p04-cycle-undirected", title="Cycle detection (undirected)",
    mode="function", difficulty="medium", estimated_minutes=12, samples=2,
    topics=["dfs", "cycle", "graph"],
    prereqs=[f"{PACK}.{UNIT}.p03-components"],
    hints=[
        "Pass the vertex you came from as a parameter. An edge back to the parent "
        "is the edge you just walked - it is not a cycle.",
        "Any OTHER edge to an already-visited vertex means two different routes "
        "reach it, which is a cycle.",
        "Wrap it in the for-every-unvisited-vertex loop: the cycle may be in a "
        "component you have not touched yet.",
    ],
    header=H4, harness=M4, starter=S4, solution=A4, tests=T4,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# Cycle detection (undirected)

```c
int hasCycle(const Graph *g);   /* 1 or 0 */
```

The graph may be disconnected.
""" + EDGE_FMT_UNDIR + r"""
## Example

```
4 4
1 2
2 3
3 4
4 1
```

```
1
```

## Why you must pass the parent

In an undirected graph every edge appears twice - `1 2` puts 2 in 1's list *and* 1 in
2's. So when the DFS is at 2 and looks at its neighbours, it sees 1, which is already
visited. That is not a cycle; it is the edge you just arrived on.

Passing `parent` and skipping exactly that one vertex fixes it. Any other edge into an
already-visited vertex genuinely closes a loop.

## The directed case is different

For a directed graph this parent trick is wrong - there you need to know whether the
visited vertex is still **on the current recursion path** (grey) or already finished
(black). Same traversal, different bookkeeping; that is the next problem.
""",
)

# ------------------------------------------------------------------ p05
H5 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + GRAPH_TYPES + PROVIDED + r"""
/* ---- Yours: 1 if the DIRECTED graph contains a cycle, else 0. ---- */
int hasCycleDirected(const Graph *g);

#endif
"""

M5 = r"""
#include <stdio.h>
#include "problem.h"
""" + read_graph(undirected=False) + r"""
int main(void) {
    Graph g;
    readGraph(&g);
    printf("%d\n", hasCycleDirected(&g));
    return 0;
}
"""

S5 = r"""
#include "problem.h"

/* 0 = untouched, 1 = on the current path, 2 = finished */
static int colour[MAXV];

static int dfs(const Graph *g, int u) {
    /* TODO
       colour[u] = 1;
       for each neighbour v:
           if colour[v] == 1 -> v is on the path we are standing on: cycle
           if colour[v] == 0 and dfs(v) found a cycle -> report it
       colour[u] = 2 before returning 0. */
    return 0;
}

int hasCycleDirected(const Graph *g) {
    return 0;   /* TODO: clear colours, try every untouched vertex */
}
"""

A5 = r"""
#include "problem.h"

static int colour[MAXV];

static int dfs(const Graph *g, int u) {
    colour[u] = 1;                       /* on the current path */
    for (int i = 0; i < g->deg[u]; i++) {
        int v = g->adj[u][i];
        if (colour[v] == 1) return 1;    /* back edge to the current path */
        if (colour[v] == 0 && dfs(g, v)) return 1;
    }
    colour[u] = 2;                       /* finished */
    return 0;
}

int hasCycleDirected(const Graph *g) {
    for (int v = 0; v <= g->n; v++) colour[v] = 0;
    for (int v = 1; v <= g->n; v++)
        if (colour[v] == 0 && dfs(g, v)) return 1;
    return 0;
}
"""

T5 = [graph_input(3, [(1, 2), (2, 3), (3, 1)]),
      graph_input(3, [(1, 2), (2, 3), (1, 3)]),
      graph_input(4, [(1, 2), (3, 4), (4, 3)]),
      graph_input(2, [(1, 2), (2, 1)]),
      graph_input(5, [(1, 2), (2, 3), (3, 4), (4, 5)])]
T5 += [graph_input(*rand_graph(3, 8, density=0.25, undirected=False)) for _ in range(5)]

write_problem(
    PACK, UNIT, "p05-cycle-directed", title="Cycle detection (directed): the three colours",
    mode="function", difficulty="medium", estimated_minutes=12, samples=2,
    topics=["dfs", "cycle", "directed graph"],
    prereqs=[f"{PACK}.{UNIT}.p04-cycle-undirected"],
    hints=[
        "A plain visited flag is not enough. You need to distinguish 'currently on "
        "the path I am standing on' from 'explored and finished'.",
        "Three states: 0 untouched, 1 on the current recursion path, 2 finished. "
        "Set 1 on entry and 2 just before returning.",
        "A neighbour coloured 1 is a back edge to something still open above you - "
        "that is the cycle. A neighbour coloured 2 is a finished subtree and is fine.",
    ],
    header=H5, harness=M5, starter=S5, solution=A5, tests=T5,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# Cycle detection (directed): the three colours

```c
int hasCycleDirected(const Graph *g);
```

## Input format

```
n m
u1 v1
...
```

`m` **directed** edges `u -> v`. Only the `u -> v` direction is added.

## Example

```
3 3
1 2
2 3
1 3
```

```
0
```

Three edges and no cycle: `1 -> 3` is a shortcut, not a loop. The undirected version of
the same edge list *would* report a cycle, which is exactly why this needs its own
algorithm.

## Why "visited" alone fails

Consider `1 -> 2`, `1 -> 3`, `2 -> 3`. Exploring from 1 we finish 2 and 3, come back
to 1, and look at `1 -> 3`: vertex 3 is visited. But that is not a cycle - 3 is
*finished*, sitting below us in the DFS tree, not above us on the path.

## Three colours

| Colour | Meaning |
|---|---|
| 0 | not touched yet |
| 1 | on the path currently being explored (entered, not yet returned from) |
| 2 | fully explored, done |

Set `colour[u] = 1` on entry and `colour[u] = 2` just before returning. Hitting a
neighbour coloured **1** means an edge back into the chain you are standing on - a
cycle. Colour **2** is harmless.

This is the same machinery that makes topological sorting possible: a directed graph
has a topological order exactly when it has no cycle.
""",
)

# ------------------------------------------------------------------ p06
H6 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + GRAPH_TYPES + PROVIDED + r"""
/* ---- Yours: a topological order of the DIRECTED graph into order[].
        Among all valid orders, produce the lexicographically smallest one.
        Return 0 (and write nothing) if the graph has a cycle. ---- */
int topoSort(const Graph *g, int order[]);   /* returns n, or 0 if impossible */

#endif
"""

M6 = r"""
#include <stdio.h>
#include "problem.h"
""" + read_graph(undirected=False) + r"""
int main(void) {
    Graph g;
    readGraph(&g);

    int order[MAXV];
    int k = topoSort(&g, order);
    if (k == 0) { printf("IMPOSSIBLE\n"); return 0; }
    for (int i = 0; i < k; i++) printf("%d%s", order[i], i + 1 < k ? " " : "");
    printf("\n");
    return 0;
}
"""

S6 = r"""
#include "problem.h"

int topoSort(const Graph *g, int order[]) {
    int indeg[MAXV] = {0}, used[MAXV] = {0}, count = 0;

    /* TODO - Kahn's algorithm
       1. indeg[v] = number of edges pointing INTO v
       2. repeat n times:
            pick the SMALLEST-numbered vertex with indeg 0 that is not used yet
            if there is none -> the rest is a cycle, return 0
            append it to order[], mark it used, and decrement indeg[] of each of
            its out-neighbours
       Picking the smallest available vertex each round is what makes the result
       lexicographically smallest. n <= 100, so a linear scan is fine. */
    return 0;
}
"""

A6 = r"""
#include "problem.h"

int topoSort(const Graph *g, int order[]) {
    int indeg[MAXV] = {0}, used[MAXV] = {0}, count = 0;

    for (int u = 1; u <= g->n; u++)
        for (int i = 0; i < g->deg[u]; i++) indeg[g->adj[u][i]]++;

    for (int step = 0; step < g->n; step++) {
        int pick = -1;
        for (int v = 1; v <= g->n; v++)
            if (!used[v] && indeg[v] == 0) { pick = v; break; }   /* smallest first */

        if (pick == -1) return 0;                                  /* cycle */
        used[pick] = 1;
        order[count++] = pick;
        for (int i = 0; i < g->deg[pick]; i++) indeg[g->adj[pick][i]]--;
    }
    return count;
}
"""

T6 = [graph_input(6, [(5, 2), (5, 0 + 1), (4, 0 + 1), (4, 3), (2, 3), (3, 6)]),
      graph_input(3, [(1, 2), (2, 3), (3, 1)]),
      graph_input(4, []),
      graph_input(5, [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5)]),
      graph_input(4, [(2, 1), (3, 1), (4, 1)])]
T6 += [graph_input(*rand_graph(3, 8, density=0.22, undirected=False)) for _ in range(5)]

write_problem(
    PACK, UNIT, "p06-topological-sort", title="Topological sort (Kahn), lexicographically smallest",
    mode="function", difficulty="medium", estimated_minutes=15, samples=2,
    topics=["topological sort", "directed graph", "indegree"],
    prereqs=[f"{PACK}.{UNIT}.p05-cycle-directed"],
    source="DSA theory: DFS/BFS applications",
    hints=[
        "indeg[v] counts edges pointing INTO v. Build it by looping over every "
        "vertex's adjacency list and incrementing the target.",
        "Each round: take a vertex with indeg 0, output it, and decrement the "
        "indegree of everything it points to - as if deleting it from the graph.",
        "If at some round no vertex has indeg 0 but vertices remain, what is left "
        "must contain a cycle, so return 0. That doubles as cycle detection.",
    ],
    header=H6, harness=M6, starter=S6, solution=A6, tests=T6,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# Topological sort (Kahn), lexicographically smallest

An ordering of the vertices such that every edge `u -> v` has `u` before `v`. Among all
valid orders, print the **lexicographically smallest**.

```c
int topoSort(const Graph *g, int order[]);   /* returns n, or 0 if impossible */
```

## Input format

```
n m
u1 v1
...
```

`m` **directed** edges. Print the order, or `IMPOSSIBLE` if the graph has a cycle.

## Example

```
5 5
1 2
1 3
2 4
3 4
4 5
```

```
1 2 3 4 5
```

## Kahn's algorithm

Count `indeg[v]`, the number of edges pointing into `v`. A vertex with indegree 0 has
no unmet prerequisite, so it can go next. Output it, then decrement the indegree of
everything it points to - as though deleting it from the graph - and repeat.

If a round finds no vertex with indegree 0 while vertices remain, every remaining
vertex depends on another remaining one, which can only happen if there is a **cycle**.
So Kahn's algorithm detects cycles for free.

## Getting the smallest order

Whenever several vertices have indegree 0, any of them is valid - so pick the
**smallest-numbered** one. With `n <= 100` a linear scan for the smallest available
vertex is completely fine and much easier to get right than a heap.
""",
)

# ------------------------------------------------------------------ p07
H7 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + GRAPH_TYPES + PROVIDED + r"""
/* ---- Yours: 1 if the graph is bipartite, else 0.
        On success colour[v] must be 0 or 1 for every vertex, and in each
        component the smallest-numbered vertex must get colour 0. ---- */
int bipartite(const Graph *g, int colour[]);

#endif
"""

M7 = r"""
#include <stdio.h>
#include "problem.h"
""" + read_graph() + r"""
int main(void) {
    Graph g;
    readGraph(&g);

    int colour[MAXV];
    if (!bipartite(&g, colour)) { printf("-1\n"); return 0; }
    for (int c = 0; c <= 1; c++) {
        int first = 1;
        for (int v = 1; v <= g.n; v++)
            if (colour[v] == c) { printf(first ? "%d" : " %d", v); first = 0; }
        printf("\n");
    }
    return 0;
}
"""

S7 = r"""
#include "problem.h"

int bipartite(const Graph *g, int colour[]) {
    /* TODO
       - colour[v] = -1 for "uncoloured"
       - for every still-uncoloured vertex (the graph may be disconnected):
           give it colour 0 and BFS/DFS from it
           every neighbour must get the OPPOSITE colour
           if a neighbour already has the SAME colour as the current vertex -> not
           bipartite, return 0
       - return 1 if you get through the whole graph */
    return 0;
}
"""

A7 = r"""
#include "problem.h"

int bipartite(const Graph *g, int colour[]) {
    int queue[MAXV];

    for (int v = 0; v <= g->n; v++) colour[v] = -1;

    for (int s = 1; s <= g->n; s++) {
        if (colour[s] != -1) continue;
        int head = 0, tail = 0;
        colour[s] = 0;                    /* smallest vertex of the component */
        queue[tail++] = s;

        while (head < tail) {
            int u = queue[head++];
            for (int i = 0; i < g->deg[u]; i++) {
                int v = g->adj[u][i];
                if (colour[v] == -1) {
                    colour[v] = 1 - colour[u];
                    queue[tail++] = v;
                } else if (colour[v] == colour[u]) {
                    return 0;             /* an edge inside one side */
                }
            }
        }
    }
    return 1;
}
"""

T7 = [graph_input(4, [(1, 2), (2, 3), (3, 4), (4, 1)]),
      graph_input(3, [(1, 2), (2, 3), (3, 1)]),
      graph_input(6, [(1, 2), (2, 3), (4, 5)]),
      graph_input(5, []),
      graph_input(2, [(1, 2)]),
      graph_input(5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])]
T7 += [graph_input(*rand_graph(4, 9, density=0.2)) for _ in range(4)]

write_problem(
    PACK, UNIT, "p07-bipartite", title="Bipartite check by 2-colouring",
    mode="function", difficulty="medium", estimated_minutes=14, samples=2,
    topics=["bfs", "bipartite", "graph"],
    prereqs=[f"{PACK}.{UNIT}.p03-components"],
    source="Core of the DSA Lab Week 3 evaluation question",
    hints=[
        "Colour the start vertex 0, then every neighbour gets 1 - colour[u]. "
        "That single expression flips 0 and 1.",
        "Use colour[v] == -1 as the visited test - one array does both jobs.",
        "Check for a conflict when the neighbour is ALREADY coloured: if it has the "
        "same colour as the current vertex, an edge joins two vertices on the same "
        "side and the graph is not bipartite.",
    ],
    header=H7, harness=M7, starter=S7, solution=A7, tests=T7,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# Bipartite check by 2-colouring

A graph is bipartite when its vertices can be split into two sets with **every edge
going between the sets**, never inside one.

```c
int bipartite(const Graph *g, int colour[]);
```

Return 1 and fill `colour[]` with 0/1, or return 0. In each component the
smallest-numbered vertex must take colour 0, so the answer is unique.
""" + EDGE_FMT_UNDIR + r"""
## Output

The two colour classes, one per line (colour 0 then colour 1), each ascending -
or `-1` if the graph is not bipartite.

## Example

```
4 4
1 2
2 3
3 4
4 1
```

```
1 3
2 4
```

A 4-cycle alternates fine. A 3-cycle does not, and prints `-1`.

## The algorithm

Traverse (BFS or DFS). Give the start vertex colour 0 and every neighbour the opposite
colour, `1 - colour[u]`. If you meet an already-coloured neighbour that has the **same**
colour as the vertex you are standing on, that edge joins two vertices on the same
side - not bipartite.

`colour[v] == -1` doubles as "not visited", so you need only one array.

## Do not forget the disconnected case

The graph need not be connected, so wrap the traversal in the for-every-uncoloured-
vertex loop. A graph is bipartite only if *every* component is.

## The theory fact worth remembering

A graph is bipartite **iff it contains no odd-length cycle**. The colouring is just a
constructive way of checking that.
""",
)

# ------------------------------------------------------------------ p08
A8 = r"""
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
"""

S8 = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXV 105

int main(void) {
    /* TODO: the whole program.
       Parse the adjacency-list lines with fgets + strtok (NOT character by
       character with %c - that is what loses marks to a trailing space),
       then 2-colour the graph with a stack-based DFS. */
    return 0;
}
"""


def bipartite_lines(n, edges, trailing=False, blank=False):
    adj = {u: set() for u in range(1, n + 1)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    out = [str(n)]
    for u in range(1, n + 1):
        nbrs = sorted(adj[u])
        rng.shuffle(nbrs)
        row = " ".join(str(x) for x in [u] + nbrs)
        if trailing:
            row += "   "
        out.append(row)
        if blank and u == 1:
            out.append("")
    return "\n".join(out) + "\n"


T8 = [bipartite_lines(4, [(1, 2), (2, 3), (3, 4), (4, 1)]),
      bipartite_lines(3, [(1, 2), (2, 3), (3, 1)]),
      bipartite_lines(6, [(1, 2), (2, 3), (4, 5)], trailing=True),
      bipartite_lines(5, [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]),
      bipartite_lines(4, [(1, 2), (3, 4)], blank=True),
      bipartite_lines(1, []),
      bipartite_lines(7, [(1, 2), (1, 3), (2, 4), (3, 4), (5, 6), (6, 7)], trailing=True)]
for _ in range(4):
    n, e = rand_graph(4, 9, density=0.2)
    T8.append(bipartite_lines(n, e, trailing=rng.random() < 0.5))

write_problem(
    PACK, UNIT, "p08-bipartite-program", title="Week 3 evaluation: bipartite from adjacency lines",
    mode="program", difficulty="hard", estimated_minutes=30, samples=2,
    topics=["dfs", "stack", "bipartite", "parsing"],
    prereqs=[f"{PACK}.{UNIT}.p07-bipartite", f"{PACK}.{UNIT}.p02-dfs-iterative"],
    source="Reconstruction of the DSA Lab Week 3 evaluation question (Aug 2026)",
    hints=[
        "Do the parsing first and print the adjacency lists back out to check it "
        "before writing any colouring code.",
        "fgets the whole line, then strtok(line, \" \\t\\r\\n\"). Giving strtok all "
        "four delimiters is what makes trailing spaces and \\r harmless.",
        "After scanf(\"%d\", &n) consume the rest of that line, or your first fgets "
        "returns an empty string and every vertex shifts by one.",
    ],
    starter=S8, solution=A8, tests=T8,
    statement=r"""
# Week 3 evaluation: bipartite from adjacency lines

> Read a graph given as adjacency-list lines, where each line begins with a vertex
> followed by its neighbours. Determine whether the graph is bipartite using DFS
> implemented with a stack. If it is, print the two colour sets; otherwise print `-1`.

**This is a reconstruction**, not the official sheet - the wording is from memory of
the Week 3 evaluation. The algorithm and the parsing are what matter, and both are
exactly what that question tested.

## Input format

- first line: the number of vertices `n`
- next `n` lines: `u v1 v2 v3 ...` - vertex `u` followed by its neighbours, in any order

The graph is undirected; each edge appears in both endpoints' lines. A vertex with no
neighbours appears alone on its line.

## Output format

Two lines: the vertices of colour 0 then the vertices of colour 1, each ascending and
space separated. In every component the smallest-numbered vertex takes colour 0. Print
`-1` if the graph is not bipartite.

## Example

```
4
1 2 4
2 1 3
3 2 4
4 1 3
```

```
1 3
2 4
```

## The parsing is the marks

You lost a test case on this question to `%c` parsing tripping over a **trailing
space**. Several tests here have trailing spaces, and one has a blank line, precisely
so that a fragile parser fails locally instead of in the exam.

The robust recipe:

```c
int ch; while ((ch = getchar()) != '\n' && ch != EOF) { }   /* after scanf("%d", &n) */
...
fgets(line, sizeof line, stdin);
char *tok = strtok(line, " \t\r\n");        /* all four delimiters */
if (tok == NULL) continue;                  /* blank line - do not count it */
```

`strtok` with that delimiter set collapses any run of spaces, tabs and carriage
returns, so trailing whitespace produces no phantom token at all. Reading character by
character and deciding what a space means yourself is how a single stray byte costs
two marks.

## The algorithm

Stack-based DFS, colouring each neighbour `1 - colour[u]`, with the
for-every-uncoloured-vertex loop around it so disconnected graphs work.
""",
)

report(UNIT, 8)
