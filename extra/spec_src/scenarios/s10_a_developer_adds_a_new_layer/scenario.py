import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s10_a_developer_adds_a_new_layer")


def run_scenario():
    r.developer = c.External.Actors.Developer

    with goal().add_a(r.layer).for_a(r.technology):

        # Create the layer
        the(r.developer).creates_a(r.layer_dir).in_the(r.layers_dir)

        # Write the skills
        with the(r.developer).writes_the(r.skills).of_the(r.layer):
            it().stores_each(r.skill).in_the(r.skills_dir).of_the(r.layer)
            it().refers_to(r.example_code).in_the(r.examples_dir)
            it().adds_an(r.example_app).if_no_suitable_example_exists()

        # Write the index file
        the(r.developer).writes_the(r.layer_index_file).that_lists_the(r.skills)


markdown_node = sunya.add_markdown_node(scenario, "A developer adds a new layer")

markdown_node.markdown = """
A developer adds a layer with the instructions for generating the code for a particular technology (e.g.
`python_lib`). Targets combine these layers.

### Steps

#### It creates the layer

The developer creates the `layers/<layer_name>` dir in the prompts-dir, where `<layer_name>` is snake_case (e.g.
`django_app`).</br>

#### It writes the skills

The developer writes one markdown file per skill in the `skills` dir of the layer. A skill describes how to
implement a particular pattern within the layer (e.g. how to write the `settings.py` file of a python library).</br>
The name of a skill file starts with a prefix that identifies the layer (e.g. `py-write-settings.md`).</br>
A skill may refer to example code in the `examples` dir of the prompts-dir. If no suitable example exists, the
developer adds a new example app.</br>

#### It writes the index file

The developer writes the `index.md` file of the layer, which is the starting point for the agent. It lists the
skills, each with a short description and a link to the skill file.</br>

### Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant Layer as layers/<layer_name>
    participant Examples as examples

    Note over Developer,Layer: Create the layer
    Developer->>Layer: create dir

    Note over Developer,Examples: Write the skills
    loop for each skill
        Developer->>Layer: write skills/<prefix>-<skill_name>.md
        opt no suitable example exists
            Developer->>Examples: add example app
        end
    end

    Note over Developer,Layer: Write the index file
    Developer->>Layer: write index.md (lists the skills)
```
"""
