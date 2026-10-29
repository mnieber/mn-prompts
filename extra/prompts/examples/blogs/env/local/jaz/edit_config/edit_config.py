"""Open the config files of the project in an editor.

The editor and the glob patterns of the files are read from /edit_config in the
config that the Jazzoo file loaded. A relative pattern is resolved against the
directory of the root module.
"""

import argparse
import glob
import os
import shlex
import sys

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


def _args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root-dir", default=os.getcwd())
    return parser.parse_args()


if __name__ == "__main__":
    edit_config(_args().root_dir)
