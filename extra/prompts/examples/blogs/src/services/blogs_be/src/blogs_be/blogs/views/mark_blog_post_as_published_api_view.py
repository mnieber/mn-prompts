from blogs_be.blogs.actions.mark_blog_post_as_published import (
    mark_blog_post_as_published,
)
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.serializers import BlogPostSerializer
from blogs_be.blogs.shortcuts import get_blog_or_400, get_blog_post_or_400
from blogs_be.common.serializers import EmptySerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.api.utils.extend_schema import extend_schema


class MarkBlogPostAsPublishedApiView(APIView):
    @extend_schema(
        request=EmptySerializer,
        responses={
            200: BlogPostSerializer,
        },
        data=dict(
            blog=get_blog_or_400,
            blog_post=get_blog_post_or_400,
        ),
        permissions=[
            (
                403,
                user_is_blog_owner,
                "You must be the blog owner to publish the blog post.",
            ),
        ],
    )
    def post(self, request, request_data, blog_post):
        return Response(
            BlogPostSerializer(mark_blog_post_as_published(blog_post)).data,
            status=status.HTTP_200_OK,
        )
