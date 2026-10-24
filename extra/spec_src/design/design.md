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
5. The developer checks that the new target appears in the output of `mn-prompts list`
