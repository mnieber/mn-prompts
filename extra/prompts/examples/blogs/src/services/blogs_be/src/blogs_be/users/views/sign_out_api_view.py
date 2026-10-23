from blogs_be.api.utils.extend_schema import extend_schema
import logging

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.common.permissions import user_is_authenticated
from blogs_be.users.actions.block_token import block_token
from blogs_be.users.utils.parse_access_token_or_401 import parse_access_token_or_401
from blogs_be.users.utils.parse_refresh_token_or_401 import parse_refresh_token_or_401

logger = logging.getLogger(__name__)


class SignOutSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class SignOutApiView(APIView):
    serializer_class = SignOutSerializer

    @extend_schema(
        request=SignOutSerializer,
        responses={status.HTTP_205_RESET_CONTENT: None},
        permissions=[
            (
                status.HTTP_401_UNAUTHORIZED,
                user_is_authenticated,
                "You must be authenticated to sign out.",
            )
        ],
    )
    def post(self, request):
        serializer = SignOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access_token = parse_access_token_or_401(serializer.validated_data["access"])
        refresh_token = parse_refresh_token_or_401(serializer.validated_data["refresh"])

        refresh_token.blacklist()
        block_token(access_token["jti"])
        return Response(status=status.HTTP_205_RESET_CONTENT)
