import pytest
from blogs_be.blogs.tests.factories import BlogFactory

from blogs_be.users.tests.factories import UserFactory

from blogs_be.blogs.actions.create_blog import (  # isort: skip noqa: F401
    BlogWithNameAlreadyExistsError,
    CreateBlogFormContainsForbiddenWordsError,
    CreateBlogForm,
    create_blog,
)


class TestCreateBlogAction:
    @pytest.fixture()
    def blog_owner(self):
        return UserFactory()

    @pytest.mark.django_db
    def test_create_blog_action_success(self, blog_owner):
        # Given
        create_blog_form = CreateBlogForm(name="Test Blog", description="A test blog")

        # When
        blog = create_blog(create_blog_form, owner=blog_owner)

        # Then
        assert blog.name == "Test Blog"
        assert blog.description == "A test blog"

    @pytest.mark.django_db
    def test_create_blog_action_with_existing_name(self, blog_owner):
        # Given
        BlogFactory(name="Existing Blog", owner=blog_owner)

        create_blog_form = CreateBlogForm(
            name="Existing Blog", description="A test blog"
        )

        # When / Then
        with pytest.raises(BlogWithNameAlreadyExistsError):
            create_blog(create_blog_form, owner=blog_owner)

    @pytest.mark.django_db
    def test_create_blog_action_with_forbidden_words(self, blog_owner):
        # Given
        BlogFactory(name="Existing Blog", owner=blog_owner)

        create_blog_form = CreateBlogForm(
            name="Another Blog", description="A forbidden blog"
        )

        # When / Then
        with pytest.raises(CreateBlogFormContainsForbiddenWordsError):
            create_blog(create_blog_form, owner=blog_owner)
