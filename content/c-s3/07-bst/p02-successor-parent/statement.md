# Week 2 ADT: minimum, maximum, successor, predecessor

This is the node from your Week 2 assignment sheet, parent pointer and all:

```c
typedef struct _BSTNode {
    int key;
    struct _BSTNode *left, *right, *parent;
} BSTNode;
typedef BSTNode *BST;
```

`init`, `insert` and `search` are provided (and `insert` maintains `parent` for you).
You write the four navigation functions.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i k` | insert | nothing |
| `m` | minimum | the key, or `-1` if the tree is empty |
| `x` | maximum | the key, or `-1` |
| `n k` | successor of the node holding `k` | the key, or `-1` if none |
| `r k` | predecessor | the key, or `-1` if none |
| `e` | exit | nothing |

## Example

```
i 15
i 6
i 18
i 3
i 7
i 17
i 20
i 13
i 9
m
x
n 13
n 15
n 20
e
```

```
3
20
15
17
-1
```

## Successor: the two cases

**If `x` has a right subtree**, the successor is the *minimum of that subtree* - go
right once, then left as far as you can.

**If it does not**, then you have already visited everything in `x`'s subtree, so the
next key must be above you. Walk up the parent pointers **while `x` is a right child**.
Climbing from a right child means the parent is smaller than you, so it cannot be the
answer. The first time you arrive at a parent from its *left*, that parent is the
successor. If you walk off the top into `NULL`, `x` held the maximum.

`predecessor` is the exact mirror: left subtree's maximum, or climb while `x` is a
*left* child.

## What the parent pointer buys you

Week 2's ADT stores `parent` specifically so case 2 is a simple upward walk. PD Lab 12
Q2 explicitly forbids the parent pointer - there you find the successor by searching
down from the root and remembering the last node you turned *left* at. Both are `O(h)`;
know both, because the two sheets ask for different ones.
