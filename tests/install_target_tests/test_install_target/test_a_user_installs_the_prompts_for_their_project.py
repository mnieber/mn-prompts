from install_target_tests.install_target_test_env import Context, TestEnv
from mn_prompts_test_env import AGENTS_FILE_TEXT


def create_env(context: Context):
    return Env(context)


def test_a_user_installs_the_prompts_for_their_project(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the targets python_lib and
    # django_app, and an empty project dir.
    if env.step(
        env.install_editable(target_names=["python_lib", "django_app"]),
        env.enter_project_dir(),
    ):
        pass

    # We install the prompts of the python_lib target.
    #
    # It should create an instructions symlink to the python_lib target, and
    # copy the agents file to AGENTS.md.
    if env.step(
        env.run_mn_prompts("install", "python_lib"),
    ):
        assert env.exit_code == 0
        assert env.instructions_link() == env.prompts_dir / "targets" / "python_lib"
        assert env.instructions_link().is_absolute()
        assert (
            env.read_project_file("instructions/index.md")
            == "# Instructions for python_lib\n"
        )
        assert env.read_project_file("AGENTS.md") == AGENTS_FILE_TEXT


class Env(TestEnv):
    pass
