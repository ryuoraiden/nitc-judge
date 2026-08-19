#ifndef PROBLEM_H
#define PROBLEM_H

/* Deliberately tiny so that overflow is reachable in a five-line test. */
#define CAP 5

typedef struct {
    int data[CAP];
    int top;        /* index of the topmost element; -1 when the stack is empty */
} Stack;

void initStack(Stack *s);
int  isEmpty(const Stack *s);
int  isFull(const Stack *s);
void push(Stack *s, int value);
int  pop(Stack *s);
int  peek(const Stack *s);

#endif
