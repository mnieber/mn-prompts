# Skill: le-add-tmux-menu

Applies when adding a `jaz tmux` target to a stack: a tmux session with a menu of commands, where each picked
command runs in its own pane next to the menu.

The `examples/blogs` stack has a complete setup. Copy its files and adapt the config.

---

## What the developer sees

```
$ jaz tmux                  # create the session (if needed) and attach to it
$ jaz tmux examples         # only show the "examples" category in the menu
$ jaz tmux session=other    # use a different session name
```

Window 1 (`Menu`) shows the numbered commands. The developer picks one or more (`1,3-4`), or types a command,
and each command is typed into a new pane. Running `jaz tmux` again re-attaches to the existing session.

## Files

```
<stack>/
    jazzoo                          # root module: loads the config, exports tmux
    env/local/config/base.yaml      # the session name and the menu
    env/local/jaz/tmux/tmux.jaz     # the tmux target
    env/local/jaz/tmux/tmux_menu.py # the script that does the work
```

Copy `tmux.jaz` and `tmux_menu.py` from `examples/blogs/env/local/jaz/tmux/` unchanged. They contain nothing
that is specific to the stack.

## The root module

If the stack has no `jazzoo` file yet, create it. Otherwise add the two lines to the existing one:

```
⚙️.load_config(path=⚙️.module.dirname / "env/local/config/base.yaml")

from ./env/local/jaz/tmux/tmux.jaz export tmux
```

## The config

```yaml
# env/local/config/base.yaml
tmux:
  session: <stack_name>
  menu:
    serve:
      - jaz be.serve
      - jaz fe.serve
    shells:
      - jaz be.shell
```

- `/tmux/session` is required.
- `/tmux/menu` maps a category to a list of shell lines. The order in the file is the order of the menu.
- The commands are config values, so they may use `${/...}` references and `${NAME}` environment variables.

RULE: use commands that keep running (servers, log tails, shells) or that the developer wants to watch. A
menu entry is typed into a fresh shell in the stack's root directory, so it must not depend on the state of
another pane.

## How it works, and what to keep when changing it

`tmux.jaz` calls `python3 tmux_menu.py open`, which creates the session, and starts
`tmux_menu.py pick` (the menu loop) in the `Menu` window. The script reads the menu with
`from jazzoo import get_config`, and runs tmux with `from jazzoo import run`.

RULE: the `tmux` target is `[interactive]`, so that `jaz` does not capture the output of `open`: tmux attaches
to the terminal, and its messages (and any errors of the script) appear when they happen.

RULE: the menu loop runs as a stand-alone script in the `Menu` pane, which `open` starts there with
`tmux send-keys`. It reads the config through `JAZZOO_CONFIG_FILES`, not through `jaz`.

RULE: `open` copies `JAZZOO_CONFIG_FILES` into the session with `tmux set-environment`. Panes are started by the
tmux server and do not inherit the environment of `jaz tmux`, so without this the menu cannot read the config.

RULE: target every tmux command explicitly. The new pane is addressed by the id that
`split-window -P -F "#{pane_id}"` prints, and the menu pane by `$TMUX_PANE`. Without a target, tmux picks the
pane in `$TMUX_PANE`, which is the menu itself.

RULE: start `pick` with `sys.executable`, so the menu runs with the same interpreter (and the same `jazzoo`)
as `open`.

## Requirements

- `tmux` is installed.
- `python3` on the `PATH` has `jazzoo` installed, i.e. the venv with `jaz` is active.

## Testing

`examples/blogs/e2e_tests/` has an end-to-end test that runs `jaz tmux` in a pseudo-terminal against an
isolated tmux server (its socket lives in the test's tmp dir), picks commands and checks the panes. Copy it
along with the target, and adapt the expected menu entries. Run it with `just e2e-tests` (a recipe in
`env/local/justfile` that runs `pytest e2e_tests` from the stack's root dir), in the venv that has `jaz`.
Extra arguments go to pytest. The test is skipped when `tmux` or `jaz` is missing.

## Checklist

- [ ] `tmux.jaz` and `tmux_menu.py` copied to `env/local/jaz/tmux/`
- [ ] `env/local/config/base.yaml` defines `/tmux/session` and `/tmux/menu`
- [ ] The root `jazzoo` module loads the config and exports `tmux`
- [ ] `jaz --list` shows `tmux`
- [ ] `jaz tmux` opens the session with the menu in window 1, and a picked command runs in a new pane
- [ ] The e2e test is copied to `e2e_tests/`, adapted to the menu, and `just e2e-tests` passes
