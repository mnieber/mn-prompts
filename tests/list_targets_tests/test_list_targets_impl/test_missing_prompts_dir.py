from list_targets_tests.list_targets_test_env import Context, TestEnv

from mn_prompts.prompts.rules.get_targets_dir import PromptsDirNotFoundError


def create_env(context: Context):
    return Env(context)


def test_missing_prompts_dir(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have a regular (non-editable) install of mn-prompts, which has no
    # prompts-dir.
    if env.step(
        env.install_regular(),
        env.enter_project_dir(),
    ):
        pass

    # We list the available targets.
    #
    # It should raise a PromptsDirNotFoundError.
    if env.step(
        env.run_mn_prompts_and_catch_error("list"),
    ):
        assert isinstance(env.error, PromptsDirNotFoundError)

    # We list the available targets in the same way as the user does.
    #
    # It should print an error that explains how to install mn-prompts as an
    # editable install, and return exit code 1.
    if env.step(
        env.run_mn_prompts_cli("list"),
    ):
        assert env.exit_code == 1
        assert env.output == ""
        assert env.error_output.startswith("PromptsDirNotFoundError: ")
        assert "editable install" in env.error_output
        assert "pip install -e" in env.error_output


class Env(TestEnv):
    pass
