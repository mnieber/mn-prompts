import typing as T

from blogs_be.blogs.enums import BlogPostLevels
from blogs_be.blogs.models import Blog, BlogPost
from blogs_be.common.utils.dataclass import dataclass
from blogs_be.blogs.rules.generate_unique_slug import generate_unique_slug
from blogs_be.blogs.rules.has_forbidden_words import has_forbidden_words
from django.conf import settings

from blogs_be.common.utils.arg_utils import optional_args


@dataclass
class CreateBlogPostForm:
    title: str
    content: T.Optional[str] = None
    level: T.Optional[BlogPostLevels] = None


def create_blog_post(create_blog_post_form: CreateBlogPostForm, blog: Blog):
    _validate_args(create_blog_post_form, blog)

    blog_post = BlogPost(
        blog=blog,
        title=create_blog_post_form.title,
        slug=generate_unique_slug(
            create_blog_post_form.title,
            fallback="post",
            taken_slugs=set(
                BlogPost.objects.filter(blog=blog).values_list("slug", flat=True)
            ),
        ),
        **optional_args(
            content=create_blog_post_form.content,
            level=create_blog_post_form.level or None,
        )
    )
    blog_post.save()

    return blog_post


def _validate_args(create_blog_post_form: CreateBlogPostForm, blog: Blog):
    if len(create_blog_post_form.title) > settings.MAX_NAME_LENGTH:
        raise BlogPostTitleTooLongError()

    if BlogPost.objects.filter(
        title__iexact=create_blog_post_form.title, blog=blog
    ).exists():
        raise BlogPostWithTitleAlreadyExistsError()

    if has_forbidden_words(create_blog_post_form.title):
        raise CreateBlogPostFormContainsForbiddenWordsError("title")

    if create_blog_post_form.content and has_forbidden_words(
        create_blog_post_form.content
    ):
        raise CreateBlogPostFormContainsForbiddenWordsError("content")


class BlogPostTitleTooLongError(Exception):
    pass


class BlogPostWithTitleAlreadyExistsError(Exception):
    pass


class CreateBlogPostFormContainsForbiddenWordsError(ValueError):
    pass
