"""Unit 11 - Tree modification questions.  Run: python scripts/authoring/unit_11_tree_variations.py"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report
from _trees import random_tree, spaced, compact, preorder as py_pre

PACK = "c-s3"
UNIT = "11-tree-variations"
rng = random.Random(1111)

write_unit(PACK, UNIT, "Tree modification questions",
           "Your Week 2 delete-by-rank question, then the BST and binary-tree questions "
           "most likely to turn up: LCA, floor/ceil, range, validation, rebuilding from "
           "preorder, balance and diameter, root-to-leaf paths.")

NODE = r"""
#include <stddef.h>   /* NULL */

typedef struct Node {
    int key;
    struct Node *left;
    struct Node *right;
} Node;
"""

PARSER = r"""
#include <ctype.h>
#include <stdlib.h>
#include "problem.h"

Node *newNode(int key) {
    Node *n = malloc(sizeof(Node));
    n->key = key;
    n->left = n->right = NULL;
    return n;
}

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    if (s[*i] != '(') return NULL;
    (*i)++;
    skipSpace(s, i);
    if (s[*i] == ')') { (*i)++; return NULL; }
    int sign = 1, v = 0;
    if (s[*i] == '-') { sign = -1; (*i)++; }
    while (isdigit((unsigned char)s[*i])) v = v * 10 + (s[(*i)++] - '0');
    Node *n = newNode(sign * v);
    n->left = buildTree(s, i);
    n->right = buildTree(s, i);
    skipSpace(s, i);
    if (s[*i] == ')') (*i)++;
    return n;
}

void freeTree(Node *r) {
    if (!r) return;
    freeTree(r->left);
    freeTree(r->right);
    free(r);
}
"""

BST_INSERT = r"""
#include <stdlib.h>
#include "problem.h"

Node *newNode(int key) {
    Node *n = malloc(sizeof(Node));
    n->key = key;
    n->left = n->right = NULL;
    return n;
}

Node *insertKey(Node *root, int key) {
    if (root == NULL) return newNode(key);
    if (key < root->key) root->left = insertKey(root->left, key);
    else if (key > root->key) root->right = insertKey(root->right, key);
    return root;
}
"""

READ_LINE = r"""
static char line[200005];

static Node *readTree(void) {
    if (fgets(line, sizeof line, stdin) == NULL) return NULL;
    int i = 0;
    return buildTree(line, &i);
}
"""


class B:
    """Tiny Python BST for generating inputs whose shape we control."""
    def __init__(self, k):
        self.k, self.l, self.r = k, None, None


def bst_insert(root, k):
    if root is None:
        return B(k)
    if k < root.k:
        root.l = bst_insert(root.l, k)
    elif k > root.k:
        root.r = bst_insert(root.r, k)
    return root


def bst_pre(t):
    return [] if t is None else [t.k] + bst_pre(t.l) + bst_pre(t.r)


# ================================================================= p01 delete by rank
A1 = r"""
#include <stdio.h>
#include <stdlib.h>

typedef struct _BSTNode {
    int key;
    struct _BSTNode *left, *right, *parent;
} BSTNode;
typedef BSTNode *BST;

static BST insert(BST T, int k) {
    BST y = NULL, x = T;
    while (x) { y = x; x = (k < x->key) ? x->left : x->right; }
    BST n = malloc(sizeof(BSTNode));
    n->key = k; n->left = n->right = NULL; n->parent = y;
    if (!y) return n;
    if (k < y->key) y->left = n; else y->right = n;
    return T;
}

static BST minimum(BST T) {
    while (T && T->left) T = T->left;
    return T;
}

/* The k-th node in inorder, or NULL.  *count is shared across the recursion. */
static BST kth(BST T, int k, int *count) {
    if (T == NULL) return NULL;
    BST found = kth(T->left, k, count);
    if (found) return found;
    if (++(*count) == k) return T;
    return kth(T->right, k, count);
}

static BST transplant(BST T, BST u, BST v) {
    if (u->parent == NULL) T = v;
    else if (u == u->parent->left) u->parent->left = v;
    else u->parent->right = v;
    if (v) v->parent = u->parent;
    return T;
}

static BST delete(BST T, BST x) {
    if (x->left == NULL) T = transplant(T, x, x->right);
    else if (x->right == NULL) T = transplant(T, x, x->left);
    else {
        BST y = minimum(x->right);
        if (y->parent != x) {
            T = transplant(T, y, y->right);
            y->right = x->right;
            y->right->parent = y;
        }
        T = transplant(T, x, y);
        y->left = x->left;
        y->left->parent = y;
    }
    free(x);
    return T;
}

