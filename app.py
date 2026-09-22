"""NITC practice judge - local single-user Flask server."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, abort, jsonify, redirect, render_template, request, url_for

from judge import md
from judge.loader import Content
from judge.runner_c import judge as judge_c, run_once
from models import Draft, ProblemState, Submission, db, get_state

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{BASE_DIR / 'instance' / 'judge.sqlite3'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Without this, browsers cache static files indefinitely (Flask sends no
# Cache-Control for them) and keep running an old judge.js after an update.
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


@app.template_global()
def asset(filename: str) -> str:
    """Static URL with the file's mtime attached, so a changed file is a new URL."""
    path = BASE_DIR / "static" / filename
    stamp = int(path.stat().st_mtime) if path.exists() else 0
    return url_for("static", filename=filename, v=stamp)


(BASE_DIR / "instance").mkdir(exist_ok=True)
db.init_app(app)
content = Content()

with app.app_context():
    db.create_all()


def _problem_or_404(problem_id: str):
    problem = content.get(problem_id)
    if problem is None:
        abort(404)
    return problem


def _states() -> dict:
    return {s.problem_id: s for s in ProblemState.query.all()}


def _serialise(result, problem, reveal_hidden: bool = False):
    """Hidden tests show their verdict but not their data, so you debug by
    reasoning about your code rather than by reading the answer key."""
    tests = []
    for t in result.tests:
        visible = t.is_sample or reveal_hidden
        tests.append({
            "index": t.index, "name": t.name, "status": t.status,
            "is_sample": t.is_sample, "visible": visible,
            "duration_ms": t.duration_ms, "note": t.note,
            "diff_at": t.diff_at,
            "stdin": t.stdin if visible else "",
            "expected": t.expected if visible else "",
            "actual": t.actual if visible else "",
            "stderr": t.stderr if visible else "",
        })
    return {
        "verdict": result.verdict,
        "compile_ok": result.compile_ok,
        "compile_log": result.compile_log,
        "warnings": result.warnings,
        "passed": result.passed,
        "total": result.total,
        "max_ms": result.max_ms,
        "tests": tests,
    }


@app.route("/")
def index():
    states = _states()
    now = datetime.now(timezone.utc)
    due = []
    for problem in content.all_problems:
        s = states.get(problem.id)
        if s and s.solved and s.review_due and s.review_due.replace(tzinfo=timezone.utc) <= now:
            due.append(problem)
    solved_ids = {pid for pid, s in states.items() if s.solved}
    return render_template("index.html", packs=content.packs, states=states,
                           due=due, solved_ids=solved_ids, total_solved=len(solved_ids),
                           total_problems=len(content.all_problems))


@app.route("/p/<problem_id>")
def problem_page(problem_id):
    problem = _problem_or_404(problem_id)
    state = db.session.get(ProblemState, problem_id)
    draft = db.session.get(Draft, problem_id)
    prev_id, next_id = content.neighbours(problem_id)
    recent = (Submission.query.filter_by(problem_id=problem_id)
              .order_by(Submission.created_at.desc()).limit(10).all())
    hints_unlocked = state.hints_unlocked if state else 1
    return render_template(
        "problem.html",
        problem=problem,
        statement_html=md.render(problem.statement),
        code=(draft.code if draft else problem.starter),
        state=state,
        hints=problem.hints[:hints_unlocked],
        hints_total=len(problem.hints),
        solution_visible=bool(state and state.solution_revealed),
        prev_id=prev_id, next_id=next_id,
        recent=recent,
    )


@app.route("/guide")
def guide():
    text = (BASE_DIR / "guides" / "cpp_to_c.md").read_text(encoding="utf-8")
    return render_template("guide.html", body=md.render(text))


@app.post("/api/draft/<problem_id>")
def save_draft(problem_id):
    _problem_or_404(problem_id)
    code = request.json.get("code", "")
    draft = db.session.get(Draft, problem_id)
    if draft is None:
        draft = Draft(problem_id=problem_id, code=code)
        db.session.add(draft)
    else:
        draft.code = code
    db.session.commit()
    return jsonify({"ok": True})


@app.post("/api/run/<problem_id>")
def api_run(problem_id):
    """Run against the sample tests, or against custom input if supplied."""
    problem = _problem_or_404(problem_id)
    payload = request.json or {}
    code = payload.get("code", "")
    custom = payload.get("stdin")

    if custom is not None and custom.strip() != "":
        result = run_once(problem, code, custom)
    else:
        result = judge_c(problem, code, tests=problem.sample_tests)
    return jsonify(_serialise(result, problem, reveal_hidden=True))


@app.post("/api/submit/<problem_id>")
def api_submit(problem_id):
    problem = _problem_or_404(problem_id)
    code = (request.json or {}).get("code", "")
    result = judge_c(problem, code)

    db.session.add(Submission(problem_id=problem_id, code=code, verdict=result.verdict,
                              passed=result.passed, total=result.total, max_ms=result.max_ms))
    state = get_state(problem_id)
    state.record_attempt(result.verdict, result.max_ms)
    draft = db.session.get(Draft, problem_id)
    if draft is None:
        db.session.add(Draft(problem_id=problem_id, code=code))
    else:
        draft.code = code
    db.session.commit()

    data = _serialise(result, problem)
    data["state"] = {
        "solved": state.solved,
        "attempts": state.attempts,
        "hints_unlocked": state.hints_unlocked,
        "can_reveal": state.failed_attempts >= 3 or state.solved,
    }
    return jsonify(data)


@app.post("/api/reveal/<problem_id>")
def api_reveal(problem_id):
    """Unlock the reference solution - gated so it stays a last resort."""
    problem = _problem_or_404(problem_id)
    state = get_state(problem_id)
    if not (state.solved or (state.failed_attempts or 0) >= 3):
        db.session.rollback()
        return jsonify({"ok": False,
                        "reason": "Solve it, or make 3 real attempts first."}), 403
    state.solution_revealed = True
    db.session.commit()
    return jsonify({"ok": True, "solution": problem.solution})


@app.post("/api/hint/<problem_id>")
def api_hint(problem_id):
    problem = _problem_or_404(problem_id)
    state = get_state(problem_id)
    state.hints_unlocked = min((state.hints_unlocked or 1) + 1, len(problem.hints))
    db.session.commit()
    return jsonify({"ok": True, "hints": problem.hints[:state.hints_unlocked],
                    "total": len(problem.hints)})


@app.post("/api/reset/<problem_id>")
def api_reset(problem_id):
    """Blank-slate re-solve: wipe the draft back to the starter stub."""
    problem = _problem_or_404(problem_id)
    draft = db.session.get(Draft, problem_id)
    if draft:
        db.session.delete(draft)
        db.session.commit()
    return jsonify({"ok": True, "code": problem.starter})


@app.post("/api/reload")
def api_reload():
    content.reload()
    return jsonify({"ok": True, "problems": len(content.all_problems)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
