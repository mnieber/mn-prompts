from install_target_tests.install_target_test_env import Context, TestEnv
from mn_prompts_test_env import AGENTS_FILE_TEXT


def create_env(context: Context):
    return Env(context)


def test_a_user_switches_to_another_target(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have installed the prompts of the python_lib target in our project.
    if env.step(
        env.install_editable(target_names=["python_lib", "django_app"]),
        env.enter_project_dir(),
        env.run_mn_prompts("install", "python_lib"),
    ):
        assert env.instructions_link() == env.prompts_dir / "targets" / "python_lib"

    # We install the prompts of the django_app target.
    #
    # It should replace the instructions symlink by one to the django_app
    # target. AGENTS.md exists already, so it should be left unchanged, and we
    # should be told to extend it with the contents of the agents file.
    if env.step(
        env.run_mn_prompts("install", "django_app"),
    ):
        assert env.exit_code == 0
        assert env.instructions_link() == env.prompts_dir / "targets" / "django_app"
        assert env.read_project_file("AGENTS.md") == AGENTS_FILE_TEXT
        assert "AGENTS.md" in env.error_output
        assert str(env.agents_file_source()) in env.error_output


class Env(TestEnv):
    pass
