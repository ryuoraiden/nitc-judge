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
