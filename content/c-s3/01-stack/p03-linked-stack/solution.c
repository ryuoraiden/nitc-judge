#include <stdio.h>
#include <stdlib.h>
#include "problem.h"

STACK SINIT(void) {
    return NULL;
}

int ISEMPTY(STACK s) {
    return s == NULL;
}

int TOP(STACK s) {
    return s->key;
}

STACK PUSH(STACK s, int value) {
    stacknode *node = malloc(sizeof(stacknode));
    if (node == NULL) return s;
    node->key = value;
    node->next = s;
    return node;
}

STACK POP(STACK s) {
    if (s == NULL) return NULL;
    stacknode *rest = s->next;   /* save before freeing */
    free(s);
    return rest;
}

void SPRNT2B(STACK s) {
    if (s == NULL) { printf("EMPTY\n"); return; }
    for (stacknode *cur = s; cur != NULL; cur = cur->next) {
        printf("%d", cur->key);
        if (cur->next != NULL) printf(" ");
    }
    printf("\n");
}
