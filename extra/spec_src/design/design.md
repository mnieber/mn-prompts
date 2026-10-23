# Glossary

agents file: the `AGENTS.md` file that explains to the agent how the instructions should be used
cwd: current working directory
entrypoint: the `mn-prompts` entrypoint
prompts-dir: the `extra/prompts` directory in the mn-prompts repository that stores the prompts

# Rationale

## The prompts/targets directory

In the targets directory you will find the instructions for generating the code for different types of applications, such as a django app or a react app. Each target refers to a combination of layers that explains how to generate the code for a particular technology (e.g. python_lib) that is used in the target.

Each target has an index.md file that is the starting point for understanding how to generate code for that target.

## The prompts/layers directory

In the layers directory you will find the instructions for generating the code for a particular technology (e.g. python_lib).

Each layer has an index.md file that is the starting point for understanding how to generate code for that layer. Moreover, each layer has a skills directory. A skill describes how to implement a particular pattern or solution within the layer. For example, in the python_lib layer we have a skill that explains how to write a settings.py file for our python library.

## The prompts/examples directory

Targets and layers will refer to example code that lives in the examples directory.

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

## The lifetime of the instructions symlink

The `instructions` symlink points into the user's clone of the mn-prompts repository. This means that:

- the symlink dangles when that clone is moved or deleted;
- after a `git pull` in the clone, the symlink points to the updated prompts.

We accept this: the user can recreate the symlink by calling `mn-prompts install <target_name>` again.

# Milestones

## MS-1: A user install the prompts for their project

1. The user clones the mn-prompts repository and pip installs it as an editable install
2. The user calls `mn-prompts install <target_name>`
   1. E.g. target_name could be "python_lib"
   2. If the prompts-dir does not exist (e.g. because mn-prompts was installed with a regular install) then the
      entrypoint prints an error explaining that mn-prompts must be installed as an editable install
   3. If <target_name> is not a sub-dir of the `targets` sub-dir of the prompts-dir then the entrypoint prints an error
      that lists the available targets
3. The entrypoint creates an `instructions` symlink in the cwd that points to the target instructions for <target_name>.
   1. The symlink is named `instructions`.
   2. The different possible target locations are in the `targets` sub-dir of the prompts-dir
   3. If `instructions` already exists in the cwd then the entrypoint prints an error
      1. Exception: if `instructions` is a symlink into a `targets` sub-dir of an mn-prompts prompts-dir (possibly a
         dangling one) then the entrypoint replaces it. This allows the user to repair the symlink (see "The lifetime
         of the instructions symlink").
4. The entrypoint copies the agents file into the cwd
   1. The file is named `AGENTS.md`.
   2. The source comes from `<prompts_dir>/agents_files/default.md`
   3. If `AGENTS.md` already exists in the cwd then the entrypoint prints an instruction for extending it

## MS-2: A user lists the available targets

1. The user calls `mn-prompts list`
   1. If the prompts-dir does not exist then the entrypoint prints the same error as in MS-1
2. The entrypoint prints the names of the sub-dirs of the `targets` sub-dir of the prompts-dir, one per line
