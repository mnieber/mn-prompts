[comment]: <> (This file is auto-generated. Do not edit directly.)

# s40_a_user_lists_the_targets_and_layers

## A user lists the targets and layers

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

