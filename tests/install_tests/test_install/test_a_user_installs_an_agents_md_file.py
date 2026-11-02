from install_tests.install_test_env import DJANGO_LAYERS, Context, TestEnv
from mn_prompts_test_env import AGENTS_FILE_TEXT


def create_env(context: Context):
    return Env(context)


def test_a_user_installs_an_agents_md_file(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib, and
    # an empty project dir. Our agent reads AGENTS.md instead of CLAUDE.md.
    if env.step(
        env.install_editable(
            targets={"python_lib": ["app", "python_lib"]}, layers=DJANGO_LAYERS
        ),
        env.enter_project_dir(),
    ):
        pass

    # We install the prompts of the python_lib target, and ask for AGENTS.md.
    #
    # The agents file should be copied to AGENTS.md (and not to CLAUDE.md), and
    # the manifest should record this.
    if env.step(
        env.run_mn_prompts("install", "--target=python_lib", "--agents-md"),
    ):
        assert env.exit_code == 0
        assert env.read_project_file("AGENTS.md") == AGENTS_FILE_TEXT
        assert not env.project_path_exists("CLAUDE.md")
        assert env.read_manifest() == {
            "target": "python_lib",
            "layers": [],
            "agents_file": "AGENTS.md",
        }

    # We remove AGENTS.md, and install again, without a target or layers.
    #
    # It should use the agents file of the manifest, so it should copy the
    # agents file to AGENTS.md again, and not create CLAUDE.md.
    if env.step(
        env.remove_project_file("AGENTS.md"),
        env.run_mn_prompts("install"),
    ):
        assert env.exit_code == 0
        assert env.read_project_file("AGENTS.md") == AGENTS_FILE_TEXT
        assert not env.project_path_exists("CLAUDE.md")
        assert env.read_manifest()["agents_file"] == "AGENTS.md"


class Env(TestEnv):
    def remove_project_file(self, name: str):
        (self.project_dir / name).unlink()
