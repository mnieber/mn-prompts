import typing as T

from blogs_be.blogs.models import Blog, BlogPost
from dataclassy import dataclass
from blogs_be.blogs.rules.has_forbidden_words import has_forbidden_words

from blogs_be.common.utils.arg_utils import optional_args


@dataclass
class CreateBlogPostForm:
    title: str
    content: T.Optional[str] = None


def create_blog_post(create_blog_post_form: CreateBlogPostForm, blog: Blog):
    _validate_args(create_blog_post_form, blog)

    blog_post = BlogPost(
        blog=blog,
        title=create_blog_post_form.title,
        **optional_args(content=create_blog_post_form.content)
    )
    blog_post.save()

    return blog_post


def _validate_args(create_blog_post_form: CreateBlogPostForm, blog: Blog):
    if BlogPost.objects.filter(title=create_blog_post_form.title, blog=blog).exists():
        raise BlogPostWithTitleAlreadyExistsError()

    if has_forbidden_words(create_blog_post_form.title):
        raise CreateBlogPostFormContainsForbiddenWordsError("title")

    if create_blog_post_form.content and has_forbidden_words(
        create_blog_post_form.content
    ):
        raise CreateBlogPostFormContainsForbiddenWordsError("content")


class BlogPostWithTitleAlreadyExistsError(Exception):
    pass


class CreateBlogPostFormContainsForbiddenWordsError(ValueError):
    pass
