# Balanced? Diameter? Mirror it.

Three recursion questions that come up constantly. The hidden `main()` prints
`isBalanced`, then `diameter`, then the **preorder of the tree after `mirror`**.

```c
int  isBalanced(Node *root);  /* at every node, child heights differ by <= 1 */
int  diameter(Node *root);    /* longest path between any two nodes, in EDGES */
void mirror(Node *root);      /* swap children everywhere, in place */
```

The tree is one line in either parenthesized notation.

## Example

```
( 1 ( 2 ( 4 ( ) ( ) ) ( 5 ( ) ( ) ) ) ( 3 ( ) ( ) ) )
```

```
1
3
1 3 2 5 4
```

The longest path is `4 - 2 - 1 - 3`: three edges.

## One pass, not two

The obvious `isBalanced` calls `height()` on both children at every node - `O(n^2)` on
a skewed tree. The better one computes heights bottom-up and returns a sentinel `-1` as
soon as some subtree is unbalanced:

```c
int l = checkedHeight(r->left);  if (l < 0) return -1;
int h = checkedHeight(r->right); if (h < 0) return -1;
if (abs(l - h) > 1) return -1;
return 1 + max(l, h);
```

## Diameter bends somewhere

Any longest path has a highest node where it turns. There it goes down as deep as
possible on the left and on the right, so its length in edges is
`height(left) + height(right)` (heights in nodes). Evaluate that at every node while
computing heights, and keep the maximum. The longest path **does not have to pass
through the root** - test 4 is built so that it doesn't.

## Mirror

Swap, then recurse into both sides. Four lines; the preorder of a mirrored tree is the
original's "root, right, left" order.
