import factory
from blogs_be.blogs.models import Blog, BlogPost
from factory.django import DjangoModelFactory


class BlogFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Blog{n}")
    description = "Some description"

    class Meta:
        model = Blog


class BlogPostFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f"BlogPost{n}")
    content = "Some content"

    class Meta:
        model = BlogPost
