"""Generate tests/*.out by running each problem's reference solution.

Expected outputs are *produced*, never hand-written.  A judge whose answer key is
wrong is worse than no judge, so the only thing allowed to author an .out file is
a program that actually ran.

    python scripts/gen_expected.py [problem_id_substring ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from judge.loader import Content
from judge.sandbox import Workspace, run
from judge.runner_c import _sources_for, _compile


def generate(problem, force: bool = True) -> tuple[int, list[str]]:
    if not problem.solution.strip():
        return 0, [f"{problem.id}: no solution.c"]
    with Workspace("gen") as ws:
        sources = _sources_for(problem, ws, problem.solution)
        comp = _compile(problem, ws, sources)
        if comp.exit_code != 0:
            return 0, [f"{problem.id}: reference solution does not compile\n{comp.stderr}"]

        problems_errors: list[str] = []
        written = 0
        exe = str(ws.path / "prog.exe")
        for in_file in sorted((problem.path / "tests").glob("*.in")):
            out_file = in_file.with_suffix(".out")
            if out_file.exists() and not force:
                continue
            data = in_file.read_text(encoding="utf-8")
            r = run([exe], ws.path, stdin_data=data,
                    timeout_ms=problem.run_timeout_ms, output_cap_kb=problem.output_cap_kb)
            if r.timed_out:
                problems_errors.append(f"{problem.id}/{in_file.name}: reference solution timed out")
                continue
            if r.crashed:
                problems_errors.append(
                    f"{problem.id}/{in_file.name}: reference solution crashed ({r.signal_name})")
                continue
            text = r.stdout.replace("\r\n", "\n")
            out_file.write_text(text, encoding="utf-8", newline="\n")
            written += 1
        return written, problems_errors


def main(argv):
    content = Content()
    targets = content.all_problems
    if argv:
        targets = [p for p in targets if any(a in p.id for a in argv)]
    if not targets:
        print("no matching problems")
        return 1

    total, all_errors = 0, []
    for problem in targets:
        n, errs = generate(problem)
        total += n
        all_errors.extend(errs)
        status = "ok" if not errs else "FAIL"
        print(f"  [{status}] {problem.id}: {n} expected file(s)")

    print(f"\n{total} expected output(s) written across {len(targets)} problem(s)")
    if all_errors:
        print("\nERRORS:")
        for e in all_errors:
            print(" -", e)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
