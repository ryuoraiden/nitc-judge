#include "problem.h"

void initQueue(CircularQueue *q) {
    /* TODO */
}

int isEmpty(const CircularQueue *q) {
    return 0;   /* TODO: use size, not the indices */
}

int isFull(const CircularQueue *q) {
    return 0;   /* TODO */
}

void enqueue(CircularQueue *q, int value) {
    /* TODO: the next free slot is (front + size) wrapped around CAP.
       Store there, then grow size. */
}

int dequeue(CircularQueue *q) {
    /* TODO: take data[front], move front forward with wraparound, shrink size. */
    return 0;
}

int frontOf(const CircularQueue *q) {
    return 0;   /* TODO */
}
