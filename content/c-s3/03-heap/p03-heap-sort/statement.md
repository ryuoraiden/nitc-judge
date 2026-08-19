# heapSort: sort by repeatedly evicting the root

`maxHeapify` and `buildMaxHeap` are both provided. Write the sort.

```c
void heapSort(int a[], int n);   /* ascending order, in place */
```

## The algorithm

1. `buildMaxHeap(a, n)` - now the largest element is at `a[0]`.
2. Swap `a[0]` with the last element of the heap. The maximum is now in its final
   sorted position, and it is no longer part of the heap.
3. The heap is one element smaller. Restore the property at the root.
4. Repeat until one element remains.

Ascending order comes out of a *max*-heap for free, because each evicted maximum
gets parked at the far end and the sorted region grows leftwards from there.

## Example

```
7
4 1 3 2 16 9 10
```

```
1 2 3 4 9 10 16
```

## The one-character bug

In step 3 the heap size is **not** `n` any more. If you call `maxHeapify(a, n, 0)`
instead of `maxHeapify(a, end, 0)`, the elements you already placed get pulled back
into the heap and the array never sorts. It is a single wrong variable and it is by
far the most common way to fail this problem, so check it before you check anything
else.

## In-place, and not stable

Heapsort uses `O(1)` extra space - a genuine advantage over mergesort. It is not a
stable sort: equal elements can be reordered. Neither property is tested here, but
both are standard viva questions.
