# Skill: dj-write-permissions

Applies when writing a `permissions.py` file for a Django app module.

Primary reference: `blogs_be/src/blogs_be/blogs/permissions.py`

---

## File location

```
<module>/permissions.py
```

## Pattern

Permission functions are plain Python functions — not DRF `BasePermission` subclasses. They return the result of calling `allow()` or `deny(reason)` (both imported from `api.utils.extend_schema`).

```python
from blogs_be.api.utils.extend_schema import allow, deny


def user_is_blog_owner(user, blog):
    if blog.owner_id != user.id:
        return deny("User must be the blog owner")
    return allow()
```

## Argument resolution

Permission function arguments are resolved from the view's data spec by name. In the example above, `user` and `blog` must be keys present in the data dict built by the view's `data=` resolver. The runtime matches argument names to data spec keys automatically.

## Wiring into a view

Permissions are declared in the view's `@extend_schema` decorator:

```python
permissions=[
    (403, user_is_blog_owner, "You must be the blog owner to create a blog post."),
]
```

Each entry is `(http_status_code, permission_fn, user_facing_message)`.

RULE: A public endpoint uses `permissions=[]`, not a permission function that always returns `allow()`.

## Checklist

- [ ] Permission function returns `allow()` or `deny(reason)`
- [ ] Function arguments match keys in the view's data spec
- [ ] Function is referenced in the view's `permissions=` list with status code and message
- [ ] Public endpoints use `permissions=[]`
