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
