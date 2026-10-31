# Skill: le-add-dial

Applies when adding the `zoo dial.*` targets to a stack: they give the function keys of the developer's fish
shell a meaning per stack. F1–F12 insert a command into the command line, and Shift+F1–F12 and Ctrl+F1–F12 `cd`
to a directory of the stack.

The `examples/blogs` stack has a complete setup. Copy its files and adapt the config.

---

## What the developer sees

```
$ zoo dial.install-fish                  # once per machine: install the fish functions and key bindings
<F2>                                     # inserts `zoo be.` into the command line
<Shift+F2>                               # cd to src/services/blogs_be
<Ctrl+F1>                                # cd to env/local
$ zoo dial.get 2 group=shift dir=true    # what the key bindings call: prints the directory
$ zoo config.print /dial                 # show all the keys
```

`zoo --list dial` lists the targets.

The keys work from any directory, also outside the stack: they use the zoo environment that is active in the
shell, and switch along with `zoo env <name>`. A key that is not in the config does nothing.

## Why zoo and not jaz

`jaz` only loads the `jazzoo` file of the current directory, so after the first `cd` into a service the keys
would stop working. `zoo` runs the target in the root directory of the active zoo environment, from any
directory. The target runs its script with `⚙️.python`, the Python that runs `zoo`, so the script can import `jazzoo`,
also in a shell where the developer did not activate a venv by hand.

RULE: the fish functions call `zoo`, never `jaz`.

## Files

```
<stack>/
    jazzoo                                  # the root proxy, see le-use-compose-ops
    env/local/jazzoo                        # loads the config, exports the dial layer
    env/local/config/base.yaml              # the keys
    env/local/jaz/dial/dial.jaz             # the dial.* targets
    env/local/jaz/dial/dial_tools.py        # the script that does the work
    env/local/jaz/dial/fish/dial_insert.fish
    env/local/jaz/dial/fish/dial_cd.fish
```

Copy `env/local/jaz/dial/` from `examples/blogs` unchanged. It contains nothing that is specific to the stack.

## The env module

If the stack has no `env/local/jazzoo` module yet, create it, together with the root proxy (see
[le-use-compose-ops](./le-use-compose-ops.md)). Otherwise add the missing lines to the existing one:

```
⚙️.load_config(path=⚙️.module.dirname / "config/base.yaml")

from ./jaz/dial/dial.jaz export * as dial
```

## The config

```yaml
# env/local/config/base.yaml
dial:
  default:
    1: zoo docker.exec be
    2: "zoo be."
    3: "zoo fe."
  shift:
    1: .
    2: src/services/blogs_be
    3: src/services/blogs_fe
  ctrl:
    1: env/local
    2: env/local/config
    3: "~"
```

- `/dial/default/<n>` is the text that F<n> inserts. It is not run: the developer completes or runs it.
- `/dial/shift/<n>` and `/dial/ctrl/<n>` are the directories that Shift+F<n> and Ctrl+F<n> `cd` to. A relative
  directory is resolved against the root directory of the stack.
- Values may use `${/...}` references, `${NAME}` environment variables and a leading `~`.

RULE: quote a value that is only `~`. A bare `~` is `null` in YAML.

RULE: use the directories and commands that the developer needs most often: the root directory of the stack,
the services, and the config directory are good candidates. Ask the developer when in doubt.

## Installing the fish bindings

`zoo dial.install-fish` installs the bindings for the current user, in the fish config directory
(`$XDG_CONFIG_HOME/fish`, or `~/.config/fish`):

- It copies `dial_insert.fish` and `dial_cd.fish` to `functions/`.
- It writes the key bindings to `conf.d/dial_bindings.fish`. For fish 4 it uses key names (`shift-f1`); for
  fish 3 it uses the escape sequences of xterm-like terminals.

The fish files do not depend on the stack, so one installation serves all stacks. Running it again updates the
files.

RULE: the installer only overwrites files that start with `# managed by zoo dial.install-fish`. When such a file
exists without this line, it stops and lists the file, and the developer removes it. It never edits
`fish_user_key_bindings.fish`, which holds the developer's own bindings. When that file, or a file in
`conf.d/`, still binds `dial_` functions, it says so, and the developer removes those bindings.

The bindings are made for the default (emacs) key bindings of fish. Vi mode is not supported.

## How it works, and what to keep when changing it

`dial_insert <n>` runs `zoo dial.get <n>`, and inserts the output into the command line. `dial_cd <group> <n>`
runs `zoo dial.get <n> group=<group> dir=true`, and `cd`s to the output. Both do nothing when `zoo` is not on
the `PATH` or the output is empty.

`dial.get` calls `⚙️.python dial_tools.py get`, which reads `/dial/<group>` with `from jazzoo import get_config`,
and prints the value of the key with `~` expanded. With `dir=true` it joins it to the root directory of the
stack. An unknown key prints nothing and exits with 0, so that a key binding can ignore it.

RULE: `dial.get` prints only the value. Anything else that it prints ends up in the command line or the `cd`.

RULE: `dial_cd` checks that the output is not empty before it calls `cd`: a bare `cd` goes to the home
directory.

RULE: the targets are `[interactive]`, so that `jaz` does not capture their output, and they quote their string
arguments with `⚙️.sh-quote`.

## Requirements

- The stack is a zoo environment (`zoo env --init ...` in the root directory), and it is active in the shell.
- fish, in a terminal that sends xterm-like escape sequences for Shift+F<n> and Ctrl+F<n> (fish 3 only).

## Checklist

- [ ] `env/local/jaz/dial/` copied from `examples/blogs`
- [ ] `env/local/config/base.yaml` defines `/dial/default`, `/dial/shift` and `/dial/ctrl`
- [ ] The `env/local/jazzoo` module loads the config and exports the `dial` layer
- [ ] `zoo --list dial` shows `dial.get` and `dial.install-fish`
- [ ] `zoo dial.get 1` prints the value of F1
- [ ] After `zoo dial.install-fish` and in a new fish shell, Shift+F1 changes to the directory of `/dial/shift/1`
