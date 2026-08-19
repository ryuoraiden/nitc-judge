"""Unit 04 - BFS.  Run: python scripts/authoring/unit_04_bfs.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report

PACK = "c-s3"
UNIT = "04-bfs"

write_unit(PACK, UNIT, "BFS and shortest paths",
           "Adjacency lists, then BFS order, distances, path reconstruction, and finally "
           "the lexicographic rule from Week 4 Practice Question 1.")

# Shared header fragment for the problems that get a prebuilt graph.
GRAPH_TYPES = r"""
#define MAXV 105

/* Vertices are numbered 1..n.  adj[u][0..deg[u]-1] holds u's out-neighbours,
   kept in ascending order by sortNeighbours(). */
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

READ_GRAPH = r"""
static void readGraph(Graph *g) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return;
    graphInit(g, n);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (scanf("%d %d", &u, &v) != 2) return;
        addEdge(g, u, v);
    }
    sortNeighbours(g);
}
"""

EDGE_FORMAT = r"""
## Input format

```
n m
u1 v1
u2 v2
...
s
```

`n` vertices numbered `1..n`, `m` directed edges `u -> v`, then the source `s`.
The graph is built and its adjacency lists sorted ascending before your function
is called.
"""

# --------------------------------------------------------------- p01
H1 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
""" + GRAPH_TYPES + r"""
void graphInit(Graph *g, int n);
void addEdge(Graph *g, int u, int v);   /* directed edge u -> v */
void sortNeighbours(Graph *g);          /* each adjacency list ascending */
void printAdj(const Graph *g);

#endif
"""

M1 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;

    Graph g;
    graphInit(&g, n);
    for (int i = 0; i < m; i++) {
        int u, v;
        if (scanf("%d %d", &u, &v) != 2) return 0;
        addEdge(&g, u, v);
    }
    sortNeighbours(&g);
    printAdj(&g);
    return 0;
}
"""

S1 = r"""
#include <stdio.h>
#include <stdlib.h>
#include "problem.h"

void graphInit(Graph *g, int n) {
    /* TODO: record n, and set every degree to zero.
       Vertices run 1..n, so do not forget index n itself. */
}

void addEdge(Graph *g, int u, int v) {
    /* TODO: append v to u's list and grow deg[u]. One line. */
}

static int cmpInt(const void *a, const void *b) {
    /* TODO: qsort comparator for ints - negative, zero or positive. */
    return 0;
}

void sortNeighbours(Graph *g) {
    /* TODO: qsort each vertex's list.
       qsort(g->adj[u], g->deg[u], sizeof(int), cmpInt); */
}

void printAdj(const Graph *g) {
    /* TODO: one line per vertex 1..n:
         "u:" followed by " v" for each neighbour, then a newline.
       A vertex with no out-edges prints just "u:". */
}
"""

A1 = r"""
#include <stdio.h>
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
    return (x > y) - (x < y);   /* no overflow, unlike x - y */
}

void sortNeighbours(Graph *g) {
    for (int u = 1; u <= g->n; u++)
        qsort(g->adj[u], g->deg[u], sizeof(int), cmpInt);
}

void printAdj(const Graph *g) {
    for (int u = 1; u <= g->n; u++) {
        printf("%d:", u);
        for (int i = 0; i < g->deg[u]; i++) printf(" %d", g->adj[u][i]);
        printf("\n");
    }
}
"""

T1 = [
    "5 8\n1 3\n1 4\n2 4\n2 5\n3 1\n3 4\n4 1\n4 2\n",
    "4 3\n1 2\n1 3\n1 4\n",
    "3 0\n",
    "6 6\n6 1\n6 3\n6 2\n1 6\n3 6\n2 6\n",
    "4 6\n4 3\n4 1\n4 2\n1 4\n2 1\n3 2\n",
]

