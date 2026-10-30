from e2e_test_env import OVERRIDE_YML, SECRETS, Context, TestEnv, requires_jaz

SECRETS_ENV = "".join(f"{name}={value}\n" for name, value in SECRETS.items())
OVERRIDE = "services: {}\n"
POSTGRES_ENV = "env/local/docker/env_files/postgres.env"

TARGETS = [
    "compose.build",
    "compose.build-base-images",
    "compose.up",
    "compose.down",
    "compose.restart",
    "compose.run",
    "compose.compile-env-files",
    "python.pip-compile",
    "python.publish",
]


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_compose_keeps_the_developer_files(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have a secrets.env and an override file of our own.
    if env.step(
        env.install_fake_tools(),
        env.write_file("env/local/secrets.env", SECRETS_ENV),
        env.write_file(OVERRIDE_YML, OVERRIDE),
    ):
        pass

    # We build and start the stack.
    #
    # It should leave both files as they are.
    if env.step(
        env.run_jaz("compose.build"),
        env.run_jaz("compose.up"),
    ):
        assert env.exit_code == 0
        assert env.read_file("env/local/secrets.env") == SECRETS_ENV
        assert env.read_file(OVERRIDE_YML) == OVERRIDE


@requires_jaz()
def test_compose_compiles_the_env_files(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have the secrets in secrets.env.
    if env.step(
        env.install_fake_tools(),
        env.write_file("env/local/secrets.env", SECRETS_ENV),
    ):
        pass

    # We compile the env files.
    #
    # The secret should be filled into the env file of postgres, and docker should
    # not be called.
    if env.step(
        env.run_jaz("compose.compile-env-files"),
    ):
        assert env.exit_code == 0
        assert "POSTGRES_PASSWORD=pg-secret" in env.read_file(POSTGRES_ENV).splitlines()
        assert env.calls("docker") == []


@requires_jaz()
def test_compose_reports_a_failing_docker(context: Context):
    # Create the test environment
    env = create_env(context)

    # We start the stack, and docker fails.
    #
    # It should fail without a traceback: docker has already printed its error.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.fail_tool("docker", 3),
        env.run_jaz("compose.up"),
    ):
        assert env.exit_code != 0
        assert "Traceback" not in env.error_output


@requires_jaz()
def test_compose_lists_its_targets(context: Context):
    # Create the test environment
    env = create_env(context)

    # We list the targets of the project.
    #
    # It should list the compose and python targets. There is no compose.shell:
    # docker.exec opens a shell in a container.
    if env.step(
        env.run_jaz("--list-all"),
    ):
        assert env.exit_code == 0
        assert all(x in env.output.splitlines() for x in TARGETS)
        assert "compose.shell" not in env.output.splitlines()


class Env(TestEnv):
    pass
