"""Differential testing for the c-s3 references.

Two claims in this pack are strong enough to deserve empirical proof rather than
an argument in a statement:

  1. plain BFS over sorted adjacency lists already yields the lexicographically
     smallest shortest path (checked against brute-force enumeration)
  2. the O(V^2) Dijkstra and the heap Dijkstra agree (independent implementations)

    python scripts/fuzz_check.py [trials]
"""
from __future__ import annotations

import random
import subprocess
import sys
from collections import deque
from itertools import count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from judge.loader import Content
from judge.runner_c import _sources_for, _compile
from judge.sandbox import Workspace, run

INF = 10 ** 9


class Built:
    """A compiled reference solution kept alive across many trials."""

    def __init__(self, problem):
        self.ws = Workspace("fuzz")
        sources = _sources_for(problem, self.ws, problem.solution)
        comp = _compile(problem, self.ws, sources)
        if comp.exit_code != 0:
            raise SystemExit(f"{problem.id} did not compile:\n{comp.stderr}")
        self.exe = str(self.ws.path / "prog.exe")

    def __call__(self, stdin: str) -> str:
        r = run([self.exe], self.ws.path, stdin_data=stdin, timeout_ms=5000)
        return r.stdout.replace("\r\n", "\n").strip()


# ----------------------------------------------------------------- brute force
def brute_lex_paths(n, adj, s):
    """Shortest paths by BFS level, choosing the lexicographically smallest by
    explicit enumeration over every shortest path.  Deliberately naive."""
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)

    # best[v] = lexicographically smallest shortest path to v, as a tuple
    best = {s: (s,)}
    for level in range(1, max(dist.values(), default=0) + 1):
        for v in sorted(k for k, d in dist.items() if d == level):
            candidates = []
            for u in range(1, n + 1):
                if dist.get(u) == level - 1 and v in adj[u] and u in best:
                    candidates.append(best[u] + (v,))
            if candidates:
                best[v] = min(candidates)

    out = []
    for v in range(1, n + 1):
        out.append("-".join(str(x) for x in best[v]) if v in best else "-1")
    return "\n".join(out)


def brute_dijkstra(n, w):
    """Plain O(V^2) Dijkstra in Python, written independently of the C code."""
    def solve(src):
        dist = [INF] * n
        done = [False] * n
        dist[src] = 0
        for _ in range(n):
            u = -1
            for i in range(n):
                if not done[i] and (u == -1 or dist[i] < dist[u]):
                    u = i
            if u == -1 or dist[u] == INF:
                break
            done[u] = True
            for v in range(n):
                if u != v and w[u][v] != 999 and dist[u] + w[u][v] < dist[v]:
                    dist[v] = dist[u] + w[u][v]
        return dist
    return solve


# ----------------------------------------------------------------- generators
def random_digraph(rng, n_range=(2, 7), density=0.4):
    n = rng.randint(*n_range)
    adj = {u: set() for u in range(1, n + 1)}
    for u in range(1, n + 1):
        for v in range(1, n + 1):
            if u != v and rng.random() < density:
                adj[u].add(v)
    return n, adj


def random_weighted(rng, n_range=(2, 7), density=0.45, wmax=20):
    n = rng.randint(*n_range)
    w = [[999] * n for _ in range(n)]
    for i in range(n):
        w[i][i] = 0
    for u in range(n):
        for v in range(n):
            if u != v and rng.random() < density:
                w[u][v] = rng.randint(0, wmax)
    return n, w


# ----------------------------------------------------------------- checks
def check_lex_paths(trials, rng):
    content = Content()
    problem = content.get("c-s3.04-bfs.p06-practice-q1")
    ref = Built(problem)
    bad = 0
    for t in range(trials):
        n, adj = random_digraph(rng)
        s = rng.randint(1, n)
        lines = [str(n)]
        for u in range(1, n + 1):
            nbrs = list(adj[u])
            rng.shuffle(nbrs)                     # unsorted on purpose
            lines.append(" ".join(str(x) for x in [u] + nbrs))
        lines.append(str(s))
        stdin = "\n".join(lines) + "\n"

        got = ref(stdin)
        want = brute_lex_paths(n, adj, s)
        if got != want:
            bad += 1
            print(f"  MISMATCH on trial {t}\n--- input\n{stdin}--- reference\n{got}\n--- brute force\n{want}")
            if bad >= 3:
                break
    return bad


def check_dijkstra(trials, rng):
    content = Content()
    matrix = Built(content.get("c-s3.05-dijkstra.p01-dijkstra-matrix"))
    heap = Built(content.get("c-s3.05-dijkstra.p04-dijkstra-heap"))
    bad = 0
    for t in range(trials):
        n, w = random_weighted(rng)
        src = rng.randint(1, n)

        matrix_in = f"{n}\n" + "\n".join(" ".join(str(x) for x in row) for row in w) + f"\n{src}\n"
        got_matrix = matrix(matrix_in)

        edges = [(u + 1, v + 1, w[u][v]) for u in range(n) for v in range(n)
                 if u != v and w[u][v] != 999]
        heap_in = (f"{n} {len(edges)}\n" +
                   "".join(f"{u} {v} {c}\n" for u, v, c in edges) + f"{src}\n")
        got_heap = heap(heap_in)

        py = brute_dijkstra(n, w)(src - 1)
        want = " ".join(str(-1 if d >= INF else d) for d in py)

        if not (got_matrix == got_heap == want):
            bad += 1
            print(f"  MISMATCH on trial {t}\n--- matrix\n{matrix_in}"
                  f"matrix={got_matrix}\nheap  ={got_heap}\npython={want}")
            if bad >= 3:
                break
    return bad


def main(argv):
    trials = int(argv[0]) if argv else 300
    rng = random.Random(20260819)

    print(f"lex-smallest shortest paths vs brute force ({trials} random digraphs)")
    bad1 = check_lex_paths(trials, rng)
    print(f"  -> {trials - bad1}/{trials} agree\n")

    print(f"Dijkstra: O(V^2) vs heap vs independent Python ({trials} random weighted graphs)")
    bad2 = check_dijkstra(trials, rng)
    print(f"  -> {trials - bad2}/{trials} agree")

    return 1 if (bad1 or bad2) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
