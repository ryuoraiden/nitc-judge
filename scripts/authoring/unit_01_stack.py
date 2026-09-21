"""Unit 01 - Stack.  Run: python scripts/authoring/unit_01_stack.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_pack, write_unit, write_problem, report

PACK = "c-s3"
UNIT = "01-stack"

write_pack(PACK)   # title, description and study path live in pack_c_s3.py
write_unit(PACK, UNIT, "Stack",
           "The array stack you will reuse for DFS and expression work. "
           "Small capacity so overflow is easy to reach.")

# --------------------------------------------------------------- p01
H1 = r"""
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
"""

M1 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    Stack s;
    initStack(&s);

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'p') {
            int v;
            if (scanf("%d", &v) != 1) break;
            if (isFull(&s)) printf("FULL\n");
            else { push(&s, v); printf("OK\n"); }
        } else if (cmd == 'o') {
            if (isEmpty(&s)) printf("EMPTY\n");
            else printf("%d\n", pop(&s));
        } else if (cmd == 'k') {
            if (isEmpty(&s)) printf("EMPTY\n");
            else printf("%d\n", peek(&s));
        } else if (cmd == 'e') {
            printf("%s\n", isEmpty(&s) ? "YES" : "NO");
        }
    }
    return 0;
}
"""

S1 = r"""
#include "problem.h"

void initStack(Stack *s) {
    /* TODO: an empty stack has no topmost element. What should top be? */
}

int isEmpty(const Stack *s) {
    return 0;   /* TODO */
}

int isFull(const Stack *s) {
    return 0;   /* TODO: CAP elements fit, and top is an index */
}

void push(Stack *s, int value) {
    /* TODO: move top up first, then store. The caller guarantees it is not full. */
}

int pop(Stack *s) {
    return 0;   /* TODO: return the top element and shrink the stack */
}

int peek(const Stack *s) {
    return 0;   /* TODO: the top element, without removing it */
}
"""

A1 = r"""
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
"""

T1 = [
    "p 10\np 20\nk\no\ne\no\ne\nq\n",
    "p 1\np 2\np 3\np 4\np 5\np 6\nk\nq\n",
    "o\nk\ne\np 7\no\no\nq\n",
    "p 3\np 1\np 4\no\np 1\np 5\nk\no\no\no\ne\nq\n",
    "e\np 42\ne\nk\no\ne\nq\n",
]

write_problem(
    PACK, UNIT, "p01-array-stack", title="Array stack: the six core operations",
    mode="function", difficulty="easy", estimated_minutes=8, samples=1,
    topics=["stack", "arrays"],
    source="Rebuilt from NITC_Lab_S2 Lab9 P1 (library book stack)",
    hints=[
        "top is an index into data[], not a count. Starting it at -1 makes push "
        "'increment then store' and pop 'read then decrement'.",
        "isFull is about the last usable index: with CAP slots the highest valid "
        "index is CAP-1, so the stack is full when top has reached it.",
        "push should be s->data[++(s->top)] = value; and pop should be "
        "return s->data[(s->top)--]; - note pre- vs post-increment.",
    ],
    header=H1, harness=M1, starter=S1, solution=A1, tests=T1,
    statement=r"""
# Array stack: the six core operations

Everything later in this unit sits on top of a working stack, so build it once and
build it right. You implement the six functions declared in `problem.h`; a hidden
`main()` drives them from a command stream.

## Commands the hidden main() understands

| Command | Meaning | Prints |
|---|---|---|
| `p v` | push the integer `v` | `OK`, or `FULL` if the stack is already full |
| `o` | pop | the popped value, or `EMPTY` |
| `k` | peek | the top value, or `EMPTY` |
| `e` | is it empty? | `YES` or `NO` |
| `q` | quit | nothing |

The driver checks `isFull` before pushing and `isEmpty` before popping, so your
`push` and `pop` may assume they are never called on a full or empty stack.

## Capacity

`CAP` is **5**. That is small on purpose: overflow is something you should be able
to reach and reason about, not a theoretical edge case.

## Example

```
p 10
p 20
k
o
e
o
e
q
```

```
OK
OK
20
20
NO
10
YES
```

## Why this shape

This is the NITC lab file split: a read-only header, your implementation, and a
`main()` you never see. You cannot fake it with a well-placed `printf` - the driver
calls your functions and prints the return values itself.
""",
)