write_problem(
    PACK, UNIT, "p01-adjacency-list", title="Build an adjacency list",
    mode="function", difficulty="easy", estimated_minutes=8, samples=1,
    topics=["graph", "adjacency list"],
    source="Representation used throughout NITC_Lab_S3_DSA Week 3 - Graphs",
    hints=[
        "graphInit must clear deg[] for indices 0..n inclusive, because vertices "
        "are numbered from 1 and index n is a real vertex.",
        "addEdge is one line: g->adj[u][g->deg[u]++] = v; The post-increment stores "
        "at the current end and then grows the list.",
        "Write the comparator as (x > y) - (x < y) rather than x - y. The "
        "subtraction overflows for large values; the comparison form never does.",
    ],
    header=H1, harness=M1, starter=S1, solution=A1, tests=T1,
    statement=r"""
# Build an adjacency list

Before any traversal, you need somewhere to put the graph. Four small functions.

```c
typedef struct {
    int n;
    int deg[MAXV];
    int adj[MAXV][MAXV];
} Graph;
```

Vertices are numbered **1..n**. `adj[u]` holds `u`'s out-neighbours and `deg[u]`
says how many there are.

## Input format

```
n m
u1 v1
...
```

`m` directed edges. Build the graph, sort every adjacency list ascending, print it.

## Output format

One line per vertex `1..n`: the vertex, a colon, then each neighbour preceded by a
space. A vertex with no out-edges prints just `u:`.

## Example

```
5 8
1 3
1 4
2 4
2 5
3 1
3 4
4 1
4 2
```

```
1: 3 4
2: 4 5
3: 1 4
4: 1 2
5:
```

## Why sorted order matters later

Keeping each list ascending looks like tidiness. It is not - it is load-bearing.
Three problems from now you will need the *lexicographically smallest* shortest
path, and the entire trick turns out to be "visit neighbours in ascending order and
take the first parent that discovers each vertex". Sorting here is what makes that
work. Get it right once and it stays right.

## A comparator detail worth keeping

The obvious `return x - y;` comparator is subtly broken: for large values the
subtraction overflows and the sign comes out wrong. `return (x > y) - (x < y);`
gives the same three-way answer and cannot overflow.
""",
)

# --------------------------------------------------------------- p02
H2 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
""" + GRAPH_TYPES + r"""
/* Provided for you. */
void graphInit(Graph *g, int n);
void addEdge(Graph *g, int u, int v);
void sortNeighbours(Graph *g);

/* Yours: write the BFS visit order starting at s into order[],
   and return how many vertices were visited. */
int bfsOrder(const Graph *g, int s, int order[]);

#endif
"""

M2 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_GRAPH + r"""
int main(void) {
    Graph g;
    readGraph(&g);
    int s;
    if (scanf("%d", &s) != 1) return 0;

    int order[MAXV];
    int count = bfsOrder(&g, s, order);

    for (int i = 0; i < count; i++) printf("%d%s", order[i], i + 1 < count ? " " : "");
    printf("\n");
    return 0;
}
"""

S2 = r"""
#include "problem.h"

int bfsOrder(const Graph *g, int s, int order[]) {
    int visited[MAXV] = {0};
    int queue[MAXV];
    int head = 0, tail = 0;

    /* TODO
       1. mark s visited and put it in the queue
       2. while the queue is not empty: take the front vertex u, append it to
          order[], and for each neighbour v of u that is not yet visited,
          mark it visited and push it
       3. return how many vertices you appended

       Mark visited when you ENQUEUE, not when you dequeue - see the statement. */

    return 0;
}
"""

A2 = r"""
#include "problem.h"

