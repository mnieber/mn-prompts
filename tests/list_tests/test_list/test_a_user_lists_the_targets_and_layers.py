from list_tests.list_test_env import Context, TestEnv


def create_env(context: Context):
    return Env(context)


def test_a_user_lists_the_targets_and_layers(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the targets python_lib and
    # django_app, and the layers that they use.
    if env.step(
        env.install_editable(
            targets={},
            layers={
                "app": [],
                "python_lib": ["app"],
                "django_app": ["app", "python_lib"],
                "local_env": [],
            },
        ),
        env.write_target(
            "python_lib",
            ["app", "python_lib", "local_env"],
            description="A Python library or command line tool",
        ),
        env.write_target(
            "django_app", ["app", "django_app"], description="A Django backend"
        ),
        env.enter_project_dir(),
    ):
        pass

    # We list the available targets and layers.
    #
    # The targets should be printed in alphabetical order, in columns, with
    # their description and the layers that their target file lists. Then the
    # layers should be printed in alphabetical order.
    if env.step(
        env.run_mn_prompts("list"),
    ):
        assert env.exit_code == 0
        assert env.output_lines() == [
            "Targets:",
            "  django_app  A Django backend                       (app, django_app)",
            "  python_lib  A Python library or command line tool  "
            + "(app, python_lib, local_env)",
            "Layers:",
            "  app",
            "  django_app",
            "  local_env",
            "  python_lib",
        ]


class Env(TestEnv):
    pass
