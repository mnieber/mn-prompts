from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
JAZZ_NOTES = "jazz-notes"
TITLE = "Kind of Blue"


def create_env(context: Context):
    return Env(context)


def test_create_blog_post_validation(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, signs in, and creates the blog Jazz Notes with the blog post
    # Kind of Blue.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog("Jazz Notes"),
        env.create_blog_post(JAZZ_NOTES, TITLE),
    ):
        pass

    # Alice creates a second blog post with the same title in the same blog.
    #
    # It should fail with BLOG_POST_TITLE_ALREADY_EXISTS.
    if env.step(
        env.create_blog_post(JAZZ_NOTES, TITLE),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["BLOG_POST_TITLE_ALREADY_EXISTS"]

    # Alice creates blog posts with a forbidden word in the title and in the
    # content.
    #
    # Both should fail with FORM_CONTAINS_FORBIDDEN_WORDS, and name the field.
    if env.step(
        env.create_blog_post(JAZZ_NOTES, "Forbidden Fruit"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["FORM_CONTAINS_FORBIDDEN_WORDS"]
        assert env.error_details() == ["title"]

    if env.step(
        env.create_blog_post(JAZZ_NOTES, "Giant Steps", content="Forbidden content"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["FORM_CONTAINS_FORBIDDEN_WORDS"]
        assert env.error_details() == ["content"]


class Env(TestEnv):
    pass
