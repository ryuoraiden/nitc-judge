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
