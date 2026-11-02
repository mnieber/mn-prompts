import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s35_a_user_reinstalls_the_instructions")


def run_scenario():
    r.user = c.External.Actors.User
    r.mn_prompts_entrypoint = c.Runtime.Entrypoints.MnPrompts
    r.install_instructions_action = c.Instructions.Actions.InstallInstructions
    r.copy_agents_file_action = c.Instructions.Actions.CopyAgentsFile
    r.get_manifest_rule = c.Instructions.Rules.GetManifest

    with goal().reinstall_the(r.instructions).in_the(r.project_dir):

        # Change the clone or the project
        the(r.user).updates_or_moves_the(r.mn_prompts_repo).or_clones_the(r.project)

        # Re-install the selection of the manifest
        with the(r.user).calls(r.mn_prompts_entrypoint).without_a(r.selection):
            with it().calls(r.install_instructions_action):
                with it().calls(r.get_manifest_rule):
                    it().reads_the(r.target_name).the(r.layer_names).and_the(
                        r.agents_file_name
                    ).from_the(r.manifest)
                it().raises(r.missing_selection_error).if_there_is_no(r.manifest)
                it().installs_the(r.instructions).of_the(r.selection)
            the(r.mn_prompts_entrypoint).calls(r.copy_agents_file_action)


markdown_node = sunya.add_markdown_node(scenario, "A user reinstalls the instructions")

markdown_node.markdown = """
A user re-installs the instructions of their project with the selection that is recorded in its manifest. The
generated `index.md` contains copies of the index snippets, so this is how the project picks up changes in the
user's clone of mn-prompts.

### Steps

#### It changes the clone or the project

The user re-installs the instructions when:

- they pulled changes into their clone of mn-prompts, which may change the index snippets, the targets and the
  layers that layers require;
- they moved their clone, so that the symlinks in the `instructions` dir are dangling;
- they cloned a project in which a team member committed the manifest (and `project.md`) of the `instructions`
  dir. Whether to commit the instructions is up to the team.

#### It re-installs the selection of the manifest

The user calls `mn-prompts install` without a `--target` and `--layer`s.</br>
`install_instructions` calls `get_manifest`, which reads the target, the layers and the name of the agents file from
`instructions/mn-prompts.yaml`. Without a manifest, it raises a `MissingSelectionError` that explains the
options.</br>
`install_instructions` then installs this selection as usual: it resolves the layers again (so that a changed
target or layer is picked up), replaces the symlinks, and regenerates the index.</br>
The entrypoint calls `copy_agents_file` with the agents file of the manifest, unless the user passes
`--agents-md`, which switches the agents file to `AGENTS.md`.</br>

### Diagram

```mermaid
sequenceDiagram
    actor User
    participant MnPrompts as mn-prompts (entrypoint)
    participant InstallInstructions as InstallInstructions (action)
    participant GetManifest as GetManifest (rule)
    participant CopyAgentsFile as CopyAgentsFile (action)

    Note over User: Change the clone or the project
    alt pull changes into the clone
        User->>User: git -C ~/mn-prompts pull
    else move the clone
        User->>User: move ~/mn-prompts, and pip install it again
    else clone the project
        User->>User: git clone <project-url>
    end

    Note over User,CopyAgentsFile: Re-install the selection of the manifest
    User->>MnPrompts: mn-prompts install
    MnPrompts->>InstallInstructions: install_instructions()
    InstallInstructions->>GetManifest: get_manifest()
    alt no manifest
        InstallInstructions-->>MnPrompts: raise MissingSelectionError
    end
    GetManifest-->>InstallInstructions: target, layers and agents file
    InstallInstructions->>InstallInstructions: install the selection (symlinks, index.md, manifest)
    InstallInstructions-->>MnPrompts: manifest
    MnPrompts->>CopyAgentsFile: copy_agents_file(agents_file_name)
```
"""
