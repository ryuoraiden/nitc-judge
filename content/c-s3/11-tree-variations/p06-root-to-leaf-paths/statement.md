# Root-to-leaf paths and path sums

```c
void rootToLeaf(Node *root, int target);
```

Print every root-to-leaf path, left to right, keys joined by `->`. Then print how many of
those paths have keys summing to `target`.

## Input

The tree on one line, then `target`.

## Example

```
( 5 ( 4 ( 11 ( 7 ( ) ( ) ) ( 2 ( ) ( ) ) ) ( ) ) ( 8 ( 13 ( ) ( ) ) ( 4 ( ) ( 1 ( ) ( ) ) ) ) )
22
```

```
5->4->11->7
5->4->11->2
5->8->13
5->8->4->1
1
```

Only `5 + 4 + 11 + 2 = 22`.

## Backtracking without undoing

Keep the current path in an array indexed by depth. A call at depth `d` writes its key
into `path[d]`; when it returns and the sibling call runs at the same depth, it simply
**overwrites** `path[d]`. Nothing ever has to be popped. The running sum works the same
way when passed as a parameter: each call has its own copy.

## What counts as a leaf

Both children `NULL`. If you print when you reach a `NULL` child instead, a node with
two empty children prints its path twice, and a node with one child prints a path that
does not end at a leaf.
