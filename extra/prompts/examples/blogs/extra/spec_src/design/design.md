# Design: a `tmux` target for the blogs project

## Goal

`jaz tmux` opens a tmux session for the blogs project with an interactive menu of
commands. Picking one or more commands runs each of them in a new pane next to the
menu. Running `jaz tmux` again while the session exists only re-attaches to it.

This replaces `dodo root.menu --tmux` (the `~mt` command in `src/.dodo/stack.root.yaml`),
which reads its menu from the `/MENU` key of the dodo config. Here the menu comes from
a YAML config file that the Jazzoo file loads with `⚙️.load_config`, and the script
reads it with `get_config`.

```
$ jaz tmux                  # create the session (if needed) and attach to it
$ jaz tmux examples         # same, but the menu only shows the "examples" category
$ jaz tmux session=blogs-2  # use a different session name
```

## Is the config feature enough?

Yes. Jazzoo itself never reads the config, but it does not need to: the Jazzoo file
only names the config file, and the Python script that does the work reads the menu
with `get_config`. The script also passes `JAZZOO_CONFIG_FILES` on to the tmux session
(see "The environment of the panes"), so that the menu, which runs inside tmux, sees
the same config.

## Files

```
examples/blogs/
    jazzoo                          # root module (new)
    env/local/config/base.yaml      # config (new)
    env/local/jaz/tmux/tmux.jaz     # the tmux target
    env/local/jaz/tmux/tmux_menu.py # the script that does the work
```

There is no Jazzoo setup in `examples/blogs` yet (it uses `just` and dodo), so the root
module is created as part of this work. For now it only loads the config and exports
the `tmux` target:

```
# jazzoo
⚙️.load_config(path=⚙️.module.dirname / "env/local/config/base.yaml")

from ./env/local/jaz/tmux/tmux.jaz export tmux
```

## The config

```yaml
# env/local/config/base.yaml
tmux:
  session: blogs
  menu:
    examples:
      - whoami
      - date
      - uptime
```

- `/tmux/session` is the default name of the tmux session. It is required.
- `/tmux/menu` maps a category to a list of shell commands. The order of the
  categories and commands is the order of the menu.
- The commands are plain shell lines. Because they are config values, they can use
  `${/...}` references and `${NAME}` environment variables.
- The keys are lower case (`tmux`, `menu`) rather than dodo's upper case (`MENU`): in
  Jazzoo the config is not shared with dodo's magic keys, so there is nothing to
  distinguish from.

## `tmux.jaz`

`tmux.jaz` is a thin wrapper that delegates to `tmux_menu.py`:

```
# env/local/jaz/tmux/tmux.jaz
🐭.script = ⚙️.module.dirname / "tmux_menu.py"

tmux(category="all", session=""):
    @python3 🐭.script open --category=🐆.category --session=🐆.session
```

- An empty `session` means: use `/tmux/session` from the config.
- `python3` must be an interpreter in which `jazzoo` is installed, since the script
  imports `get_config` from it.

### Why a Python script, and not a pure Jazzoo target

The menu loop cannot run inside a Jazzoo block. Jazzoo captures the stdout of every
block (for `⚙️.stdout`) and only prints it when the block has finished. A menu that
prints its choices and then waits for input would show nothing. The menu therefore
runs as a stand-alone script in a tmux pane, and since that script is needed anyway,
the session setup lives in it too. This keeps all tmux logic in one file.

The `open` step can run inside a Jazzoo block. `tmux attach-session` draws on the
terminal that it gets through stdin, which Jazzoo leaves connected, so attaching
works even though stdout is captured (verified with tmux 3.2a). Only tmux's
`[detached ...]` message is delayed until the block ends.

## `tmux_menu.py`

The script has two sub-commands: `open` (run by `jaz tmux`) and `pick` (run in the
menu pane).

### `open`

1. Resolve the session name: the `--session` argument, else `/tmux/session`.
2. Check whether the session exists with `tmux has-session -t <session>` (instead of
   parsing `tmux ls`, as dodo does).
3. If it does not exist:
   - `tmux new-session -d -s <session> -c <project dir>`, where the project dir is
     the current working directory. Window 0 is a plain shell.
   - `tmux set-environment -t <session> JAZZOO_CONFIG_FILES <value>`.
   - `tmux new-window -t <session>:1 -n Menu -c <project dir>`.
   - `tmux send-keys -t <session>:1 "<python> <script> pick --category=<category>" C-m`,
     where `<python>` is `sys.executable`, so the menu runs with the same interpreter
     (and the same `jazzoo`) as the `open` step.
4. Attach: `tmux attach-session -t <session>`. When the script already runs inside
   tmux (`$TMUX` is set), it uses `tmux switch-client -t <session>` instead, because
   tmux refuses to nest sessions. Dodo does not handle this case.

The `--category` argument only affects a newly created session. When the session
already exists, `open` only attaches, and the menu keeps the category it was started
with.

### `pick`

The menu loop runs forever in the `Menu` window:

