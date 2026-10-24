from install_target_tests.install_target_test_env import Context, TestEnv

from mn_prompts.prompts.rules.get_targets_dir import PromptsDirNotFoundError


def create_env(context: Context):
    return Env(context)


def test_install_without_prompts_dir(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have a regular (non-editable) install of mn-prompts, which has no
    # prompts-dir.
    if env.step(
        env.install_regular(),
        env.enter_project_dir(),
    ):
        pass

    # We install the python_lib target.
    #
    # It should raise a PromptsDirNotFoundError, and create no files.
    if env.step(
        env.run_mn_prompts_and_catch_error("install", "python_lib"),
    ):
        assert isinstance(env.error, PromptsDirNotFoundError)
        assert not env.project_path_exists("instructions")
        assert not env.project_path_exists("AGENTS.md")


class Env(TestEnv):
    pass
