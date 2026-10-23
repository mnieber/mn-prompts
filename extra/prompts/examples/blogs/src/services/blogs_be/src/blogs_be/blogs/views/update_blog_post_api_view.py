from blogs_be.blogs.actions.update_blog_post import (
    BlogPostWithTitleAlreadyExistsError,
    update_blog_post,
)
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.serializers import BlogPostSerializer, UpdateBlogPostFormSerializer
from blogs_be.blogs.shortcuts import get_blog_post_or_400
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.common.form_serializer import FormSerializer


class UpdateBlogPostRequestSerializer(FormSerializer):
    update_blog_post_form = UpdateBlogPostFormSerializer()


class UpdateBlogPostApiView(APIView):
    @extend_schema(
        request=UpdateBlogPostRequestSerializer,
        responses={
            200: BlogPostSerializer,
        },
        data=dict(
            blog_post=get_blog_post_or_400,
            blog=lambda blog_post: blog_post.blog,
        ),
        permissions=[
            (
                403,
                user_is_blog_owner,
                "You must be the blog owner to update the blog post.",
            ),
        ],
    )
    def post(self, request, request_data, blog_post):
        try:
            updated_blog_post = update_blog_post(
                update_blog_post_form=request_data.update_blog_post_form,
                blog_post=blog_post,
            )
        except BlogPostWithTitleAlreadyExistsError:
            raise ValidationError(code="BLOG_WITH_THIS_TITLE_ALREADY_EXISTS")

        return Response(
            BlogPostSerializer(updated_blog_post).data, status=status.HTTP_200_OK
        )
