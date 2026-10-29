"""Open a tmux session with a menu of commands.

`open` creates the session (if needed) and attaches to it. `pick` is the menu loop
that runs in the session's Menu window. The menu is read from /tmux/menu in the
config that the Jazzoo file loaded.
"""

import argparse
import os
import shutil
import subprocess
import sys
import time

from jazzoo import get_config as get

CONFIG_FILES_ENV_VAR = "JAZZOO_CONFIG_FILES"
MENU_WINDOW = "1"


def run(args, capture=False):
    """Run a command; raise on a non-zero exit code. Return stdout if capture is set.

    This is a stand-in for the `run` function that Jazzoo will provide.
    """
    completed = subprocess.run(args, check=True, capture_output=capture, text=True)
    return completed.stdout if capture else None


def _normalize(category):
    return category.replace(" ", "-")


def _get_commands_and_labels(category):
    menu = get("/tmux/menu")
    categories = [x for x in menu if category == "all" or _normalize(x) == category]
    if not categories:
        known = ", ".join(_normalize(x) for x in menu)
        sys.exit(f"Unknown category: {category} (known: {known})")

    label_size = max(len(x) for x in categories)
    commands, labels = [], []
    for name in categories:
        for command in menu[name]:
            commands.append(command)
            labels.append(f"{len(commands):>2} [{name:>{label_size}}] - {command}")

    if not commands:
        sys.exit("No commands found in /tmux/menu")
    return commands, labels


def _parse_selection(text):
    """Parse a selection like `1,3-4` into a list of indices; None if it is not one."""
    indices = []
    for term in "".join(text.split()).split(","):
        first, sep, last = term.partition("-")
        if not first.isdigit() or (sep and not last.isdigit()):
            return None
        indices.extend(range(int(first), int(last if sep else first) + 1))
    return indices


def _has_session(session):
    completed = subprocess.run(
        ["tmux", "has-session", "-t", session], capture_output=True
    )
    return completed.returncode == 0


def open_session(category, session):
    if not shutil.which("tmux"):
        sys.exit("tmux is not installed")

    session = session or get("/tmux/session")

    if not _has_session(session):
        # Fail before the session exists if the menu is empty or the category unknown
        _get_commands_and_labels(category)

        project_dir = os.getcwd()
        run(["tmux", "new-session", "-d", "-s", session, "-c", project_dir])
        # Panes are started by the tmux server, so they don't inherit our environment
        run(
            [
                "tmux",
                "set-environment",
                "-t",
                session,
                CONFIG_FILES_ENV_VAR,
                os.environ.get(CONFIG_FILES_ENV_VAR, ""),
            ]
        )
        window = f"{session}:{MENU_WINDOW}"
        run(["tmux", "new-window", "-t", window, "-n", "Menu", "-c", project_dir])
        pick_command = f"{sys.executable} {os.path.abspath(__file__)} pick --category={category}"
        run(["tmux", "send-keys", "-t", window, pick_command, "C-m"])

    if os.environ.get("TMUX"):
        run(["tmux", "switch-client", "-t", session])
    else:
        run(["tmux", "attach-session", "-t", session])


def pick(category):
    commands, labels = _get_commands_and_labels(category)
    menu_pane = os.environ["TMUX_PANE"]

    while True:
        run(["tmux", "send-keys", "-t", menu_pane, "-R", ""])
        print()
        for label in labels:
            print(label)
        print()

        while True:
            text = input(
                "Select one or more commands (e.g. 1,3-4), "
                "or type a command, or type 0 to exit: "
            ).strip()
            if not text:
                continue
            indices = _parse_selection(text)
            if indices is None:
                selected = [text]
                break
            if indices == [0]:
                return
            if all(1 <= idx <= len(commands) for idx in indices):
                selected = [commands[idx - 1] for idx in indices]
                break
            print(f"Please pick numbers between 1 and {len(commands)}")

        for command in selected:
            print(command)
            pane = run(
                ["tmux", "split-window", "-v", "-t", menu_pane, "-P", "-F", "#{pane_id}"],
                capture=True,
            ).strip()
            # Give the shell in the new pane time to start
            time.sleep(0.5)
            run(["tmux", "send-keys", "-t", pane, command, "C-m"])
            run(["tmux", "select-layout", "-t", menu_pane, "tiled"])

        run(["tmux", "select-pane", "-t", menu_pane])


def _args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    open_parser = subparsers.add_parser("open")
    open_parser.add_argument("--category", default="all")
    open_parser.add_argument("--session", default="")

    pick_parser = subparsers.add_parser("pick")
    pick_parser.add_argument("--category", default="all")

    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    if args.action == "open":
        open_session(args.category, args.session)
    else:
        pick(args.category)
