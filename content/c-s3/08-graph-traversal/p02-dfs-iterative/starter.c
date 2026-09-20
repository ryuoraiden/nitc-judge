#include "problem.h"

int dfsIterative(const Graph *g, int s, int order[]) {
    int visited[MAXV] = {0};
    int stack[MAXE];      /* NOT MAXV - see the statement */
    int top = -1, count = 0;

    /* TODO
       - push s
       - while the stack is not empty:
           pop u
           if u is already visited, skip it (it was pushed more than once)
           mark it, append it to order[]
           push its unvisited neighbours in DESCENDING order
       Descending, so the smallest one ends up on top and is popped first. */

    return count;
}
