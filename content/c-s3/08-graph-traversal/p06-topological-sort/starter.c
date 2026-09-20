#include "problem.h"

int topoSort(const Graph *g, int order[]) {
    int indeg[MAXV] = {0}, used[MAXV] = {0}, count = 0;

    /* TODO - Kahn's algorithm
       1. indeg[v] = number of edges pointing INTO v
       2. repeat n times:
            pick the SMALLEST-numbered vertex with indeg 0 that is not used yet
            if there is none -> the rest is a cycle, return 0
            append it to order[], mark it used, and decrement indeg[] of each of
            its out-neighbours
       Picking the smallest available vertex each round is what makes the result
       lexicographically smallest. n <= 100, so a linear scan is fine. */
    return 0;
}
