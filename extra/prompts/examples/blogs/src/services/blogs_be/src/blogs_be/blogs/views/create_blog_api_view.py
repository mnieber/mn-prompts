from blogs_be.blogs.actions.create_blog import (
    create_blog,
    BlogWithNameAlreadyExistsError,
    CreateBlogFormContainsForbiddenWordsError,
)
from blogs_be.blogs.serializers import BlogSerializer, CreateBlogFormSerializer
from blogs_be.common.permissions import user_is_authenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.common.form_serializer import FormSerializer


class CreateBlogRequestSerializer(FormSerializer):
    create_blog_form = CreateBlogFormSerializer()


class CreateBlogApiView(APIView):
    @extend_schema(
        request=CreateBlogRequestSerializer,
        responses={
            200: BlogSerializer,
        },
        data=dict(),
        permissions=[(status.HTTP_401_UNAUTHORIZED, user_is_authenticated)],
    )
    def post(self, request, request_data):
        try:
            blog = create_blog(
                create_blog_form=request_data.create_blog_form,
                owner=request.user,
            )
        except BlogWithNameAlreadyExistsError:
            raise ValidationError(code="BLOG_NAME_ALREADY_EXISTS")
        except CreateBlogFormContainsForbiddenWordsError as e:
            raise ValidationError(code="FORM_CONTAINS_FORBIDDEN_WORDS", detail=str(e))

        return Response(BlogSerializer(blog).data, status=status.HTTP_201_CREATED)
