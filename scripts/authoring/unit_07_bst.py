"""Unit 07 - Binary search trees.  Run: python scripts/authoring/unit_07_bst.py"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report

PACK = "c-s3"
UNIT = "07-bst"
rng = random.Random(707)

write_unit(PACK, UNIT, "Binary search trees",
           "The DSA Lab Week 2 ADT (with parent pointers) one function at a time, then "
           "the PD Lab 12 programs (Q1, Q2, Q4) with their official samples. Deletion is "
           "the one to drill.")

# ----------------------------------------------------------------- helpers

def ops_script(n_ins=10, n_ops=8, cmds=("s", "d", "p"), vmax=60, delete_absent=True):
    """A random menu script. Values are drawn from a small range so that searches
    and deletes hit as often as they miss."""
    lines, live = [], []
    for _ in range(n_ins):
        v = rng.randint(1, vmax)
        if v not in live:
            live.append(v)
        lines.append(f"i {v}")
        if rng.random() < 0.3:
            lines.append(rng.choice([c for c in cmds if c in ("p", "t", "b")] or ["p"]))
    for _ in range(n_ops):
        c = rng.choice(cmds)
        if c in ("s", "d", "n", "r"):
            hit = live and rng.random() < 0.7
            v = rng.choice(live) if hit else rng.randint(1, vmax)
            if c == "d" and v in live and (delete_absent or True):
                live.remove(v)
            lines.append(f"{c} {v}")
        elif c == "k":
            lines.append(f"k {rng.randint(1, max(1, len(live)))}")
        else:
            lines.append(c)
    lines.append("e")
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------- p01
H1 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
#include <stddef.h>   /* NULL */

typedef struct Node {
    int key;
    struct Node *left;
    struct Node *right;
} Node;

/* ---- Yours. ---- */
Node *insertKey(Node *root, int key);   /* returns the (possibly new) root */
Node *searchKey(Node *root, int key);   /* NULL if absent */

#endif
"""

M1 = r"""
#include <stdio.h>
#include "problem.h"

static void inorder(Node *r) { if (!r) return; inorder(r->left); printf("%d ", r->key); inorder(r->right); }
static void preorder(Node *r) { if (!r) return; printf("%d ", r->key); preorder(r->left); preorder(r->right); }

int main(void) {
    Node *root = NULL;
    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'i') {
            int v; if (scanf("%d", &v) != 1) break;
            root = insertKey(root, v);
        } else if (cmd == 's') {
            int v; if (scanf("%d", &v) != 1) break;
            printf(searchKey(root, v) ? "PRESENT\n" : "NOT PRESENT\n");
        } else if (cmd == 'p') {
            if (root == NULL) printf("NULL");
            inorder(root); printf("\n");
        } else if (cmd == 't') {
            if (root == NULL) printf("NULL");
            preorder(root); printf("\n");
        }
    }
    return 0;
}
"""

S1 = r"""
#include <stdlib.h>
#include "problem.h"

Node *insertKey(Node *root, int key) {
    /* TODO
       - empty tree: malloc a node, set key, left = right = NULL, return it
       - key < root->key : root->left  = insertKey(root->left, key)
       - key > root->key : root->right = insertKey(root->right, key)
       - equal: the tests never insert a duplicate; just return root
       Always return root at the end - that is what re-links the parent. */
    return root;
}

Node *searchKey(Node *root, int key) {
    /* TODO: NULL or a match ends it; otherwise go left or right. O(h), never both. */
    return NULL;
}
"""

A1 = r"""
#include <stdlib.h>
#include "problem.h"

Node *insertKey(Node *root, int key) {
    if (root == NULL) {
        Node *n = malloc(sizeof(Node));
        n->key = key;
        n->left = n->right = NULL;
        return n;
    }
    if (key < root->key) root->left = insertKey(root->left, key);
    else if (key > root->key) root->right = insertKey(root->right, key);
    return root;
}

Node *searchKey(Node *root, int key) {
    if (root == NULL || root->key == key) return root;
    return key < root->key ? searchKey(root->left, key) : searchKey(root->right, key);
}
"""

T1 = ["i 5\ni 3\ni 10\ni 15\np\nt\ns 10\ns 7\ne\n",
      "p\ns 1\ni 42\np\nt\ns 42\ne\n",
      "i 50\ni 30\ni 70\ni 20\ni 40\ni 60\ni 80\np\nt\ns 60\ns 55\ne\n",
      "i 1\ni 2\ni 3\ni 4\ni 5\np\nt\ne\n",
      "i 5\ni 4\ni 3\ni 2\ni 1\np\nt\ne\n"]
T1 += [ops_script(10, 6, cmds=("s", "p", "t")) for _ in range(3)]

write_problem(
    PACK, UNIT, "p01-insert-search", title="BST insert and search",
    mode="function", difficulty="easy", estimated_minutes=8, samples=2,
    topics=["bst", "recursion"],
    source="DSA Lab Week 2 ADT: insert(T,k) and search(T,k)",
    hints=[
        "Both functions are the same shape: compare with root->key and go into ONE "
        "subtree. Searching both sides means you have written a binary-tree search, "
        "not a BST search.",
        "insertKey returns the root so the caller can reattach it: "
        "root->left = insertKey(root->left, key). Forgetting the assignment builds "
        "a tree that silently loses every node.",
        "The empty-tree case is where the new node is actually created - that is the "
        "base case of the recursion, not a special case before it.",
    ],
    header=H1, harness=M1, starter=S1, solution=A1, tests=T1,
    statement=r"""
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
""",
)

# ----------------------------------------------------------------- p02
BST_PARENT_H = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
#include <stddef.h>   /* NULL */

/* The exact node from the Week 2 assignment sheet. */
typedef struct _BSTNode {
    int key;
    struct _BSTNode *left;
    struct _BSTNode *right;
    struct _BSTNode *parent;
} BSTNode;

