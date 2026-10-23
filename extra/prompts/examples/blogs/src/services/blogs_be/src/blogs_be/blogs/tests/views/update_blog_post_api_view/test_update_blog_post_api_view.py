import deepdiff
import pytest
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.tests.factories import BlogFactory, BlogPostFactory
from blogs_be.blogs.views.update_blog_post_api_view import UpdateBlogPostApiView
from django.urls import reverse
from rest_framework.test import APIClient

from blogs_be.api.utils.extend_schema.permissions import checks_permission
from blogs_be.users.tests.factories import UserFactory


class TestUpdateBlogPostApiView:
    @pytest.fixture()
    def api_client(self):
        return APIClient()

    @pytest.fixture()
    def blog_owner(self):
        return UserFactory()

    @pytest.fixture()
    def blog(self, blog_owner):
        return BlogFactory(
            owner=blog_owner, name="Original blog", description="Original description"
        )

    @pytest.fixture()
    def blog_post(self, blog):
        return BlogPostFactory(
            blog=blog, title="Original blog-post", content="Original content"
        )

    @pytest.mark.django_db()
    def test_update_blog_post_api_view_success(
        self, api_client, blog, blog_owner, blog_post
    ):
        # Given
        api_client.force_authenticate(user=blog_owner)
        url = reverse(
            "update-blog-post",
            kwargs=dict(blog_key=blog.id, blog_post_key=blog_post.id),
        )

        # When
        response = api_client.post(
            url,
            data=dict(
                update_blog_post_form=dict(
                    title="Updated title",
                    content="Updated content",
                )
            ),
        )

        # Then
        assert response.status_code == 200

        result = response.json()
        diff = deepdiff.DeepDiff(
            {
                "id": str(blog_post.id),
                "title": "Updated title",
                "slug": "original-blog-post",
                "content": "Updated content",
                "blog_id": str(blog.id),
            },
            result,
            custom_operators=[],
        )
        assert not diff, f"JSON response differs: {diff.pretty()}"

    def test_update_blog_post_api_view_permissions(self):
        assert checks_permission(UpdateBlogPostApiView.post, user_is_blog_owner)
