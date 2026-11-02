from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv

OUR_AGENTS_FILE_TEXT = "# Agents\n\nAlways run the tests before you commit.\n"


def create_env(context: Context):
    return Env(context)


def test_git_ignore_existing_agents_file(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib, and
    # a project that already has its own CLAUDE.md.
    if env.step(
        env.install_editable(
            targets={"python_lib": ["app", "python_lib"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
        env.write_agents_file(OUR_AGENTS_FILE_TEXT),
    ):
        pass

    # We install the prompts, and ask to ignore the installed files.
    #
    # Our CLAUDE.md should be left unchanged, but it should still be ignored.
    if env.step(
        env.run_mn_prompts("install", "--target=python_lib", "--git-ignore"),
    ):
        assert env.read_project_file("CLAUDE.md") == OUR_AGENTS_FILE_TEXT
        assert env.read_project_file(".gitignore") == "/CLAUDE.md\n/instructions/\n"


class Env(TestEnv):
    pass
