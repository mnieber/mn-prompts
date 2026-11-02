import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s40_a_user_lists_the_targets_and_layers")


def run_scenario():
    r.user = c.External.Actors.User
    r.mn_prompts_entrypoint = c.Runtime.Entrypoints.MnPrompts
    r.get_target_names_rule = c.Targets.Rules.GetTargetNames
    r.get_target_rule = c.Targets.Rules.GetTarget
    r.get_layer_names_rule = c.Layers.Rules.GetLayerNames
    r.get_prompts_dir_rule = c.Prompts.Rules.GetPromptsDir

    with goal().list_the_available(r.targets).and_the(r.layers):
        with the(r.user).calls(r.mn_prompts_entrypoint).with_the(r.list_command):

            # List the targets
            with it().calls(r.get_target_names_rule):
                with it().calls(r.get_prompts_dir_rule):
                    it().raises(r.prompts_dir_not_found_error).if_it_does_not_exist()
                it().returns_the_sorted(r.target_names)
            with the(r.mn_prompts_entrypoint).calls(r.get_target_rule).for_each(
                r.target_name
            ):
                it().reads_the(r.description).and_the(r.layer_names).from_the(
                    r.target_file
                )
            the(r.mn_prompts_entrypoint).prints_the(r.targets).in_columns()

            # List the layers
            with the(r.mn_prompts_entrypoint).calls(r.get_layer_names_rule):
                it().returns_the_sorted(r.layer_names)
            the(r.mn_prompts_entrypoint).prints_the(r.layer_names)


markdown_node = sunya.add_markdown_node(scenario, "A user lists the targets and layers")

markdown_node.markdown = """
A user lists the targets and the layers that they can install in their project.

### Steps

#### It lists the targets

The user calls `mn-prompts list`.</br>
The entrypoint calls `get_target_names`, which locates the prompts-dir (via `get_prompts_dir`) and returns the names
of the target files in its targets dir, in alphabetical order.</br>
For each target, `get_target` reads the description and the layers from the target file. The entrypoint prints the
targets under a `Targets:` header, one per line, with the name, the description and the layers in columns.</br>

#### It lists the layers

The entrypoint calls `get_layer_names`, which returns the names of the dirs in the layers dir of the prompts-dir,
in alphabetical order. The entrypoint prints them under a `Layers:` header, one per line.</br>

### Diagram

```mermaid
sequenceDiagram
    actor User
    participant MnPrompts as mn-prompts (entrypoint)
    participant GetTargetNames as GetTargetNames (rule)
    participant GetTarget as GetTarget (rule)
    participant GetLayerNames as GetLayerNames (rule)

    Note over User,GetTarget: List the targets
    User->>MnPrompts: mn-prompts list
    MnPrompts->>GetTargetNames: get_target_names()
    alt prompts_dir does not exist
        GetTargetNames-->>MnPrompts: raise PromptsDirNotFoundError
    end
    GetTargetNames-->>MnPrompts: sorted target_names
    loop for each target_name
        MnPrompts->>GetTarget: get_target(target_name)
        GetTarget-->>MnPrompts: target (description, layer names)
    end
    MnPrompts-->>User: Targets: name, description and layers, in columns

    Note over MnPrompts,GetLayerNames: List the layers
    MnPrompts->>GetLayerNames: get_layer_names()
    GetLayerNames-->>MnPrompts: sorted layer_names
    MnPrompts-->>User: Layers: one per line
```
"""