int bfsOrder(const Graph *g, int s, int order[]) {
    int visited[MAXV] = {0};
    int queue[MAXV];
    int head = 0, tail = 0;
    int count = 0;

    visited[s] = 1;
    queue[tail++] = s;

    while (head < tail) {
        int u = queue[head++];
        order[count++] = u;

        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->adj[u][i];
            if (!visited[v]) {
                visited[v] = 1;      /* on enqueue, not on dequeue */
                queue[tail++] = v;
            }
        }
    }
    return count;
}
"""

T2 = [
    "5 8\n1 3\n1 4\n2 4\n2 5\n3 1\n3 4\n4 1\n4 2\n1\n",
    "6 6\n1 2\n1 3\n2 4\n3 4\n4 5\n5 6\n1\n",
    "4 2\n1 2\n3 4\n1\n",
    "7 8\n1 2\n1 3\n1 4\n2 5\n3 5\n4 6\n5 7\n6 7\n1\n",
    "5 4\n2 1\n3 2\n4 3\n5 4\n5\n",
    "3 3\n1 1\n1 2\n2 3\n1\n",
]

write_problem(
    PACK, UNIT, "p02-bfs-order", title="BFS visit order",
    mode="function", difficulty="easy", estimated_minutes=10, samples=1,
    topics=["bfs", "queue", "graph"],
    prereqs=[f"{PACK}.{UNIT}.p01-adjacency-list",
             f"{PACK}.02-queue.p01-array-queue"],
    source="Rebuilt from NITC_Lab_S3_DSA Week 3 - Graphs (BFSTraversal)",
    hints=[
        "The queue is just an array with two indices: head and tail. "
        "head < tail means 'not empty'. No wraparound needed - each vertex is "
        "enqueued at most once, so MAXV slots are always enough.",
        "Append u to order[] when you DEQUEUE it, and mark neighbours visited when "
        "you ENQUEUE them.",
        "If you mark visited on dequeue instead of on enqueue, a vertex with two "
        "in-edges gets queued twice and appears twice in the output.",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# BFS visit order

The graph is built and sorted for you. Write the traversal.

```c
int bfsOrder(const Graph *g, int s, int order[]);
```

Fill `order[]` with the vertices in the order BFS visits them, and return the
count. Only vertices reachable from `s` appear.
""" + EDGE_FORMAT + r"""
## Example

```
5 8
1 3
1 4
2 4
2 5
3 1
3 4
4 1
4 2
1
```

```
1 3 4 2 5
```

From 1 we reach 3 and 4 (ascending). From 3, nothing new. From 4 we reach 2. From
2 we reach 5.

## The bug this problem exists to catch

Mark a vertex visited **when you enqueue it**, not when you dequeue it.

If you only mark on dequeue, consider a vertex `v` with edges into it from both `a`
and `b`, where `a` and `b` are both in the queue. `a` is processed and pushes `v`.
Then `b` is processed - `v` is still unmarked, so `b` pushes `v` again. Now `v` is
in the queue twice and appears twice in your output.

It is a two-line difference and it only shows up on graphs where some vertex has
two in-edges - so a chain or a tree will pass happily while a real graph fails.
Test 4 has exactly that shape.

## The queue

`head` and `tail` indices into a plain array. `head < tail` means non-empty. No
wraparound is needed here: each vertex is enqueued at most once, so the array never
needs to reuse a slot.
""",
)

# --------------------------------------------------------------- p03
H3 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
""" + GRAPH_TYPES + r"""
void graphInit(Graph *g, int n);
void addEdge(Graph *g, int u, int v);
void sortNeighbours(Graph *g);

/* Yours: dist[v] = number of edges on a shortest s->v path, or -1 if
   v cannot be reached.  dist[s] is 0. */
void bfsDistances(const Graph *g, int s, int dist[]);

#endif
"""

M3 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_GRAPH + r"""
int main(void) {
    Graph g;
    readGraph(&g);
    int s;
    if (scanf("%d", &s) != 1) return 0;

    int dist[MAXV];
    bfsDistances(&g, s, dist);

    for (int v = 1; v <= g.n; v++) printf("%d%s", dist[v], v < g.n ? " " : "");
    printf("\n");
    return 0;
}
"""

S3 = r"""
#include "problem.h"

