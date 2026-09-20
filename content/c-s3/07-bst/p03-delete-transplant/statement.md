# BST deletion (transplant, all three cases)

The single most test-worthy BST operation, and the one people get 80% right.

```c
BST transplant(BST T, BST u, BST v);   /* put subtree v where subtree u was */
BST delete(BST T, BST x);
```

Both return the root, because deleting the root changes it.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i k` | insert | nothing |
| `d k` | delete the node holding `k` | `NOT PRESENT` if there is no such key |
| `p` | inorder | keys, or `NULL` |
| `t` | preorder | keys, or `NULL` |
| `e` | exit | nothing |

Both traversals are printed on purpose: inorder stays sorted no matter how badly you
mangle the shape, so **only the preorder reveals a wrong deletion**.

## The three cases

1. **No left child** - replace `x` with `x->right`. (Covers leaves too: `x->right` is
   `NULL`, and transplanting `NULL` is exactly what a leaf needs.)
2. **No right child** - replace `x` with `x->left`.
3. **Two children** - the replacement must be `x`'s **successor**, `y = minimum(x->right)`:
   the smallest key bigger than everything on the left and smaller than everything
   remaining on the right. Two sub-cases:
   - `y` is `x`'s direct right child: just transplant `x` with `y` and give `y` the
     left subtree.
   - `y` is deeper: first lift `y` out of where it is with `transplant(T, y, y->right)`,
     give `y` the old `x->right`, and only then transplant `x` with `y`.

## Example

```
i 15
i 6
i 18
i 3
i 7
i 17
i 20
i 13
i 9
p
t
d 6
p
t
e
```

```
3 6 7 9 13 15 17 18 20
15 6 3 7 13 9 18 17 20
3 7 9 13 15 17 18 20
15 7 3 13 9 18 17 20
```

Deleting 6 (two children) promotes 7, its successor.

## Why `y->parent != x` matters

If the successor is `x`'s direct right child, it is already in the right place and
lifting it out first would detach the subtree you are about to hand it. If it is
deeper, you *must* lift it first. Handling only one of the two sub-cases is the
classic half-correct deletion: it passes every test where the successor happens to be
adjacent and corrupts the tree everywhere else.

## Successor or predecessor?

Either is valid BST-wise, but they give **different shapes**, and the preorder output
here is checked against the successor version - the one CLRS and your Week 2 sheet use.
