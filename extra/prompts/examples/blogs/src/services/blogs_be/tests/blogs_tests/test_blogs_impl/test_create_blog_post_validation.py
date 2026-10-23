from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
JAZZ_NOTES = "jazz-notes"
ROCK_NOTES = "rock-notes"
TITLE = "Kind of Blue"


def create_env(context: Context):
    return Env(context)


def test_create_blog_post_validation(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, signs in, and creates the blogs Jazz Notes and Rock Notes.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog("Jazz Notes"),
        env.create_blog("Rock Notes"),
    ):
        pass

    # Alice creates a blog post without content.
    #
    # The content is optional, so the blog post should be created.
    if env.step(
        env.create_blog_post(JAZZ_NOTES, TITLE),
    ):
        assert env.response.status_code == 201
        assert env.response_json()["content"] is None

    # Alice creates a second blog post with the same title in the same blog.
    #
    # It should fail with BLOG_POST_TITLE_ALREADY_EXISTS.
    if env.step(
        env.create_blog_post(JAZZ_NOTES, TITLE),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["BLOG_POST_TITLE_ALREADY_EXISTS"]

    # Alice creates a blog post with the same title in another blog.
    #
    # Titles only need to be unique within a blog, so it should be created.
    if env.step(
        env.create_blog_post(ROCK_NOTES, TITLE),
    ):
        assert env.response.status_code == 201

    # Alice creates blog posts with a forbidden word in the title and in the
    # content.
    #
    # Both should fail with FORM_CONTAINS_FORBIDDEN_WORDS.
    if env.step(
        env.create_blog_post(JAZZ_NOTES, "Forbidden Fruit"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["FORM_CONTAINS_FORBIDDEN_WORDS"]

    if env.step(
        env.create_blog_post(JAZZ_NOTES, "Giant Steps", content="Forbidden content"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["FORM_CONTAINS_FORBIDDEN_WORDS"]


class Env(TestEnv):
    pass
