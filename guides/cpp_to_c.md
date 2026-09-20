# C++ to C: the translation guide

Striver teaches graphs with the STL. The lab and the test want plain C. The algorithms
are identical - only the containers change, and there are about fifteen patterns to
learn. This page is those patterns, then the traps that turn a correct translation into
a crash.

## The one idea behind all of it

C++ containers grow. C arrays do not. So in C you **size every array from the
constraints in the problem statement**, once, up front:

```c
#define MAXV 105          /* n <= 100, plus slack, plus room for 1-based indexing */
#define MAXE 10005        /* m <= n(n-1)/2 */
```

Every NITC question gives you `n <= 100` or similar. Read the constraint, add a few,
and you never need `malloc` for graph work.

## Containers

| C++ | C |
|---|---|
| `vector<int> adj[n];` | `int adj[MAXV][MAXV]; int deg[MAXV];` |
| `adj[u].push_back(v);` | `adj[u][deg[u]++] = v;` |
| `for (auto v : adj[u])` | `for (int i = 0; i < deg[u]; i++) { int v = adj[u][i]; ... }` |
| `adj[u].size()` | `deg[u]` |
| `vector<pair<int,int>> adj[n];` (weighted) | `int to[MAXV][MAXV], wt[MAXV][MAXV], deg[MAXV];` |
| `for (auto [v, w] : adj[u])` | `for (int i = 0; i < deg[u]; i++) { int v = to[u][i], w = wt[u][i]; ... }` |
| `vector<int> vis(n, 0);` | `int vis[MAXV]; for (int i = 0; i < n; i++) vis[i] = 0;` |
| `vector<int> dist(n, 1e9);` | `int dist[MAXV]; for (int i = 0; i < n; i++) dist[i] = INF;` |
| `pair<int,int> p; p.first` | `typedef struct { int dist, node; } Pair;` then `p.dist` |
| `vector<vector<int>> edges;` (u, v, w) | `typedef struct { int u, v, w; } Edge; Edge edges[MAXE];` |

For matrix inputs (the `999` questions) you often need no adjacency list at all -
`int w[MAXV][MAXV]` read straight from input is the graph.

## Queue, stack, priority queue

**`queue<int>`** becomes an array and two indices:

```c
int q[MAXV], head = 0, tail = 0;
q[tail++] = s;              /* q.push(s)   */
int u = q[head++];          /* q.front(); q.pop(); */
while (head < tail) { }     /* while (!q.empty()) */
```

**`stack<int>`** becomes an array and a top index:

```c
int st[MAXE], top = -1;
st[++top] = s;              /* st.push(s)  */
int u = st[top--];          /* st.top(); st.pop(); */
while (top >= 0) { }        /* while (!st.empty()) */
```

**`priority_queue<pair<int,int>, vector<pair<int,int>>, greater<...>>`** has no C
equivalent. Two options:

- For `n <= 100` (every NITC question so far): **drop the heap entirely** and find the
  minimum with a linear scan each round. That is `O(V^2)` Dijkstra / Prim, it is what
  the lab solutions use, and it is less code to get wrong under time pressure.
- If you need the heap, use the min-heap from Unit 03 (`heapInsert` / `heapExtractMin`
  with an `Item { key, id }`), and keep Striver's "skip stale entries" check.

## Sorting

```cpp
sort(v.begin(), v.end());
sort(edges.begin(), edges.end(), [](auto &a, auto &b){ return a[2] < b[2]; });
```

```c
int cmpInt(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
qsort(v, n, sizeof(int), cmpInt);

int cmpEdge(const void *a, const void *b) {
    const Edge *x = a, *y = b;
    return (x->w > y->w) - (x->w < y->w);
}
qsort(edges, m, sizeof(Edge), cmpEdge);
```

C++ comparators answer "is a before b?" (true/false). `qsort` comparators answer
"negative, zero or positive". Returning `a < b` from a qsort comparator compiles and
silently sorts wrong.

## Functions and references

