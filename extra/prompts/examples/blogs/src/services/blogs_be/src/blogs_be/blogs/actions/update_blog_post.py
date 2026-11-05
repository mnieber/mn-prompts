import typing as T

from blogs_be.blogs.enums import BlogPostLevels
from blogs_be.blogs.models import BlogPost
from blogs_be.common.utils.dataclass import dataclass
from blogs_be.blogs.rules.has_forbidden_words import has_forbidden_words
from django.conf import settings


@dataclass
class UpdateBlogPostForm:
    title: T.Optional[str] = None
    content: T.Optional[str] = None
    level: T.Optional[BlogPostLevels] = None


def update_blog_post(update_blog_post_form: UpdateBlogPostForm, blog_post: BlogPost):
    _validate_args(update_blog_post_form, blog_post)

    update_fields = []
    if update_blog_post_form.title is not None:
        blog_post.title = update_blog_post_form.title
        update_fields.append("title")
    if update_blog_post_form.content is not None:
        blog_post.content = update_blog_post_form.content
        update_fields.append("content")
    if update_blog_post_form.level:
        blog_post.level = update_blog_post_form.level
        update_fields.append("level")

    blog_post.save(update_fields=update_fields)

    return blog_post


def _validate_args(update_blog_post_form: UpdateBlogPostForm, blog_post: BlogPost):
    if (
        update_blog_post_form.title is not None
        and not update_blog_post_form.title.strip()
    ):
        raise BlogPostTitleBlankError()

    if (
        update_blog_post_form.title
        and len(update_blog_post_form.title) > settings.MAX_NAME_LENGTH
    ):
        raise BlogPostTitleTooLongError()

    if (
        update_blog_post_form.title
        and BlogPost.objects.filter(
            title__iexact=update_blog_post_form.title, blog=blog_post.blog
        )
        .exclude(id=blog_post.id)
        .exists()
    ):
        raise BlogPostWithTitleAlreadyExistsError()

    if update_blog_post_form.title and has_forbidden_words(update_blog_post_form.title):
        raise UpdateBlogPostFormContainsForbiddenWordsError("title")

    if update_blog_post_form.content and has_forbidden_words(
        update_blog_post_form.content
    ):
        raise UpdateBlogPostFormContainsForbiddenWordsError("content")


class BlogPostTitleBlankError(Exception):
    pass


class BlogPostTitleTooLongError(Exception):
    pass


class BlogPostWithTitleAlreadyExistsError(Exception):
    pass


class UpdateBlogPostFormContainsForbiddenWordsError(ValueError):
    pass
