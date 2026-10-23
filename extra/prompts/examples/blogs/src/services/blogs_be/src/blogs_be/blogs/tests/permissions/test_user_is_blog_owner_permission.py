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
