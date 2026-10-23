from blogs_be.api.utils.extend_schema import extend_schema
import logging

from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings as jwt_api_settings
from rest_framework_simplejwt.views import TokenRefreshView

from blogs_be.users.actions.block_token import block_token
from blogs_be.users.utils.parse_access_token_or_401 import parse_access_token_or_401
from blogs_be.users.utils.parse_refresh_token_or_401 import parse_refresh_token_or_401
from blogs_be.users.models import User

logger = logging.getLogger(__name__)


class RefreshTokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class RefreshTokenApiView(TokenRefreshView):
    @extend_schema(
        request=RefreshTokenSerializer, responses={200: None}, permissions=[]
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prev_access_token = parse_access_token_or_401(
            serializer.validated_data["access"],
            verify=False,  # we need the jti even if the token expired
        )
        refresh_token = parse_refresh_token_or_401(serializer.validated_data["refresh"])

        user_id = refresh_token[jwt_api_settings.USER_ID_CLAIM]
        user = User.objects.filter(pk=user_id).first()
        if not user or user.is_anonymous:
            raise serializers.ValidationError(code="USER_NOT_FOUND")

        response = super().post(request)

        # The base-class implementation of the post method returns a Response object
        # that still has the access token that comes from the previous refresh token.
        # However, we want to block that token. Therefore, we swap the access token
        # with the one that is related to the new refresh token.
        response.data["access"] = str(refresh_token.access_token)

        if response.status_code == 200:
            block_token(prev_access_token["jti"])
        return response
