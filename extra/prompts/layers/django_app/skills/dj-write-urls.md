# Skill: dj-write-urls

Applies when writing a `urls.py` file for a Django app module.

Primary reference: `blogs_be/src/blogs_be/blogs/urls.py`

---

## File location

```
<module>/urls.py
```

## Pattern

Import each view class from its own view file, then list all URL patterns in `urlpatterns`:

```python
from blogs_be.blogs.views.create_blog_api_view import CreateBlogApiView
from blogs_be.blogs.views.create_blog_post_api_view import CreateBlogPostApiView
from blogs_be.blogs.views.get_blogs_api_view import GetBlogsApiView
from django.urls import path


urlpatterns = [
    path(
        "create/",
        CreateBlogApiView.as_view(),
        name="create-blog",
    ),
    path(
        "<str:blog_key>/blog-posts/create/",
        CreateBlogPostApiView.as_view(),
        name="create-blog-post",
    ),
    path(
        "<str:blog_key>/blog-posts/list/",
        GetBlogsApiView.as_view(),
        name="get-blog-posts",
    ),
]
```

RULE: Each `path()` call must have a `name=` argument. Use kebab-case names (e.g. `"create-blog-post"`).

RULE: URL path parameters that identify a resource use the `<str:resource_key>` convention (e.g. `<str:blog_key>`). The resolver function in the view's `data=` spec receives this parameter by name.

## URL naming conventions

- Action endpoints: `<verb>-<resource>` (e.g. `create-blog`, `delete-blog-posts`)
- Query endpoints: `get-<resource>` (e.g. `get-blogs`, `get-blog-posts`)

## Checklist

- [ ] Each view is imported from its own view file
- [ ] Every `path()` has a `name=` in kebab-case
- [ ] Path parameters follow `<str:resource_key>` convention