void bfsDistances(const Graph *g, int s, int dist[]) {
    /* TODO
       1. set every dist[v] to -1 (meaning "not reached yet")
       2. dist[s] = 0, enqueue s
       3. when you discover an unvisited neighbour v of u:
              dist[v] = dist[u] + 1
          and enqueue it
       dist[v] != -1 doubles as your visited flag - no separate array needed. */
}
"""

A3 = r"""
#include "problem.h"

void bfsDistances(const Graph *g, int s, int dist[]) {
    for (int v = 0; v <= g->n; v++) dist[v] = -1;

    int queue[MAXV];
    int head = 0, tail = 0;

    dist[s] = 0;
    queue[tail++] = s;

    while (head < tail) {
        int u = queue[head++];
        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->adj[u][i];
            if (dist[v] == -1) {          /* -1 means undiscovered */
                dist[v] = dist[u] + 1;
                queue[tail++] = v;
            }
        }
    }
}
"""

T3 = [
    "5 8\n1 3\n1 4\n2 4\n2 5\n3 1\n3 4\n4 1\n4 2\n1\n",
    "6 5\n1 2\n2 3\n3 4\n4 5\n5 6\n1\n",
    "5 3\n1 2\n1 3\n4 5\n1\n",
    "7 8\n1 2\n1 3\n1 4\n2 5\n3 5\n4 6\n5 7\n6 7\n1\n",
    "4 4\n1 2\n2 3\n3 4\n4 1\n3\n",
    "3 0\n2\n",
]

write_problem(
    PACK, UNIT, "p03-bfs-distances", title="BFS distances (and why BFS gives shortest paths)",
    mode="function", difficulty="easy", estimated_minutes=8, samples=1,
    topics=["bfs", "shortest path"],
    prereqs=[f"{PACK}.{UNIT}.p02-bfs-order"],
    source="Foundation for Week 4 Practice Question 1",
    hints=[
        "You do not need a separate visited[] array. dist[v] == -1 already means "
        "'not discovered yet', so one array does both jobs.",
        "The update is dist[v] = dist[u] + 1 at the moment you discover v, where u "
        "is the vertex you are currently expanding.",
        "Initialise dist for indices 0..n so that vertex n is covered - vertices "
        "are 1-based here.",
    ],
    header=H3, harness=M3, starter=S3, solution=A3, tests=T3,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# BFS distances (and why BFS gives shortest paths)

```c
void bfsDistances(const Graph *g, int s, int dist[]);
```

`dist[v]` is the number of edges on a shortest path from `s` to `v`, `0` for `s`
itself, and `-1` if `v` is unreachable.
""" + EDGE_FORMAT + r"""
## Output

`dist[1] dist[2] ... dist[n]` on one line, space separated.

## Example

```
5 8
1 3
1 4
2 4
2 5
3 1
3 4
4 1
4 2
1
```

```
0 2 1 1 3
```

## One array, two jobs

You do not need a `visited[]` array here. `dist[v] == -1` already means "not
discovered yet". Initialise everything to `-1`, set `dist[s] = 0`, and the check
`if (dist[v] == -1)` does exactly the work `if (!visited[v])` would have.

## Why the first time you reach a vertex is the shortest time

BFS pulls vertices out of the queue in non-decreasing order of distance: everything
at distance `d` comes out before anything at distance `d+1`. So the first time `v`
is discovered, it is discovered from some `u` at the smallest possible distance, and
`dist[u] + 1` is genuinely minimal.

That guarantee is exactly what breaks once edges have different weights - a
two-edge path can be cheaper than a one-edge path - and that is the reason
Dijkstra has to exist at all. You will meet it in the next unit.
""",
)

# --------------------------------------------------------------- p04
H4 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
""" + GRAPH_TYPES + r"""
void graphInit(Graph *g, int n);
void addEdge(Graph *g, int u, int v);
void sortNeighbours(Graph *g);

/* Yours: write a shortest s->t path into path[] (from s to t, in that order)
   and return its length in vertices.  Return 0 if t is unreachable.
   If s == t the path is just s, length 1. */
