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
