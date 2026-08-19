"""Unit 03 - Heap.  Run: python scripts/authoring/unit_03_heap.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report

PACK = "c-s3"
UNIT = "03-heap"

write_unit(PACK, UNIT, "Heap and priority queue",
           "One function per rung: heapify, then build, then sort, then the min-heap "
           "priority queue that Dijkstra will pull from.")

INDEXING = r"""
## Array indexing (0-based)

```
parent(i) = (i - 1) / 2
left(i)   = 2*i + 1
right(i)  = 2*i + 2
```

Same convention as your Lab 11 heap code, so what you write here transfers directly.
"""

# --------------------------------------------------------------- p01
H1 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

/* Restore the max-heap property at index i, assuming the subtrees rooted at
   left(i) and right(i) are already valid max-heaps.
   n is the heap size (only indices 0..n-1 are part of the heap). */
void maxHeapify(int a[], int n, int i);

#endif
"""

M1 = r"""
#include <stdio.h>
#include "problem.h"

#define MAXN 1000

int main(void) {
    int n, i;
    if (scanf("%d", &n) != 1) return 0;
    int a[MAXN];
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);
    if (scanf("%d", &i) != 1) return 0;

    maxHeapify(a, n, i);

    for (int k = 0; k < n; k++) printf("%d%s", a[k], k + 1 < n ? " " : "");
    printf("\n");
    return 0;
}
"""

S1 = r"""
#include "problem.h"

void maxHeapify(int a[], int n, int i) {
    /* TODO
       1. work out the indices of the left and right children
       2. find the largest of a[i], a[left], a[right] - but only for children
          that actually exist (index < n)
       3. if the largest is not i, swap them and recurse on the position the
          old value moved into
       If i is already the largest, there is nothing to do. */
}
"""

A1 = r"""
#include "problem.h"

void maxHeapify(int a[], int n, int i) {
    int left = 2 * i + 1;
    int right = 2 * i + 2;
    int largest = i;

    if (left < n && a[left] > a[largest]) largest = left;
    if (right < n && a[right] > a[largest]) largest = right;

    if (largest != i) {
        int tmp = a[i];
        a[i] = a[largest];
        a[largest] = tmp;
        maxHeapify(a, n, largest);   /* the value sank; fix where it landed */
    }
}
"""

T1 = [
    "7\n1 14 10 8 7 9 3\n0\n",
    "5\n50 40 30 20 10\n0\n",
    "7\n4 14 10 8 7 9 3\n0\n",
    "6\n2 9 8 1 3 4\n0\n",
    "4\n1 2 3 4\n1\n",
    "1\n42\n0\n",
    "9\n5 20 19 8 12 18 17 2 3\n0\n",
]

write_problem(
    PACK, UNIT, "p01-max-heapify", title="maxHeapify: fix exactly one violation",
    mode="function", difficulty="easy", estimated_minutes=8, samples=2,
    topics=["heap", "recursion"],
    source="Rebuilt from NITC_Lab_S2 Lab11 P1 (bank loan heapsort), heapify only",
    hints=[
        "Compute left = 2*i+1 and right = 2*i+2 first, then guard every access "
        "with 'index < n'. A child that does not exist must never be compared.",
        "Track the winner in a variable called largest, starting at i. Compare "
        "against left, then against largest again for right - not against a[i] "
        "twice, or you can miss the right child.",
        "After swapping, recurse on largest, not on i. The displaced value moved "
        "down to index largest and may still violate the property there.",
    ],
    header=H1, harness=M1, starter=S1, solution=A1, tests=T1,
    statement=r"""
# maxHeapify: fix exactly one violation

This is the primitive every other heap operation is built from, so it gets a rung
of its own. Write one function.

```c
void maxHeapify(int a[], int n, int i);
```

**Precondition:** the subtrees rooted at `left(i)` and `right(i)` are already valid
max-heaps. Only `a[i]` itself may be out of place.

**Postcondition:** the subtree rooted at `i` is a valid max-heap.
""" + INDEXING + r"""
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
""",
)

# --------------------------------------------------------------- p02
H2 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

/* Provided for you - identical to what you wrote in the previous problem. */
void maxHeapify(int a[], int n, int i);

/* Yours: turn an arbitrary array into a max-heap, in place. */
void buildMaxHeap(int a[], int n);

