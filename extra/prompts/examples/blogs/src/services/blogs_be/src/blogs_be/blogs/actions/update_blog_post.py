import typing as T

from blogs_be.blogs.models import BlogPost
from blogs_be.common.utils.dataclass import dataclass
from blogs_be.blogs.rules.has_forbidden_words import has_forbidden_words


@dataclass
class UpdateBlogPostForm:
    title: T.Optional[str] = None
    content: T.Optional[str] = None


def update_blog_post(update_blog_post_form: UpdateBlogPostForm, blog_post: BlogPost):
    _validate_args(update_blog_post_form, blog_post)

    update_fields = []
    if update_blog_post_form.title is not None:
        blog_post.title = update_blog_post_form.title
        update_fields.append("title")
    if update_blog_post_form.content is not None:
        blog_post.content = update_blog_post_form.content
        update_fields.append("content")

    blog_post.save(update_fields=update_fields)

    return blog_post


def _validate_args(update_blog_post_form: UpdateBlogPostForm, blog_post: BlogPost):
    if (
        update_blog_post_form.title
        and BlogPost.objects.filter(
            title=update_blog_post_form.title, blog=blog_post.blog
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


class BlogPostWithTitleAlreadyExistsError(Exception):
    pass


class UpdateBlogPostFormContainsForbiddenWordsError(ValueError):
    pass
