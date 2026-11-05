from users_tests.users_test_env import PASSWORD, Context, TestEnv

ALICE = "alice@example.com"
NEW_PASSWORD = "an even better passphrase"


def create_env(context: Context):
    return Env(context)


def test_a_user_resets_their_password(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice has an account, and forgot her password. She asks for a reset link.
    #
    # It should succeed, and send her an email.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.sign_out(),
        env.request_password_reset(ALICE),
    ):
        assert env.response.status_code == 200

    # Alice follows the link in the email, and chooses a new password.
    #
    # It should succeed, without signing her in.
    if env.step(
        env.reset_password(NEW_PASSWORD),
    ):
        assert env.response.status_code == 401
        assert env.signed_in_email() is None

    # Alice signs in with her old password.
    #
    # It should fail.
    if env.step(
        env.sign_in(ALICE, PASSWORD),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["email_password_mismatch"]

    # Alice signs in with her new password.
    #
    # It should succeed.
    if env.step(
        env.sign_in(ALICE, NEW_PASSWORD),
    ):
        assert env.response.status_code == 200
        assert env.signed_in_email() == ALICE


class Env(TestEnv):
    pass
