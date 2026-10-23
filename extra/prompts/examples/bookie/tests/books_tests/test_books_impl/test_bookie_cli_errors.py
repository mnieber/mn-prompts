from books_tests.books_test_env import Context, TestEnv

TITLE = "The Hobbit"
TOO_MANY_CHAPTERS_MESSAGE = (
    "TooManyChaptersError: "
    "Cannot create book with 11 chapters. Maximum allowed is 10."
)


def create_env(context: Context):
    return Env(context)


def test_bookie_cli_errors(context: Context):
    # Create the test environment
    env = create_env(context)

    # We run bookie without a command.
    #
    # It should exit with a usage error.
    if env.step(
        env.run_bookie_and_catch_exit(),
    ):
        assert env.system_exit.code == 2
        assert "the following arguments are required: command" in env.error_output

    # We try to create a book with too many chapters.
    #
    # Bookie should print the error with a hint (but no traceback), and return
    # exit code 1.
    if env.step(
        env.run_bookie_cli("create-book", f"--title={TITLE}", "--chapters=11"),
    ):
        assert env.exit_code == 1
        assert env.output == ""
        assert env.error_output.splitlines() == [
            TOO_MANY_CHAPTERS_MESSAGE,
            "Hint: run with -v to see the traceback.",
        ]

    # We try again in verbose mode.
    #
    # Bookie should print the traceback, followed by the error.
    if env.step(
        env.run_bookie_cli("-v", "create-book", f"--title={TITLE}", "--chapters=11"),
    ):
        assert env.exit_code == 1
        assert env.error_output.startswith("Traceback")
        assert env.error_output.splitlines()[-1] == TOO_MANY_CHAPTERS_MESSAGE


class Env(TestEnv):
    pass
