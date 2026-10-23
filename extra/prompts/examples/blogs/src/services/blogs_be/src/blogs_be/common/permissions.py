from blogs_be.api.utils.extend_schema import allow, deny


def user_is_authenticated(user):
    if not user.is_authenticated:
        return deny("Not authenticated")
    return allow()
