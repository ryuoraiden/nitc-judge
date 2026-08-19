#include "problem.h"

void initStack(Stack *s) { s->top = -1; }
int  isEmpty(const Stack *s) { return s->top < 0; }
void push(Stack *s, long long value) { s->data[++(s->top)] = value; }
long long pop(Stack *s) { return s->data[(s->top)--]; }
