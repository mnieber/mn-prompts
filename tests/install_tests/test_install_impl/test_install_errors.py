from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv

from mn_prompts.instructions.actions.install_instructions import MissingSelectionError
from mn_prompts.layers.rules.get_layer import (
    MissingIndexSnippetError,
    UnknownLayerError,
)
from mn_prompts.layers.rules.get_selected_layers import LayerDependencyCycleError
from mn_prompts.targets.rules.get_target import UnknownTargetError


def create_env(context: Context):
    return Env(context)


def test_install_errors(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the targets python_lib and
    # django_app, and an empty project dir.
    if env.step(
        env.install_editable(
            targets={
                "python_lib": ["app", "python_lib"],
                "django_app": ["app", "django_app"],
            },
            layers=DJANGO_LAYERS,
        ),
        env.enter_project_dir(),
    ):
        pass

    # We install a target that does not exist.
    #
    # It should raise an UnknownTargetError that lists the available targets
    # in alphabetical order, and create no files.
    if env.step(
        env.run_mn_prompts_and_catch_error("install", "--target=react_app"),
    ):
        assert isinstance(env.error, UnknownTargetError)
        assert env.error_lines()[-2:] == ["django_app", "python_lib"]
        assert not env.project_path_exists("instructions")
        assert not env.project_path_exists("CLAUDE.md")

    # We install a layer that does not exist.
    #
    # It should raise an UnknownLayerError that lists the available layers in
    # alphabetical order, and create no files.
    if env.step(
        env.run_mn_prompts_and_catch_error(
            "install", "--target=python_lib", "--layer=vue_app"
        ),
    ):
        assert isinstance(env.error, UnknownLayerError)
        assert "vue_app" in env.error_lines()[0]
        assert env.error_lines()[-5:] == [
            "app",
            "django_app",
            "local_env",
            "python_lib",
            "react_app",
        ]
        assert not env.project_path_exists("instructions")

    # The react_app layer requires a layer that does not exist, and we install
    # it.
    #
    # It should raise an UnknownLayerError that says which layer requires it.
    if env.step(
        env.write_layer("react_app", ["app", "typescript"]),
        env.run_mn_prompts_and_catch_error("install", "--layer=react_app"),
    ):
        assert isinstance(env.error, UnknownLayerError)
        assert "typescript" in env.error_lines()[0]
        assert "react_app" in env.error_lines()[0]
        assert not env.project_path_exists("instructions")

    # The local_env layer has no index-snippet, and we install it.
    #
    # It should raise a MissingIndexSnippetError, and create no files.
    if env.step(
        env.remove_index_snippet("local_env"),
        env.run_mn_prompts_and_catch_error("install", "--layer=local_env"),
    ):
        assert isinstance(env.error, MissingIndexSnippetError)
        assert "local_env" in str(env.error)
        assert not env.project_path_exists("instructions")

    # The app layer requires the django_app layer, which requires the app
    # layer, and we install the django_app target.
    #
    # It should raise a LayerDependencyCycleError, and create no files.
    if env.step(
        env.write_layer("app", ["django_app"]),
        env.run_mn_prompts_and_catch_error("install", "--target=django_app"),
    ):
        assert isinstance(env.error, LayerDependencyCycleError)
        assert not env.project_path_exists("instructions")

    # We install without a target or layers, but there is no earlier install.
    #
    # It should raise a MissingSelectionError, and create no files.
    if env.step(
        env.run_mn_prompts_and_catch_error("install"),
    ):
        assert isinstance(env.error, MissingSelectionError)
        assert "--target" in str(env.error)
        assert "--layer" in str(env.error)
        assert not env.project_path_exists("instructions")
        assert not env.project_path_exists("CLAUDE.md")


class Env(TestEnv):
    def remove_index_snippet(self, layer_name: str):
        (self.prompts_dir / "layers" / layer_name / "index-snippet.md").unlink()

    # Queries

    def error_lines(self):
        return [line.strip() for line in str(self.error).splitlines()]