typedef BSTNode *BST;
"""

M2 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    BST T = NULL;
    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'i') {
            int v; if (scanf("%d", &v) != 1) break;
            T = insert(T, v);
        } else if (cmd == 'm') {
            BST r = minimum(T);
            printf(r ? "%d\n" : "-1\n", r ? r->key : 0);
        } else if (cmd == 'x') {
            BST r = maximum(T);
            printf(r ? "%d\n" : "-1\n", r ? r->key : 0);
        } else if (cmd == 'n' || cmd == 'r') {
            int v; if (scanf("%d", &v) != 1) break;
            BST x = search(T, v);
            BST r = (x == NULL) ? NULL : (cmd == 'n' ? successor(T, x) : predecessor(T, x));
            printf(r ? "%d\n" : "-1\n", r ? r->key : 0);
        }
    }
    return 0;
}
"""

PARENT_OPS = r"""
#include <stdlib.h>
#include "problem.h"

BST init(int key) {
    BST n = malloc(sizeof(BSTNode));
    n->key = key;
    n->left = n->right = n->parent = NULL;
    return n;
}

BST insert(BST T, int k) {
    BST y = NULL, x = T;
    while (x != NULL) {                 /* walk down, remembering the parent */
        y = x;
        x = (k < x->key) ? x->left : x->right;
    }
    BST n = init(k);
    n->parent = y;
    if (y == NULL) return n;            /* tree was empty */
    if (k < y->key) y->left = n; else y->right = n;
    return T;
}

BST search(BST T, int k) {
    while (T != NULL && T->key != k) T = (k < T->key) ? T->left : T->right;
    return T;
}
"""

S2 = r"""
#include "problem.h"

BST minimum(BST T) {
    /* TODO: leftmost node, or NULL for an empty tree. */
    return NULL;
}

BST maximum(BST T) {
    /* TODO: rightmost node. */
    return NULL;
}

BST successor(BST T, BST x) {
    /* TODO: the node with the smallest key greater than x->key.
       Case 1: x has a right subtree -> the minimum of that subtree.
       Case 2: no right subtree -> walk UP via parent while x is a RIGHT child;
               the first ancestor you reach from its left is the answer.
       Return NULL if x holds the maximum. */
    return NULL;
}

BST predecessor(BST T, BST x) {
    /* TODO: the mirror image of successor. */
    return NULL;
}
"""

A2 = r"""
#include "problem.h"

BST minimum(BST T) {
    if (T == NULL) return NULL;
    while (T->left != NULL) T = T->left;
    return T;
}

BST maximum(BST T) {
    if (T == NULL) return NULL;
    while (T->right != NULL) T = T->right;
    return T;
}

BST successor(BST T, BST x) {
    (void)T;
    if (x == NULL) return NULL;
    if (x->right != NULL) return minimum(x->right);

    BST y = x->parent;
    while (y != NULL && x == y->right) { x = y; y = y->parent; }
    return y;
}

BST predecessor(BST T, BST x) {
    (void)T;
    if (x == NULL) return NULL;
    if (x->left != NULL) return maximum(x->left);

    BST y = x->parent;
    while (y != NULL && x == y->left) { x = y; y = y->parent; }
    return y;
}
"""

T2 = ["i 15\ni 6\ni 18\ni 3\ni 7\ni 17\ni 20\ni 13\ni 9\nm\nx\nn 13\nn 15\nn 20\nr 6\nr 3\nr 15\ne\n",
      "m\nx\nn 5\ne\n",
      "i 42\nm\nx\nn 42\nr 42\ne\n",
      "i 1\ni 2\ni 3\ni 4\ni 5\nn 1\nn 5\nr 1\nr 5\nm\nx\ne\n",
      "i 5\ni 4\ni 3\ni 2\ni 1\nn 1\nn 5\nr 1\nr 5\ne\n"]
T2 += [ops_script(9, 8, cmds=("n", "r", "m", "x")) for _ in range(4)]

write_problem(
    PACK, UNIT, "p02-successor-parent", title="Week 2 ADT: minimum, maximum, successor, predecessor",
    mode="function", difficulty="medium", estimated_minutes=15, samples=2,
    topics=["bst", "parent pointer"],
    prereqs=[f"{PACK}.{UNIT}.p01-insert-search"],
    source="NITC_Lab_S3_DSA Week 2 - BSTs, ADT functions min(T) and successor(T,x)",
    hints=[
        "minimum is a while loop going left. No recursion needed, and it is the "
        "helper successor calls.",
        "successor case 1: if x has a right subtree, the answer is the minimum of "
        "that subtree - the smallest thing bigger than x.",
        "successor case 2: no right subtree means you have finished x's whole "
        "subtree, so walk up. While x is its parent's RIGHT child, keep climbing; "
        "the first time you arrive from the left, that parent is the successor. "
        "Reaching NULL means x was the maximum.",
    ],
    header=BST_PARENT_H + r"""
/* ---- Provided for you. ---- */
BST init(int key);
BST insert(BST T, int k);
BST search(BST T, int k);

/* ---- Yours. ---- */
BST minimum(BST T);
BST maximum(BST T);
BST successor(BST T, BST x);     /* NULL if x holds the largest key */
BST predecessor(BST T, BST x);   /* NULL if x holds the smallest key */

#endif
""",
    harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"bst_ops.c": PARENT_OPS},
    statement=r"""
# Week 2 ADT: minimum, maximum, successor, predecessor

This is the node from your Week 2 assignment sheet, parent pointer and all:

```c
typedef struct _BSTNode {
    int key;
    struct _BSTNode *left, *right, *parent;
} BSTNode;
typedef BSTNode *BST;
```

`init`, `insert` and `search` are provided (and `insert` maintains `parent` for you).
You write the four navigation functions.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i k` | insert | nothing |
| `m` | minimum | the key, or `-1` if the tree is empty |
| `x` | maximum | the key, or `-1` |
| `n k` | successor of the node holding `k` | the key, or `-1` if none |
| `r k` | predecessor | the key, or `-1` if none |
| `e` | exit | nothing |

## Example

```
i 15
i 6
i 18
i 3
i 7
i 17
i 20
i 13
i 9
m
x
n 13
n 15
n 20
e
```

```
3
20
15
17
-1
```

## Successor: the two cases

**If `x` has a right subtree**, the successor is the *minimum of that subtree* - go
right once, then left as far as you can.

**If it does not**, then you have already visited everything in `x`'s subtree, so the
next key must be above you. Walk up the parent pointers **while `x` is a right child**.
Climbing from a right child means the parent is smaller than you, so it cannot be the
answer. The first time you arrive at a parent from its *left*, that parent is the
successor. If you walk off the top into `NULL`, `x` held the maximum.

`predecessor` is the exact mirror: left subtree's maximum, or climb while `x` is a
*left* child.

## What the parent pointer buys you

Week 2's ADT stores `parent` specifically so case 2 is a simple upward walk. PD Lab 12
Q2 explicitly forbids the parent pointer - there you find the successor by searching
down from the root and remembering the last node you turned *left* at. Both are `O(h)`;
know both, because the two sheets ask for different ones.
""",
)

