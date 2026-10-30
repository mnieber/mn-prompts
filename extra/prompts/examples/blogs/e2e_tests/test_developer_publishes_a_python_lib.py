from pathlib import Path

from e2e_test_env import PASSWORD_PROMPT, Context, TestEnv, requires_jaz

LIB_DIR = "src/libs/python_toolkit"
TOKEN = "pypi-test-token-0123456789"
PYPI_URL = "https://upload.pypi.org/legacy/"
TEST_PYPI_URL = "https://test.pypi.org/legacy/"

TEST_PYPI_CONFIG = f"""\
python:
  pypi:
    publish_url: {TEST_PYPI_URL}
"""


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_developer_publishes_a_python_lib(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have the library python_toolkit 0.2.0 in src/libs.
    if env.step(
        env.install_fake_tools(),
        env.write_lib(LIB_DIR, "python_toolkit", "0.2.0"),
    ):
        pass

    # The developer publishes the library, and types their token as the password.
    #
    # It should build the library outside its own dir, show the built files and
    # where they go before it asks for the password, and then upload exactly these
    # files to PyPI as __token__.
    if env.step(
        env.run_jaz_and_type_password(
            TOKEN, "python.publish", f"package-dir={LIB_DIR}"
        ),
    ):
        assert env.exit_code == 0
        assert env.password_prompted
        assert env.uv_commands() == ["build", "publish"]

        assert env.relative_path(env.built_package_dir()) == LIB_DIR
        assert not env.out_dir().is_relative_to(env.project_file(LIB_DIR))

        assert env.shown_before_prompt("python_toolkit-0.2.0.tar.gz")
        assert env.shown_before_prompt("python_toolkit-0.2.0-py3-none-any.whl")
        assert env.shown_before_prompt(PYPI_URL)
        assert env.shown_before_prompt("__token__")

        assert env.option(env.uv_call("publish"), "--publish-url") == PYPI_URL
        assert env.option(env.uv_call("publish"), "--username") == "__token__"
        assert env.uploaded_files() == [
            "python_toolkit-0.2.0-py3-none-any.whl",
            "python_toolkit-0.2.0.tar.gz",
        ]

        # The token reaches uv through its environment, where other users can't
        # see it, and is not echoed
        assert env.uv_call("publish")["env"]["UV_PUBLISH_PASSWORD"] == TOKEN
        assert all(TOKEN not in " ".join(x["args"]) for x in env.calls())
        assert TOKEN not in env.output

        # The temp dir of the build is removed
        assert not env.out_dir().exists()

    # The developer bumps the version to 0.2.1, sets the publish url to TestPyPI in
    # their local.yaml, and publishes again.
    #
    # It should upload the 0.2.1 files to TestPyPI, still as the user __token__ of
    # base.yaml.
    if env.step(
        env.forget_calls(),
        env.write_lib(LIB_DIR, "python_toolkit", "0.2.1"),
        env.write_local_config(TEST_PYPI_CONFIG),
        env.run_jaz_and_type_password(
            TOKEN, "python.publish", f"package-dir={LIB_DIR}"
        ),
    ):
        assert env.exit_code == 0
        assert env.option(env.uv_call("publish"), "--publish-url") == TEST_PYPI_URL
        assert env.option(env.uv_call("publish"), "--username") == "__token__"
        assert env.uploaded_files() == [
            "python_toolkit-0.2.1-py3-none-any.whl",
            "python_toolkit-0.2.1.tar.gz",
        ]


class Env(TestEnv):
    # Queries

    def uv_commands(self) -> list:
        return [x["args"][0] for x in self.calls("uv")]

    def built_package_dir(self) -> str:
        return self.positional_args(self.uv_call("build"))[-1]

    def out_dir(self) -> Path:
        return Path(self.option(self.uv_call("build"), "--out-dir"))

    def uploaded_files(self) -> list:
        return sorted(
            Path(x).name for x in self.positional_args(self.uv_call("publish"))
        )

    def shown_before_prompt(self, text: str) -> bool:
        prompt_idx = self.output.find(PASSWORD_PROMPT)
        return 0 <= self.output.find(text) < prompt_idx
