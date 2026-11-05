from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from users_tests.users_test_env import PASSWORD, Context, TestEnv

from blogs_be.users.tests.factories import InactiveUserFactory

ALICE = "alice@example.com"
BOB = "bob@example.com"
CAROL = "carol@example.com"
ADMIN = "admin@example.com"


def create_env(context: Context):
    return Env(context)


def test_sign_in_errors(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice has an account, and signs in with the wrong password.
    #
    # It should fail with email_password_mismatch.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.sign_out(),
        env.sign_in(ALICE, password="wrong password"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["email_password_mismatch"]

    # Someone signs in with an email that is not known.
    #
    # It should give the same error.
    if env.step(
        env.sign_in("nobody@example.com"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["email_password_mismatch"]

    # Bob has an account that is not active, and signs in.
    #
    # It should not sign him in, and no step should be pending.
    if env.step(
        env.create_inactive_user(BOB),
        env.sign_in(BOB),
    ):
        assert env.response.status_code == 401
        assert env.pending_flows() == []
        assert env.signed_in_email() is None


def test_too_many_failed_attempts(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice has an account, and someone keeps guessing her password.
    #
    # It should stop trying the password, also when the password is correct.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.sign_out(),
        env.guess_password_many_times(ALICE),
        env.sign_in(ALICE),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["too_many_login_attempts"]
        assert env.signed_in_email() is None


def test_signing_in_with_an_unverified_email(context: Context):
    # Create the test environment
    env = create_env(context)

    # Carol signs up in a browser, and doesn't verify her email.
    if env.step(
        env.sign_up(CAROL),
    ):
        pass

    # Carol signs in from a new browser.
    #
    # It should not sign her in, and say that verifying is pending.
    if env.step(
        env.use_new_browser(),
        env.sign_in(CAROL),
    ):
        assert env.response.status_code == 401
        assert env.pending_flows() == ["verify_email"]
        assert env.signed_in_email() is None


def test_signing_in_while_signed_in(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice is signed in, and signs in again.
    #
    # It should fail with a 409, and she should stay signed in.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.sign_in(ALICE),
    ):
        assert env.response.status_code == 409
        assert env.signed_in_email() == ALICE


def test_a_superuser_signs_in(context: Context):
    # Create the test environment
    env = create_env(context)

    # A superuser, created with createsuperuser, signs in.
    #
    # It should sign them in, without verifying their email.
    if env.step(
        env.create_superuser(ADMIN),
        env.sign_in(ADMIN),
    ):
        assert env.response.status_code == 200
        assert env.signed_in_email() == ADMIN


class Env(TestEnv):
    def create_inactive_user(self, email: str):
        """The API doesn't deactivate accounts, so we create it directly."""
        InactiveUserFactory(email=email, password=PASSWORD)

    def create_superuser(self, email: str):
        """The API doesn't create superusers."""
        get_user_model().objects.create_superuser(email=email, password=PASSWORD)

    def guess_password_many_times(self, email: str):
        for _ in range(10):
            self.sign_in(email, password="wrong password")

    def use_new_browser(self):
        self.context.api_client = APIClient()