# ----------------------------------------------------------------- p03
M3 = r"""
#include <stdio.h>
#include "problem.h"

static void inorder(BST r) { if (!r) return; inorder(r->left); printf("%d ", r->key); inorder(r->right); }
static void preorder(BST r) { if (!r) return; printf("%d ", r->key); preorder(r->left); preorder(r->right); }

int main(void) {
    BST T = NULL;
    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'i') {
            int v; if (scanf("%d", &v) != 1) break;
            T = insert(T, v);
        } else if (cmd == 'd') {
            int v; if (scanf("%d", &v) != 1) break;
            BST x = search(T, v);
            if (x == NULL) printf("NOT PRESENT\n");
            else T = delete(T, x);
        } else if (cmd == 'p') {
            if (T == NULL) printf("NULL");
            inorder(T); printf("\n");
        } else if (cmd == 't') {
            if (T == NULL) printf("NULL");
            preorder(T); printf("\n");
        }
    }
    return 0;
}
"""

S3 = r"""
#include <stdlib.h>
#include "problem.h"

/* Replace the subtree rooted at u with the subtree rooted at v.
   Returns the new root of the whole tree. */
BST transplant(BST T, BST u, BST v) {
    /* TODO
       - if u is the root (u->parent == NULL), v becomes the new root
       - else if u is its parent's left child, set that left pointer to v
       - else set the right pointer to v
       - if v is not NULL, fix v->parent
       Return the root: T normally, v when u was the root. */
    return T;
}

BST delete(BST T, BST x) {
    /* TODO - three cases:
       1. no left child  -> transplant x with x->right
       2. no right child -> transplant x with x->left
       3. two children   -> y = minimum(x->right)   (x's successor)
            if y is not x's direct child:
                transplant y with y->right
                y->right = x->right; y->right->parent = y;
            transplant x with y
            y->left = x->left; y->left->parent = y;
       free(x) at the end. */
    return T;
}
"""

A3 = r"""
#include <stdlib.h>
#include "problem.h"

BST transplant(BST T, BST u, BST v) {
    if (u->parent == NULL) T = v;                    /* u was the root */
    else if (u == u->parent->left) u->parent->left = v;
    else u->parent->right = v;
    if (v != NULL) v->parent = u->parent;
    return T;
}

BST delete(BST T, BST x) {
    if (x->left == NULL) {
        T = transplant(T, x, x->right);
    } else if (x->right == NULL) {
        T = transplant(T, x, x->left);
    } else {
        BST y = minimum(x->right);                   /* x's successor */
        if (y->parent != x) {
            T = transplant(T, y, y->right);          /* detach y, keep its right child */
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
"""

T3 = ["i 15\ni 6\ni 18\ni 3\ni 7\ni 17\ni 20\ni 13\ni 9\np\nt\nd 6\np\nt\nd 15\np\nt\ne\n",
      "i 5\ni 3\ni 10\ni 15\np\nd 10\np\nt\nd 5\np\nt\nd 3\nd 15\np\ne\n",
      "i 50\nd 50\np\nt\nd 7\ne\n",
      "i 10\ni 5\ni 15\ni 12\ni 18\ni 11\ni 13\np\nt\nd 10\np\nt\ne\n",
      "i 1\ni 2\ni 3\ni 4\ni 5\nd 1\np\nt\nd 3\np\nt\ne\n",
      "i 5\ni 4\ni 3\ni 2\ni 1\nd 5\np\nt\nd 3\np\nt\ne\n"]
T3 += [ops_script(11, 9, cmds=("d", "p", "t")) for _ in range(4)]

