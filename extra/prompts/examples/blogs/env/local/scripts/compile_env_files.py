#!/usr/bin/env python3
"""
Compiles .env.in template files into .env files by expanding environment variables.

Usage:
    python compile_env_files.py --input=./secrets.env ./env_files_dir

The --input flag can be used multiple times to load variables from multiple files.
Variables from input files are loaded into the environment before rendering templates.
"""

import argparse
import glob
import os
import re

try:
    from expandvars import expandvars
except ImportError:
    raise ImportError(
        "The expandvars module was not found. Please install it into your local env "
        + "with `pip install expandvars`."
    )

header_block = """# This file is auto-generated. Do not edit directly.
# To modify, edit the corresponding .env.in file and re-run `just compile-env-files`.
#
# This file may contain secrets. Handle with care.
#
# DO NOT COMMIT TO VERSION CONTROL.
#
"""


def get_lines(f):
    """Parse env file content, handling multi-line quoted strings."""
    quote = None
    escape = False
    line = ""

    for char in f.read():
        line += char

        if char == "\n":
            if quote:
                continue
            yield line
            line, quote, escape = "", None, False
        elif quote and escape:
            escape = False
        elif quote and char == "\\":
            escape = True
        elif char == "'" or char == '"':
            if quote and quote == char:
                quote = None
            elif not quote:
                quote = char
    yield line


def compile_env_line(env_line, is_strict=True):
    """Parse an env line and set the variable in os.environ."""
    regex = r"(export\s*)?([^=]+)=(.*)"
    matches = list(re.finditer(regex, env_line, re.DOTALL))

    if len(matches) == 1:
        groups = matches[0].groups()
        key = groups[1].strip()
        value = expandvars(groups[2], nounset=is_strict)
        os.environ[key] = value
        return True

    return False


def load_input_file(file_path, is_strict=True):
    """Load variables from an env file into os.environ."""
    with open(file_path) as f:
        for env_line in get_lines(f):
            stripped = env_line.strip()
            if stripped and not stripped.startswith("#"):
                compile_env_line(stripped, is_strict)


def render_file(file_path, is_strict=True):
    """Render an env template file by expanding variables."""
    content = header_block
    with open(file_path) as f:
        for env_line in get_lines(f):
            if env_line.strip().startswith("#"):
                output_line = env_line
            else:
                output_line = expandvars(env_line, nounset=is_strict)
            content += output_line
    return content


def main():
    parser = argparse.ArgumentParser(
        description="Compile .env.in templates into .env files"
    )
    parser.add_argument(
        "--input",
        action="append",
        dest="input_files",
        default=[],
        help="Input file(s) containing variables to load (can be used multiple times)",
    )
    parser.add_argument(
        "env_files_dir",
        help="Directory containing .env.in files to compile",
    )

    args = parser.parse_args()

    # Load variables from input files
    for input_file in args.input_files:
        if not os.path.exists(input_file):
            print(f"Error: Input file not found: {input_file}")
            return 1
        load_input_file(input_file)

    # Find and render all .env.in files
    pattern = os.path.join(args.env_files_dir, "*.env.in")
    env_in_files = glob.glob(pattern)

    if not env_in_files:
        print(f"No .env.in files found in {args.env_files_dir}")
        return 0

    for env_in_file in sorted(env_in_files):
        output_file = env_in_file[:-3]  # Remove ".in" suffix
        existing_content = ""
        if os.path.exists(output_file):
            with open(output_file, "r") as f:
                existing_content = f.read()

        content = render_file(env_in_file)
        if content != existing_content:
            with open(output_file, "w") as f:
                f.write(content)
            print(f"Compiled: {env_in_file} -> {output_file}")

    print(f"Compiled {len(env_in_files)} file(s)")
    return 0


if __name__ == "__main__":
    exit(main())
