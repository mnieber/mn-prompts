from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv


def create_env(context: Context):
    return Env(context)


def test_git_ignore_entries(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib, and
    # a project with a .gitignore that doesn't end with a newline.
    if env.step(
        env.install_editable(
            targets={"python_lib": ["app", "python_lib"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
        env.write_project_file(".gitignore", "__pycache__/\n*.egg-info"),
    ):
        pass

    # We install the prompts of the python_lib target, and ask to ignore the
    # installed files.
    #
    # The existing lines should be kept, and the entries should be appended on
    # new lines.
    if env.step(
        env.run_mn_prompts("install", "--target=python_lib", "--git-ignore"),
    ):
        assert env.read_project_file(".gitignore") == (
            "__pycache__/\n*.egg-info\n/CLAUDE.md\n/instructions/\n"
        )

    # Our .gitignore already ignores the installed files, but in another form.
    # We re-install and ask again to ignore the installed files.
    #
    # It should recognise the entries, and leave .gitignore unchanged.
    for git_ignore_text in [
        "CLAUDE.md\ninstructions\n",
        "  /CLAUDE.md  \n/instructions\n",
        "CLAUDE.md\ninstructions/\n",
    ]:
        if env.step(
            env.write_project_file(".gitignore", git_ignore_text),
            env.run_mn_prompts("install", "--git-ignore"),
        ):
            assert env.read_project_file(".gitignore") == git_ignore_text

    # Our .gitignore only ignores the instructions dir. We re-install and ask
    # again to ignore the installed files.
    #
    # It should only add the agents file.
    if env.step(
        env.write_project_file(".gitignore", "instructions/\n"),
        env.run_mn_prompts("install", "--git-ignore"),
    ):
        assert env.read_project_file(".gitignore") == "instructions/\n/CLAUDE.md\n"


class Env(TestEnv):
    pass
