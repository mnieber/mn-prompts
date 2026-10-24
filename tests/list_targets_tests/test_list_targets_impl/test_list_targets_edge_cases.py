import shutil

from list_targets_tests.list_targets_test_env import Context, TestEnv


def create_env(context: Context):
    return Env(context)


def test_list_targets_edge_cases(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib. The
    # targets dir also contains a hidden dir and a file.
    if env.step(
        env.install_editable(target_names=["python_lib"]),
        env.create_hidden_dir_in_targets_dir(".claude"),
        env.create_file_in_targets_dir("README.md"),
        env.enter_project_dir(),
    ):
        pass

    # We list the available targets.
    #
    # Only python_lib should be printed.
    if env.step(
        env.run_mn_prompts("list"),
    ):
        assert env.exit_code == 0
        assert env.output_lines() == ["python_lib"]

    # We remove the python_lib target, and list the targets again.
    #
    # Nothing should be printed, and this is not an error.
    if env.step(
        env.remove_target("python_lib"),
        env.run_mn_prompts("list"),
    ):
        assert env.exit_code == 0
        assert env.output == ""


class Env(TestEnv):
    def create_hidden_dir_in_targets_dir(self, name: str):
        (self.prompts_dir / "targets" / name).mkdir()

    def create_file_in_targets_dir(self, name: str):
        (self.prompts_dir / "targets" / name).write_text("The available targets.\n")

    def remove_target(self, target_name: str):
        shutil.rmtree(self.prompts_dir / "targets" / target_name)
