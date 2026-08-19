#include "problem.h"

void initQueue(CircularQueue *q) {
    q->front = 0;
    q->size = 0;
}

int isEmpty(const CircularQueue *q) {
    return q->size == 0;
}

int isFull(const CircularQueue *q) {
    return q->size == CAP;
}

void enqueue(CircularQueue *q, int value) {
    int slot = (q->front + q->size) % CAP;
    q->data[slot] = value;
    q->size++;
}

int dequeue(CircularQueue *q) {
    int value = q->data[q->front];
    q->front = (q->front + 1) % CAP;
    q->size--;
    return value;
}

int frontOf(const CircularQueue *q) {
    return q->data[q->front];
}
