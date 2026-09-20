"""Scans content/ into an in-memory index.

Problems are folders, not database rows: a problem is a directory containing a
meta.json plus its statement, starter, reference solution and tests.  That keeps
them diffable, hand-editable, and trivial to add in bulk - and means adding the S3
pack later is a content change with no code change.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

CONTENT_ROOT = Path(__file__).resolve().parent.parent / "content"

DEFAULT_COMPILE_FLAGS = ["-Wall", "-Wextra", "-std=c11", "-O0"]


@dataclass
class Test:
    name: str
    stdin: str
    expected: str
    is_sample: bool


@dataclass
class Problem:
    id: str
    slug: str
    title: str
    mode: str
    path: Path
    pack_id: str
    unit_id: str
    unit_title: str
    difficulty: str = "easy"
    topics: list = field(default_factory=list)
    estimated_minutes: int = 10
    source: str = ""
    prereqs: list = field(default_factory=list)
    statement: str = ""
    starter: str = ""
    solution: str = ""
    header: str = ""
    header_name: str = "problem.h"
    harness: str = ""
    extra_sources: dict = field(default_factory=dict)
    hints: list = field(default_factory=list)
    tests: list = field(default_factory=list)
    # "core" is what the test needs; "extra" is an optional variation.
    tier: str = "core"
    allow_empty: bool = False   # some tests legitimately expect no output
    # An idiomatic C++ (Striver-style) version of the same program, reading the
    # same stdin.  Shown as the source for a C++ -> C translation drill.
    cpp_reference: str = ""
    cpp_notes: list = field(default_factory=list)
    compare_strategy: str = "trim-trailing-ws"
    compile_flags: list = field(default_factory=lambda: list(DEFAULT_COMPILE_FLAGS))
    compile_timeout_ms: int = 10000
    run_timeout_ms: int = 2000
    output_cap_kb: int = 64

    @property
    def sample_tests(self):
        return [t for t in self.tests if t.is_sample]


@dataclass
class Unit:
    id: str
    title: str
    description: str
    pack_id: str
    problems: list = field(default_factory=list)


@dataclass
class Pack:
    id: str
    title: str
    description: str
    language: str
    units: list = field(default_factory=list)

    @property
    def problems(self):
        return [p for u in self.units for p in u.problems]


def _read(path: Path, default: str = "") -> str:
    return path.read_text(encoding="utf-8") if path.exists() else default


def _load_tests(problem_dir: Path, sample_count: int) -> list:
    tests_dir = problem_dir / "tests"
    if not tests_dir.exists():
        return []
    tests = []
    for i, in_file in enumerate(sorted(tests_dir.glob("*.in"))):
        out_file = in_file.with_suffix(".out")
        tests.append(Test(
            name=in_file.stem,
            stdin=_read(in_file),
            expected=_read(out_file),
            is_sample=i < sample_count,
        ))
    return tests


def _load_problem(problem_dir: Path, pack_id: str, unit_id: str, unit_title: str) -> Problem:
    meta = json.loads(_read(problem_dir / "meta.json", "{}"))
    mode = meta.get("mode", "program")
    compile_cfg = meta.get("compile", {})
    run_cfg = meta.get("run", {})
    header_name = meta.get("header_name", "problem.h")

    extra = {}
    extra_dir = problem_dir / "extra"
    if extra_dir.exists():
        for f in sorted(extra_dir.iterdir()):
            if f.suffix == ".c":
                extra[f.name] = _read(f)

    slug = problem_dir.name
    return Problem(
        id=meta.get("id") or f"{pack_id}.{unit_id}.{slug}",
        slug=slug,
        title=meta.get("title", slug),
        mode=mode,
        path=problem_dir,
        pack_id=pack_id,
        unit_id=unit_id,
        unit_title=unit_title,
        difficulty=meta.get("difficulty", "easy"),
        topics=meta.get("topics", []),
        estimated_minutes=meta.get("estimated_minutes", 10),
        source=meta.get("source", ""),
        prereqs=meta.get("prereqs", []),
        statement=_read(problem_dir / "statement.md"),
        starter=_read(problem_dir / "starter.c"),
        solution=_read(problem_dir / "solution.c"),
        header=_read(problem_dir / header_name),
        header_name=header_name,
        harness=_read(problem_dir / "harness_main.c"),
        extra_sources=extra,
        hints=meta.get("hints", []),
        tests=_load_tests(problem_dir, meta.get("samples", 1)),
        tier=meta.get("tier", "core"),
        allow_empty=meta.get("allow_empty", False),
        cpp_reference=_read(problem_dir / "reference.cpp"),
        cpp_notes=meta.get("cpp_notes", []),
        compare_strategy=meta.get("compare", "trim-trailing-ws"),
        compile_flags=compile_cfg.get("flags", list(DEFAULT_COMPILE_FLAGS)),
        compile_timeout_ms=compile_cfg.get("timeout_ms", 10000),
        run_timeout_ms=run_cfg.get("timeout_ms", 2000),
        output_cap_kb=run_cfg.get("output_cap_kb", 64),
    )


class Content:
    """The loaded content tree.  Call reload() to pick up edits without a restart."""

    def __init__(self, root: Path = CONTENT_ROOT):
        self.root = root
        self.packs: list = []
        self.by_id: dict = {}
        self.reload()

    def reload(self):
        packs, by_id = [], {}
        if not self.root.exists():
            self.packs, self.by_id = packs, by_id
            return
        for pack_dir in sorted(d for d in self.root.iterdir() if d.is_dir()):
            pack_meta = json.loads(_read(pack_dir / "pack.json", "{}"))
            pack = Pack(
                id=pack_meta.get("id", pack_dir.name),
                title=pack_meta.get("title", pack_dir.name),
                description=pack_meta.get("description", ""),
                language=pack_meta.get("language", "c"),
            )
            for unit_dir in sorted(d for d in pack_dir.iterdir() if d.is_dir()):
                unit_meta = json.loads(_read(unit_dir / "unit.json", "{}"))
                unit = Unit(
                    id=unit_dir.name,
                    title=unit_meta.get("title", unit_dir.name),
                    description=unit_meta.get("description", ""),
                    pack_id=pack.id,
                )
                for problem_dir in sorted(d for d in unit_dir.iterdir() if d.is_dir()):
                    if not (problem_dir / "meta.json").exists():
                        continue
                    problem = _load_problem(problem_dir, pack.id, unit.id, unit.title)
                    unit.problems.append(problem)
                    by_id[problem.id] = problem
                if unit.problems:
                    pack.units.append(unit)
            if pack.units:
                packs.append(pack)
        self.packs, self.by_id = packs, by_id

    def get(self, problem_id: str):
        return self.by_id.get(problem_id)

    @property
    def all_problems(self):
        return [p for pack in self.packs for p in pack.problems]

    def ordered_ids(self):
        return [p.id for p in self.all_problems]

    def neighbours(self, problem_id: str):
        ids = self.ordered_ids()
        if problem_id not in ids:
            return None, None
        i = ids.index(problem_id)
        return (ids[i - 1] if i > 0 else None,
                ids[i + 1] if i < len(ids) - 1 else None)
