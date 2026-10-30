"""Run the docker compose commands of the project.

The compose files live in env/local/docker. Which of them a command uses follows
the layers of the local env: the base file, the src overlays, the Dockerfile.local
images (when local is on) and the developer's override file. Local is on when
--local is true, or when it is empty and /compose/use_dockerfile_local is true.

Before build, up, down, run and init, the .env.in files are compiled into .env files.

Init starts the stack with the init-stack file last: each service runs init-dev and
then its server, and docker compose waits until the healthchecks pass.
"""

import argparse
import os
import shlex
import sys
import urllib.request
import webbrowser
from pathlib import Path

from jazzoo import CommandFailedError
from jazzoo import get_config as get
from jazzoo import run

COMPOSE_YML = "docker-compose.yml"
BASE_IMAGES_YML = "docker-compose.base-images.yml"
DOCKERFILE_LOCAL_YML = "docker-compose.dockerfile-local.yml"
SRC_OVERLAYS_YML = "docker-compose.src-overlays.yml"
OVERRIDE_YML = "docker-compose.override.yml"
INIT_STACK_YML = "docker-compose.init-stack.yml"

INIT_WAIT_TIMEOUT = "600"
DEFAULT_HOMEPAGE = "http://localhost:3000/"


def _compose_dir(root_dir):
    return Path(root_dir) / "env/local/docker"


def _is_local(local):
    if local == "":
        return bool(get("/compose/use_dockerfile_local", default=False))
    return local == "true"


def _compose(root_dir, files, args, is_build=False, check=True):
    file_args = []
    for filename in files:
        file_args += ["--file", str(_compose_dir(root_dir) / filename)]
    env = dict(
        ROOT_DIR=str(root_dir),
        COMPOSE_PROJECT_NAME=get("/docker/compose_project"),
        DOCKER_BUILDKIT="1",
    )
    if is_build:
        env["COMPOSE_BAKE"] = "true"
    return run(
        ["docker", "compose", *file_args, *args], env=env, check=check, echo=True
    )


def _run_files(root_dir, local):
    """The compose files of the commands that run containers."""
    return [
        COMPOSE_YML,
        SRC_OVERLAYS_YML,
        *([DOCKERFILE_LOCAL_YML] if _is_local(local) else []),
        OVERRIDE_YML,
    ]


def compile_env_files(root_dir):
    local_dir = Path(root_dir) / "env/local"
    secrets_env = local_dir / "secrets.env"
    secrets_env.touch()
    run(
        [
            sys.executable,
            str(local_dir / "scripts/compile_env_files.py"),
            f"--input={secrets_env}",
            str(local_dir / "docker/env_files"),
        ]
    )


def build(root_dir, local, no_cache):
    compile_env_files(root_dir)
    files = [COMPOSE_YML, *([DOCKERFILE_LOCAL_YML] if _is_local(local) else [])]
    no_cache_args = ["--no-cache"] if no_cache else []
    _compose(root_dir, files, ["--progress=plain", "build", *no_cache_args], True)


def build_base_images(root_dir, no_cache):
    build_args = []
    for name in ("os_custom_packages", "pip_custom_packages"):
        value = get(f"/compose/{name}", default="")
        if value:
            build_args += ["--build-arg", f"{name.upper()}={value}"]
    no_cache_args = ["--no-cache"] if no_cache else []
    _compose(
        root_dir,
        [BASE_IMAGES_YML],
        ["--progress=plain", "build", *build_args, *no_cache_args],
        True,
    )


def up(root_dir, local):
    (_compose_dir(root_dir) / OVERRIDE_YML).touch()
    compile_env_files(root_dir)
    _compose(root_dir, _run_files(root_dir, local), ["up"])


def down(root_dir, volumes):
    compile_env_files(root_dir)
    files = [COMPOSE_YML, SRC_OVERLAYS_YML, OVERRIDE_YML]
    volumes_args = ["--volumes"] if volumes else []
    _compose(root_dir, files, ["down", "--remove-orphans", *volumes_args])


def run_in_container(root_dir, service, cmd, local):
    compile_env_files(root_dir)
    args = ["run", "--rm", "--remove-orphans", "--service-ports", service]
    _compose(root_dir, _run_files(root_dir, local), [*args, *shlex.split(cmd)])


def init(root_dir, local):
    (_compose_dir(root_dir) / OVERRIDE_YML).touch()
    compile_env_files(root_dir)
    files = [*_run_files(root_dir, local), INIT_STACK_YML]
    args = ["up", "--detach", "--force-recreate", "--wait"]
    try:
        _compose(root_dir, files, [*args, "--wait-timeout", INIT_WAIT_TIMEOUT])
    except CommandFailedError:
        # Show why a service did not become healthy
        _compose(root_dir, files, ["logs", "--tail=50"], check=False)
        raise

    homepage = get("/compose/init/homepage", default=DEFAULT_HOMEPAGE)
    # Ask for html, as a browser does: the Vite dev server answers 404 otherwise
    request = urllib.request.Request(homepage, headers={"Accept": "text/html"})
    try:
        with urllib.request.urlopen(request, timeout=10):
            pass
    except OSError as e:
        print(f"The stack is healthy, but {homepage} failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\nThe stack is initialised, and its servers run: {homepage}")
    if sys.stdin.isatty():
        answer = input(f"Open {homepage} in the browser? [Y/n] ")
        if answer.strip().lower() in ("", "y", "yes"):
            webbrowser.open(homepage)
    print("'docker logs -f <container>' shows the output of a server.")
    print("'jaz compose.up' goes back to starting the servers yourself.")


def _args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    def add_parser(name):
        result = subparsers.add_parser(name)
        result.add_argument("--root-dir", required=True)
        return result

    build_parser = add_parser("build")
    build_parser.add_argument("--local", default="")
    build_parser.add_argument("--no-cache", action="store_true")

    build_base_images_parser = add_parser("build-base-images")
    build_base_images_parser.add_argument("--no-cache", action="store_true")

    up_parser = add_parser("up")
    up_parser.add_argument("--local", default="")

    down_parser = add_parser("down")
    down_parser.add_argument("--volumes", action="store_true")

    run_parser = add_parser("run")
    run_parser.add_argument("--service", required=True)
    run_parser.add_argument("--cmd", default="")
    run_parser.add_argument("--local", default="")

    init_parser = add_parser("init")
    init_parser.add_argument("--local", default="")

    add_parser("compile-env-files")

    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    try:
        if args.action == "build":
            build(args.root_dir, args.local, args.no_cache)
        elif args.action == "build-base-images":
            build_base_images(args.root_dir, args.no_cache)
        elif args.action == "up":
            up(args.root_dir, args.local)
        elif args.action == "down":
            down(args.root_dir, args.volumes)
        elif args.action == "run":
            run_in_container(args.root_dir, args.service, args.cmd, args.local)
        elif args.action == "init":
            init(args.root_dir, args.local)
        else:
            compile_env_files(args.root_dir)
    except CommandFailedError as e:
        # The command has already printed its error
        sys.exit(e.result.returncode)
