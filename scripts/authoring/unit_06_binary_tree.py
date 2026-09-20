"""Unit 06 - Binary trees.  Run: python scripts/authoring/unit_06_binary_tree.py"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_unit, write_problem, report
from _trees import random_tree, spaced, compact

PACK = "c-s3"
UNIT = "06-binary-tree"
rng = random.Random(606)

write_unit(PACK, UNIT, "Binary trees",
           "Pointer trees, the two parenthesized input notations from PD Lab 10, "
           "traversals, level order, and the three Lab 10 tree programs verbatim.")

NODE = r"""
#include <stddef.h>   /* NULL */

typedef struct Node {
    int data;
    struct Node *left;
    struct Node *right;
} Node;
"""

# The reference parser.  It accepts both NITC notations: every child written out
# ("( 1 ( ) ( ) )") and bare leaves ("(20(11(2)())...)").
PARSER = r"""
#include <ctype.h>
#include <stdlib.h>
#include "problem.h"

Node *newNode(int value) {
    Node *n = malloc(sizeof(Node));
    n->data = value;
    n->left = n->right = NULL;
    return n;
}

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    if (s[*i] != '(') return NULL;          /* no subtree here at all */
    (*i)++;
    skipSpace(s, i);
    if (s[*i] == ')') { (*i)++; return NULL; }   /* "( )" is an empty child */

    int sign = 1, value = 0;
    if (s[*i] == '-') { sign = -1; (*i)++; }
    while (isdigit((unsigned char)s[*i])) value = value * 10 + (s[(*i)++] - '0');

    Node *n = newNode(sign * value);
    n->left = buildTree(s, i);              /* each returns NULL without consuming */
    n->right = buildTree(s, i);             /* anything if the next char is not '(' */
    skipSpace(s, i);
    if (s[*i] == ')') (*i)++;
    return n;
}

void freeTree(Node *root) {
    if (root == NULL) return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}
"""

PROVIDED_DECLS = r"""
/* ---- Provided for you. ---- */
Node *newNode(int value);
Node *buildTree(const char *s, int *i);   /* parses either parenthesized notation */
void  freeTree(Node *root);
"""

READ_LINE = r"""
static char line[200005];

static Node *readTree(void) {
    if (fgets(line, sizeof line, stdin) == NULL) return NULL;
    int i = 0;
    return buildTree(line, &i);
}
"""


def tree_inputs(count, sizes=(1, 14), fmt="mixed"):
    out = []
    shapes = ["random", "random", "random", "left", "right", "full"]
    for k in range(count):
        n = rng.randint(*sizes)
        t = random_tree(rng, n, shape=shapes[k % len(shapes)])
        use = fmt if fmt != "mixed" else ("spaced" if k % 2 == 0 else "compact")
        out.append((t, spaced(t) if use == "spaced" else compact(t)))
    return out


NOTATION = r"""
## Input notation

One line holding the tree in either NITC parenthesized notation:

```
( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )
(20(11(2)())(8(6)(10)))
```

`( )` or `()` is an empty child; a leaf may appear bare as `(2)`. The tree is parsed
for you before your function is called.
"""

# --------------------------------------------------------------- p01 traversals
H1 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + PROVIDED_DECLS + r"""
/* ---- Yours: print the node values in order, each followed by a space. ---- */
void preorder(Node *root);
void inorder(Node *root);
void postorder(Node *root);

#endif
"""

M1 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_LINE + r"""
int main(void) {
    Node *root = readTree();
    preorder(root);  printf("\n");
    inorder(root);   printf("\n");
    postorder(root); printf("\n");
    freeTree(root);
    return 0;
}
"""

S1 = r"""
#include <stdio.h>
#include "problem.h"

void preorder(Node *root) {
    /* TODO: root, then left subtree, then right subtree.
       Every recursive tree function starts with the same line:
       if (root == NULL) return; */
}

void inorder(Node *root) {
    /* TODO: left, root, right */
}

void postorder(Node *root) {
    /* TODO: left, right, root */
}
"""

A1 = r"""
#include <stdio.h>
#include "problem.h"

void preorder(Node *root) {
    if (root == NULL) return;
    printf("%d ", root->data);
    preorder(root->left);
    preorder(root->right);
}

void inorder(Node *root) {
    if (root == NULL) return;
    inorder(root->left);
    printf("%d ", root->data);
    inorder(root->right);
}

void postorder(Node *root) {
    if (root == NULL) return;
    postorder(root->left);
    postorder(root->right);
    printf("%d ", root->data);
}
"""

T1 = ["( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )\n", "(20(11(2)())(8(6)(10)))\n", "(7)\n"]
T1 += [s + "\n" for _, s in tree_inputs(5)]

write_problem(
    PACK, UNIT, "p01-traversals", title="Preorder, inorder, postorder",
    mode="function", difficulty="easy", estimated_minutes=6, samples=2,
    topics=["binary tree", "recursion", "traversal"],
    source="Foundation for PD Lab 10 Q2-Q4 and DSA Lab Week 2",
    hints=[
        "Every one of these is three lines after the base case "
        "'if (root == NULL) return;'. Only the position of the printf moves.",
        "Pre = print before both recursive calls, in = between them, post = after both.",
    ],
    header=H1, harness=M1, starter=S1, solution=A1, tests=T1,
    extra={"parse.c": PARSER},
    statement=r"""
# Preorder, inorder, postorder

The three depth-first traversals. Each is the same three-line recursion with the
`printf` in a different place - make sure you can write all three without thinking,
because every other tree problem is built on them.

```c
void preorder(Node *root);   /* root, left, right */
void inorder(Node *root);    /* left, root, right */
void postorder(Node *root);  /* left, right, root */
```

Print each value followed by a single space. The hidden `main()` prints the newline.
""" + NOTATION + r"""
## Example

```
( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )
```

```
1 2 4 3
4 2 1 3
4 2 3 1
```

