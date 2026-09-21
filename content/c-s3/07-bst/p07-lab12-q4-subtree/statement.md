# PD Lab 12 Q4: is BST1 a subtree of BST2?

**Official statement** - PD Lab 12, Q4. Tests 1-3 are the sheet's three samples.

> A BST (BST1) is considered a subtree of BST2 if there exists a node in BST2 such that
> the subtree rooted at that node is **identical** to BST1.

## Input format

- `N1`, then `N1` book IDs inserted into BST1 in that order
- `N2`, then `N2` book IDs inserted into BST2 in that order

## Output format

`BST1 is a subtree of BST2` or `BST1 is NOT a subtree of BST2`.

## Samples

```
3
3 1 5
5
10 5 15 1 3
```

```
BST1 is NOT a subtree of BST2
```

```
3
4 2 5
6
6 4 8 2 5 7
```

```
BST1 is a subtree of BST2
```

In sample 1 the keys 1, 3 and 5 all appear in BST2, but not in BST1's shape. 5 is the
parent of 1 there, and 3 hangs below 1. "Contains the keys" is not "is a subtree".

## Two functions

```c
int identical(Node *a, Node *b) {
    if (a == NULL || b == NULL) return a == b;
    return a->key == b->key && identical(a->left, b->left) && identical(a->right, b->right);
}
```

Then find the candidate. In a general binary tree you would have to try `identical` at
every node of BST2. Here the keys are unique and ordered, so **exactly one** node can
match: the one holding BST1's root key. Find it with an ordinary `O(h)` BST search and
compare once.

## Identical means all of it

Test 7 has BST1 = `5(3, 7)` and a BST2 where 5 has children 3 and 7, but 7 has a child
of its own. The top of the subtree matches and the whole thing does not, so the answer
is NOT.
