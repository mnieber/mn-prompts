# Skill: le-add-edit-config

Applies when adding a `jaz edit-config` target to a stack: it opens the stack's config files in an editor, so
that the developer does not have to look up where they live.

The `examples/blogs` stack has a complete setup. Copy its files and adapt the config.

---

## What the developer sees

```
$ jaz edit-config           # open the config files in the editor
```

## Files

```
<stack>/
    jazzoo                                      # root module: loads the config, exports edit-config
    env/local/config/base.yaml                  # the editor and the files to open
    env/local/jaz/edit_config/edit_config.jaz   # the edit-config target
    env/local/jaz/edit_config/edit_config.py    # the script that does the work
```

Copy `edit_config.jaz` and `edit_config.py` from `examples/blogs/env/local/jaz/edit_config/` unchanged. They
contain nothing that is specific to the stack.

## The root module

If the stack has no `jazzoo` file yet, create it. Otherwise add the missing lines to the existing one:

```
⚙️.load_config(path=⚙️.module.dirname / "env/local/config/base.yaml")

from ./env/local/jaz/edit_config/edit_config.jaz export edit-config
```

## The config

```yaml
# env/local/config/base.yaml
edit_config:
  editor: gedit
  files:
    - env/local/config/*.yaml
```

- `/edit_config/files` is required. It is a list of glob patterns; `**` matches any depth and a leading `~` is
  the home directory. A relative pattern is resolved against the directory of the root module.
- The files are opened in the order of the patterns, sorted within a pattern, and each file once. A pattern that
  matches nothing is skipped; when no pattern matches a file, the target fails.
- `/edit_config/editor` is a command line, so it may carry options (`code --new-window`). The files are added as
  extra arguments. When it is missing, `$VISUAL` and then `$EDITOR` are used.
- Both are config values, so they may use `${/...}` references and `${NAME}` environment variables.

RULE: list every config file that the developer may want to change, also the optional ones (e.g. a
`local.yaml` that `⚙️.load_config` loads with `required=false`), so that one command opens them all.

## How it works, and what to keep when changing it

`edit_config.jaz` calls `python3 edit_config.py --root-dir=<dir of the root module>`. The script reads
`/edit_config` with `from jazzoo import get_config`, expands the patterns, and starts the editor with
`from jazzoo import run`.

RULE: the `edit-config` target is `[interactive]`, and the script waits for the editor, so that an editor that
runs in the terminal (`vim`) works. A graphical editor that returns at once (`code`, an already running `gedit`)
just makes the target end early.

## Requirements

- The editor is installed.
- `python3` on the `PATH` has `jazzoo` installed, i.e. the venv with `jaz` is active.

## Checklist

- [ ] `edit_config.jaz` and `edit_config.py` copied to `env/local/jaz/edit_config/`
- [ ] `env/local/config/base.yaml` defines `/edit_config/files` (and optionally `/edit_config/editor`)
- [ ] The root `jazzoo` module loads the config and exports `edit-config`
- [ ] `jaz --list` shows `edit-config`
- [ ] `jaz edit-config` opens every config file of the stack in the editor
