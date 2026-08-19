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
