import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s40_a_user_lists_the_available_targets")


def run_scenario():
    r.user = c.External.Actors.User
    r.mn_prompts_entrypoint = c.Runtime.Entrypoints.MnPrompts
    r.get_target_names_rule = c.Targets.Rules.GetTargetNames
    r.get_targets_dir_rule = c.Prompts.Rules.GetTargetsDir
    r.get_prompts_dir_rule = c.Prompts.Rules.GetPromptsDir

    with goal().list_the_available(r.targets):
        with the(r.user).calls(r.mn_prompts_entrypoint).with_the(r.list_command):
            with it().calls(r.get_target_names_rule):
                with it().calls(r.get_targets_dir_rule):
                    it().calls(r.get_prompts_dir_rule)
                    it().raises(r.prompts_dir_not_found_error).if_it_does_not_exist()
                it().returns_the_sorted(r.target_names)
            the(r.mn_prompts_entrypoint).prints_the(r.target_names).one_per_line()


markdown_node = sunya.add_markdown_node(
    scenario, "A user lists the available targets"
)

markdown_node.markdown = """
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
"""