int bfsPath(const Graph *g, int s, int t, int path[]);

#endif
"""

M4 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_GRAPH + r"""
int main(void) {
    Graph g;
    readGraph(&g);
    int s, t;
    if (scanf("%d %d", &s, &t) != 2) return 0;

    int path[MAXV];
    int len = bfsPath(&g, s, t, path);

    if (len == 0) {
        printf("NO PATH\n");
    } else {
        for (int i = 0; i < len; i++) printf("%d%s", path[i], i + 1 < len ? "-" : "");
        printf("\n");
    }
    return 0;
}
"""

S4 = r"""
#include "problem.h"

int bfsPath(const Graph *g, int s, int t, int path[]) {
    int parent[MAXV];
    /* TODO
       1. BFS from s, recording parent[v] = the vertex you discovered v from.
          Use parent[s] = -1 (or 0) as the stop marker.
       2. if t was never discovered, return 0
       3. walk backwards from t via parent[] - that gives the path REVERSED -
          then reverse it into path[] so it reads s .. t
       4. return the number of vertices written */
    (void)parent;
    return 0;
}
"""

A4 = r"""
#include "problem.h"

int bfsPath(const Graph *g, int s, int t, int path[]) {
    int parent[MAXV];
    int seen[MAXV];
    for (int v = 0; v <= g->n; v++) { parent[v] = -1; seen[v] = 0; }

    int queue[MAXV];
    int head = 0, tail = 0;
    seen[s] = 1;
    queue[tail++] = s;

    while (head < tail) {
        int u = queue[head++];
        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->adj[u][i];
            if (!seen[v]) {
                seen[v] = 1;
                parent[v] = u;
                queue[tail++] = v;
            }
        }
    }

    if (!seen[t]) return 0;

    /* Collect t -> s, which comes out reversed. */
    int stack[MAXV], len = 0;
    for (int x = t; x != -1; x = parent[x]) stack[len++] = x;

    for (int i = 0; i < len; i++) path[i] = stack[len - 1 - i];
    return len;
}
"""

T4 = [
    "5 8\n1 3\n1 4\n2 4\n2 5\n3 1\n3 4\n4 1\n4 2\n1 5\n",
    "5 8\n1 3\n1 4\n2 4\n2 5\n3 1\n3 4\n4 1\n4 2\n1 1\n",
    "5 3\n1 2\n1 3\n4 5\n1 5\n",
    "6 6\n1 2\n1 3\n2 4\n3 4\n4 5\n5 6\n1 6\n",
    "7 8\n1 2\n1 3\n1 4\n2 5\n3 5\n4 6\n5 7\n6 7\n1 7\n",
    "4 4\n1 2\n2 3\n3 4\n4 1\n3 2\n",
]

write_problem(
    PACK, UNIT, "p04-bfs-path", title="Reconstruct the path with a parent array",
    mode="function", difficulty="medium", estimated_minutes=12, samples=2,
    topics=["bfs", "shortest path", "path reconstruction"],
    prereqs=[f"{PACK}.{UNIT}.p03-bfs-distances"],
    source="Foundation for Week 4 Practice Question 1",
    hints=[
        "During BFS record parent[v] = u at the same moment you mark v discovered. "
        "One extra line inside the loop you already wrote.",
        "Walking parent[] from t gives you the path backwards. Collect it into a "
        "temporary array, then copy it into path[] in reverse.",
        "Use parent[s] = -1 as the terminator, and stop the walk when x becomes -1. "
        "The loop 'for (int x = t; x != -1; x = parent[x])' does the whole traversal.",
    ],
    header=H4, harness=M4, starter=S4, solution=A4, tests=T4,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# Reconstruct the path with a parent array

Distances tell you *how far*. This tells you *which way*.

```c
int bfsPath(const Graph *g, int s, int t, int path[]);
```

Write a shortest `s -> t` path into `path[]` in order from `s` to `t`, and return
its length in vertices. Return `0` if `t` is unreachable. If `s == t`, the path is
just `s` and the length is `1`.
""" + EDGE_FORMAT.replace("then the source `s`", "then `s` and `t`") + r"""
## Output

The path with `-` between vertices, or `NO PATH`.

## Example

```
5 8
1 3
1 4
2 4
2 5
3 1
3 4
4 1
4 2
1 5
```

```
1-4-2-5
```

## The idea

BFS already knows the path - it just is not writing it down. Add one line: at the
moment you discover `v` from `u`, record `parent[v] = u`.

Afterwards, start at `t` and follow `parent` repeatedly until you fall off the
start. That walk hands you the path **backwards**, so collect it into a scratch
array and reverse it on the way out.

```c
for (int x = t; x != -1; x = parent[x]) stack[len++] = x;
```

Set `parent[s] = -1` so the walk terminates, and make sure every entry starts at
`-1` so an unreachable vertex cannot be mistaken for a discovered one.

## Where this is heading

You now have every piece of Week 4 Practice Question 1 except one rule about
*which* parent to keep when a vertex could be discovered from several. That rule is
the next problem.
""",
)

