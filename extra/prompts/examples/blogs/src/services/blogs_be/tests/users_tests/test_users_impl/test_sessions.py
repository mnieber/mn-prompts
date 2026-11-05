from rest_framework.test import APIClient
from users_tests.users_test_env import AUTH_URL, PASSWORD, Context, TestEnv

ALICE = "alice@example.com"
NEW_PASSWORD = "an even better passphrase"


def create_env(context: Context):
    return Env(context)


def test_a_write_needs_the_csrf_token(context: Context):
    # Create the test environment
    env = create_env(context)

    # We use a client that checks the CSRF token, like the middleware does for a browser.
    # We load the session, as the frontend does when it starts.
    #
    # It should give us the CSRF cookie.
    if env.step(
        env.create_account(ALICE),
        env.use_client_that_checks_csrf(),
        env.get_session(),
    ):
        assert env.response.status_code == 401
        assert env.csrf_cookie()

    # We sign in without the CSRF token.
    #
    # It should fail with a 403.
    if env.step(
        env.sign_in_with_csrf_header(ALICE, csrf_token=None),
    ):
        assert env.response.status_code == 403

    # We sign in with the CSRF token.
    #
    # It should succeed.
    if env.step(
        env.sign_in_with_csrf_header(ALICE, csrf_token=env.csrf_cookie()),
    ):
        assert env.response.status_code == 200

    # We create a blog without the CSRF token.
    #
    # It should fail with a 403.
    if env.step(
        env.create_blog(csrf_token=None),
    ):
        assert env.response.status_code == 403

    # We create a blog with the CSRF token. Signing in has changed the token.
    #
    # It should succeed.
    if env.step(
        env.create_blog(csrf_token=env.csrf_cookie()),
    ):
        assert env.response.status_code == 201


def test_a_session_stops_working(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice is signed in, and creates a blog.
    #
    # It should succeed.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog(),
    ):
        assert env.response.status_code == 201

    # Alice signs out, and uses the API.
    #
    # It should fail with a 401.
    if env.step(
        env.sign_out(),
        env.create_blog(),
    ):
        assert env.response.status_code == 401

    # Alice signs in again. She then resets her password in another browser, and returns
    # to the first browser.
    #
    # The session in the first browser should have stopped working.
    if env.step(
        env.sign_in(ALICE, PASSWORD),
        env.use_other_browser(),
        env.request_password_reset(ALICE),
        env.reset_password(NEW_PASSWORD),
        env.use_first_browser(),
    ):
        assert env.signed_in_email() is None


class Env(TestEnv):
    def __post_init__(self):
        self.first_browser = self.context.api_client

    def create_account(self, email: str):
        self.sign_up_and_sign_in(email)
        self.sign_out()

    def use_client_that_checks_csrf(self):
        self.context.api_client = APIClient(enforce_csrf_checks=True)

    def use_other_browser(self):
        self.context.api_client = APIClient()

    def use_first_browser(self):
        self.context.api_client = self.first_browser

    def sign_in_with_csrf_header(self, email: str, csrf_token):
        self.response = self.context.api_client.post(
            f"{AUTH_URL}login",
            dict(email=email, password=PASSWORD),
            format="json",
            **self._csrf_header(csrf_token),
        )

    def create_blog(self, csrf_token=None):
        self.response = self.context.api_client.post(
            "/api/blogs/create/",
            dict(create_blog_form=dict(name="Jazz", description=None)),
            format="json",
            **self._csrf_header(csrf_token),
        )

    def _csrf_header(self, csrf_token):
        return dict(HTTP_X_CSRFTOKEN=csrf_token) if csrf_token else {}

    # Queries

    def csrf_cookie(self):
        return self.context.api_client.cookies["csrftoken"].value
