from blogs_tests.blogs_test_env import Context, TestEnv

ALICE = "alice@example.com"
JAZZ_NOTES = "jazz-notes"
ROCK_NOTES = "rock-notes"
KIND_OF_BLUE = "Kind of Blue"
GIANT_STEPS = "Giant Steps"
CONTENT = "Recorded in 1959."


def create_env(context: Context):
    return Env(context)


def test_update_blog_post_validation(context: Context):
    # Create the test environment
    env = create_env(context)

    # Alice signs up, signs in, and creates the blog Jazz Notes with the blog
    # posts Kind of Blue and Giant Steps.
    if env.step(
        env.sign_up_and_sign_in(ALICE),
        env.create_blog("Jazz Notes"),
        env.create_blog_post(JAZZ_NOTES, KIND_OF_BLUE, content=CONTENT),
        env.create_blog_post(JAZZ_NOTES, GIANT_STEPS, content=CONTENT),
    ):
        pass

    # Alice only updates the content of Kind of Blue.
    #
    # The title should stay the same.
    if env.step(
        env.update_blog_post(JAZZ_NOTES, "kind-of-blue", content="Updated content"),
    ):
        assert env.response.status_code == 200
        assert env.response_json()["title"] == KIND_OF_BLUE
        assert env.response_json()["content"] == "Updated content"

    # Alice updates Kind of Blue without any changes.
    #
    # The blog post should stay the same.
    if env.step(
        env.update_blog_post(JAZZ_NOTES, "kind-of-blue"),
    ):
        assert env.response.status_code == 200
        assert env.response_json()["title"] == KIND_OF_BLUE
        assert env.response_json()["content"] == "Updated content"

    # Alice renames Kind of Blue to Giant Steps.
    #
    # It should fail with BLOG_WITH_THIS_TITLE_ALREADY_EXISTS.
    if env.step(
        env.update_blog_post(JAZZ_NOTES, "kind-of-blue", title=GIANT_STEPS),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["BLOG_WITH_THIS_TITLE_ALREADY_EXISTS"]

    # Alice creates Rock Notes with the blog post Paranoid, and renames it to
    # Giant Steps.
    #
    # Titles only need to be unique within a blog, so it should be renamed.
    if env.step(
        env.create_blog("Rock Notes"),
        env.create_blog_post(ROCK_NOTES, "Paranoid"),
        env.update_blog_post(ROCK_NOTES, "paranoid", title=GIANT_STEPS),
    ):
        assert env.response.status_code == 200
        assert env.response_json()["title"] == GIANT_STEPS

    # Alice updates Kind of Blue with a forbidden word in the title and in the
    # content.
    #
    # Both should fail with FORM_CONTAINS_FORBIDDEN_WORDS.
    if env.step(
        env.update_blog_post(JAZZ_NOTES, "kind-of-blue", title="Forbidden Fruit"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["FORM_CONTAINS_FORBIDDEN_WORDS"]

    if env.step(
        env.update_blog_post(JAZZ_NOTES, "kind-of-blue", content="Forbidden content"),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["FORM_CONTAINS_FORBIDDEN_WORDS"]


class Env(TestEnv):
    pass
