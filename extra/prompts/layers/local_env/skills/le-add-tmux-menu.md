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
`from jazzoo import get_config`.

RULE: the menu loop must run as a stand-alone script in a tmux pane, never inside a Jazzoo block. Jazzoo
captures the stdout of a block and prints it only when the block ends, so a menu inside a block would show
nothing. (`tmux attach-session` does work inside a block, because tmux draws on the terminal it gets through
stdin.)

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

## Checklist

- [ ] `tmux.jaz` and `tmux_menu.py` copied to `env/local/jaz/tmux/`
- [ ] `env/local/config/base.yaml` defines `/tmux/session` and `/tmux/menu`
- [ ] The root `jazzoo` module loads the config and exports `tmux`
- [ ] `jaz --list` shows `tmux`
- [ ] `jaz tmux` opens the session with the menu in window 1, and a picked command runs in a new pane
