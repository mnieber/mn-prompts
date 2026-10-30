"""Dial: the function keys of the shell, configured per project.

`get` prints the value of a key in /dial/<group>/<number>, with `~` and the config
references expanded. With --dir, a relative value is resolved against the root
directory of the project. An unknown key prints nothing, so that a key binding can
ignore it.

`install-fish` copies the fish functions next to this script into the fish config
directory, and writes the key bindings to conf.d/dial_bindings.fish: F<n> inserts
the value of group default, shift-F<n> and ctrl-F<n> cd to the directory of group
shift and ctrl. It only overwrites files that it wrote itself.
"""

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys

from jazzoo import ConfigError
from jazzoo import get_config as get

MARKER = "# managed by zoo dial.install-fish"
NR_OF_KEYS = 12

# The escape sequences of shift-F<n> and ctrl-F<n> in xterm-like terminals, for fish 3
# (fish 4 names these keys). {m} is the modifier: 2 for shift, 5 for ctrl.
FISH3_SEQUENCES = [
    r"\e\[1\;{m}P",
    r"\e\[1\;{m}Q",
    r"\e\[1\;{m}R",
    r"\e\[1\;{m}S",
    r"\e\[15\;{m}~",
    r"\e\[17\;{m}~",
    r"\e\[18\;{m}~",
    r"\e\[19\;{m}~",
    r"\e\[20\;{m}~",
    r"\e\[21\;{m}~",
    r"\e\[23\;{m}~",
    r"\e\[24\;{m}~",
]


def get_value(group, number, root_dir, as_dir):
    try:
        keys = get(f"/dial/{group}", default={})
    except ConfigError as e:
        sys.exit(str(e))

    # YAML may give the keys as numbers or strings
    for key, value in keys.items():
        # A bare ~ in YAML is null, not the home directory
        if str(key) == number and value is not None:
            value = os.path.expanduser(str(value))
            if as_dir:
                value = os.path.normpath(os.path.join(root_dir, value))
            print(value)
            return


def _get_fish_config_dir():
    config_home = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return os.path.join(config_home, "fish")


def _get_fish_major_version():
    output = subprocess.run(
        ["fish", "--version"], capture_output=True, text=True, check=True
    ).stdout
    match = re.search(r"version (\d+)", output)
    if not match:
        sys.exit(f"Cannot read the fish version from: {output}")
    return int(match.group(1))


def _get_bindings(fish_major_version):
    lines = [
        MARKER,
        "# F<n>: insert the value of dial key <n> of group default",
        "# shift-F<n>, ctrl-F<n>: cd to the directory of dial key <n> of group shift, ctrl",
    ]
    for n in range(1, NR_OF_KEYS + 1):
        if fish_major_version >= 4:
            keys = [f"f{n}", f"shift-f{n}", f"ctrl-f{n}"]
        else:
            keys = [
                f"-k f{n}",
                FISH3_SEQUENCES[n - 1].format(m=2),
                FISH3_SEQUENCES[n - 1].format(m=5),
            ]
        lines.append(f'bind {keys[0]} "dial_insert {n}"')
        lines.append(f'bind {keys[1]} "dial_cd shift {n}"')
        lines.append(f'bind {keys[2]} "dial_cd ctrl {n}"')
    return "\n".join(lines) + "\n"


def _is_managed(path):
    with open(path) as f:
        return f.readline().strip() == MARKER


def _find_old_dial_bindings(fish_config_dir):
    paths = [
        os.path.join(fish_config_dir, "functions", "fish_user_key_bindings.fish"),
        *glob.glob(os.path.join(fish_config_dir, "conf.d", "*.fish")),
    ]
    return [
        path
        for path in paths
        if os.path.isfile(path)
        and not _is_managed(path)
        and re.search(r"\bdial_", open(path).read())
    ]


def install_fish(fish_dir):
    fish_config_dir = _get_fish_config_dir()
    sources = sorted(glob.glob(os.path.join(fish_dir, "*.fish")))
    targets = {
        os.path.join(fish_config_dir, "functions", os.path.basename(source)): source
        for source in sources
    }
    bindings_file = os.path.join(fish_config_dir, "conf.d", "dial_bindings.fish")

    # Never overwrite a file that the developer wrote
    foreign = [
        path
        for path in [*targets, bindings_file]
        if os.path.exists(path) and not _is_managed(path)
    ]
    if foreign:
        sys.exit(
            "These files exist and were not written by dial.install-fish. "
            "Remove them first:\n" + "\n".join(f"  {path}" for path in foreign)
        )

    for target, source in targets.items():
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copyfile(source, target)
        print(f"Wrote {target}")

    os.makedirs(os.path.dirname(bindings_file), exist_ok=True)
    with open(bindings_file, "w") as f:
        f.write(_get_bindings(_get_fish_major_version()))
    print(f"Wrote {bindings_file}")

    old = _find_old_dial_bindings(fish_config_dir)
    if old:
        print(
            "\nThese files also bind dial keys. Remove those bindings, so that they "
            "do not override the new ones:\n" + "\n".join(f"  {path}" for path in old)
        )
    print("\nOpen a new fish shell to use the bindings.")


def _args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("--group", required=True)
    get_parser.add_argument("--number", required=True)
    get_parser.add_argument("--root-dir", default=os.getcwd())
    get_parser.add_argument("--dir", action="store_true")

    install_parser = subparsers.add_parser("install-fish")
    install_parser.add_argument("--fish-dir", required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    if args.action == "get":
        get_value(args.group, args.number, args.root_dir, args.dir)
    else:
        install_fish(args.fish_dir)
