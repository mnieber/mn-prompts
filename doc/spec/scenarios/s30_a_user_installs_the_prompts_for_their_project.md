[comment]: <> (This file is auto-generated. Do not edit directly.)

# s30_a_user_installs_the_prompts_for_their_project

## A user installs the prompts for their project

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