# --------------------------------------------------------------- p02
H2 = r"""
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
"""

E2 = r"""
#include "problem.h"

void initStack(Stack *s) { s->top = -1; }
int  isEmpty(const Stack *s) { return s->top < 0; }
void push(Stack *s, long long value) { s->data[++(s->top)] = value; }
long long pop(Stack *s) { return s->data[(s->top)--]; }
"""

M2 = r"""
#include <stdio.h>
#include <string.h>
#include "problem.h"

int main(void) {
    char line[1024];
    while (fgets(line, sizeof line, stdin)) {
        size_t n = strlen(line);
        while (n > 0 && (line[n - 1] == '\n' || line[n - 1] == '\r')) line[--n] = '\0';
        if (n == 0) continue;
        printf("%lld\n", evalPostfix(line));
    }
    return 0;
}
"""

S2 = r"""
#include <ctype.h>
#include "problem.h"

long long evalPostfix(const char *expr) {
    Stack s;
    initStack(&s);

    /* TODO: walk the string once.
       - skip spaces
       - a run of digits is one operand: build the number, then push it
       - an operator pops TWO values, combines them, and pushes the result
       Remember the order: the first pop is the RIGHT operand. */

    return 0;
}
"""

A2 = r"""
#include <ctype.h>
#include "problem.h"

long long evalPostfix(const char *expr) {
    Stack s;
    initStack(&s);

    for (const char *p = expr; *p != '\0'; ) {
        if (*p == ' ') { p++; continue; }

        if (isdigit((unsigned char)*p)) {
            long long value = 0;
            while (isdigit((unsigned char)*p)) {
                value = value * 10 + (*p - '0');
                p++;
            }
            push(&s, value);
        } else {
            char op = *p++;
            long long right = pop(&s);      /* first pop is the right operand */
            long long left  = pop(&s);
            long long result = 0;
            switch (op) {
                case '+': result = left + right; break;
                case '-': result = left - right; break;
                case '*': result = left * right; break;
                case '/': result = (right != 0) ? left / right : 0; break;
                default:  result = 0; break;
            }
            push(&s, result);
        }
    }

    return isEmpty(&s) ? 0 : pop(&s);
}
"""

T2 = [
    "3 4 +\n5 1 2 + 4 * + 3 -\n",
    "2 3 4 * +\n10 2 /\n7 3 -\n",
    "100 20 -\n6 7 *\n12 3 / 4 +\n",
    "1 2 + 3 + 4 + 5 +\n9 8 7 6 5 + + + +\n",
    "20 3 -\n3 20 -\n8 2 / 2 /\n",
]

write_problem(
    PACK, UNIT, "p02-postfix-eval", title="Evaluate a postfix expression",
    mode="function", difficulty="easy", estimated_minutes=10, samples=1,
    topics=["stack", "parsing"],
    prereqs=[f"{PACK}.{UNIT}.p01-array-stack"],
    source="Rebuilt from NITC_Lab_S2 Lab10 P5 (expression trees)",
    hints=[
        "One pass over the string is enough. Track your position with a pointer "
        "and advance it yourself rather than using a for loop over an index.",
        "Operand digits can be multi-digit: keep consuming while isdigit() holds, "
        "building value = value * 10 + (*p - '0').",
        "Order matters for - and /. The first value you pop is the RIGHT operand: "
        "for '7 3 -' you pop 3, then 7, and compute 7 - 3.",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"stack_ops.c": E2},
    statement=r"""
# Evaluate a postfix expression

The stack operations are **already written for you** this time (in a file you do
not see). Your job is the one function that uses them: `evalPostfix`.

Each input line is one postfix expression: operands and operators separated by
single spaces. Print the value of each expression on its own line.

## Rules

- Operands are non-negative integers, possibly multi-digit.
- Operators are `+`, `-`, `*`, `/` and are always binary.
- Division is integer division, and never by zero in the tests.
- Every expression is well-formed.

## Example

```
3 4 +
5 1 2 + 4 * + 3 -
```

```
7
14
```

The second one evaluates as `1 + 2 = 3`, then `3 * 4 = 12`, then `5 + 12 = 17`,
then `17 - 3 = 14`.

## The trap

`-` and `/` are not commutative, and the stack hands you the operands in reverse.
For `7 3 -` the first `pop()` gives you `3`, not `7`. Getting this backwards is the
single most common bug in this problem, and it passes the `+` and `*` tests
happily while failing everything else.
""",
)