static void inorder(BST r)  { if (!r) return; inorder(r->left); printf("%d ", r->key); inorder(r->right); }
static void preorder(BST r) { if (!r) return; printf("%d ", r->key); preorder(r->left); preorder(r->right); }

int main(void) {
    BST T = NULL;
    char c;
    while (scanf(" %c", &c) == 1) {
        if (c == 'e') break;
        if (c == 'i') {
            int k; if (scanf("%d", &k) != 1) break;
            T = insert(T, k);
        } else if (c == 'r') {
            int k, count = 0;
            if (scanf("%d", &k) != 1) break;
            BST x = (k >= 1) ? kth(T, k, &count) : NULL;
            if (x == NULL) { printf("-1\n"); continue; }
            printf("%d\n", x->key);
            T = delete(T, x);
        } else if (c == 'p') {
            if (!T) printf("NULL");
            inorder(T); printf("\n");
        } else if (c == 't') {
            if (!T) printf("NULL");
            preorder(T); printf("\n");
        }
    }
    return 0;
}
"""

S1 = r"""
#include <stdio.h>
#include <stdlib.h>

typedef struct _BSTNode {
    int key;
    struct _BSTNode *left, *right, *parent;
} BSTNode;
typedef BSTNode *BST;

int main(void) {
    /* TODO - it is two things you already have, glued together:
         1. find the k-th smallest node (inorder with a shared counter)
         2. delete THAT NODE with the Week 2 transplant delete
       Print the deleted key, or -1 if the tree has fewer than k nodes. */
    return 0;
}
"""


def rank_script(n_ins, n_ops):
    keys = rng.sample(range(1, 90), n_ins)
    lines = [f"i {k}" for k in keys]
    size = n_ins
    lines.append("t")
    for _ in range(n_ops):
        roll = rng.random()
        if roll < 0.6:
            k = rng.randint(1, size + 1) if rng.random() < 0.9 else rng.choice([0, size + 3])
            lines.append(f"r {k}")
            if 1 <= k <= size:
                size -= 1
        elif roll < 0.8:
            lines.append(rng.choice(["p", "t"]))
        else:
            v = rng.randint(1, 90)
            lines.append(f"i {v}")          # may duplicate; harmless for the tests' shape
            if v not in keys:
                keys.append(v)
                size += 1
            else:
                lines.pop()
    lines += ["p", "t", "e"]
    return "\n".join(lines) + "\n"


T1 = ["i 50\ni 30\ni 70\ni 20\ni 40\ni 60\ni 80\nr 4\np\nt\nr 1\np\nt\nr 5\np\nt\ne\n",
      "r 1\np\ni 5\nr 2\nr 1\np\nt\ne\n",
      "i 15\ni 6\ni 18\ni 3\ni 7\ni 17\ni 20\ni 13\ni 9\nr 2\nt\nr 5\nt\nr 7\nt\np\ne\n",
      "i 1\ni 2\ni 3\ni 4\nr 1\nr 1\nt\nr 2\nt\ne\n"]
T1 += [rank_script(rng.randint(6, 14), rng.randint(4, 8)) for _ in range(6)]

write_problem(
    PACK, UNIT, "p01-delete-by-rank", title="Week 2 modification: delete by rank",
    mode="program", difficulty="hard", estimated_minutes=30, samples=1,
    topics=["bst", "deletion", "order statistics"],
    prereqs=[f"{PACK}.07-bst.p03-delete-transplant", f"{PACK}.07-bst.p04-kth-successor-noparent"],
    source="Reconstruction of the DSA Lab Week 2 modification question",
    hints=[
        "Split it: kth(T, k, &count) returns the NODE of rank k, then the ordinary "
        "delete(T, x) removes it. Neither part is new.",
        "Return the node pointer from the inorder search, not the key - the Week 2 "
        "delete takes a node, and searching for the key again wastes the work.",
        "Delete the node before the next command, and remember ranks shift: after "
        "removing rank 1, the old rank 2 becomes rank 1.",
    ],
    starter=S1, solution=A1, tests=T1,
    statement=r"""
# Week 2 modification: delete by rank

**This is a reconstruction** of your Week 2 modification question. The exact I/O is
lost; the task - delete the node by its *rank* rather than its key - is what matters.

