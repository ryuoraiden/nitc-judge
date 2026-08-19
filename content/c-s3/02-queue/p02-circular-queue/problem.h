#ifndef PROBLEM_H
#define PROBLEM_H

#define CAP 5

/* Circular queue: indices wrap around with %, and an explicit count tells
   empty and full apart (front == rear alone cannot). */
typedef struct {
    int data[CAP];
    int front;   /* index of the first element */
    int size;    /* how many elements are currently stored */
} CircularQueue;

void initQueue(CircularQueue *q);
int  isEmpty(const CircularQueue *q);
int  isFull(const CircularQueue *q);
void enqueue(CircularQueue *q, int value);
int  dequeue(CircularQueue *q);
int  frontOf(const CircularQueue *q);

#endif
