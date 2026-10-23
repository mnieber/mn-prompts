from blogs_be.blogs.models import Blog, BlogPost
from rest_framework.exceptions import ValidationError
from blogs_be.common.utils.ids import is_uuid


def get_blog_or_400(blog_key):
    kwargs = {"pk" if is_uuid(blog_key) else "slug": blog_key}

    blog = Blog.objects.filter(**kwargs).first()
    if not blog:
        raise ValidationError(code="BLOG_NOT_FOUND")

    return blog


def get_blog_post_or_400(blog_post_key):
    kwargs = {"pk" if is_uuid(blog_post_key) else "slug": blog_post_key}

    blog_post = BlogPost.objects.filter(**kwargs).first()
    if not blog_post:
        raise ValidationError(code="BLOG_POST_NOT_FOUND")

    return blog_post
