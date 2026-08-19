#include "problem.h"

void initStack(Stack *s) {
    s->top = -1;
}

int isEmpty(const Stack *s) {
    return s->top < 0;
}

int isFull(const Stack *s) {
    return s->top >= CAP - 1;
}

void push(Stack *s, int value) {
    s->data[++(s->top)] = value;
}

int pop(Stack *s) {
    return s->data[(s->top)--];
}

int peek(const Stack *s) {
    return s->data[s->top];
}
