"""Compile-and-run pipeline for C problems.

Two shapes of problem are supported:

  program  - the student writes everything including main().  Their file is the
             only translation unit.
  function - the student writes only the implementation file.  A hidden harness
             (harness_main.c) supplies main() and drives the functions declared in
             a read-only header the student can see.  This is the shape NITC labs
             actually use, and it is the one that cannot be faked with printf.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import compare as cmp
from .sandbox import Workspace, run

STUDENT_FILE = "solution.c"


@dataclass
class TestOutcome:
    index: int
    name: str
    is_sample: bool
    status: str                 # AC WA TLE RE OLE
    stdin: str = ""
    expected: str = ""
    actual: str = ""
    stderr: str = ""
    duration_ms: int = 0
    note: str = ""
    diff_at: tuple | None = None

    @property
    def ok(self) -> bool:
        return self.status == "AC"


@dataclass
class JudgeResult:
    verdict: str                # AC WA TLE RE OLE CE
    tests: list = field(default_factory=list)
    compile_log: str = ""
    compile_ok: bool = True
    warnings: str = ""
    passed: int = 0
    total: int = 0
    max_ms: int = 0

    @property
    def all_passed(self) -> bool:
        return self.verdict == "AC"


def _sources_for(problem, ws: Workspace, code: str) -> list[str]:
    """Materialise the workspace and return the translation units to compile."""
    ws.write(STUDENT_FILE, code)
    sources = [STUDENT_FILE]
    if problem.mode == "function":
        # Header is read-only from the student's perspective but must be on disk
        # for both their file and the harness to include.
        ws.write(problem.header_name, problem.header)
        ws.write("harness_main.c", problem.harness)
        sources.insert(0, "harness_main.c")
    for name, content in problem.extra_sources.items():
        ws.write(name, content)
        sources.append(name)
    return sources


def _compile(problem, ws: Workspace, sources: list[str]):
    flags = problem.compile_flags
    cmd = ["gcc", *flags, *sources, "-o", "prog.exe", "-lm"]
    return run(cmd, ws.path, timeout_ms=problem.compile_timeout_ms, output_cap_kb=256)


def _clean_log(text: str) -> str:
    """Strip the workspace path noise out of gcc diagnostics."""
    lines = []
    for line in text.split("\n"):
        if "harness_main.c" in line and "In function" in line:
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def judge(problem, code: str, tests=None) -> JudgeResult:
    """Run `code` against `tests` (defaults to every test the problem defines)."""
    tests = problem.tests if tests is None else tests
    with Workspace(problem.slug) as ws:
        sources = _sources_for(problem, ws, code)
        comp = _compile(problem, ws, sources)
        if comp.exit_code != 0:
            return JudgeResult(
                verdict="CE",
                compile_ok=False,
                compile_log=_clean_log(comp.stderr) or "compilation failed",
                total=len(tests),
            )

        result = JudgeResult(verdict="AC", compile_ok=True,
                             warnings=_clean_log(comp.stderr), total=len(tests))
        exe = str(ws.path / "prog.exe")

        for i, t in enumerate(tests):
            r = run([exe], ws.path, stdin_data=t.stdin,
                    timeout_ms=problem.run_timeout_ms,
                    output_cap_kb=problem.output_cap_kb)
            result.max_ms = max(result.max_ms, r.duration_ms)

            if r.timed_out:
                status, note = "TLE", f"exceeded {problem.run_timeout_ms} ms"
            elif r.output_capped:
                status, note = "OLE", "printed far more output than expected - infinite loop?"
            elif r.crashed:
                status, note = "RE", r.signal_name
            else:
                ok, note = cmp.compare(r.stdout, t.expected, problem.compare_strategy)
                status = "AC" if ok else "WA"

            outcome = TestOutcome(
                index=i, name=t.name, is_sample=t.is_sample, status=status,
                stdin=t.stdin, expected=t.expected, actual=r.stdout,
                stderr=r.stderr[:2000], duration_ms=r.duration_ms, note=note,
            )
            if status == "WA":
                outcome.diff_at = cmp.first_difference(r.stdout, t.expected)
            result.tests.append(outcome)
            if outcome.ok:
                result.passed += 1

        # Report the most informative failure, not merely the first.
        for severity in ("CE", "RE", "OLE", "TLE", "WA"):
            if any(t.status == severity for t in result.tests):
                result.verdict = severity
                break
        return result


def run_once(problem, code: str, stdin_data: str) -> JudgeResult:
    """Free-form execution against custom input - no verdict, no expected output."""
    with Workspace(problem.slug) as ws:
        sources = _sources_for(problem, ws, code)
        comp = _compile(problem, ws, sources)
        if comp.exit_code != 0:
            return JudgeResult(verdict="CE", compile_ok=False,
                               compile_log=_clean_log(comp.stderr) or "compilation failed")
        r = run([str(ws.path / "prog.exe")], ws.path, stdin_data=stdin_data,
                timeout_ms=problem.run_timeout_ms, output_cap_kb=problem.output_cap_kb)
        status = ("TLE" if r.timed_out else "OLE" if r.output_capped
                  else "RE" if r.crashed else "OK")
        res = JudgeResult(verdict=status, compile_ok=True,
                          warnings=_clean_log(comp.stderr), max_ms=r.duration_ms, total=1)
        res.tests.append(TestOutcome(
            index=0, name="custom", is_sample=True, status=status, stdin=stdin_data,
            expected="", actual=r.stdout, stderr=r.stderr[:2000],
            duration_ms=r.duration_ms, note=r.signal_name,
        ))
        return res