## Reading them off a picture quickly

For a hand-check under exam pressure: walk around the tree anticlockwise starting at
the root's left. Preorder records each node the first time you pass it (on its left
side), inorder when you pass underneath it, postorder the last time (on its right side).
""",
)

# --------------------------------------------------------------- p02 parser
H2 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + r"""
/* ---- Provided for you. ---- */
Node *newNode(int value);
void  freeTree(Node *root);

/* ---- Yours: parse a tree starting at s[*i], advancing *i past it.
        Return NULL for an empty subtree "( )" / "()", and also return NULL
        WITHOUT consuming anything if s[*i] (after spaces) is not '('. ---- */
Node *buildTree(const char *s, int *i);

#endif
"""

PROVIDED_NODE = r"""
#include <stdlib.h>
#include "problem.h"

Node *newNode(int value) {
    Node *n = malloc(sizeof(Node));
    n->data = value;
    n->left = n->right = NULL;
    return n;
}

void freeTree(Node *root) {
    if (root == NULL) return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}
"""

M2 = r"""
#include <stdio.h>
#include "problem.h"

static char line[200005];

static void pre(Node *r) { if (!r) return; printf("%d ", r->data); pre(r->left); pre(r->right); }
static void in(Node *r)  { if (!r) return; in(r->left); printf("%d ", r->data); in(r->right); }

int main(void) {
    if (fgets(line, sizeof line, stdin) == NULL) return 0;
    int i = 0;
    Node *root = buildTree(line, &i);
    if (root == NULL) { printf("EMPTY\n"); return 0; }
    /* preorder + inorder together pin down the exact shape you built */
    pre(root); printf("\n");
    in(root);  printf("\n");
    freeTree(root);
    return 0;
}
"""

S2 = r"""
#include <ctype.h>
#include "problem.h"

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    /* TODO
       1. if s[*i] is not '(' -> return NULL, consuming nothing
       2. consume '(' and skip spaces
       3. if s[*i] is ')' -> consume it, return NULL (empty child)
       4. read the number digit by digit, make a node
       5. node->left  = buildTree(s, i);
          node->right = buildTree(s, i);
          (step 1 makes these return NULL safely when a child is missing)
       6. skip spaces, consume the closing ')', return the node */
    return NULL;
}
"""

A2 = r"""
#include <ctype.h>
#include "problem.h"

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    if (s[*i] != '(') return NULL;
    (*i)++;
    skipSpace(s, i);
    if (s[*i] == ')') { (*i)++; return NULL; }

    int sign = 1, value = 0;
    if (s[*i] == '-') { sign = -1; (*i)++; }
    while (isdigit((unsigned char)s[*i])) value = value * 10 + (s[(*i)++] - '0');

    Node *n = newNode(sign * value);
    n->left = buildTree(s, i);
    n->right = buildTree(s, i);
    skipSpace(s, i);
    if (s[*i] == ')') (*i)++;
    return n;
}
"""

T2 = ["( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )\n", "(20(11(2)())(8(6)(10)))\n",
      "(5)\n", "(12()(2()(13()(4()(5)))))\n", "(100(15(2(10)())())())\n",
      "( 42 ( ) ( ) )\n", "( )\n", "(9(8(7(6))))\n", "(123(45)(6789))\n"]
T2 += [s + "\n" for _, s in tree_inputs(4, sizes=(6, 18))]

write_problem(
    PACK, UNIT, "p02-parse-notation", title="Parse the parenthesized notation",
    mode="function", difficulty="medium", estimated_minutes=15, samples=2,
    topics=["binary tree", "recursion", "parsing"],
    source="The input format of PD Lab 10 Q2, Q3 and Q5",
    hints=[
        "Pass the position as int *i and advance it through the string; every "
        "recursive call continues exactly where the previous one stopped.",
        "The key design choice: if the next non-space character is not '(', return "
        "NULL WITHOUT moving *i. That single rule makes '(2)' (bare leaf) and "
        "'(2()())' (explicit empties) parse identically.",
        "Numbers can be multi-digit: value = value * 10 + (s[*i] - '0') while isdigit. "
        "Reading one character as the value is the classic bug - it passes on "
        "single-digit trees only.",
    ],
    header=H2, harness=M2, starter=S2, solution=A2, tests=T2,
    extra={"node.c": PROVIDED_NODE},
    statement=r"""
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
""",
)

# --------------------------------------------------------------- p03 height/size
H3 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + PROVIDED_DECLS + r"""
/* ---- Yours. ---- */
int height(Node *root);        /* nodes on the longest root-to-leaf path; empty = 0 */
int countNodes(Node *root);
int countLeaves(Node *root);   /* nodes with no children */

#endif
"""

M3 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_LINE + r"""
int main(void) {
    Node *root = readTree();
    printf("%d %d %d\n", height(root), countNodes(root), countLeaves(root));
    freeTree(root);
    return 0;
}
"""

S3 = r"""
#include "problem.h"

int height(Node *root) {
    return 0;   /* TODO: 0 for empty, else 1 + the larger child height */
}

int countNodes(Node *root) {
    return 0;   /* TODO */
}

int countLeaves(Node *root) {
    return 0;   /* TODO: careful - an empty tree is not a leaf */
}
"""

A3 = r"""
#include "problem.h"

int height(Node *root) {
    if (root == NULL) return 0;
    int l = height(root->left), r = height(root->right);
    return 1 + (l > r ? l : r);
}

int countNodes(Node *root) {
    if (root == NULL) return 0;
    return 1 + countNodes(root->left) + countNodes(root->right);
}

