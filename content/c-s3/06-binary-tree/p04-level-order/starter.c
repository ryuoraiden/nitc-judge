#include <stdio.h>
#include "problem.h"

void levelOrder(Node *root) {
    static Node *q[MAXQ];    /* a queue of node POINTERS */
    int head = 0, tail = 0;

    /* TODO
       - push root (if not NULL)
       - while the queue is not empty:
           size = tail - head        <- how many nodes are on THIS level
           pop exactly 'size' nodes, printing each and pushing its children
           print a newline
       Freezing 'size' before the inner loop is what separates the levels. */
}