write_problem(
    PACK, UNIT, "p03-delete-transplant", title="BST deletion (transplant, all three cases)",
    mode="function", difficulty="hard", estimated_minutes=25, samples=2,
    topics=["bst", "pointers", "deletion"],
    prereqs=[f"{PACK}.{UNIT}.p02-successor-parent"],
    source="NITC_Lab_S3_DSA Week 2 - BSTs, delete(T,x); the NITC 'BST Deletion' handout",
    hints=[
        "Write transplant first and test it mentally on the root: if u->parent is "
        "NULL then v becomes the new tree root, which is why these functions return "
        "the root.",
        "Cases 1 and 2 are one line each. Note that case 1 also covers a leaf "
        "(x->right is NULL, so you transplant NULL, which is exactly right).",
        "Case 3: y = minimum(x->right). If y is NOT x's direct right child, first "
        "lift y out with transplant(T, y, y->right) and give y the old x->right. "
        "Then transplant x with y and hand y the left subtree. Skipping the "
        "'y->parent != x' check corrupts the tree whenever the successor is adjacent.",
    ],
    header=BST_PARENT_H + r"""
/* ---- Provided for you. ---- */
BST init(int key);
BST insert(BST T, int k);
BST search(BST T, int k);
BST minimum(BST T);

/* ---- Yours. ---- */
BST transplant(BST T, BST u, BST v);   /* returns the root */
BST delete(BST T, BST x);              /* returns the root */

#endif
""",
    harness=M3, starter=S3, solution=A3, tests=T3,
    extra={"bst_ops.c": PARENT_OPS + r"""
BST minimum(BST T) {
    if (T == NULL) return NULL;
    while (T->left != NULL) T = T->left;
    return T;
}
"""},
    statement=r"""
# BST deletion (transplant, all three cases)

The single most test-worthy BST operation, and the one people get 80% right.

```c
BST transplant(BST T, BST u, BST v);   /* put subtree v where subtree u was */
BST delete(BST T, BST x);
```

Both return the root, because deleting the root changes it.

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i k` | insert | nothing |
| `d k` | delete the node holding `k` | `NOT PRESENT` if there is no such key |
| `p` | inorder | keys, or `NULL` |
| `t` | preorder | keys, or `NULL` |
| `e` | exit | nothing |

Both traversals are printed on purpose: inorder stays sorted no matter how badly you
mangle the shape, so **only the preorder reveals a wrong deletion**.

## The three cases

1. **No left child** - replace `x` with `x->right`. (Covers leaves too: `x->right` is
   `NULL`, and transplanting `NULL` is exactly what a leaf needs.)
2. **No right child** - replace `x` with `x->left`.
3. **Two children** - the replacement must be `x`'s **successor**, `y = minimum(x->right)`:
   the smallest key bigger than everything on the left and smaller than everything
   remaining on the right. Two sub-cases:
   - `y` is `x`'s direct right child: just transplant `x` with `y` and give `y` the
     left subtree.
   - `y` is deeper: first lift `y` out of where it is with `transplant(T, y, y->right)`,
     give `y` the old `x->right`, and only then transplant `x` with `y`.

## Example

```
i 15
i 6
i 18
i 3
i 7
i 17
i 20
i 13
i 9
p
t
d 6
p
t
e
```

```
3 6 7 9 13 15 17 18 20
15 6 3 7 13 9 18 17 20
3 7 9 13 15 17 18 20
15 7 3 13 9 18 17 20
```

Deleting 6 (two children) promotes 7, its successor.

## Why `y->parent != x` matters

If the successor is `x`'s direct right child, it is already in the right place and
lifting it out first would detach the subtree you are about to hand it. If it is
deeper, you *must* lift it first. Handling only one of the two sub-cases is the
classic half-correct deletion: it passes every test where the successor happens to be
adjacent and corrupts the tree everywhere else.

## Successor or predecessor?

Either is valid BST-wise, but they give **different shapes**, and the preorder output
here is checked against the successor version - the one CLRS and your Week 2 sheet use.
""",
)

# ----------------------------------------------------------------- p04
H4 = r"""
#ifndef PROBLEM_H
#define PROBLEM_H
#include <stddef.h>   /* NULL */

/* Note: NO parent pointer - PD Lab 12 Q2 forbids it. */
typedef struct Node {
    int key;
    struct Node *left;
    struct Node *right;
} Node;

/* ---- Provided. ---- */
Node *insertKey(Node *root, int key);
Node *searchKey(Node *root, int key);

/* ---- Yours. ---- */
int kthSmallest(Node *root, int k);   /* the k-th smallest key, or -1 if k is too big */
int maximum(Node *root);              /* -1 if the tree is empty */
int successorOf(Node *root, int key); /* next key in inorder after `key`, or -1 */

#endif
"""

NOPARENT_OPS = r"""
#include <stdlib.h>
#include "problem.h"

Node *insertKey(Node *root, int key) {
    if (root == NULL) {
        Node *n = malloc(sizeof(Node));
        n->key = key;
        n->left = n->right = NULL;
        return n;
    }
    if (key < root->key) root->left = insertKey(root->left, key);
    else if (key > root->key) root->right = insertKey(root->right, key);
    return root;
}

Node *searchKey(Node *root, int key) {
    if (root == NULL || root->key == key) return root;
    return key < root->key ? searchKey(root->left, key) : searchKey(root->right, key);
}
"""

M4 = r"""
#include <stdio.h>
#include "problem.h"

int main(void) {
    Node *root = NULL;
    char cmd;
    while (scanf(" %c", &cmd) == 1) {
        if (cmd == 'e') break;
        if (cmd == 'i') {
            int v; if (scanf("%d", &v) != 1) break;
            root = insertKey(root, v);
        } else if (cmd == 'k') {
            int k; if (scanf("%d", &k) != 1) break;
            printf("%d\n", kthSmallest(root, k));
        } else if (cmd == 'm') {
            printf("%d\n", maximum(root));
        } else if (cmd == 'n') {
            int v; if (scanf("%d", &v) != 1) break;
            printf("%d\n", successorOf(root, v));
        }
    }
    return 0;
}
"""

S4 = r"""
#include "problem.h"

int kthSmallest(Node *root, int k) {
    /* TODO: inorder is sorted, so the k-th smallest is the k-th node an inorder
       traversal visits. Walk inorder with a counter and stop at k.
       A helper taking a counter by pointer is the easy way:
           static void walk(Node *r, int k, int *count, int *answer)
       Return -1 if the tree has fewer than k nodes. */
    return -1;
}

int maximum(Node *root) {
    /* TODO: rightmost key, -1 if empty. */
    return -1;
}

int successorOf(Node *root, int key) {
    /* TODO - WITHOUT a parent pointer.
       Walk down from the root. Every time you move LEFT, the node you are leaving
       is bigger than key, so remember it as the best candidate so far. Moving
       right can never be the successor. When you fall off the tree (or land on
       key and it has a right subtree), you have the answer. */
    return -1;
}
"""

