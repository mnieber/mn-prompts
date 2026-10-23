from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
BOB = "bob@example.com"
BOBS_BLOG = "rock-notes"
PARANOID = "Paranoid"


def create_env(context: Context):
    return Env(context)


def test_blog_ownership(context: Context):
    # Create the test environment
    env = create_env(context)

    # Bob signs up, signs in, and creates the blog Rock Notes with the blog post
    # Paranoid. Then Alice signs up, signs in, and creates the blog Jazz Notes.
    if env.step(
        env.sign_up_and_sign_in(BOB),
        env.create_blog("Rock Notes"),
        env.create_blog_post(BOBS_BLOG, PARANOID),
        env.sign_up_and_sign_in(ALICE),
        env.create_blog("Jazz Notes"),
    ):
        pass

    # Alice creates a blog post in Bob's blog.
    #
    # Only the owner can do this, so it should fail with a 403.
    if env.step(
        env.create_blog_post(BOBS_BLOG, "Kind of Blue"),
    ):
        assert env.response.status_code == 403

    # Alice edits Paranoid.
    #
    # It should fail with a 403.
    if env.step(
        env.update_blog_post(BOBS_BLOG, "paranoid", title="Iron Man"),
    ):
        assert env.response.status_code == 403

    # Alice deletes Paranoid.
    #
    # It should fail with a 403, and Paranoid should not be deleted.
    if env.step(
        env.delete_blog_posts(BOBS_BLOG, [env.blog_post_id(PARANOID)]),
    ):
        assert env.response.status_code == 403
        assert env.blog_post_titles(BOBS_BLOG) == [PARANOID]

    # We sign out, and look at the list of blogs and at the blog posts of Rock
    # Notes.
    #
    # Everyone may read blogs, so we should see the blogs of Alice and Bob.
    if env.step(
        env.sign_out(),
        env.get_blogs(),
    ):
        assert env.response.status_code == 200
        assert {blog["owner_id"] for blog in env.response_json()} == {
            env.user_ids[ALICE],
            env.user_ids[BOB],
        }

    if env.step(
        env.get_blog_posts(BOBS_BLOG),
    ):
        assert env.response.status_code == 200
        assert [post["title"] for post in env.response_json()] == [PARANOID]


class Env(TestEnv):
    pass
