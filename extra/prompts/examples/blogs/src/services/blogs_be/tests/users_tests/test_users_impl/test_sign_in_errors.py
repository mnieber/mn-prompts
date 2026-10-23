from users_tests.users_test_env import PASSWORD, Context, TestEnv

from blogs_be.users.tests.factories import InactiveUserFactory

ALICE = "alice@example.com"
BOB = "bob@example.com"


def create_env(context: Context):
    return Env(context)


def test_sign_in_errors(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, and signs in with the wrong password.
    #
    # It should fail with INVALID_CREDENTIALS.
    if env.step(
        env.sign_up(ALICE),
        env.sign_in(ALICE, password="wrong password"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["INVALID_CREDENTIALS"]

    # Bob has an account that is not active, and signs in.
    #
    # It should fail with INACTIVE_ACCOUNT.
    if env.step(
        env.create_inactive_user(BOB),
        env.sign_in(BOB),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["INACTIVE_ACCOUNT"]


class Env(TestEnv):
    def create_inactive_user(self, email: str):
        """Signing up activates the account, so we create it directly."""
        InactiveUserFactory(email=email, password=PASSWORD)