> Using the Week 2 BST ADT (nodes with a parent pointer), support deleting the node of
> **rank `k`**, i.e. the `k`-th smallest key.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i x` | insert `x` | nothing |
| `r k` | delete the `k`-th smallest node | its key, or `-1` if there is no rank `k` |
| `p` | inorder | keys, or `NULL` |
| `t` | preorder | keys, or `NULL` |
| `e` | exit | nothing |

Deletion is the standard two-children-means-successor delete, so the **preorder** after
a deletion is fixed.

## Sample

```
i 50
i 30
i 70
i 20
i 40
i 60
i 80
r 4
p
t
r 1
p
t
r 5
p
t
e
```

```
50
20 30 40 60 70 80
60 30 20 40 70 80
20
30 40 60 70 80
60 30 40 70 80
80
30 40 60 70
60 30 40 70
```

Rank 4 of seven keys is the root, 50; its successor 60 takes its place.

## The twist is composition

"Delete by rank" is two things you already have: the inorder-counter search from
`kthSmallest`, and the transplant delete. The only glue is making the search return
the **node** (so `delete` can take it directly) instead of printing its key.

## If they ask for it in O(h)

Counting through inorder is `O(n)`. The textbook way to do it in `O(h)` is an
**order-statistic tree**: every node also stores `size`, the number of nodes in its
subtree. Then rank `k` is found by comparing `k` with `size(left) + 1` at each node and
going left or right - like binary search. The price is updating `size` on every
insert and delete. If a question insists on `O(h)` for rank queries, that is what it
wants.
""",
)

# ================================================================= p02 BST queries
H2 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + r"""
/* ---- Provided. ---- */
Node *newNode(int key);
Node *insertKey(Node *root, int key);

/* ---- Yours.  All O(h): each walks ONE root-to-leaf path. ---- */
int  lcaBST(Node *root, int a, int b);    /* both keys are present */
int  floorKey(Node *root, int x);         /* largest key <= x, or -1 */
int  ceilKey(Node *root, int x);          /* smallest key >= x, or -1 */
void printRange(Node *root, int lo, int hi);  /* keys in [lo, hi] ascending, each + ' ' */

#endif
"""

M2 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    Node *root = NULL;
    char c;
    while (scanf(" %c", &c) == 1) {
        if (c == 'e') break;
        int a, b;
        if (c == 'i') { if (scanf("%d", &a) != 1) break; root = insertKey(root, a); }
        else if (c == 'l') { if (scanf("%d %d", &a, &b) != 2) break; printf("%d\n", lcaBST(root, a, b)); }
        else if (c == 'f') { if (scanf("%d", &a) != 1) break; printf("%d\n", floorKey(root, a)); }
        else if (c == 'c') { if (scanf("%d", &a) != 1) break; printf("%d\n", ceilKey(root, a)); }
        else if (c == 'r') { if (scanf("%d %d", &a, &b) != 2) break; printRange(root, a, b); printf("\n"); }
    }
    return 0;
}
"""

S2 = r"""
#include <stdio.h>
#include "problem.h"

int lcaBST(Node *root, int a, int b) {
    /* TODO: both smaller than root -> go left; both larger -> go right;
       otherwise they split here (or one of them IS here): root is the LCA. */
    return -1;
}

int floorKey(Node *root, int x) {
    /* TODO: walk down. Equal -> done. Root bigger than x -> go left.
       Root smaller -> it is a candidate; remember it and go right. */
    return -1;
}

int ceilKey(Node *root, int x) {
    return -1;   /* TODO: mirror of floor */
}

void printRange(Node *root, int lo, int hi) {
    /* TODO: inorder, but skip subtrees that cannot contain anything in range:
       only go left if root->key > lo, only go right if root->key < hi. */
}
"""

A2 = r"""
#include <stdio.h>
#include "problem.h"

int lcaBST(Node *root, int a, int b) {
    while (root != NULL) {
        if (a < root->key && b < root->key) root = root->left;
        else if (a > root->key && b > root->key) root = root->right;
        else return root->key;            /* they split here */
    }
    return -1;
}

int floorKey(Node *root, int x) {
    int best = -1;
    while (root != NULL) {
        if (root->key == x) return x;
        if (root->key > x) root = root->left;
        else { best = root->key; root = root->right; }   /* candidate, look for bigger */
    }
    return best;
}

int ceilKey(Node *root, int x) {
    int best = -1;
    while (root != NULL) {
        if (root->key == x) return x;
        if (root->key < x) root = root->right;
        else { best = root->key; root = root->left; }
    }
    return best;
}

void printRange(Node *root, int lo, int hi) {
    if (root == NULL) return;
    if (root->key > lo) printRange(root->left, lo, hi);     /* smaller keys may qualify */
    if (root->key >= lo && root->key <= hi) printf("%d ", root->key);
    if (root->key < hi) printRange(root->right, lo, hi);    /* larger keys may qualify */
}
"""


def query_script(n):
    keys = rng.sample(range(1, 100), n)
    lines = [f"i {k}" for k in keys]
    for _ in range(8):
        q = rng.choice("lfcr")
        if q == "l":
            a, b = rng.choice(keys), rng.choice(keys)
            lines.append(f"l {a} {b}")
        elif q in "fc":
            lines.append(f"{q} {rng.randint(0, 101)}")
        else:
            lo = rng.randint(0, 90)
            lines.append(f"r {lo} {lo + rng.randint(0, 40)}")
    lines.append("e")
    return "\n".join(lines) + "\n"


T2 = ["i 20\ni 8\ni 22\ni 4\ni 12\ni 10\ni 14\nl 10 14\nl 14 8\nl 10 22\nf 13\nc 13\nf 3\nc 23\nr 9 15\ne\n",
      "l 1 1\nf 5\nc 5\nr 1 10\ne\n".replace("l 1 1\n", ""),
      "i 5\nl 5 5\nf 5\nc 5\nf 4\nc 6\nr 5 5\nr 6 9\ne\n"]
T2 += [query_script(rng.randint(6, 15)) for _ in range(6)]

write_problem(
    PACK, UNIT, "p02-bst-queries", title="BST queries: LCA, floor, ceil, range",
    mode="function", difficulty="medium", estimated_minutes=18, samples=1, allow_empty=False,
    topics=["bst", "lca", "floor", "ceil", "range query"],
    prereqs=[f"{PACK}.07-bst.p04-kth-successor-noparent"],
    source="Standard BST questions (the ordering lets each walk ONE path)",
    hints=[
        "LCA in a BST needs no recursion into both sides: while a and b are both on "
        "the same side of root, move to that side. The first node where they split "
        "is the LCA.",
        "floor: every time you step RIGHT, the node you leave is <= x - a candidate. "
        "Remember the latest candidate; it is the answer when you fall off the tree.",
        "printRange prunes: only descend left when root->key > lo, and right when "
        "root->key < hi. Without pruning it is still correct, just O(n).",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"bst.c": BST_INSERT},
    statement=r"""
# BST queries: LCA, floor, ceil, range

Four short questions that use the BST ordering to avoid searching the whole tree. The
first three walk **one root-to-leaf path**, `O(h)`. Range reporting cannot - every key in
range has to be printed - but it skips every subtree that lies entirely outside the
range, so it costs `O(h + k)` for `k` reported keys.

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
""",
)

# ================================================================= p03 validate BST
H3 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + r"""
/* ---- Provided. ---- */
Node *newNode(int key);
Node *buildTree(const char *s, int *i);
void  freeTree(Node *root);

/* ---- Yours: 1 if this binary tree is a valid BST (strict: no duplicates), else 0. ---- */
int isBST(Node *root);

#endif
"""

M3 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_LINE + r"""
int main(void) {
    int q;
    if (scanf("%d", &q) != 1) return 0;
    int ch;
    while ((ch = getchar()) != '\n' && ch != EOF) { }
    while (q--) {
        Node *root = readTree();
        printf("%s\n", isBST(root) ? "YES" : "NO");
        freeTree(root);
    }
    return 0;
}
"""

S3 = r"""
#include <limits.h>
#include "problem.h"

int isBST(Node *root) {
    /* TODO
       Checking only root->left->key < root->key < root->right->key at every node
       is NOT enough (see the statement). Pass down the allowed range instead:
           static int check(Node *r, long long lo, long long hi)
       every key must satisfy lo < key < hi; going left tightens hi to the
       parent's key, going right tightens lo. */
    return 0;
}
"""

A3 = r"""
#include <limits.h>
#include "problem.h"

static int check(Node *r, long long lo, long long hi) {
    if (r == NULL) return 1;
    if (r->key <= lo || r->key >= hi) return 0;
    return check(r->left, lo, r->key) && check(r->right, r->key, hi);
}

int isBST(Node *root) {
    return check(root, (long long)INT_MIN - 1, (long long)INT_MAX + 1);
}
"""


def bst_to_T(b):
    from _trees import T
    return None if b is None else T(b.k, bst_to_T(b.l), bst_to_T(b.r))


def mutate(t):
    """Swap one pair of values in a valid BST, usually making it invalid."""
    from _trees import T  # noqa: F401
    nodes = []
    stack = [t]
    while stack:
        x = stack.pop()
        if x:
            nodes.append(x)
            stack += [x.l, x.r]
    if len(nodes) >= 2:
        a, b = rng.sample(nodes, 2)
        a.v, b.v = b.v, a.v
    return t


cases = ["( 10 ( 5 ( ) ( ) ) ( 15 ( 12 ( ) ( ) ) ( 20 ( ) ( ) ) ) )",
         "( 10 ( 5 ( ) ( ) ) ( 15 ( 6 ( ) ( ) ) ( 20 ( ) ( ) ) ) )",
         "( 10 ( 5 ( ) ( 11 ( ) ( ) ) ) ( 15 ( ) ( ) ) )",
         "( 7 ( ) ( ) )",
         "( 5 ( 5 ( ) ( ) ) ( ) )",
         "(2(1)(3))", "(2(3)(1))"]
T3 = [f"{len(cases)}\n" + "\n".join(cases) + "\n"]
for _ in range(4):
    lines = []
    for _ in range(6):
        root = None
        for k in rng.sample(range(1, 200), rng.randint(3, 15)):
            root = bst_insert(root, k)
        t = bst_to_T(root)
        if rng.random() < 0.55:
            t = mutate(t)
        lines.append(spaced(t) if rng.random() < 0.5 else compact(t))
    T3.append(f"{len(lines)}\n" + "\n".join(lines) + "\n")

write_problem(
    PACK, UNIT, "p03-validate-bst", title="Is this binary tree a BST?",
    mode="function", difficulty="medium", estimated_minutes=12, samples=1,
    topics=["bst", "validation", "recursion"],
    prereqs=[f"{PACK}.06-binary-tree.p02-parse-notation"],
    source="Classic BST question; uses the PD Lab 10 tree notation",
    hints=[
        "The trap: 'left child < node < right child' at every node is not enough. "
        "A key deep in the left subtree must also be smaller than every ANCESTOR it "
        "is left of.",
        "Pass an allowed open interval (lo, hi) down the recursion. Left child gets "
        "(lo, node->key); right child gets (node->key, hi).",
        "Use long long bounds starting outside the int range so that keys equal to "
        "INT_MIN or INT_MAX are not rejected by the sentinels.",
    ],
    header=H3, harness=M3, starter=S3, solution=A3, tests=T3,
    extra={"parse.c": PARSER.replace("int key)", "int key)")},
    statement=r"""
# Is this binary tree a BST?

```c
int isBST(Node *root);   /* 1 or 0; duplicates are not allowed */
```

## Input

The number of trees `q`, then `q` lines, each a tree in either parenthesized
notation. Print `YES` or `NO` for each.

## Example

```
7
( 10 ( 5 ( ) ( ) ) ( 15 ( 12 ( ) ( ) ) ( 20 ( ) ( ) ) ) )
( 10 ( 5 ( ) ( ) ) ( 15 ( 6 ( ) ( ) ) ( 20 ( ) ( ) ) ) )
( 10 ( 5 ( ) ( 11 ( ) ( ) ) ) ( 15 ( ) ( ) ) )
( 7 ( ) ( ) )
( 5 ( 5 ( ) ( ) ) ( ) )
(2(1)(3))
(2(3)(1))
```

```
YES
NO
NO
YES
NO
YES
NO
```

## The trap in tree 2

```
      10
     /  \
    5    15
        /  \
       6    20
