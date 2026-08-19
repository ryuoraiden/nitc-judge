"""Unit 02 - Queue.  Run: python scripts/authoring/unit_02_queue.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report

PACK = "c-s3"
UNIT = "02-queue"

write_unit(PACK, UNIT, "Queue",
           "The queue BFS runs on. Build the naive one, feel where it breaks, "
           "then fix it with wraparound.")

CMDS = r"""
| Command | Meaning | Prints |
|---|---|---|
| `n v` | enqueue `v` | `OK`, or `FULL` |
| `d` | dequeue | the value removed, or `EMPTY` |
| `f` | front | the front value, or `EMPTY` |
| `e` | is it empty? | `YES` or `NO` |
| `q` | quit | nothing |
"""

# --------------------------------------------------------------- p01
H1 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

#define CAP 5

/* A plain linear queue: front and rear only ever move forward.
   Empty is front > rear.  Full is rear == CAP - 1. */
typedef struct {
    int data[CAP];
    int front;   /* index of the first element */
    int rear;    /* index of the last element; -1 before anything is queued */
} Queue;

void initQueue(Queue *q);
int  isEmpty(const Queue *q);
int  isFull(const Queue *q);
void enqueue(Queue *q, int value);
int  dequeue(Queue *q);
int  frontOf(const Queue *q);

#endif
"""

M1 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    Queue q;
    initQueue(&q);

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'n') {
            int v;
            if (scanf("%d", &v) != 1) break;
            if (isFull(&q)) printf("FULL\n");
            else { enqueue(&q, v); printf("OK\n"); }
        } else if (cmd == 'd') {
            if (isEmpty(&q)) printf("EMPTY\n");
            else printf("%d\n", dequeue(&q));
        } else if (cmd == 'f') {
            if (isEmpty(&q)) printf("EMPTY\n");
            else printf("%d\n", frontOf(&q));
        } else if (cmd == 'e') {
            printf("%s\n", isEmpty(&q) ? "YES" : "NO");
        }
    }
    return 0;
}
"""

S1 = r"""
#include "problem.h"

void initQueue(Queue *q) {
    /* TODO: which pair of values makes 'front > rear' true straight away? */
}

int isEmpty(const Queue *q) {
    return 0;   /* TODO */
}

int isFull(const Queue *q) {
    return 0;   /* TODO: rear has run off the end of the array */
}

void enqueue(Queue *q, int value) {
    /* TODO: rear moves forward, then store */
}

int dequeue(Queue *q) {
    return 0;   /* TODO: read at front, then front moves forward */
}

int frontOf(const Queue *q) {
    return 0;   /* TODO */
}
"""

A1 = r"""
#include "problem.h"

void initQueue(Queue *q) {
    q->front = 0;
    q->rear = -1;
}

int isEmpty(const Queue *q) {
    return q->front > q->rear;
}

int isFull(const Queue *q) {
    return q->rear >= CAP - 1;
}

void enqueue(Queue *q, int value) {
    q->data[++(q->rear)] = value;
}

int dequeue(Queue *q) {
    return q->data[(q->front)++];
}

int frontOf(const Queue *q) {
    return q->data[q->front];
}
"""

T1 = [
    "n 10\nn 20\nf\nd\nf\ne\nd\ne\nq\n",
    "n 1\nn 2\nn 3\nn 4\nn 5\nn 6\nf\nq\n",
    "n 1\nn 2\nd\nd\nn 3\nn 4\nn 5\nn 6\nf\nq\n",
    "d\nf\ne\nn 7\nd\nd\nq\n",
    "n 3\nn 1\nn 4\nd\nf\nn 1\nd\nd\ne\nd\ne\nq\n",
]

write_problem(
    PACK, UNIT, "p01-array-queue", title="Linear array queue (and why it wastes space)",
    mode="function", difficulty="easy", estimated_minutes=8, samples=1,
    topics=["queue", "arrays"],
    prereqs=[f"{PACK}.01-stack.p01-array-stack"],
    source="Rebuilt from NITC_Lab_S2 Lab9 P2 (hospital patient queue)",
    hints=[
        "Two indices moving in the same direction: front chases rear. "
        "init to front=0, rear=-1 so that front > rear reads as empty.",
        "enqueue is 'advance rear, then store'; dequeue is 'read at front, then "
        "advance front'. Mirror images of the stack's push and pop.",
        "isFull here is only about rear hitting CAP-1. It does not care that "
        "slots before front are free - that is the flaw this problem exists to show.",
    ],
    header=H1, harness=M1, starter=S1, solution=A1, tests=T1,
    statement=r"""
