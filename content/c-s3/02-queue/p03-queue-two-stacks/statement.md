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

| Command | Meaning | Prints |
|---|---|---|
| `n v` | enqueue `v` | `OK`, or `FULL` |
| `d` | dequeue | the value removed, or `EMPTY` |
| `f` | front | the front value, or `EMPTY` |
| `e` | is it empty? | `YES` or `NO` |
| `q` | quit | nothing |

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
