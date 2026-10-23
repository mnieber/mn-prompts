from blogs_be.blogs.models import Blog, BlogPost
from django_filters import rest_framework as filters


class BlogFilterSet(filters.FilterSet):
    sort = filters.OrderingFilter(
        fields=[
            "name",
        ]
    )

    class Meta:
        model = Blog
        fields = {
            "audience": ["exact"],
            "slug": ["exact"],
        }


class BlogPostFilterSet(filters.FilterSet):
    sort = filters.OrderingFilter(
        fields=[
            "title",
        ]
    )

    class Meta:
        model = BlogPost
        fields = {
            "is_published": ["exact"],
            "slug": ["exact"],
        }
