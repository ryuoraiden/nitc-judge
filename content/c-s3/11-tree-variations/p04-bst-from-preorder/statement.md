# Rebuild a BST from its preorder

Given the preorder traversal of a BST, rebuild it and print its postorder, its level
order, and its height.

## Input format

`n`, then `n` distinct keys: the preorder sequence.

## Output format

Three lines: postorder, level order (both space separated), and the height counted in
nodes.

## Sample

```
7
50 30 20 40 70 60 80
```

```
20 40 30 60 80 70 50
50 30 70 20 40 60 80
3
```

## Why preorder alone is enough here

For a general binary tree, preorder does not determine the shape - you also need the
inorder (unit 06, *rebuild from preorder + inorder*). For a BST you already have the
inorder for free: it is just the keys **sorted**. So preorder alone pins the tree down.

The easiest way to rebuild it: **insert the keys in preorder order** into an empty BST.
Preorder lists every node before its descendants, so when each key is inserted its
ancestors are already there and the BST rule sends it to exactly its original position.
That is `O(n h)`; there is an `O(n)` version that passes an upper bound down the
recursion, but the insertion one is the one to write under time pressure.

## Height again

Nodes, not edges: a single node has height 1. Check which one a question means.
