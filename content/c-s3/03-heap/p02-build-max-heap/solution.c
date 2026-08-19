#include "problem.h"

void buildMaxHeap(int a[], int n) {
    /* Leaves are already valid one-element heaps, so start at the last
       internal node and work backwards to the root. */
    for (int i = n / 2 - 1; i >= 0; i--) {
        maxHeapify(a, n, i);
    }
}
