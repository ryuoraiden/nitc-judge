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
