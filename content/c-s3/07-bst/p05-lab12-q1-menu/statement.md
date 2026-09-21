# PD Lab 12 Q1: BST menu (insert, search, delete, traversals)

**Official statement** - PD Lab 12, Q1. Test 1 is the sheet's sample.

> Write a menu driven C program for a Binary search tree (BST) of integers... The list
> of menu options are `i`, `p`, `d`, `s`, `t`, `b` or `e`.
>
> **NOTE:** Your program should not contain any arrays. Assume that the BST at every stage
> always has unique key values. Insert, search and delete must be `O(h)`; the
> traversals `O(n)`.

## Commands

| Input | Function | Output |
|---|---|---|
| `i num` | `InsertKey(Root, num)` | nothing |
| `s num` | `SearchKey(Root, num)` | `PRESENT` or `NOT PRESENT` |
| `d num` | `DeleteKey(Root, num)` | see below |
| `p` | `Inorder(Root)` | the keys, or `NULL` if empty |
| `t` | `Preorder(Root)` | the keys, or `NULL` if empty |
| `b` | `Postorder(Root)` | the keys, or `NULL` if empty |
| `e` | exit | nothing |

## Sample

```
i 5
i 3
i 10
i 15
p
s 10
d 10
p
i 1
i 2
p
t
b
e
```

```
3 5 10 15
PRESENT
3 5 15
1 2 3 5 15
5 3 1 2 15
2 1 3 15 5
```

## Two things the sheet leaves open

**Deleting a key that is not there.** The sheet says both `NOT PRESENT in the BST` (in
the function list) and nothing at all (in the output spec). These tests **never delete an
absent key**, so either choice passes. In the exam, pick one and say which.

**Which node replaces a deleted node with two children.** These tests use the inorder
**successor** (smallest key in the right subtree), the standard textbook choice. The
predecessor gives a different but equally valid tree, so its preorder differs from
these tests. If your lab evaluator used predecessor, only tests 3 and 4 would disagree.

## Delete without a parent pointer

Unlike the Week 2 ADT, there is no `parent` field here, so transplant is not available.
The recursive form re-links as it returns:

```c
if (num < root->key)      root->left  = DeleteKey(root->left, num);
else if (num > root->key) root->right = DeleteKey(root->right, num);
else { /* found: 0, 1 or 2 children */ }
return root;
```

For two children, copy the successor's key into this node, then delete that key from
the right subtree - which is now a 0- or 1-child case.

## "No arrays"

The sheet forbids arrays, so no queue for level order and no buffer for traversals.
Recursion handles all three traversals without one.
