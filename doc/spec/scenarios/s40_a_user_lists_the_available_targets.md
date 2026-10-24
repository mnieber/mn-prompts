[comment]: <> (This file is auto-generated. Do not edit directly.)

# s40_a_user_lists_the_available_targets

## A user lists the available targets

A user lists the targets that they can install in their project.

### Steps

#### It lists the targets

The user calls `mn-prompts list`.</br>
The entrypoint calls `get_target_names`, which locates the prompts-dir (via `get_targets_dir` and
`get_prompts_dir`) and returns the names of the sub-dirs of its targets dir.</br>
The entrypoint prints the target names, one per line.</br>

### Diagram

```mermaid
sequenceDiagram
    actor User
    participant MnPrompts as mn-prompts (entrypoint)
    participant GetTargetNames as GetTargetNames (rule)
    participant GetTargetsDir as GetTargetsDir (rule)
    participant GetPromptsDir as GetPromptsDir (rule)

    User->>MnPrompts: mn-prompts list
    MnPrompts->>GetTargetNames: get_target_names()
    GetTargetNames->>GetTargetsDir: get_targets_dir()
    GetTargetsDir->>GetPromptsDir: get_prompts_dir()
    GetPromptsDir-->>GetTargetsDir: prompts_dir
    alt prompts_dir does not exist
        GetTargetsDir-->>MnPrompts: raise PromptsDirNotFoundError
    end
    GetTargetsDir-->>GetTargetNames: targets_dir
    GetTargetNames-->>MnPrompts: sorted target_names
    MnPrompts-->>User: target names, one per line
```

