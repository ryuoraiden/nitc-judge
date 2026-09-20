# BST insert and search

The two operations everything else is built on.

```c
Node *insertKey(Node *root, int key);   /* returns the (possibly new) root */
Node *searchKey(Node *root, int key);   /* NULL if the key is absent */
```

## Commands the hidden main() understands

| Command | Meaning | Prints |
|---|---|---|
| `i k` | insert `k` | nothing |
| `s k` | search | `PRESENT` or `NOT PRESENT` |
| `p` | inorder | the keys, or `NULL` if the tree is empty |
| `t` | preorder | the keys, or `NULL` if the tree is empty |
| `e` | exit | nothing |

## Example

```
i 5
i 3
i 10
i 15
p
t
s 10
s 7
e
```

```
3 5 10 15
5 3 10 15
PRESENT
NOT PRESENT
```

## Why inorder comes out sorted

Inorder visits left subtree, node, right subtree - and in a BST everything in the left
subtree is smaller and everything in the right is larger. So inorder is *always*
sorted. That is the single most useful fact about BSTs: whenever a question asks for
"the k-th smallest", "the successor", or "is this a valid BST", it is really asking
you to think about the inorder sequence.

Preorder is printed too because inorder alone cannot tell two different BSTs apart -
`1 2 3` is the inorder of every BST on those keys. Preorder pins down the shape.

## The return-value discipline

`insertKey` returns a root because the recursive call may create a new node that has
to be linked in:

```c
root->left = insertKey(root->left, key);
```

Writing just `insertKey(root->left, key);` compiles perfectly and builds a tree that
never grows past its root.
