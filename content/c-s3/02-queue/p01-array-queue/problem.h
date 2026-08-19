#ifndef PROBLEM_H
#define PROBLEM_H

#define CAP 5

/* A plain linear queue: front and rear only ever move forward.
   Empty is front > rear.  Full is rear == CAP - 1. */
typedef struct {
    int data[CAP];
    int front;   /* index of the first element */
    int rear;    /* index of the last element; -1 before anything is queued */
} Queue;

void initQueue(Queue *q);
int  isEmpty(const Queue *q);
int  isFull(const Queue *q);
void enqueue(Queue *q, int value);
int  dequeue(Queue *q);
int  frontOf(const Queue *q);

#endif