1. Clear the pane (`tmux send-keys -R ""`, as dodo does) and print the menu:

   ```
    1 [examples] - whoami
    2 [examples] - date
   ```

   With `--category=<name>`, only that category is listed. The category names in
   the labels are padded to the same width. A category name with spaces is matched
   with dashes on the command line (`build tools` → `build-tools`), as in dodo.

2. Ask: `Select one or more commands (e.g. 1,3-4), or type a command, or type 0 to exit: `.
   - A selection is a comma-separated list of numbers and ranges (`1,3-4`). Spaces are
     ignored.
   - An input that is not a valid selection is used as a free-text command.
   - `0` ends the loop; the pane then returns to its shell.
   - An index that is out of range prints an error and asks again.
3. For each selected command: split the menu window (`tmux split-window -v`), wait
   briefly so that the shell in the new pane is ready, send the command with
   `tmux send-keys -t <new pane> <command> C-m`, and re-tile with
   `tmux select-layout tiled`. The new pane is targeted by the id that
   `split-window -P -F "#{pane_id}"` prints: without a target, tmux would pick the
   pane in `$TMUX_PANE`, which is the menu itself.
4. Select the menu pane again, using `$TMUX_PANE` (dodo uses pane 0, which is wrong
   when the menu is not the first pane).

The commands are typed into a shell in the new pane, not run by the script. So a
command keeps running after it is started, the user can stop it with ctrl-c and
re-run it with the arrow keys, and the menu is free for the next pick.

### The environment of the panes

Panes are shells that the tmux _server_ starts. They do not inherit the environment
of `jaz tmux`; if a tmux server was already running (for another session), they get
the environment of whoever started that server. `open` therefore copies
`JAZZOO_CONFIG_FILES` into the session environment with `tmux set-environment`, so
that it reaches the menu window and every pane that is split from it. This makes
`get_config` work in the menu, and a `jaz ...` command in a pane starts with the
config of the session, because an inherited `JAZZOO_CONFIG_FILES` forms the start of
its config list.

Other variables (e.g. those loaded with `⚙️.load_env`) are not copied. The commands in
the menu are expected to load what they need themselves, as `jaz` targets do.

### The ad-hoc `run` function

Until Jazzoo has its own `run` function, the script defines a small helper:

```python
def run(args, capture=False):
    """Run a command; raise on a non-zero exit code. Return stdout if capture is set."""
```

- `args` is a list, so no shell quoting is needed (the command that is sent with
  `send-keys` is one argument).
- `tmux has-session` is the only call whose non-zero exit is expected; it uses
  `subprocess.run` directly and checks the return code.
- The helper is the only place that calls `subprocess`, so it can be swapped for
  Jazzoo's `run` later without touching the rest of the script.

### Errors

- `tmux` not installed: the script exits with `tmux is not installed`.
- No commands in the (filtered) menu: the script exits with
  `No commands found in /tmux/menu` before it creates a session.
- An unknown category: the script exits with the list of known categories.
- Config errors (`ConfigError`) are not caught; their message names the file and
  path.

## What we take from `dodo menu`, and what we leave out

Taken:

- The menu with categories, numbered commands and the `1,3-4` selection syntax.
- Free-text commands.
- Running each picked command in a new pane and re-tiling.
- Re-attaching instead of re-creating an existing session.

Changed:

- The menu runs as a separate `pick` sub-command instead of re-running itself with a
  hidden `--continue` flag through `send-keys " ".join(sys.argv)`. That trick depends
  on the shell in the pane resolving `sys.argv[0]` the same way, and would re-run
  `jaz` (with its captured stdout) instead of the script.
- `tmux has-session` instead of parsing `tmux ls`.
- `switch-client` when already inside tmux.
- The menu pane is found with `$TMUX_PANE` instead of assuming pane 0.

Left out:

- **`--list`** (print the menu and exit) and **non-tmux mode** (pick commands and run
  them one after the other in the current terminal). They are easy to add as extra
  sub-commands, but are not needed for the tmux workflow.
- **`--run N`** (run command N without asking).

## Decisions

- **The interpreter.** `tmux.jaz` calls `python3` from the `PATH`, so the venv in which
  `jazzoo` is installed must be active.
- **The session name.** There is no `$USER` fallback: the name comes from the `session`
  argument, else from `/tmux/session`, which the config must define. Every project sets
  its own name anyway, and a missing key gives a clear `ConfigKeyError`.
- **The menu commands.** For now the menu holds simple example commands (e.g.
  `whoami`). The real commands are added later. The dodo menu setup stays as it is.

## Notes for Jazzoo's future `run` function

This target shows two requirements for the planned `run` function (and for Jazzoo's
blocks in general):

- **Interactive commands.** Because every block's stdout is captured, a block that
  prompts the user (a menu, `read`, `docker exec -it ... fish`) shows its output only
  when it ends. `run` (or a block attribute) needs a mode in which stdout goes
  straight to the terminal and is not captured.
- **Expected failures.** `tmux has-session` signals "no" with a non-zero exit code.
  `run` needs a way to return the exit code instead of raising an `ExecutionError`.
