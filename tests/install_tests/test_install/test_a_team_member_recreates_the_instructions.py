from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv

PROJECT_TEXT = "# Our project\n\nThe backend lives in src/backend.\n"
COMMITTED_FILE_NAMES = ["mn-prompts.yaml", "project.md"]


def create_env(context: Context):
    return Env(context)


def test_a_team_member_recreates_the_instructions(context: Context):
    # Create the test environment
    env = create_env(context)

    # A colleague installed the django_app target in our project, added a
    # project.md with notes about the project, and committed only the manifest
    # and project.md of the instructions dir.
    if env.step(
        env.install_editable(
            targets={"django_app": ["app", "django_app"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
        env.run_mn_prompts("install", "--target=django_app"),
        env.write_project_file("instructions/project.md", PROJECT_TEXT),
    ):
        pass

    # We clone the project.
    #
    # The instructions dir should only contain the committed files.
    if env.step(
        env.clone_project(),
    ):
        assert env.instructions_entries() == COMMITTED_FILE_NAMES

    # We install again, without a target or layers.
    #
    # It should re-create the instructions dir from the manifest, and leave
    # project.md unchanged.
    if env.step(
        env.run_mn_prompts("install"),
    ):
        assert env.exit_code == 0
        assert env.instructions_entries() == [
            "app_layer",
            "django_app_layer",
            "examples",
            "index.md",
            "mn-prompts.yaml",
            "project.md",
            "python_lib_layer",
        ]
        assert env.index_layer_order() == ["app", "python_lib", "django_app"]
        assert env.read_project_file("instructions/project.md") == PROJECT_TEXT


class Env(TestEnv):
    def clone_project(self):
        """Removes the files of the instructions dir that were not committed."""
        for path in (self.project_dir / "instructions").iterdir():
            if path.name not in COMMITTED_FILE_NAMES:
                path.unlink()
