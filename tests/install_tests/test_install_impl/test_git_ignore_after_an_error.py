from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv

from mn_prompts.targets.rules.get_target import UnknownTargetError

GIT_IGNORE_TEXT = "__pycache__/\n"


def create_env(context: Context):
    return Env(context)


def test_git_ignore_after_an_error(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib, and
    # a project with a .gitignore.
    if env.step(
        env.install_editable(
            targets={"python_lib": ["app", "python_lib"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
        env.write_project_file(".gitignore", GIT_IGNORE_TEXT),
    ):
        pass

    # We install the prompts of a target that doesn't exist, and ask to ignore
    # the installed files.
    #
    # It should raise an UnknownTargetError, and leave .gitignore unchanged.
    if env.step(
        env.run_mn_prompts_and_catch_error(
            "install", "--target=pyhton_lib", "--git-ignore"
        ),
    ):
        assert isinstance(env.error, UnknownTargetError)
        assert env.read_project_file(".gitignore") == GIT_IGNORE_TEXT


class Env(TestEnv):
    pass
