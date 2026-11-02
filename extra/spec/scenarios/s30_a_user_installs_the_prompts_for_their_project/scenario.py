import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s30_a_user_installs_the_prompts_for_their_project")


def run_scenario():
    r.user = c.External.Actors.User
    r.mn_prompts_entrypoint = c.Runtime.Entrypoints.MnPrompts
    r.install_instructions_action = c.Instructions.Actions.InstallInstructions
    r.copy_agents_file_action = c.Instructions.Actions.CopyAgentsFile
    r.get_prompts_dir_rule = c.Prompts.Rules.GetPromptsDir
    r.get_target_rule = c.Targets.Rules.GetTarget
    r.get_selected_layers_rule = c.Layers.Rules.GetSelectedLayers
    r.get_layer_rule = c.Layers.Rules.GetLayer
    r.get_index_text_rule = c.Instructions.Rules.GetIndexText

    with goal().install_the(r.instructions).of_a(r.selection).in_the(r.project_dir):

        # Install mn-prompts
        the(r.user).clones_the(r.mn_prompts_repo)
        the(r.user).pip_installs_the(r.mn_prompts_repo).as_an_editable_install()

        with the(r.user).calls(r.mn_prompts_entrypoint).with_a(r.target_name).and_the(
            r.layer_names
        ):
            with it().calls(r.install_instructions_action):

                # Select the layers
                with it().calls(r.get_prompts_dir_rule):
                    it().raises(r.prompts_dir_not_found_error).if_it_does_not_exist()
                it().raises(r.instructions_exist_error).if_the(
                    r.instructions_dir
                ).was_not_installed_by_mn_prompts()
                with it().calls(r.get_target_rule).with_the(r.target_name):
                    it().reads_the(r.layer_names).from_the(r.target_file)
                with it().calls(r.get_selected_layers_rule).with_the(r.layer_names):
                    with it().calls(r.get_layer_rule).for_each(r.layer):
                        it().reads_the(r.index_snippet).and_the(r.required_layers)
                    it().adds_the(r.required_layers)
                    it().orders_the(r.selected_layers).by_their_dependencies()

                # Link the layers
                it().creates_the(r.instructions_dir)
                it().creates_a(r.layer_symlink).for_each(r.selected_layer)
                it().removes_the(r.layer_symlinks).of_the_layers_that_are_not_selected()
                it().creates_an(r.examples_symlink)

                # Generate the index
                with it().calls(r.get_index_text_rule).with_the(r.selected_layers):
                    it().inserts_the(r.index_snippets).into_the(r.index_template)
                it().writes_the(r.index_file)
                it().writes_the(r.manifest)

            # Copy the agents file
            with the(r.mn_prompts_entrypoint).calls(r.copy_agents_file_action):
                it().copies_the(r.agents_file).to_the(r.claude_md_file).or_to_the(
                    r.agents_md_file
                )
                it().leaves_the(r.agents_file).unchanged_if_it_exists()
            the(r.mn_prompts_entrypoint).prints_how_to_extend_the(r.agents_file)

        # Add project-specific instructions
        the(r.user).writes_the(r.project_file).in_the(r.instructions_dir)


markdown_node = sunya.add_markdown_node(
    scenario, "A user installs the prompts for their project"
)

