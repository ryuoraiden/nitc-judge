# k-th smallest and successor without a parent pointer

PD Lab 12 Q2 says explicitly: *"When you define the structure for a node of the BST, it
should not contain the parent pointer"* and *"Your program should not contain any
arrays."* So both of these have to work top-down.

```c
int kthSmallest(Node *root, int k);    /* -1 if the tree has fewer than k nodes */
int maximum(Node *root);               /* -1 if empty */
int successorOf(Node *root, int key);  /* -1 if there is no larger key */
```

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i k` | insert | nothing |
| `k n` | n-th smallest | the key, or `-1` |
| `m` | maximum | the key, or `-1` |
| `n k` | successor of `k` | the key, or `-1` |
| `e` | exit | nothing |

## Example

```
i 5
i 3
i 10
i 15
k 1
k 2
k 3
k 4
m
n 5
n 15
e
```

```
3
5
10
15
15
10
-1
```

## k-th smallest

Inorder is sorted, so the k-th smallest is simply the k-th node inorder visits. Keep a
counter, increment it *between* the two recursive calls, and stop when it reaches `k`.

The counter must be shared across the whole traversal, so pass it as `int *count` - a
plain `int` parameter would give every recursive call its own copy and the count would
reset on the way back up. (This is the `*count` pattern your Lab 12 solution uses.)

Time is `O(n)` in the worst case, which is what the sheet asks for.

## Successor without climbing

With no parent pointer you cannot walk up, so collect the answer on the way **down**:

- if `key < cur->key`, then `cur` is bigger than `key` - it is a *candidate*. Record it
  and go left to look for something smaller that is still bigger than `key`.
- otherwise `cur` is too small to be the answer; go right.

The last candidate you recorded is the successor. Nothing recorded means `key` is the
maximum. Note this even works when `key` itself is not in the tree - it finds the
smallest key greater than it.
