"""Process execution with wall-clock timeouts and hard output caps.

This judge only ever runs code the user wrote themselves on their own machine, so
there is no container and no privilege dropping.  What it does guarantee is that a
runaway program cannot hang the server or fill the disk: every run is bounded in
time and in bytes written, and the process is killed the moment either is hit.
"""
from __future__ import annotations

import os
import sys
import shutil
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

# All scratch work happens under one root so a crash leaves a single tree to clean.
WORK_ROOT = Path(tempfile.gettempdir()) / "nitc-judge-work"


def _silence_crash_dialogs():
    """Stop Windows Error Reporting from holding a crashed child process open.

    A segfaulting program otherwise pops a "program stopped working" dialog and
    sits there until it is dismissed, which the judge can only observe as a
    timeout - so a null-pointer bug gets reported as TLE instead of RE.  Child
    processes inherit the parent's error mode, so setting it once here covers
    every program the judge ever launches.
    """
    if sys.platform != "win32":
        return
    SEM_FAILCRITICALERRORS = 0x0001
    SEM_NOGPFAULTERRORBOX = 0x0002
    SEM_NOOPENFILEERRORBOX = 0x8000
    try:
        import ctypes

        ctypes.windll.kernel32.SetErrorMode(
            SEM_FAILCRITICALERRORS | SEM_NOGPFAULTERRORBOX | SEM_NOOPENFILEERRORBOX)
    except Exception:
        pass  # worst case a crash reads as a timeout; not worth failing over


_silence_crash_dialogs()


@dataclass
class RunResult:
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None
    duration_ms: int = 0
    timed_out: bool = False
    output_capped: bool = False
    signal_name: str = ""

    @property
    def crashed(self) -> bool:
        return self.exit_code is not None and self.exit_code != 0


# Windows surfaces fatal exceptions as large unsigned status codes rather than
# POSIX signals; map the ones a C student actually hits to something readable.
_WIN_STATUS = {
    0xC0000005: "SIGSEGV (invalid memory access - likely a bad pointer or out-of-bounds index)",
    0xC00000FD: "stack overflow (runaway recursion?)",
    0xC0000094: "integer division by zero",
    0xC0000409: "stack buffer overrun",
    0xC000001D: "illegal instruction",
    0x3: "abort() - often a failed assert or heap corruption",
}


def describe_exit(code: int | None) -> str:
    if code is None or code == 0:
        return ""
    unsigned = code & 0xFFFFFFFF
    if unsigned in _WIN_STATUS:
        return _WIN_STATUS[unsigned]
    if code < 0:  # POSIX-style negative signal number
        try:
            import signal

            return signal.Signals(-code).name
        except Exception:
            return f"signal {-code}"
    return f"exit code {code}"


def _drain(stream, cap_bytes: int, sink: dict, key: str, on_overflow):
    """Read a pipe into `sink`, stopping (and signalling) once cap_bytes is passed."""
    chunks: list[bytes] = []
    total = 0
    try:
        while True:
            chunk = stream.read(8192)
            if not chunk:
                break
            total += len(chunk)
            if total > cap_bytes:
                chunks.append(chunk[: max(0, cap_bytes - (total - len(chunk)))])
                sink[key] = b"".join(chunks)
                on_overflow()
                return
            chunks.append(chunk)
    except (ValueError, OSError):
        pass  # pipe closed under us by the killer
    sink[key] = b"".join(chunks)


def run(cmd, cwd: Path, stdin_data: str = "", timeout_ms: int = 2000,
        output_cap_kb: int = 64) -> RunResult:
    cap = output_cap_kb * 1024
    started = time.perf_counter()
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )

    sink: dict[str, bytes] = {}
    state = {"capped": False}

    def overflow():
        state["capped"] = True
        try:
            proc.kill()
        except Exception:
            pass

    threads = [
        threading.Thread(target=_drain, args=(proc.stdout, cap, sink, "out", overflow), daemon=True),
        threading.Thread(target=_drain, args=(proc.stderr, cap, sink, "err", overflow), daemon=True),
    ]
    for t in threads:
        t.start()

    timed_out = False
    try:
        proc.stdin.write(stdin_data.encode("utf-8"))
    except (BrokenPipeError, OSError):
        pass  # program exited without reading its input - legal
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass

    try:
        proc.wait(timeout=timeout_ms / 1000)
    except subprocess.TimeoutExpired:
        timed_out = True
        proc.kill()
        proc.wait()

    for t in threads:
        t.join(timeout=1.0)
    duration = int((time.perf_counter() - started) * 1000)

    code = proc.returncode
    return RunResult(
        stdout=sink.get("out", b"").decode("utf-8", errors="replace"),
        stderr=sink.get("err", b"").decode("utf-8", errors="replace"),
        exit_code=code,
        duration_ms=duration,
        timed_out=timed_out,
        output_capped=state["capped"],
        signal_name="" if timed_out or state["capped"] else describe_exit(code),
    )


class Workspace:
    """A throwaway directory that cleans itself up."""

    def __init__(self, prefix: str = "run"):
        WORK_ROOT.mkdir(parents=True, exist_ok=True)
        self.path = Path(tempfile.mkdtemp(prefix=prefix + "-", dir=str(WORK_ROOT)))

    def write(self, name: str, content: str) -> Path:
        target = self.path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        return target

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.path, ignore_errors=True)
        return False