int countLeaves(Node *root) {
    if (root == NULL) return 0;
    if (root->left == NULL && root->right == NULL) return 1;
    return countLeaves(root->left) + countLeaves(root->right);
}
"""

T3 = ["( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )\n", "(7)\n", "( )\n",
      "(12()(2()(13()(4()(5)))))\n", "(500(25(10)(30))(75(60)(90)))\n"]
T3 += [s + "\n" for _, s in tree_inputs(5, sizes=(2, 20))]

write_problem(
    PACK, UNIT, "p03-height-size-leaves", title="Height, size and leaves",
    mode="function", difficulty="easy", estimated_minutes=7, samples=2,
    topics=["binary tree", "recursion"],
    prereqs=[f"{PACK}.{UNIT}.p01-traversals"],
    hints=[
        "Each function is: base case for NULL, then combine the answers from the "
        "two children. Trust the recursion - do not try to trace the whole tree.",
        "height = 1 + max(height(left), height(right)). C has no integer max; "
        "write l > r ? l : r.",
        "countLeaves needs two base cases: NULL gives 0, and a node with both "
        "children NULL gives 1.",
    ],
    header=H3, harness=M3, starter=S3, solution=A3, tests=T3,
    extra={"parse.c": PARSER},
    statement=r"""
# Height, size and leaves

Three recursive functions with the same skeleton: a base case for `NULL`, then combine
what the two children report.

```c
int height(Node *root);       /* nodes on the longest root-to-leaf path, 0 if empty */
int countNodes(Node *root);
int countLeaves(Node *root);
```

The hidden `main()` prints `height nodes leaves` on one line.
""" + NOTATION + r"""
## Example

```
( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )
```

```
3 4 2
```

## Height: nodes or edges?

Textbooks disagree. Here height counts **nodes**, so a single node has height 1 and an
empty tree 0. The other convention counts edges (single node 0, empty -1). In a test,
read which one the question means - an off-by-one here fails every test case at once.
""",
)

# --------------------------------------------------------------- p04 level order
H4 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + PROVIDED_DECLS + r"""
#define MAXQ 100005

/* ---- Yours: print each level on its own line, left to right, values
        followed by a space.  Print nothing at all for an empty tree. ---- */
void levelOrder(Node *root);

#endif
"""

M4 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_LINE + r"""
int main(void) {
    Node *root = readTree();
    levelOrder(root);
    freeTree(root);
    return 0;
}
"""

S4 = r"""
#include <stdio.h>
#include "problem.h"

void levelOrder(Node *root) {
    static Node *q[MAXQ];    /* a queue of node POINTERS */
    int head = 0, tail = 0;

    /* TODO
       - push root (if not NULL)
       - while the queue is not empty:
           size = tail - head        <- how many nodes are on THIS level
           pop exactly 'size' nodes, printing each and pushing its children
           print a newline
       Freezing 'size' before the inner loop is what separates the levels. */
}
"""

A4 = r"""
#include <stdio.h>
#include "problem.h"

void levelOrder(Node *root) {
    static Node *q[MAXQ];
    int head = 0, tail = 0;
    if (root == NULL) return;

    q[tail++] = root;
    while (head < tail) {
        int size = tail - head;          /* nodes on the current level */
        for (int k = 0; k < size; k++) {
            Node *cur = q[head++];
            printf("%d ", cur->data);
            if (cur->left)  q[tail++] = cur->left;
            if (cur->right) q[tail++] = cur->right;
        }
        printf("\n");
    }
}
"""

T4 = ["( 1 ( 2 ( 4 ( ) ( ) ) ( ) ) ( 3 ( ) ( ) ) )\n", "(120(5(25(15)(10))(20(6)(7)))(85(130)(135()(200))))\n",
      "(7)\n", "( )\n", "(12()(2()(13()(4()(5)))))\n"]
T4 += [s + "\n" for _, s in tree_inputs(5, sizes=(4, 22))]

write_problem(
    PACK, UNIT, "p04-level-order", title="Level order, one line per level",
    mode="function", difficulty="medium", estimated_minutes=10, samples=2, allow_empty=True,
    topics=["binary tree", "bfs", "queue"],
    prereqs=[f"{PACK}.{UNIT}.p01-traversals", f"{PACK}.04-bfs.p02-bfs-order"],
    source="PD Lab 10 Q4 option 5",
    hints=[
        "It is BFS on a tree. The queue holds Node * pointers, not ints: "
        "static Node *q[MAXQ].",
        "To split levels: before processing a level, record size = tail - head. "
        "Pop exactly that many; everything they push belongs to the next level.",
        "No visited array needed - a tree has no cycles, so each node is reached "
        "exactly once, from its parent.",
    ],
    header=H4, harness=M4, starter=S4, solution=A4, tests=T4,
    extra={"parse.c": PARSER},
    statement=r"""
# Level order, one line per level

BFS on a tree: visit the root, then everything at depth 1, then depth 2, and so on.

```c
void levelOrder(Node *root);
```

Print each level on its own line, left to right, each value followed by a space.
""" + NOTATION + r"""
## Example

```
(120(5(25(15)(10))(20(6)(7)))(85(130)(135()(200))))
```

```
120
5 85
25 20 130 135
15 10 6 7 200
```

## Splitting the levels

A plain BFS prints everything on one line. To break it into levels, look at the queue
at the start of each level: **it contains exactly the nodes of that level and nothing
else**. So record `size = tail - head`, pop exactly `size` nodes, and print a newline.
Everything those nodes pushed belongs to the next level.

## The queue holds pointers

`static Node *q[MAXQ];` - an array of `Node *`. It is `static` so a large capacity
does not sit on the function's stack frame.
""",
)

# --------------------------------------------------------------- p05 depth k (Lab10 Q2)
A5 = r"""
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left, *right;
} Node;

static char line[2000005];

static void skipSpace(const char *s, int *i) {
    while (s[*i] == ' ' || s[*i] == '\t' || s[*i] == '\n' || s[*i] == '\r') (*i)++;
}

