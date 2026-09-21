# Is this binary tree a BST?

```c
int isBST(Node *root);   /* 1 or 0; duplicates are not allowed */
```

## Input

The number of trees `q`, then `q` lines, each a tree in either parenthesized
notation. Print `YES` or `NO` for each.

## Example

```
7
( 10 ( 5 ( ) ( ) ) ( 15 ( 12 ( ) ( ) ) ( 20 ( ) ( ) ) ) )
( 10 ( 5 ( ) ( ) ) ( 15 ( 6 ( ) ( ) ) ( 20 ( ) ( ) ) ) )
( 10 ( 5 ( ) ( 11 ( ) ( ) ) ) ( 15 ( ) ( ) ) )
( 7 ( ) ( ) )
( 5 ( 5 ( ) ( ) ) ( ) )
(2(1)(3))
(2(3)(1))
```

```
YES
NO
NO
YES
NO
YES
NO
```

## The trap in tree 2

```
      10
     /  \
    5    15
        /  \
       6    20
```

Check each node against its own children only: `5 < 10 < 15` fine, `6 < 15 < 20` fine.
Looks valid - but 6 sits in 10's **right** subtree and is smaller than 10. The local
check misses it.

## The fix: pass the allowed range down

Every node lives inside an interval set by its ancestors. The root may be anything;
going left, the upper bound becomes the parent's key; going right, the lower bound
does:

```c
static int check(Node *r, long long lo, long long hi) {
    if (r == NULL) return 1;
    if (r->key <= lo || r->key >= hi) return 0;
    return check(r->left, lo, r->key) && check(r->right, r->key, hi);
}
```

The equivalent alternative: do an inorder traversal and check the sequence is
**strictly increasing**. Same answer, and a good one to mention in a viva.
