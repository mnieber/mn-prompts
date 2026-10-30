import http.server
import threading
import typing as T

from e2e_test_env import (
    COMPOSE_YML,
    DOCKERFILE_LOCAL_YML,
    INIT_STACK_YML,
    OVERRIDE_YML,
    SRC_OVERLAYS_YML,
    Context,
    TestEnv,
    requires_jaz,
)

INIT_COMMAND = [
    "up",
    "--detach",
    "--force-recreate",
    "--wait",
    "--wait-timeout",
    "600",
]
OPEN_PROMPT = "in the browser? [Y/n]"


def create_env(context: Context):
    return Env(context)


@requires_jaz()
def test_developer_initialises_the_stack(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have the blogs project, and docker is faked. The homepage of the stack is
    # served on a local port.
    if env.step(
        env.install_fake_tools(),
        env.export_secrets(),
        env.serve_homepage(),
    ):
        assert not env.project_file(OVERRIDE_YML).exists()

    # We initialise the stack, without a terminal.
    #
    # It should create the override file, and start the stack in init mode: with
    # the files of up, and the init-stack file last. It should wait until the stack
    # is healthy, and recreate the containers, so that init-dev runs again. Then it
    # should get the homepage from the host, and print it without asking to open it.
    if env.step(
        env.run_jaz("compose.init"),
    ):
        assert env.exit_code == 0
        assert env.project_file(OVERRIDE_YML).exists()
        assert len(env.calls("docker")) == 1
        assert env.compose_files(env.last_call()) == [
            COMPOSE_YML,
            SRC_OVERLAYS_YML,
            OVERRIDE_YML,
            INIT_STACK_YML,
        ]
        assert env.compose_command(env.last_call()) == INIT_COMMAND
        assert env.last_call()["env"]["COMPOSE_PROJECT_NAME"] == "blogs"
        assert env.homepage_requests == ["/"]
        assert env.homepage in env.output
        assert OPEN_PROMPT not in env.output
        assert env.calls("browser") == []

    # We initialise the stack in a terminal, and answer yes to open the homepage.
    #
    # It should open the homepage in the browser.
    if env.step(
        env.forget_calls(),
        env.run_jaz_and_answer(OPEN_PROMPT, "y", "compose.init"),
    ):
        assert env.exit_code == 0
        assert env.prompted
        assert [x["args"] for x in env.calls("browser")] == [[env.homepage]]

    # We initialise the stack in a terminal, and answer no.
    #
    # It should not open the browser.
    if env.step(
        env.forget_calls(),
        env.run_jaz_and_answer(OPEN_PROMPT, "n", "compose.init"),
    ):
        assert env.exit_code == 0
        assert env.prompted
        assert env.calls("browser") == []

    # We initialise the stack with the Dockerfile.local images.
    #
    # It should add the dockerfile-local file, and keep the init-stack file last.
    if env.step(
        env.forget_calls(),
        env.run_jaz("compose.init", "local=true"),
    ):
        assert env.exit_code == 0
        assert env.compose_files(env.last_call()) == [
            COMPOSE_YML,
            SRC_OVERLAYS_YML,
            DOCKERFILE_LOCAL_YML,
            OVERRIDE_YML,
            INIT_STACK_YML,
        ]


class Env(TestEnv):
    def __post_init__(self):
        self.homepage: T.Optional[str] = None
        self.homepage_requests: T.List[str] = []

    def serve_homepage(self):
        """Serves a homepage on a free local port, records the paths of its requests
        in env.homepage_requests, and makes it the /compose/init/homepage of the
        project."""
        requests = self.homepage_requests

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<html>blogs</html>")

            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.context.request.addfinalizer(server.shutdown)
        self.homepage = f"http://127.0.0.1:{server.server_address[1]}/"
        self.write_local_config(f"compose:\n  init:\n    homepage: {self.homepage}\n")

    # Queries

    def last_call(self) -> dict:
        return self.calls("docker")[-1]
