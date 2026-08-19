#include "problem.h"

int bfsOrder(const Graph *g, int s, int order[]) {
    int visited[MAXV] = {0};
    int queue[MAXV];
    int head = 0, tail = 0;

    /* TODO
       1. mark s visited and put it in the queue
       2. while the queue is not empty: take the front vertex u, append it to
          order[], and for each neighbour v of u that is not yet visited,
          mark it visited and push it
       3. return how many vertices you appended

       Mark visited when you ENQUEUE, not when you dequeue - see the statement. */

    return 0;
}
