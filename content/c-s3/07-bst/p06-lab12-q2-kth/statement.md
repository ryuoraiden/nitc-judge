# PD Lab 12 Q2: k-th smallest, maximum, successor (no parent pointer)

**Official statement** - PD Lab 12, Q2. Test 1 is the sheet's sample.

> Design a C program featuring a menu-driven interface for a binary search tree (BST)
> consisting of integers that can output the k-th smallest integer in the tree...
>
> **NOTE:** When you define the structure for a node of the BST, it **should not contain
> the parent pointer**. Your program **should not contain any arrays**. Assume that the
> BST at every stage always has unique key values.
>
> Insert, search, delete, maximum and successor `O(h)`; k-th smallest `O(n)`.

## Commands

| Input | Function | Output |
|---|---|---|
| `i num` | `InsertKey` | nothing |
| `s num` | `SearchKey` | `PRESENT` or `NOT PRESENT` |
| `d num` | `DeleteKey` | `NOT PRESENT` if `num` is not in the tree |
| `k k` | `KthSmallest` | the k-th smallest key |
| `m` | `Maximum` | the largest key |
| `n num` | `Successor` | the next key after `num` in inorder |
| `e` | exit | nothing |

## Sample

```
i 5
i 3
i 10
i 15
k 3
d 10
k 3
i 10
k 2
s 10
m
n 5
e
```

```
10
15
5
PRESENT
15
10
```

## What the tests avoid

The sheet does not say what to print for `k` larger than the tree, `m` on an empty
tree, or `n` on the maximum. The tests never ask those, so any behaviour passes. In the
exam, printing nothing (or `-1`) and saying so is reasonable.

## Successor without climbing

With no parent pointer you cannot walk up, so collect the answer on the way **down**:
whenever `num < root->key`, the current node is bigger than `num` - a candidate -
so remember it and go left to look for something smaller. Otherwise go right. The last
remembered candidate is the successor.
