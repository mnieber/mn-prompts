from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
BOB = "bob@example.com"
JAZZ_NOTES = "jazz-notes"
KIND_OF_BLUE = "kind-of-blue"


def create_env(context: Context):
    return Env(context)


def test_a_user_publishes_a_blog_post(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, signs in, and creates the blog Jazz Notes with the blog post
    # Kind of Blue.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog("Jazz Notes"),
        env.create_blog_post(JAZZ_NOTES, "Kind of Blue"),
    ):
        assert env.response_json()["is_published"] is False

    # Alice publishes Kind of Blue.
    #
    # It should be published.
    if env.step(
        env.mark_blog_post_as_published(JAZZ_NOTES, KIND_OF_BLUE),
    ):
        assert env.response.status_code == 200
        assert env.response_json()["is_published"] is True

    # We look at the blog posts of Jazz Notes.
    #
    # Kind of Blue should be published.
    if env.step(
        env.get_blog_posts(JAZZ_NOTES),
    ):
        assert env.response_json()[0]["is_published"] is True

    # Alice publishes Kind of Blue again.
    #
    # It should stay published.
    if env.step(
        env.mark_blog_post_as_published(JAZZ_NOTES, KIND_OF_BLUE),
    ):
        assert env.response.status_code == 200
        assert env.response_json()["is_published"] is True


def test_publishing_fails(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, signs in, and creates the blog Jazz Notes with the blog post
    # Kind of Blue.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog("Jazz Notes"),
        env.create_blog_post(JAZZ_NOTES, "Kind of Blue"),
    ):
        pass

    # Alice publishes a blog post that doesn't exist.
    #
    # It should fail with BLOG_POST_NOT_FOUND.
    if env.step(
        env.mark_blog_post_as_published(JAZZ_NOTES, "giant-steps"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["BLOG_POST_NOT_FOUND"]

    # Bob signs up, signs in, and publishes Kind of Blue.
    #
    # Only the owner can do this, so it should fail with a 403.
    if env.step(
        env.sign_up_and_sign_in(BOB),
        env.mark_blog_post_as_published(JAZZ_NOTES, KIND_OF_BLUE),
    ):
        assert env.response.status_code == 403

    # We look at the blog posts of Jazz Notes.
    #
    # Kind of Blue should not be published.
    if env.step(
        env.get_blog_posts(JAZZ_NOTES),
    ):
        assert env.response_json()[0]["is_published"] is False


class Env(TestEnv):
    def mark_blog_post_as_published(self, blog_slug: str, blog_post_slug: str):
        self._post(
            "mark-blog-post-as-published",
            url_kwargs=dict(blog_key=blog_slug, blog_post_key=blog_post_slug),
        )
