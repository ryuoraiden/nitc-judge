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

| Command | Meaning | Prints |
|---|---|---|
| `n v` | enqueue `v` | `OK`, or `FULL` |
| `d` | dequeue | the value removed, or `EMPTY` |
| `f` | front | the front value, or `EMPTY` |
| `e` | is it empty? | `YES` or `NO` |
| `q` | quit | nothing |

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
