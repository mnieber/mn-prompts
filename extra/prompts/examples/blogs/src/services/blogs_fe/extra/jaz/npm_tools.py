"""Run the npm commands of blogs_fe in its container.

`publish` builds a package into a temp dir (the publish dir), shows what it contains,
logs in to npm when needed, asks for confirmation and publishes the publish dir. npm
asks for the second factor (2FA) itself.
"""

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

from jazzoo import CommandAbortedError, CommandError, CommandFailedError, run

# The files that are published next to the output of tsc
EXTRA_FILES = ["README.md", "LICENSE"]


def publish(package_dir):
    package_dir = Path(package_dir)
    manifest_path = package_dir / "package.json"
    if not manifest_path.exists():
        sys.exit(f"No package.json in {package_dir}")

    manifest = json.loads(manifest_path.read_text())
    name, version = manifest["name"], manifest["version"]

    if _is_on_registry(name, version):
        sys.exit(f"{name}@{version} is already on the registry: bump the version")

    with tempfile.TemporaryDirectory(prefix="npm-publish-") as publish_dir:
        publish_dir = Path(publish_dir)
        _build(package_dir, publish_dir, manifest)

        registry = _npm_output(["config", "get", "registry"])
        print(f"Package:  {name}@{version}")
        print(f"Registry: {registry}")
        print("Files:")
        for path in sorted(x for x in publish_dir.rglob("*") if x.is_file()):
            print(f"  {path.relative_to(publish_dir)}")

        user = _logged_in_user()
        print(f"npm user: {user}")

        if not _confirm(f"Publish {name}@{version}? This can't be undone. [y/N] "):
            sys.exit("Publish aborted")

        run(["npm", "publish"], cwd=str(publish_dir))
        print(f"Published {name}@{version}")


def _is_on_registry(name, version):
    result = run(
        ["npm", "view", f"{name}@{version}", "version"], capture=True, check=False
    )
    if result.stdout.strip():
        return True
    if result.returncode != 0 and "E404" not in result.stderr:
        sys.exit(f"Could not check the registry:\n{result.stderr}")
    return False


def _build(package_dir, publish_dir, manifest):
    tsc = package_dir / "node_modules/.bin/tsc"
    if not tsc.exists():
        sys.exit(f"No tsc in {package_dir}: install the packages of this package first")

    print(f"Building {package_dir}")
    run([str(tsc), "-p", ".", "--outDir", str(publish_dir)], cwd=str(package_dir))

    for filename in EXTRA_FILES:
        if (package_dir / filename).exists():
            shutil.copy2(package_dir / filename, publish_dir / filename)

    (publish_dir / "package.json").write_text(
        json.dumps(_publish_manifest(manifest), indent=2) + "\n"
    )


def _publish_manifest(manifest):
    """The development condition points to TypeScript source that isn't published."""
    result = json.loads(json.dumps(manifest))
    for conditions in result.get("exports", {}).values():
        if isinstance(conditions, dict):
            conditions.pop("development", None)
    return result


def _logged_in_user():
    user = _npm_output(["whoami"], check=False)
    if not user:
        print("You are not logged in to npm.")
        run(["npm", "login"])
        user = _npm_output(["whoami"])
    return user


def _npm_output(args, check=True):
    result = run(["npm", *args], capture=True, check=False)
    if check and result.returncode != 0:
        sys.exit(f"npm {' '.join(args)} failed:\n{result.stderr}")
    return result.stdout.strip() if result.returncode == 0 else ""


def _confirm(question):
    try:
        return input(question).strip().lower() == "y"
    except (KeyboardInterrupt, EOFError):
        print()
        return False


def _args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action", required=True)

    publish_parser = subparsers.add_parser("publish")
    publish_parser.add_argument("--package-dir", required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = _args()
    try:
        if args.action == "publish":
            publish(args.package_dir)
    except CommandFailedError as e:
        # The command has already printed its error
        sys.exit(e.result.returncode)
    except CommandAbortedError:
        sys.exit("Publish aborted")
    except CommandError as e:
        sys.exit(str(e))
