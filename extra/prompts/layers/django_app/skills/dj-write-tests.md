# Skill: dj-write-tests

Applies when writing tests for a Django app. The tests are workflow tests and impl tests: follow the
`py-write-workflow-tests` skill of the python_lib layer. This skill only adds what is specific to Django.

Primary references:

- `blogs_be/tests/blogs_be_test_env.py` (the base `Context` and `TestEnv`)
- `blogs_be/tests/blogs_tests/blogs_test_env.py` (the API actions of a feature)
- `blogs_be/tests/blogs_tests/test_blogs/test_a_user_edits_and_deletes_a_blog_post.py` (a workflow test)
- `blogs_be/tests/blogs_tests/test_blogs_impl/test_blog_ownership.py` (permissions)

---

## File layout

The tests live in the `tests/` directory of the service (not inside the app package), with one test package per
module (e.g. `blogs_tests`, `users_tests`). Add `testpaths = ["tests"]` to the `[tool.pytest.ini_options]` of
`pyproject.toml`.

The impl tests are grouped by theme, e.g. `test_create_blog_post_validation.py`, `test_update_blog_post_validation.py` and
`test_blog_ownership.py`.

## Use the API like the frontend does

The scenarios start with the frontend calling an API view, so the tests do the same. An action posts to (or gets
from) a url with the `APIClient`, and stores the response in `env.response`:

```python
class TestEnv(BlogsBeTestEnv):
    def create_blog_post(self, blog_slug: str, title: str, content=None):
        self._post(
            "create-blog-post",
            url_kwargs=dict(blog_key=blog_slug),
            create_blog_post_form=dict(title=title, content=content),
        )
```

- `_post` and `_get` are private helpers of the base `TestEnv` that call `reverse()` with the url name.
- Use the slug (not the id) as the url key when the view accepts both: it makes the test easier to read.

## Errors are responses

An API view turns an error into a response, so the tests don't need `*_and_catch_error` actions. Assert on the
status code, and on the error codes (via the `env.error_codes()` query):

```python
    # Alice creates a second blog post with the same title in the same blog.
    #
    # It should fail with BLOG_POST_TITLE_ALREADY_EXISTS.
    if env.step(
        env.create_blog_post(JAZZ_NOTES, TITLE),
    ):
        assert env.response.status_code == 400
        assert env.error_codes() == ["BLOG_POST_TITLE_ALREADY_EXISTS"]
```

## Users and permissions

- Users sign up and sign in through the API (`env.sign_up_and_sign_in(ALICE)`). Signing in makes the `APIClient`
  send the access token in the next requests, and `env.sign_out()` stops it. Don't use `force_authenticate`.
- A test can switch between users by signing in as another user.
- Permissions are tested through their behaviour: another user tries the action, gets a 403, and nothing changes
  (see `test_blog_ownership.py`). There are no separate tests of the permission functions.

## The database

- The `context` fixture in the `conftest.py` of the test package depends on the `db` fixture of pytest-django, so
  the tests don't need a `@pytest.mark.django_db` marker:

  ```python
  @pytest.fixture
  def context(db):
      return Context(api_client=APIClient())
  ```

- Queries may read the database, e.g. to get the id of a blog post (`env.blog_post_id(TITLE)`), or to check that
  nothing was deleted (`env.blog_post_titles(BLOG_SLUG)`).
- Create the starting state through the API. Use a factory (see [dj-write-factories](./dj-write-factories.md))
  only for a state that the API can't create (e.g. an inactive user), in an action whose docstring says why.

## Checking a response

Compare the JSON of a response with a plain dict. Get the expected ids from the database (or from
`env.user_ids`), not from the response itself:

```python
        assert env.response_json() == {
            "id": env.blog_post_id(TITLE),
            "title": TITLE,
            "slug": "kind-of-blue",
            "blog_id": env.blog_id(BLOG_SLUG),
            "content": CONTENT,
            "is_published": False,
            "level": "medium",
        }
```

## Checklist

- [ ] The tests follow the `py-write-workflow-tests` skill
- [ ] Each scenario has a workflow test; the edge cases are in impl tests, grouped by theme
- [ ] Actions call the API with the `APIClient`, and store the response in `env.response`
- [ ] Errors are checked with the status code and `env.error_codes()`
- [ ] Users sign in through the API; permissions are tested through their behaviour (403)
- [ ] The `context` fixture depends on `db`; factories are only used for states that the API can't create
