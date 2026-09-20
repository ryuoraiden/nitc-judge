# Left, right and top views

*Optional variation.* Three views of the same tree, all built on level order.

- **Left view**: the first node of each level.
- **Right view**: the last node of each level.
- **Top view**: looking down from above. Give the root horizontal distance 0, a left
  child `hd - 1` and a right child `hd + 1`. For each distance, the node seen from above
  is the first one a level-order traversal reaches. Print from the leftmost column.

Each function prints one line.

## Input notation

One line holding the tree in either NITC parenthesized notation:

```
( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )
(20(11(2)())(8(6)(10)))
```

`( )` or `()` is an empty child; a leaf may appear bare as `(2)`. The tree is parsed
for you before your function is called.

## Example

```
( 1 ( 2 ( 4 ( ) ( ) ) ( 5 ( ) ( ) ) ) ( 3 ( ) ( 6 ( ) ( ) ) ) )
```

```
1 2 4
1 3 6
4 2 1 3 6
```

## Storing one value per column

`hd` is always between `-n` and `n`, so an ordinary array indexed by `hd + n` holds the
first value seen in each column. Remember the smallest and largest `hd` you saw so you
know where to start and stop printing.
