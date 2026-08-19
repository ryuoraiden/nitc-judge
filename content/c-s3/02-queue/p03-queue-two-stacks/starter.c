#include <stdlib.h>
#include "problem.h"

QUEUE QINIT(void) {
    QUEUE q = malloc(sizeof(queuenode));
    q->F = SINIT();
    q->B = SINIT();
    return q;
}

int ISEMPTYQUEUE(QUEUE q) {
    return 0;   /* TODO: the queue is empty only when BOTH stacks are empty */
}

QUEUE ENQUEUE(QUEUE q, int value) {
    /* TODO: this is the cheap one - push onto B and return. */
    return q;
}

/* Helper worth writing: if F is empty, pour everything from B into F.
   Popping B and pushing onto F reverses the order, which is exactly what
   turns last-in-first-out into first-in-first-out. */
static void pour(QUEUE q) {
    /* TODO */
}

QUEUE DEQUEUE(QUEUE q) {
    /* TODO: make sure F has something (pour if needed), then pop F. */
    return q;
}

int FRONT(QUEUE q) {
    /* TODO: same pouring rule, but read instead of remove. */
    return 0;
}
