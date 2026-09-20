# Preorder, inorder, postorder

The three depth-first traversals. Each is the same three-line recursion with the
`printf` in a different place - make sure you can write all three without thinking,
because every other tree problem is built on them.

```c
void preorder(Node *root);   /* root, left, right */
void inorder(Node *root);    /* left, root, right */
void postorder(Node *root);  /* left, right, root */
```

Print each value followed by a single space. The hidden `main()` prints the newline.

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
( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )
```

```
1 2 4 3
4 2 1 3
4 2 3 1
```

## Reading them off a picture quickly

For a hand-check under exam pressure: walk around the tree anticlockwise starting at
the root's left. Preorder records each node the first time you pass it (on its left
side), inorder when you pass underneath it, postorder the last time (on its right side).
