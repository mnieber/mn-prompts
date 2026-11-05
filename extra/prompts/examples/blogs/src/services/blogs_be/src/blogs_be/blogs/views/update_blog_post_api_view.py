from blogs_be.blogs.actions.update_blog_post import (
    BlogPostTitleBlankError,
    BlogPostTitleTooLongError,
    BlogPostWithTitleAlreadyExistsError,
    UpdateBlogPostFormContainsForbiddenWordsError,
    update_blog_post,
)
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.serializers import BlogPostSerializer, UpdateBlogPostFormSerializer
from blogs_be.blogs.shortcuts import get_blog_or_400, get_blog_post_or_400
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
            blog=get_blog_or_400,
            blog_post=get_blog_post_or_400,
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
        except BlogPostTitleBlankError:
            raise ValidationError(code="BLOG_POST_TITLE_BLANK")
        except BlogPostTitleTooLongError:
            raise ValidationError(code="BLOG_POST_TITLE_TOO_LONG")
        except BlogPostWithTitleAlreadyExistsError:
            raise ValidationError(code="BLOG_POST_TITLE_ALREADY_EXISTS")
        except UpdateBlogPostFormContainsForbiddenWordsError as e:
            raise ValidationError(code="FORM_CONTAINS_FORBIDDEN_WORDS", detail=str(e))

        return Response(
            BlogPostSerializer(updated_blog_post).data, status=status.HTTP_200_OK
        )