# --------------------------------------------------------------- p05
H5 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
""" + GRAPH_TYPES + r"""
void graphInit(Graph *g, int n);
void addEdge(Graph *g, int u, int v);
void sortNeighbours(Graph *g);   /* already called: adjacency lists are ascending */

/* Yours: fill parent[] so that following it back from any reachable vertex v
   spells out the lexicographically smallest shortest path from s to v.
   parent[s] must be -1.  Leave parent[v] = -1 for unreachable v too. */
void lexShortestPaths(const Graph *g, int s, int parent[]);

#endif
"""

M5 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_GRAPH + r"""
int main(void) {
    Graph g;
    readGraph(&g);
    int s;
    if (scanf("%d", &s) != 1) return 0;

    int parent[MAXV];
    for (int v = 0; v <= g.n; v++) parent[v] = -1;

    lexShortestPaths(&g, s, parent);

    for (int v = 1; v <= g.n; v++) {
        if (v != s && parent[v] == -1) { printf("-1\n"); continue; }
        int stack[MAXV], len = 0;
        for (int x = v; x != -1; x = parent[x]) stack[len++] = x;
        for (int i = len - 1; i >= 0; i--)
            printf("%d%s", stack[i], i > 0 ? "-" : "");
        printf("\n");
    }
    return 0;
}
"""

S5 = r"""
#include "problem.h"

void lexShortestPaths(const Graph *g, int s, int parent[]) {
    /* TODO: this is ordinary BFS with parent recording - the same loop you
       wrote in the previous problem.

       The lexicographic rule needs NO extra comparison code. Read the
       statement to see why sorted adjacency lists plus first-discovery-wins
       is already exactly the right answer. */
}
"""

A5 = r"""
#include "problem.h"

