"""Persistence for *your* data only - problems themselves live on disk as folders."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Spaced-repetition ladder, in days.  A problem re-surfaces for review at each
# step; failing a review drops it back to the start.
REVIEW_STEPS = [1, 4, 10, 30, 90]


def _now():
    return datetime.now(timezone.utc)


class Submission(db.Model):
    """One graded attempt.  Kept in full so you can diff how a solution evolved."""
    id = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.String(200), index=True, nullable=False)
    code = db.Column(db.Text, nullable=False)
    verdict = db.Column(db.String(8), nullable=False)
    passed = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    max_ms = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=_now, index=True)


class Draft(db.Model):
    """Autosaved editor buffer, one per problem."""
    problem_id = db.Column(db.String(200), primary_key=True)
    code = db.Column(db.Text, nullable=False)
    updated_at = db.Column(db.DateTime, default=_now, onupdate=_now)


class ProblemState(db.Model):
    """Rolled-up progress: solved status, hint gating, spaced-repetition schedule."""
    problem_id = db.Column(db.String(200), primary_key=True)
    attempts = db.Column(db.Integer, default=0)
    failed_attempts = db.Column(db.Integer, default=0)
    solved_at = db.Column(db.DateTime, nullable=True)
    first_solved_unaided = db.Column(db.Boolean, default=False)
    hints_unlocked = db.Column(db.Integer, default=1)
    solution_revealed = db.Column(db.Boolean, default=False)
    best_ms = db.Column(db.Integer, nullable=True)
    review_step = db.Column(db.Integer, default=0)
    review_due = db.Column(db.DateTime, nullable=True, index=True)
    notes = db.Column(db.Text, default="")

    @property
    def solved(self) -> bool:
        return self.solved_at is not None

    def record_attempt(self, verdict: str, max_ms: int = 0):
        self.attempts = (self.attempts or 0) + 1
        if verdict == "AC":
            if not self.solved:
                self.solved_at = _now()
                # "Unaided" means solved without ever revealing the solution.
                self.first_solved_unaided = not self.solution_revealed
            if self.best_ms is None or max_ms < self.best_ms:
                self.best_ms = max_ms
            self.schedule_review(passed=True)
        else:
            self.failed_attempts = (self.failed_attempts or 0) + 1
            # Earn hints by trying, not by waiting.
            self.hints_unlocked = min((self.hints_unlocked or 1) + 1, 3)
            if self.solved:
                self.schedule_review(passed=False)

    def schedule_review(self, passed: bool):
        step = (self.review_step or 0)
        step = min(step + 1, len(REVIEW_STEPS)) if passed else 0
        self.review_step = step
        days = REVIEW_STEPS[min(step, len(REVIEW_STEPS) - 1)]
        self.review_due = _now() + timedelta(days=days)


def get_state(problem_id: str) -> ProblemState:
    state = db.session.get(ProblemState, problem_id)
    if state is None:
        # Column defaults only apply on INSERT, so a freshly constructed object
        # would have None everywhere until it is flushed.  Set them explicitly:
        # callers compare these numerically straight away.
        state = ProblemState(problem_id=problem_id, attempts=0, failed_attempts=0,
                             hints_unlocked=1, solution_revealed=False,
                             review_step=0, notes="")
        db.session.add(state)
    return state