# Linear array queue (and why it wastes space)

A queue with two indices that only move forward. `front` points at the first
element, `rear` at the last.

## Commands
""" + CMDS + r"""
## Example

```
n 10
n 20
f
d
f
e
d
e
q
```

```
OK
OK
10
10
20
NO
20
YES
```

## Watch what test 3 does to you

```
n 1
n 2
d
d
n 3
n 4
n 5
n 6
```

Two enqueues, two dequeues, then four more enqueues. The queue holds at most one
item at a time - and yet the sixth `n` reports `FULL`, with `CAP` set to 5 and the
queue nearly empty.

That is not a bug in your code. `rear` has walked off the end of the array and the
slots behind `front` are stranded. Implement it exactly as specified, watch it
happen, and then go fix it properly in the next problem. Feeling the flaw is the
point of this rung.
""",
)

# --------------------------------------------------------------- p02
H2 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

#define CAP 5

/* Circular queue: indices wrap around with %, and an explicit count tells
   empty and full apart (front == rear alone cannot). */
typedef struct {
    int data[CAP];
    int front;   /* index of the first element */
    int size;    /* how many elements are currently stored */
} CircularQueue;

void initQueue(CircularQueue *q);
int  isEmpty(const CircularQueue *q);
int  isFull(const CircularQueue *q);
void enqueue(CircularQueue *q, int value);
int  dequeue(CircularQueue *q);
int  frontOf(const CircularQueue *q);

#endif
"""

M2 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    CircularQueue q;
    initQueue(&q);

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'n') {
            int v;
            if (scanf("%d", &v) != 1) break;
            if (isFull(&q)) printf("FULL\n");
            else { enqueue(&q, v); printf("OK\n"); }
        } else if (cmd == 'd') {
            if (isEmpty(&q)) printf("EMPTY\n");
            else printf("%d\n", dequeue(&q));
        } else if (cmd == 'f') {
            if (isEmpty(&q)) printf("EMPTY\n");
            else printf("%d\n", frontOf(&q));
        } else if (cmd == 'e') {
            printf("%s\n", isEmpty(&q) ? "YES" : "NO");
        }
    }
    return 0;
}
"""

S2 = r"""
#include "problem.h"

void initQueue(CircularQueue *q) {
    /* TODO */
}

int isEmpty(const CircularQueue *q) {
    return 0;   /* TODO: use size, not the indices */
}

int isFull(const CircularQueue *q) {
    return 0;   /* TODO */
}

void enqueue(CircularQueue *q, int value) {
    /* TODO: the next free slot is (front + size) wrapped around CAP.
       Store there, then grow size. */
}

int dequeue(CircularQueue *q) {
    /* TODO: take data[front], move front forward with wraparound, shrink size. */
    return 0;
}

int frontOf(const CircularQueue *q) {
    return 0;   /* TODO */
}
"""

A2 = r"""
#include "problem.h"

void initQueue(CircularQueue *q) {
    q->front = 0;
    q->size = 0;
}

int isEmpty(const CircularQueue *q) {
    return q->size == 0;
}

int isFull(const CircularQueue *q) {
    return q->size == CAP;
}

void enqueue(CircularQueue *q, int value) {
    int slot = (q->front + q->size) % CAP;
    q->data[slot] = value;
    q->size++;
}

int dequeue(CircularQueue *q) {
    int value = q->data[q->front];
    q->front = (q->front + 1) % CAP;
    q->size--;
    return value;
}

int frontOf(const CircularQueue *q) {
    return q->data[q->front];
}
"""

T2 = [
    "n 1\nn 2\nd\nd\nn 3\nn 4\nn 5\nn 6\nn 7\nf\ne\nq\n",
    "n 10\nn 20\nf\nd\nf\ne\nd\ne\nq\n",
    "n 1\nn 2\nn 3\nn 4\nn 5\nn 6\nf\nq\n",
    "n 1\nn 2\nn 3\nd\nd\nd\ne\nn 4\nn 5\nf\nd\nd\ne\nq\n",
    "d\nf\ne\nn 8\nf\nd\nd\ne\nn 9\nn 10\nn 11\nn 12\nn 13\nn 14\nf\nq\n",
]

write_problem(
    PACK, UNIT, "p02-circular-queue", title="Circular queue: reuse the stranded slots",
    mode="function", difficulty="medium", estimated_minutes=10, samples=1,
    topics=["queue", "arrays", "modular arithmetic"],
    prereqs=[f"{PACK}.{UNIT}.p01-array-queue"],
    source="Rebuilt from NITC_Lab_S2 Lab9 P5 (circular student queue)",
    hints=[
        "Keep front and size instead of front and rear. size makes empty and full "
        "trivially distinguishable, which front == rear alone cannot do.",
        "The slot to write into is (front + size) % CAP. Derive it: front is where "
        "element 0 sits, so element number 'size' sits size steps later, modulo CAP.",
        "dequeue advances front with q->front = (q->front + 1) % CAP and decrements "
        "size. The value in the vacated slot does not need clearing.",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    statement=r"""
