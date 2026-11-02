from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv


def create_env(context: Context):
    return Env(context)


def test_no_git_ignore_without_the_option(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib, and
    # an empty project dir.
    if env.step(
        env.install_editable(
            targets={"python_lib": ["app", "python_lib"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
    ):
        pass

    # We install the prompts of the python_lib target, without --git-ignore.
    #
    # It should not create a .gitignore.
    if env.step(
        env.run_mn_prompts("install", "--target=python_lib"),
    ):
        assert env.exit_code == 0
        assert not env.project_path_exists(".gitignore")


class Env(TestEnv):
    pass
