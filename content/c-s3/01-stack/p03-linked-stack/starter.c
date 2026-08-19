#include <stdio.h>
#include <stdlib.h>
#include "problem.h"

STACK SINIT(void) {
    return NULL;   /* an empty linked stack is just a null pointer */
}

int ISEMPTY(STACK s) {
    return 0;   /* TODO */
}

int TOP(STACK s) {
    return 0;   /* TODO */
}

STACK PUSH(STACK s, int value) {
    /* TODO: malloc a node, fill it in, link it in front, return the new top */
    return s;
}

STACK POP(STACK s) {
    /* TODO: remember the second node, free the first, return the second.
       Freeing before you have saved s->next loses the rest of the stack. */
    return s;
}

void SPRNT2B(STACK s) {
    /* TODO: print keys from top to bottom, single space between them,
       newline at the end. Print EMPTY (and a newline) for an empty stack. */
}
