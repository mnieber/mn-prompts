import socket

from e2e_test_env import (
    COMPOSE_YML,
    DOCKERFILE_LOCAL_YML,
    INIT_STACK_YML,
    OVERRIDE_YML,
    SECRETS,
    Context,
    TestEnv,
    requires_jaz,
)

SECRETS_ENV = "".join(f"{name}={value}\n" for name, value in SECRETS.items())
OVERRIDE = "services: {}\n"
POSTGRES_ENV = "env/local/docker/env_files/postgres.env"

TARGETS = [
    "compose.build",
    "compose.build-base-images",
    "compose.up",
    "compose.init",
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
def test_compose_down_removes_the_volumes(context: Context):
    # Create the test environment
    env = create_env(context)

    # We stop the stack with volumes=true.
    #
    # It should also remove the volumes, so that the next up starts with a new and
    # uninitialised stack.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.run_jaz("compose.down", "volumes=true"),
    ):
        assert env.exit_code == 0
        assert env.compose_command(env.calls("docker")[-1]) == [
            "down",
            "--remove-orphans",
            "--volumes",
        ]


@requires_jaz()
def test_compose_reads_local_as_a_jazzoo_flag(context: Context):
    # Create the test environment
    env = create_env(context)

    # We build with local=y, which jazzoo reads as true.
    #
    # It should build from the Dockerfile.local files.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.run_jaz("compose.build", "local=y"),
    ):
        assert env.exit_code == 0
        assert env.compose_files(env.calls("docker")[-1]) == [
            COMPOSE_YML,
            DOCKERFILE_LOCAL_YML,
        ]


@requires_jaz()
def test_compose_init_reports_an_unhealthy_stack(context: Context):
    # Create the test environment
    env = create_env(context)

    # We initialise the stack, and docker compose up fails (e.g. a service did not
    # become healthy).
    #
    # It should print the last lines of the logs of the stack, with the same files
    # as up, and fail without a traceback. It should not get the homepage, nor open
    # the browser.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.fail_tool("docker", 3),
        env.run_jaz("compose.init"),
    ):
        assert env.exit_code != 0
        assert "Traceback" not in env.error_output
        assert [env.compose_command(x)[0] for x in env.calls("docker")] == [
            "up",
            "logs",
        ]
        assert env.compose_command(env.calls("docker")[1]) == ["logs", "--tail=50"]
        assert env.compose_files(env.calls("docker")[1])[-1] == INIT_STACK_YML
        assert env.calls("browser") == []


@requires_jaz()
def test_compose_init_reports_an_unreachable_homepage(context: Context):
    # Create the test environment
    env = create_env(context)

    # The stack is healthy, but nothing listens on the port of the homepage.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.use_unreachable_homepage(),
    ):
        pass

    # We initialise the stack.
    #
    # It should report the homepage that it could not get, and end with exit code 1,
    # without a traceback and without opening the browser.
    if env.step(
        env.run_jaz("compose.init"),
    ):
        assert env.exit_code == 1
        assert env.homepage in env.error_output
        assert "Traceback" not in env.error_output
        assert env.calls("browser") == []


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
    def __post_init__(self):
        self.homepage = None

    def use_unreachable_homepage(self):
        """Makes a local port on which nothing listens the homepage of the project."""
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        self.homepage = f"http://127.0.0.1:{port}/"
        self.write_local_config(f"compose:\n  init:\n    homepage: {self.homepage}\n")
