import logging

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger(__name__)


def parse_access_token_or_401(access_token_str, verify: bool = True):
    try:
        return AccessToken(access_token_str, verify=verify)
    except TokenError as e:
        logger.info(f"Failed to parse access token: {e}")
        raise AuthenticationFailed()
