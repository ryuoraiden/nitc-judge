#ifndef PROBLEM_H
#define PROBLEM_H

#define MAXV 105

/* Disjoint-set forest over 1..n. */
typedef struct {
    int parent[MAXV];
    int rank[MAXV];
} DSU;

void dsuInit(DSU *d, int n);
int  find(DSU *d, int x);            /* representative of x's set, with path compression */
int  unite(DSU *d, int a, int b);    /* 1 if they were separate and got merged, 0 if already together */

#endif
