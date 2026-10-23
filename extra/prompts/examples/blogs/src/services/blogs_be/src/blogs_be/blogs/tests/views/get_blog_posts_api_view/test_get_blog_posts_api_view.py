import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blogs_be.blogs.tests.factories import BlogFactory, BlogPostFactory
from blogs_be.users.tests.factories import UserFactory


class TestGetBlogPostsApiView:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture()
    def blog_owner(self):
        return UserFactory()

    @pytest.mark.django_db
    def test_get_blog_posts_api_view_success(self, api_client, blog_owner):
        blog = BlogFactory(owner=blog_owner)
        BlogPostFactory.create_batch(3, blog=blog)
        url = reverse("get-blog-posts", kwargs=dict(blog_key=blog.slug))

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
