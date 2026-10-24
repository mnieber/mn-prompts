import shutil

from install_target_tests.install_target_test_env import Context, TestEnv

from mn_prompts.targets.actions.install_target import (
    InstructionsExistError,
    UnknownTargetError,
)

NOTES_TEXT = "Our own notes.\n"


def create_env(context: Context):
    return Env(context)


def test_install_target_errors(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the targets python_lib and
    # django_app, and an empty project dir.
    if env.step(
        env.install_editable(target_names=["python_lib", "django_app"]),
        env.enter_project_dir(),
    ):
        pass

    # We install a target that does not exist.
    #
    # It should raise an UnknownTargetError that lists the available targets
    # in alphabetical order, and create no files.
    if env.step(
        env.run_mn_prompts_and_catch_error("install", "react_app"),
    ):
        assert isinstance(env.error, UnknownTargetError)
        assert env.error_lines()[-2:] == ["django_app", "python_lib"]
        assert not env.project_path_exists("instructions")
        assert not env.project_path_exists("AGENTS.md")

    # Our project has an instructions dir of its own, and we install the
    # python_lib target.
    #
    # It should raise an InstructionsExistError, leave the instructions dir
    # unchanged, and not create AGENTS.md.
    if env.step(
        env.create_instructions_dir(),
        env.run_mn_prompts_and_catch_error("install", "python_lib"),
    ):
        assert isinstance(env.error, InstructionsExistError)
        assert env.read_project_file("instructions/notes.md") == NOTES_TEXT
        assert not env.project_path_exists("AGENTS.md")

    # The instructions in our project are a symlink to a dir outside the
    # prompts-dir, and we install the python_lib target.
    #
    # It should raise an InstructionsExistError, and leave the symlink
    # unchanged.
    if env.step(
        env.remove_instructions(),
        env.create_docs_dir(),
        env.create_instructions_symlink(env.docs_dir),
        env.run_mn_prompts_and_catch_error("install", "python_lib"),
    ):
        assert isinstance(env.error, InstructionsExistError)
        assert env.instructions_link() == env.docs_dir
        assert not env.project_path_exists("AGENTS.md")

    # The instructions in our project are a symlink into the targets dir of
    # another clone of mn-prompts (that was moved), and we install the
    # python_lib target.
    #
    # Only symlinks into our own prompts-dir are replaced, so it should raise an
    # InstructionsExistError, and leave the symlink unchanged.
    if env.step(
        env.remove_instructions(),
        env.create_instructions_symlink(env.moved_clone_target_dir()),
        env.run_mn_prompts_and_catch_error("install", "python_lib"),
    ):
        assert isinstance(env.error, InstructionsExistError)
        assert env.instructions_link() == env.moved_clone_target_dir()
        assert not env.project_path_exists("AGENTS.md")


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
        if path.is_symlink():
            path.unlink()
        else:
            shutil.rmtree(path)

    # Queries

    def error_lines(self):
        return [line.strip() for line in str(self.error).splitlines()]

    def moved_clone_target_dir(self):
        return (
            self.context.tmp_path
            / "old-mn-prompts"
            / "extra"
            / "prompts"
            / "targets"
            / "python_lib"
        )
