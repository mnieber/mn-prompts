from django.core import mail
from rest_framework.test import APIClient
from users_tests.users_test_env import Context, TestEnv

ALICE = "alice@example.com"
BOB = "bob@example.com"


def create_env(context: Context):
    return Env(context)


def test_sign_up_errors(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up with a password that is too common.
    #
    # It should fail with password_too_common, and not create an account.
    if env.step(
        env.sign_up(ALICE, password="password123"),
    ):
        assert env.response.status_code == 400
        assert env.error_params() == ["password"]
        assert env.error_codes() == ["password_too_common"]

    # Alice signs up with a password that is too short.
    #
    # It should fail with password_too_short.
    if env.step(
        env.sign_up(ALICE, password="x9!k"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["password_too_short"]

    # Alice signs up with an invalid email address.
    #
    # It should fail on the email field.
    if env.step(
        env.sign_up("not-an-email"),
    ):
        assert env.response.status_code == 400
        assert env.error_params() == ["email"]


def test_signing_up_does_not_reveal_an_account(context: Context):
    # Create the test environment
    env = create_env(context)

    # Bob signs up with a new email address, to see what that response looks like.
    if env.step(
        env.sign_up(BOB),
        env.remember_response(),
    ):
        pass

    # Alice has an account. Someone else signs up with her email address.
    #
    # The response should be the same as for a new email address, and only Alice should
    # receive an email, which doesn't contain a verification link.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.sign_out(),
        env.clear_emails(),
        env.sign_up(ALICE),
    ):
        assert env.response.status_code == env.remembered_status
        assert env.pending_flows() == env.remembered_flows
        assert [x.to for x in mail.outbox] == [[ALICE]]
        assert "verify-email" not in mail.outbox[-1].body


class Env(TestEnv):
    def remember_response(self):
        self.remembered_status = self.response.status_code
        self.remembered_flows = self.pending_flows()
        self.context.api_client = APIClient()

    def clear_emails(self):
        mail.outbox.clear()

    # Queries

    def error_params(self):
        return [error["param"] for error in self.response.json()["errors"]]
