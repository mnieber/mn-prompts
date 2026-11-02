from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv


def create_env(context: Context):
    return Env(context)


def test_git_ignore_agents_file(context: Context):
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

    # We install the prompts with --agents-md, and ask to ignore the installed
    # files.
    #
    # It should ignore AGENTS.md instead of CLAUDE.md.
    if env.step(
        env.run_mn_prompts(
            "install", "--target=python_lib", "--agents-md", "--git-ignore"
        ),
    ):
        assert env.read_project_file(".gitignore") == "/AGENTS.md\n/instructions/\n"

    # We remove .gitignore, and re-install without a target or layers.
    #
    # It should use the agents file of the manifest, so it should ignore
    # AGENTS.md again.
    if env.step(
        env.remove_project_file(".gitignore"),
        env.run_mn_prompts("install", "--git-ignore"),
    ):
        assert env.read_project_file(".gitignore") == "/AGENTS.md\n/instructions/\n"


class Env(TestEnv):
    def remove_project_file(self, name: str):
        (self.project_dir / name).unlink()
