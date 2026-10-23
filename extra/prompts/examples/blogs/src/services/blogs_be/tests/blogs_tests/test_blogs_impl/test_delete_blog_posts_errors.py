import uuid

from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
JAZZ_NOTES = "jazz-notes"
KIND_OF_BLUE = "Kind of Blue"


def create_env(context: Context):
    return Env(context)


def test_delete_blog_posts_errors(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, signs in, and creates the blog Jazz Notes with the blog post
    # Kind of Blue.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog("Jazz Notes"),
        env.create_blog_post(JAZZ_NOTES, KIND_OF_BLUE),
    ):
        pass

    # Alice deletes Kind of Blue together with a blog post that doesn't exist.
    #
    # It should fail with BLOG_POSTS_NOT_FOUND, and Kind of Blue should not be
    # deleted.
    if env.step(
        env.delete_blog_posts(
            JAZZ_NOTES, [env.blog_post_id(KIND_OF_BLUE), str(uuid.uuid4())]
        ),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["BLOG_POSTS_NOT_FOUND"]
        assert env.blog_post_titles(JAZZ_NOTES) == [KIND_OF_BLUE]

    # Alice deletes blog posts from a blog that doesn't exist.
    #
    # It should fail with BLOG_NOT_FOUND.
    if env.step(
        env.delete_blog_posts("rock-notes", [env.blog_post_id(KIND_OF_BLUE)]),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["BLOG_NOT_FOUND"]


class Env(TestEnv):
    pass
