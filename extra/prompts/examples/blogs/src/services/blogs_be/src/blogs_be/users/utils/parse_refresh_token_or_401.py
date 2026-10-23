import logging

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


def parse_refresh_token_or_401(refresh_token_str):
    try:
        return RefreshToken(refresh_token_str)
    except TokenError as e:
        logger.info(f"Failed to parse refresh token: {e}")
        raise AuthenticationFailed()
