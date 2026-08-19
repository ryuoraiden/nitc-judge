# Reconstruct the path with a parent array

Distances tell you *how far*. This tells you *which way*.

```c
int bfsPath(const Graph *g, int s, int t, int path[]);
```

Write a shortest `s -> t` path into `path[]` in order from `s` to `t`, and return
its length in vertices. Return `0` if `t` is unreachable. If `s == t`, the path is
just `s` and the length is `1`.

## Input format

```
n m
u1 v1
u2 v2
...
s
```

`n` vertices numbered `1..n`, `m` directed edges `u -> v`, then `s` and `t`.
The graph is built and its adjacency lists sorted ascending before your function
is called.

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
