# Week 2 modification: delete by rank

**This is a reconstruction** of your Week 2 modification question. The exact I/O is
lost; the task - delete the node by its *rank* rather than its key - is what matters.

> Using the Week 2 BST ADT (nodes with a parent pointer), support deleting the node of
> **rank `k`**, i.e. the `k`-th smallest key.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i x` | insert `x` | nothing |
| `r k` | delete the `k`-th smallest node | its key, or `-1` if there is no rank `k` |
| `p` | inorder | keys, or `NULL` |
| `t` | preorder | keys, or `NULL` |
| `e` | exit | nothing |

Deletion is the standard two-children-means-successor delete, so the **preorder** after
a deletion is fixed.

## Sample

```
i 50
i 30
i 70
i 20
i 40
i 60
i 80
r 4
p
t
r 1
p
t
r 5
p
t
e
```

```
50
20 30 40 60 70 80
60 30 20 40 70 80
20
30 40 60 70 80
60 30 40 70 80
80
30 40 60 70
60 30 40 70
```

Rank 4 of seven keys is the root, 50; its successor 60 takes its place.

## The twist is composition

"Delete by rank" is two things you already have: the inorder-counter search from
`kthSmallest`, and the transplant delete. The only glue is making the search return
the **node** (so `delete` can take it directly) instead of printing its key.

## If they ask for it in O(h)

Counting through inorder is `O(n)`. The textbook way to do it in `O(h)` is an
**order-statistic tree**: every node also stores `size`, the number of nodes in its
subtree. Then rank `k` is found by comparing `k` with `size(left) + 1` at each node and
going left or right - like binary search. The price is updating `size` on every
insert and delete. If a question insists on `O(h)` for rank queries, that is what it
wants.
