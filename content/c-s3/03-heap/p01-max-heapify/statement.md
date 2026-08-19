# maxHeapify: fix exactly one violation

This is the primitive every other heap operation is built from, so it gets a rung
of its own. Write one function.

```c
void maxHeapify(int a[], int n, int i);
```

**Precondition:** the subtrees rooted at `left(i)` and `right(i)` are already valid
max-heaps. Only `a[i]` itself may be out of place.

**Postcondition:** the subtree rooted at `i` is a valid max-heap.

## Array indexing (0-based)

```
parent(i) = (i - 1) / 2
left(i)   = 2*i + 1
right(i)  = 2*i + 2
```

Same convention as your Lab 11 heap code, so what you write here transfers directly.

## Input / output

First line `n`, then `n` array values, then the index `i`. Print the array after
one `maxHeapify(a, n, i)` call, space separated on one line.

## Example

```
7
1 14 10 8 7 9 3
0
```

```
14 8 10 1 7 9 3
```

The 1 at the root sinks: it swaps with 14, then again with 8, and comes to rest at
index 3.

## The two mistakes to avoid

**Forgetting the bounds check.** `2*i+1` can run past the end. Every comparison
must be guarded by `< n`, or you are reading whatever happens to sit past the heap.

**Recursing on the wrong index.** After the swap, the troublesome value is now at
`largest`, not at `i`. Recursing on `i` terminates immediately and quietly leaves
the heap broken further down - which shows up as a wrong answer three problems
later, not here.
