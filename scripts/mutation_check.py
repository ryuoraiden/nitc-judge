"""Mutation testing: do the tests actually reject wrong solutions?

fuzz_check*.py prove the reference solutions are right.  This proves the TESTS are
strong: each entry below is a realistic wrong solution (the mistake a student
actually makes), built by editing the reference.  Every one must fail at least one
test.  A mutant that scores AC means a student could make that mistake and be told
they are correct.

    python scripts/mutation_check.py [problem_id_substring ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from judge.loader import Content
from judge.runner_c import judge

WRONG_LEX = r"""
#include "problem.h"
/* Wrong: parent = the SMALLEST-numbered predecessor one level up. That is not
   the same as the lexicographically smallest complete path. */
void lexShortestPaths(const Graph *g, int s, int parent[]) {
    int dist[MAXV], q[MAXV], h = 0, t = 0;
    for (int v = 0; v <= g->n; v++) dist[v] = -1;
    dist[s] = 0; q[t++] = s;
    while (h < t) { int u = q[h++];
        for (int i = 0; i < g->deg[u]; i++) { int v = g->adj[u][i];
            if (dist[v] == -1) { dist[v] = dist[u] + 1; q[t++] = v; } } }
    for (int v = 1; v <= g->n; v++) parent[v] = -1;
    for (int u = g->n; u >= 1; u--)
        for (int i = 0; i < g->deg[u]; i++) { int v = g->adj[u][i];
            if (v != s && dist[u] >= 0 && dist[v] == dist[u] + 1) parent[v] = u; }
}
"""

# (problem id, what the student got wrong, edits to the reference | full source)
MUTANTS = [
    # ---------------------------------------------------------------- BFS / Q1
    ("c-s3.04-bfs.p05-lex-smallest-paths", "smallest predecessor instead of lex-smallest path", WRONG_LEX),
    ("c-s3.04-bfs.p05-lex-smallest-paths", "neighbours visited largest-first",
     [("for (int i = 0; i < g->deg[u]; i++) {\n            int v = g->adj[u][i];\n            if (!seen[v]) {",
       "for (int i = g->deg[u] - 1; i >= 0; i--) {\n            int v = g->adj[u][i];\n            if (!seen[v]) {")]),
    ("c-s3.04-bfs.p06-practice-q1", "forgot to sort each adjacency line",
     [("qsort(adj[u], deg[u], sizeof(int), cmpInt);", "")]),
    ("c-s3.04-bfs.p06-practice-q1", "neighbours visited largest-first",
     [("for (int i = 0; i < deg[u]; i++) {\n            int v = adj[u][i];",
       "for (int i = deg[u] - 1; i >= 0; i--) {\n            int v = adj[u][i];")]),

    # ---------------------------------------------------------------- Dijkstra / Q2
    ("c-s3.05-dijkstra.p01-dijkstra-matrix", "treats 999 as a real road",
     [("if (w[u][v] == NOEDGE || u == v) continue;", "if (u == v) continue;")]),
    ("c-s3.05-dijkstra.p01-dijkstra-matrix", "never marks vertices done (re-picks the same one)",
     [("done[u] = 1;", "")]),
    ("c-s3.05-dijkstra.p03-practice-q2", "sums the distances instead of taking the max",
     [("if (dist[v] > worst) worst = dist[v];", "worst += dist[v];")]),
    ("c-s3.05-dijkstra.p03-practice-q2", "forgot k is 1-based",
     [("    k--;                                  /* the sheet numbers locations from 1 */\n", "")]),
    ("c-s3.05-dijkstra.p03-practice-q2", "treats 999 as a real road",
     [("if (u == v || w[u][v] == NOEDGE) continue;", "if (u == v) continue;")]),

    # ---------------------------------------------------------------- MQ4 SPT
    ("c-s3.10-graph-variations.p01-dijkstra-spt-matrix", "writes tree edges in both directions (MST habit)",
     [("tree[parent[v]][v] = w[parent[v]][v];",
       "tree[parent[v]][v] = tree[v][parent[v]] = w[parent[v]][v];")]),
    ("c-s3.10-graph-variations.p01-dijkstra-spt-matrix", "counts the depot as a leaf when it has one child",
     [("if (v != s && children[v] == 0) leaves++;",
       "if ((v != s && children[v] == 0) || (v == s && children[v] == 1)) leaves++;")]),
    ("c-s3.10-graph-variations.p01-dijkstra-spt-matrix", "treats a 0 off the diagonal as 'no road'",
     [("if (u == v || w[u][v] == NOEDGE) continue;", "if (u == v || w[u][v] == NOEDGE || w[u][v] == 0) continue;")]),
    ("c-s3.10-graph-variations.p01-dijkstra-spt-matrix", "forgot the leaf-count line",
     [('    printf("%d\\n", leaves);\n', "")]),

    # ---------------------------------------------------------------- negative weights
    ("c-s3.05-dijkstra.p05-negative-cycle", "one relaxation pass too few",
     [("for (int pass = 0; pass < n - 1; pass++) {", "for (int pass = 0; pass < n - 2; pass++) {")]),
    # Needs the INF guard too: without it, "infinity" itself drifts down through
    # the unreachable cycle and the mistake gets caught by accident.
    ("c-s3.05-dijkstra.p05-negative-cycle", "only looks for cycles reachable from vertex 1",
     [("for (int i = 0; i < n; i++) dist[i] = 0;",
       "for (int i = 0; i < n; i++) dist[i] = (i == 0) ? 0 : 1000000000;"),
      ("if (u == v || w[u][v] == NOEDGE) continue;",
       "if (u == v || w[u][v] == NOEDGE || dist[u] >= 1000000000) continue;", 2)]),
    ("c-s3.10-graph-variations.p03-bellman-ford", "no INF guard (relaxes from unreachable vertices)",
     [("            if (dist[eu[i]] == INF) continue;          /* never relax from \"infinity\" */\n", "")]),
    ("c-s3.10-graph-variations.p03-bellman-ford", "prints -1 for unreachable instead of INF",
     [('if (dist[v] == INF) printf("INF");', 'if (dist[v] == INF) printf("-1");')]),
    ("c-s3.10-graph-variations.p04-floyd-warshall", "k as the INNER loop",
     [("    for (int k = 1; k <= n; k++)\n        for (int i = 1; i <= n; i++)\n            for (int j = 1; j <= n; j++) {",
       "    for (int i = 1; i <= n; i++)\n        for (int j = 1; j <= n; j++)\n            for (int k = 1; k <= n; k++) {")]),
    ("c-s3.10-graph-variations.p04-floyd-warshall", "no INF guard",
     [("                if (d[i][k] == INF || d[k][j] == INF) continue;\n", "")]),

    # ---------------------------------------------------------------- MST
    ("c-s3.09-mst.p01-disjoint-set", "unite links the vertices, not their roots",
     [("int ra = find(d, a), rb = find(d, b);\n    if (ra == rb) return 0;",
       "int ra = a, rb = b;\n    if (find(d, a) == find(d, b)) return 0;")]),
    ("c-s3.09-mst.p04-week5-q1-prim", "Dijkstra-style key (distance from s, not one edge)",
     [("if (w[u][v] < key[v]) { key[v] = w[u][v]; parent[v] = u; }",
       "if (key[u] + w[u][v] < key[v]) { key[v] = key[u] + w[u][v]; parent[v] = u; }")]),
    ("c-s3.09-mst.p04-week5-q1-prim", "writes each tree edge in one direction only",
     [("tree[u][v] = tree[v][u] = w[u][v];", "tree[u][v] = w[u][v];")]),
    ("c-s3.09-mst.p05-week5-q2-kruskal", "does not print the finished tree a second time",
     [("    printTree();                       /* the finished tree again */\n", "")]),
    ("c-s3.09-mst.p05-week5-q2-kruskal", "prints snapshots before discovering the graph is disconnected",
     [("    if (taken != n - 1) { printf(\"-1\\n\"); return 0; }\n\n    /* Pass 2",
       "    /* Pass 2"),
      ("    printTree();                       /* the finished tree again */\n",
       "    if (taken != n - 1) { printf(\"-1\\n\"); return 0; }\n    printTree();\n")]),
    ("c-s3.10-graph-variations.p05-prim-blocked-steps", "ignores the blocked edges",
     [("        w[u][v] = w[v][u] = 0;                  /* blocked == the edge does not exist */\n", "")]),
    ("c-s3.10-graph-variations.p05-prim-blocked-steps", "prints a snapshot for the source too",
     [("        if (parent[u] != -1) {                  /* s itself adds no edge */",
       "        if (print && parent[u] == -1) printTree();\n        if (parent[u] != -1) {")]),

    # ---------------------------------------------------------------- DFS / bipartite
    ("c-s3.08-graph-traversal.p02-dfs-iterative", "pushes neighbours ascending",
     [("for (int i = g->deg[u] - 1; i >= 0; i--) {", "for (int i = 0; i < g->deg[u]; i++) {")]),
    ("c-s3.08-graph-traversal.p02-dfs-iterative", "marks on push instead of on pop",
     [("        if (visited[u]) continue;      /* a duplicate push from another neighbour */\n        visited[u] = 1;\n", ""),
      ("            if (!visited[v]) stack[++top] = v;", "            if (!visited[v]) { visited[v] = 1; stack[++top] = v; }"),
      ("    stack[++top] = s;\n", "    stack[++top] = s;\n    visited[s] = 1;\n")]),
    ("c-s3.08-graph-traversal.p08-bipartite-program", "only colours the component of vertex 1",
     [("    for (int s = 1; s <= n; s++) {\n        if (colour[s] != -1) continue;",
       "    for (int s = 1; s <= 1; s++) {\n        if (colour[s] != -1) continue;")]),

    # ---------------------------------------------------------------- binary trees
    ("c-s3.06-binary-tree.p02-parse-notation", "reads one digit per value",
     [("while (isdigit((unsigned char)s[*i])) value = value * 10 + (s[(*i)++] - '0');",
       "if (isdigit((unsigned char)s[*i])) value = s[(*i)++] - '0';")]),
    ("c-s3.06-binary-tree.p05-depth-k-subtree", "only searches the left subtree for x",
     [("return l ? l : findNode(root->right, x);", "return l;")]),
    ("c-s3.06-binary-tree.p05-depth-k-subtree", "prints right before left",
     [("    printAtDepth(root->left, k - 1, first);\n    printAtDepth(root->right, k - 1, first);",
       "    printAtDepth(root->right, k - 1, first);\n    printAtDepth(root->left, k - 1, first);")]),
    ("c-s3.06-binary-tree.p06-postorder-notation", "fixed 1000-byte input buffer",
     [("static char s[200005];", "static char s[1000];"), ('scanf("%200000s", s)', 'scanf("%999s", s)')]),

    # ---------------------------------------------------------------- BST
    ("c-s3.07-bst.p03-delete-transplant", "always lifts the successor (no y->parent != x check)",
     [("if (y->parent != x) {", "if (1) {")]),
    ("c-s3.07-bst.p05-lab12-q1-menu", "predecessor instead of successor for two children",
     [("        Node *succ = root->right;\n        while (succ->left != NULL) succ = succ->left;\n        root->key = succ->key;                        /* copy the successor up... */\n        root->right = DeleteKey(root->right, succ->key);  /* ...then delete it below */",
       "        Node *pred = root->left;\n        while (pred->right != NULL) pred = pred->right;\n        root->key = pred->key;\n        root->left = DeleteKey(root->left, pred->key);")]),
    ("c-s3.07-bst.p05-lab12-q1-menu", "prints nothing for an empty tree",
     [('else if (c == \'p\') { if (!root) printf("NULL"); Inorder(root);', "else if (c == 'p') { Inorder(root);")]),
    ("c-s3.07-bst.p06-lab12-q2-kth", "k-th smallest off by one",
     [("if (++(*count) == k) { printf", "if ((*count)++ == k) { printf")]),
    ("c-s3.07-bst.p06-lab12-q2-kth", "successor only looks in the right subtree",
     [("        if (num < root->key) { best = root; root = root->left; }\n        else root = root->right;",
       "        if (num < root->key) root = root->left;\n        else if (num > root->key) root = root->right;\n        else { Node *r = root->right; while (r && r->left) r = r->left; best = r; break; }")]),
    ("c-s3.07-bst.p07-lab12-q4-subtree", "compares only the root keys",
     [("return a->key == b->key && identical(a->left, b->left) && identical(a->right, b->right);",
       "return a->key == b->key;")]),
    ("c-s3.07-bst.p07-lab12-q4-subtree", "checks keys are present, not the shape",
     [("return a->key == b->key && identical(a->left, b->left) && identical(a->right, b->right);",
       "return a->key == b->key && (a->left == NULL || identical(a->left, b->left)) && (a->right == NULL || identical(a->right, b->right));")]),
    ("c-s3.11-tree-variations.p01-delete-by-rank", "rank off by one (0-based k)",
     [("if (++(*count) == k) return T;", "if ((*count)++ == k) return T;")]),
    ("c-s3.11-tree-variations.p01-delete-by-rank", "always lifts the successor",
     [("if (y->parent != x) {", "if (1) {")]),
]


# Deliberately NOT listed - equivalent mutants, which no valid test can kill:
#  - MQ4 "count the root as a leaf": the sheet guarantees n >= 2 and everything
#    reachable, so the root always has a child and is never counted anyway.
#  - bipartite "count blank lines as vertices": that only drops trailing vertex
#    lines, and every edge is also listed in the other endpoint's line.


def build(problem, edits):
    if isinstance(edits, str):
        return edits
    src = problem.solution
    for edit in edits:
        old, new = edit[0], edit[1]
        expected = edit[2] if len(edit) > 2 else 1
        if src.count(old) != expected:
            raise ValueError(f"anchor found {src.count(old)}x, expected {expected}x "
                             f"in {problem.id}: {old[:60]!r}")
        src = src.replace(old, new)
    return src


def main(argv):
    content = Content()
    mutants = [m for m in MUTANTS if not argv or any(a in m[0] for a in argv)]
    killed = survived = 0
    for pid, label, edits in mutants:
        problem = content.get(pid)
        if problem is None:
            print(f"  ??? unknown problem {pid}")
            survived += 1
            continue
        result = judge(problem, build(problem, edits))
        if result.verdict == "AC":
            survived += 1
            print(f"  SURVIVED  {pid.split('.', 1)[1]:<44} {label}")
        else:
            killed += 1
            print(f"  killed    {pid.split('.', 1)[1]:<44} {label}  [{result.verdict}]")
    print(f"\n{killed} killed, {survived} survived, of {len(mutants)} mutants")
    return 1 if survived else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
