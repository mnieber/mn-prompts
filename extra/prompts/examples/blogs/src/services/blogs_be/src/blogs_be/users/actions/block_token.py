from blogs_be.users.models import BlockedToken


def block_token(jti):
    BlockedToken.objects.get_or_create(jti=jti)
