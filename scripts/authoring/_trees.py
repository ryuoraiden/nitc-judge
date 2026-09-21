"""Random binary trees and the two NITC parenthesized notations.

Spaced (PD Lab 10 Q2):   ( 1 ( 2 ( ) ( ) ) ( ) )     every null child written as ( )
Compact (PD Lab 10 Q3):  (20(11(2)())(8(6)(10)))    a leaf may be written bare as (2)
"""
from __future__ import annotations

import random


class T:
    __slots__ = ("v", "l", "r")

    def __init__(self, v, l=None, r=None):
        self.v, self.l, self.r = v, l, r


def random_tree(rng: random.Random, n: int, values=None, shape="random"):
    """A tree with n distinct values.  shape: random | left | right | full."""
    vals = list(values) if values is not None else rng.sample(range(1, 100), n)
    if n == 0:
        return None
    if shape == "left":
        root = None
        for v in reversed(vals):
            root = T(v, root, None)
        return root
    if shape == "right":
        root = None
        for v in reversed(vals):
            root = T(v, None, root)
        return root
    if shape == "full":
        nodes = [T(v) for v in vals]
        for i, node in enumerate(nodes):
            if 2 * i + 1 < n:
                node.l = nodes[2 * i + 1]
            if 2 * i + 2 < n:
                node.r = nodes[2 * i + 2]
        return nodes[0]

    def build(vs):
        if not vs:
            return None
        k = rng.randint(0, len(vs) - 1)
        return T(vs[0], build(vs[1:k + 1]), build(vs[k + 1:]))
    return build(vals)


# Both serialisers are iterative: test trees near the sheets' size limits are
# thousands of levels deep, far past Python's recursion limit.

def _serialise(t, empty, leaf, open_, sep, close):
    out, stack = [], [t]
    while stack:
        x = stack.pop()
        if isinstance(x, str):
            out.append(x)
        elif x is None:
            out.append(empty)
        elif leaf is not None and x.l is None and x.r is None:
            out.append(leaf.format(x.v))
        else:
            # pushed in reverse: "(v" left sep right close
            stack += [close, x.r, sep, x.l, sep, open_.format(x.v)]
    return "".join(out)


def spaced(t) -> str:
    return _serialise(t, "( )", None, "( {}", " ", " )")


def compact(t, bare_leaves=True) -> str:
    return _serialise(t, "()", "({})" if bare_leaves else None, "({}", "", ")")


def preorder(t):
    return [] if t is None else [t.v] + preorder(t.l) + preorder(t.r)


def inorder(t):
    return [] if t is None else inorder(t.l) + [t.v] + inorder(t.r)


def postorder(t):
    return [] if t is None else postorder(t.l) + postorder(t.r) + [t.v]


def values(t):
    return preorder(t)