A4 = r"""
#include "problem.h"

static void walk(Node *r, int k, int *count, int *answer) {
    if (r == NULL || *answer != -1) return;
    walk(r->left, k, count, answer);
    if (*answer != -1) return;
    (*count)++;
    if (*count == k) { *answer = r->key; return; }
    walk(r->right, k, count, answer);
}

int kthSmallest(Node *root, int k) {
    int count = 0, answer = -1;
    if (k <= 0) return -1;
    walk(root, k, &count, &answer);
    return answer;
}

int maximum(Node *root) {
    if (root == NULL) return -1;
    while (root->right != NULL) root = root->right;
    return root->key;
}

int successorOf(Node *root, int key) {
    int best = -1;
    Node *cur = root;
    while (cur != NULL) {
        if (key < cur->key) { best = cur->key; cur = cur->left; }  /* candidate */
        else cur = cur->right;                                     /* too small */
    }
    return best;
}
"""

T4 = ["i 5\ni 3\ni 10\ni 15\nk 1\nk 2\nk 3\nk 4\nm\nn 5\nn 15\ne\n",
      "i 20\ni 10\ni 30\ni 5\ni 15\ni 25\ni 35\nk 1\nk 4\nk 7\nm\nn 15\nn 30\nn 35\ne\n",
      "k 1\nm\nn 5\ne\n",
      "i 7\nk 1\nk 2\nm\nn 7\ne\n",
      "i 1\ni 2\ni 3\ni 4\ni 5\nk 3\nn 3\nm\ne\n"]
T4 += [ops_script(9, 8, cmds=("k", "m", "n")) for _ in range(4)]

write_problem(
    PACK, UNIT, "p04-kth-successor-noparent", title="k-th smallest and successor without a parent pointer",
    mode="function", difficulty="medium", estimated_minutes=15, samples=2,
    topics=["bst", "inorder"],
    prereqs=[f"{PACK}.{UNIT}.p01-insert-search"],
    source="Core of NITC_Lab_S2_PD Lab 12 Q2 (which forbids the parent pointer)",
    hints=[
        "k-th smallest = the k-th node visited by an inorder traversal, because "
        "inorder is sorted. Count nodes as you visit them.",
        "Pass the counter by pointer (int *count) so it survives across recursive "
        "calls, and stop the traversal once you have the answer.",
        "successorOf with no parent: descend from the root; every time you go LEFT "
        "record the node you left as the best candidate, and going right never "
        "produces a candidate. The last recorded candidate is the successor.",
    ],
    header=H4, harness=M4, starter=S4, solution=A4, tests=T4,
    extra={"bst_ops.c": NOPARENT_OPS},
    statement=r"""
# k-th smallest and successor without a parent pointer

PD Lab 12 Q2 says explicitly: *"When you define the structure for a node of the BST, it
should not contain the parent pointer"* and *"Your program should not contain any
arrays."* So both of these have to work top-down.

```c
int kthSmallest(Node *root, int k);    /* -1 if the tree has fewer than k nodes */
int maximum(Node *root);               /* -1 if empty */
int successorOf(Node *root, int key);  /* -1 if there is no larger key */
```

## Commands

| Command | Meaning | Prints |
|---|---|---|
| `i k` | insert | nothing |
| `k n` | n-th smallest | the key, or `-1` |
| `m` | maximum | the key, or `-1` |
| `n k` | successor of `k` | the key, or `-1` |
| `e` | exit | nothing |

## Example

```
i 5
i 3
i 10
i 15
k 1
k 2
k 3
k 4
m
n 5
n 15
e
```

```
3
5
10
15
15
10
-1
```

## k-th smallest

Inorder is sorted, so the k-th smallest is simply the k-th node inorder visits. Keep a
counter, increment it *between* the two recursive calls, and stop when it reaches `k`.

The counter must be shared across the whole traversal, so pass it as `int *count` - a
plain `int` parameter would give every recursive call its own copy and the count would
reset on the way back up. (This is the `*count` pattern your Lab 12 solution uses.)

Time is `O(n)` in the worst case, which is what the sheet asks for.

## Successor without climbing

With no parent pointer you cannot walk up, so collect the answer on the way **down**:

- if `key < cur->key`, then `cur` is bigger than `key` - it is a *candidate*. Record it
  and go left to look for something smaller that is still bigger than `key`.
- otherwise `cur` is too small to be the answer; go right.

The last candidate you recorded is the successor. Nothing recorded means `key` is the
maximum. Note this even works when `key` itself is not in the tree - it finds the
smallest key greater than it.
""",
)



class _B:
    def __init__(self, k):
        self.k, self.l, self.r = k, None, None


def bst_insert(root, k):
    if root is None:
        return _B(k)
    if k < root.k:
        root.l = bst_insert(root.l, k)
    elif k > root.k:
        root.r = bst_insert(root.r, k)
    return root


def bst_pre(t):
    return [] if t is None else [t.k] + bst_pre(t.l) + bst_pre(t.r)


# ================================================================= p05 PD Lab 12 Q1 (menu, traversals)
LAB12_NODE = r"""
typedef struct Node {
    int key;
    struct Node *left, *right;
} Node;
"""

LAB12_CORE = r"""
static Node *newNode(int key) {
    Node *n = malloc(sizeof(Node));
    n->key = key;
    n->left = n->right = NULL;
    return n;
}

static Node *InsertKey(Node *root, int num) {
    if (root == NULL) return newNode(num);
    if (num < root->key) root->left = InsertKey(root->left, num);
    else if (num > root->key) root->right = InsertKey(root->right, num);
    return root;
}

static Node *SearchKey(Node *root, int num) {
    while (root != NULL && root->key != num) root = (num < root->key) ? root->left : root->right;
    return root;
}

/* Two children: replace with the inorder SUCCESSOR (smallest key on the right). */
static Node *DeleteKey(Node *root, int num) {
    if (root == NULL) return NULL;
    if (num < root->key) root->left = DeleteKey(root->left, num);
    else if (num > root->key) root->right = DeleteKey(root->right, num);
    else {
        if (root->left == NULL) { Node *r = root->right; free(root); return r; }
        if (root->right == NULL) { Node *l = root->left; free(root); return l; }
        Node *succ = root->right;
        while (succ->left != NULL) succ = succ->left;
        root->key = succ->key;                        /* copy the successor up... */
        root->right = DeleteKey(root->right, succ->key);  /* ...then delete it below */
    }
    return root;
}
"""

