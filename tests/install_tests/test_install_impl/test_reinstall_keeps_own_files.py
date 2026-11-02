from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv

PROJECT_TEXT = "# Our project\n"
NOTES_TEXT = "Our own notes.\n"


def create_env(context: Context):
    return Env(context)


def test_reinstall_keeps_own_files(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have installed the python_lib target plus the react_app layer in our
    # project, and added a project.md and a notes dir to the instructions dir.
    if env.step(
        env.install_editable(
            targets={"python_lib": ["app", "python_lib"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
        env.run_mn_prompts("install", "--target=python_lib", "--layer=react_app"),
        env.write_project_file("instructions/project.md", PROJECT_TEXT),
        env.create_notes_dir(),
    ):
        pass

    # We move our clone of mn-prompts, and pip install it again.
    #
    # The symlinks in the instructions dir should be dangling.
    if env.step(
        env.move_clone("mn-prompts-moved"),
    ):
        assert not env.link("instructions/app_layer").exists()
        assert not env.link("instructions/react_app_layer").exists()

    # We install the python_lib target, without the react_app layer.
    #
    # The symlinks of the selected layers and the examples should point into the
    # moved clone. The react_app symlink belongs to mn-prompts (although it
    # points into the old clone), so it should be removed. Our own files should
    # be left unchanged.
    if env.step(
        env.run_mn_prompts("install", "--target=python_lib"),
    ):
        assert env.exit_code == 0
        assert env.instructions_entries() == [
            "app_layer",
            "examples",
            "index.md",
            "mn-prompts.yaml",
            "notes",
            "project.md",
            "python_lib_layer",
        ]
        assert env.link("instructions/app_layer") == env.layer_dir("app")
        assert env.link("instructions/python_lib_layer") == env.layer_dir("python_lib")
        assert env.link("instructions/examples") == env.prompts_dir / "examples"
        assert env.read_project_file("instructions/project.md") == PROJECT_TEXT
        assert env.read_project_file("instructions/notes/todo.md") == NOTES_TEXT


class Env(TestEnv):
    def create_notes_dir(self):
        notes_dir = self.project_dir / "instructions" / "notes"
        notes_dir.mkdir()
        (notes_dir / "todo.md").write_text(NOTES_TEXT)

    def move_clone(self, dir_name: str):
        new_clone_dir = self.clone_dir.parent / dir_name
        self.clone_dir.rename(new_clone_dir)
        self.clone_dir = new_clone_dir
        self.prompts_dir = new_clone_dir / "extra" / "prompts"
        self._locate_package(new_clone_dir / "src" / "mn_prompts")
