import pytest
from blogs_be.blogs.tests.factories import BlogFactory, BlogPostFactory

from blogs_be.blogs.actions.update_blog_post import (
    BlogPostWithTitleAlreadyExistsError,
    UpdateBlogPostFormContainsForbiddenWordsError,
    UpdateBlogPostForm,
    update_blog_post,
)
from blogs_be.users.tests.factories import UserFactory


class TestUpdateBlogPostAction:
    @pytest.fixture()
    def blog_owner(self):
        return UserFactory()

    @pytest.fixture()
    def blog(self, blog_owner):
        return BlogFactory(name="My Blog", description="Foo", owner=blog_owner)

    @pytest.fixture()
    def blog_post(self, blog):
        return BlogPostFactory(
            title="Original title", content="Original content", blog=blog
        )

    @pytest.mark.django_db
    def test_update_blog_post_action_success(self, blog_post):
        # Given
        update_blog_post_form = UpdateBlogPostForm(
            title="Updated Title", content="Updated content"
        )

        # When
        updated_blog_post = update_blog_post(update_blog_post_form, blog_post=blog_post)

        # Then
        assert updated_blog_post.title == "Updated Title"
        assert updated_blog_post.content == "Updated content"

    @pytest.mark.django_db
    def test_update_blog_post_action_partial_update(self, blog_post):
        # Given
        update_blog_post_form = UpdateBlogPostForm(title="Updated Title")

        # When
        updated_blog_post = update_blog_post(update_blog_post_form, blog_post=blog_post)

        # Then
        assert updated_blog_post.title == "Updated Title"
        assert updated_blog_post.content == "Original content"

    @pytest.mark.django_db
    def test_update_blog_post_action_with_existing_title(self, blog, blog_post):
        # Given
        BlogPostFactory(title="Existing Blog-post", blog=blog)
        update_blog_post_form = UpdateBlogPostForm(title="Existing Blog-post")

        # When / Then
        with pytest.raises(BlogPostWithTitleAlreadyExistsError):
            update_blog_post(update_blog_post_form, blog_post=blog_post)

    @pytest.mark.django_db
    def test_update_blog_post_action_with_forbidden_words(self, blog, blog_post):
        # Given
        BlogPostFactory(title="Existing Blog-post", blog=blog)
        update_blog_post_form = UpdateBlogPostForm(title="Forbidden Blog-post")

        # When / Then
        with pytest.raises(UpdateBlogPostFormContainsForbiddenWordsError):
            update_blog_post(update_blog_post_form, blog_post=blog_post)

    @pytest.mark.django_db
    def test_update_blog_post_action_no_changes(self, blog_post):
        # Given
        update_blog_post_form = UpdateBlogPostForm()

        # When
        updated_blog_post = update_blog_post(update_blog_post_form, blog_post=blog_post)

        # Then
        assert updated_blog_post.title == "Original title"
        assert updated_blog_post.content == "Original content"
