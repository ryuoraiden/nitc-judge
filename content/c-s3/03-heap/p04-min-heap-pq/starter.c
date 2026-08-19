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
