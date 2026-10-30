# Skill: le-manage-jazzoo-configs

Applies when adding the `jaz config.*` targets to a stack: they open the stack's
config files in an editor, and print the config that the stack's scripts see.

The `examples/blogs` stack has a complete setup. Copy its files and adapt the config.

---

## What the developer sees

```
$ jaz config.edit               # open the config files in the editor
$ jaz config.print              # print the whole config, with every value expanded
$ jaz config.print /tmux/menu   # print the part of the config at a path
$ jaz config.print to-file=/tmp/config.json   # write it to a file instead
```

`jaz --list config` lists the targets.

## Which config `config.print` shows

`config.print` shows the config that a script would see at the moment it runs, i.e. the files that are in the
config list at that point, merged in their order:

- From the command line, these are the files that the Jazzoo modules load at the top level: the config that
  every target starts with. A file that a function loads in its body is not shown.
- Called from a function, it also shows the files that the function loaded before the call. This makes it a
  debug helper: insert a call into a target to see the config that its scripts get.

```
from ./env/local/jaz/config/config.jaz import * as config

deploy():
    ⚙️.load_config(path=⚙️.module.dirname / "env/local/config/deploy.yaml")
    # debug: remove when done
    🐭.config.print(to-file="/tmp/config.json")
    ⚙️.python deploy.py
```

Use `to-file` when the target prints other output, so that the config does not get mixed into it.

RULE: do not make `config.print` load the files of `/edit_config/files`. That list holds every file a
developer may want to edit, which may include alternatives (`deploy.dev.yaml`, `deploy.prod.yaml`) that are
never loaded together, and its order is not the order in which they are loaded. Merging them gives a config
that no script ever sees.

## Files

```
<stack>/
    jazzoo                               # root module: loads the config, exports the config layer
    env/local/config/base.yaml           # the editor and the files to open
    env/local/jaz/config/config.jaz      # the config.* targets
    env/local/jaz/config/config_tools.py # the script that does the work
```

Copy `config.jaz` and `config_tools.py` from `examples/blogs/env/local/jaz/config/` unchanged. They contain
nothing that is specific to the stack.

## The root module

If the stack has no `jazzoo` file yet, create it. Otherwise add the missing lines to the existing one:

```
⚙️.load_config(path=⚙️.module.dirname / "env/local/config/base.yaml")

from ./env/local/jaz/config/config.jaz export * as config
```

## The config

`config.print` needs no settings. `config.edit` reads `/edit_config`:

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

`config.jaz` calls `⚙️.python config_tools.py edit --root-dir=<dir of the root module>` and
`⚙️.python config_tools.py print --path=<path> --to-file=<file>`. The script reads the config with
`from jazzoo import get_config`, and starts the editor with `from jazzoo import run`.

`print` prints the value at the path as JSON (`json.dumps(indent=2)`), so that the script needs only the
standard library, and its output can be piped into `jq`. Every value is expanded, so the output shows what a
script would get from `get_config`. A path that does not exist, or a value that cannot be expanded (e.g. an
unset environment variable), makes the target fail with the message of `get_config`. Printing a part of the
config avoids a broken value elsewhere.

RULE: both targets are `[interactive]`, so that `jaz` does not capture their output. The `edit` script waits
for the editor, so that an editor that runs in the terminal (`vim`) works. A graphical editor that returns at
once (`code`, an already running `gedit`) just makes the target end early.

RULE: `config.print` quotes its `path` and `to-file` arguments with `⚙️.sh-quote`, because they are
command-line arguments.

## Requirements

- The editor is installed.
- `jaz` is installed. The scripts run with `⚙️.python`, the Python that runs `jaz`, so they can import `jazzoo`.

## Checklist

- [ ] `config.jaz` and `config_tools.py` copied to `env/local/jaz/config/`
- [ ] `env/local/config/base.yaml` defines `/edit_config/files` (and optionally `/edit_config/editor`)
- [ ] The root `jazzoo` module loads the config and exports the `config` layer
- [ ] `jaz --list config` shows `config.edit` and `config.print`
- [ ] `jaz config.edit` opens every config file of the stack in the editor
- [ ] `jaz config.print` prints the config