| C++ | C |
|---|---|
| `void dfs(int u, vector<int>& vis)` | `void dfs(int u, int vis[])` - arrays are already passed by pointer |
| `void f(int &count)` | `void f(int *count)`, call as `f(&count)`, use `(*count)++` |
| `bool` | `int` (or `#include <stdbool.h>`) |
| `min(a, b)`, `max(a, b)` | write `a < b ? a : b` - C has no integer `min` |
| `INT_MAX` | `#include <limits.h>` |
| `nullptr` | `NULL` |
| `new Node(x)` | `Node *n = malloc(sizeof(Node)); n->data = x; n->left = n->right = NULL;` |
| class with members (e.g. `DisjointSet`) | global arrays + plain functions |

Striver often writes graph code inside a `class Solution` with member functions. In C,
lift the members out to globals (or pass them as parameters) and make the methods plain
functions. Globals are fine in a lab program.

## Input and output

| C++ | C |
|---|---|
| `cin >> n;` | `scanf("%d", &n);` |
| `cin >> ch;` (skips whitespace) | `scanf(" %c", &ch);` - **the space matters** |
| `cout << x << " ";` | `printf("%d ", x);` |
| `getline(cin, line);` | `fgets(line, sizeof line, stdin);` |
| `stringstream ss(line); while (ss >> x)` | `strtok(line, " \t\r\n")` loop, then `atoi` |
| `long long` with `cin` | `scanf("%lld", &x)` / `printf("%lld", x)` |

## The traps

**Big local arrays crash.** `int adj[1005][1005];` inside `main` is 4 MB on the stack.
Windows gives you 1 MB. The program dies before printing anything. Make big arrays
`static` or global. Everything at `MAXV = 105` is fine anywhere.

**`memset` only works for 0 and -1.** It sets *bytes*. `memset(dist, 0, sizeof dist)`
and `memset(par, -1, sizeof par)` are fine; `memset(dist, 1e9, ...)` fills with garbage.
Use a loop for anything else.

**Stack-based DFS needs a bigger stack than you think.** With mark-on-pop, a vertex can
be pushed once per incoming edge, so the stack must hold up to `m` entries, not `n`.
`int st[MAXV]` overflows on dense graphs.

**`dist[u] + w` overflows at `INT_MAX`.** C++ code often uses `1e9` precisely to avoid
this. If you use `INT_MAX`, check `dist[u] != INT_MAX` before adding.

**`scanf("%d")` cannot see line ends.** For adjacency-list lines (`u v1 v2 v3 ...` with
a variable count) you must read the whole line with `fgets` and split it. After
`scanf("%d", &n)`, consume the leftover newline before the first `fgets`:

```c
int ch; while ((ch = getchar()) != '\n' && ch != EOF) { }
```

and split with `strtok(line, " \t\r\n")` so trailing spaces and Windows line endings
produce no phantom tokens. Parsing with `%c` character by character is exactly how a
test case gets lost to a trailing space.

**1-based vs 0-based.** Striver is almost always 0-based. NITC questions are almost
always 1-based. Either size arrays `n + 1` and stay 1-based throughout, or convert once
on input (`u--`) and once on output (`+ 1`). Mixing the two is the single most common
source of a wrong answer that "looks right".

## One full example

Striver-style BFS:

```cpp
vector<int> bfs(int n, vector<int> adj[]) {
    vector<int> vis(n, 0), order;
    queue<int> q;
    vis[0] = 1; q.push(0);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        order.push_back(u);
        for (auto v : adj[u])
            if (!vis[v]) { vis[v] = 1; q.push(v); }
    }
    return order;
}
```

The same thing in C, line for line:

```c
int bfs(int n, int adj[][MAXV], int deg[], int order[]) {
    int vis[MAXV] = {0}, q[MAXV], head = 0, tail = 0, cnt = 0;
    vis[0] = 1; q[tail++] = 0;
    while (head < tail) {
        int u = q[head++];
        order[cnt++] = u;
        for (int i = 0; i < deg[u]; i++) {
            int v = adj[u][i];
            if (!vis[v]) { vis[v] = 1; q[tail++] = v; }
        }
    }
    return cnt;               /* the vector's size comes back as a count */
}
```

Every graph problem in this judge marked **C++ ref** has a complete C++ version in its
**C++ → C** tab that passes the same tests. Read it, close it, write the C.