A5 = r"""
#include <stdio.h>
#include <stdlib.h>
""" + LAB12_NODE + LAB12_CORE + r"""
static void Inorder(Node *r)   { if (!r) return; Inorder(r->left); printf("%d ", r->key); Inorder(r->right); }
static void Preorder(Node *r)  { if (!r) return; printf("%d ", r->key); Preorder(r->left); Preorder(r->right); }
static void Postorder(Node *r) { if (!r) return; Postorder(r->left); Postorder(r->right); printf("%d ", r->key); }

int main(void) {
    Node *root = NULL;
    char c;
    while (scanf(" %c", &c) == 1) {
        int num;
        if (c == 'e') break;
        else if (c == 'i') { if (scanf("%d", &num) != 1) break; root = InsertKey(root, num); }
        else if (c == 's') {
            if (scanf("%d", &num) != 1) break;
            printf(SearchKey(root, num) ? "PRESENT\n" : "NOT PRESENT\n");
        }
        else if (c == 'd') {
            if (scanf("%d", &num) != 1) break;
            if (SearchKey(root, num) == NULL) printf("NOT PRESENT\n");
            else root = DeleteKey(root, num);
        }
        else if (c == 'p') { if (!root) printf("NULL"); Inorder(root);   printf("\n"); }
        else if (c == 't') { if (!root) printf("NULL"); Preorder(root);  printf("\n"); }
        else if (c == 'b') { if (!root) printf("NULL"); Postorder(root); printf("\n"); }
    }
    return 0;
}
"""

S5 = r"""
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    struct Node *left, *right;
} Node;

int main(void) {
    /* TODO: menu loop over i / s / d / p / t / b / e as in the statement.
       No arrays anywhere - the sheet forbids them. */
    return 0;
}
"""


def menu_script(ops, cmds, keyspace=60, absent_delete=False):
    """Random menu input.  Deletes only target keys that are present unless
    absent_delete, because the sheet does not pin down the absent-delete text."""
    live, lines = [], []
    for _ in range(ops):
        c = rng.choice(cmds)
        if c == "i":
            k = rng.randint(1, keyspace)
            if k in live:
                continue                      # the sheet assumes unique keys
            live.append(k)
            lines.append(f"i {k}")
        elif c == "d":
            if live and (not absent_delete or rng.random() < 0.8):
                k = rng.choice(live)
                live.remove(k)
            else:
                k = rng.randint(1, keyspace)
                if k in live:
                    live.remove(k)
            lines.append(f"d {k}")
        elif c == "s":
            lines.append(f"s {rng.choice(live) if live and rng.random() < 0.6 else rng.randint(1, keyspace)}")
        elif c == "k":
            if live:
                lines.append(f"k {rng.randint(1, len(live))}")
        elif c == "m":
            if live:
                lines.append("m")
        elif c == "n":
            srt = sorted(live)
            if len(srt) >= 2:
                lines.append(f"n {rng.choice(srt[:-1])}")   # something that HAS a successor
        else:
            lines.append(c)
    lines.append("e")
    return "\n".join(lines) + "\n"


T5 = ["i 5\ni 3\ni 10\ni 15\np\ns 10\nd 10\np\ni 1\ni 2\np\nt\nb\ne\n",
      "p\nt\nb\ns 4\ni 4\np\nd 4\np\nt\ne\n",
      # two-children deletions, where successor vs predecessor shows in preorder
      "i 50\ni 30\ni 70\ni 20\ni 40\ni 60\ni 80\nd 50\nt\nd 30\nt\nd 70\nt\np\nb\ne\n",
      "i 15\ni 6\ni 18\ni 3\ni 7\ni 17\ni 20\ni 13\ni 9\nd 6\nt\nd 15\nt\nb\ne\n"]
T5 += [menu_script(rng.randint(15, 30), "iiiidspptb") for _ in range(5)]
T5.append(menu_script(900, "iiiiidddsptb", keyspace=5000))   # big: ~900 operations

write_problem(
    PACK, UNIT, "p05-lab12-q1-menu", title="PD Lab 12 Q1: BST menu (insert, search, delete, traversals)",
    mode="program", difficulty="medium", estimated_minutes=30, samples=1,
    topics=["bst", "deletion", "menu-driven"],
    prereqs=[f"{PACK}.{UNIT}.p03-delete-transplant"],
    source="NITC_Lab_S2_PD Assignments/Lab12 Assignment-8, Q1 (official; test 1 is the official sample)",
    hints=[
        "Read the command with scanf(\" %c\", &c) - the leading space skips the newline "
        "left by the previous line. Without it every other command reads '\\n'.",
        "The two-children delete: find the smallest key in the right subtree, copy it "
        "into the node, then delete that key from the right subtree recursively.",
        "An empty tree prints NULL for p, t and b - check before calling the traversal.",
    ],
    starter=S5, solution=A5, tests=T5,
    statement=r"""
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
""",
)

