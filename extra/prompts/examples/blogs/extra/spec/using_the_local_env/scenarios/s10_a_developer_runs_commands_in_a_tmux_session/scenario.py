import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s10_a_developer_runs_commands_in_a_tmux_session")


def run_scenario():
    r.developer = c.External.Actors.Developer
    r.tmux = c.External.Actors.Tmux
    r.tmux_target = c.Tmux.Targets.Tmux
    r.open_session_action = c.Tmux.Actions.OpenSession
    r.pick_action = c.Tmux.Actions.Pick

    with goal().open_a(r.tmux_session).with_a(r.menu).of_the(r.commands):
        the(r.root_module).loads_the(r.local_config)
        with the(r.developer).runs(r.tmux_target):
            with it().calls(r.open_session_action):
                it().reads_the(r.session_name).from_the(r.local_config)
                with it().creates_the(r.tmux_session).if_it_does_not_exist():
                    it().copies_the(r.config_list).into_the(r.tmux_session)
                    it().starts(r.pick_action).in_the(r.menu_window)
                it().attaches_to_the(r.tmux_session)

    with goal().run_the(r.selected_commands).in_the(r.tmux_session):
        with the(r.pick_action).reads_the(r.menu).from_the(r.local_config):
            it().shows_the(r.menu)
            the(r.developer).selects(r.commands).or_types_a(r.free_text_command)
            with the(r.pick_action).for_each_of_the(r.selected_commands):
                it().asks(r.tmux).to_split_the(r.menu_window)
                it().sends_the(r.command).to_the(r.new_pane)
            it().selects_the(r.menu_pane).again()


markdown_node = sunya.add_markdown_node(
    scenario, "A developer runs commands in a tmux session"
)

markdown_node.markdown = """
The developer opens a tmux session for the blogs project, which has a menu of commands. Each command that the
developer picks runs in its own pane next to the menu.

## Diagram

```mermaid
flowchart TD
    run(["The developer runs jaz tmux"]) --> session_name

    subgraph open_session ["Open a tmux session with a menu of the commands"]
        session_name["Read the session name from the local config [1]"] --> exists{{"Does the tmux session exist?"}}:::choice
        exists -- no --> create["Create the tmux session [2]"]
        exists -- yes --> attach["Attach to the tmux session [3]"]
        create --> attach
    end

    attach --> menu

    subgraph run_commands ["Run the selected commands in the tmux session"]
        menu["Show the menu [4]"] --> pick["The developer selects commands, or types a command"]
        pick --> panes["Run each command in a new pane next to the menu [5]"]
        panes -- "the developer picks the next commands" --> menu
    end

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - The tmux target delegates to the tmux_menu.py script

The root module loads `env/local/config/base.yaml` with `⚙️.load_config`.</br>
`jaz tmux` calls `open_session` of the `tmux_menu.py` script, which reads the config with `get_config`.
`open_session` reads the session name from `/tmux/session`.</br>

#### [2] - The session knows the config files of the project

`open_session` copies `JAZZOO_CONFIG_FILES` into the environment of the session, and starts `pick` in the `Menu`
window.</br>

#### [3] - Inside tmux, the developer switches to the session

When the developer is already inside tmux, `open_session` switches to the session instead of attaching to it.</br>

#### [4] - The menu is defined in the local config

`pick` reads the menu from `/tmux/menu`.</br>

#### [5] - The developer can pick several commands at once

The developer selects one or more commands (e.g. `1,3-4`). For each selected command, `pick` splits the `Menu`
window and sends the command to the new pane.</br>
`pick` then selects the menu pane again, so that the developer can pick the next commands.</br>
"""
