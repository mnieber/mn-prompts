# Skill: py-publish-to-pypi

Applies when preparing a Python library for PyPI, publishing it, or adding the `jaz python.publish` target to a
project.

The `examples/blogs` stack has the target. Copy its files and adapt the config.

---

## What the developer sees

```
$ jaz python.publish package-dir=src/libs/python_toolkit
Building /path/to/blogs/src/libs/python_toolkit
Built python_toolkit-0.2.0-py3-none-any.whl
Built python_toolkit-0.2.0.tar.gz
Uploading to https://upload.pypi.org/legacy/ as __token__
Password:
Uploaded python_toolkit-0.2.0-py3-none-any.whl, python_toolkit-0.2.0.tar.gz
```

- `package-dir` is required. A relative path is relative to the root dir of the project (the dir of the root
  `jazzoo` file), an absolute path is used as it is.
- The target builds the sdist and the wheel with `uv build` into a temp dir, and uploads exactly these files
  with `uv publish`. Old files in the `dist/` dir of the library are never uploaded.
- The names of the built files show the package name and version before the password is asked.
- The password is not echoed, and is never stored. An empty password (or Ctrl+C) aborts the upload.
- For PyPI, the user name is `__token__` and the password is an API token, which the developer creates in their
  PyPI account settings. PyPI doesn't accept account passwords for uploads.

**When to use it.** Publishing changes a public index and can't be undone: a version can be yanked, but its
number can never be reused. **RULE:** Only run `python.publish` when the developer asks, and never type the
password for them. Since the target asks for the password in the terminal, the developer runs it themselves.

## Preparing the library

PyPI shows the `[project]` metadata of the `pyproject.toml` on the page of the package:

```toml
[project]
name = "python_toolkit"
version = "0.2.0"
description = "Logging helpers for the services of the blogs stack"
readme = "README.md"
authors = [{ name = "Jane Doe", email = "jane@example.com" }]
license = "MIT"
requires-python = ">=3.10"
dependencies = ["requests>=2.31.0"]

[project.urls]
Homepage = "https://github.com/example/python_toolkit"
```

- `name` must be free on PyPI (search for it first). It is the name that users `pip install`.
- `authors` is the author of the package. It lives in the `pyproject.toml` of each library, not in the jazzoo
  config.
- `readme` is rendered as the description on PyPI.

**RULE:** Bump `version` before each publish. PyPI never accepts the same version twice, and the upload of an
existing version fails.

## The config

```yaml
# env/local/config/base.yaml
python:
  pypi:
    username: __token__
    publish_url: https://upload.pypi.org/legacy/
```

- `/python/pypi/username` is the user name of the upload.
- `/python/pypi/publish_url` is the upload url of the index.

To upload to another index (e.g. TestPyPI, to try out a release), the developer overrides the settings in their
own `local.yaml` (see [le-use-compose-ops](../../local_env/skills/le-use-compose-ops.md)):

```yaml
# env/local/config/local.yaml
python:
  pypi:
    publish_url: https://test.pypi.org/legacy/
```

**RULE:** There is no setting, `secrets.env` entry or environment variable for the password: it is always typed
at the prompt.

## Adding the target to a project

```
<project>/
    jazzoo                          # loads base.yaml (+ local.yaml), exports python
    env/local/
        config/base.yaml            # /python/pypi
        jaz/python/python.jaz       # the python targets, among which publish
        jaz/python/python_tools.py  # the script that does the work
```

**RULE:** Copy `python.jaz` and `python_tools.py` from `examples/blogs/env/local/jaz/python/` as they are, and
add the `/python/pypi` section to `base.yaml`. The root `jazzoo` file exports the layer:

```
⚙️.load_config(path=⚙️.module.dirname / "env/local/config/base.yaml")
⚙️.load_config(path=⚙️.module.dirname / "env/local/config/local.yaml", required=false)

from ./env/local/jaz/python/python.jaz export * as python
```

## How the target works

`python.jaz` calls `⚙️.python python_tools.py publish --root-dir=<root dir> --package-dir=<package dir>`. The
script:

1. fails with a short message when the package dir has no `pyproject.toml`;
2. runs `uv build --out-dir=<temp dir> <package dir>`, and prints the built files;
3. asks for the password with `getpass`;
4. runs `uv publish --publish-url=<publish url> --username=<username> <the built files>`, with the password in
   `UV_PUBLISH_PASSWORD` (not in the args, where other users could see it in the process list);
5. removes the temp dir.

A failing `uv` ends the target without a traceback: `uv` has already printed the reason.

## Requirements

- `jaz` is installed, and `uv` is on the `PATH`.

## Checklist

- [ ] The `[project]` metadata has `name`, `version`, `description`, `readme`, `authors` and `license`
- [ ] The version is bumped
- [ ] `python.jaz` and `python_tools.py` are copied as they are
- [ ] `base.yaml` has `/python/pypi/username` and `/python/pypi/publish_url`
- [ ] The developer runs `jaz python.publish` themselves, and types the token
