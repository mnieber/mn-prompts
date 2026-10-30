from e2e_test_env import (
    COMPOSE_YML,
    DOCKERFILE_LOCAL_YML,
    OVERRIDE_YML,
    SRC_OVERLAYS_YML,
    Context,
    TestEnv,
    requires_jaz,
)

LOCAL_CONFIG = """\
compose:
  use_dockerfile_local: true
  os_custom_packages: nano curl fish
"""


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_developer_uses_local_settings(context: Context):
    # Create the test environment
    env = create_env(context)

    # The developer writes their own settings to local.yaml: build from the
    # Dockerfile.local files, and add some packages to the base images.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.write_local_config(LOCAL_CONFIG),
    ):
        pass

    # We build the base images.
    #
    # It should pass the custom OS packages as one build arg, and no build arg for
    # the pip packages, which are still empty.
    if env.step(
        env.run_jaz("compose.build-base-images"),
    ):
        assert env.exit_code == 0
        assert env.build_args(env.last_call()) == ["OS_CUSTOM_PACKAGES=nano curl fish"]

    # We build the images of the services.
    #
    # It should add the dockerfile-local file.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.build"),
    ):
        assert env.exit_code == 0
        assert env.compose_files(env.last_call()) == [COMPOSE_YML, DOCKERFILE_LOCAL_YML]

    # We start the stack.
    #
    # The dockerfile-local file should come after the src overlays and before the
    # override file, as in the just recipe.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.up"),
    ):
        assert env.exit_code == 0
        assert env.compose_files(env.last_call()) == [
            COMPOSE_YML,
            SRC_OVERLAYS_YML,
            DOCKERFILE_LOCAL_YML,
            OVERRIDE_YML,
        ]

    # We build once from the Dockerfiles, against the setting.
    #
    # It should only use the base compose file.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.build", "local=false"),
    ):
        assert env.exit_code == 0
        assert env.compose_files(env.last_call()) == [COMPOSE_YML]

    # We build without the docker cache.
    #
    # It should pass --no-cache to the build.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.build", "no-cache=true"),
    ):
        assert env.exit_code == 0
        assert env.compose_command(env.last_call()) == ["build", "--no-cache"]


class Env(TestEnv):
    # Queries

    def last_call(self) -> dict:
        return self.calls("docker")[-1]