# ================================================================= p06 PD Lab 12 Q2 (kth, max, successor)
A6 = r"""
#include <stdio.h>
#include <stdlib.h>
""" + LAB12_NODE + LAB12_CORE + r"""
static void KthSmallest(Node *root, int k, int *count) {
    if (root == NULL || *count >= k) return;
    KthSmallest(root->left, k, count);
    if (*count >= k) return;
    if (++(*count) == k) { printf("%d\n", root->key); return; }
    KthSmallest(root->right, k, count);
}

static void Maximum(Node *root) {
    if (root == NULL) return;
    while (root->right != NULL) root = root->right;
    printf("%d\n", root->key);
}

/* No parent pointer: descend from the root remembering the last left turn. */
static void Successor(Node *root, int num) {
    Node *best = NULL;
    while (root != NULL) {
        if (num < root->key) { best = root; root = root->left; }
        else root = root->right;
    }
    if (best) printf("%d\n", best->key);
}

int main(void) {
    Node *root = NULL;
    char c;
    while (scanf(" %c", &c) == 1) {
        int num;
        if (c == 'e') break;
        else if (c == 'i') { if (scanf("%d", &num) != 1) break; root = InsertKey(root, num); }
        else if (c == 's') {
            if (scanf("%d", &num) != 1) break;
            printf(SearchKey(root, num) ? "PRESENT\n" : "NOT PRESENT\n");
        }
        else if (c == 'd') {
            if (scanf("%d", &num) != 1) break;
            if (SearchKey(root, num) == NULL) printf("NOT PRESENT\n");
            else root = DeleteKey(root, num);
        }
        else if (c == 'k') { int count = 0; if (scanf("%d", &num) != 1) break; KthSmallest(root, num, &count); }
        else if (c == 'm') Maximum(root);
        else if (c == 'n') { if (scanf("%d", &num) != 1) break; Successor(root, num); }
    }
    return 0;
}
"""

S6 = r"""
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {       /* the sheet forbids a parent pointer */
    int key;
    struct Node *left, *right;
} Node;

int main(void) {
    /* TODO: menu loop over i / d / s / k / m / n / e as in the statement. */
    return 0;
}
"""

T6 = ["i 5\ni 3\ni 10\ni 15\nk 3\nd 10\nk 3\ni 10\nk 2\ns 10\nm\nn 5\ne\n",
      "i 20\ni 10\ni 30\ni 5\ni 15\ni 25\ni 35\nk 1\nk 7\nn 15\nn 35\nn 5\nd 99\nd 20\nk 4\nm\ne\n".replace("n 35\n", ""),
      "i 8\nd 8\ns 8\ni 4\ni 2\ni 6\nk 2\nn 2\nn 4\nm\ne\n"]
T6 += [menu_script(rng.randint(15, 30), "iiiiddskmn", absent_delete=True) for _ in range(5)]
T6.append(menu_script(900, "iiiiiddskkmn", keyspace=5000, absent_delete=True))

write_problem(
    PACK, UNIT, "p06-lab12-q2-kth", title="PD Lab 12 Q2: k-th smallest, maximum, successor (no parent pointer)",
    mode="program", difficulty="medium", estimated_minutes=30, samples=1,
    topics=["bst", "order statistics", "menu-driven"],
    prereqs=[f"{PACK}.{UNIT}.p04-kth-successor-noparent", f"{PACK}.{UNIT}.p05-lab12-q1-menu"],
    source="NITC_Lab_S2_PD Assignments/Lab12 Assignment-8, Q2 (official; test 1 is the official sample)",
    hints=[
        "k-th smallest is an inorder walk with a counter passed by pointer; print when "
        "the counter reaches k and stop descending.",
        "Successor without a parent pointer: walk down from the root; every time you "
        "go LEFT, the node you leave is a candidate. The last candidate is the answer.",
        "Here deleting an absent key prints NOT PRESENT - the Q2 output spec says so "
        "explicitly, unlike Q1.",
    ],
    starter=S6, solution=A6, tests=T6,
    statement=r"""
# PD Lab 12 Q2: k-th smallest, maximum, successor (no parent pointer)

**Official statement** - PD Lab 12, Q2. Test 1 is the sheet's sample.

> Design a C program featuring a menu-driven interface for a binary search tree (BST)
> consisting of integers that can output the k-th smallest integer in the tree...
>
> **NOTE:** When you define the structure for a node of the BST, it **should not contain
> the parent pointer**. Your program **should not contain any arrays**. Assume that the
> BST at every stage always has unique key values.
>
> Insert, search, delete, maximum and successor `O(h)`; k-th smallest `O(n)`.

## Commands

| Input | Function | Output |
|---|---|---|
| `i num` | `InsertKey` | nothing |
| `s num` | `SearchKey` | `PRESENT` or `NOT PRESENT` |
| `d num` | `DeleteKey` | `NOT PRESENT` if `num` is not in the tree |
| `k k` | `KthSmallest` | the k-th smallest key |
| `m` | `Maximum` | the largest key |
| `n num` | `Successor` | the next key after `num` in inorder |
| `e` | exit | nothing |

## Sample

```
i 5
i 3
i 10
i 15
k 3
d 10
k 3
i 10
k 2
s 10
m
n 5
e
```

```
10
15
5
PRESENT
15
10
```

## What the tests avoid

The sheet does not say what to print for `k` larger than the tree, `m` on an empty
tree, or `n` on the maximum. The tests never ask those, so any behaviour passes. In the
exam, printing nothing (or `-1`) and saying so is reasonable.

## Successor without climbing

With no parent pointer you cannot walk up, so collect the answer on the way **down**:
whenever `num < root->key`, the current node is bigger than `num` - a candidate -
so remember it and go left to look for something smaller. Otherwise go right. The last
remembered candidate is the successor.
""",
)

