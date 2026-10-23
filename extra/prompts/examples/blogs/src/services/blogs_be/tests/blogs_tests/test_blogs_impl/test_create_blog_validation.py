from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
BLOG_NAME = "Jazz Notes"


def create_env(context: Context):
    return Env(context)


def test_create_blog_validation(context: Context):
    # Create the test environment
    env = create_env(context)

    # We create a blog without signing in.
    #
    # It should fail with a 401.
    if env.step(
        env.create_blog(BLOG_NAME),
    ):
        assert env.response.status_code == 401

    # Alice signs up, signs in and creates a blog without a description.
    #
    # The description is optional, so the blog should be created.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog(BLOG_NAME),
    ):
        assert env.response.status_code == 201
        assert env.response_json()["description"] is None

    # Alice creates a second blog with the same name.
    #
    # It should fail with BLOG_NAME_ALREADY_EXISTS.
    if env.step(
        env.create_blog(BLOG_NAME),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["BLOG_NAME_ALREADY_EXISTS"]

    # Alice creates blogs with a forbidden word in the name and in the
    # description.
    #
    # Both should fail with FORM_CONTAINS_FORBIDDEN_WORDS.
    if env.step(
        env.create_blog("Forbidden Notes"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["FORM_CONTAINS_FORBIDDEN_WORDS"]

    if env.step(
        env.create_blog("Rock Notes", description="A forbidden description"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["FORM_CONTAINS_FORBIDDEN_WORDS"]


class Env(TestEnv):
    pass
