"""Differential tests for units 10 and 11 against independent Python models.

    python scripts/fuzz_check3.py [trials]
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "authoring"))

from judge.loader import Content
from judge.runner_c import _compile, _sources_for
from judge.sandbox import Workspace, run
from _trees import random_tree, spaced, T

INF = 10 ** 9


class Built:
    def __init__(self, problem):
        self.ws = Workspace("fuzz3")
        comp = _compile(problem, self.ws, _sources_for(problem, self.ws, problem.solution))
        if comp.exit_code != 0:
            raise SystemExit(f"{problem.id} did not compile:\n{comp.stderr}")
        self.exe = str(self.ws.path / "prog.exe")

    def __call__(self, stdin):
        r = run([self.exe], self.ws.path, stdin_data=stdin, timeout_ms=5000)
        text = r.stdout.replace("\r\n", "\n")
        return "\n".join(line.rstrip() for line in text.split("\n")).strip()


def rand_digraph(rng, lo, hi, dens=0.4, nmax=7):
    n = rng.randint(2, nmax)
    w = {(u, v): rng.randint(lo, hi) for u in range(1, n + 1) for v in range(1, n + 1)
         if u != v and rng.random() < dens}
    return n, w


# ------------------------------------------------------------ python models
def py_floyd(n, w):
    d = [[0 if i == j else w.get((i, j), INF) for j in range(n + 1)] for i in range(n + 1)]
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if d[i][k] < INF and d[k][j] < INF and d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d


def py_bellman(n, w, s):
    dist = [INF] * (n + 1)
    dist[s] = 0
    for _ in range(n - 1):
        for (u, v), c in w.items():
            if dist[u] < INF and dist[u] + c < dist[v]:
                dist[v] = dist[u] + c
    for (u, v), c in w.items():
        if dist[u] < INF and dist[u] + c < dist[v]:
            return None
    return dist


def py_kruskal(n, edges):
    parent = list(range(n + 1))

    def f(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    cost = taken = 0
    for u, v, c in sorted(edges, key=lambda e: e[2]):
        a, b = f(u), f(v)
        if a != b:
            parent[a] = b
            cost += c
            taken += 1
    return cost if taken == n - 1 else -1


# ------------------------------------------------------------ checks
def check_floyd(rng, c, trials):
    fw = Built(c.get("c-s3.10-graph-variations.p04-floyd-warshall"))
    bad = 0
    for _ in range(trials):
        n, w = rand_digraph(rng, -4, 15, 0.35)
        text = f"{n}\n" + "\n".join(" ".join(str(0 if i == j else w.get((i, j), 999))
                                              for j in range(1, n + 1)) for i in range(1, n + 1)) + "\n"
        d = py_floyd(n, w)
        if any(d[i][i] < 0 for i in range(1, n + 1)):
            want = "NEGATIVE CYCLE"
        else:
            want = "\n".join(" ".join("INF" if d[i][j] >= INF else str(d[i][j])
                                      for j in range(1, n + 1)) for i in range(1, n + 1))
        if fw(text) != want:
            bad += 1
    return bad


def check_bellman(rng, c, trials):
    bf = Built(c.get("c-s3.10-graph-variations.p03-bellman-ford"))
    bad = 0
    for _ in range(trials):
        n, w = rand_digraph(rng, -4, 15, 0.35)
        s = rng.randint(1, n)
        text = f"{n} {len(w)} {s}\n" + "".join(f"{u} {v} {x}\n" for (u, v), x in w.items())
        dist = py_bellman(n, w, s)
        want = "NEGATIVE CYCLE" if dist is None else \
            " ".join("INF" if x >= INF else str(x) for x in dist[1:])
        if bf(text) != want:
            bad += 1
    return bad


def check_count(rng, c, trials):
    prog = Built(c.get("c-s3.10-graph-variations.p02-count-shortest-paths"))
    bad = 0
    for _ in range(trials):
        n, w = rand_digraph(rng, 1, 3, 0.45)
        s, t = 1, rng.randint(1, n)
        d = py_floyd(n, w)
        # count shortest paths by brute force over all simple paths
        best, ways = d[s][t], 0

        def dfs(u, cost, seen):
            nonlocal ways
            if cost > best:
                return
            if u == t:
                if cost == best:
                    ways += 1
                return
            for (a, b), x in w.items():
                if a == u and b not in seen:
                    dfs(b, cost + x, seen | {b})
        if best < INF:
            dfs(s, 0, {s})
        want = f"{best}\n{ways}" if best < INF else "-1\n0"
        text = f"{n} {len(w)}\n" + "".join(f"{u} {v} {x}\n" for (u, v), x in w.items()) + f"{s} {t}\n"
        if prog(text) != want:
            bad += 1
    return bad


def check_prim(rng, c, trials):
    blocked_prog = Built(c.get("c-s3.10-graph-variations.p05-prim-blocked-steps"))
    heap_prog = Built(c.get("c-s3.10-graph-variations.p06-prim-heap"))
    bad = 0
    for _ in range(trials):
        n = rng.randint(2, 7)
        pairs = [(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1) if rng.random() < 0.5]
        ws = rng.sample(range(1, 100), len(pairs))
        edges = [(u, v, x) for (u, v), x in zip(pairs, ws)]
        blocked = rng.sample(pairs, rng.randint(0, min(2, len(pairs))))
        s = rng.randint(1, n)
        open_edges = [e for e in edges if (e[0], e[1]) not in blocked]
        want = py_kruskal(n, open_edges)

        text = (f"{n} {len(edges)} {s}\n" + "".join(f"{u} {v} {x}\n" for u, v, x in edges)
                + f"{len(blocked)}\n" + "".join(f"{u} {v}\n" for u, v in blocked))
        got_blocked = int(blocked_prog(text).split("\n")[-1])
        heap_text = f"{n} {len(open_edges)} {s}\n" + "".join(f"{u} {v} {x}\n" for u, v, x in open_edges)
        got_heap = int(heap_prog(heap_text))
        if got_blocked != want or got_heap != want:
            bad += 1
    return bad


def check_spt(rng, c, trials):
    prog = Built(c.get("c-s3.10-graph-variations.p01-dijkstra-spt-matrix"))
    bad = done = 0
    while done < trials:
        n, w = rand_digraph(rng, 1, 30, 0.4)
        s = rng.randint(1, n)
        d = py_floyd(n, w)
        tree = [[0 if i == j else -1 for j in range(n + 1)] for i in range(n + 1)]
        ok = True
        for v in range(1, n + 1):
            if v == s or d[s][v] >= INF:
                continue
            preds = [u for (u, b), x in w.items() if b == v and d[s][u] + x == d[s][v]]
            if len(preds) != 1:
                ok = False
                break
            tree[preds[0]][v] = w[(preds[0], v)]
        if not ok:
            continue                           # tests only use graphs with a unique SPT
        done += 1
        text = f"{n}\n" + "\n".join(" ".join(str(0 if i == j else w.get((i, j), 999))
                                              for j in range(1, n + 1)) for i in range(1, n + 1)) + f"\n{s}\n"
        want = "\n".join(" ".join(map(str, tree[i][1:])) for i in range(1, n + 1))
        if prog(text) != want:
            bad += 1
    return bad


# ---- trees -------------------------------------------------------------------
class PB:
    def __init__(self, k):
        self.k, self.l, self.r, self.p = k, None, None, None


def pb_insert(root, k):
    y, x = None, root
    while x:
        y, x = x, (x.l if k < x.k else x.r)
    n = PB(k)
    n.p = y
    if y is None:
        return n
    if k < y.k:
        y.l = n
    else:
        y.r = n
    return root


def pb_transplant(root, u, v):
    if u.p is None:
        root = v
    elif u is u.p.l:
        u.p.l = v
    else:
        u.p.r = v
    if v:
        v.p = u.p
    return root


def pb_delete(root, x):
    if x.l is None:
        return pb_transplant(root, x, x.r)
    if x.r is None:
        return pb_transplant(root, x, x.l)
    y = x.r
    while y.l:
        y = y.l
    if y.p is not x:
        root = pb_transplant(root, y, y.r)
        y.r = x.r
        y.r.p = y
    root = pb_transplant(root, x, y)
    y.l = x.l
    y.l.p = y
    return root


def pb_inorder(t):
    return [] if t is None else pb_inorder(t.l) + [t] + pb_inorder(t.r)


def pb_pre(t):
    return [] if t is None else [t.k] + pb_pre(t.l) + pb_pre(t.r)


def check_rank(rng, c, trials):
    prog = Built(c.get("c-s3.11-tree-variations.p01-delete-by-rank"))
    bad = 0
    for _ in range(trials):
        keys = rng.sample(range(1, 80), rng.randint(1, 12))
        root, lines, want = None, [], []
        for k in keys:
            root = pb_insert(root, k)
            lines.append(f"i {k}")
        for _ in range(rng.randint(1, 6)):
            nodes = pb_inorder(root)
            k = rng.randint(0, len(nodes) + 1)
            lines.append(f"r {k}")
            if 1 <= k <= len(nodes):
                want.append(str(nodes[k - 1].k))
                root = pb_delete(root, nodes[k - 1])
            else:
                want.append("-1")
            lines.append("t")
            want.append(" ".join(map(str, pb_pre(root))) or "NULL")
        lines.append("e")
        if prog("\n".join(lines) + "\n") != "\n".join(want):
            bad += 1
    return bad


def check_queries(rng, c, trials):
    prog = Built(c.get("c-s3.11-tree-variations.p02-bst-queries"))
    bad = 0
    for _ in range(trials):
        keys = rng.sample(range(1, 60), rng.randint(1, 12))
        root = None
        for k in keys:
            root = pb_insert(root, k)
        lines, want = [f"i {k}" for k in keys], []
        for _ in range(6):
            q = rng.choice("lfcr")
            if q == "l":
                a, b = rng.choice(keys), rng.choice(keys)
                lines.append(f"l {a} {b}")
                x = root
                while not (min(a, b) <= x.k <= max(a, b)):
                    x = x.l if a < x.k else x.r
                want.append(str(x.k))
            elif q == "f":
                x = rng.randint(0, 61)
                lines.append(f"f {x}")
                want.append(str(max([k for k in keys if k <= x], default=-1)))
            elif q == "c":
                x = rng.randint(0, 61)
                lines.append(f"c {x}")
                want.append(str(min([k for k in keys if k >= x], default=-1)))
            else:
                lo = rng.randint(0, 50)
                hi = lo + rng.randint(0, 20)
                lines.append(f"r {lo} {hi}")
                want.append(" ".join(str(k) for k in sorted(keys) if lo <= k <= hi))
        lines.append("e")
        if prog("\n".join(lines) + "\n") != "\n".join(want).strip():
            bad += 1
    return bad


def tree_inorder(t):
    return [] if t is None else tree_inorder(t.l) + [t.v] + tree_inorder(t.r)


def check_validate(rng, c, trials):
    prog = Built(c.get("c-s3.11-tree-variations.p03-validate-bst"))
    bad = 0
    for _ in range(trials):
        t = random_tree(rng, rng.randint(1, 10), values=rng.sample(range(1, 30), 10))
        seq = tree_inorder(t)
        want = "YES" if all(a < b for a, b in zip(seq, seq[1:])) else "NO"
        if prog(f"1\n{spaced(t)}\n") != want:
            bad += 1
    return bad


def ht(t):
    return 0 if t is None else 1 + max(ht(t.l), ht(t.r))


def balanced(t):
    return t is None or (abs(ht(t.l) - ht(t.r)) <= 1 and balanced(t.l) and balanced(t.r))


def all_nodes(t):
    return [] if t is None else [t] + all_nodes(t.l) + all_nodes(t.r)


def diameter(t):
    return max((ht(x.l) + ht(x.r) for x in all_nodes(t)), default=0)


def mirror_pre(t):
    return [] if t is None else [t.v] + mirror_pre(t.r) + mirror_pre(t.l)


def check_shape(rng, c, trials):
    prog = Built(c.get("c-s3.11-tree-variations.p05-balanced-diameter-mirror"))
    bad = 0
    for _ in range(trials):
        t = random_tree(rng, rng.randint(1, 16), shape=rng.choice(["random", "random", "full", "left"]))
        want = f"{int(balanced(t))}\n{diameter(t)}\n" + " ".join(map(str, mirror_pre(t)))
        if prog(spaced(t) + "\n") != want:
            bad += 1
    return bad


def paths(t, acc=()):
    if t is None:
        return []
    acc = acc + (t.v,)
    if t.l is None and t.r is None:
        return [acc]
    return paths(t.l, acc) + paths(t.r, acc)


def check_paths(rng, c, trials):
    prog = Built(c.get("c-s3.11-tree-variations.p06-root-to-leaf-paths"))
    bad = 0
    for _ in range(trials):
        t = random_tree(rng, rng.randint(1, 14))
        ps = paths(t)
        target = sum(rng.choice(ps))
        want = "\n".join("->".join(map(str, p)) for p in ps) + f"\n{sum(1 for p in ps if sum(p) == target)}"
        if prog(spaced(t) + f"\n{target}\n") != want:
            bad += 1
    return bad


def main(argv):
    trials = int(argv[0]) if argv else 150
    rng = random.Random(20260921)
    c = Content()
    total = 0
    for name, fn in [
        ("Floyd-Warshall vs Python", check_floyd),
        ("Bellman-Ford vs Python", check_bellman),
        ("shortest-path counting vs brute-force path enumeration", check_count),
        ("Prim (blocked) and heap Prim vs Python Kruskal", check_prim),
        ("Dijkstra SPT matrix vs Python", check_spt),
        ("delete-by-rank vs Python CLRS model (preorder)", check_rank),
        ("BST LCA/floor/ceil/range vs brute force", check_queries),
        ("isBST vs 'inorder strictly increasing'", check_validate),
        ("balanced / diameter / mirror vs brute force", check_shape),
        ("root-to-leaf paths vs Python", check_paths),
    ]:
        bad = fn(rng, c, trials)
        total += bad
        print(f"{'ok ' if not bad else 'BAD'} {trials - bad:>4}/{trials}  {name}")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
