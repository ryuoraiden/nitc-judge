"""End-to-end check against a running server: python scripts/smoke_test.py"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from judge.loader import Content

BASE = "http://127.0.0.1:5000"


def post(path, payload):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return r.status, r.read().decode()


WRONG = """
#include "problem.h"

void maxHeapify(int a[], int n, int i) {
    int left = 2 * i + 1, right = 2 * i + 2, largest = i;
    if (left < n && a[left] > a[largest]) largest = left;
    if (right < n && a[right] > a[largest]) largest = right;
    if (largest != i) {
        int t = a[i]; a[i] = a[largest]; a[largest] = t;
        maxHeapify(a, n, i);      /* BUG: recurses on i, not largest */
    }
}
"""

BROKEN = """
#include "problem.h"
void maxHeapify(int a[], int n, int i) {
    this is not C
}
"""

HANGS = """
#include "problem.h"
void maxHeapify(int a[], int n, int i) {
    while (1) { }
}
"""

CRASHES = """
#include "problem.h"
void maxHeapify(int a[], int n, int i) {
    int *p = (int *)0;
    *p = 1;
}
"""

PID = "c-s3.03-heap.p01-max-heapify"
results = []


def expect(label, got, want):
    ok = got == want
    results.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: got {got!r}, expected {want!r}")


print("page loads")
for path in ["/", f"/p/{PID}", "/p/does-not-exist"]:
    try:
        status, body = get(path)
    except urllib.error.HTTPError as e:
        status, body = e.code, ""
    want = 404 if "does-not-exist" in path else 200
    expect(f"GET {path}", status, want)

problem = Content().get(PID)

print("\nsubmit verdicts")
r = post(f"/api/submit/{PID}", {"code": problem.solution})
expect("reference solution", r["verdict"], "AC")
expect("  all tests passed", r["passed"], r["total"])
expect("  clean compile", r["warnings"], "")

r = post(f"/api/submit/{PID}", {"code": WRONG})
expect("recurses on wrong index", r["verdict"], "WA")
failing = [t for t in r["tests"] if t["status"] == "WA"]
expect("  at least one test fails", len(failing) > 0, True)
sample_fail = next((t for t in failing if t["visible"]), None)
expect("  visible failure carries a diff position", bool(sample_fail and sample_fail["diff_at"]), True)
hidden = [t for t in r["tests"] if not t["is_sample"]]
expect("  hidden tests stay hidden", all(t["expected"] == "" for t in hidden), True)

r = post(f"/api/submit/{PID}", {"code": BROKEN})
expect("syntax error", r["verdict"], "CE")
expect("  compile log is populated", len(r["compile_log"]) > 10, True)

r = post(f"/api/submit/{PID}", {"code": HANGS})
expect("infinite loop", r["verdict"], "TLE")

r = post(f"/api/submit/{PID}", {"code": CRASHES})
expect("null dereference", r["verdict"], "RE")

print("\ncustom input run")
r = post(f"/api/run/{PID}", {"code": problem.solution, "stdin": "5\n1 9 8 7 6\n0\n"})
expect("runs against custom stdin", r["verdict"], "OK")
expect("  output is correct", r["tests"][0]["actual"].strip(), "9 7 8 1 6")

print("\nprogress and gating")
r = post(f"/api/reveal/{PID}", {})
expect("solution unlocked after solving", r.get("ok"), True)

fresh = "c-s3.05-dijkstra.p04-dijkstra-heap"
try:
    post(f"/api/reveal/{fresh}", {})
    expect("unsolved problem stays locked", "allowed", "403")
except urllib.error.HTTPError as e:
    expect("unsolved problem stays locked", e.code, 403)

r = post(f"/api/draft/{PID}", {"code": "/* draft */"})
expect("draft saves", r.get("ok"), True)
r = post(f"/api/reset/{PID}", {})
expect("reset restores starter", r["code"].strip() == problem.starter.strip(), True)

print(f"\n{sum(results)}/{len(results)} checks passed")
sys.exit(0 if all(results) else 1)
