"""Run a command in the container of a service.

The command runs with docker exec, through jazzoo's run_docker: it gets a terminal
when this script runs in one. cmd is split into words like a shell would, but it
does not run in a shell. The exit code of the command becomes the exit code of the
script.
"""

import argparse
import shlex
import sys

from jazzoo import CommandError, run, run_docker


def run_in_container(container, cmd, user, workdir):
    words = shlex.split(cmd)
    if not words:
        sys.exit("The command is empty")
    run_in = run_docker(container, user=user or None, workdir=workdir or None)(run)
    result = run_in(words, check=False)
    sys.exit(result.returncode)


def _args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--container", required=True)
    run_parser.add_argument("--cmd", required=True)
    run_parser.add_argument("--user", default="")
    run_parser.add_argument("--workdir", default="")

    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    try:
        run_in_container(args.container, args.cmd, args.user, args.workdir)
    except CommandError as e:
        sys.exit(str(e))