static Node *buildTree(const char *s, int *i) {
    skipSpace(s, i);
    if (s[*i] != '(') return NULL;
    (*i)++;
    skipSpace(s, i);
    if (s[*i] == ')') { (*i)++; return NULL; }
    int value = 0;
    while (isdigit((unsigned char)s[*i])) value = value * 10 + (s[(*i)++] - '0');
    Node *n = malloc(sizeof(Node));
    n->data = value;
    n->left = buildTree(s, i);
    n->right = buildTree(s, i);
    skipSpace(s, i);
    if (s[*i] == ')') (*i)++;
    return n;
}

static Node *findNode(Node *root, int x) {
    if (root == NULL || root->data == x) return root;
    Node *l = findNode(root->left, x);
    return l ? l : findNode(root->right, x);
}

static void printAtDepth(Node *root, int k, int *first) {
    if (root == NULL) return;
    if (k == 0) {
        printf(*first ? "%d" : " %d", root->data);
        *first = 0;
        return;
    }
    printAtDepth(root->left, k - 1, first);
    printAtDepth(root->right, k - 1, first);
}

static void freeTree(Node *r) {
    if (!r) return;
    freeTree(r->left); freeTree(r->right); free(r);
}

int main(void) {
    int x, k, i = 0, first = 1;
    if (fgets(line, sizeof line, stdin) == NULL) return 0;
    if (scanf("%d %d", &x, &k) != 2) return 0;

    Node *root = buildTree(line, &i);
    printAtDepth(findNode(root, x), k, &first);
    printf("\n");
    freeTree(root);
    return 0;
}
"""

S5 = r"""
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left, *right;
} Node;

int main(void) {
    /* TODO: the whole program.
       1. read the tree line with fgets (it contains spaces - scanf("%s") would stop
          at the first one)
       2. read x and k with scanf
       3. parse the tree, find the node holding x
       4. print every node exactly k levels below it, left to right */
    return 0;
}
"""

T5 = ["( 2 ( 7 ( 10 ( ) ( ) ) ( 6 ( 5 ( ) ( ) ) ( 11 ( ) ( ) ) ) ) ( 9 ( ) ( 3 ( ) ( ) ) ) )\n7\n2\n",
      "( 2 ( 7 ( 10 ( ) ( ) ) ( 6 ( 5 ( ) ( ) ) ( 11 ( ) ( ) ) ) ) ( 9 ( ) ( 3 ( ) ( ) ) ) )\n2\n1\n",
      "( 2 ( 7 ( 10 ( ) ( ) ) ( 6 ( 5 ( ) ( ) ) ( 11 ( ) ( ) ) ) ) ( 9 ( ) ( 3 ( ) ( ) ) ) )\n2\n3\n",
      "( 2 ( 7 ( 10 ( ) ( ) ) ( 6 ( 5 ( ) ( ) ) ( 11 ( ) ( ) ) ) ) ( 9 ( ) ( 3 ( ) ( ) ) ) )\n9\n1\n"]
def _nodes(t):
    return [] if t is None else [t] + _nodes(t.l) + _nodes(t.r)


def _at_depth(t, k):
    if t is None:
        return []
    return [t] if k == 0 else _at_depth(t.l, k - 1) + _at_depth(t.r, k - 1)


# Pick (x, k) so there IS an answer - a random pick usually lands on a leaf.
# Test 3 (x=9, k=1 on the sample tree) already covers a single-node answer.
for t, _ in tree_inputs(6, sizes=(9, 25), fmt="spaced"):
    choices = [(n.v, k) for n in _nodes(t) for k in range(1, 5) if _at_depth(n, k)]
    x, k = rng.choice(choices)
    T5.append(f"{spaced(t)}\n{x}\n{k}\n")
# ...and exactly one deliberate "nothing that deep" case.
T5.append("( 2 ( 7 ( 10 ( ) ( ) ) ( 6 ( 5 ( ) ( ) ) ( 11 ( ) ( ) ) ) ) ( 9 ( ) ( 3 ( ) ( ) ) ) )\n9\n3\n")

write_problem(
    PACK, UNIT, "p05-depth-k-subtree", title="PD Lab 10 Q2: nodes at depth k below x",
    mode="program", difficulty="medium", estimated_minutes=20, samples=1, allow_empty=True,
    topics=["binary tree", "recursion", "parsing"],
    prereqs=[f"{PACK}.{UNIT}.p02-parse-notation"],
    source="NITC_Lab_S2_PD Assignments/Lab10 Assignment-6, Q2 (verbatim)",
    hints=[
        "Three separate jobs: parse, find x, print depth k. Write them as three "
        "functions; each is short.",
        "findNode searches BOTH subtrees - this is a plain binary tree, not a BST, so "
        "there is no left/right shortcut.",
        "printAtDepth(node, k): if k == 0 print node; otherwise recurse into both "
        "children with k - 1. Left before right gives left-to-right order.",
    ],
    starter=S5, solution=A5, tests=T5,
    statement=r"""
# PD Lab 10 Q2: nodes at depth k below x

Verbatim from PD Lab 10.

> Given the parenthesis representation of a binary tree `T` with `n` nodes, a node with
> key value `x` and a positive integer `k < n`, print all the nodes at a depth of `k` in
> the subtree of `T` rooted at `x`. Assume that all key values in the tree are unique.

## Input format

- first line: the space-separated parentheses representation of the tree
- second line: the integer `x`
- third line: the integer `k`

## Output format

One line with the key values at depth `k` below `x`, space separated, left to right.
If there are none, print an empty line.

## Sample

```
( 2 ( 7 ( 10 ( ) ( ) ) ( 6 ( 5 ( ) ( ) ) ( 11 ( ) ( ) ) ) ) ( 9 ( ) ( 3 ( ) ( ) ) ) )
7
2
```

```
5 11
```

## The input trap

The tree line contains spaces, so `scanf("%s")` reads only `(`. Read the whole line
with `fgets` first, **then** `scanf` the two integers. Doing it in the other order does
not work either: a `scanf` before `fgets` leaves a newline that `fgets` swallows as an
empty line.
""",
)

# --------------------------------------------------------------- p06 postorder (Lab10 Q3)
A6 = r"""
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left, *right;
} Node;

