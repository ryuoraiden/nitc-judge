# Parse the parenthesized notation

Every PD Lab 10 tree question hands you the tree as a string. If the parser is wrong,
nothing after it can be right, so it gets its own rung.

```c
Node *buildTree(const char *s, int *i);
```

`*i` is your position in the string. Parse one subtree starting there, leave `*i`
just past it, and return its root.

## Both notations must work

```
( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )      spaces, every empty child written
(20(11(2)())(8(6)(10)))                          no spaces, bare leaves like (2)
(12()(2()(13()(4()(5)))))                         right-skewed
```

`( )` and `()` both mean an empty child. `(2)` is a leaf whose two children are simply
not written.

## Output

The hidden `main()` prints your tree's preorder and inorder on two lines - together
those pin down the exact shape you built - or `EMPTY` if you return `NULL`.

## The rule that makes it easy

Write the function so that **if the next non-space character is not `(`, it returns
`NULL` and consumes nothing**. Then a node is simply:

```
'('  number  buildTree  buildTree  ')'
```

and a missing child makes the recursive call see `)` instead of `(`, return `NULL`
harmlessly, and leave the `)` for the parent to consume. Bare leaves and explicit
empty children fall out of the same code with no special cases.

## Why `int *i` and not `int i`

The position has to survive across recursive calls: when the left subtree's call
returns, the right subtree must start where the left one finished. A plain `int` would
be a copy, and every call would restart from the same place.
