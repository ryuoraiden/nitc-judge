# buildMaxHeap: one loop, two decisions

`maxHeapify` is given to you now. Write the function that turns an arbitrary array
into a max-heap by calling it.

```c
void buildMaxHeap(int a[], int n);
```

The body is a single `for` loop. All the difficulty is in two choices: **where it
starts** and **which way it runs**.

## Input / output

`n`, then `n` values. Print the array after `buildMaxHeap`.

## Example

```
7
4 1 3 2 16 9 10
```

```
16 4 10 2 1 9 3
```

## Think it through before you write it

`maxHeapify(a, n, i)` only works if the subtrees below `i` are *already* heaps. So
you cannot start at the root and work down - the precondition would not hold.

Which nodes need no work at all? A leaf has no children, so it is trivially a valid
heap already. With `n` elements, which indices are leaves? Work that out and both
the starting index and the direction fall straight out.

## Why this is not `n log n`

Running `maxHeapify` on `n/2` nodes at `O(log n)` each suggests `O(n log n)`, but
`buildMaxHeap` is actually `O(n)`. Most of those nodes sit near the bottom and can
only sink one or two levels; only the handful near the root can travel far. The
sum works out linear. Worth being able to say out loud in a viva.