static char s[200005];

static Node *buildTree(const char *str, int *i) {
    if (str[*i] != '(') return NULL;
    (*i)++;
    if (str[*i] == ')') { (*i)++; return NULL; }
    int value = 0;
    while (isdigit((unsigned char)str[*i])) value = value * 10 + (str[(*i)++] - '0');
    Node *n = malloc(sizeof(Node));
    n->data = value;
    n->left = buildTree(str, i);
    n->right = buildTree(str, i);
    if (str[*i] == ')') (*i)++;
    return n;
}

static void postorder(Node *r, int *first) {
    if (r == NULL) return;
    postorder(r->left, first);
    postorder(r->right, first);
    printf(*first ? "%d" : " %d", r->data);
    *first = 0;
}

static void freeTree(Node *r) {
    if (!r) return;
    freeTree(r->left); freeTree(r->right); free(r);
}

int main(void) {
    int i = 0, first = 1;
    if (scanf("%200000s", s) != 1) return 0;
    Node *root = buildTree(s, &i);
    postorder(root, &first);
    printf("\n");
    freeTree(root);
    return 0;
}
"""

S6 = r"""
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *left, *right;
} Node;

int main(void) {
    /* TODO: read the string (no spaces in this format, so scanf("%s") is fine),
       build the tree, print its postorder. */
    return 0;
}
"""

T6 = ["(20(11(2)())(8(6)(10)))\n", "(100(15(2(10)())())())\n", "(12()(2()(13()(4()(5)))))\n",
      "(500(25(10)(30))(75(60)(90)))\n", "(120(5(25(15)(10))(20(6)(7)))(85(130)(135()(200))))\n",
      "(1)\n"]
for k in range(4):
    n = rng.randint(5, 30)
    t = random_tree(rng, n, values=rng.sample(range(1, 100001), n),
                    shape=["random", "left", "right", "random"][k])
    T6.append(compact(t, bare_leaves=(k % 2 == 0)) + "\n")

write_problem(
    PACK, UNIT, "p06-postorder-notation", title="PD Lab 10 Q3: build and print postorder",
    mode="program", difficulty="medium", estimated_minutes=15, samples=5,
    topics=["binary tree", "recursion", "parsing"],
    prereqs=[f"{PACK}.{UNIT}.p02-parse-notation"],
    source="NITC_Lab_S2_PD Assignments/Lab10 Assignment-6, Q3 (verbatim; tests 1-5 are the official samples)",
    hints=[
        "The parser from the previous rung works unchanged - there are just no spaces "
        "to skip.",
        "Values go up to 100000, so they are multi-digit. Sample 1 has 20 and 11: "
        "if you read one digit per node you will build a completely different tree.",
    ],
    starter=S6, solution=A6, tests=T6,
    statement=r"""
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
""",
)

# --------------------------------------------------------------- p07 vehicle tree (Lab10 Q4)
A7 = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Vehicle {
    int vno;
    char model[32];
    int price;
    struct Vehicle *left, *right;
} Vehicle;

static Vehicle *q[10005];

static Vehicle *newVehicle(int vno, const char *model, int price) {
    Vehicle *v = malloc(sizeof(Vehicle));
    v->vno = vno;
    strncpy(v->model, model, sizeof v->model - 1);
    v->model[sizeof v->model - 1] = '\0';
    v->price = price;
    v->left = v->right = NULL;
    return v;
}

/* Level-order insertion: the new node goes into the first free child slot
   found by a BFS, left before right. */
static Vehicle *insertLevelOrder(Vehicle *root, Vehicle *node) {
    if (root == NULL) return node;
    int head = 0, tail = 0;
    q[tail++] = root;
    while (head < tail) {
        Vehicle *cur = q[head++];
        if (cur->left == NULL) { cur->left = node; return root; }
        q[tail++] = cur->left;
        if (cur->right == NULL) { cur->right = node; return root; }
        q[tail++] = cur->right;
    }
    return root;
}

static void show(Vehicle *v) { printf("%d %s %d\n", v->vno, v->model, v->price); }

static void inorder(Vehicle *r)   { if (!r) return; inorder(r->left); show(r); inorder(r->right); }
static void preorder(Vehicle *r)  { if (!r) return; show(r); preorder(r->left); preorder(r->right); }
static void postorder(Vehicle *r) { if (!r) return; postorder(r->left); postorder(r->right); show(r); }

static void levelOrder(Vehicle *root) {
    if (root == NULL) return;
    int head = 0, tail = 0;
    q[tail++] = root;
    while (head < tail) {
        Vehicle *cur = q[head++];
        show(cur);
        if (cur->left) q[tail++] = cur->left;
        if (cur->right) q[tail++] = cur->right;
    }
}

static Vehicle *search(Vehicle *r, int vno) {
    if (r == NULL || r->vno == vno) return r;
    Vehicle *l = search(r->left, vno);
    return l ? l : search(r->right, vno);
}

static void freeTree(Vehicle *r) {
    if (!r) return;
    freeTree(r->left); freeTree(r->right); free(r);
}

int main(void) {
    Vehicle *root = NULL;
    int opt;
    while (scanf("%d", &opt) == 1) {
        if (opt == 1) {
            int vno, price;
            char model[64];
            if (scanf("%d %63s %d", &vno, model, &price) != 3) break;
            root = insertLevelOrder(root, newVehicle(vno, model, price));
        } else if (opt == 2) inorder(root);
        else if (opt == 3) preorder(root);
        else if (opt == 4) postorder(root);
        else if (opt == 5) levelOrder(root);
        else if (opt == 6) {
            int vno;
            if (scanf("%d", &vno) != 1) break;
            Vehicle *v = search(root, vno);
            if (v) show(v); else printf("-1\n");
        } else if (opt == 7) break;
    }
    freeTree(root);
    return 0;
}
"""

