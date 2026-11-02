# Glossary

### Agents file

The file in the project dir that tells the agent to read `instructions/index.md`, and to follow the spec-driven
development process. It is `CLAUDE.md` by default, or `AGENTS.md` with `--agents-md`, and its name is recorded in
the manifest. mn-prompts copies it from `agents_files/default.md` in the prompts-dir, and never replaces an existing
agents file.

### Example

A reference app in `extra/prompts/examples/` (e.g. `bookie`, `blogs`) that shows the patterns of one or more layers.
Skills and index-snippets refer to it with a path that starts with `examples/`, which is linked into every
instructions dir.

### Index template

The file `index_template.md` in the prompts-dir. It holds the text that every generated index shares, and a
`{{layers}}` placeholder where the index-snippets of the selected layers are inserted.

### Index-snippet

The file `index-snippet.md` of a layer: the part of the generated `instructions/index.md` that tells the agent when
to consult the layer. Its optional frontmatter lists the layers that it requires (`requires`). It is written
relative to the instructions dir, and reads correctly with any set of other layers.

### Instructions dir

The `instructions` dir that mn-prompts creates in the project dir. It contains a symlink per selected layer
(`<layer_name>_layer`), an `examples` symlink, the generated `index.md`, and the manifest. It may also hold a
`project.md` with project-specific instructions, which mn-prompts never changes.

### Layer

A dir in `extra/prompts/layers/` with the instructions for one technology (e.g. `app`, `python_lib`, `django_app`).
It has an `index.md` that lists its skills, an index-snippet, and a `skills` dir. A layer may require other layers,
which are then selected with it.

### Manifest

The file `instructions/mn-prompts.yaml`. It records what the user asked for (the target and the layers, not the
resolved selection), and the name of the agents file. It marks the instructions dir as installed by mn-prompts, and
lets `mn-prompts install` without arguments re-install the same selection.

### Project dir

The dir in which the user runs `mn-prompts install` (the cwd). mn-prompts creates the instructions dir and the agents
file in it, and, with `--git-ignore`, updates its `.gitignore`.

### Prompts-dir

The dir `extra/prompts/` in the clone of the mn-prompts repository, which holds the targets, the layers, the
examples, the index template and the agents files. mn-prompts finds it relative to its own source code, so it must
be an editable install of a clone.

### Selection

The layers that are installed: the layers of the target and the `--layer`s that the user asked for, plus the layers
that these require. The selected layers are ordered so that each layer comes after the layers that it requires, with
ties broken by name. An install with a selection replaces the previous selection.

### Skill

A file in the `skills` dir of a layer (e.g. `py-write-action.md`) that explains how to do one task or write one kind
of code unit, with rules (`RULE:`) that the agent follows closely. It is not a skill of the agent's own Skill tool.

### Target

A named set of layers for a kind of project, in `extra/prompts/targets/<target_name>.yaml`, with a description and
a list of layers (e.g. `django_app` is `app`, `django_app` and `python_lib`). The user picks at most one target, and
may add layers to it.
