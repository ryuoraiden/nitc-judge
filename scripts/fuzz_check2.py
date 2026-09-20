"""Differential tests for the tree / traversal / MST units.

Claims worth proving rather than asserting in a statement:
  1. stack DFS (mark-on-pop, descending push) == recursive DFS, always
  2. Prim-from-any-source and Kruskal agree on MST cost
  3. BST delete keeps the tree sorted and removes exactly the right key
  4. the parenthesized parser round-trips every tree shape

    python scripts/fuzz_check2.py [trials]
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from judge.loader import Content
from judge.runner_c import _compile, _sources_for
from judge.sandbox import Workspace, run

sys.path.insert(0, str(Path(__file__).resolve().parent / "authoring"))
from _trees import random_tree, spaced, compact, preorder, inorder  # noqa: E402


class Built:
    def __init__(self, problem):
        self.ws = Workspace("fuzz2")
        comp = _compile(problem, self.ws, _sources_for(problem, self.ws, problem.solution))
        if comp.exit_code != 0:
            raise SystemExit(f"{problem.id} did not compile:\n{comp.stderr}")
        self.exe = str(self.ws.path / "prog.exe")

    def __call__(self, stdin):
        r = run([self.exe], self.ws.path, stdin_data=stdin, timeout_ms=5000)
        text = r.stdout.replace("\r\n", "\n")
        # Match the judge's own comparison: trailing whitespace is not significant.
        return "\n".join(line.rstrip() for line in text.split("\n")).strip()


def undirected_graph(rng, nmin=3, nmax=9, density=0.3):
    n = rng.randint(nmin, nmax)
    edges = sorted({(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)
                    if rng.random() < density})
    return n, edges


def fmt(n, edges, extra=""):
    return f"{n} {len(edges)}\n" + "".join(f"{u} {v}\n" for u, v in edges) + extra


# ------------------------------------------------------------------ 1. DFS
def check_dfs(trials, rng, content):
    rec = Built(content.get("c-s3.08-graph-traversal.p01-dfs-recursive"))
    itr = Built(content.get("c-s3.08-graph-traversal.p02-dfs-iterative"))
    bad = 0
    for t in range(trials):
        n, edges = undirected_graph(rng)
        s = rng.randint(1, n)
        stdin = fmt(n, edges, f"{s}\n")
        a, b = rec(stdin), itr(stdin)
        if a != b:
            bad += 1
            if bad <= 2:
                print(f"  MISMATCH\n{stdin}recursive={a}\niterative={b}")
    return bad


# ------------------------------------------------------------------ 2. MST
def check_mst(trials, rng, content):
    kruskal = Built(content.get("c-s3.09-mst.p02-kruskal-cost"))
    prim = Built(content.get("c-s3.09-mst.p03-prim-matrix"))
    bad = 0
    for t in range(trials):
        n = rng.randint(3, 8)
        pairs = sorted({(u, v) for u in range(1, n + 1) for v in range(u + 1, n + 1)
                        if rng.random() < 0.45})
        if not pairs:
            continue
        ws = rng.sample(range(1, 200), len(pairs))
        edges = [(u, v, w) for (u, v), w in zip(pairs, ws)]

        k_in = f"{n} {len(edges)}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges)
        k_cost = int(kruskal(k_in))

        # Prim from every possible source must give the same cost.
        for s in range(1, n + 1):
            p_in = f"{n} {len(edges)} {s}\n" + "".join(f"{u} {v} {w}\n" for u, v, w in edges)
            p_cost = int(prim(p_in).split("\n")[0])
            if p_cost != k_cost:
                bad += 1
                if bad <= 2:
                    print(f"  MISMATCH kruskal={k_cost} prim(s={s})={p_cost}\n{k_in}")
                break
    return bad


# ------------------------------------------------------------------ 3. BST delete
def check_bst(trials, rng, content):
    bst = Built(content.get("c-s3.07-bst.p03-delete-transplant"))
    bad = 0
    for t in range(trials):
        keys = rng.sample(range(1, 60), rng.randint(1, 14))
        live = []
        script = []
        for k in keys:
            script.append(f"i {k}")
            live.append(k)
        for _ in range(rng.randint(1, 6)):
            if live and rng.random() < 0.8:
                v = rng.choice(live)
                live.remove(v)
            else:
                v = rng.randint(1, 60)
                if v in live:
                    live.remove(v)
            script.append(f"d {v}")
        script.append("p")
        script.append("e")
        out = bst("\n".join(script) + "\n").split("\n")
        got = out[-1].strip()
        want = " ".join(str(x) for x in sorted(live)) if live else "NULL"
        if got != want:
            bad += 1
            if bad <= 2:
                print(f"  MISMATCH\n{chr(10).join(script)}\ngot ={got}\nwant={want}")
    return bad


# ------------------------------------------------------------------ 4. parser
def check_parser(trials, rng, content):
    parse = Built(content.get("c-s3.06-binary-tree.p02-parse-notation"))
    bad = 0
    for t in range(trials):
        n = rng.randint(1, 20)
        shape = rng.choice(["random", "left", "right", "full"])
        tree = random_tree(rng, n, values=rng.sample(range(1, 10000), n), shape=shape)
        text = spaced(tree) if t % 2 == 0 else compact(tree, bare_leaves=(t % 4 == 1))
        got = parse(text + "\n")
        want = " ".join(map(str, preorder(tree))) + "\n" + " ".join(map(str, inorder(tree)))
        if got != want:
            bad += 1
            if bad <= 2:
                print(f"  MISMATCH on {text}\ngot ={got!r}\nwant={want!r}")
    return bad


def main(argv):
    trials = int(argv[0]) if argv else 200
    rng = random.Random(20260920)
    content = Content()
    total = 0

    for name, fn in [("iterative DFS == recursive DFS", check_dfs),
                     ("Prim (every source) == Kruskal cost", check_mst),
                     ("BST delete keeps the exact key set, sorted", check_bst),
                     ("parenthesized parser round-trips", check_parser)]:
        print(f"{name} ({trials} trials)")
        bad = fn(trials, rng, content)
        total += bad
        print(f"  -> {trials - bad}/{trials} agree\n")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
