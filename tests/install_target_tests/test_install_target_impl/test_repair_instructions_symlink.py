from install_target_tests.install_target_test_env import Context, TestEnv


def create_env(context: Context):
    return Env(context)


def test_repair_instructions_symlink(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have installed the prompts of the python_lib target in our project.
    if env.step(
        env.install_editable(target_names=["python_lib"]),
        env.enter_project_dir(),
        env.run_mn_prompts("install", "python_lib"),
    ):
        pass

    # After a git pull in the clone, the python_lib target is renamed to
    # python_package.
    #
    # The instructions symlink should be dangling.
    if env.step(
        env.rename_target("python_lib", "python_package"),
    ):
        assert env.project_path_exists("instructions")
        assert not env.instructions_link().exists()

    # We install the prompts of the python_package target.
    #
    # The dangling symlink points into the targets dir of the prompts-dir, so it
    # should be replaced by a symlink to the python_package target.
    if env.step(
        env.run_mn_prompts("install", "python_package"),
    ):
        assert env.exit_code == 0
        assert env.instructions_link() == env.prompts_dir / "targets" / "python_package"
        assert (
            env.read_project_file("instructions/index.md")
            == "# Instructions for python_lib\n"
        )


class Env(TestEnv):
    def rename_target(self, target_name: str, new_target_name: str):
        targets_dir = self.prompts_dir / "targets"
        (targets_dir / target_name).rename(targets_dir / new_target_name)
