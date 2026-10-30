import getpass
import os

from e2e_test_env import Context, TestEnv, requires_tmux_and_jaz

SESSION = "blogs"
MENU_WINDOW = "blogs:1"
PROMPT = "Select one or more commands"
CONFIG_FILES = ["env/local/config/base.yaml", "env/local/config/local.yaml"]

# Commands that run on the host, next to the serve commands of the base config
LOCAL_CONFIG = """
tmux:
  menu:
    examples:
      - whoami
      - date
      - uptime
"""


def create_env(context: Context):
    return Env(context)


@requires_tmux_and_jaz()
def test_developer_runs_commands_in_a_tmux_session(context: Context):
    # Create the test environment
    env = create_env(context)

    # We add a category of example commands to the menu, in our local config.
    if env.step(
        env.write_local_config(LOCAL_CONFIG),
    ):
        pass

    # We run jaz tmux with a category that is not in the menu.
    #
    # It should fail with the list of known categories, before it creates a
    # session.
    if env.step(
        env.run_jaz("tmux", "nope"),
    ):
        assert env.exit_code != 0
        assert "Unknown category: nope (known: serve, examples)" in env.error_output
        assert env.sessions() == []

    # We run jaz tmux in a terminal.
    #
    # It should create the blogs session and attach to it. The Menu window should
    # show the commands of the config, and the session should know the config
    # files, so that the menu could read them.
    if env.step(
        env.run_jaz_in_terminal("tmux"),
        env.wait_until(lambda: PROMPT in env.pane_text(MENU_WINDOW)),
    ):
        assert env.sessions() == [SESSION]
        assert len(env.clients(SESSION)) == 1
        assert " 1 [   serve] - jaz be.run-server" in env.pane_text(MENU_WINDOW)
        assert " 3 [examples] - whoami" in env.pane_text(MENU_WINDOW)
        assert env.session_env(SESSION, "JAZZOO_CONFIG_FILES") == os.pathsep.join(
            str(env.project_file(x)) for x in CONFIG_FILES
        )

    # We pick the first two example commands in the menu.
    #
    # Each should run in a new pane: the whoami pane shows the user. When the menu
    # asks again, the menu pane should be the active pane, ready for the next pick.
    if env.step(
        env.remember_menu_pane(),
        env.type_in_pane(MENU_WINDOW, "3,4"),
        env.wait_until(lambda: len(env.panes(MENU_WINDOW)) == 3),
        env.wait_until(lambda: env.pane_shows_line(getpass.getuser())),
        env.wait_until(lambda: PROMPT in env.last_line(env.menu_pane)),
    ):
        assert env.active_pane(MENU_WINDOW) == env.menu_pane

    # We type a command that is not in the menu.
    #
    # It should run in another new pane.
    if env.step(
        env.type_in_pane(MENU_WINDOW, "echo free-text"),
        env.wait_until(lambda: len(env.panes(MENU_WINDOW)) == 4),
        env.wait_until(lambda: env.pane_shows_line("free-text")),
        env.wait_until(lambda: PROMPT in env.last_line(env.menu_pane)),
    ):
        assert env.active_pane(MENU_WINDOW) == env.menu_pane

    # We run jaz tmux in a second terminal.
    #
    # It should attach to the existing session, without creating another session
    # or a new menu.
    if env.step(
        env.run_jaz_in_terminal("tmux"),
        env.wait_until(lambda: len(env.clients(SESSION)) == 2),
    ):
        assert env.sessions() == [SESSION]
        assert len(env.panes(MENU_WINDOW)) == 4


class Env(TestEnv):
    def __post_init__(self):
        self.menu_pane = None

    def remember_menu_pane(self):
        self.menu_pane = self.active_pane(MENU_WINDOW)

    # Queries

    def pane_shows_line(self, text: str) -> bool:
        return any(
            text in [line.strip() for line in self.pane_text(pane).splitlines()]
            for pane in self.panes(MENU_WINDOW)
            if pane != self.menu_pane
        )

    def last_line(self, pane: str) -> str:
        lines = [line for line in self.pane_text(pane).splitlines() if line.strip()]
        return lines[-1] if lines else ""
