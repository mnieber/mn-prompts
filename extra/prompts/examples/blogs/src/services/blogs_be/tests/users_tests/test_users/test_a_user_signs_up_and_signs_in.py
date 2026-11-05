from django.contrib.auth import get_user_model
from django.core import mail
from users_tests.users_test_env import Context, TestEnv

ALICE = "alice@example.com"


def create_env(context: Context):
    return Env(context)


def test_a_user_signs_up_and_signs_in(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up.
    #
    # She should receive a verification email, and verifying should be pending.
    if env.step(
        env.sign_up(ALICE),
    ):
        assert env.response.status_code == 401
        assert env.pending_flows() == ["verify_email"]
        assert mail.outbox[-1].to == [ALICE]
        assert "http://testserver/account/verify-email/" in mail.outbox[-1].body

    # Alice follows the link in the email.
    #
    # It should succeed, without signing her in.
    if env.step(
        env.verify_email(),
    ):
        assert env.response.status_code == 401
        assert env.pending_flows() == []
        assert env.signed_in_email() is None

    # Alice signs in.
    #
    # She should be signed in, with her email and id in the response.
    if env.step(
        env.sign_in(ALICE),
    ):
        assert env.response.status_code == 200
        assert env.response_json()["data"]["user"]["email"] == ALICE
        assert env.response_json()["data"]["user"]["id"] == env.user_id(ALICE)
        assert env.signed_in_email() == ALICE

    # Alice signs out.
    #
    # She should no longer be signed in.
    if env.step(
        env.sign_out(),
    ):
        assert env.response.status_code == 401
        assert env.signed_in_email() is None


class Env(TestEnv):
    # Queries

    def user_id(self, email: str):
        return str(get_user_model().objects.get(email=email).id)
