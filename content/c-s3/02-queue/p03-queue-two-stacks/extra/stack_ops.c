#include <stdlib.h>
#include "problem.h"

STACK SINIT(void) { return NULL; }
int   SISEMPTY(STACK s) { return s == NULL; }
int   STOP(STACK s) { return s->key; }

STACK SPUSH(STACK s, int value) {
    stacknode *node = malloc(sizeof(stacknode));
    if (node == NULL) return s;
    node->key = value;
    node->next = s;
    return node;
}

STACK SPOP(STACK s) {
    if (s == NULL) return NULL;
    stacknode *rest = s->next;
    free(s);
    return rest;
}
