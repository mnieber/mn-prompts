from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import (
    JWTAuthentication as OriginalJWTAuthentication,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from blogs_be.users.models import BlockedToken


class JWTAuthentication(OriginalJWTAuthentication):
    def authenticate(self, request):
        raw_token = self.get_raw_token(self.get_header(request) or "")
        if not raw_token:
            return None

        try:
            token = AccessToken(raw_token)
        except TokenError:
            raise AuthenticationFailed("Invalid token")

        if BlockedToken.objects.filter(jti=token.get("jti")).exists():
            raise AuthenticationFailed("Invalid token")

        user = super().authenticate(request)
        if user is None:
            return None

        return user


class JWTAuthenticationScheme(SimpleJWTScheme):
    target_class = "api.auth.JWTAuthentication"
