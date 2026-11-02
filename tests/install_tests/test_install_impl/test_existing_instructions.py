import shutil

from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv

from mn_prompts.instructions.actions.install_instructions import (
    InstructionsExistError,
)

NOTES_TEXT = "Our own notes.\n"


def create_env(context: Context):
    return Env(context)


def test_existing_instructions(context: Context):
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

    # Our project has an instructions dir of its own, and we install the
    # python_lib target.
    #
    # The dir has no manifest, so it should raise an InstructionsExistError,
    # leave the instructions dir unchanged, and not create CLAUDE.md.
    if env.step(
        env.create_instructions_dir(),
        env.run_mn_prompts_and_catch_error("install", "--target=python_lib"),
    ):
        assert isinstance(env.error, InstructionsExistError)
        assert env.instructions_entries() == ["notes.md"]
        assert not env.project_path_exists("CLAUDE.md")

    # The instructions in our project are a file, and we install the python_lib
    # target.
    #
    # It should raise an InstructionsExistError, and leave the file unchanged.
    if env.step(
        env.remove_instructions(),
        env.write_project_file("instructions", NOTES_TEXT),
        env.run_mn_prompts_and_catch_error("install", "--target=python_lib"),
    ):
        assert isinstance(env.error, InstructionsExistError)
        assert env.read_project_file("instructions") == NOTES_TEXT

    # The instructions in our project are a symlink to a dir outside the
    # prompts-dir, and we install the python_lib target.
    #
    # It should raise an InstructionsExistError, and leave the symlink
    # unchanged.
    if env.step(
        env.remove_instructions(),
        env.create_docs_dir(),
        env.create_instructions_symlink(env.docs_dir),
        env.run_mn_prompts_and_catch_error("install", "--target=python_lib"),
    ):
        assert isinstance(env.error, InstructionsExistError)
        assert env.link("instructions") == env.docs_dir

    # The instructions in our project are the symlink to the python_lib target
    # dir that an old version of mn-prompts created, and we install the
    # python_lib target.
    #
    # There is no migration, so it should raise an InstructionsExistError, and
    # leave the symlink unchanged.
    if env.step(
        env.remove_instructions(),
        env.create_instructions_symlink(env.old_target_dir()),
        env.run_mn_prompts_and_catch_error("install", "--target=python_lib"),
    ):
        assert isinstance(env.error, InstructionsExistError)
        assert env.link("instructions") == env.old_target_dir()

    # We have installed the python_lib target, but then replaced the
    # python_lib_layer symlink with a dir of our own. We install again.
    #
    # It should raise an InstructionsExistError, and leave the dir unchanged.
    if env.step(
        env.remove_instructions(),
        env.run_mn_prompts("install", "--target=python_lib"),
        env.replace_symlink_with_dir("instructions/python_lib_layer"),
        env.run_mn_prompts_and_catch_error("install", "--target=python_lib"),
    ):
        assert isinstance(env.error, InstructionsExistError)
        assert "python_lib_layer" in str(env.error)
        assert env.read_project_file("instructions/python_lib_layer/notes.md") == (
            NOTES_TEXT
        )


class Env(TestEnv):
    def __post_init__(self):
        self.docs_dir = None

    def create_instructions_dir(self):
        (self.project_dir / "instructions").mkdir()
        (self.project_dir / "instructions" / "notes.md").write_text(NOTES_TEXT)

    def create_docs_dir(self):
        self.docs_dir = self.context.tmp_path / "docs"
        self.docs_dir.mkdir()

    def remove_instructions(self):
        path = self.project_dir / "instructions"
        if path.is_symlink() or path.is_file():
            path.unlink()
        else:
            shutil.rmtree(path)

    def replace_symlink_with_dir(self, name: str):
        path = self.project_dir / name
        path.unlink()
        path.mkdir()
        (path / "notes.md").write_text(NOTES_TEXT)

    # Queries

    def old_target_dir(self):
        return self.prompts_dir / "targets" / "python_lib"
