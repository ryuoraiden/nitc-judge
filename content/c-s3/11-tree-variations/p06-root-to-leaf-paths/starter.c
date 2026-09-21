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
