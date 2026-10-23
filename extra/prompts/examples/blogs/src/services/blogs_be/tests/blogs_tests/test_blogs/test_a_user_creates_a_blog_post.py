from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
BLOG_NAME = "Jazz Notes"
BLOG_SLUG = "jazz-notes"
TITLE = "Kind of Blue"
CONTENT = "Miles Davis recorded Kind of Blue in two sessions in 1959."


def create_env(context: Context):
    return Env(context)


def test_a_user_creates_a_blog_post(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, signs in and creates the blog Jazz Notes.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog(BLOG_NAME),
    ):
        pass

    # Alice creates the blog post Kind of Blue in Jazz Notes.
    #
    # The blog post should be created. It should not be published yet.
    if env.step(
        env.create_blog_post(BLOG_SLUG, TITLE, content=CONTENT),
    ):
        assert env.response.status_code == 201
        assert env.response_json() == {
            "id": env.blog_post_id(TITLE),
            "title": TITLE,
            "slug": "kind-of-blue",
            "blog_id": env.blog_id(BLOG_SLUG),
            "content": CONTENT,
            "is_published": False,
            "level": "medium",
        }

    # We look at the blog posts of Jazz Notes.
    #
    # It should contain Kind of Blue.
    if env.step(
        env.get_blog_posts(BLOG_SLUG),
    ):
        assert env.response.status_code == 200
        assert [post["title"] for post in env.response_json()] == [TITLE]


class Env(TestEnv):
    pass
