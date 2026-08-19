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
