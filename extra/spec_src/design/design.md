# Glossary

agents file: the `AGENTS.md` file that explains to the agent how the instructions should be used
cwd: current working directory
entrypoint: the `mn-prompts` entrypoint
prompts-dir: the `extra/prompts` directory in the mn-prompts repository that stores the prompts
target: a sub-dir of the `targets` sub-dir of the prompts-dir with instructions for generating a type of application
layer: a sub-dir of the `layers` sub-dir of the prompts-dir with instructions for using a particular technology
skill: a markdown file in the `skills` sub-dir of a layer that describes how to implement a particular pattern

# Rationale

## Targets share layers through symlinks

Different targets often use the same technology. For example, both the python_lib and the django_app target use the app layer and the python_lib layer. Instead of duplicating these layers, each target contains symlinks to the layers it uses (see MS-1). The same holds for the example code, which is shared by all targets.

## Only editable installs are supported

The prompts-dir contains symlinks (e.g. from targets to layers). Wheels cannot contain symlinks, so a regular install
would either break these symlinks or duplicate the files they point to. Therefore we only support editable installs
from a git clone of the mn-prompts repository:

```bash
git clone <repo-url> ~/mn-prompts
pip install -e ~/mn-prompts
```

We prefer a plain clone over `pip install -e git+<url>`, because the latter puts the clone inside the Python
environment, where it is deleted when that environment is recreated.

## Locating the prompts-dir

The entrypoint locates the prompts-dir relative to the source code of the `mn_prompts` package, i.e.
`Path(mn_prompts.__file__).parents[2] / "extra" / "prompts"`. This only works for an editable install.

This location is computed by a single rule (`get_prompts_dir()`), which is also used to decide whether an existing
`instructions` symlink belongs to mn-prompts (see MS-2). The tests point `mn_prompts.__file__` into a fake clone
that they create themselves, so that this rule finds the prompts-dir of that clone.

## The lifetime of the instructions symlink

The `instructions` symlink points into the user's clone of the mn-prompts repository. This means that:

- the symlink dangles when that clone is moved or deleted;
- after a `git pull` in the clone, the symlink points to the updated prompts.

We accept this: the user can recreate the symlink by calling `mn-prompts install <target_name>` again. The
entrypoint only replaces a symlink that points into the `targets` sub-dir of its own prompts-dir. When the clone was moved, the old symlink points elsewhere, and the user must remove it before installing again.

# Milestones

## MS-1: A developer adds a new layers

1. The developer creates a directory for each new layer in the `layers` sub-dir of the prompts-dir
   1. A layer contains the instructions for generating the code for a particular technology (e.g. python_lib)
   2. The directory name is the snake_case <layer_name>, e.g. `django_app`
2. The developer writes the skills of each new layer
   1. The skills are stored in the `skills` sub-dir of the layer, one markdown file per skill
   2. A skill describes how to implement a particular pattern or solution within the layer. For example, the
      python_lib layer has a skill that explains how to write a settings.py file for our python library.
   3. The name of a skill file starts with a prefix that identifies the layer, e.g. `py-write-settings.md` or
      `dj-write-api-view.md`
   4. A skill may refer to example code in the `examples` sub-dir of the prompts-dir. If no suitable example exists, the
      developer adds a new example application to that directory.
3. The developer writes the `index.md` file of each new layer
   1. This file is the starting point for understanding how to generate code for that layer
   2. It lists the skills of the layer, each with a short description and a link to the skill file

## MS-2: A developer adds a new target

1. The developer creates a directory for the new target in the `targets` sub-dir of the prompts-dir
   1. A target contains the instructions for generating the code for a type of application, such as a django app or a react app
   2. The directory name is the <target_name> that the user passes to `mn-prompts install`
2. The developer adds a symlink to the target directory for each layer that the target uses
   1. The symlink is named `<layer_name>_layer` and points to `../../layers/<layer_name>`
   2. These can be new layers as well as existing ones (see "Targets share layers through symlinks")
3. The developer adds an `examples` symlink to the target directory that points to `../../examples`
4. The developer writes the `index.md` file of the target
   1. This file is the starting point for understanding how to generate code for that target
   2. It explains which layer `index.md` files the agent should consult, and for what purpose
   3. It refers to the relevant example applications via the `examples` symlink
5. The developer checks that the new target appears in the output of `mn-prompts list` (see MS-3)

## MS-3: A user installs the prompts for their project

1. The user clones the mn-prompts repository and pip installs it as an editable install
2. The user calls `mn-prompts install <target_name>`
   1. E.g. target_name could be "python_lib"
   2. If the prompts-dir does not exist (e.g. because mn-prompts was installed with a regular install) then the
      entrypoint prints an error explaining that mn-prompts must be installed as an editable install
   3. If <target_name> is not a sub-dir of the `targets` sub-dir of the prompts-dir then the entrypoint prints an error
      that lists the available targets
   4. The entrypoint checks for these errors (and the one in 3.3) before it creates or changes any file
3. The entrypoint creates an `instructions` symlink in the cwd that points to the target instructions for <target_name>.
   1. The symlink is named `instructions`.
   2. The symlink is absolute: it points to `<prompts_dir>/targets/<target_name>`
   3. If `instructions` already exists in the cwd then the entrypoint prints an error
      1. Exception: if `instructions` is a symlink into the `targets` sub-dir of the prompts-dir (possibly a dangling
         one) then the entrypoint replaces it. This allows the user to repair the symlink, or to switch to another
         target (see "The lifetime of the instructions symlink").
4. The entrypoint copies the agents file into the cwd
   1. The file is named `AGENTS.md`.
   2. The source comes from `<prompts_dir>/agents_files/default.md`
   3. If `AGENTS.md` already exists in the cwd then the entrypoint leaves it unchanged, and prints an instruction for
      extending it with the contents of the source file. This is not an error: the exit code is 0, and the
      instruction is printed to stderr (like the error messages), so that stdout is kept for the output.

## MS-4: A user lists the available targets

1. The user calls `mn-prompts list`
   1. If the prompts-dir does not exist then the entrypoint prints the same error as in MS-3
2. The entrypoint prints the names of the sub-dirs of the `targets` sub-dir of the prompts-dir, one per line
   1. The names are sorted alphabetically
   2. Hidden sub-dirs (e.g. `.claude`) and files are skipped
   3. The error for an unknown target in MS-3 lists the targets in the same way
