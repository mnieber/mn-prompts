import dataclasses
import fcntl
import os
import pty
import shutil
import struct
import subprocess
import sys
import termios
import threading
import time
import typing as T
from pathlib import Path

import pytest

# The root of the blogs example, where the root jazzoo module lives
BLOGS_DIR = Path(__file__).resolve().parent.parent


@dataclasses.dataclass
class Context:
    tmp_path: Path
    monkeypatch: pytest.MonkeyPatch
    request: pytest.FixtureRequest


class TestEnv:
    __test__ = False

    def __init__(self, context: Context):
        self.context = context
        self.exit_code: T.Optional[int] = None
        self.output: T.Optional[str] = None
        self.error_output: T.Optional[str] = None
        self.attached: T.List[subprocess.Popen] = []

        # An isolated tmux server: its socket lives below tmp_path, so the test
        # never touches the developer's own sessions
        context.monkeypatch.setenv("TMUX_TMPDIR", str(context.tmp_path))
        context.monkeypatch.delenv("TMUX", raising=False)
        # jaz and the python3 that tmux.jaz calls must come from this venv
        bin_dir = os.path.dirname(sys.executable)
        context.monkeypatch.setenv("PATH", bin_dir + os.pathsep + os.environ["PATH"])
        # Stop the tmux server, also when the test fails
        context.request.addfinalizer(self.close)

        self.__post_init__()

    def __post_init__(self):
        pass

    def step(self, *_):
        return True

    def close(self):
        self._tmux("kill-server")
        for process in self.attached:
            process.wait(timeout=10)

    def run_jaz(self, *args: str):
        """Runs jaz in the blogs dir, without a terminal, and waits until it ends."""
        completed = subprocess.run(
            ["jaz", *args],
            cwd=BLOGS_DIR,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.exit_code = completed.returncode
        self.output = completed.stdout
        self.error_output = completed.stderr

    def run_jaz_in_terminal(self, *args: str):
        """Starts jaz in the blogs dir in a pseudo-terminal, as a developer would.
        It keeps running while it is attached to the tmux session."""
        master, slave = pty.openpty()
        # Give the terminal a size, as a developer's terminal has
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 120, 0, 0))
        process = subprocess.Popen(
            ["jaz", *args],
            cwd=BLOGS_DIR,
            stdin=slave,
            stdout=slave,
            stderr=slave,
            start_new_session=True,
        )
        os.close(slave)
        self.attached.append(process)
        # tmux draws on the terminal; drain it, so that the tmux client never blocks
        threading.Thread(target=_drain, args=(master,), daemon=True).start()

    def type_in_pane(self, target: str, text: str):
        self._tmux("send-keys", "-t", target, text, "C-m")

    def wait_until(self, condition: T.Callable[[], bool], timeout: float = 10):
        deadline = time.monotonic() + timeout
        while not condition():
            if time.monotonic() > deadline:
                raise TimeoutError("the condition was not met in time")
            time.sleep(0.2)

    def _tmux(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["tmux", *args], capture_output=True, text=True)

    # Queries

    def sessions(self) -> T.List[str]:
        result = self._tmux("list-sessions", "-F", "#{session_name}")
        return result.stdout.split() if result.returncode == 0 else []

    def panes(self, window: str) -> T.List[str]:
        result = self._tmux("list-panes", "-t", window, "-F", "#{pane_id}")
        return result.stdout.split() if result.returncode == 0 else []

    def active_pane(self, window: str) -> str:
        return self._tmux(
            "display-message", "-p", "-t", window, "#{pane_id}"
        ).stdout.strip()

    def pane_text(self, pane: str) -> str:
        # -J joins the lines that tmux wrapped because the pane is narrow
        return self._tmux("capture-pane", "-p", "-J", "-t", pane).stdout

    def clients(self, session: str) -> T.List[str]:
        result = self._tmux("list-clients", "-t", session, "-F", "#{client_name}")
        return result.stdout.split() if result.returncode == 0 else []

    def session_env(self, session: str, name: str) -> T.Optional[str]:
        result = self._tmux("show-environment", "-t", session, name)
        if result.returncode != 0:
            return None
        return result.stdout.strip().partition("=")[2]


def _drain(fd: int):
    try:
        while os.read(fd, 1024):
            pass
    except OSError:
        pass
    finally:
        os.close(fd)


def requires_tmux_and_jaz():
    bin_dir = os.path.dirname(sys.executable)
    return pytest.mark.skipif(
        shutil.which("tmux") is None
        or shutil.which("jaz", path=bin_dir + os.pathsep + os.environ["PATH"]) is None,
        reason="needs tmux and jaz",
    )
