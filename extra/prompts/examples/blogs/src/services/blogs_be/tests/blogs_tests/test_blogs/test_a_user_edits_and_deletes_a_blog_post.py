from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
BLOG_NAME = "Jazz Notes"
BLOG_SLUG = "jazz-notes"
KIND_OF_BLUE = "Kind of Blue"
A_LOVE_SUPREME = "A Love Supreme"
UPDATED_TITLE = "Kind of Blue (1959)"
UPDATED_CONTENT = "The best-selling jazz record of all time."


def create_env(context: Context):
    return Env(context)


def test_a_user_edits_and_deletes_a_blog_post(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, signs in, and creates the blog Jazz Notes with two blog
    # posts.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog(BLOG_NAME),
        env.create_blog_post(BLOG_SLUG, KIND_OF_BLUE, content="Draft"),
        env.create_blog_post(BLOG_SLUG, A_LOVE_SUPREME, content="Draft"),
    ):
        pass

    # Alice edits the title and the content of Kind of Blue.
    #
    # The blog post should be updated.
    if env.step(
        env.update_blog_post(
            BLOG_SLUG, "kind-of-blue", title=UPDATED_TITLE, content=UPDATED_CONTENT
        ),
    ):
        assert env.response.status_code == 200
        assert env.response_json()["title"] == UPDATED_TITLE
        assert env.response_json()["content"] == UPDATED_CONTENT

        # The slug is used in urls, so it should not change with the title
        assert env.response_json()["slug"] == "kind-of-blue"

    # Alice deletes A Love Supreme.
    #
    # Only the edited blog post should remain.
    if env.step(
        env.delete_blog_posts(BLOG_SLUG, [env.blog_post_id(A_LOVE_SUPREME)]),
    ):
        assert env.response.status_code == 204
        assert env.response.data == {"deleted_count": 1}
        assert env.blog_post_titles(BLOG_SLUG) == [UPDATED_TITLE]


class Env(TestEnv):
    pass
