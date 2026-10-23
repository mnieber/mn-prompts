from blogs_be.blogs.actions.create_blog_post import (
    BlogPostWithTitleAlreadyExistsError,
    CreateBlogPostFormContainsForbiddenWordsError,
    create_blog_post,
)
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.serializers import BlogPostSerializer, CreateBlogPostFormSerializer
from blogs_be.blogs.shortcuts import get_blog_or_400
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.common.form_serializer import FormSerializer


class CreateBlogPostRequestSerializer(FormSerializer):
    create_blog_post_form = CreateBlogPostFormSerializer()


class CreateBlogPostApiView(APIView):
    @extend_schema(
        request=CreateBlogPostRequestSerializer,
        responses={
            200: BlogPostSerializer,
        },
        data=dict(
            blog=get_blog_or_400,
        ),
        permissions=[
            (
                403,
                user_is_blog_owner,
                "You must be the blog owner to create a blog post.",
            ),
        ],
    )
    def post(self, request, request_data, blog):
        try:
            blog_post = create_blog_post(
                create_blog_post_form=request_data.create_blog_post_form,
                blog=blog,
            )
        except BlogPostWithTitleAlreadyExistsError:
            raise ValidationError(code="BLOG_POST_TITLE_ALREADY_EXISTS")
        except CreateBlogPostFormContainsForbiddenWordsError as e:
            raise ValidationError(code="FORM_CONTAINS_FORBIDDEN_WORDS", detail=str(e))

        return Response(
            BlogPostSerializer(blog_post).data, status=status.HTTP_201_CREATED
        )
