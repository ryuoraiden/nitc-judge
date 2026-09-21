"""Pack-level settings for c-s3: the title and the Test 1 study path.

Run after the unit scripts: python scripts/authoring/pack_c_s3.py

The essentials are the problems to do before the test, in the order to do them:
graphs first (weakest area first within them), then trees. Everything else in the
pack is practice or an optional variation.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _authoring import write_pack

ESSENTIALS = [
    # BFS shortest paths - Practice Q1
    "c-s3.04-bfs.p05-lex-smallest-paths",
    "c-s3.04-bfs.p06-practice-q1",
    # Dijkstra - Practice Q2 and the MQ4 modification question
    "c-s3.05-dijkstra.p01-dijkstra-matrix",
    "c-s3.05-dijkstra.p03-practice-q2",
    "c-s3.10-graph-variations.p01-dijkstra-spt-matrix",
    # negative weights and all-pairs
    "c-s3.05-dijkstra.p05-negative-cycle",
    "c-s3.10-graph-variations.p03-bellman-ford",
    "c-s3.10-graph-variations.p04-floyd-warshall",
    # MST - Week 5 and its modification
    "c-s3.09-mst.p01-disjoint-set",
    "c-s3.09-mst.p04-week5-q1-prim",
    "c-s3.09-mst.p05-week5-q2-kruskal",
    "c-s3.10-graph-variations.p05-prim-blocked-steps",
    # DFS - Week 3 and its evaluation question
    "c-s3.08-graph-traversal.p02-dfs-iterative",
    "c-s3.08-graph-traversal.p08-bipartite-program",
    # binary trees - the notation and PD Lab 10
    "c-s3.06-binary-tree.p02-parse-notation",
    "c-s3.06-binary-tree.p05-depth-k-subtree",
    "c-s3.06-binary-tree.p06-postorder-notation",
    # BSTs - deletion, PD Lab 12 full programs, the Week 2 modification
    "c-s3.07-bst.p03-delete-transplant",
    "c-s3.07-bst.p05-lab12-q1-menu",
    "c-s3.07-bst.p06-lab12-q2-kth",
    "c-s3.07-bst.p07-lab12-q4-subtree",
    "c-s3.11-tree-variations.p01-delete-by-rank",
]

write_pack(
    "c-s3",
    title="NITC DSA - Test 1 prep",
    description=("Stack, queue and heap, then BFS/DFS, shortest paths, MST, binary trees "
                 "and BSTs. Official lab questions use their sheet's wording and sample; "
                 "reconstructed ones say so at the top of the statement."),
    essentials=ESSENTIALS,
)
print(f"  c-s3 pack: {len(ESSENTIALS)} essentials")
