# Skill: dj-write-shortcuts

Applies when writing a `shortcuts.py` file for a Django app module.

Primary reference: `blogs_be/src/blogs_be/blogs/shortcuts.py`

---

## File location

```
<module>/shortcuts.py
```

## What are shortcuts?

Shortcuts are small helper functions that look up a model instance (or perform another common query) and raise a `ValidationError` if the lookup fails. They are designed to be used as resolver functions in the view's `data=` spec.

## Pattern

```python
from blogs_be.blogs.models import Blog, BlogPost
from rest_framework.exceptions import ValidationError
from blogs_be.common.utils.ids import is_uuid


def get_blog_or_400(blog_key):
    kwargs = {"pk" if is_uuid(blog_key) else "slug": blog_key}

    blog = Blog.objects.filter(**kwargs).first()
    if not blog:
        raise ValidationError(code="BLOG_NOT_FOUND")

    return blog


def get_blog_post_or_400(blog_post_key):
    kwargs = {"pk" if is_uuid(blog_post_key) else "slug": blog_post_key}

    blog_post = BlogPost.objects.filter(**kwargs).first()
    if not blog_post:
        raise ValidationError(code="BLOG_POST_NOT_FOUND")

    return blog_post
```

RULE: Shortcut functions use `is_uuid` (from `common.utils.ids`) to determine whether the key is a UUID (look up by `pk`) or a slug (look up by `slug`). This lets callers use either format interchangeably.

RULE: On failure, raise `ValidationError(code="RESOURCE_NOT_FOUND")`. Use `SCREAMING_SNAKE_CASE` for the error code string.

RULE: Shortcut functions take the raw URL parameter value (a string) as their only argument, matching how they are registered in the view's `data=` dict.

## Checklist

- [ ] File lives at `<module>/shortcuts.py`
- [ ] Uses `is_uuid` to support both UUID and slug lookups
- [ ] Raises `ValidationError(code=...)` when the object is not found
- [ ] Function signature matches the URL parameter name used in the view's `data=` dict
