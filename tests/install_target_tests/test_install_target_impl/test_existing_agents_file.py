from install_target_tests.install_target_test_env import Context, TestEnv

OUR_AGENTS_FILE_TEXT = "# Agents\n\nAlways run the tests before you commit.\n"


def create_env(context: Context):
    return Env(context)


def test_existing_agents_file(context: Context):
    # Create the test environment
    env = create_env(context)

    # We have an editable install of mn-prompts with the target python_lib, and
    # a project that already has its own AGENTS.md.
    if env.step(
        env.install_editable(target_names=["python_lib"]),
        env.enter_project_dir(),
        env.write_agents_file(OUR_AGENTS_FILE_TEXT),
    ):
        pass

    # We install the prompts of the python_lib target.
    #
    # It should create the instructions symlink, but leave our AGENTS.md
    # unchanged. We should be told to extend AGENTS.md with the contents of the
    # agents file, and this is not an error.
    if env.step(
        env.run_mn_prompts_cli("install", "python_lib"),
    ):
        assert env.exit_code == 0
        assert env.instructions_link() == env.prompts_dir / "targets" / "python_lib"
        assert env.read_project_file("AGENTS.md") == OUR_AGENTS_FILE_TEXT
        assert "AGENTS.md" in env.error_output
        assert str(env.agents_file_source()) in env.error_output


class Env(TestEnv):
    pass
