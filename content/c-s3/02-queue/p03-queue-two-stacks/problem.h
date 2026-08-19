#ifndef PROBLEM_H
#define PROBLEM_H

/* --- Linked stack, already implemented for you in a separate file. --- */
typedef struct _stack {
    int key;
    struct _stack *next;
} stacknode;

typedef stacknode *STACK;

STACK SINIT(void);
int   SISEMPTY(STACK s);
int   STOP(STACK s);
STACK SPUSH(STACK s, int value);
STACK SPOP(STACK s);

/* --- The queue you build out of two of them. Same shape as Week 3's QUEUE.h. --- */
typedef struct _queue {
    STACK F;   /* front stack: dequeue pops from here */
    STACK B;   /* back stack: enqueue pushes onto here */
} queuenode;

typedef queuenode *QUEUE;

QUEUE QINIT(void);
int   ISEMPTYQUEUE(QUEUE q);
QUEUE ENQUEUE(QUEUE q, int value);
QUEUE DEQUEUE(QUEUE q);      /* removes the front element */
int   FRONT(QUEUE q);        /* front element; caller checks ISEMPTYQUEUE first */

#endif
