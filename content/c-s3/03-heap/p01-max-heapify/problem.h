#ifndef PROBLEM_H
#define PROBLEM_H

/* Restore the max-heap property at index i, assuming the subtrees rooted at
   left(i) and right(i) are already valid max-heaps.
   n is the heap size (only indices 0..n-1 are part of the heap). */
void maxHeapify(int a[], int n, int i);

#endif
