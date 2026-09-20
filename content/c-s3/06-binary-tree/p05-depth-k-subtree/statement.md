# PD Lab 10 Q2: nodes at depth k below x

Verbatim from PD Lab 10.

> Given the parenthesis representation of a binary tree `T` with `n` nodes, a node with
> key value `x` and a positive integer `k < n`, print all the nodes at a depth of `k` in
> the subtree of `T` rooted at `x`. Assume that all key values in the tree are unique.

## Input format

- first line: the space-separated parentheses representation of the tree
- second line: the integer `x`
- third line: the integer `k`

## Output format

One line with the key values at depth `k` below `x`, space separated, left to right.
If there are none, print an empty line.

## Sample

```
( 2 ( 7 ( 10 ( ) ( ) ) ( 6 ( 5 ( ) ( ) ) ( 11 ( ) ( ) ) ) ) ( 9 ( ) ( 3 ( ) ( ) ) ) )
7
2
```

```
5 11
```

## The input trap

The tree line contains spaces, so `scanf("%s")` reads only `(`. Read the whole line
with `fgets` first, **then** `scanf` the two integers. Doing it in the other order does
not work either: a `scanf` before `fgets` leaves a newline that `fgets` swallows as an
empty line.