S7 = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Vehicle {
    int vno;
    char model[32];
    int price;
    struct Vehicle *left, *right;
} Vehicle;

int main(void) {
    /* TODO: menu loop until option 7.
       Option 1 inserts in LEVEL ORDER (first free child slot found by BFS, left
       before right) - this is NOT a BST, vno does not decide the position. */
    return 0;
}
"""

MODELS = ["RoyalEnfield", "Dizire", "Venue", "Creta", "Swift", "Nexon", "Alto", "City",
          "Verna", "Thar", "Polo", "Baleno", "Innova", "Scorpio", "Kwid"]


def vehicle_script(n_insert, extra_ops):
    vnos = rng.sample(range(100, 251), n_insert + 3)
    lines, inserted = [], []
    for k in range(n_insert):
        lines.append(f"1 {vnos[k]} {rng.choice(MODELS)} {rng.randint(1, 100)}")
        inserted.append(vnos[k])
        if rng.random() < 0.25:
            lines.append(str(rng.randint(2, 5)))
    for _ in range(extra_ops):
        op = rng.randint(2, 6)
        if op == 6:
            pick = rng.choice(inserted) if rng.random() < 0.6 else vnos[-1]
            lines.append(f"6 {pick}")
        else:
            lines.append(str(op))
    lines.append("7")
    return "\n".join(lines) + "\n"


T7 = ["1 105 RoyalEnfield 4\n1 102 Dizire 8\n1 108 Venue 14\n2\n3\n4\n5\n6 108\n6 103\n7\n",
      "2\n5\n6 150\n1 150 Thar 20\n2\n6 150\n7\n"]
T7 += [vehicle_script(rng.randint(3, 9), rng.randint(3, 7)) for _ in range(5)]

write_problem(
    PACK, UNIT, "p07-vehicle-tree", title="PD Lab 10 Q4: vehicle parking tree (level-order insert)",
    mode="program", difficulty="medium", estimated_minutes=25, samples=1,
    topics=["binary tree", "queue", "structs", "menu-driven"],
    prereqs=[f"{PACK}.{UNIT}.p04-level-order"],
    source="NITC_Lab_S2_PD Assignments/Lab10 Assignment-6, Q4 (verbatim; test 1 is the official sample)",
    hints=[
        "Insertion is a BFS: pop nodes in level order; the first one with a NULL "
        "left gets the new node there, else the first with a NULL right. Check left "
        "before right for every node.",
        "Keep the records in the tree nodes themselves: a struct with vno, model, "
        "price, left and right. Read the model with %s - models have no spaces.",
        "search must look in both subtrees (not a BST). Print -1 when not found.",
    ],
    starter=S7, solution=A7, tests=T7,
    statement=r"""
# PD Lab 10 Q4: vehicle parking tree

Verbatim from PD Lab 10: a menu-driven program over a binary tree of vehicle records,
where vehicles are placed in **level order** as they arrive - not by vehicle number.

## Menu

| Option | Meaning | Output |
|---|---|---|
| `1 <Vno> <Vmodel> <Price>` | insert in level order | none |
| `2` | inorder | one record per line |
| `3` | preorder | one record per line |
| `4` | postorder | one record per line |
| `5` | level order | one record per line |
| `6 <Vno>` | search | the record, or `-1` |
| `7` | exit | none |

A record prints as `Vno Vmodel Price`, space separated. `100 <= Vno <= 250`, the model
is a single word of at most 30 characters, `1 <= Price <= 100`.

## Sample

```
1 105 RoyalEnfield 4
1 102 Dizire 8
1 108 Venue 14
2
3
4
5
6 108
6 103
7
```

```
102 Dizire 8
105 RoyalEnfield 4
108 Venue 14
105 RoyalEnfield 4
102 Dizire 8
108 Venue 14
102 Dizire 8
108 Venue 14
105 RoyalEnfield 4
105 RoyalEnfield 4
102 Dizire 8
108 Venue 14
108 Venue 14
-1
```

(The sheet prints the seven menu lines before the sample input; those are the menu,
not input.)

## Level order is not BST order

105 arrives first and becomes the root. 102 goes to the first free slot in level order -
root's left - and 108 to root's right. With a fourth vehicle it would go under 102's
left, **whatever its number**. The inorder output happens to look sorted in the sample
only because of the arrival order; test 3 onward will show you it is not.
""",
)

# --------------------------------------------------------------- p08 views (extra)
H8 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + PROVIDED_DECLS + r"""
#define MAXQ 100005

/* ---- Yours: each prints one line (values followed by a space, then '\n'). ---- */
void leftView(Node *root);    /* first node of every level */
void rightView(Node *root);   /* last node of every level */
void topView(Node *root);     /* first node seen at each horizontal distance,
                                 printed from leftmost column to rightmost */

#endif
"""

M8 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_LINE + r"""
int main(void) {
    Node *root = readTree();
    leftView(root);
    rightView(root);
    topView(root);
    freeTree(root);
    return 0;
}
"""

S8 = r"""
#include <stdio.h>
#include "problem.h"

void leftView(Node *root) {
    /* TODO: level order; print the FIRST node of each level. */
    printf("\n");
}

void rightView(Node *root) {
    /* TODO: level order; print the LAST node of each level. */
    printf("\n");
}

void topView(Node *root) {
    /* TODO: level order, carrying a horizontal distance with each node
       (root 0, left child hd-1, right child hd+1). The first node to reach a
       given hd is the one visible from above. hd ranges over -n..n, so an
       ordinary array indexed by hd + n can record what each column saw. */
    printf("\n");
}
"""

A8 = r"""
#include <stdio.h>
#include "problem.h"

static Node *q[MAXQ];
static int hdq[MAXQ];

