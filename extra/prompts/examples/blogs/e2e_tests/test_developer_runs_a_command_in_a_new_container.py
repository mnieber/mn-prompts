from e2e_test_env import (
    COMPOSE_YML,
    OVERRIDE_YML,
    SRC_OVERLAYS_YML,
    Context,
    TestEnv,
    requires_jaz,
)

RUN_ARGS = ["run", "--rm", "--remove-orphans", "--service-ports", "blogs_be"]


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_developer_runs_a_command_in_a_new_container(context: Context):
    # Create the test environment
    env = create_env(context)

    # We run the migrations of blogs_be in a new container.
    #
    # It should use the same compose files as up, and pass the words of the command
    # after the name of the service.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.run_jaz("compose.run", "blogs_be", "cmd=python manage.py migrate"),
    ):
        assert env.exit_code == 0
        assert env.compose_files(env.last_call()) == [
            COMPOSE_YML,
            SRC_OVERLAYS_YML,
            OVERRIDE_YML,
        ]
        assert env.compose_command(env.last_call()) == [
            *RUN_ARGS,
            "python",
            "manage.py",
            "migrate",
        ]

    # We run a new blogs_be container without a command.
    #
    # It should run the default command of the service.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.run", "blogs_be"),
    ):
        assert env.exit_code == 0
        assert env.compose_command(env.last_call()) == RUN_ARGS


class Env(TestEnv):
    # Queries

    def last_call(self) -> dict:
        return self.calls("docker")[-1]
