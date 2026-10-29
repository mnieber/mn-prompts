"""Edit and print the config of the project.

`edit` opens the config files in an editor. The editor and the glob patterns of
the files are read from /edit_config in the config that the Jazzoo file loaded. A
relative pattern is resolved against the directory of the root module.

`print` prints the merged config, or the part of it at a path, with every value
expanded, as JSON. It shows the files that are in the config list when it runs:
from the command line, the files that the Jazzoo modules load at the top level.
Called from a function, also the files that the function loaded before the call.
"""

import argparse
import glob
import json
import os
import shlex
import sys

from jazzoo import ConfigError
from jazzoo import get_config as get
from jazzoo import run


def _get_editor():
    editor = get("/edit_config/editor", default=None)
    editor = editor or os.environ.get("VISUAL") or os.environ.get("EDITOR")
    if not editor:
        sys.exit("No editor: set /edit_config/editor, $VISUAL or $EDITOR")
    return shlex.split(editor)


def _get_files(root_dir):
    files = []
    for pattern in get("/edit_config/files"):
        pattern = os.path.join(root_dir, os.path.expanduser(pattern))
        for path in sorted(glob.glob(pattern, recursive=True)):
            path = os.path.abspath(path)
            if os.path.isfile(path) and path not in files:
                files.append(path)

    if not files:
        sys.exit("No files match the patterns in /edit_config/files")
    return files


def edit_config(root_dir):
    editor = _get_editor()
    files = _get_files(root_dir)
    # Wait for the editor, so that an editor that runs in the terminal works
    run([*editor, *files])


def print_config(path, to_file):
    try:
        value = get(path)
    except (ConfigError, ValueError) as e:
        sys.exit(str(e))

    text = json.dumps(value, indent=2)
    if to_file:
        with open(to_file, "w") as f:
            f.write(text + "\n")
    else:
        print(text)


def _args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    edit_parser = subparsers.add_parser("edit")
    edit_parser.add_argument("--root-dir", default=os.getcwd())

    print_parser = subparsers.add_parser("print")
    print_parser.add_argument("--path", default="/")
    print_parser.add_argument("--to-file", default="")

    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    if args.action == "edit":
        edit_config(args.root_dir)
    else:
        print_config(args.path, args.to_file)
