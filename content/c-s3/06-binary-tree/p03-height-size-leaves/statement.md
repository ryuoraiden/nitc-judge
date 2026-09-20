# Height, size and leaves

Three recursive functions with the same skeleton: a base case for `NULL`, then combine
what the two children report.

```c
int height(Node *root);       /* nodes on the longest root-to-leaf path, 0 if empty */
int countNodes(Node *root);
int countLeaves(Node *root);
```

The hidden `main()` prints `height nodes leaves` on one line.

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
3 4 2
```

## Height: nodes or edges?

Textbooks disagree. Here height counts **nodes**, so a single node has height 1 and an
empty tree 0. The other convention counts edges (single node 0, empty -1). In a test,
read which one the question means - an off-by-one here fails every test case at once.
