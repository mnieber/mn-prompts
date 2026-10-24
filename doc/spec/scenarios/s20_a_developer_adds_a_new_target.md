[comment]: <> (This file is auto-generated. Do not edit directly.)

# s20_a_developer_adds_a_new_target

## A developer adds a new target

A developer adds a target with the instructions for generating a type of application (e.g. a django app). The
target combines the layers of the technologies that this application uses.

### Steps

#### It creates the target

The developer creates the `targets/<target_name>` dir in the prompts-dir. The `<target_name>` is the name that the
user passes to `mn-prompts install`.</br>

#### It adds the symlinks

For each layer that the target uses, the developer adds a `<layer_name>_layer` symlink to
`../../layers/<layer_name>`. This lets targets share layers without duplicating them.</br>
The developer adds an `examples` symlink to `../../examples`.</br>

#### It writes the index file

The developer writes the `index.md` file of the target, which is the starting point for the agent. It explains
which layer `index.md` files to consult, and for what purpose, and refers to the relevant example apps.</br>

#### It checks the target

The developer calls `mn-prompts list`, and checks that the new target is listed.</br>

### Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant Target as targets/<target_name>
    participant MnPrompts as mn-prompts (entrypoint)

    Note over Developer,Target: Create the target
    Developer->>Target: create dir

    Note over Developer,Target: Add the symlinks
    loop for each layer
        Developer->>Target: symlink <layer_name>_layer -> ../../layers/<layer_name>
    end
    Developer->>Target: symlink examples -> ../../examples

    Note over Developer,Target: Write the index file
    Developer->>Target: write index.md

    Note over Developer,MnPrompts: Check the target
    Developer->>MnPrompts: mn-prompts list
    MnPrompts-->>Developer: target names (including <target_name>)
```

