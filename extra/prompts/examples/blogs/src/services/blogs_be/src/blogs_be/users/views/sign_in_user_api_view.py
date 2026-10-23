from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.common.form_serializer import FormSerializer
from blogs_be.users.actions.sign_in_user import (
    AccountIsNotActiveError,
    InvalidCredentialsError,
    sign_in_user,
)
from blogs_be.users.serializers import SignInUserFormSerializer
from blogs_be.common.serializers import WriteSerializerMixin


class SignInUserRequestSerializer(FormSerializer):
    sign_in_user_form = SignInUserFormSerializer()


class SignInUserResponseSerializer(WriteSerializerMixin, serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user_id = serializers.CharField()


class SignInUserApiView(APIView):
    @extend_schema(
        request=SignInUserRequestSerializer,
        responses={
            200: SignInUserResponseSerializer,
        },
        data=dict(),
        permissions=[],
    )
    def post(self, request, request_data):
        try:
            action_result_dict = sign_in_user(request_data.sign_in_user_form)
            response_serializer = SignInUserResponseSerializer(
                data=dict(
                    **action_result_dict, user_id=request_data.sign_in_user_form.email
                )
            )
            response_serializer.is_valid(raise_exception=True)
            response_data = response_serializer.validated_data
        except InvalidCredentialsError:
            raise ValidationError(code="INVALID_CREDENTIALS")
        except AccountIsNotActiveError:
            raise ValidationError(code="INACTIVE_ACCOUNT")

        return Response(response_data, status=status.HTTP_200_OK)
