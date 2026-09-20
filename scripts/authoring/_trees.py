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


def spaced(t) -> str:
    if t is None:
        return "( )"
    return f"( {t.v} {spaced(t.l)} {spaced(t.r)} )"


def compact(t, bare_leaves=True) -> str:
    if t is None:
        return "()"
    if bare_leaves and t.l is None and t.r is None:
        return f"({t.v})"
    return f"({t.v}{compact(t.l, bare_leaves)}{compact(t.r, bare_leaves)})"


def preorder(t):
    return [] if t is None else [t.v] + preorder(t.l) + preorder(t.r)


def inorder(t):
    return [] if t is None else inorder(t.l) + [t.v] + inorder(t.r)


def postorder(t):
    return [] if t is None else postorder(t.l) + postorder(t.r) + [t.v]


def values(t):
    return preorder(t)