#endif
"""

E2 = r"""
#include "problem.h"

void maxHeapify(int a[], int n, int i) {
    int left = 2 * i + 1, right = 2 * i + 2, largest = i;
    if (left < n && a[left] > a[largest]) largest = left;
    if (right < n && a[right] > a[largest]) largest = right;
    if (largest != i) {
        int tmp = a[i]; a[i] = a[largest]; a[largest] = tmp;
        maxHeapify(a, n, largest);
    }
}
"""

M2 = r"""
#include <stdio.h>
#include "problem.h"

#define MAXN 1000

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int a[MAXN];
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);

    buildMaxHeap(a, n);

    for (int k = 0; k < n; k++) printf("%d%s", a[k], k + 1 < n ? " " : "");
    printf("\n");
    return 0;
}
"""

S2 = r"""
#include "problem.h"

void buildMaxHeap(int a[], int n) {
    /* TODO: one loop, calling maxHeapify. Two decisions to get right:
       - where does the loop start?
       - which direction does it run? */
}
"""

A2 = r"""
#include "problem.h"

void buildMaxHeap(int a[], int n) {
    /* Leaves are already valid one-element heaps, so start at the last
       internal node and work backwards to the root. */
    for (int i = n / 2 - 1; i >= 0; i--) {
        maxHeapify(a, n, i);
    }
}
"""

T2 = [
    "7\n4 1 3 2 16 9 10\n",
    "6\n1 2 3 4 5 6\n",
    "5\n5 4 3 2 1\n",
    "8\n3 3 3 3 3 3 3 3\n",
    "9\n27 17 3 16 13 10 1 5 7\n",
    "2\n1 2\n",
    "10\n1 1 2 2 3 3 4 4 5 5\n",
]

write_problem(
    PACK, UNIT, "p02-build-max-heap", title="buildMaxHeap: one loop, two decisions",
    mode="function", difficulty="easy", estimated_minutes=6, samples=2,
    topics=["heap"],
    prereqs=[f"{PACK}.{UNIT}.p01-max-heapify"],
    source="Rebuilt from NITC_Lab_S2 Lab11 P1",
    hints=[
        "Every leaf is already a valid heap of one element, so there is no point "
        "calling maxHeapify on any of them.",
        "With n elements the leaves are exactly the indices from n/2 onwards, so "
        "the last node worth fixing is n/2 - 1.",
        "Run the loop downwards, from n/2 - 1 to 0. maxHeapify requires its "
        "children to be valid already, so you must fix the bottom before the top.",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"heapify.c": E2},
    statement=r"""
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
""",
)

# --------------------------------------------------------------- p03
H3 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

/* Both provided for you. */
void maxHeapify(int a[], int n, int i);
void buildMaxHeap(int a[], int n);

/* Yours: sort a[0..n-1] into ascending order, in place, using the heap. */
void heapSort(int a[], int n);

#endif
"""

E3 = r"""
#include "problem.h"

void maxHeapify(int a[], int n, int i) {
    int left = 2 * i + 1, right = 2 * i + 2, largest = i;
    if (left < n && a[left] > a[largest]) largest = left;
    if (right < n && a[right] > a[largest]) largest = right;
    if (largest != i) {
        int tmp = a[i]; a[i] = a[largest]; a[largest] = tmp;
        maxHeapify(a, n, largest);
    }
}

void buildMaxHeap(int a[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--) maxHeapify(a, n, i);
}
"""

M3 = r"""
#include <stdio.h>
#include "problem.h"

#define MAXN 2000

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    int a[MAXN];
    for (int k = 0; k < n; k++) scanf("%d", &a[k]);

    heapSort(a, n);

    for (int k = 0; k < n; k++) printf("%d%s", a[k], k + 1 < n ? " " : "");
    printf("\n");
    return 0;
}
"""

S3 = r"""
#include "problem.h"

void heapSort(int a[], int n) {
    /* TODO
       1. buildMaxHeap once, so the largest element sits at index 0
       2. repeatedly: swap a[0] with the last element of the *current* heap,
          shrink the heap by one, and restore the heap property at the root
       The shrinking is the part people get wrong - see the statement. */
}
"""

