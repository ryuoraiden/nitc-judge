# Min-heap priority queue (the one Dijkstra uses)

Same array-heap machinery, three changes: it is a **min**-heap, it carries a
payload alongside the priority, and it supports insertion (so it grows, rather than
being built once from a fixed array).

```c
typedef struct { int key; int id; } Item;
```

`key` is the priority. `id` is the payload - it will be a vertex number when you
get to Dijkstra.

## Ordering, including ties

Smallest `key` comes out first. **If two items have the same `key`, the smaller
`id` comes out first.**

(This is **not** the rule from the PD Lab 11 ticket and patient questions this is
rebuilt from: those were *max*-priority queues where ties go to whoever arrived first.
Same machinery, different comparison - read which one a question asks for.)

That tie-break is not decoration. Without it, which of two equal-key items surfaces
first depends on incidental swap order, and the same program could print different
valid answers on different days. Pinning the rule makes the output deterministic and
therefore testable. Write the comparison once as a helper and call it from both the
bubble-up and the sift-down.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i key id` | insert | `OK` |
| `x` | extract minimum | `key id`, or `EMPTY` |
| `e` | is it empty? | `YES` or `NO` |
| `q` | quit | nothing |

## Example

```
i 5 1
i 3 2
i 8 3
x
x
x
x
q
```

```
OK
OK
OK
3 2
5 1
8 3
EMPTY
```

## Two loops, opposite directions

**`heapInsert`** puts the new item at the end and bubbles it *up* while it beats
its parent. A new item can only ever be too small for where it landed, so up is the
only direction it can move.

**`heapExtractMin`** saves `a[0]`, moves the *last* item into the root, shrinks the
heap, then sifts *down*. Moving the last element in (rather than, say, promoting the
smaller child repeatedly) is what keeps the tree complete, which is what lets the
whole structure live in a flat array with no pointers.
