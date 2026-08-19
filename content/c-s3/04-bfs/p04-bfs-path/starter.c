#include "problem.h"

int bfsPath(const Graph *g, int s, int t, int path[]) {
    int parent[MAXV];
    /* TODO
       1. BFS from s, recording parent[v] = the vertex you discovered v from.
          Use parent[s] = -1 (or 0) as the stop marker.
       2. if t was never discovered, return 0
       3. walk backwards from t via parent[] - that gives the path REVERSED -
          then reverse it into path[] so it reads s .. t
       4. return the number of vertices written */
    (void)parent;
    return 0;
}
