from django.db import models

from blogs_be.blogs.enums import Audiences, BlogPostLevels
from blogs_be.common.fields import SingleLineTextField
from blogs_be.common.models import BaseModel
from django.utils.text import slugify


class Blog(BaseModel):
    name = SingleLineTextField()
    slug = SingleLineTextField()
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="blogs"
    )
    audience = models.TextField(choices=Audiences.choices, default=Audiences.ANY)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "-":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(BaseModel):
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

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "-":
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
