from list_targets_tests.list_targets_test_env import Context, TestEnv


def create_env(context: Context):
    return Env(context)


def test_a_user_lists_the_available_targets(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the targets python_lib,
    # django_app and react_app.
    if env.step(
        env.install_editable(target_names=["python_lib", "django_app", "react_app"]),
        env.enter_project_dir(),
    ):
        pass

    # We list the available targets.
    #
    # The names of the targets should be printed in alphabetical order, one per
    # line.
    if env.step(
        env.run_mn_prompts("list"),
    ):
        assert env.exit_code == 0
        assert env.output_lines() == ["django_app", "python_lib", "react_app"]


class Env(TestEnv):
    pass
