"""Helpers for the content generators in this folder.

The generated folders under content/ are the source of truth - these scripts just
make it practical to author a whole unit at once and regenerate it after an edit
to a shared harness.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT = ROOT / "content"

DEFAULT_META = {
    "difficulty": "easy",
    "topics": [],
    "estimated_minutes": 10,
    "samples": 1,
    "compare": "trim-trailing-ws",
    "hints": [],
    "prereqs": [],
    "source": "",
}


def write_pack(pack_id: str, title: str = None, description: str = None,
               language: str = None, essentials: list = None):
    """Merge into pack.json rather than replacing it: several scripts own
    different keys (a unit script sets the title, pack_c_s3.py the study path)."""
    d = CONTENT / pack_id
    d.mkdir(parents=True, exist_ok=True)
    path = d / "pack.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    data["id"] = pack_id
    for key, value in (("title", title), ("description", description),
                       ("language", language), ("essentials", essentials)):
        if value is not None:
            data[key] = value
    data.setdefault("language", "c")
    _json(path, data)
    return d


def write_unit(pack_id: str, unit_id: str, title: str, description: str):
    d = CONTENT / pack_id / unit_id
    d.mkdir(parents=True, exist_ok=True)
    _json(d / "unit.json", {"title": title, "description": description})
    return d


def write_problem(pack_id, unit_id, slug, *, title, mode, statement, starter,
                  solution, header=None, harness=None, tests=(), extra=None,
                  cpp=None, **meta):
    d = CONTENT / pack_id / unit_id / slug
    (d / "tests").mkdir(parents=True, exist_ok=True)

    full = dict(DEFAULT_META)
    full.update(meta)
    full["id"] = f"{pack_id}.{unit_id}.{slug}"
    full["title"] = title
    full["mode"] = mode
    _json(d / "meta.json", full)

    _text(d / "statement.md", statement)
    _text(d / "starter.c", starter)
    _text(d / "solution.c", solution)
    if header is not None:
        _text(d / "problem.h", header)
    if harness is not None:
        _text(d / "harness_main.c", harness)
    if cpp is not None:
        _text(d / "reference.cpp", cpp)
    for name, body in (extra or {}).items():
        (d / "extra").mkdir(exist_ok=True)
        _text(d / "extra" / name, body)

    # Old .in files are removed so shrinking a test set does not leave orphans
    # whose stale .out files would silently keep passing.
    for stale in (d / "tests").glob("*.in"):
        stale.unlink()
    for stale in (d / "tests").glob("*.out"):
        stale.unlink()
    for i, data in enumerate(tests):
        _text(d / "tests" / f"{i:02d}.in", data if data.endswith("\n") else data + "\n")
    return d


def _json(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8", newline="\n")


def _text(path: Path, body: str):
    body = body.lstrip("\n")
    if not body.endswith("\n"):
        body += "\n"
    path.write_text(body, encoding="utf-8", newline="\n")


def report(name: str, count: int):
    print(f"  {name}: {count} problems written")