static void view(Node *root, int wantLast) {
    int head = 0, tail = 0;
    if (root) q[tail++] = root;
    while (head < tail) {
        int size = tail - head;
        for (int k = 0; k < size; k++) {
            Node *cur = q[head++];
            if ((!wantLast && k == 0) || (wantLast && k == size - 1)) printf("%d ", cur->data);
            if (cur->left) q[tail++] = cur->left;
            if (cur->right) q[tail++] = cur->right;
        }
    }
    printf("\n");
}

void leftView(Node *root)  { view(root, 0); }
void rightView(Node *root) { view(root, 1); }

void topView(Node *root) {
    static int seen[2 * MAXQ + 1], val[2 * MAXQ + 1];
    int head = 0, tail = 0, lo = 0, hi = 0;
    if (root == NULL) { printf("\n"); return; }

    /* horizontal distances fit in [-tail, tail]; offset them to be array indices */
    const int OFF = MAXQ;
    for (int i = 0; i < 2 * MAXQ + 1; i++) seen[i] = 0;

    q[tail] = root; hdq[tail] = 0; tail++;
    while (head < tail) {
        Node *cur = q[head];
        int hd = hdq[head];
        head++;
        if (!seen[hd + OFF]) { seen[hd + OFF] = 1; val[hd + OFF] = cur->data; }
        if (hd < lo) lo = hd;
        if (hd > hi) hi = hd;
        if (cur->left)  { q[tail] = cur->left;  hdq[tail] = hd - 1; tail++; }
        if (cur->right) { q[tail] = cur->right; hdq[tail] = hd + 1; tail++; }
    }
    for (int hd = lo; hd <= hi; hd++) printf("%d ", val[hd + OFF]);
    printf("\n");
}
"""

T8 = ["( 1 ( 2 ( 4 ( ) ( ) ) ( 5 ( ) ( ) ) ) ( 3 ( ) ( 6 ( ) ( ) ) ) )\n",
      "(120(5(25(15)(10))(20(6)(7)))(85(130)(135()(200))))\n", "(7)\n",
      "(1(2()(3()(4()(5))))())\n"]
T8 += [s + "\n" for _, s in tree_inputs(5, sizes=(5, 20))]

write_problem(
    PACK, UNIT, "p08-views", title="Left, right and top views",
    mode="function", difficulty="medium", estimated_minutes=18, samples=2, tier="extra",
    topics=["binary tree", "bfs", "queue"],
    prereqs=[f"{PACK}.{UNIT}.p04-level-order"],
    source="PD Lab 10 (tree views)",
    hints=[
        "Left and right view are level order with the per-level size loop: print "
        "when k == 0 (left) or k == size - 1 (right).",
        "Top view needs a horizontal distance per node. Keep a parallel int queue "
        "hdq[] next to the Node* queue so they move together.",
        "hd is between -n and n. Index an array with hd + OFFSET instead of using a "
        "map, and track the smallest and largest hd seen for the final print loop.",
    ],
    header=H8, harness=M8, starter=S8, solution=A8, tests=T8,
    extra={"parse.c": PARSER},
    statement=r"""
# Left, right and top views

*Optional variation.* Three views of the same tree, all built on level order.

- **Left view**: the first node of each level.
- **Right view**: the last node of each level.
- **Top view**: looking down from above. Give the root horizontal distance 0, a left
  child `hd - 1` and a right child `hd + 1`. For each distance, the node seen from above
  is the first one a level-order traversal reaches. Print from the leftmost column.

Each function prints one line.
""" + NOTATION + r"""
## Example

```
( 1 ( 2 ( 4 ( ) ( ) ) ( 5 ( ) ( ) ) ) ( 3 ( ) ( 6 ( ) ( ) ) ) )
```

```
1 2 4
1 3 6
4 2 1 3 6
```

## Storing one value per column

`hd` is always between `-n` and `n`, so an ordinary array indexed by `hd + n` holds the
first value seen in each column. Remember the smallest and largest `hd` you saw so you
know where to start and stop printing.
""",
)

# --------------------------------------------------------------- p09 build from traversals (extra)
H9 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + r"""
/* ---- Provided. ---- */
Node *newNode(int value);
void  freeTree(Node *root);

/* ---- Yours: rebuild the tree from its preorder and inorder sequences
        (all values distinct), and return the root. ---- */
Node *buildFromPreIn(int pre[], int in[], int n);

#endif
"""

M9 = r"""
#include <stdio.h>
#include "problem.h"

static void post(Node *r) { if (!r) return; post(r->left); post(r->right); printf("%d ", r->data); }

int main(void) {
    int n;
    static int pre[10005], in[10005];
    if (scanf("%d", &n) != 1) return 0;
    for (int i = 0; i < n; i++) scanf("%d", &pre[i]);
    for (int i = 0; i < n; i++) scanf("%d", &in[i]);
    Node *root = buildFromPreIn(pre, in, n);
    post(root);
    printf("\n");
    freeTree(root);
    return 0;
}
"""

S9 = r"""
#include "problem.h"

Node *buildFromPreIn(int pre[], int in[], int n) {
    /* TODO
       pre[0] is the root. Find it in in[] at position k:
         in[0..k-1]   is the left subtree  (k nodes)
         in[k+1..n-1] is the right subtree (n-k-1 nodes)
       and in pre[] the left subtree is pre[1..k], the right is pre[k+1..n-1].
       Pointer arithmetic lets you recurse on sub-arrays: pre + 1, in + k + 1 ... */
    return 0;
}
"""

A9 = r"""
#include "problem.h"

