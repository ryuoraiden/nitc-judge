# BST queries: LCA, floor, ceil, range

Four short questions that each use the BST ordering to walk **one path** instead of
searching the whole tree.

```c
int  lcaBST(Node *root, int a, int b);          /* both keys present */
int  floorKey(Node *root, int x);               /* largest key <= x, or -1 */
int  ceilKey(Node *root, int x);                /* smallest key >= x, or -1 */
void printRange(Node *root, int lo, int hi);    /* keys in [lo, hi], ascending */
```

## Commands

`i x` insert, `l a b` LCA, `f x` floor, `c x` ceil, `r lo hi` range, `e` exit.

## Example

```
i 20
i 8
i 22
i 4
i 12
i 10
i 14
l 10 14
l 14 8
l 10 22
f 13
c 13
f 3
c 23
r 9 15
e
```

```
12
8
20
12
14
-1
-1
10 12 14
```

## The shared idea

At every node the ordering tells you which side the answer must be on:

| question | at node `r` |
|---|---|
| LCA of `a`, `b` | both `< r` -> left; both `> r` -> right; otherwise `r` is the answer |
| floor of `x` | `r > x` -> left; `r <= x` -> **candidate**, then right to look for a bigger one |
| ceil of `x` | mirror: `r >= x` -> candidate, then left |
| range `[lo, hi]` | skip the left subtree if `r <= lo`, skip the right if `r >= hi` |

Compare with the plain binary-tree LCA from unit 06, which has to search both subtrees
at every node. The BST version is a single loop.

The floor/ceil "remember the last candidate on the way down" is the same trick as the
no-parent successor in unit 07 - worth noticing, because it answers a whole family of
"closest key" questions.
