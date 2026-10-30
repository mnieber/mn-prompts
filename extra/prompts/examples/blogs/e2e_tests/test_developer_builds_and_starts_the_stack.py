from e2e_test_env import (
    BASE_IMAGES_YML,
    COMPOSE_YML,
    OVERRIDE_YML,
    SRC_OVERLAYS_YML,
    Context,
    TestEnv,
    requires_jaz,
)

ENV_FILES = [
    "env/local/docker/env_files/blogs_be.env",
    "env/local/docker/env_files/blogs_fe.env",
    "env/local/docker/env_files/postgres.env",
]


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_developer_builds_and_starts_the_stack(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have the blogs project, without a local.yaml, and docker is faked.
    if env.step(
        env.install_fake_tools(),
    ):
        assert not env.project_file("env/local/config/local.yaml").exists()

    # We build the base images.
    #
    # It should run docker compose with the base-images file, for the blogs project.
    # The custom packages are empty, so there should be no build args.
    if env.step(
        env.run_jaz("compose.build-base-images"),
    ):
        assert env.exit_code == 0
        assert len(env.calls("docker")) == 1
        assert env.compose_files(env.last_call()) == [BASE_IMAGES_YML]
        assert env.compose_command(env.last_call()) == ["build"]
        assert env.build_args(env.last_call()) == []
        assert env.last_call()["env"]["ROOT_DIR"] == str(env.project_dir)
        assert env.last_call()["env"]["COMPOSE_PROJECT_NAME"] == "blogs"
        assert env.last_call()["env"]["DOCKER_BUILDKIT"] == "1"
        assert env.last_call()["env"]["COMPOSE_BAKE"] == "true"

    # We build the images of the services.
    #
    # It should first create secrets.env and compile the env files. The images are
    # built from the Dockerfiles, so only the base compose file is used.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.build"),
    ):
        assert env.exit_code == 0
        assert env.project_file("env/local/secrets.env").exists()
        assert all(env.project_file(x).exists() for x in ENV_FILES)
        assert len(env.calls("docker")) == 1
        assert env.compose_files(env.last_call()) == [COMPOSE_YML]
        assert env.compose_command(env.last_call()) == ["build"]

    # We start the stack.
    #
    # It should create the override file, and start the stack with the src overlays
    # and the override file.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.up"),
    ):
        assert env.exit_code == 0
        assert env.project_file(OVERRIDE_YML).exists()
        assert len(env.calls("docker")) == 1
        assert env.compose_files(env.last_call()) == [
            COMPOSE_YML,
            SRC_OVERLAYS_YML,
            OVERRIDE_YML,
        ]
        assert env.compose_command(env.last_call()) == ["up"]
        assert env.last_call()["env"]["COMPOSE_PROJECT_NAME"] == "blogs"

    # We stop the stack.
    #
    # It should use the same files as up, and remove the orphan containers.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.down"),
    ):
        assert env.exit_code == 0
        assert len(env.calls("docker")) == 1
        assert env.compose_files(env.last_call()) == [
            COMPOSE_YML,
            SRC_OVERLAYS_YML,
            OVERRIDE_YML,
        ]
        assert env.compose_command(env.last_call()) == ["down", "--remove-orphans"]


class Env(TestEnv):
    # Queries

    def last_call(self) -> dict:
        return self.calls("docker")[-1]
