import typing as T

from blogs_be.blogs.models import Blog
from blogs_be.blogs.rules.has_forbidden_words import has_forbidden_words
from blogs_be.common.utils.dataclass import dataclass
from django.contrib.auth import get_user_model

from blogs_be.common.utils.arg_utils import optional_args

User = get_user_model()


@dataclass
class CreateBlogForm:
    name: str
    description: T.Optional[str] = None


def create_blog(create_blog_form: CreateBlogForm, owner: User):
    _validate_args(create_blog_form)

    blog = Blog(
        name=create_blog_form.name,
        owner=owner,
        **optional_args(description=create_blog_form.description)
    )
    blog.save()

    return blog


def _validate_args(create_blog_form: CreateBlogForm):
    if Blog.objects.filter(name=create_blog_form.name).exists():
        raise BlogWithNameAlreadyExistsError()

    if has_forbidden_words(create_blog_form.name):
        raise CreateBlogFormContainsForbiddenWordsError("name")

    if create_blog_form.description and has_forbidden_words(
        create_blog_form.description
    ):
        raise CreateBlogFormContainsForbiddenWordsError("description")


class BlogWithNameAlreadyExistsError(Exception):
    pass


class CreateBlogFormContainsForbiddenWordsError(ValueError):
    pass