```

Check each node against its own children only: `5 < 10 < 15` fine, `6 < 15 < 20` fine.
Looks valid - but 6 sits in 10's **right** subtree and is smaller than 10. The local
check misses it.

## The fix: pass the allowed range down

Every node lives inside an interval set by its ancestors. The root may be anything;
going left, the upper bound becomes the parent's key; going right, the lower bound
does:

```c
static int check(Node *r, long long lo, long long hi) {
    if (r == NULL) return 1;
    if (r->key <= lo || r->key >= hi) return 0;
    return check(r->left, lo, r->key) && check(r->right, r->key, hi);
}
```

The equivalent alternative: do an inorder traversal and check the sequence is
**strictly increasing**. Same answer, and a good one to mention in a viva.
""",
)

# ================================================================= p04 BST from preorder
A4 = r"""
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    struct Node *left, *right;
} Node;

static Node *insertKey(Node *r, int k) {
    if (r == NULL) {
        r = malloc(sizeof(Node));
        r->key = k; r->left = r->right = NULL;
        return r;
    }
    if (k < r->key) r->left = insertKey(r->left, k);
    else r->right = insertKey(r->right, k);
    return r;
}

static void postorder(Node *r) { if (!r) return; postorder(r->left); postorder(r->right); printf("%d ", r->key); }

static int height(Node *r) {
    if (!r) return 0;
    int a = height(r->left), b = height(r->right);
    return 1 + (a > b ? a : b);
}

static Node *q[100005];

static void levelOrder(Node *root) {
    int h = 0, t = 0;
    if (root) q[t++] = root;
    while (h < t) {
        Node *c = q[h++];
        printf("%d ", c->key);
        if (c->left) q[t++] = c->left;
        if (c->right) q[t++] = c->right;
    }
    printf("\n");
}

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    Node *root = NULL;
    for (int i = 0; i < n; i++) {
        int k;
        if (scanf("%d", &k) != 1) break;
        root = insertKey(root, k);   /* inserting a preorder in order rebuilds the tree */
    }
    postorder(root); printf("\n");
    levelOrder(root);
    printf("%d\n", height(root));
    return 0;
}
"""

S4 = r"""
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    struct Node *left, *right;
} Node;

int main(void) {
    /* TODO
       Read n and the preorder sequence of a BST.
       Rebuild the tree, then print its postorder, its level order, and its
       height (in nodes), one per line. */
    return 0;
}
"""

T4 = ["7\n50 30 20 40 70 60 80\n", "5\n1 2 3 4 5\n", "5\n5 4 3 2 1\n", "1\n42\n",
      "9\n15 6 3 7 13 9 18 17 20\n"]
for _ in range(5):
    root = None
    for k in rng.sample(range(1, 500), rng.randint(6, 25)):
        root = bst_insert(root, k)
    pre = bst_pre(root)
    T4.append(f"{len(pre)}\n{' '.join(map(str, pre))}\n")

write_problem(
    PACK, UNIT, "p04-bst-from-preorder", title="Rebuild a BST from its preorder",
    mode="program", difficulty="medium", estimated_minutes=15, samples=1,
    topics=["bst", "traversal"],
    prereqs=[f"{PACK}.07-bst.p01-insert-search"],
    source="Classic BST reconstruction question",
    hints=[
        "For a BST, preorder alone determines the tree - unlike a general binary "
        "tree, which also needs the inorder.",
        "The simplest correct rebuild: insert the preorder keys one by one into an "
        "empty BST. Every parent is inserted before its children, so each key lands "
        "exactly where it was.",
        "Level order needs a queue of Node* - the unit 06 level-order code, printed "
        "on one line this time.",
    ],
    starter=S4, solution=A4, tests=T4,
    statement=r"""
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
""",
)

# ================================================================= p05 balance / diameter / mirror
H5 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + r"""
/* ---- Provided. ---- */
Node *newNode(int key);
Node *buildTree(const char *s, int *i);
void  freeTree(Node *root);

/* ---- Yours. ---- */
int  isBalanced(Node *root);   /* 1 if at EVERY node the subtree heights differ by <= 1 */
int  diameter(Node *root);     /* edges on the longest path between any two nodes; 0 if <= 1 node */
void mirror(Node *root);       /* swap left and right at every node, in place */

#endif
"""

M5 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_LINE + r"""
static void pre(Node *r) { if (!r) return; printf("%d ", r->key); pre(r->left); pre(r->right); }

int main(void) {
    Node *root = readTree();
    printf("%d\n", isBalanced(root));
    printf("%d\n", diameter(root));
    mirror(root);
    pre(root);
    printf("\n");
    freeTree(root);
    return 0;
}
"""

S5 = r"""
#include "problem.h"

int isBalanced(Node *root) {
    /* TODO: calling height() at every node is O(n^2). Better: one helper that
       returns the height, or -1 as soon as it finds an unbalanced subtree. */
    return 0;
}

int diameter(Node *root) {
    /* TODO: the longest path bends at some node, going down its left side and
       its right side. At every node, left height + right height is a candidate.
       Compute heights bottom-up and keep the best candidate in a variable passed
       by pointer. */
    return 0;
}

void mirror(Node *root) {
    /* TODO: swap the two children, then mirror both subtrees. */
}
"""

A5 = r"""
#include "problem.h"

/* Height in nodes, or -1 if any subtree below is unbalanced. */
static int checkedHeight(Node *r) {
    if (r == NULL) return 0;
    int l = checkedHeight(r->left);
    if (l < 0) return -1;
    int h = checkedHeight(r->right);
    if (h < 0) return -1;
    if (l - h > 1 || h - l > 1) return -1;
    return 1 + (l > h ? l : h);
}

int isBalanced(Node *root) {
    return checkedHeight(root) >= 0;
}

/* Height in nodes; updates *best with the widest bend seen, in edges. */
static int heightAndDiameter(Node *r, int *best) {
    if (r == NULL) return 0;
    int l = heightAndDiameter(r->left, best);
    int h = heightAndDiameter(r->right, best);
    if (l + h > *best) *best = l + h;        /* path bending at r, measured in edges */
    return 1 + (l > h ? l : h);
}

int diameter(Node *root) {
    int best = 0;
    heightAndDiameter(root, &best);
    return best;
}

void mirror(Node *root) {
    if (root == NULL) return;
    Node *t = root->left;
    root->left = root->right;
    root->right = t;
    mirror(root->left);
    mirror(root->right);
}
"""

T5 = ["( 1 ( 2 ( 4 ( ) ( ) ) ( 5 ( ) ( ) ) ) ( 3 ( ) ( ) ) )\n",
      "(1(2(3(4))))\n",
      "(7)\n",
      "(1(2(4(8)(9))(5()(10(11))))(3))\n",
      "(1(2)(3(4)(5(6)(7))))\n"]
for k in range(6):
    T5.append(spaced(random_tree(rng, rng.randint(3, 20),
                                 shape=["random", "random", "full", "left"][k % 4])) + "\n")

write_problem(
    PACK, UNIT, "p05-balanced-diameter-mirror", title="Balanced? Diameter? Mirror it.",
    mode="function", difficulty="medium", estimated_minutes=20, samples=1,
    topics=["binary tree", "recursion", "height"],
    prereqs=[f"{PACK}.06-binary-tree.p03-height-size-leaves"],
    source="The three most common binary-tree recursion questions",
    hints=[
        "Both isBalanced and diameter are height() with extra work at each node. "
        "Compute the two child heights once and use them twice.",
        "isBalanced: return -1 from the height helper the moment any subtree is "
        "unbalanced, and propagate it. That keeps it O(n).",
        "diameter: the longest path bends at some node. At each node, "
        "leftHeight + rightHeight is the length in edges of the best path bending "
        "there; keep the maximum in an int passed by pointer.",
    ],
    header=H5, harness=M5, starter=S5, solution=A5, tests=T5,
    extra={"parse.c": PARSER},
    statement=r"""
# Balanced? Diameter? Mirror it.

Three recursion questions that come up constantly. The hidden `main()` prints
`isBalanced`, then `diameter`, then the **preorder of the tree after `mirror`**.

```c
int  isBalanced(Node *root);  /* at every node, child heights differ by <= 1 */
int  diameter(Node *root);    /* longest path between any two nodes, in EDGES */
void mirror(Node *root);      /* swap children everywhere, in place */
```

The tree is one line in either parenthesized notation.

## Example

```
( 1 ( 2 ( 4 ( ) ( ) ) ( 5 ( ) ( ) ) ) ( 3 ( ) ( ) ) )
```

```
1
3
1 3 2 5 4
```

The longest path is `4 - 2 - 1 - 3`: three edges.

## One pass, not two

The obvious `isBalanced` calls `height()` on both children at every node - `O(n^2)` on
a skewed tree. The better one computes heights bottom-up and returns a sentinel `-1` as
soon as some subtree is unbalanced:

```c
int l = checkedHeight(r->left);  if (l < 0) return -1;
int h = checkedHeight(r->right); if (h < 0) return -1;
if (abs(l - h) > 1) return -1;
return 1 + max(l, h);
```

## Diameter bends somewhere

Any longest path has a highest node where it turns. There it goes down as deep as
possible on the left and on the right, so its length in edges is
`height(left) + height(right)` (heights in nodes). Evaluate that at every node while
computing heights, and keep the maximum. The longest path **does not have to pass
through the root** - test 4 is built so that it doesn't.

## Mirror

Swap, then recurse into both sides. Four lines; the preorder of a mirrored tree is the
original's "root, right, left" order.
""",
)

# ================================================================= p06 root-to-leaf paths
H6 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + r"""
#define MAXDEPTH 100005

/* ---- Provided. ---- */
Node *newNode(int key);
Node *buildTree(const char *s, int *i);
void  freeTree(Node *root);

/* ---- Yours: print every root-to-leaf path on its own line, left to right,
        keys joined by "->".  Then print how many of those paths have a key sum
        equal to target. ---- */
void rootToLeaf(Node *root, int target);

#endif
"""

M6 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_LINE + r"""
int main(void) {
    Node *root = readTree();
    int target;
    if (scanf("%d", &target) != 1) target = 0;
    rootToLeaf(root, target);
    freeTree(root);
    return 0;
}
"""

S6 = r"""
#include <stdio.h>
#include "problem.h"

static int path[MAXDEPTH];

void rootToLeaf(Node *root, int target) {
    /* TODO
       A recursive helper that carries the path so far:
           static void walk(Node *r, int depth, int sum, int target, int *count)
         - write r->key into path[depth]
         - at a LEAF (both children NULL): print path[0..depth] joined by "->",
           and count it if sum == target
         - otherwise recurse into the children with depth + 1
       You never need to "remove" a key when backtracking: the next call simply
       overwrites path[depth]. */
    (void)path;
}
"""

A6 = r"""
#include <stdio.h>
#include "problem.h"

static int path[MAXDEPTH];

static void walk(Node *r, int depth, int sum, int target, int *count) {
    if (r == NULL) return;
    path[depth] = r->key;                /* overwritten on backtrack: no pop needed */
    sum += r->key;

    if (r->left == NULL && r->right == NULL) {
        for (int i = 0; i <= depth; i++) printf(i ? "->%d" : "%d", path[i]);
        printf("\n");
        if (sum == target) (*count)++;
        return;
    }
    walk(r->left, depth + 1, sum, target, count);
    walk(r->right, depth + 1, sum, target, count);
}

void rootToLeaf(Node *root, int target) {
    int count = 0;
    walk(root, 0, 0, target, &count);
    printf("%d\n", count);
}
"""

T6 = ["( 5 ( 4 ( 11 ( 7 ( ) ( ) ) ( 2 ( ) ( ) ) ) ( ) ) ( 8 ( 13 ( ) ( ) ) ( 4 ( ) ( 1 ( ) ( ) ) ) ) )\n22\n",
      "(1)\n1\n", "(1(2)(3))\n5\n", "(10(20(40)(50))(30()(60)))\n90\n"]
for _ in range(5):
    t = random_tree(rng, rng.randint(4, 15))
    T6.append(spaced(t) + f"\n{rng.randint(20, 150)}\n")

write_problem(
    PACK, UNIT, "p06-root-to-leaf-paths", title="Root-to-leaf paths and path sums",
    mode="function", difficulty="medium", estimated_minutes=15, samples=1,
    topics=["binary tree", "recursion", "backtracking"],
    prereqs=[f"{PACK}.06-binary-tree.p01-traversals"],
    source="Common binary-tree question",
    hints=[
        "Carry the depth down the recursion and store the key at path[depth]. When "
        "the call returns, the next sibling call overwrites that slot - so no "
        "explicit 'undo' is needed.",
        "A leaf is a node with BOTH children NULL. Checking only 'root == NULL' "
        "prints every path twice (once per missing child).",
        "Carry the running sum as a plain int parameter; each call gets its own "
        "copy, which is exactly the backtracking you want.",
    ],
    header=H6, harness=M6, starter=S6, solution=A6, tests=T6,
    extra={"parse.c": PARSER},
    statement=r"""
# Root-to-leaf paths and path sums

```c
void rootToLeaf(Node *root, int target);
```

Print every root-to-leaf path, left to right, keys joined by `->`. Then print how many of
those paths have keys summing to `target`.

## Input

The tree on one line, then `target`.

## Example

```
( 5 ( 4 ( 11 ( 7 ( ) ( ) ) ( 2 ( ) ( ) ) ) ( ) ) ( 8 ( 13 ( ) ( ) ) ( 4 ( ) ( 1 ( ) ( ) ) ) ) )
22
```

```
5->4->11->7
5->4->11->2
5->8->13
5->8->4->1
1
```

Only `5 + 4 + 11 + 2 = 22`.

## Backtracking without undoing

Keep the current path in an array indexed by depth. A call at depth `d` writes its key
into `path[d]`; when it returns and the sibling call runs at the same depth, it simply
**overwrites** `path[d]`. Nothing ever has to be popped. The running sum works the same
way when passed as a parameter: each call has its own copy.

## What counts as a leaf

Both children `NULL`. If you print when you reach a `NULL` child instead, a node with
two empty children prints its path twice, and a node with one child prints a path that
does not end at a leaf.
""",
)

report(UNIT, 6)
