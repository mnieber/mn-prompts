import argparse
import sys
import traceback
from pathlib import Path

from mn_prompts.prompts.rules.get_agents_file import get_agents_file
from mn_prompts.targets.actions.copy_agents_file import copy_agents_file
from mn_prompts.targets.actions.install_target import install_target
from mn_prompts.targets.rules.get_target_names import get_target_names


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        description="mn-prompts - Install code generation prompts in a project"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    subparsers.required = True

    # Install command
    install_parser = subparsers.add_parser(
        "install", help="Install the instructions of a target in the cwd"
    )
    install_parser.add_argument("target_name", help="Name of the target")

    # List command
    subparsers.add_parser("list", help="List the available targets")

    # Global arguments
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )

    return parser.parse_args(argv)


def run(argv=None):
    args = _parse_args(argv)

    if args.command == "install":
        project_dir = Path.cwd()
        install_target(args.target_name, project_dir)
        if not copy_agents_file(project_dir):
            print(
                "AGENTS.md already exists, so it was not replaced. Extend it with "
                f"the contents of {get_agents_file()}",
                file=sys.stderr,
            )

    if args.command == "list":
        for target_name in get_target_names():
            print(target_name)

    return 0


def main(argv=None):
    # Runs the tool for the user: errors are printed instead of raised
    try:
        return run(argv)
    except Exception as error:
        args = sys.argv[1:] if argv is None else argv
        verbose = any(arg.startswith("-v") or arg == "--verbose" for arg in args)
        if verbose:
            traceback.print_exc()
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        if not verbose:
            print("Hint: run with -v to see the traceback.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
