#include "problem.h"

void initQueue(Queue *q) {
    q->front = 0;
    q->rear = -1;
}

int isEmpty(const Queue *q) {
    return q->front > q->rear;
}

int isFull(const Queue *q) {
    return q->rear >= CAP - 1;
}

void enqueue(Queue *q, int value) {
    q->data[++(q->rear)] = value;
}

int dequeue(Queue *q) {
    return q->data[(q->front)++];
}

int frontOf(const Queue *q) {
    return q->data[q->front];
}