# Circular queue: reuse the stranded slots

Same interface as the linear queue, one real change: the indices wrap. A slot
freed by `dequeue` becomes available again.

## The representation

This version stores `front` and `size` rather than `front` and `rear`:

```c
typedef struct {
    int data[CAP];
    int front;
    int size;
} CircularQueue;
```

Why not `front` and `rear`? Because with wraparound, `front == rear` is ambiguous -
it is true for both a completely empty and a completely full queue, and you cannot
tell which without extra information. Storing `size` removes the ambiguity outright.
(The other classic fix is to leave one slot permanently empty. Both work; this one
is easier to reason about.)

## Commands
""" + CMDS + r"""
## The same test that broke the linear queue

```
n 1
n 2
d
d
n 3
n 4
n 5
n 6
n 7
f
e
```

```
OK
OK
1
2
OK
OK
OK
OK
OK
3
NO
```

Nine enqueues through a five-slot array, no `FULL` in sight, because the two slots
released at the start got reused. That is the whole point of the wraparound.

## Where the modulo goes

The next free slot is `(front + size) % CAP`. Convince yourself of that before you
write it: `front` holds element 0, so element number `size` sits `size` steps
further along, wrapping at `CAP`.
""",
)

# --------------------------------------------------------------- p03
H3 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H

/* --- Linked stack, already implemented for you in a separate file. --- */
typedef struct _stack {
    int key;
    struct _stack *next;
} stacknode;

typedef stacknode *STACK;

STACK SINIT(void);
int   SISEMPTY(STACK s);
int   STOP(STACK s);
STACK SPUSH(STACK s, int value);
STACK SPOP(STACK s);

/* --- The queue you build out of two of them. Same shape as Week 3's QUEUE.h. --- */
typedef struct _queue {
    STACK F;   /* front stack: dequeue pops from here */
    STACK B;   /* back stack: enqueue pushes onto here */
} queuenode;

typedef queuenode *QUEUE;

QUEUE QINIT(void);
int   ISEMPTYQUEUE(QUEUE q);
QUEUE ENQUEUE(QUEUE q, int value);
QUEUE DEQUEUE(QUEUE q);      /* removes the front element */
int   FRONT(QUEUE q);        /* front element; caller checks ISEMPTYQUEUE first */

#endif
"""

E3 = r"""
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
"""

M3 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    QUEUE q = QINIT();

    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'q') break;
        if (cmd == 'n') {
            int v;
            if (scanf("%d", &v) != 1) break;
            q = ENQUEUE(q, v);
            printf("OK\n");
        } else if (cmd == 'd') {
            if (ISEMPTYQUEUE(q)) printf("EMPTY\n");
            else { printf("%d\n", FRONT(q)); q = DEQUEUE(q); }
        } else if (cmd == 'f') {
            if (ISEMPTYQUEUE(q)) printf("EMPTY\n");
            else printf("%d\n", FRONT(q));
        } else if (cmd == 'e') {
            printf("%s\n", ISEMPTYQUEUE(q) ? "YES" : "NO");
        }
    }
    return 0;
}
"""

S3 = r"""
#include <stdlib.h>
#include "problem.h"

QUEUE QINIT(void) {
    QUEUE q = malloc(sizeof(queuenode));
    q->F = SINIT();
    q->B = SINIT();
    return q;
}

int ISEMPTYQUEUE(QUEUE q) {
    return 0;   /* TODO: the queue is empty only when BOTH stacks are empty */
}

QUEUE ENQUEUE(QUEUE q, int value) {
    /* TODO: this is the cheap one - push onto B and return. */
    return q;
}

/* Helper worth writing: if F is empty, pour everything from B into F.
   Popping B and pushing onto F reverses the order, which is exactly what
   turns last-in-first-out into first-in-first-out. */
