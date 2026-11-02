import argparse
import sys
import traceback
from pathlib import Path

from mn_prompts.instructions.actions.add_to_git_ignore import add_to_git_ignore
from mn_prompts.instructions.actions.copy_agents_file import copy_agents_file
from mn_prompts.instructions.actions.install_instructions import install_instructions
from mn_prompts.layers.rules.get_layer_names import get_layer_names
from mn_prompts.prompts.rules.get_agents_file import get_agents_file
from mn_prompts.targets.rules.get_target import get_target
from mn_prompts.targets.rules.get_target_names import get_target_names


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        description="mn-prompts - Install code generation prompts in a project"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    subparsers.required = True

    # Install command
    install_parser = subparsers.add_parser(
        "install",
        help="Install the instructions of a target and/or layers in the cwd. Without "
        "a target and layers, the earlier selection is re-installed",
    )
    install_parser.add_argument("--target", help="Name of the target")
    install_parser.add_argument(
        "--layer",
        action="append",
        default=[],
        help="Name of a layer (can be repeated)",
    )
    install_parser.add_argument(
        "--agents-md",
        action="store_true",
        help="Copy the agents file to AGENTS.md instead of CLAUDE.md",
    )
    install_parser.add_argument(
        "--git-ignore",
        action="store_true",
        help="Add the agents file and the instructions dir to the .gitignore of the cwd",
    )

    # List command
    subparsers.add_parser("list", help="List the available targets and layers")

    # Global arguments
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity"
    )

    return parser.parse_args(argv)


def _print_targets_and_layers():
    targets = [get_target(target_name) for target_name in get_target_names()]
    name_width = max((len(target.name) for target in targets), default=0)
    description_width = max((len(target.description) for target in targets), default=0)

    print("Targets:")
    for target in targets:
        print(
            f"  {target.name:<{name_width}}  "
            f"{target.description:<{description_width}}  "
            f"({', '.join(target.layer_names)})"
        )
    print("Layers:")
    for layer_name in get_layer_names():
        print(f"  {layer_name}")


def run(argv=None):
    args = _parse_args(argv)

    if args.command == "install":
        project_dir = Path.cwd()
        manifest = install_instructions(
            project_dir, args.target, args.layer, args.agents_md
        )
        if not copy_agents_file(project_dir, manifest.agents_file_name):
            print(
                f"{manifest.agents_file_name} already exists, so it was not replaced. "
                f"Extend it with the contents of {get_agents_file()}",
                file=sys.stderr,
            )
        if args.git_ignore:
            add_to_git_ignore(
                project_dir, [f"/{manifest.agents_file_name}", "/instructions/"]
            )

    if args.command == "list":
        _print_targets_and_layers()

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