Node *buildFromPreIn(int pre[], int in[], int n) {
    if (n <= 0) return NULL;
    Node *root = newNode(pre[0]);
    int k = 0;
    while (in[k] != pre[0]) k++;          /* root's position in inorder */
    root->left = buildFromPreIn(pre + 1, in, k);
    root->right = buildFromPreIn(pre + 1 + k, in + k + 1, n - k - 1);
    return root;
}
"""

from _trees import preorder as _pre, inorder as _in  # noqa: E402

T9 = ["7\n1 2 4 5 3 6 7\n4 2 5 1 6 3 7\n", "1\n9\n9\n", "4\n1 2 3 4\n4 3 2 1\n", "4\n1 2 3 4\n1 2 3 4\n"]
for _ in range(5):
    t = random_tree(rng, rng.randint(5, 25), values=rng.sample(range(1, 500), 25)[:25])
    p, i = _pre(t), _in(t)
    T9.append(f"{len(p)}\n{' '.join(map(str, p))}\n{' '.join(map(str, i))}\n")

write_problem(
    PACK, UNIT, "p09-build-from-traversals", title="Rebuild a tree from preorder + inorder",
    mode="function", difficulty="hard", estimated_minutes=15, samples=1, tier="extra",
    topics=["binary tree", "recursion", "divide and conquer"],
    prereqs=[f"{PACK}.{UNIT}.p01-traversals"],
    source="PD Lab 10 Q5 options (e)/(f), integer version",
    hints=[
        "The first element of preorder is always the root of the current subtree.",
        "Everything left of the root in inorder is the left subtree, so its size k "
        "tells you how many of the following preorder elements belong to the left.",
        "Recurse on sub-arrays with pointer arithmetic: left is (pre + 1, in, k), "
        "right is (pre + 1 + k, in + k + 1, n - k - 1).",
    ],
    header=H9, harness=M9, starter=S9, solution=A9, tests=T9,
    extra={"node.c": PROVIDED_NODE},
    statement=r"""
# Rebuild a tree from preorder + inorder

*Optional variation.* Given the preorder and inorder sequences of a tree with distinct
values, rebuild it. The hidden `main()` prints the postorder of what you built.

## Input

`n`, then the preorder sequence, then the inorder sequence.

## Example

```
7
1 2 4 5 3 6 7
4 2 5 1 6 3 7
```

```
4 5 2 6 7 3 1
```

## The idea in one sentence

Preorder tells you **who the root is** (its first element); inorder tells you **how
the rest splits** (everything left of the root is the left subtree). Recurse on both
halves.

In C you do not need to copy sub-arrays: `pre + 1` is a pointer to the rest of the
preorder array, and a recursive call on `(pre + 1, in, k)` sees exactly the left
subtree's slice.
""",
)

# --------------------------------------------------------------- p10 LCA (extra)
H10 = "#ifndef PROBLEM_H\n#define PROBLEM_H\n" + NODE + PROVIDED_DECLS + r"""
/* ---- Yours: lowest common ancestor of the nodes holding a and b.
        Both are guaranteed to be in the tree; a node is its own ancestor. ---- */
Node *lca(Node *root, int a, int b);

#endif
"""

M10 = r"""
#include <stdio.h>
#include "problem.h"
""" + READ_LINE + r"""
int main(void) {
    Node *root = readTree();
    int q;
    if (scanf("%d", &q) != 1) return 0;
    while (q--) {
        int a, b;
        if (scanf("%d %d", &a, &b) != 2) break;
        Node *r = lca(root, a, b);
        printf("%d\n", r ? r->data : -1);
    }
    freeTree(root);
    return 0;
}
"""

S10 = r"""
#include "problem.h"

Node *lca(Node *root, int a, int b) {
    /* TODO
       - NULL, or root holds a or b  -> return root
       - ask both subtrees
       - both answers non-NULL -> a and b are on different sides: root is the LCA
       - otherwise return whichever answer is non-NULL */
    return 0;
}
"""

A10 = r"""
#include "problem.h"

Node *lca(Node *root, int a, int b) {
    if (root == NULL || root->data == a || root->data == b) return root;
    Node *l = lca(root->left, a, b);
    Node *r = lca(root->right, a, b);
    if (l && r) return root;
    return l ? l : r;
}
"""

T10 = ["( 3 ( 5 ( 6 ( ) ( ) ) ( 2 ( 7 ( ) ( ) ) ( 4 ( ) ( ) ) ) ) ( 1 ( 0 ( ) ( ) ) ( 8 ( ) ( ) ) ) )\n4\n5 1\n5 4\n7 4\n6 8\n"]
for _ in range(5):
    t = random_tree(rng, rng.randint(4, 20))
    vals = _pre(t)
    qs = [f"{rng.choice(vals)} {rng.choice(vals)}" for _ in range(5)]
    T10.append(spaced(t) + "\n5\n" + "\n".join(qs) + "\n")

write_problem(
    PACK, UNIT, "p10-lca", title="Lowest common ancestor",
    mode="function", difficulty="medium", estimated_minutes=12, samples=1, tier="extra",
    topics=["binary tree", "recursion"],
    prereqs=[f"{PACK}.{UNIT}.p03-height-size-leaves"],
    source="Standard binary-tree variation",
    hints=[
        "Return a pointer up the recursion: 'I found a or b in my subtree, here it is'.",
        "If both the left and the right call report something, the two targets are "
        "on opposite sides - the current node is where their paths split.",
    ],
    header=H10, harness=M10, starter=S10, solution=A10, tests=T10,
    extra={"parse.c": PARSER},
    statement=r"""
# Lowest common ancestor

*Optional variation.* The lowest node that has both `a` and `b` in its subtree (a node
counts as its own ancestor).

## Input

The tree line, then `q`, then `q` lines `a b`. Print one LCA value per query.

## Example

```
( 3 ( 5 ( 6 ( ) ( ) ) ( 2 ( 7 ( ) ( ) ) ( 4 ( ) ( ) ) ) ) ( 1 ( 0 ( ) ( ) ) ( 8 ( ) ( ) ) ) )
4
5 1
5 4
7 4
6 8
```

```
3
5
2
3
```

## The recursion

Each call returns "whichever of `a` / `b` I found in my subtree", or `NULL`. If both
children report something, the targets are on different sides and **this** node is the
LCA. If only one does, pass it upward. In a BST (next unit) there is a faster version
that uses the ordering instead of searching both sides.
""",
)

report(UNIT, 10)
