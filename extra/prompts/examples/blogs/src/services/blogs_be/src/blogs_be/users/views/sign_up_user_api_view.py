from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.common.form_serializer import FormSerializer
from blogs_be.users.actions.create_user import (
    PasswordsDoNotMatchError,
    UserWithEmailAlreadyExistsError,
    create_user,
)
from blogs_be.users.serializers import CreateUserFormSerializer, UserSerializer


class SignUpUserRequestSerializer(FormSerializer):
    create_user_form = CreateUserFormSerializer()


class SignUpUserApiView(APIView):
    @extend_schema(
        request=SignUpUserRequestSerializer,
        responses={
            201: UserSerializer,
        },
        data=dict(),
        permissions=[],
    )
    def post(self, request, request_data):
        try:
            user = create_user(request_data.create_user_form, is_active=True)
        except UserWithEmailAlreadyExistsError:
            raise ValidationError(code="USER_EMAIL_ALREADY_EXISTS")
        except PasswordsDoNotMatchError:
            raise ValidationError(code="PASSWORDS_DO_NOT_MATCH")

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
