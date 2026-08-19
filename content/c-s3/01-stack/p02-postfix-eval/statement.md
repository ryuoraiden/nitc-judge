# Evaluate a postfix expression

The stack operations are **already written for you** this time (in a file you do
not see). Your job is the one function that uses them: `evalPostfix`.

Each input line is one postfix expression: operands and operators separated by
single spaces. Print the value of each expression on its own line.

## Rules

- Operands are non-negative integers, possibly multi-digit.
- Operators are `+`, `-`, `*`, `/` and are always binary.
- Division is integer division, and never by zero in the tests.
- Every expression is well-formed.

## Example

```
3 4 +
5 1 2 + 4 * + 3 -
```

```
7
14
```

The second one evaluates as `1 + 2 = 3`, then `3 * 4 = 12`, then `5 + 12 = 17`,
then `17 - 3 = 14`.

## The trap

`-` and `/` are not commutative, and the stack hands you the operands in reverse.
For `7 3 -` the first `pop()` gives you `3`, not `7`. Getting this backwards is the
single most common bug in this problem, and it passes the `+` and `*` tests
happily while failing everything else.
