# Design: composable layers

## Summary

Today a target is a hand-written dir (`targets/<target_name>`) with layer symlinks and an `index.md`, and
`mn-prompts install <target_name>` turns the project's `instructions` into a symlink to that dir. A user whose
project doesn't match one of the targets exactly (e.g. a Python library that also has a React frontend) can't get a
suitable set of instructions.

In the new design a target is just a named set of layers. The user picks a target, any number of extra layers, or
both, and mn-prompts builds a real `instructions` dir in the project: one symlink per selected layer, an `examples`
symlink, and a generated `index.md` that is composed from the index-snippets of the selected layers.

## What the user does

```bash
mn-prompts install --target=python_lib                      # the layers of a target
mn-prompts install --target=python_lib --layer=react_app    # a target plus extra layers
mn-prompts install --layer=app --layer=python_lib           # only layers, no target
mn-prompts install --target=python_lib --agents-md         # write AGENTS.md instead of CLAUDE.md
mn-prompts install                                          # re-install the current selection
mn-prompts list                                             # the targets and the layers
```

- `--target` is optional and can be given at most once. `--layer` can be given any number of times.
- The selection is the union of the layers of the target and the `--layer`s, plus the layers that these require
  (see "Layer dependencies").
- `install` without `--target` and `--layer` re-installs the selection that is recorded in the manifest of the
  existing install. This is what the user runs after a `git pull` in the clone, or after moving the clone. Without
  a manifest it's an error that explains the options.
- `install` with a selection replaces the previous selection; it does not add to it (decision D3).
- The agents file is copied to `CLAUDE.md` by default, or to `AGENTS.md` with `--agents-md` (decision D15).

## What should happen

`mn-prompts install --target=django_app` in a project creates:

```
instructions/
  index.md            # generated from the index template and the index-snippets
  mn-prompts.yaml     # the manifest: target and layers that the user asked for
  app_layer        -> <clone>/extra/prompts/layers/app
  django_app_layer -> <clone>/extra/prompts/layers/django_app
  python_lib_layer -> <clone>/extra/prompts/layers/python_lib
  examples         -> <clone>/extra/prompts/examples
```

and copies the agents file to `CLAUDE.md` (or to `AGENTS.md`, with `--agents-md`). The agents file still points to
`./instructions/index.md`, so it doesn't change. An existing `CLAUDE.md` (or `AGENTS.md`) is left unchanged, and
mn-prompts prints how to extend it, as before.

The symlinks are absolute, as today. The manifest records what the user asked for (not the resolved set), so that a
re-install picks up changes to the target and to the layer dependencies, and the name of the agents file:

```yaml
target: django_app
layers: []
agents_file: CLAUDE.md
```

### Re-installing over an existing install

- An `instructions` dir that contains `mn-prompts.yaml` is ours. mn-prompts rewrites `index.md` and the manifest,
  removes the `*_layer` symlinks into the prompts-dir that are no longer selected, and creates the missing ones.
  Other files in the dir are left alone.
- Any other `instructions` file, dir or symlink is left alone, and mn-prompts raises `InstructionsExistError`. This
  includes the `instructions` symlink of the old version of mn-prompts: there is no migration, the user removes it
  and installs again.
- All errors (unknown target, unknown layer, missing snippet, dependency cycle) are detected before any file is
  changed.

## Changes in the prompts-dir

```
extra/prompts/
  index_template.md            # the frame of the generated index.md
  targets/
    python_lib.yaml
    django_app.yaml
    react_app.yaml
    stack.yaml
  layers/
    python_lib/
      index.md                 # unchanged: lists the skills of the layer
      index-snippet.md         # new: the part of the generated index.md for this layer
      skills/...
  examples/
  agents_files/default.md
```

A target file:

```yaml
description: A Python library or command line tool
layers: [app, python_lib, local_env]
```

An index-snippet (frontmatter is optional):

```markdown
---
requires: [app, python_lib]
---
Consult [django_app_layer/index.md](./django_app_layer/index.md) for:

- Django-specific spec sections declared implicitly in scenarios: Django models, ApiViews, DomainEvents
- the django_app skills, such as dj-write-api-view

Reference app: [examples/blogs/src/services/blogs_be/](./examples/blogs/src/services/blogs_be/)
```

