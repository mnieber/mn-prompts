from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv


def create_env(context: Context):
    return Env(context)


def test_a_user_ignores_the_installed_files(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib, and
    # an empty project dir. We don't want to commit the installed files.
    if env.step(
        env.install_editable(
            targets={"python_lib": ["app", "python_lib"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
    ):
        assert not env.project_path_exists(".gitignore")

    # We install the prompts of the python_lib target, and ask to ignore the
    # installed files.
    #
    # It should create a .gitignore with the agents file and the instructions
    # dir, anchored to the project dir.
    if env.step(
        env.run_mn_prompts("install", "--target=python_lib", "--git-ignore"),
    ):
        assert env.exit_code == 0
        assert env.index_layer_order() == ["app", "python_lib"]
        assert env.read_project_file(".gitignore") == "/CLAUDE.md\n/instructions/\n"

    # We re-install the prompts, and ask again to ignore the installed files.
    #
    # The entries are already in .gitignore, so it should be unchanged.
    if env.step(
        env.run_mn_prompts("install", "--git-ignore"),
    ):
        assert env.exit_code == 0
        assert env.read_project_file(".gitignore") == "/CLAUDE.md\n/instructions/\n"


class Env(TestEnv):
    pass