static void pour(QUEUE q) {
    /* TODO */
}

QUEUE DEQUEUE(QUEUE q) {
    /* TODO: make sure F has something (pour if needed), then pop F. */
    return q;
}

int FRONT(QUEUE q) {
    /* TODO: same pouring rule, but read instead of remove. */
    return 0;
}
"""

A3 = r"""
#include <stdlib.h>
#include "problem.h"

QUEUE QINIT(void) {
    QUEUE q = malloc(sizeof(queuenode));
    q->F = SINIT();
    q->B = SINIT();
    return q;
}

int ISEMPTYQUEUE(QUEUE q) {
    return SISEMPTY(q->F) && SISEMPTY(q->B);
}

QUEUE ENQUEUE(QUEUE q, int value) {
    q->B = SPUSH(q->B, value);
    return q;
}

/* Only ever called when F is empty, so each element moves across at most once. */
static void pour(QUEUE q) {
    if (!SISEMPTY(q->F)) return;
    while (!SISEMPTY(q->B)) {
        q->F = SPUSH(q->F, STOP(q->B));
        q->B = SPOP(q->B);
    }
}

QUEUE DEQUEUE(QUEUE q) {
    pour(q);
    if (!SISEMPTY(q->F)) q->F = SPOP(q->F);
    return q;
}

int FRONT(QUEUE q) {
    pour(q);
    return STOP(q->F);
}
"""

T3 = [
    "n 1\nn 2\nn 3\nf\nd\nf\nd\nd\ne\nq\n",
    "n 1\nd\nn 2\nd\nn 3\nd\ne\nd\nq\n",
    "e\nd\nf\nn 5\ne\nf\nd\ne\nq\n",
    "n 10\nn 20\nd\nn 30\nn 40\nd\nd\nn 50\nd\nd\ne\nq\n",
    "n 7\nn 8\nn 9\nn 10\nd\nd\nn 11\nf\nd\nd\nd\ne\nq\n",
]

write_problem(
    PACK, UNIT, "p03-queue-two-stacks", title="A queue built from two stacks",
    mode="function", difficulty="medium", estimated_minutes=14, samples=1,
    topics=["queue", "stack", "amortized analysis"],
    prereqs=[f"{PACK}.01-stack.p03-linked-stack",
             f"{PACK}.{UNIT}.p01-array-queue"],
    source="Matches QUEUE.h from NITC_Lab_S3_DSA Week 3 - Graphs",
    hints=[
        "Enqueue is the easy half: push onto B, done. All the thinking lives in "
        "dequeue.",
        "Popping every element off B and pushing each onto F reverses them. A "
        "reversed LIFO is a FIFO - that single observation is the whole trick.",
        "Only pour when F is empty. If you pour on every dequeue you get the right "
        "answers but ruin the running time, because elements move back and forth "
        "repeatedly instead of crossing once.",
    ],
    header=H3, harness=M3, starter=S3, solution=A3, tests=T3,
    extra={"stack_ops.c": E3},
    statement=r"""
# A queue built from two stacks

This is the structure your Week 3 `QUEUE.h` actually declares:

```c
typedef struct _queue { STACK F, B; } queuenode;
```

A queue made of two stacks and nothing else. The linked stack is provided; you
write the five queue functions.

## The idea

- **`ENQUEUE`** pushes onto `B` (back). Cheap, always.
- **`DEQUEUE`** pops from `F` (front). But `F` starts empty, so when it is empty
  you first **pour** `B` into `F`: pop every element off `B` and push it onto `F`.

Pouring reverses the order. A stack hands back the newest first; after one
reversal it hands back the oldest first. That is a queue.

## Commands
""" + CMDS + r"""
except `n v` always prints `OK` here - there is no capacity limit.

## Example

```
n 1
n 2
n 3
f
d
f
d
d
e
q
```

```
OK
OK
OK
1
1
2
2
3
YES
```

## Only pour when F is empty

The condition matters more than it looks. Pour **only** when `F` is empty, never
otherwise. Get that right and each element crosses between the stacks exactly
once in its lifetime, so `n` operations cost `O(n)` total - `O(1)` amortized each,
even though one individual dequeue might do `O(n)` work.

Pour on every dequeue and you still get every answer right, and every test here
still passes. It is just quadratic. This is the cheapest possible introduction to
the difference between "correct" and "correct and fast", and it is worth
internalising before Dijkstra, where the same distinction decides whether your
solution is `O(V^2)` or `O(E log V)`.
""",
)

report(UNIT, 3)