The index template contains the text that every install shares (what the dir is, how paths work, see
"Complications" C5) and one placeholder, `{{layers}}`, where the snippets go. The template is not part of a layer,
because a selection without the `app` layer (e.g. the `stack` target) still needs a frame.

`mn-prompts list` prints the targets (with their description and layers) and then the layers:

```
Targets:
  django_app   A Django backend                (app, django_app, python_lib)
  python_lib   A Python library or command...  (app, local_env, python_lib)
  ...
Layers:
  app
  django_app
  ...
```

## Decisions

These are proposals; each lists the alternatives that were not picked.

- **D1. A target is a yaml file with a list of layer names.** Alternatives: keep target dirs with symlinks (then the
  symlinks duplicate the list, and nothing reads the target's `index.md` anymore); a single `targets.yaml` with all
  targets (fewer files, but `list` and adding a target would edit a shared file).
- **D2. The instructions dir is a real dir with one absolute symlink per layer, plus `examples`.** This is what the
  user asked for. `examples` is always linked: it's shared by all layers, and snippets and skills refer to it.
- **D3. `install` replaces the selection; it doesn't add to it.** The command is then declarative: the same command
  line always gives the same result, and removing a layer needs no extra command. Alternative: add to the existing
  selection, plus a `remove` command (shorter command lines for incremental changes, but the result depends on
  history).
- **D4. A manifest (`instructions/mn-prompts.yaml`) records the requested target and layers.** It marks the dir as
  ours, and lets `mn-prompts install` (no args) regenerate the install. Alternative: derive the selection from the
  `*_layer` symlinks (no extra file, but the target is lost, and a dir with only an `index.md` can't be recognised
  as ours).
- **D5. Layers declare their dependencies (`requires`) in the frontmatter of their index-snippet, and these are
  installed automatically.** See C3. Alternatives: a separate `layer.yaml` (cleaner separation of data and text, one
  more file per layer); no dependencies, where the user (or the target) is responsible (then `--layer=django_app`
  silently gives broken instructions).
- **D6. Snippets are ordered by dependency, then by name.** See C1. Alternative: an explicit `order` number per
  layer.
- **D7. The generated `index.md` is fully owned by mn-prompts** and starts with a "generated, do not edit" comment.
  Project-specific text goes into an optional `instructions/project.md`, which the template refers to if it exists.
  See C6. Alternative: preserve user text outside `<!-- mn-prompts:begin/end -->` markers in `index.md`.
- **D8. A layer without an index-snippet is an error** (`MissingIndexSnippetError`), reported before any change.
  Alternative: fall back to a generic "Consult ./x_layer/index.md" line (friendlier, but hides a missing snippet).

- **D9. mn-prompts leaves version control to the user**, and writes no `.gitignore`: a team may not commit the
  instructions at all. A team that does can commit `mn-prompts.yaml` and `project.md`, and run `mn-prompts install`
  (no args) after cloning: an instructions dir that only contains these files is recognised as ours (it has a
  manifest).
- **D10. In an instructions dir of mn-prompts, every `*_layer` symlink belongs to mn-prompts.** A re-install
  replaces the symlinks of the selected layers and removes all other `*_layer` symlinks, also when they point into
  another (moved) clone. A `*_layer` entry that is not a symlink, or an `examples` entry that is not a symlink,
  raises `InstructionsExistError`. Alternative: only touch symlinks into the current prompts-dir (then a moved
  clone leaves stale symlinks behind).
- **D11. The generated `index.md` starts with the line
  `[comment]: <> (This file is generated by mn-prompts. Do not edit directly.)`**, followed by a blank line and the
  rendered template. Snippets are stripped of their frontmatter and surrounding whitespace, and joined with a blank
  line.
- **D12. mn-prompts depends on PyYAML** to read the target files, the frontmatter of the snippets and the manifest.
- **D13. Code units.** `PromptsDirNotFoundError` moves to the `get_prompts_dir` rule, which now checks that the dir
  exists. `UnknownTargetError` is raised by the `get_target` rule, `UnknownLayerError` and
  `MissingIndexSnippetError` by the `get_layer` rule, and `LayerDependencyCycleError` by the `get_selected_layers`
  rule. The `install_instructions` action (which replaces `install_target`) raises `InstructionsExistError` and
  `MissingSelectionError` (no selection and no manifest). `copy_agents_file` moves to the `instructions` package.
- **D14. `list` prints the layers of a target as they are written in the target file** (not resolved with their
  dependencies), and pads the names and descriptions into columns. Without targets or layers it prints only the
  `Targets:` and `Layers:` headers.
- **D15. The agents file is `CLAUDE.md` by default, and `AGENTS.md` with `--agents-md`.** The choice is recorded in
  the manifest (`agents_file`). A re-install without a target and layers uses the agents file of the manifest,
  unless `--agents-md` is given (which then is recorded). A re-install with a selection is declarative (D3): without
  `--agents-md` it uses `CLAUDE.md`. Switching from one to the other doesn't remove the old file. Alternatives: a
  `--agents-file=<name>` option for any file name; keep using the manifest's agents file for every re-install.

## Complications of index-snippets

### C1. Ordering

The generated index reads top to bottom, and the agent gives weight to what comes first. The `app` layer describes
the workflow that all the other layers plug into, so it must come first; layers that build on other layers (e.g.
`django_app` on `python_lib`) read best after them. A topological sort on `requires`, with ties broken by name, gives
this order without extra metadata: `app`, `python_lib`, `django_app`, `local_env`, `react_app`. A cycle in `requires`
is an error.

### C2. Text that depends on the combination of layers

The current target indexes contain text that only makes sense for a particular combination, which a snippet can't
know about:

- The Overview of the `django_app` target says "read django_app/index.md **and** python_lib/index.md".
- The `stack` target has its own Overview (initial setup, add services, configure) instead of the five development
  phases, because it has no `app` layer.
- The "Key Principles" mix principles of several layers (e.g. "Forms co-location" is python_lib, "One file per
  component" is react_app), and some are repeated in every target.
- The "Examples" sections list exactly the example apps that are relevant for the combination.

Proposal: no conditionals or templating inside snippets. Instead:

- the Overview becomes generic text in the index template ("read the index of each layer below to identify the
  skills that apply");
- the development-phases pointer moves into the `app` snippet; the stack-setup phases of the `stack` target are
  dropped, because the `local_env` index already lists the order in which to apply its skills;
- each layer's Key Principles move into that layer's own `index.md` (the `app` layer already has them), so they are
  read when the layer is consulted, and never duplicated;
- each snippet names its own reference app. The same example may be named by two snippets (e.g. `bookie` by
  `python_lib` and `django_app`); that duplication is harmless.

A snippet must therefore be written so that it reads correctly with any set of other layers. This is a rule for
the s10 scenario ("A developer adds a new layer").

### C3. Layers depend on other layers

Today the targets hide this, but the layers already refer to each other:

- hard dependencies: `django_app` builds on `python_lib` (`dj-write-tests` follows `py-write-workflow-tests`,
  `dj-write-settings` overrides `py-write-settings`), and every development layer builds on the `app` workflow;
- soft references: `app-apply-development-phases` names both `py-write-workflow-tests` and
  `fe-write-workflow-tests`; `fe-write-workflow-tests` calls itself the counterpart of `py-write-workflow-tests`;
  `local_env` links to the `django_app`, `react_app` and `python_lib` layers, and `py-publish-to-pypi` to
  `le-use-compose-ops`.

Note that the `react_app` target already doesn't include `python_lib`, so the soft references dangle today. With
free composition this becomes common, so:

- hard dependencies are declared with `requires` (D5);
- soft references stay, and the index template tells the agent that a skill may name a skill of a layer that is
  not installed, which it should then ignore. Alternatively, `requires` could get an `optional:` sibling that is
  only used for documentation (not proposed).

### C4. Snippet paths are relative to the install, not to the snippet file

A snippet is stored in `layers/<layer>/index-snippet.md`, but it ends up in `instructions/index.md`. Its links must
therefore be written as `./<layer>_layer/...` and `./examples/...`, i.e. relative to the instructions dir. This
only works because the symlink names are fixed (`<layer_name>_layer`), so that naming becomes part of the contract.
Previewing a snippet in a markdown viewer shows broken links; that is acceptable. Alternative (not proposed): a
`{{layer_dir}}` placeholder that mn-prompts fills in.

### C5. Paths inside skills (existing problem, made more visible)

Skill files are read through the layer symlinks, and the OS resolves `..` physically: `a_layer/skills/../..` is the
`layers` dir of the clone, not the instructions dir (verified with a small experiment). The layers currently use
three conventions:

1. links to other layers relative to the real file location (`../../django_app/index.md`): these work physically,
   but they lead the agent into the clone, also into layers that are not installed;
2. "Primary reference" paths relative to the logical layer dir (`../examples/blogs/...` in `local_env`): these only
   work if the agent normalises the path textually, and fail when it lets the OS resolve them;
3. bare paths (`examples/blogs/env/local/jaz/...`): these work if the agent reads them relative to the instructions
   dir.

The hand-written `instructions/index.md` of this repo contains a "Paths between layers" note for this. Proposal:
make convention 3 the only one. Skills refer to other layers by skill name (`the py-write-settings skill (python_lib
layer)`) and to examples by a path relative to the instructions dir (`examples/blogs/...`), and the index template
says so once. This is a clean-up of the layers that can be done before or after this feature, but the template text
depends on it.

### C6. User edits and project-specific content

The generated `index.md` is rewritten on every install. Some projects need their own text in it; e.g. this repo's
own `instructions/index.md` has a "parts of this repository" table that maps sub-dirs to layers, which no snippet
can produce. With D7 this text goes into `instructions/project.md`, which mn-prompts never touches, and to which
the template refers ("If ./project.md exists, read it first: it says which layers apply to which part of the
project"). The mn-prompts repo can then use its own installer for its `instructions` dir.

### C7. Snippets are copied, so `git pull` no longer updates the index

Today the project's `instructions` symlink points into the clone, so a `git pull` updates everything. The layer
symlinks keep that property for the layers, but the snippets and the template are copied into `index.md`, and a
changed snippet (or a target that gains a layer) only reaches the project after a re-install. Mitigations:

- `mn-prompts install` without arguments re-installs from the manifest (D4), and the README's "Updating the
  instructions" section says to run it after a pull;
- optional (not proposed now): the generated `index.md` records a hash of its inputs, and `mn-prompts list` or a
  `status` command warns when the install is stale.

Alternative that avoids the copy: `index.md` only lists links to the snippet files (`./django_app_layer/index-
snippet.md`) instead of including their text. This costs the agent one extra read per layer, and the snippet then
duplicates the purpose of the layer's own `index.md`, so it's not proposed.

### C8. Snippet format

Snippets are inserted under a `## The layers` heading of the template, so they must not contain `#` or `##`
headings, and they should be short (a few bullets and a reference app): the layer's `index.md` holds the detail.
mn-prompts strips the frontmatter and joins the snippets with a blank line, without further processing.

### C9. Things that no longer exist

- The target dirs, their symlinks and their `index.md`s are removed. The untracked `.claude/settings.local.json`
  files in `targets/django_app` and `targets/python_lib` are deleted with them.
- `UnknownTargetError` stays; `UnknownLayerError` and `MissingIndexSnippetError` are new.
- The positional `target_name` argument of `install` becomes `--target`. Keeping the positional form as an alias is
  not proposed: the tool is young, and two forms complicate the README.

## Changes to the scenarios

- s10 (adds a new layer): a step to write `index-snippet.md`, with `requires`, and the rules of C2, C4 and C8.
- s20 (adds a new target): the target becomes a yaml file; no symlinks and no `index.md`.
- s30 (installs the prompts): `--target`/`--layer`, the instructions dir, the generated index, the manifest, and
  re-installing.
- s40 (lists the targets): also lists the layers, and the description and layers of each target.

## Settled questions

- A layer does not contribute to the template outside its snippet.
- mn-prompts leaves version control to the user (D9).
