from e2e_test_env import DOCKERFILE_LOCAL_YML, Context, TestEnv, requires_jaz

PIP_COMPILE_ARGS = [
    "pip",
    "compile",
    "--python-version=3.12",
    "--upgrade",
    "requirements.in",
    "requirements.editable",
    "-o",
    "requirements.txt",
]


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_developer_restarts_the_stack(context: Context):
    # Create the test environment
    env = create_env(context)

    # The developer adds a requirement to blogs_be, and compiles the requirements.
    #
    # It should run uv in the directory of blogs_be, with BLOGS_LIBS_DIR pointing to
    # the libs of the project. blogs_fe is not in /python/services, so it should
    # not be compiled.
    if env.step(
        env.install_fake_tools(),
        env.add_requirement("blogs_be", "requests"),
        env.run_jaz("python.pip-compile"),
    ):
        assert env.exit_code == 0
        assert len(env.calls("uv")) == 1
        assert env.calls("uv")[0]["args"] == PIP_COMPILE_ARGS
        assert env.relative_path(env.calls("uv")[0]["cwd"]) == "src/services/blogs_be"
        assert env.calls("uv")[0]["env"]["BLOGS_LIBS_DIR"] == str(
            env.project_file("src/libs")
        )

    # We restart the stack.
    #
    # It should stop the stack, compile the requirements, build the images and
    # start the stack, in that order.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.restart"),
    ):
        assert env.exit_code == 0
        assert env.call_summary() == [
            ("docker", "down"),
            ("uv", "pip compile"),
            ("docker", "build"),
            ("docker", "up"),
        ]

    # We restart the stack with the Dockerfile.local files, and without the docker
    # cache.
    #
    # The build should use the dockerfile-local file and --no-cache, and up should
    # also use the dockerfile-local file.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.restart", "local=true", "no-cache=true"),
    ):
        assert env.exit_code == 0
        assert DOCKERFILE_LOCAL_YML in env.compose_files(env.docker_call("build"))
        assert env.compose_command(env.docker_call("build")) == ["build", "--no-cache"]
        assert DOCKERFILE_LOCAL_YML in env.compose_files(env.docker_call("up"))


class Env(TestEnv):
    def add_requirement(self, service: str, requirement: str):
        path = f"src/services/{service}/requirements.in"
        self.write_file(path, self.read_file(path).rstrip("\n") + f"\n{requirement}\n")

    # Queries

    def docker_call(self, command: str) -> dict:
        (call,) = [
            x for x in self.calls("docker") if self.compose_command(x)[0] == command
        ]
        return call
