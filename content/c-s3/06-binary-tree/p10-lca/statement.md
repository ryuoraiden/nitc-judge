# Lowest common ancestor

*Optional variation.* The lowest node that has both `a` and `b` in its subtree (a node
counts as its own ancestor).

## Input

The tree line, then `q`, then `q` lines `a b`. Print one LCA value per query.

## Example

```
( 3 ( 5 ( 6 ( ) ( ) ) ( 2 ( 7 ( ) ( ) ) ( 4 ( ) ( ) ) ) ) ( 1 ( 0 ( ) ( ) ) ( 8 ( ) ( ) ) ) )
4
5 1
5 4
7 4
6 8
```

```
3
5
2
3
```

## The recursion

Each call returns "whichever of `a` / `b` I found in my subtree", or `NULL`. If both
children report something, the targets are on different sides and **this** node is the
LCA. If only one does, pass it upward. In a BST (next unit) there is a faster version
that uses the ordering instead of searching both sides.
