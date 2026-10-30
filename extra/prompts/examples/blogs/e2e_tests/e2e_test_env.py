import dataclasses
import fcntl
import importlib.util
import json
import os
import pty
import select
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

# The compose files, relative to the root of the project
COMPOSE_YML = "env/local/docker/docker-compose.yml"
BASE_IMAGES_YML = "env/local/docker/docker-compose.base-images.yml"
DOCKERFILE_LOCAL_YML = "env/local/docker/docker-compose.dockerfile-local.yml"
SRC_OVERLAYS_YML = "env/local/docker/docker-compose.src-overlays.yml"
OVERRIDE_YML = "env/local/docker/docker-compose.override.yml"

# The files of env/local that belong to the developer, or that are generated
LOCAL_FILES = [
    ".local.env",
    "secrets.env",
    "config/local.yaml",
    "docker/docker-compose.override.yml",
]

# The secrets that the .env.in files of the services use
SECRETS = {
    "BLOGS_BE_DJANGO_DATABASE_PASSWORD": "db-secret",
    "BLOGS_BE_DJANGO_SECRET_KEY": "django-secret",
    "BLOGS_BE_DJANGO_SUPERUSER_PASSWORD": "admin-secret",
    "BLOGS_USER_PASSWORD": "user-secret",
    "POSTGRES_PASSWORD": "pg-secret",
}

# The variables that the fake tools record
RECORDED_VARS = [
    "ROOT_DIR",
    "COMPOSE_PROJECT_NAME",
    "DOCKER_BUILDKIT",
    "COMPOSE_BAKE",
    "BLOGS_LIBS_DIR",
    "UV_PUBLISH_PASSWORD",
]

# The prompt of python.publish
PASSWORD_PROMPT = "Password:"

FAKE_TOOL = """#!{python}
import json
import os
import sys

with open(os.environ["FAKE_TOOLS_CALLS_FILE"], "a") as f:
    call = dict(
        tool="{tool}",
        args=sys.argv[1:],
        cwd=os.getcwd(),
        env={{name: os.environ.get(name) for name in {recorded_vars}}},
    )
    f.write(json.dumps(call) + "\\n")
{extra}
sys.exit(int(os.environ.get("FAKE_{tool_upper}_EXIT_CODE", "0")))
"""

# What the fake uv does besides recording its call: uv build writes a fake sdist
# and wheel into its --out-dir, named after the pyproject.toml of the package dir.
# FAKE_UV_PUBLISH_EXIT_CODE makes only uv publish fail.
FAKE_UV_EXTRA = """
import re
from pathlib import Path


def option(args, name):
    for idx, arg in enumerate(args):
        if arg.startswith(name + "="):
            return arg.split("=", 1)[1]
        if arg == name:
            return args[idx + 1]
    return None


args = sys.argv[1:]
if args[:1] == ["build"] and os.environ.get("FAKE_UV_EXIT_CODE", "0") == "0":
    out_dir = option(args, "--out-dir")
    package_dirs = [x for x in args[1:] if not x.startswith("-") and x != out_dir]
    package_dir = Path(package_dirs[-1] if package_dirs else os.getcwd())
    pyproject = (package_dir / "pyproject.toml").read_text()
    name = re.search(r'^name = "(.*)"', pyproject, re.M).group(1)
    version = re.search(r'^version = "(.*)"', pyproject, re.M).group(1)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    (Path(out_dir) / f"{name}-{version}.tar.gz").write_text("sdist")
    (Path(out_dir) / f"{name}-{version}-py3-none-any.whl").write_text("wheel")
if args[:1] == ["publish"] and "FAKE_UV_PUBLISH_EXIT_CODE" in os.environ:
    sys.exit(int(os.environ["FAKE_UV_PUBLISH_EXIT_CODE"]))
"""

