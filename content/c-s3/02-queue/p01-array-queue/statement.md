# Linear array queue (and why it wastes space)

A queue with two indices that only move forward. `front` points at the first
element, `rear` at the last.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `n v` | enqueue `v` | `OK`, or `FULL` |
| `d` | dequeue | the value removed, or `EMPTY` |
| `f` | front | the front value, or `EMPTY` |
| `e` | is it empty? | `YES` or `NO` |
| `q` | quit | nothing |

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