# ================================================================= p07 PD Lab 12 Q4 (subtree)
A7 = r"""
#include <stdio.h>
#include <stdlib.h>
""" + LAB12_NODE + r"""
static Node *newNode(int key) {
    Node *n = malloc(sizeof(Node));
    n->key = key;
    n->left = n->right = NULL;
    return n;
}

static Node *insert(Node *root, int key) {
    if (root == NULL) return newNode(key);
    if (key < root->key) root->left = insert(root->left, key);
    else root->right = insert(root->right, key);
    return root;
}

/* Same shape and same keys, node for node. */
static int identical(Node *a, Node *b) {
    if (a == NULL || b == NULL) return a == b;
    return a->key == b->key && identical(a->left, b->left) && identical(a->right, b->right);
}

/* Keys are unique, so the only candidate is the node holding BST1's root key.
   Find it in O(h), then compare. */
static int isSubtree(Node *t1, Node *t2) {
    if (t1 == NULL) return 1;
    while (t2 != NULL && t2->key != t1->key) t2 = (t1->key < t2->key) ? t2->left : t2->right;
    return t2 != NULL && identical(t1, t2);
}

static Node *readBST(void) {
    int n, k;
    Node *root = NULL;
    if (scanf("%d", &n) != 1) return NULL;
    for (int i = 0; i < n; i++)
        if (scanf("%d", &k) == 1) root = insert(root, k);
    return root;
}

int main(void) {
    Node *t1 = readBST();
    Node *t2 = readBST();
    printf(isSubtree(t1, t2) ? "BST1 is a subtree of BST2\n" : "BST1 is NOT a subtree of BST2\n");
    return 0;
}
"""

S7 = r"""
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int key;
    struct Node *left, *right;
} Node;

int main(void) {
    /* TODO: build both BSTs by inserting in the given order, then decide whether
       some node of BST2 roots a subtree IDENTICAL to BST1 (same shape, same keys). */
    return 0;
}
"""


def subtree_case(want_yes):
    keys = rng.sample(range(1, 200), rng.randint(6, 20))
    root = None
    for k in keys:
        root = bst_insert(root, k)
    # pick a node with at least one child so the subtree is interesting
    nodes = []
    stack = [root]
    while stack:
        x = stack.pop()
        if x:
            nodes.append(x)
            stack += [x.l, x.r]
    pick = rng.choice([x for x in nodes if x.l or x.r] or nodes)
    sub = bst_pre(pick)                    # inserting a preorder rebuilds the same shape
    if not want_yes:
        mode = rng.choice(["drop", "add", "reorder"])
        if mode == "drop" and len(sub) > 1:
            sub = sub[:-1]                 # missing a node: same prefix, smaller tree
        elif mode == "add":
            extra = rng.randint(1, 199)
            while extra in keys:
                extra = rng.randint(1, 199)
            sub = sub + [extra]
        else:
            sub = sorted(sub)              # same keys, different shape (a chain)
    return f"{len(sub)}\n{' '.join(map(str, sub))}\n{len(keys)}\n{' '.join(map(str, keys))}\n"


T7 = ["3\n3 1 5\n5\n10 5 15 1 3\n",
      "3\n4 2 5\n6\n6 4 8 2 5 7\n",
      "2\n2 3\n5\n10 8 12 7 9\n",
      "5\n10 5 15 1 3\n5\n10 5 15 1 3\n",          # a tree is a subtree of itself
      "1\n7\n4\n10 5 15 7\n",                      # a single leaf
      "1\n5\n4\n10 5 15 7\n",                      # key present, but 5 has a child here
      "3\n5 3 7\n5\n10 5 3 7 6\n"]                  # extra node below: NOT identical
for k in range(6):
    T7.append(subtree_case(want_yes=(k % 2 == 0)))

write_problem(
    PACK, UNIT, "p07-lab12-q4-subtree", title="PD Lab 12 Q4: is BST1 a subtree of BST2?",
    mode="program", difficulty="medium", estimated_minutes=20, samples=3,
    topics=["bst", "recursion", "tree comparison"],
    prereqs=[f"{PACK}.{UNIT}.p01-insert-search"],
    source="NITC_Lab_S2_PD Assignments/Lab12 Assignment-8, Q4 (official; tests 1-3 are the official samples)",
    hints=[
        "Write identical(a, b) first: both NULL -> yes; one NULL -> no; otherwise "
        "equal keys AND identical left AND identical right.",
        "Keys are unique, so only ONE node of BST2 can possibly match: the one holding "
        "BST1's root key. Search for it like a normal BST search, then compare.",
        "Identical means the whole subtree, not just a prefix. A matching node with an "
        "extra descendant (test 7) is NOT a subtree.",
    ],
    starter=S7, solution=A7, tests=T7,
    statement=r"""
# PD Lab 12 Q4: is BST1 a subtree of BST2?

**Official statement** - PD Lab 12, Q4. Tests 1-3 are the sheet's three samples.

> A BST (BST1) is considered a subtree of BST2 if there exists a node in BST2 such that
> the subtree rooted at that node is **identical** to BST1.

## Input format

- `N1`, then `N1` book IDs inserted into BST1 in that order
- `N2`, then `N2` book IDs inserted into BST2 in that order

## Output format

`BST1 is a subtree of BST2` or `BST1 is NOT a subtree of BST2`.

## Samples

```
3
3 1 5
5
10 5 15 1 3
```

```
BST1 is NOT a subtree of BST2
```

```
3
4 2 5
6
6 4 8 2 5 7
```

```
BST1 is a subtree of BST2
```

In sample 1 the keys 1, 3 and 5 all appear in BST2, but not in BST1's shape. 5 is the
parent of 1 there, and 3 hangs below 1. "Contains the keys" is not "is a subtree".

## Two functions

```c
int identical(Node *a, Node *b) {
    if (a == NULL || b == NULL) return a == b;
    return a->key == b->key && identical(a->left, b->left) && identical(a->right, b->right);
}
```

Then find the candidate. In a general binary tree you would have to try `identical` at
every node of BST2. Here the keys are unique and ordered, so **exactly one** node can
match: the one holding BST1's root key. Find it with an ordinary `O(h)` BST search and
compare once.

## Identical means all of it

Test 7 has BST1 = `5(3, 7)` and a BST2 where 5 has children 3 and 7, but 7 has a child
of its own. The top of the subtree matches and the whole thing does not, so the answer
is NOT.
""",
)


report(UNIT, 7)
