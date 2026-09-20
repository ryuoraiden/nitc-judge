# PD Lab 10 Q3: build and print postorder

Verbatim from PD Lab 10. The first five tests are the five official samples from the
assignment sheet.

> Given a parenthesis representation of a binary tree, write a C program to construct
> the binary tree and print its postorder traversal.
>
> Each node is represented as `(V(LeftSubtree)(RightSubtree))`. If a node has no left
> and right children, it is represented as `V()()`. The input is guaranteed to be a
> valid binary tree representation.

## Input

A single string `S` with no spaces. `1 <= V <= 10^5`, `|S| <= 10^5`.

## Output

The postorder traversal on one line, space separated.

## Samples

```
(20(11(2)())(8(6)(10)))
```
```
2 11 6 10 8 20
```

```
(12()(2()(13()(4()(5)))))
```
```
5 4 13 2 12
```

Note that the samples write leaves both ways - `(2)` and `(5)` bare, but the statement
says `V()()`. A parser built on "return NULL without consuming if the next character is
not `(`" handles both without caring which one it gets.
