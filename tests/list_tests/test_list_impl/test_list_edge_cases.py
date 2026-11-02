import shutil

from list_tests.list_test_env import Context, TestEnv


def create_env(context: Context):
    return Env(context)


def test_list_edge_cases(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib and
    # the layer app. The targets dir and the layers dir also contain a hidden
    # dir and a file that are not targets or layers.
    if env.step(
        env.install_editable(targets={"python_lib": ["app"]}, layers={"app": []}),
        env.create_hidden_dir(env.prompts_dir / "targets" / ".claude"),
        env.create_hidden_dir(env.prompts_dir / "layers" / ".claude"),
        env.create_file(env.prompts_dir / "targets" / "README.md"),
        env.create_file(env.prompts_dir / "layers" / "README.md"),
        env.enter_project_dir(),
    ):
        pass

    # We list the available targets and layers.
    #
    # Only the python_lib target and the app layer should be printed.
    if env.step(
        env.run_mn_prompts("list"),
    ):
        assert env.exit_code == 0
        assert env.output_lines() == [
            "Targets:",
            "  python_lib  The python_lib target  (app)",
            "Layers:",
            "  app",
        ]

    # The target file of python_lib has no description.
    #
    # The description should be empty.
    if env.step(
        env.write_target_without_description("python_lib", ["app"]),
        env.run_mn_prompts("list"),
    ):
        assert env.output_lines()[1] == "  python_lib    (app)"

    # We remove the python_lib target and the app layer, and list again.
    #
    # Only the headers should be printed, and this is not an error.
    if env.step(
        env.remove_target("python_lib"),
        env.remove_layer("app"),
        env.run_mn_prompts("list"),
    ):
        assert env.exit_code == 0
        assert env.output_lines() == ["Targets:", "Layers:"]


class Env(TestEnv):
    def create_hidden_dir(self, path):
        path.mkdir()

    def create_file(self, path):
        path.write_text("Not a target or layer.\n")

    def write_target_without_description(self, target_name, layer_names):
        (self.prompts_dir / "targets" / f"{target_name}.yaml").write_text(
            f"layers: [{', '.join(layer_names)}]\n"
        )

    def remove_target(self, target_name: str):
        (self.prompts_dir / "targets" / f"{target_name}.yaml").unlink()

    def remove_layer(self, layer_name: str):
        shutil.rmtree(self.prompts_dir / "layers" / layer_name)
