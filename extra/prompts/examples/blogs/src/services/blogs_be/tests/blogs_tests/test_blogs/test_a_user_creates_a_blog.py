from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
BLOG_NAME = "Jazz Notes"
BLOG_DESCRIPTION = "Notes on my favourite jazz records"


def create_env(context: Context):
    return Env(context)


def test_a_user_creates_a_blog(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up and signs in.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
    ):
        pass

    # Alice creates the blog Jazz Notes.
    #
    # The blog should be created, with Alice as its owner.
    if env.step(
        env.create_blog(BLOG_NAME, description=BLOG_DESCRIPTION),
    ):
        assert env.response.status_code == 201
        assert env.response_json() == {
            "id": env.blog_id("jazz-notes"),
            "name": BLOG_NAME,
            "slug": "jazz-notes",
            "description": BLOG_DESCRIPTION,
            "owner_id": env.user_ids[ALICE],
            "audience": "any",
        }

    # We look at the list of blogs.
    #
    # It should contain Jazz Notes.
    if env.step(
        env.get_blogs(),
    ):
        assert env.response.status_code == 200
        assert [blog["name"] for blog in env.response_json()] == [BLOG_NAME]


class Env(TestEnv):
    pass
