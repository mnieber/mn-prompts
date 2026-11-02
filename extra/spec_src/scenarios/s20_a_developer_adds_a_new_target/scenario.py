import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s20_a_developer_adds_a_new_target")


def run_scenario():
    r.developer = c.External.Actors.Developer
    r.mn_prompts_entrypoint = c.Runtime.Entrypoints.MnPrompts

    with goal().add_a(r.target).for_a(r.type_of_application):

        # Write the target file
        with the(r.developer).writes_a(r.target_file).in_the(r.targets_dir):
            it().describes_the(r.type_of_application)
            it().lists_the(r.layers).of_the(r.target)

        # Check the target
        with the(r.developer).calls(r.mn_prompts_entrypoint).with_the(r.list_command):
            it().prints_the(r.target_name).the(r.description).and_the(r.layers).of_the(
                r.target
            )


markdown_node = sunya.add_markdown_node(scenario, "A developer adds a new target")

markdown_node.markdown = """
A developer adds a target for a type of application (e.g. a django app). A target is a named set of layers, so
that a user can install these layers with a single option.

### Steps

#### It writes the target file

The developer writes the `targets/<target_name>.yaml` file in the prompts-dir. The `<target_name>` is the name that
the user passes to `mn-prompts install --target`.</br>
The file has a `description` of the type of application, and lists the `layers` of the technologies that this
application uses (e.g. `layers: [app, django_app, python_lib]`). The layers that these layers require don't need
to be listed, because they are installed automatically.</br>

#### It checks the target

The developer calls `mn-prompts list`, and checks that the new target is listed, with its description and
layers.</br>

### Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant Targets as targets
    participant MnPrompts as mn-prompts (entrypoint)

    Note over Developer,Targets: Write the target file
    Developer->>Targets: write <target_name>.yaml (description, layers)

    Note over Developer,MnPrompts: Check the target
    Developer->>MnPrompts: mn-prompts list
    MnPrompts-->>Developer: targets (including <target_name>) and layers
```
"""