# --------------------------------------------------------------- p03
H3 = r"""
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
"""

M3 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    STACK s = SINIT();

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'p') {
            int v;
            if (scanf("%d", &v) != 1) break;
            s = PUSH(s, v);
        } else if (cmd == 'o') {
            if (ISEMPTY(s)) printf("EMPTY\n");
            else { printf("%d\n", TOP(s)); s = POP(s); }
        } else if (cmd == 't') {
            if (ISEMPTY(s)) printf("EMPTY\n");
            else printf("%d\n", TOP(s));
        } else if (cmd == 'd') {
            SPRNT2B(s);
        }
    }
    return 0;
}
"""

S3 = r"""
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
"""

A3 = r"""
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
"""

T3 = [
    "p 1\np 2\np 3\nd\no\nd\nt\nq\n",
    "d\no\nt\np 9\nd\no\nd\nq\n",
    "p 5\np 5\np 5\nd\no\no\no\no\nd\nq\n",
    "p 10\np 20\np 30\np 40\no\no\nd\np 99\nd\nt\nq\n",
    "p 7\nd\nq\n",
]

write_problem(
    PACK, UNIT, "p03-linked-stack", title="Linked stack, Week 3 style",
    mode="function", difficulty="medium", estimated_minutes=12, samples=1,
    topics=["stack", "linked list", "pointers"],
    prereqs=[f"{PACK}.{UNIT}.p01-array-stack"],
    source="Matches STACK.h from NITC_Lab_S3_DSA Week 3 - Graphs",
    hints=[
        "An empty linked stack is NULL. That is why every operation takes the top "
        "pointer and returns the (possibly new) top pointer.",
        "PUSH is three lines: malloc, set key and next = s, return the new node. "
        "The new node becomes the head, so nothing else needs to move.",
        "POP must save s->next into a local variable BEFORE calling free(s). "
        "Reading s->next after freeing s is use-after-free - it often appears to "
        "work, which is what makes it dangerous.",
    ],
    header=H3, harness=M3, starter=S3, solution=A3, tests=T3,
    statement=r"""
# Linked stack, Week 3 style

Same stack, no array. This is the exact interface from `STACK.h` in your Week 3
graph assignment, down to the shouty function names - so once this works you can
read that assignment's code without squinting.

```c
typedef struct _stack { int key; struct _stack *next; } stacknode;
typedef stacknode *STACK;
```

A `STACK` **is** a pointer to the top node. Empty is `NULL`. That is why `PUSH` and
`POP` return a `STACK`: the top changes, and the caller reassigns it with
`s = PUSH(s, v);`.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `p v` | push `v` | nothing |
| `o` | pop | the value popped, or `EMPTY` |
| `t` | top | the top value, or `EMPTY` |
| `d` | dump | all keys top to bottom, space separated, or `EMPTY` |
| `q` | quit | nothing |

## Example

```
p 1
p 2
p 3
d
o
d
t
q
```

```
3 2 1
3
2 1
2
```

## The pointer bug that matters

In `POP`, save `s->next` into a local **before** you `free(s)`. If you free first
and then read `s->next`, you are reading memory you have handed back. On this
toolchain it will usually appear to work, which is exactly why it is worth
building the habit now.

Also: every node you `malloc` in `PUSH` should be `free`d in `POP`. Nothing here
checks that yet, but the same discipline is what `freeTree` will demand later.
""",
)

report(UNIT, 3)
