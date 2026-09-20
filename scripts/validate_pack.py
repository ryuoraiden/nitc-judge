"""Prove every problem is well-formed before you ever see it.

For each problem this asserts:
  1. the reference solution compiles and passes 100% of its own tests
  2. the starter stub compiles (it should fail tests, not fail to build)
  3. the starter does NOT accidentally already pass - a stub that passes means
     the tests are too weak to distinguish a real solution from an empty one
  4. tests exist, expected outputs exist, and no expected output is empty by mistake

    python scripts/validate_pack.py [problem_id_substring ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from judge.loader import Content
from judge.compare import compare
from judge.runner_c import judge
from judge.sandbox import Workspace, run

GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"


def check_cpp(problem) -> list[str]:
    """The C++ reference is shown as a translation source, so it must be exactly
    as correct as the C one: a complete program passing the same tests."""
    with Workspace("cpp") as ws:
        ws.write("reference.cpp", problem.cpp_reference)
        comp = run(["g++", "-std=c++17", "-O2", "-Wall", "reference.cpp", "-o", "ref.exe"],
                   ws.path, timeout_ms=60000, output_cap_kb=256)
        if comp.exit_code != 0:
            return [f"reference.cpp does not compile:\n{comp.stderr[:400]}"]
        bad = []
        for t in problem.tests:
            r = run([str(ws.path / "ref.exe")], ws.path, stdin_data=t.stdin,
                    timeout_ms=problem.run_timeout_ms * 2)
            ok, _ = compare(r.stdout, t.expected, problem.compare_strategy)
            if not ok:
                bad.append(t.name)
        if bad:
            return [f"reference.cpp fails tests {bad}"]
        if comp.stderr.strip():
            return [f"WARN reference.cpp compiles with warnings:\n{comp.stderr[:300]}"]
    return []


def check(problem) -> list[str]:
    errors: list[str] = []

    if not problem.tests:
        return [f"no tests found in {problem.path / 'tests'}"]
    if not problem.solution.strip():
        return ["solution.c is missing or empty"]
    if problem.mode == "function":
        if not problem.header.strip():
            errors.append(f"mode=function but {problem.header_name} is missing")
        if not problem.harness.strip():
            errors.append("mode=function but harness_main.c is missing")
    for t in problem.tests:
        if t.expected.strip() == "" and not problem.allow_empty:
            errors.append(f"test {t.name}: expected output is empty "
                          "(did you forget to run gen_expected.py?)")

    ref = judge(problem, problem.solution)
    if ref.verdict != "AC":
        detail = ref.compile_log if not ref.compile_ok else ""
        failing = [f"{t.name}:{t.status}" for t in ref.tests if not t.ok]
        errors.append(f"reference solution scored {ref.verdict} "
                      f"({ref.passed}/{ref.total}) {failing} {detail[:400]}")
    elif ref.warnings:
        errors.append(f"WARN reference solution compiles with warnings:\n{ref.warnings[:400]}")

    if problem.starter.strip():
        stub = judge(problem, problem.starter)
        if not stub.compile_ok:
            errors.append(f"starter.c does not compile:\n{stub.compile_log[:400]}")
        elif stub.verdict == "AC":
            errors.append("starter.c already passes every test - the tests cannot "
                          "distinguish a real solution from the stub")

    return errors


def main(argv):
    content = Content()
    targets = content.all_problems
    if argv:
        targets = [p for p in targets if any(a in p.id for a in argv)]
    if not targets:
        print("no matching problems")
        return 1

    failed = warned = 0
    for problem in targets:
        errors = check(problem)
        hard = [e for e in errors if not e.startswith("WARN")]
        soft = [e for e in errors if e.startswith("WARN")]
        if hard:
            failed += 1
            print(f"{RED}FAIL{RESET} {problem.id}")
            for e in hard:
                print(f"       {e}")
        elif soft:
            warned += 1
            print(f"{YELLOW}WARN{RESET} {problem.id}")
            for e in soft:
                print(f"       {e[5:]}")
        else:
            print(f"{GREEN} ok {RESET} {problem.id}  "
                  f"({len(problem.tests)} tests, {problem.mode})")

    print(f"\n{len(targets)} problem(s): {len(targets) - failed - warned} clean, "
          f"{warned} warned, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
