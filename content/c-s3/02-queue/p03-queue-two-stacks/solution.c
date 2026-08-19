#include <stdlib.h>
#include "problem.h"

QUEUE QINIT(void) {
    QUEUE q = malloc(sizeof(queuenode));
    q->F = SINIT();
    q->B = SINIT();
    return q;
}

int ISEMPTYQUEUE(QUEUE q) {
    return SISEMPTY(q->F) && SISEMPTY(q->B);
}

QUEUE ENQUEUE(QUEUE q, int value) {
    q->B = SPUSH(q->B, value);
    return q;
}

/* Only ever called when F is empty, so each element moves across at most once. */
static void pour(QUEUE q) {
    if (!SISEMPTY(q->F)) return;
    while (!SISEMPTY(q->B)) {
        q->F = SPUSH(q->F, STOP(q->B));
        q->B = SPOP(q->B);
    }
}

QUEUE DEQUEUE(QUEUE q) {
    pour(q);
    if (!SISEMPTY(q->F)) q->F = SPOP(q->F);
    return q;
}

int FRONT(QUEUE q) {
    pour(q);
    return STOP(q->F);
}
