"""Run the Python commands of the project on the host.

`pip-compile` compiles the requirements.txt of each service in /python/services,
from its requirements.in and requirements.editable. BLOGS_LIBS_DIR points to the
libs of the project, so that the `-e ${BLOGS_LIBS_DIR}/...` lines resolve.
"""

import argparse
import sys
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


def _args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    pip_compile_parser = subparsers.add_parser("pip-compile")
    pip_compile_parser.add_argument("--root-dir", required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    try:
        pip_compile(args.root_dir)
    except CommandFailedError as e:
        # uv has already printed its error
        sys.exit(e.result.returncode)
