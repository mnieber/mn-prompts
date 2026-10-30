"""Run docker commands on the containers of the project.

A container is picked by name: an exact name, or a part of a name that matches one
container. Without a name, or when the name matches several containers, the
developer picks from a numbered list. Only the running containers of the compose
project in /docker/compose_project are listed; without it, all running containers.
"""

import argparse
import shlex
import sys

from jazzoo import CommandFailedError
from jazzoo import get_config as get
from jazzoo import run


def _containers():
    project = get("/docker/compose_project", default=None)
    filter_args = (
        ["--filter", f"label=com.docker.compose.project={project}"] if project else []
    )
    output = run(
        ["docker", "ps", *filter_args, "--format", "{{.ID}} {{.Names}} {{.Image}}"],
        capture=True,
    ).stdout

    result = []
    for line in output.splitlines():
        if line:
            cid, name, image = line.split()
            result.append(dict(cid=cid, name=name, image=image))
    if not result:
        sys.exit("No running containers found")
    return sorted(result, key=lambda x: x["name"])


def _parse_selection(text):
    """Parse a selection like `1,3-4` into a list of indices; None if it is not one."""
    indices = []
    for term in "".join(text.split()).split(","):
        first, sep, last = term.partition("-")
        if not first.isdigit() or (sep and not last.isdigit()):
            return None
        indices.extend(range(int(first), int(last if sep else first) + 1))
    return indices


def _pick(containers, many):
    print("0 - exit")
    for idx, container in enumerate(containers):
        print(f"{idx + 1} - {container['name']}")
    print()

    if many:
        question = "Select one or more containers (e.g. 1,3-4): "
    else:
        question = "Select a container: "
    while True:
        try:
            text = input(question).strip()
        except EOFError:
            sys.exit(0)
        indices = _parse_selection(text)
        if indices == [0]:
            sys.exit(0)
        if (
            indices
            and (many or len(indices) == 1)
            and all(1 <= idx <= len(containers) for idx in indices)
        ):
            return [containers[idx - 1] for idx in indices]
        what = "numbers" if many else "a number"
        print(f"Please pick {what} between 1 and {len(containers)}")


def _select(name, many=False):
    containers = _containers()
    exact = [x for x in containers if x["name"] == name]
    if exact:
        return exact

    matches = [x for x in containers if name in x["name"]]
    if not matches:
        print(f"No container matches: {name}")
        matches = containers
    if len(matches) == 1:
        return matches
    return _pick(matches, many)


def exec_in_container(name, cmd, user):
    (container,) = _select(name)
    cmd = cmd or get("/docker/shell", default="sh")
    user_args = ["--user", user] if user else []
    # Pass on the exit code of the shell or command, without a traceback
    result = run(
        ["docker", "exec", "-it", *user_args, container["name"], *shlex.split(cmd)],
        check=False,
    )
    sys.exit(result.returncode)


def kill(name):
    for container in _select(name, many=True):
        run(["docker", "kill", container["name"]])


def inspect(name, ip):
    ip_args = (
        ["-f", "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"] if ip else []
    )
    for container in _select(name, many=True):
        run(["docker", "inspect", *ip_args, container["name"]])


def commit(name):
    (container,) = _select(name)
    run(["docker", "commit", container["cid"], container["image"]])


def _args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    exec_parser = subparsers.add_parser("exec")
    exec_parser.add_argument("--name", default="")
    exec_parser.add_argument("--cmd", default="")
    exec_parser.add_argument("--user", default="")

    kill_parser = subparsers.add_parser("kill")
    kill_parser.add_argument("--name", default="")

    inspect_parser = subparsers.add_parser("inspect")
    inspect_parser.add_argument("--name", default="")
    inspect_parser.add_argument("--ip", action="store_true")

    commit_parser = subparsers.add_parser("commit")
    commit_parser.add_argument("--name", default="")

    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    try:
        if args.action == "exec":
            exec_in_container(args.name, args.cmd, args.user)
        elif args.action == "kill":
            kill(args.name)
        elif args.action == "inspect":
            inspect(args.name, args.ip)
        else:
            commit(args.name)
    except CommandFailedError as e:
        # docker has already printed its error
        sys.exit(e.result.returncode)
    except KeyboardInterrupt:
        # ctrl-c cancels; end the line of the prompt instead of showing a traceback
        print()
        sys.exit(130)