A3 = r"""
#include "problem.h"

void heapSort(int a[], int n) {
    buildMaxHeap(a, n);

    for (int end = n - 1; end > 0; end--) {
        int tmp = a[0];        /* current maximum */
        a[0] = a[end];
        a[end] = tmp;          /* park it at the end, now outside the heap */

        maxHeapify(a, end, 0); /* note: size is end, not n */
    }
}
"""

T3 = [
    "7\n4 1 3 2 16 9 10\n",
    "6\n5 2 9 1 7 3\n",
    "8\n8 7 6 5 4 3 2 1\n",
    "8\n1 2 3 4 5 6 7 8\n",
    "5\n3 3 3 3 3\n",
    "1\n7\n",
    "12\n45 12 89 3 67 23 90 1 34 78 56 11\n",
    "10\n-5 3 -2 0 8 -9 4 1 -1 6\n",
]

write_problem(
    PACK, UNIT, "p03-heap-sort", title="heapSort: sort by repeatedly evicting the root",
    mode="function", difficulty="medium", estimated_minutes=8, samples=2,
    topics=["heap", "sorting"],
    prereqs=[f"{PACK}.{UNIT}.p02-build-max-heap"],
    source="Rebuilt from NITC_Lab_S2 Lab11 P1/P2",
    hints=[
        "Build the heap once, outside the loop. Rebuilding it every iteration is "
        "correct but throws away the whole point of the algorithm.",
        "Each iteration: swap a[0] with a[end], then heapify the root over a "
        "SMALLER heap. The element you just parked at a[end] is finished.",
        "The size argument to maxHeapify must be end, not n. Passing n drags the "
        "already-sorted tail back into the heap and the array never converges.",
    ],
    header=H3, harness=M3, starter=S3, solution=A3, tests=T3,
    extra={"heap_ops.c": E3},
    statement=r"""
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
""",
)

# --------------------------------------------------------------- p04
H4 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXH 20000

/* A priority queue entry: key is the priority, id is the payload
   (which will be a vertex number once you reach Dijkstra). */
typedef struct {
    int key;
    int id;
} Item;

typedef struct {
    Item a[MAXH];
    int size;
} MinHeap;

void heapInit(MinHeap *h);
int  heapEmpty(const MinHeap *h);
void heapInsert(MinHeap *h, int key, int id);
Item heapExtractMin(MinHeap *h);   /* caller checks heapEmpty first */

#endif
"""

M4 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    MinHeap h;
    heapInit(&h);

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'i') {
            int key, id;
            if (scanf("%d %d", &key, &id) != 2) break;
            heapInsert(&h, key, id);
            printf("OK\n");
        } else if (cmd == 'x') {
            if (heapEmpty(&h)) printf("EMPTY\n");
            else {
                Item it = heapExtractMin(&h);
                printf("%d %d\n", it.key, it.id);
            }
        } else if (cmd == 'e') {
            printf("%s\n", heapEmpty(&h) ? "YES" : "NO");
        }
    }
    return 0;
}
"""

S4 = r"""
#include "problem.h"

/* Returns 1 if x should come out before y.
   Order by key; break ties by the smaller id so the output is deterministic. */
static int before(Item x, Item y) {
    return 0;   /* TODO */
}

static void swapItems(Item *x, Item *y) {
    Item t = *x; *x = *y; *y = t;
}

void heapInit(MinHeap *h) {
    h->size = 0;
}

int heapEmpty(const MinHeap *h) {
    return 0;   /* TODO */
}

void heapInsert(MinHeap *h, int key, int id) {
    /* TODO: put the new item at the end, then bubble it UP while it should
       come before its parent. parent(i) = (i - 1) / 2 */
}

Item heapExtractMin(MinHeap *h) {
    /* TODO: save the root, move the last item into the root, shrink, then
       sift DOWN from the root. Return the saved root. */
    Item empty = {0, 0};
    return empty;
}
"""

