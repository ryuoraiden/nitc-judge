# BFS visit order

The graph is built and sorted for you. Write the traversal.

```c
int bfsOrder(const Graph *g, int s, int order[]);
```

Fill `order[]` with the vertices in the order BFS visits them, and return the
count. Only vertices reachable from `s` appear.

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
