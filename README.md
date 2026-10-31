# mn-prompts

mn-prompts installs a curated set of code generation instructions in your project, so that a coding agent (such
as Claude Code or Codex) builds your code in a consistent, spec-driven way.

## Why use mn-prompts

A coding agent that starts from a blank prompt makes its own choices about how to structure the code, and these
choices differ from one session (and one project) to the next. mn-prompts gives the agent a fixed set of
instructions to follow instead:

- **A spec-driven workflow.** The agent writes specifications first (design, test plan, tests, code, scenarios),
  and then maps them to the implementation, rather than jumping straight into code.
- **Concrete skills.** Each technology comes with skills that describe how to implement a particular pattern, e.g.
  how to write an action, a rule or a model in a Python library, or a serializer in a Django app.
- **Reference apps.** The skills point to complete example apps, so that the agent can copy proven patterns
  instead of inventing new ones.
- **One source for all your projects.** The instructions live in your clone of mn-prompts, and each project links
  to them. When you improve a skill (or pull in an update), every project that uses it picks up the change.

## Concepts

The instructions live in the prompts-dir (`extra/prompts`) of the mn-prompts repository:

- A **layer** (`layers/<layer_name>`) holds the instructions for one technology, e.g. `python_lib` or
  `django_app`. Its `index.md` lists the skills of the layer.
- A **target** (`targets/<target_name>`) holds the instructions for one type of application. It combines the
  layers of the technologies that this application uses (through symlinks), and its `index.md` tells the agent
  which layers to consult, and for what purpose.
- The **examples** dir holds the reference apps that the skills refer to.

The available targets are:

| Target       | Use it for                                                       |
| ------------ | ---------------------------------------------------------------- |
| `python_lib` | A Python library or command line tool                            |
| `django_app` | A Django backend                                                 |
| `react_app`  | A React frontend                                                 |
| `stack`      | A local development stack (Docker Compose) of multiple services  |

## Installation

mn-prompts only supports editable installs from a git clone:

```bash
git clone <repo-url> ~/mn-prompts
pip install -e ~/mn-prompts
```

An editable install is required because the prompts-dir contains symlinks (e.g. from targets to layers), which a
wheel cannot contain. Use a plain clone rather than `pip install -e git+<url>`: the latter puts the clone inside
your Python environment, where it's deleted when that environment is recreated.

## Usage

```bash
mn-prompts list                   # list the available targets
mn-prompts install <target_name>  # e.g. mn-prompts install python_lib
```

### Installing the instructions in a project

Run `mn-prompts install <target_name>` in the root dir of your project. This:

1. creates an `instructions` symlink to the target dir in your clone of mn-prompts;
2. creates an `AGENTS.md` file that tells the agent to read `./instructions/index.md` before writing code, and to
   follow the spec-driven development process that is described there.

If `AGENTS.md` already exists, then it's left unchanged, and mn-prompts prints the path of the file whose contents
you should add to it. If your agent reads another file than `AGENTS.md` (e.g. Claude Code reads `CLAUDE.md`), then
copy the contents of `AGENTS.md` to that file, or refer to `AGENTS.md` from it.

### Working with the agent

Ask the agent to build a feature as you normally would. Because of `AGENTS.md`, it starts by reading
`./instructions/index.md`, picks the skills that apply to the code it needs to write, and follows them.

### Switching targets and repairing the symlink

Run `mn-prompts install <other_target_name>` to switch your project to another target, or run
`mn-prompts install <target_name>` again to repair a broken `instructions` symlink (e.g. after moving your clone of
mn-prompts). An existing `instructions` symlink into the prompts-dir is replaced; any other existing
`instructions` file or dir is left alone, and mn-prompts reports an error instead.

### Updating the instructions

Since your project links to your clone, you update the instructions of all your projects at once with:

```bash
git -C ~/mn-prompts pull
```

## Extending mn-prompts

You can add your own layers and targets to your clone of mn-prompts:

- **Add a layer:** create `layers/<layer_name>` in the prompts-dir, write one markdown file per skill in its
  `skills` dir (prefixed with an abbreviation of the layer, e.g. `py-write-settings.md`), and write an `index.md`
  that lists the skills. See [s10_a_developer_adds_a_new_layer](doc/spec/scenarios/s10_a_developer_adds_a_new_layer.md).
- **Add a target:** create `targets/<target_name>`, add a `<layer_name>_layer` symlink to `../../layers/<layer_name>`
  for each layer that it uses, add an `examples` symlink to `../../examples`, and write an `index.md` that explains
  which layers to consult. Then check that `mn-prompts list` shows the new target. See
  [s20_a_developer_adds_a_new_target](doc/spec/scenarios/s20_a_developer_adds_a_new_target.md).
