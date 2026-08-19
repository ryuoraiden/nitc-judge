# NITC Practice Judge

A local, single-user practice platform built from your own NITC lab assignments.
LeetCode-shaped: problem on the left, editor on the right, Run against samples,
Submit against everything, three-column diff when a test fails.

Currently loaded: **21 problems** covering Stack, Queue, Heap, BFS and Dijkstra,
laid out as a ladder that ends at the Week 4 SSSP practice questions.

## Running it

```bash
python nitc-judge/app.py
```

Then open <http://localhost:5000>. Requires `gcc` on PATH (MinGW-w64 is what this
was built against) and `pip install -r requirements.txt` (Flask, Flask-SQLAlchemy).

## The two problem modes

**`function`** - the shape NITC labs actually use. You are given a read-only
header, you write only the implementation, and a hidden `harness_main.c` drives
your functions. You never see the driver, so you cannot fake a pass with a
well-placed `printf`.

**`program`** - you write the whole thing including `main()`. stdin in, stdout
out, diffed against expected. Used for the verbatim practice questions.

A third family (`py-cli`, `py-flask`, `py-html`) is planned for the MAD 1 track and
is not built yet.

## Layout

```
app.py                 Flask routes
models.py              submissions, drafts, per-problem progress (sqlite)
judge/
  sandbox.py           process execution: timeouts, output caps, crash reporting
  runner_c.py          compile + run + verdict for both modes
  compare.py           output comparison strategies, first-difference locator
  loader.py            scans content/ into memory
  md.py                small Markdown subset renderer
content/c-s3/          the problems - folders, not database rows
scripts/
  authoring/           one generator per unit; regenerate a unit after editing it
  gen_expected.py      produce tests/*.out by RUNNING the reference solution
  validate_pack.py     prove every problem is well-formed
  fuzz_check.py        differential testing against brute force
  smoke_test.py        end-to-end API check against a running server
```

## Adding or changing problems

Problems are folders on disk, so they are diffable and hand-editable. A problem
directory holds `meta.json`, `statement.md`, `starter.c`, `solution.c`, its tests,
and for `function` mode a `problem.h` and `harness_main.c`.

After any change to a reference solution or a test input:

```bash
python scripts/gen_expected.py      # regenerate expected outputs
python scripts/validate_pack.py     # prove nothing broke
```

**Expected outputs are never hand-written.** `gen_expected.py` produces every
`.out` by actually running the reference solution. A judge with a wrong answer key
is worse than no judge, so nothing but a program that ran is allowed to author one.

`validate_pack.py` enforces four properties per problem: the reference compiles
warning-free and passes 100%; the starter stub compiles; the starter does **not**
already pass (otherwise the tests cannot tell a real solution from an empty one);
and no expected output is accidentally empty.

## How the content was verified

Beyond the per-problem validation:

- **Practice Q1, Q2 and Q4** reproduce the official sample outputs from
  `Practice Question - 4.pdf` exactly.
- Each reference was cross-checked against **your own Week 4 solution** on every
  test - 7/7, 8/8 and 7/7 agreement respectively.
- `fuzz_check.py` verifies the two load-bearing claims empirically over 250 random
  graphs each: that plain BFS over sorted adjacency lists really does yield the
  lexicographically smallest shortest path (checked against brute-force
  enumeration of all shortest paths), and that the `O(V^2)` and heap Dijkstras
  agree with each other and with an independent Python implementation.

## Known limitations

- **No memory-leak detection.** This MinGW build ships no `libasan`/`libubsan`, so
  `-fsanitize=address` and `-fsanitize=undefined` both fail at link. Static
  feedback is limited to `-Wall -Wextra`. The planned substitute is a linked
  `malloc`/`free` tracking object file, which would let the linked-list and tree
  problems actually grade `free`-discipline. Not built yet.
- **No sandboxing.** The judge runs your own code on your own machine with no
  isolation. It bounds time and output so a runaway program cannot hang the server
  or fill the disk, and that is the extent of it. Do not point this at code you did
  not write.
- **CodeMirror loads from a CDN.** Offline, the editor degrades to a plain
  textarea, which still works.
- Progress tracking, hint gating and the spaced-repetition schedule are stored and
  updated, but only the review queue surfaces in the dashboard so far.

## Keyboard

`Ctrl+Enter` run · `Ctrl+Shift+Enter` submit
