import json

from e2e_test_env import Context, TestEnv, requires_jaz

LOCAL_CONFIG = """
docker:
  shell: fish
fe:
  shell: bash
"""


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_developer_runs_the_servers_by_hand(context: Context):
    # Create the test environment
    env = create_env(context)

    # The stack runs, and docker is faked.
    if env.step(
        env.install_fake_tools(),
    ):
        pass

    # We look at the tmux menu.
    #
    # It should only have the commands that run the servers.
    if env.step(
        env.run_jaz("config.print", "/tmux/menu"),
    ):
        assert env.exit_code == 0
        assert json.loads(env.output) == {
            "serve": ["jaz be.run-server", "jaz fe.run-server"]
        }

    # We run the server of the backend, and then the server of the frontend.
    #
    # Each should run jaz run-server in the container of the service, which it
    # knows from the config: it should not list the containers.
    if env.step(
        env.run_jaz("be.run-server"),
        env.run_jaz("fe.run-server"),
    ):
        assert env.exit_code == 0
        assert env.exec_calls() == [
            ["blogs_be", "jaz", "run-server"],
            ["blogs_fe", "jaz", "run-server"],
        ]
        assert [x for x in env.calls("docker") if x["args"][:1] == ["ps"]] == []

    # We open a shell in the backend, and then in the frontend.
    #
    # Each should open /docker/shell in the container of the service: /be/shell
    # and /fe/shell follow it.
    if env.step(
        env.forget_calls(),
        env.run_jaz("be.shell"),
        env.run_jaz("fe.shell"),
    ):
        assert env.exit_code == 0
        assert env.exec_calls() == [["blogs_be", "sh"], ["blogs_fe", "sh"]]

    # We use fish as our shell, but bash in the frontend.
    #
    # be.shell should open fish, and fe.shell bash.
    if env.step(
        env.write_local_config(LOCAL_CONFIG),
        env.forget_calls(),
        env.run_jaz("be.shell"),
        env.run_jaz("fe.shell"),
    ):
        assert env.exit_code == 0
        assert env.exec_calls() == [["blogs_be", "fish"], ["blogs_fe", "bash"]]

    # We run a command as root in the work dir /app of the backend.
    #
    # It should pass the user and the work dir to docker exec, and split the
    # command into words.
    if env.step(
        env.forget_calls(),
        env.run_jaz(
            "be.exec", "cmd=python manage.py check", "user=root", "workdir=/app"
        ),
    ):
        assert env.exit_code == 0
        assert env.docker_args() == [
            "exec",
            "--interactive",
            "--user",
            "root",
            "--workdir",
            "/app",
            "blogs_be",
            "python",
            "manage.py",
            "check",
        ]

    # We run a command that fails with exit code 3.
    #
    # The target should fail, and report the exit code of the command, without a
    # traceback.
    if env.step(
        env.fail_tool("docker", 3),
        env.run_jaz("be.exec", "cmd=false"),
    ):
        assert env.exit_code != 0
        assert "exit code 3" in env.error_output
        assert "Traceback" not in env.error_output

    # We look at the dial keys.
    #
    # F2 and F3 should insert the start of a be and fe command, and Shift+F1,
    # Shift+F2 and Shift+F3 should go to the root dir, the backend and the frontend.
    if env.step(
        env.read_dial_key("2", store_as="f2"),
        env.read_dial_key("3", store_as="f3"),
        env.read_dial_key("1", group="shift", store_as="shift_f1"),
        env.read_dial_key("2", group="shift", store_as="shift_f2"),
        env.read_dial_key("3", group="shift", store_as="shift_f3"),
    ):
        assert env.f2 == "zoo be."
        assert env.f3 == "zoo fe."
        assert env.shift_f1 == str(env.project_dir)
        assert env.shift_f2 == str(env.project_file("src/services/blogs_be"))
        assert env.shift_f3 == str(env.project_file("src/services/blogs_fe"))


class Env(TestEnv):
    def __post_init__(self):
        self.f2 = None
        self.f3 = None
        self.shift_f1 = None
        self.shift_f2 = None
        self.shift_f3 = None

    def read_dial_key(self, number: str, store_as: str, group: str = "default"):
        """Stores what dial.get prints for the key, as the key bindings call it: the
        keys of the shift group are directories."""
        dir_args = ["dir=true"] if group == "shift" else []
        self.run_jaz("dial.get", number, f"group={group}", *dir_args)
        setattr(self, store_as, self.output.strip())

    # Queries

    def exec_calls(self):
        """The container and the command of each docker exec call, without the
        options."""
        return [
            [x for x in call["args"][1:] if not x.startswith("--")]
            for call in self.calls("docker")
            if call["args"][:1] == ["exec"]
        ]

    def docker_args(self):
        """The arguments of the last docker call."""
        return self.calls("docker")[-1]["args"]
