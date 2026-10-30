"""Run the Python commands of the project on the host.

`pip-compile` compiles the requirements.txt of each service in /python/services,
from its requirements.in and requirements.editable. BLOGS_LIBS_DIR points to the
libs of the project, so that the `-e ${BLOGS_LIBS_DIR}/...` lines resolve.

`publish` builds a library into a temp dir, asks for the password (for PyPI: an API
token) and uploads the files of the build to /python/pypi/publish_url as
/python/pypi/username. The password reaches uv in its environment, so that it never
shows up in the args of a process.
"""

import argparse
import getpass
import sys
import tempfile
from pathlib import Path

from jazzoo import CommandFailedError
from jazzoo import get_config as get
from jazzoo import run


def pip_compile(root_dir):
    libs_dir = Path(root_dir) / "src/libs"
    for service in get("/python/services", default=[]):
        run(
            [
                "uv",
                "pip",
                "compile",
                "--python-version=3.12",
                "--upgrade",
                "requirements.in",
                "requirements.editable",
                "-o",
                "requirements.txt",
            ],
            cwd=str(Path(root_dir) / "src/services" / service),
            env=dict(BLOGS_LIBS_DIR=str(libs_dir)),
            echo=True,
        )


def publish(root_dir, package_dir):
    package_dir = Path(root_dir) / package_dir
    if not (package_dir / "pyproject.toml").exists():
        sys.exit(f"No pyproject.toml in {package_dir}")

    username = get("/python/pypi/username")
    publish_url = get("/python/pypi/publish_url")

    with tempfile.TemporaryDirectory(prefix="publish-") as out_dir:
        print(f"Building {package_dir}")
        run(["uv", "build", f"--out-dir={out_dir}", str(package_dir)])
        files = sorted(Path(out_dir).iterdir())
        for path in files:
            print(f"Built {path.name}")

        print(f"Uploading to {publish_url} as {username}")
        try:
            password = getpass.getpass("Password: ")
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit("Upload aborted")
        if not password:
            sys.exit("Upload aborted: no password")

        run(
            [
                "uv",
                "publish",
                f"--publish-url={publish_url}",
                f"--username={username}",
                *[str(x) for x in files],
            ],
            env=dict(UV_PUBLISH_PASSWORD=password),
        )
        print("Uploaded " + ", ".join(x.name for x in files))


def _args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    pip_compile_parser = subparsers.add_parser("pip-compile")
    pip_compile_parser.add_argument("--root-dir", required=True)

    publish_parser = subparsers.add_parser("publish")
    publish_parser.add_argument("--root-dir", required=True)
    publish_parser.add_argument("--package-dir", required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    try:
        if args.action == "pip-compile":
            pip_compile(args.root_dir)
        elif args.action == "publish":
            publish(args.root_dir, args.package_dir)
    except CommandFailedError as e:
        # uv has already printed its error
        sys.exit(e.result.returncode)
