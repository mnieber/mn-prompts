import factory
from blogs_be.blogs.models import Blog, BlogPost
from django.utils.text import slugify
from factory.django import DjangoModelFactory


class BlogFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Blog{n}")
    slug = factory.LazyAttribute(lambda x: slugify(x.name))
    description = "Some description"

    class Meta:
        model = Blog


class BlogPostFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f"BlogPost{n}")
    slug = factory.LazyAttribute(lambda x: slugify(x.title))
    content = "Some content"

    class Meta:
        model = BlogPost
