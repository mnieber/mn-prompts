from e2e_test_env import Context, TestEnv, requires_jaz

NO_SERVICES = """\
python:
  services: []
"""


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_pip_compile_without_services(context: Context):
    # Create the test environment
    env = create_env(context)

    # The developer removes all services from /python/services, and compiles the
    # requirements.
    #
    # It should succeed without calling uv.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.write_local_config(NO_SERVICES),
        env.run_jaz("python.pip-compile"),
    ):
        assert env.exit_code == 0
        assert env.calls("uv") == []


@requires_jaz()
def test_restart_stops_when_pip_compile_fails(context: Context):
    # Create the test environment
    env = create_env(context)

    # We compile the requirements, and uv fails.
    #
    # It should fail without a traceback.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.fail_tool("uv", 2),
        env.run_jaz("python.pip-compile"),
    ):
        assert env.exit_code != 0
        assert "Traceback" not in env.error_output

    # We restart the stack, and uv fails.
    #
    # It should stop after down: the images are not built, and the stack is not
    # started.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.restart"),
    ):
        assert env.exit_code != 0
        assert env.call_summary() == [("docker", "down"), ("uv", "pip compile")]


class Env(TestEnv):
    pass
