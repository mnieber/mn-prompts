import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blogs_be.blogs.tests.factories import BlogFactory, BlogPostFactory
from blogs_be.users.tests.factories import UserFactory


class TestDeleteBlogPostsApiView:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def blog_owner(self):
        return UserFactory()

    @pytest.mark.django_db
    def test_delete_blog_posts_view_success(self, api_client, blog_owner):
        api_client.force_authenticate(user=blog_owner)
        blog = BlogFactory(owner=blog_owner)
        blog_posts = BlogPostFactory.create_batch(3, blog=blog)
        url = reverse("delete-blog-posts", kwargs=dict(blog_key=blog.slug))
        data = {
            "delete_blog_posts_form": {
                "blog_post_ids": [str(post.id) for post in blog_posts]
            }
        }

        response = api_client.post(url, data, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["deleted_count"] == 3
        assert blog.blog_posts.count() == 0
