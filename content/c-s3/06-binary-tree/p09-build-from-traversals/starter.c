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
