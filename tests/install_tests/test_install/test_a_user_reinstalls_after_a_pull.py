from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv

NEW_SNIPPET_TEXT = "Consult ./python_lib_layer/index.md for any Python code.\n"


def create_env(context: Context):
    return Env(context)


def test_a_user_reinstalls_after_a_pull(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have installed the prompts of the python_lib target in our project.
    if env.step(
        env.install_editable(
            targets={"python_lib": ["app", "python_lib"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
        env.run_mn_prompts("install", "--target=python_lib"),
    ):
        assert env.index_layer_order() == ["app", "python_lib"]

    # After a git pull in the clone, the python_lib target also uses the
    # local_env layer, and the snippet of the python_lib layer has changed.
    #
    # The installed index is a copy, so it should not have changed yet.
    if env.step(
        env.write_target("python_lib", ["app", "python_lib", "local_env"]),
        env.write_layer("python_lib", ["app"], snippet_text=NEW_SNIPPET_TEXT),
    ):
        assert env.index_layer_order() == ["app", "python_lib"]
        assert "any Python code" not in env.read_project_file("instructions/index.md")

    # We install again, without a target or layers.
    #
    # It should re-install the selection of the manifest: the index should
    # have the new snippet and the local_env layer, the local_env symlink should
    # be added, and the manifest should be unchanged.
    if env.step(
        env.run_mn_prompts("install"),
    ):
        assert env.exit_code == 0
        assert env.index_layer_order() == ["app", "local_env", "python_lib"]
        assert "any Python code" in env.read_project_file("instructions/index.md")
        assert env.link("instructions/local_env_layer") == env.layer_dir("local_env")
        assert env.read_manifest() == {
            "target": "python_lib",
            "layers": [],
            "agents_file": "CLAUDE.md",
        }


class Env(TestEnv):
    pass
