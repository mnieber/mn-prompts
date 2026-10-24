import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s30_a_user_installs_the_prompts_for_their_project")


def run_scenario():
    r.user = c.External.Actors.User
    r.mn_prompts_entrypoint = c.Runtime.Entrypoints.MnPrompts
    r.install_target_action = c.Targets.Actions.InstallTarget
    r.copy_agents_file_action = c.Targets.Actions.CopyAgentsFile
    r.get_targets_dir_rule = c.Prompts.Rules.GetTargetsDir
    r.get_prompts_dir_rule = c.Prompts.Rules.GetPromptsDir

    with goal().install_the(r.instructions).of_a(r.target).in_the(r.project_dir):

        # Install mn-prompts
        the(r.user).clones_the(r.mn_prompts_repo)
        the(r.user).pip_installs_the(r.mn_prompts_repo).as_an_editable_install()

        # Install the target
        with the(r.user).calls(r.mn_prompts_entrypoint).with_the(r.target_name):
            with it().calls(r.install_target_action).with_the(r.target_name):
                with it().calls(r.get_targets_dir_rule):
                    it().calls(r.get_prompts_dir_rule)
                    it().raises(r.prompts_dir_not_found_error).if_it_does_not_exist()
                it().raises(r.unknown_target_error).if_the(r.target).does_not_exist()
                it().raises(r.instructions_exist_error).if_the(r.instructions).exist()
                it().creates_an(r.instructions_symlink).to_the(r.target)

            # Copy the agents file
            with the(r.mn_prompts_entrypoint).calls(r.copy_agents_file_action):
                it().copies_the(r.agents_file).to_the(r.project_dir)
                it().leaves_the(r.agents_file).unchanged_if_it_exists()
            the(r.mn_prompts_entrypoint).prints_how_to_extend_the(r.agents_file)


markdown_node = sunya.add_markdown_node(
    scenario, "A user installs the prompts for their project"
)

markdown_node.markdown = """
A user installs the instructions of a target (e.g. `python_lib`) in their project. The project gets an
`instructions` symlink into the user's clone of mn-prompts, and an `AGENTS.md` file that tells the agent how to use
these instructions.

### Steps

#### It installs mn-prompts

The user clones the mn-prompts repository, and pip installs it as an editable install.</br>
Only editable installs are supported: the prompts-dir (`extra/prompts`) contains symlinks (e.g. from targets to
layers), which a wheel cannot contain.</br>
The user installs from a plain clone rather than with `pip install -e git+<url>`, because the latter puts the clone
inside the Python environment, where it's deleted when that environment is recreated.</br>

#### It installs the target

The user calls `mn-prompts install <target_name>` in the project dir.</br>
The entrypoint calls `install_target`, which locates the prompts-dir (via `get_targets_dir` and
`get_prompts_dir`) and checks that the target exists.</br>
`install_target` creates an `instructions` symlink to the target dir. An existing symlink into the prompts-dir is
replaced, so that the user can repair it, or switch to another target.</br>

#### It copies the agents file

The entrypoint calls `copy_agents_file`, which copies `agents_files/default.md` of the prompts-dir to `AGENTS.md`
in the project dir.</br>
If `AGENTS.md` already exists, then it's left unchanged, and the entrypoint prints how to extend it with the
contents of the agents file.</br>

### Diagram

```mermaid
sequenceDiagram
    actor User
    participant MnPrompts as mn-prompts (entrypoint)
    participant InstallTarget as InstallTarget (action)
    participant GetTargetsDir as GetTargetsDir (rule)
    participant GetPromptsDir as GetPromptsDir (rule)
    participant CopyAgentsFile as CopyAgentsFile (action)

    Note over User: Install mn-prompts
    User->>User: git clone <repo-url> ~/mn-prompts
    User->>User: pip install -e ~/mn-prompts

    Note over User,GetPromptsDir: Install the target
    User->>MnPrompts: mn-prompts install <target_name>
    MnPrompts->>InstallTarget: install_target(target_name)
    InstallTarget->>GetTargetsDir: get_targets_dir()
    GetTargetsDir->>GetPromptsDir: get_prompts_dir()
    GetPromptsDir-->>GetTargetsDir: prompts_dir
    alt prompts_dir does not exist
        GetTargetsDir-->>MnPrompts: raise PromptsDirNotFoundError
    end
    GetTargetsDir-->>InstallTarget: targets_dir
    alt target does not exist
        InstallTarget-->>MnPrompts: raise UnknownTargetError
    else instructions exist (and are not a symlink into targets_dir)
        InstallTarget-->>MnPrompts: raise InstructionsExistError
    end
    InstallTarget->>InstallTarget: create instructions symlink to the target

    Note over MnPrompts,CopyAgentsFile: Copy the agents file
    MnPrompts->>CopyAgentsFile: copy_agents_file()
    alt AGENTS.md does not exist
        CopyAgentsFile->>CopyAgentsFile: copy agents_files/default.md to AGENTS.md
    else AGENTS.md exists
        CopyAgentsFile-->>MnPrompts: not copied
        MnPrompts-->>User: how to extend AGENTS.md
    end
```
"""
