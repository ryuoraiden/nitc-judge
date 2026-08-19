#ifndef PROBLEM_H
#define PROBLEM_H

#define CAP 256

typedef struct {
    long long data[CAP];
    int top;
} Stack;

/* --- Already implemented for you, in a separate file. Just call them. --- */
void initStack(Stack *s);
int  isEmpty(const Stack *s);
void push(Stack *s, long long value);
long long pop(Stack *s);

/* --- This is the one you write. --- */
long long evalPostfix(const char *expr);

#endif
