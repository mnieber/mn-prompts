from pathlib import Path

from e2e_test_env import Context, TestEnv, requires_jaz

NO_SERVICES = """\
python:
  services: []
"""

LIB_DIR = "src/libs/python_toolkit"
TOKEN = "pypi-test-token-0123456789"


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_pip_compile_without_services(context: Context):
    # Create the test environment
    env = create_env(context)

    # The developer removes all services from /python/services, and compiles the
    # requirements.
    #
    # It should succeed without calling uv.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.write_local_config(NO_SERVICES),
        env.run_jaz("python.pip-compile"),
    ):
        assert env.exit_code == 0
        assert env.calls("uv") == []


@requires_jaz()
def test_restart_stops_when_pip_compile_fails(context: Context):
    # Create the test environment
    env = create_env(context)

    # We compile the requirements, and uv fails.
    #
    # It should fail without a traceback.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.fail_tool("uv", 2),
        env.run_jaz("python.pip-compile"),
    ):
        assert env.exit_code != 0
        assert "Traceback" not in env.error_output

    # We restart the stack, and uv fails.
    #
    # It should stop after down: the images are not built, and the stack is not
    # started.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.restart"),
    ):
        assert env.exit_code != 0
        assert env.call_summary() == [("docker", "down"), ("uv", "pip compile")]


@requires_jaz()
def test_publish_without_pyproject(context: Context):
    # Create the test environment
    env = create_env(context)

    # We publish a dir that has a README.md, but no pyproject.toml.
    #
    # It should fail with a message that names the dir, before it asks for the
    # password or calls uv.
    if env.step(
        env.install_fake_tools(),
        env.write_file(f"{LIB_DIR}/README.md", "# python_toolkit\n"),
        env.run_jaz_and_type_password(
            TOKEN, "python.publish", f"package-dir={LIB_DIR}"
        ),
    ):
        assert env.exit_code != 0
        assert LIB_DIR in env.output
        assert "Traceback" not in env.output
        assert not env.password_prompted
        assert env.calls("uv") == []


@requires_jaz()
def test_publish_stops_when_the_build_fails(context: Context):
    # Create the test environment
    env = create_env(context)

    # We publish a library, and uv build fails.
    #
    # It should fail without a traceback, and without asking for the password or
    # uploading. jaz itself exits with 1, and reports the exit code of uv.
    if env.step(
        env.install_fake_tools(),
        env.write_lib(LIB_DIR, "python_toolkit", "0.2.0"),
        env.fail_tool("uv", 2),
        env.run_jaz_and_type_password(
            TOKEN, "python.publish", f"package-dir={LIB_DIR}"
        ),
    ):
        assert env.exit_code != 0
        assert "exit code 2" in env.output
        assert "Traceback" not in env.output
        assert not env.password_prompted
        assert env.uv_commands() == ["build"]


@requires_jaz()
def test_publish_aborts_on_an_empty_password(context: Context):
    # Create the test environment
    env = create_env(context)

    # We publish a library, and only press enter at the password prompt.
    #
    # It should abort without uploading, and remove the temp dir of the build.
    if env.step(
        env.install_fake_tools(),
        env.write_lib(LIB_DIR, "python_toolkit", "0.2.0"),
        env.run_jaz_and_type_password("", "python.publish", f"package-dir={LIB_DIR}"),
    ):
        assert env.exit_code != 0
        assert env.password_prompted
        assert "Traceback" not in env.output
        assert env.uv_commands() == ["build"]
        assert not env.out_dir().exists()


@requires_jaz()
def test_publish_reports_a_failing_upload(context: Context):
    # Create the test environment
    env = create_env(context)

    # We publish a library, and uv publish fails (e.g. the version already exists
    # on PyPI).
    #
    # It should fail without a traceback: uv has already printed the reason, and
    # jaz reports the exit code of uv. The temp dir of the build is removed.
    if env.step(
        env.install_fake_tools(),
        env.write_lib(LIB_DIR, "python_toolkit", "0.2.0"),
        env.fail_uv_publish(3),
        env.run_jaz_and_type_password(
            TOKEN, "python.publish", f"package-dir={LIB_DIR}"
        ),
    ):
        assert env.exit_code != 0
        assert "exit code 3" in env.output
        assert "Traceback" not in env.output
        assert env.uv_commands() == ["build", "publish"]
        assert not env.out_dir().exists()


@requires_jaz()
def test_publish_ignores_old_files_in_dist(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have a library with an old sdist in its dist dir.
    if env.step(
        env.install_fake_tools(),
        env.write_lib(LIB_DIR, "python_toolkit", "0.2.0"),
        env.write_file(f"{LIB_DIR}/dist/python_toolkit-0.1.0.tar.gz", "old sdist"),
    ):
        pass

    # We publish the library.
    #
    # It should upload only the files of the new build, from the temp dir of the
    # build, and leave the old file alone.
    if env.step(
        env.run_jaz_and_type_password(
            TOKEN, "python.publish", f"package-dir={LIB_DIR}"
        ),
    ):
        assert env.exit_code == 0
        assert env.uploaded_files() == [
            "python_toolkit-0.2.0-py3-none-any.whl",
            "python_toolkit-0.2.0.tar.gz",
        ]
        assert env.uploaded_dirs() == [env.out_dir()]
        assert env.read_file(f"{LIB_DIR}/dist/python_toolkit-0.1.0.tar.gz") == (
            "old sdist"
        )


@requires_jaz()
def test_publish_takes_an_absolute_package_dir(context: Context):
    # Create the test environment
    env = create_env(context)

    # We publish a library outside the project, by its absolute path.
    #
    # It should build the library at that path.
    if env.step(
        env.install_fake_tools(),
        env.write_lib_outside_the_project("woodstock", "1.0.0"),
        env.run_jaz_and_type_password(
            TOKEN, "python.publish", f"package-dir={env.outside_lib_dir}"
        ),
    ):
        assert env.exit_code == 0
        assert Path(env.built_package_dir()) == env.outside_lib_dir
        assert env.uploaded_files() == [
            "woodstock-1.0.0-py3-none-any.whl",
            "woodstock-1.0.0.tar.gz",
        ]


@requires_jaz()
def test_publish_requires_a_package_dir(context: Context):
    # Create the test environment
    env = create_env(context)

    # We publish without a package-dir.
    #
    # It should fail without calling uv.
    if env.step(
        env.install_fake_tools(),
        env.run_jaz("python.publish"),
    ):
        assert env.exit_code != 0
        assert env.calls("uv") == []


class Env(TestEnv):
    def __post_init__(self):
        self.outside_lib_dir = None

    def fail_uv_publish(self, exit_code: int):
        """Makes only uv publish fail, so that the build still succeeds."""
        self.context.monkeypatch.setenv("FAKE_UV_PUBLISH_EXIT_CODE", str(exit_code))

    def write_lib_outside_the_project(self, name: str, version: str):
        self.outside_lib_dir = self.context.tmp_path.resolve() / "elsewhere" / name
        self.write_lib(str(self.outside_lib_dir), name, version)

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

    def uploaded_dirs(self) -> list:
        return sorted(
            {Path(x).parent for x in self.positional_args(self.uv_call("publish"))}
        )