A4 = r"""
#include "problem.h"

static int before(Item x, Item y) {
    if (x.key != y.key) return x.key < y.key;
    return x.id < y.id;
}

static void swapItems(Item *x, Item *y) {
    Item t = *x; *x = *y; *y = t;
}

void heapInit(MinHeap *h) {
    h->size = 0;
}

int heapEmpty(const MinHeap *h) {
    return h->size == 0;
}

void heapInsert(MinHeap *h, int key, int id) {
    int i = h->size++;
    h->a[i].key = key;
    h->a[i].id = id;

    while (i > 0) {
        int parent = (i - 1) / 2;
        if (!before(h->a[i], h->a[parent])) break;
        swapItems(&h->a[i], &h->a[parent]);
        i = parent;
    }
}

Item heapExtractMin(MinHeap *h) {
    Item root = h->a[0];
    h->a[0] = h->a[--(h->size)];

    int i = 0;
    for (;;) {
        int left = 2 * i + 1, right = 2 * i + 2, best = i;
        if (left  < h->size && before(h->a[left],  h->a[best])) best = left;
        if (right < h->size && before(h->a[right], h->a[best])) best = right;
        if (best == i) break;
        swapItems(&h->a[i], &h->a[best]);
        i = best;
    }
    return root;
}
"""

T4 = [
    "i 5 1\ni 3 2\ni 8 3\nx\nx\nx\nx\nq\n",
    "i 4 7\ni 4 2\ni 4 9\nx\nx\nx\ne\nq\n",
    "x\ne\ni 1 1\ne\nx\ne\nq\n",
    "i 9 1\ni 7 2\ni 5 3\ni 3 4\ni 1 5\nx\nx\nx\nx\nx\nq\n",
    "i 1 1\ni 2 2\ni 3 3\ni 4 4\ni 5 5\nx\nx\nx\nx\nx\nq\n",
    "i 10 1\nx\ni 20 2\ni 5 3\nx\ni 15 4\nx\nx\ne\nq\n",
    "i 3 30\ni 1 10\ni 3 20\ni 2 25\ni 1 5\nx\nx\nx\nx\nx\ne\nq\n",
]

write_problem(
    PACK, UNIT, "p04-min-heap-pq", title="Min-heap priority queue (the one Dijkstra uses)",
    mode="function", difficulty="medium", estimated_minutes=15, samples=2,
    topics=["heap", "priority queue"],
    prereqs=[f"{PACK}.{UNIT}.p01-max-heapify"],
    source="Rebuilt from NITC_Lab_S2 Lab11 P3/P5 (ticket and patient priority queues)",
    hints=[
        "Insert appends at index size and bubbles UP; extract takes index 0, moves "
        "the LAST item into the hole, and sifts DOWN. Two directions, two loops.",
        "parent(i) = (i-1)/2 with integer division. Stop bubbling when i reaches 0 "
        "or when the item no longer beats its parent.",
        "Write the before() comparison once and call it everywhere. Inlining the "
        "comparison in three places is how the tie-break rule ends up applied in "
        "only two of them.",
    ],
    header=H4, harness=M4, starter=S4, solution=A4, tests=T4,
    statement=r"""
# Min-heap priority queue (the one Dijkstra uses)

Same array-heap machinery, three changes: it is a **min**-heap, it carries a
payload alongside the priority, and it supports insertion (so it grows, rather than
being built once from a fixed array).

```c
typedef struct { int key; int id; } Item;
```

`key` is the priority. `id` is the payload - it will be a vertex number when you
get to Dijkstra.

## Ordering, including ties

Smallest `key` comes out first. **If two items have the same `key`, the smaller
`id` comes out first.**

That tie-break is not decoration. Without it, which of two equal-key items surfaces
first depends on incidental swap order, and the same program could print different
valid answers on different days. Pinning the rule makes the output deterministic and
therefore testable. Write the comparison once as a helper and call it from both the
bubble-up and the sift-down.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i key id` | insert | `OK` |
| `x` | extract minimum | `key id`, or `EMPTY` |
| `e` | is it empty? | `YES` or `NO` |
| `q` | quit | nothing |

## Example

```
i 5 1
i 3 2
i 8 3
x
x
x
x
q
```

```
OK
OK
OK
3 2
5 1
8 3
EMPTY
```

## Two loops, opposite directions

**`heapInsert`** puts the new item at the end and bubbles it *up* while it beats
its parent. A new item can only ever be too small for where it landed, so up is the
only direction it can move.

**`heapExtractMin`** saves `a[0]`, moves the *last* item into the root, shrinks the
heap, then sifts *down*. Moving the last element in (rather than, say, promoting the
smaller child repeatedly) is what keeps the tree complete, which is what lets the
whole structure live in a flat array with no pointers.
""",
)

report(UNIT, 4)
