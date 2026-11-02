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
  `django_app`. Its `index.md` lists the skills of the layer, and its `index-snippet.md` is the part of the
  project's index that tells the agent when to consult the layer. A layer may require other layers (e.g.
  `django_app` requires `python_lib`), which are then installed with it.
- A **target** (`targets/<target_name>.yaml`) is a named set of layers for one type of application.
- The **examples** dir holds the reference apps that the skills refer to.

The available targets (run `mn-prompts list` to see their layers) are:

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

An editable install is required because your projects link to the layers in your clone, which a wheel cannot
provide. Use a plain clone rather than `pip install -e git+<url>`: the latter puts the clone inside
your Python environment, where it's deleted when that environment is recreated.

## Usage

```bash
mn-prompts list                                          # list the available targets and layers
mn-prompts install --target=python_lib                   # install the layers of a target
mn-prompts install --target=python_lib --layer=react_app # ... plus extra layers
mn-prompts install --layer=app --layer=react_app         # install only these layers
mn-prompts install --target=python_lib --agents-md       # write AGENTS.md instead of CLAUDE.md
mn-prompts install                                       # re-install the current selection
```

### Installing the instructions in a project

Run `mn-prompts install` with a `--target`, any number of `--layer`s, or both, in the root dir of your project.
The layers that the selected layers require are added automatically. This:

1. creates an `instructions` dir with:
   - a symlink to each selected layer in your clone of mn-prompts (`<layer_name>_layer`), and to the examples;
   - an `index.md` that is generated from the index-snippets of the selected layers;
   - a `mn-prompts.yaml` file that records the target and layers that you asked for, and the agents file;
2. creates a `CLAUDE.md` file (or an `AGENTS.md` file, with `--agents-md`) that tells the agent to read
   `./instructions/index.md` before writing code, and to follow the spec-driven development process that is
   described there.

If the agents file already exists, then it's left unchanged, and mn-prompts prints the path of the file whose
contents you should add to it. When you run `mn-prompts install` without a target or layers, it uses the agents file
of the earlier install.

### Working with the agent

Ask the agent to build a feature as you normally would. Because of `CLAUDE.md` (or `AGENTS.md`), it starts by reading
`./instructions/index.md`, picks the skills that apply to the code it needs to write, and follows them.

### Project-specific instructions

`index.md` is regenerated on every install, so don't edit it. Put the instructions that are specific to your project
(e.g. which layers apply to which part of a monorepo) in `instructions/project.md`: the index tells the agent to
read it first, and mn-prompts never changes it.

### Changing the selection, and repairing the instructions

Run `mn-prompts install` with another target or other layers to replace the selection: the symlinks of the layers
that are no longer selected are removed. Run `mn-prompts install` without arguments to re-install the current
selection, e.g. to repair the symlinks after moving your clone of mn-prompts. Files of your own in the
`instructions` dir are left alone.

Any other existing `instructions` file, dir or symlink (e.g. one without `mn-prompts.yaml`) is left alone, and
mn-prompts reports an error instead.

### Committing the instructions

Whether you commit the instructions is up to you. Note that the symlinks point into your clone, so they only work on
your machine. A team can commit `mn-prompts.yaml` and `project.md` only: after cloning the project, a team member
runs `mn-prompts install` to re-create the instructions dir.

### Updating the instructions

Your projects link to the layers in your clone, but `index.md` is generated from copies of the index-snippets. After
updating your clone, run `mn-prompts install` in each project to pick up changes to the snippets and the targets:

```bash
git -C ~/mn-prompts pull
mn-prompts install
```

## Extending mn-prompts

You can add your own layers and targets to your clone of mn-prompts:

- **Add a layer:** create `layers/<layer_name>` in the prompts-dir, write one markdown file per skill in its
  `skills` dir (prefixed with an abbreviation of the layer, e.g. `py-write-settings.md`), write an `index.md`
  that lists the skills, and write an `index-snippet.md` (see below). See [s10_a_developer_adds_a_new_layer](doc/spec/scenarios/s10_a_developer_adds_a_new_layer.md).
- **Add a target:** create `targets/<target_name>.yaml` with a `description` and the list of `layers` that it
  uses. Then check that `mn-prompts list` shows the new target. See
  [s20_a_developer_adds_a_new_target](doc/spec/scenarios/s20_a_developer_adds_a_new_target.md).

An index-snippet says when the agent should consult the layer, and names its reference app. It's inserted in the
generated `index.md` of the project, under a `## The layers` heading of `index_template.md`, so:

- it uses no `#` or `##` headings, and is kept short (the details are in the layer's `index.md`);
- its links are relative to the project's `instructions` dir (e.g. `./python_lib_layer/index.md`,
  `./examples/bookie/`), not to the snippet file;
- it reads correctly with any combination of other layers;
- it declares the layers that it requires in its frontmatter:

```markdown
---
requires: [app, python_lib]
---
Consult [django_app_layer/index.md](./django_app_layer/index.md) for ...
```

In the skill files, refer to a skill of another layer by its name (e.g. "the `py-write-settings` skill of the
python_lib layer"), and to an example by a path relative to the `instructions` dir (e.g. `examples/blogs/...`).
