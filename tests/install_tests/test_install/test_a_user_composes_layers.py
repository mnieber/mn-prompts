from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv
from mn_prompts_test_env import AGENTS_FILE_TEXT


def create_env(context: Context):
    return Env(context)


def test_a_user_composes_layers(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib.
    if env.step(
        env.install_editable(
            targets={"python_lib": ["app", "python_lib"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
    ):
        pass

    # Our Python library has a React frontend, so we install the python_lib
    # target plus the react_app layer.
    #
    # The instructions should have the layers of the target and the react_app
    # layer, and the manifest should record both.
    if env.step(
        env.run_mn_prompts("install", "--target=python_lib", "--layer=react_app"),
    ):
        assert env.exit_code == 0
        assert env.index_layer_order() == ["app", "python_lib", "react_app"]
        assert env.link("instructions/react_app_layer") == env.layer_dir("react_app")
        assert env.read_manifest() == {
            "target": "python_lib",
            "layers": ["react_app"],
            "agents_file": "CLAUDE.md",
        }

    # We drop the Python part, and install only the app and react_app layers.
    #
    # The new selection should replace the previous one: the python_lib symlink
    # should be removed, and the manifest should have no target. CLAUDE.md
    # exists already, so it should be left unchanged, and we should be told to
    # extend it with the contents of the agents file.
    if env.step(
        env.run_mn_prompts("install", "--layer=app", "--layer=react_app"),
    ):
        assert env.exit_code == 0
        assert env.index_layer_order() == ["app", "react_app"]
        assert env.instructions_entries() == [
            "app_layer",
            "examples",
            "index.md",
            "mn-prompts.yaml",
            "react_app_layer",
        ]
        assert env.read_manifest() == {
            "target": None,
            "layers": ["app", "react_app"],
            "agents_file": "CLAUDE.md",
        }
        assert env.read_project_file("CLAUDE.md") == AGENTS_FILE_TEXT
        assert "CLAUDE.md" in env.error_output
        assert str(env.agents_file_source()) in env.error_output


class Env(TestEnv):
    pass