# The options of the uv commands that take a value
UV_VALUE_OPTIONS = ["--out-dir", "--publish-url", "--username"]


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
        self.password_prompted: T.Optional[bool] = None
        self.attached: T.List[subprocess.Popen] = []
        # A copy of the project, so that the developer's own files don't change the
        # results, and are not overwritten
        self.project_dir = context.tmp_path.resolve() / "blogs"
        self.calls_file = context.tmp_path / "calls.jsonl"
        _copy_project(self.project_dir)

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
        if shutil.which("tmux"):
            self._tmux("kill-server")
        for process in self.attached:
            process.wait(timeout=10)

    def run_jaz(self, *args: str):
        """Runs jaz in the project, without a terminal, and waits until it ends."""
        completed = subprocess.run(
            ["jaz", *args],
            cwd=self.project_dir,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.exit_code = completed.returncode
        self.output = completed.stdout
        self.error_output = completed.stderr

    def run_jaz_in_terminal(self, *args: str):
        """Starts jaz in the project in a pseudo-terminal, as a developer would.
        It keeps running while it is attached to the tmux session."""
        master, slave = pty.openpty()
        # Give the terminal a size, as a developer's terminal has
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", 40, 120, 0, 0))
        process = subprocess.Popen(
            ["jaz", *args],
            cwd=self.project_dir,
            stdin=slave,
            stdout=slave,
            stderr=slave,
            start_new_session=True,
        )
        os.close(slave)
        self.attached.append(process)
        # tmux draws on the terminal; drain it, so that the tmux client never blocks
        threading.Thread(target=_drain, args=(master,), daemon=True).start()

    def run_jaz_and_type_password(self, password: str, *args: str):
        """Runs jaz in the project in a pseudo-terminal, as a developer would, and
        types the password (and enter) when jaz asks for it. Stores what the terminal
        showed in env.output, and whether jaz asked for the password in
        env.password_prompted."""
        master, slave = pty.openpty()
        process = subprocess.Popen(
            ["jaz", *args],
            cwd=self.project_dir,
            stdin=slave,
            stdout=slave,
            stderr=slave,
            start_new_session=True,
        )
        os.close(slave)
        output = b""
        self.password_prompted = False
        deadline = time.monotonic() + 30
        while True:
            if time.monotonic() > deadline:
                process.kill()
                raise TimeoutError("jaz did not end in time")
            ready, _, _ = select.select([master], [], [], 0.2)
            if ready:
                try:
                    chunk = os.read(master, 1024)
                except OSError:
                    # The terminal is closed: jaz has ended
                    chunk = b""
                if not chunk:
                    break
                output += chunk
                if not self.password_prompted and PASSWORD_PROMPT.encode() in output:
                    self.password_prompted = True
                    os.write(master, password.encode() + b"\n")
            elif process.poll() is not None:
                break
        os.close(master)
        self.exit_code = process.wait(timeout=10)
        self.output = output.decode(errors="replace").replace("\r\n", "\n")

    def install_fake_tools(self):
        """Puts fake docker and uv executables first on the PATH. They record each
        call in calls.jsonl, and succeed unless fail_tool says otherwise."""
        bin_dir = self.context.tmp_path / "bin"
        bin_dir.mkdir()
        for tool in ("docker", "uv"):
            path = bin_dir / tool
            path.write_text(
                FAKE_TOOL.format(
                    python=sys.executable,
                    tool=tool,
                    tool_upper=tool.upper(),
                    recorded_vars=RECORDED_VARS,
                    extra=FAKE_UV_EXTRA if tool == "uv" else "",
                )
            )
            path.chmod(0o755)
        self.context.monkeypatch.setenv("FAKE_TOOLS_CALLS_FILE", str(self.calls_file))
        self.context.monkeypatch.setenv(
            "PATH", str(bin_dir) + os.pathsep + os.environ["PATH"]
        )

    def export_secrets(self):
        """Exports the secrets, so that the env files compile without a secrets.env.
        Without them, compile_env_files.py fails on the unbound variables."""
        for name, value in SECRETS.items():
            self.context.monkeypatch.setenv(name, value)

    def fail_tool(self, tool: str, exit_code: int):
        self.context.monkeypatch.setenv(
            f"FAKE_{tool.upper()}_EXIT_CODE", str(exit_code)
        )

    def write_local_config(self, text: str):
        self.write_file("env/local/config/local.yaml", text)

    def write_file(self, path: str, text: str):
        """Writes a file of the project, relative to its root."""
        (self.project_dir / path).parent.mkdir(parents=True, exist_ok=True)
        (self.project_dir / path).write_text(text)

    def write_lib(self, path: str, name: str, version: str):
        """Writes the pyproject.toml of a library. A relative path is relative to the
        root of the project."""
        self.write_file(
            f"{path}/pyproject.toml",
            f'[project]\nname = "{name}"\nversion = "{version}"\n',
        )

    def forget_calls(self):
        self.calls_file.unlink(missing_ok=True)

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

    def calls(self, tool: T.Optional[str] = None) -> T.List[dict]:
        """The calls of the fake tools, in the order in which they were made."""
        if not self.calls_file.exists():
            return []
        calls = [json.loads(x) for x in self.calls_file.read_text().splitlines()]
        return [x for x in calls if tool is None or x["tool"] == tool]

    def call_summary(self) -> T.List[T.Tuple[str, str]]:
        """Each call as (tool, command), e.g. ("docker", "up"), ("uv", "pip compile")."""
        return [
            (
                call["tool"],
                (
                    self.compose_command(call)[0]
                    if call["tool"] == "docker"
                    else " ".join(call["args"][:2])
                ),
            )
            for call in self.calls()
        ]

    def compose_files(self, call: dict) -> T.List[str]:
        """The files of the --file options of a docker compose call, relative to the
        root of the project."""
        args = call["args"]
        return [
            self.relative_path(args[idx + 1])
            for idx, arg in enumerate(args)
            if arg == "--file"
        ]

    def compose_command(self, call: dict) -> T.List[str]:
        """The arguments of a docker compose call after its global options, e.g.
        ["build", "--no-cache"]."""
        args = call["args"]
        assert args[0] == "compose"
        idx = 1
        while idx < len(args) and args[idx].startswith("--"):
            idx += 2 if args[idx] == "--file" else 1
        return args[idx:]

    def build_args(self, call: dict) -> T.List[str]:
        args = call["args"]
        return [args[idx + 1] for idx, arg in enumerate(args) if arg == "--build-arg"]

    def uv_call(self, command: str) -> dict:
        """The last call of uv with this command, e.g. "build" or "publish"."""
        return [x for x in self.calls("uv") if x["args"][:1] == [command]][-1]

    def option(self, call: dict, name: str) -> T.Optional[str]:
        """The value of an option of a call, as --name=value or --name value."""
        args = call["args"]
        for idx, arg in enumerate(args):
            if arg.startswith(name + "="):
                return arg.split("=", 1)[1]
            if arg == name:
                return args[idx + 1]
        return None

    def positional_args(self, call: dict) -> T.List[str]:
        """The args of a uv call after its command that are not options."""
        args = call["args"][1:]
        result = []
        idx = 0
        while idx < len(args):
            if args[idx] in UV_VALUE_OPTIONS:
                idx += 2
                continue
            if not args[idx].startswith("-"):
                result.append(args[idx])
            idx += 1
        return result

    def relative_path(self, path: str) -> str:
        return str(Path(path).resolve().relative_to(self.project_dir))

    def project_file(self, path: str) -> Path:
        return self.project_dir / path

    def read_file(self, path: str) -> str:
        return (self.project_dir / path).read_text()


def _copy_project(project_dir: Path):
    """Copies the root module, env/local (without the developer's own files and the
    generated env files) and the requirements files of the services."""
    project_dir.mkdir(parents=True)
    shutil.copy2(BLOGS_DIR / "jazzoo", project_dir / "jazzoo")

    local_dir = BLOGS_DIR / "env/local"

    def ignore(src, names):
        rel_dir = Path(src).relative_to(local_dir)
        return [
            name
            for name in names
            if name == "__pycache__"
            or str(rel_dir / name) in LOCAL_FILES
            or (rel_dir == Path("docker/env_files") and name.endswith(".env"))
        ]

    shutil.copytree(local_dir, project_dir / "env/local", ignore=ignore)

    for service_dir in (BLOGS_DIR / "src/services").iterdir():
        target_dir = project_dir / "src/services" / service_dir.name
        target_dir.mkdir(parents=True)
        for path in service_dir.glob("requirements.*"):
            shutil.copy2(path, target_dir / path.name)
    (project_dir / "src/libs").mkdir()


def _drain(fd: int):
    try:
        while os.read(fd, 1024):
            pass
    except OSError:
        pass
    finally:
        os.close(fd)


def requires_jaz():
    """The compose targets also need expandvars, for compile_env_files.py."""
    bin_dir = os.path.dirname(sys.executable)
    return pytest.mark.skipif(
        shutil.which("jaz", path=bin_dir + os.pathsep + os.environ["PATH"]) is None
        or importlib.util.find_spec("expandvars") is None,
        reason="needs jaz and expandvars",
    )


def requires_tmux_and_jaz():
    bin_dir = os.path.dirname(sys.executable)
    return pytest.mark.skipif(
        shutil.which("tmux") is None
        or shutil.which("jaz", path=bin_dir + os.pathsep + os.environ["PATH"]) is None,
        reason="needs tmux and jaz",
    )
