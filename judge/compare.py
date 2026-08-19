"""Output comparison strategies.

Every strategy receives already-decoded text and returns (ok, note).  The note is
shown to the user only when it adds something the diff view cannot: e.g. "matches
except for trailing whitespace".
"""
from __future__ import annotations


def normalize_newlines(text: str) -> str:
    """gcc-built programs on Windows emit CRLF for '\n'.  Expected files are LF."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _strip_trailing(text: str) -> str:
    lines = [line.rstrip() for line in text.split("\n")]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _exact(actual: str, expected: str):
    return actual == expected, ""


def _trim(actual: str, expected: str):
    a, e = _strip_trailing(actual), _strip_trailing(expected)
    if a != e:
        return False, ""
    note = "" if actual == expected else "trailing whitespace differs"
    return True, note


def _tokens(actual: str, expected: str):
    if actual.split() == expected.split():
        note = "" if _strip_trailing(actual) == _strip_trailing(expected) else "line breaks differ"
        return True, note
    return False, ""


def _float_eps(actual: str, expected: str, eps: float = 1e-6):
    at, et = actual.split(), expected.split()
    if len(at) != len(et):
        return False, ""
    for x, y in zip(at, et):
        if x == y:
            continue
        try:
            if abs(float(x) - float(y)) > eps:
                return False, ""
        except ValueError:
            return False, ""
    return True, ""


STRATEGIES = {
    "exact": _exact,
    "trim-trailing-ws": _trim,
    "tokens": _tokens,
    "float-eps": _float_eps,
}


def compare(actual: str, expected: str, strategy: str = "trim-trailing-ws"):
    fn = STRATEGIES.get(strategy, _trim)
    return fn(normalize_newlines(actual), normalize_newlines(expected))


def first_difference(actual: str, expected: str):
    """Return (line_no, col_no) of the first differing character, 1-indexed.

    Used by the UI to point at exactly where the outputs diverge, which is the
    single most useful thing when debugging a near-miss.
    """
    a = normalize_newlines(actual).split("\n")
    e = normalize_newlines(expected).split("\n")
    for i in range(max(len(a), len(e))):
        al = a[i] if i < len(a) else None
        el = e[i] if i < len(e) else None
        if al == el:
            continue
        if al is None or el is None:
            return i + 1, 1
        for j in range(max(len(al), len(el))):
            if j >= len(al) or j >= len(el) or al[j] != el[j]:
                return i + 1, j + 1
        return i + 1, 1
    return None
