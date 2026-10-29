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
The developer runs `jaz tmux` to open a tmux session for the blogs project. The session
has a menu of commands, which is defined under `/tmux/menu` in the local config. Each
command that the developer picks runs in its own pane next to the menu. The `tmux`
target delegates to the `tmux_menu.py` script, which reads the config with
`get_config`.

### Steps

#### It opens the tmux session

The root module loads `env/local/config/base.yaml` with `⚙️.load_config`.</br>
The developer runs `jaz tmux`, which calls `open_session`.</br>
`open_session` reads the session name from `/tmux/session`.</br>
If the session does not exist yet, `open_session` creates it, copies
`JAZZOO_CONFIG_FILES` into the session environment, and starts `pick` in the
`Menu` window.</br>
Finally, `open_session` attaches to the session (or switches to it when the developer
is already inside tmux).</br>

#### It runs the selected commands

`pick` reads the menu from `/tmux/menu` and shows it.</br>
The developer selects one or more commands (e.g. `1,3-4`), or types a command.</br>
For each selected command, `pick` splits the `Menu` window and sends the command to the
new pane.</br>
`pick` then selects the menu pane again, so that the developer can pick the next
commands.</br>

### Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant TT as tmux (target)
    participant OS as open_session
    participant Pick as pick
    participant Tmux as tmux

    Note over Developer,Tmux: Open the tmux session
    Developer->>TT: jaz tmux
    TT->>OS: tmux_menu.py open
    OS->>OS: read /tmux/session

    opt session does not exist
        OS->>Tmux: new-session
        OS->>Tmux: set-environment JAZZOO_CONFIG_FILES
        OS->>Tmux: new-window Menu
        OS->>Tmux: send-keys "tmux_menu.py pick"
        Tmux->>Pick: start
    end
    OS->>Tmux: attach-session

    Note over Developer,Tmux: Run the selected commands
    Pick->>Pick: read /tmux/menu
    Pick-->>Developer: menu
    Developer->>Pick: 1,2

    loop each selected command
        Pick->>Tmux: split-window
        Pick->>Tmux: send-keys command
    end
    Pick->>Tmux: select-pane (menu)
```
"""
