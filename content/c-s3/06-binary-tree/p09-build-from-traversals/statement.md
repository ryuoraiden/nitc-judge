# Rebuild a tree from preorder + inorder

*Optional variation.* Given the preorder and inorder sequences of a tree with distinct
values, rebuild it. The hidden `main()` prints the postorder of what you built.

## Input

`n`, then the preorder sequence, then the inorder sequence.

## Example

```
7
1 2 4 5 3 6 7
4 2 5 1 6 3 7
```

```
4 5 2 6 7 3 1
```

## The idea in one sentence

Preorder tells you **who the root is** (its first element); inorder tells you **how
the rest splits** (everything left of the root is the left subtree). Recurse on both
halves.

In C you do not need to copy sub-arrays: `pre + 1` is a pointer to the rest of the
preorder array, and a recursive call on `(pre + 1, in, k)` sees exactly the left
subtree's slice.
