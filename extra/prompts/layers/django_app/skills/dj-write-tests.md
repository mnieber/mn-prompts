# Skill: dj-write-tests

Applies when writing tests for actions, API views, and permissions in a Django app module.

Primary references:
- `blogs_be/src/blogs_be/blogs/tests/actions/create_blog_post/test_create_blog_post_action.py`
- `blogs_be/src/blogs_be/blogs/tests/views/create_blog_post_api_view/test_create_blog_post_api_view.py`
- `blogs_be/src/blogs_be/blogs/tests/permissions/test_user_is_blog_owner_permission.py`

---

## File locations

```
<module>/tests/actions/<action_name>/test_<action_name>_action.py
<module>/tests/views/<view_name>/test_<view_name>.py
<module>/tests/permissions/test_<permission_name>_permission.py
```

## Action tests

Test the action function directly. Use pytest fixtures to create the database state, and assert on the returned object or on raised exceptions.

```python
import pytest
from blogs_be.blogs.actions.create_blog_post import (
    BlogPostWithTitleAlreadyExistsError,
    CreateBlogPostForm,
    create_blog_post,
)
from blogs_be.blogs.tests.factories import BlogFactory, BlogPostFactory
from blogs_be.users.tests.factories import UserFactory


class TestCreateBlogPostAction:
    @pytest.fixture()
    def blog_owner(self):
        return UserFactory()

    @pytest.fixture
    def blog(self, blog_owner):
        return BlogFactory(owner=blog_owner)

    @pytest.mark.django_db
    def test_create_blog_post_action_success(self, blog):
        create_blog_post_form = CreateBlogPostForm(title="Test BlogPost", content="A test blog post")
        blog_post = create_blog_post(create_blog_post_form, blog=blog)
        assert blog_post.title == "Test BlogPost"

    @pytest.mark.django_db
    def test_create_blog_post_action_with_existing_title(self, blog):
        BlogPostFactory(title="Existing BlogPost", blog=blog)
        create_blog_post_form = CreateBlogPostForm(title="Existing BlogPost", content="...")
        with pytest.raises(BlogPostWithTitleAlreadyExistsError):
            create_blog_post(create_blog_post_form, blog=blog)
```

RULE: Test one success case and one case per exception the action can raise. Do not test every combination of inputs — keep action tests focused on boundary conditions that the action itself enforces.

## API view tests

Use `APIClient` and `reverse()`. Verify the HTTP status code and the response JSON shape using `deepdiff.DeepDiff`.

Always include a separate `test_<view_name>_permissions` test that uses `checks_permission` to verify the view is wired to the correct permission function. This test does not require `@pytest.mark.django_db`.

```python
import deepdiff
import pytest
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.tests.factories import BlogFactory
from blogs_be.blogs.views.create_blog_post_api_view import CreateBlogPostApiView
from django.urls import reverse
from rest_framework.test import APIClient

from blogs_be.api.utils.extend_schema.permissions import checks_permission
from blogs_be.common.utils.test_utils import DeepDiffOperator, rhs_is_not_none
from blogs_be.users.tests.factories import UserFactory


class TestCreateBlogPostApiView:
    @pytest.fixture()
    def api_client(self):
        return APIClient()

    @pytest.fixture()
    def blog_owner(self):
        return UserFactory()

    @pytest.fixture()
    def blog(self, blog_owner):
        return BlogFactory(owner=blog_owner)

    @pytest.mark.django_db()
    def test_create_blog_post_api_view_success(self, api_client, blog_owner, blog):
        api_client.force_authenticate(user=blog_owner)
        url = reverse("create-blog-post", kwargs=dict(blog_key=blog.slug))
        response = api_client.post(
            url,
            data=dict(create_blog_post_form=dict(title="My blog title", content="My blog content")),
        )
        assert response.status_code == 201
        result = response.json()
        diff = deepdiff.DeepDiff(
            {"id": "some id", "blog_id": str(blog.id), "title": "My blog title"},
            result,
            custom_operators=[DeepDiffOperator(rhs_is_not_none, "id")],
        )
        assert not diff, f"JSON response differs: {diff.pretty()}"

    def test_create_blog_post_api_view_permissions(self):
        assert checks_permission(CreateBlogPostApiView.post, user_is_blog_owner)
```

RULE: Do not re-test that the api-view handles every exception the underlying action may raise. Since the action tests already verify those conditions, duplicating them in the api-view test bloats the test suite without adding value.

## Permission tests

Test each permission function directly, verifying both the allow and deny branches.

```python
import pytest
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.tests.factories import BlogFactory
from blogs_be.users.tests.factories import UserFactory


class TestUserIsBlogOwnerPermission:
    @pytest.fixture()
    def blog_owner(self):
        return UserFactory()

    @pytest.fixture()
    def other_user(self):
        return UserFactory()

    @pytest.fixture
    def blog(self, blog_owner):
        return BlogFactory(owner=blog_owner)

    @pytest.mark.django_db
    def test_user_is_blog_owner_success(self, blog, blog_owner):
        result = user_is_blog_owner(blog_owner, blog)
        assert result.permission_allowed
        assert result.reason is None

    @pytest.mark.django_db
    def test_user_is_blog_owner_failure_not_owner(self, blog, other_user):
        result = user_is_blog_owner(other_user, blog)
        assert not result.permission_allowed
        assert result.reason == "User must be the blog owner"
```

## Checklist

- [ ] Action tests: one success case + one case per exception type
- [ ] Action tests: use `pytest.raises` to assert exceptions
- [ ] API view tests: include a `test_..._permissions` test using `checks_permission`
- [ ] API view tests: do not duplicate action exception coverage
- [ ] API view tests: use `deepdiff.DeepDiff` for response JSON comparison
- [ ] Permission tests: cover both `allow` and `deny` branches
- [ ] All database tests marked with `@pytest.mark.django_db`
