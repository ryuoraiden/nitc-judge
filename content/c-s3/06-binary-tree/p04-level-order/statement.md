# Level order, one line per level

BFS on a tree: visit the root, then everything at depth 1, then depth 2, and so on.

```c
void levelOrder(Node *root);
```

Print each level on its own line, left to right, each value followed by a space.

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
(120(5(25(15)(10))(20(6)(7)))(85(130)(135()(200))))
```

```
120
5 85
25 20 130 135
15 10 6 7 200
```

## Splitting the levels

A plain BFS prints everything on one line. To break it into levels, look at the queue
at the start of each level: **it contains exactly the nodes of that level and nothing
else**. So record `size = tail - head`, pop exactly `size` nodes, and print a newline.
Everything those nodes pushed belongs to the next level.

## The queue holds pointers

`static Node *q[MAXQ];` - an array of `Node *`. It is `static` so a large capacity
does not sit on the function's stack frame.
