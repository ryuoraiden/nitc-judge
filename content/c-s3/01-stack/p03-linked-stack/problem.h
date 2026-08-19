#ifndef PROBLEM_H
#define PROBLEM_H

/* Same shape as STACK.h from your Week 3 graph assignment. */
typedef struct _stack {
    int key;
    struct _stack *next;
} stacknode;

typedef stacknode *STACK;

STACK SINIT(void);            /* a fresh empty stack */
int   ISEMPTY(STACK s);
int   TOP(STACK s);           /* key of the top node; caller checks ISEMPTY first */
STACK PUSH(STACK s, int value);   /* returns the NEW top */
STACK POP(STACK s);               /* frees the top node, returns the new top */
void  SPRNT2B(STACK s);           /* print top to bottom, space separated */

#endif
