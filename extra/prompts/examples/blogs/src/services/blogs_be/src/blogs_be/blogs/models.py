from django.db import models

from blogs_be.blogs.enums import Audiences, BlogPostLevels
from blogs_be.common.fields import SingleLineTextField
from blogs_be.common.models import BaseModel


class Blog(BaseModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["slug"], name="unique_blog_slug"),
        ]

    name = SingleLineTextField()
    slug = SingleLineTextField()
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="blogs"
    )
    audience = models.TextField(choices=Audiences.choices, default=Audiences.ANY)

    def __str__(self):
        return self.name


class BlogPost(BaseModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["blog", "slug"], name="unique_blog_post_slug_per_blog"
            ),
        ]

    blog = models.ForeignKey(
        "blogs.Blog", on_delete=models.CASCADE, related_name="blog_posts"
    )
    title = SingleLineTextField()
    slug = SingleLineTextField()
    content = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    level = models.TextField(
        choices=BlogPostLevels.choices, default=BlogPostLevels.MEDIUM
    )

    def __str__(self):
        return self.title