markdown_node.markdown = """
A user installs the instructions of a target (e.g. `python_lib`), of a set of layers, or of both, in their project.
The project gets an `instructions` dir with symlinks to the layers in the user's clone of mn-prompts and a generated
`index.md`, and a `CLAUDE.md` (or `AGENTS.md`) file that tells the agent how to use these instructions.

### Steps

#### It installs mn-prompts

The user clones the mn-prompts repository, and pip installs it as an editable install.</br>
Only editable installs are supported: the project links to the layers in the prompts-dir (`extra/prompts`) of the
clone.</br>
The user installs from a plain clone rather than with `pip install -e git+<url>`, because the latter puts the clone
inside the Python environment, where it's deleted when that environment is recreated.</br>

#### It selects the layers

The user calls `mn-prompts install` in the project dir, with an optional `--target` and any number of `--layer`s
(e.g. `mn-prompts install --target=python_lib --layer=react_app`).</br>
The entrypoint calls `install_instructions`, which locates the prompts-dir, and checks that the `instructions` dir
either doesn't exist or was installed by mn-prompts (it contains a manifest).</br>
The selection is the union of the layers of the target (`get_target` reads them from the target file) and the
`--layer`s. `get_selected_layers` adds the layers that these require (`get_layer` reads them from the frontmatter
of the index snippet), and orders the layers so that each layer comes after the layers that it requires.</br>
All errors (e.g. an unknown target or layer) are reported before any file is changed.</br>

#### It links the layers

`install_instructions` creates the `instructions` dir, with an absolute `<layer_name>_layer` symlink to each
selected layer, and an `examples` symlink to the reference apps.</br>
A new selection replaces the previous one: the symlinks of the layers that are no longer selected are removed.
Other files in the `instructions` dir are left alone.</br>

#### It generates the index

`get_index_text` inserts the index snippets of the selected layers, in order, into the index template of the
prompts-dir. `install_instructions` writes the result to `index.md`, which tells the agent which layers to consult,
and for what purpose.</br>
It also writes the manifest (`mn-prompts.yaml`), which records the target and the layers that the user asked for,
and the name of the agents file.</br>

#### It copies the agents file

The entrypoint calls `copy_agents_file`, which copies `agents_files/default.md` of the prompts-dir to `CLAUDE.md`
in the project dir, or to `AGENTS.md` if the user passed `--agents-md`.</br>
If the file already exists, then it's left unchanged, and the entrypoint prints how to extend it with the contents
of the agents file.</br>

#### It adds project-specific instructions

The user may write a `project.md` file in the `instructions` dir, e.g. to say which layers apply to which part of
the project. The generated index tells the agent to read it first, and mn-prompts never changes it.</br>

### Diagram

```mermaid
sequenceDiagram
    actor User
    participant MnPrompts as mn-prompts (entrypoint)
    participant InstallInstructions as InstallInstructions (action)
    participant GetTarget as GetTarget (rule)
    participant GetSelectedLayers as GetSelectedLayers (rule)
    participant GetIndexText as GetIndexText (rule)
    participant CopyAgentsFile as CopyAgentsFile (action)

    Note over User: Install mn-prompts
    User->>User: git clone <repo-url> ~/mn-prompts
    User->>User: pip install -e ~/mn-prompts

    Note over User,GetSelectedLayers: Select the layers
    User->>MnPrompts: mn-prompts install --target=<target_name> --layer=<layer_name>
    MnPrompts->>InstallInstructions: install_instructions(target_name, layer_names, agents_md)
    alt prompts-dir does not exist
        InstallInstructions-->>MnPrompts: raise PromptsDirNotFoundError
    else instructions exist, and were not installed by mn-prompts
        InstallInstructions-->>MnPrompts: raise InstructionsExistError
    end
    InstallInstructions->>GetTarget: get_target(target_name)
    GetTarget-->>InstallInstructions: target (with its layer names)
    InstallInstructions->>GetSelectedLayers: get_selected_layers(layer_names)
    GetSelectedLayers-->>InstallInstructions: layers, with the required layers, in order

    Note over InstallInstructions: Link the layers
    InstallInstructions->>InstallInstructions: create <layer_name>_layer symlinks, and the examples symlink
    InstallInstructions->>InstallInstructions: remove the symlinks of layers that are not selected

    Note over InstallInstructions,GetIndexText: Generate the index
    InstallInstructions->>GetIndexText: get_index_text(layers)
    GetIndexText-->>InstallInstructions: index template with the index snippets
    InstallInstructions->>InstallInstructions: write index.md and mn-prompts.yaml
    InstallInstructions-->>MnPrompts: manifest

    Note over MnPrompts,CopyAgentsFile: Copy the agents file
    MnPrompts->>CopyAgentsFile: copy_agents_file(agents_file_name)
    alt CLAUDE.md (or AGENTS.md) does not exist
        CopyAgentsFile->>CopyAgentsFile: copy agents_files/default.md
    else it exists
        CopyAgentsFile-->>MnPrompts: not copied
        MnPrompts-->>User: how to extend the agents file
    end

    Note over User: Add project-specific instructions
    User->>User: write instructions/project.md
```
"""
