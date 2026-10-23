from users_tests.users_test_env import Context, TestEnv

ALICE = "alice@example.com"


def create_env(context: Context):
    return Env(context)


def test_sign_up_errors(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, but the password confirmation is different.
    #
    # It should fail with PASSWORDS_DO_NOT_MATCH.
    if env.step(
        env.sign_up(ALICE, password="secret-1", password_confirmation="secret-2"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["PASSWORDS_DO_NOT_MATCH"]

    # Alice signs up correctly, and then signs up again.
    #
    # The second attempt should fail with USER_EMAIL_ALREADY_EXISTS.
    if env.step(
        env.sign_up(ALICE),
        env.sign_up(ALICE),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["USER_EMAIL_ALREADY_EXISTS"]


class Env(TestEnv):
    pass
