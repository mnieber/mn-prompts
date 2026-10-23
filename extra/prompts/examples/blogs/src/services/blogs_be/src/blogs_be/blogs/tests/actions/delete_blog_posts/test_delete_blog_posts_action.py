import pytest
from blogs_be.users.tests.factories import UserFactory
from uuid import uuid4
from blogs_be.blogs.actions.delete_blog_posts import (
    delete_blog_posts,
    DeleteBlogPostsForm,
)
from blogs_be.blogs.models import BlogPost
from blogs_be.blogs.tests.factories import BlogFactory, BlogPostFactory
from blogs_be.blogs.actions.delete_blog_posts import BlogPostsNotFoundError


class TestDeleteBlogPostsAction:
    @pytest.fixture
    def blog_owner(self):
        return UserFactory()

    @pytest.mark.django_db
    def test_delete_blog_posts_action_success(self, blog_owner):
        # Given
        blog = BlogFactory(owner=blog_owner)
        blog_posts = BlogPostFactory.create_batch(3, blog=blog)
        form = DeleteBlogPostsForm(blog_post_ids=[str(post.id) for post in blog_posts])

        # When
        deleted_count = delete_blog_posts(form, blog=blog)

        # Then
        assert deleted_count == 3
        assert BlogPost.objects.count() == 0

    @pytest.mark.django_db
    def test_delete_blog_posts_action_not_found(self, blog_owner):
        # Given
        blog = BlogFactory(owner=blog_owner)
        blog_posts = BlogPostFactory.create_batch(3, blog=blog)
        non_existent_id = str(uuid4())
        form = DeleteBlogPostsForm(
            blog_post_ids=[str(blog_posts[0].id), non_existent_id]
        )

        # When
        with pytest.raises(BlogPostsNotFoundError):
            delete_blog_posts(form, blog=blog)

        # Then
        assert BlogPost.objects.count() == 3
