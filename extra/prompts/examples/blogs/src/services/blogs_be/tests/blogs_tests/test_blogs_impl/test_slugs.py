from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
JAZZ_NOTES = "jazz-notes"


def create_env(context: Context):
    return Env(context)


def test_blog_slugs(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, signs in, and creates the blog Jazz Notes.
    #
    # The slug should be derived from the name.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog("Jazz Notes"),
    ):
        assert env.response_json()["slug"] == JAZZ_NOTES

    # Alice creates a blog with a different name that gives the same slug.
    #
    # It should get a suffix.
    if env.step(
        env.create_blog("Jazz-Notes"),
    ):
        assert env.response_json()["slug"] == "jazz-notes-2"


class Env(TestEnv):
    pass