void lexShortestPaths(const Graph *g, int s, int parent[]) {
    int seen[MAXV];
    for (int v = 0; v <= g->n; v++) seen[v] = 0;

    int queue[MAXV];
    int head = 0, tail = 0;

    seen[s] = 1;
    parent[s] = -1;
    queue[tail++] = s;

    while (head < tail) {
        int u = queue[head++];
        /* g->adj[u] is ascending, so neighbours are offered smallest-first. */
        for (int i = 0; i < g->deg[u]; i++) {
            int v = g->adj[u][i];
            if (!seen[v]) {
                seen[v] = 1;
                parent[v] = u;   /* first discovery wins, and it is the best one */
                queue[tail++] = v;
            }
        }
    }
}
"""

T5 = [
    "5 8\n1 3\n1 4\n2 4\n2 5\n3 1\n3 4\n4 1\n4 2\n1\n",
    "4 4\n1 2\n1 3\n2 4\n3 4\n1\n",
    "6 7\n1 3\n1 2\n2 4\n3 4\n4 5\n2 5\n5 6\n1\n",
    "5 4\n1 2\n1 3\n2 4\n3 4\n1\n",
    "7 9\n1 4\n1 2\n1 3\n2 5\n3 5\n4 5\n5 6\n6 7\n4 7\n1\n",
    "5 3\n1 2\n2 3\n4 5\n1\n",
]

write_problem(
    PACK, UNIT, "p05-lex-smallest-paths",
    title="Lexicographically smallest shortest paths",
    mode="function", difficulty="medium", estimated_minutes=14, samples=2,
    topics=["bfs", "shortest path", "lexicographic order"],
    prereqs=[f"{PACK}.{UNIT}.p04-bfs-path"],
    source="Core of NITC_Lab_S3_DSA Week 4 Practice Question 1",
    hints=[
        "Do not write a path comparison. Plain BFS with parent recording, over "
        "adjacency lists that are already sorted, is the entire answer.",
        "Think about the order vertices enter the queue. Within one BFS level, is "
        "that order related to the lexicographic order of their paths?",
        "Induction: if level-d vertices enter the queue in lexicographic order of "
        "their paths, then expanding them in that order, each with ascending "
        "neighbours, makes level d+1 enter in lexicographic order too.",
    ],
    header=H5, harness=M5, starter=S5, solution=A5, tests=T5,
    extra={"graph_build.c": GRAPH_BUILD},
    statement=r"""
# Lexicographically smallest shortest paths

This is the rule at the heart of Week 4 Practice Question 1.

When several shortest paths tie, you must report the **lexicographically smallest**
one: compare the two vertex sequences position by position, and the one with the
smaller vertex at the first difference wins.

```c
void lexShortestPaths(const Graph *g, int s, int parent[]);
```

Fill `parent[]` so that walking it back from any reachable `v` spells the
lexicographically smallest shortest path. `parent[s] = -1`, and `-1` for
unreachable vertices too.
""" + EDGE_FORMAT + r"""
## Output

One line per vertex `1..n`: the path from `s`, joined by `-`. Unreachable prints
`-1`.

## Example

```
5 8
1 3
1 4
2 4
2 5
3 1
3 4
4 1
4 2
1
```

```
1
1-4-2
1-3
1-4
1-4-2-5
```

## Now stop and think before you code

The instinct is to compare candidate paths whenever a vertex could be reached from
two different parents. **Do not.** Plain BFS with `parent[v] = u` on first discovery
already produces the lexicographically smallest path - provided each adjacency list
is ascending, which the builder guarantees.

Here is the argument, and it is worth following rather than taking on trust.

All shortest paths to a level-`d` vertex have the same length, so comparing them
lexicographically means comparing them position by position over equal lengths.

*Base:* level 1 vertices are the neighbours of `s`, and they enter the queue in
ascending order. Their paths are `s-v`, so queue order is lexicographic order.

*Step:* suppose every vertex at level `d` entered the queue in lexicographic order
of its path. BFS expands them in exactly that order. When we expand `u`, we offer
its neighbours in ascending order. A level-`d+1` vertex `w` discovered from `u` gets
the path `path(u) + w`. If `u1` was queued before `u2` then `path(u1) < path(u2)`,
and since both have the same length, appending anything preserves that order. Within
a single `u`, smaller `w` comes first. So level `d+1` also enters the queue in
lexicographic order - and the first parent to claim each vertex is the best one.

The rule you actually implement: **sort the adjacency lists, and let first discovery
win.** No path comparison anywhere.
""",
)

# --------------------------------------------------------------- p06
A6 = r"""
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
"""

S6 = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXV 105

int main(void) {
    /* TODO: the whole program this time - parsing, BFS and printing.

       Parsing is the awkward part. Each of the n lines is
           <vertex> <neighbour> <neighbour> ...
       with a variable number of neighbours, so a plain scanf loop cannot know
       when to stop. Read whole lines with fgets and split them with strtok.

       Careful: after scanf("%d", &n) the newline is still sitting in the input,
       so the first fgets would return an empty line. Consume it first. */

    return 0;
}
"""

