from blogs_be.api.utils.extend_schema import allow, deny


def user_is_blog_owner(user, blog):
    if blog.owner_id != user.id:
        return deny("User must be the blog owner")
    return allow()
