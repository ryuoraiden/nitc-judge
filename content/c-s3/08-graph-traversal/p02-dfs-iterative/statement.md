# DFS with an explicit stack

Your Week 3 assignment requires DFS to be **iterative, using the STACK ADT** - not
recursive. This is that version, and it must produce **exactly the same order** as the
recursive one.

```c
int dfsIterative(const Graph *g, int s, int order[]);
```

## Input format

```
n m
u1 v1
...
```

`n` vertices numbered `1..n` and `m` **undirected** edges (each one is added in both
directions for you). Adjacency lists are sorted ascending before your function runs.

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