T6 = [
    "5\n1 3 4\n2 4 5\n3 1 4\n4 1 2 3\n5 2\n1\n",
    "4\n1 2 3\n2 4\n3 4\n4\n1\n",
    "6\n1 3 2\n2 4\n3 4\n4 5\n5 6\n6\n1\n",
    "5\n1 2 3\n2 4\n3 4\n4 5\n5\n1\n",
    "7\n1 4 2 3\n2 5\n3 5\n4 5 7\n5 6\n6 7\n7\n1\n",
    "5\n1 2\n2 3\n3\n4 5\n5\n1\n",
    "3\n1\n2 1\n3 2\n1\n",
]

write_problem(
    PACK, UNIT, "p06-practice-q1", title="Practice Question 1 (full)",
    mode="program", difficulty="hard", estimated_minutes=25, samples=1,
    topics=["bfs", "shortest path", "parsing", "lexicographic order"],
    prereqs=[f"{PACK}.{UNIT}.p05-lex-smallest-paths"],
    source="NITC_Lab_S3_DSA Week 4 - SSSP, Practice Question 1 (verbatim)",
    hints=[
        "Split the job in three: parse, BFS, print. Get parsing working and print "
        "the adjacency lists back out before you write a line of BFS.",
        "After scanf(\"%d\", &n) the newline remains in the buffer. Consume it with "
        "a getchar loop, or your first fgets returns an empty string.",
        "Each line starts with the vertex number itself, so the FIRST token is the "
        "vertex and the rest are its neighbours. Sort those neighbours ascending, "
        "then it is exactly the previous problem.",
    ],
    starter=S6, solution=A6, tests=T6,
    statement=r"""
# Practice Question 1 (full)

The real thing, verbatim from the Week 4 sheet. You write the entire program this
time - parsing, traversal and output.

> Write a program that takes an unweighted directed graph `G`, in the form of an
> adjacency list, and a vertex `s` in `G` as inputs, and find (and print) the
> shortest paths between vertex `s` and every other vertex. If multiple shortest
> paths exist, choose the lexicographically smallest path.

## Input format

- first line: the number of vertices `n`
- next `n` lines: the adjacency list of `G`
- last line: the source vertex `s`

Each adjacency line begins with the vertex itself, followed by its neighbours:

```
4 1 2 3
```

means vertex `4` has edges to `1`, `2` and `3`. A vertex with no out-edges appears
alone on its line. Neighbours are **not** guaranteed to be in ascending order.

## Output format

`n` lines, one per vertex `1..n` in increasing order: the path from `s` to that
vertex, with `-` between vertices. The line for `s` itself is just `s`.

If a vertex is unreachable from `s`, print `-1`. (The sheet does not say what to do
here; this is the same choice your own Week 4 solution made, and test 6 checks it.)

## Sample

```
5
1 3 4
2 4 5
3 1 4
4 1 2 3
5 2
1
```

```
1
1-4-2
1-3
1-4
1-4-2-5
```

## The parsing is the hard part

The graph logic is exactly the previous problem. What is genuinely new is reading
an adjacency list where **each line has a different number of numbers**, so a plain
`scanf("%d")` loop has no way to know when a line ends.

Read whole lines with `fgets`, then split them with `strtok(line, " \t\r\n")`.

One trap that costs people ten minutes: after `scanf("%d", &n)`, the newline after
`n` is still in the input buffer, so your first `fgets` returns an empty line and
everything shifts by one. Consume the rest of that line first:

```c
int ch;
while ((ch = getchar()) != '\n' && ch != EOF) { }
```

Build it in three stages - parse and echo the adjacency lists, then BFS, then the
path printing - and you will find the bug in whichever stage has it, instead of
staring at a wrong final answer.
""",
)

report(UNIT, 6)
