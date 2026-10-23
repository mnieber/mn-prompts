# Skill: dj-write-api-view

Applies when writing an API view file inside a `views/` subdirectory.

Primary references:
- `blogs_be/src/blogs_be/blogs/views/create_blog_post_api_view.py` (POST/CREATE view)
- `blogs_be/src/blogs_be/blogs/views/get_blog_posts_api_view.py` (GET view with filtering)
- `blogs_be/src/blogs_be/blogs/views/update_blog_post_api_view.py` (POST/UPDATE view)
- `blogs_be/src/blogs_be/blogs/views/delete_blog_posts_api_view.py` (POST/DELETE view)

---

## File location

```
<module>/views/<action_name>_api_view.py
```

RULE: Each view class lives in its own file. Do not put multiple API views in one file.

## Class structure

Each view file contains one `APIView` subclass with either a `get` or a `post` method (not both).

The `@extend_schema` decorator (from `api.utils.extend_schema`) is placed on the method, not the class.

## `extend_schema` parameters

| Parameter | Purpose |
|-----------|---------|
| `request` | Serializer class describing the POST body (omit for GET views) |
| `responses` | Dict mapping HTTP status code to response serializer |
| `data` | Dict mapping variable names to resolver functions that build the "data spec" |
| `permissions` | List of `(status_code, permission_fn, message)` tuples; use `[]` for public endpoints |

### Data spec (`data=`)

The data spec is resolved incrementally. The runtime starts with a dict that contains:
- All URL path parameters (e.g. `blog_key` from `<str:blog_key>/`)
- `request.user` under the key `"user"`

Each entry in `data=` maps a variable name to a callable that receives the previously resolved variables as keyword arguments. If a resolver raises an exception, `extend_schema` propagates it.

The resolved variables are injected as extra keyword arguments into the view method (e.g. `blog` in `def post(self, request, request_data, blog)`).

**Deriving data from resolved values:** Use lambda functions to compute values from previously resolved data:

```python
data=dict(
    blog_post=get_blog_post_or_400,         # Resolves first from URL param
    blog=lambda blog_post: blog_post.blog,  # Derives blog from blog_post
)
```

The lambda receives the previously resolved `blog_post` as a keyword argument and extracts its related blog. This derived value is then available to permission functions and the view method.

### Permissions (`permissions=`)

Each entry is a 3-tuple: `(http_status_code, permission_fn, error_message)`.

Permission functions receive arguments from the data spec — the argument names must match keys in the resolved data dict. If the permission check fails, the given HTTP status is returned with the error message.

## POST view pattern

```python
from blogs_be.blogs.actions.create_blog_post import (
    BlogPostWithTitleAlreadyExistsError,
    create_blog_post,
)
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.serializers import BlogPostSerializer, CreateBlogPostFormSerializer
from blogs_be.blogs.shortcuts import get_blog_or_400
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.common.form_serializer import FormSerializer


class CreateBlogPostRequestSerializer(FormSerializer):
    create_blog_post_form = CreateBlogPostFormSerializer()


class CreateBlogPostApiView(APIView):
    @extend_schema(
        request=CreateBlogPostRequestSerializer,
        responses={200: BlogPostSerializer},
        data=dict(
            blog=get_blog_or_400,
        ),
        permissions=[
            (403, user_is_blog_owner, "You must be the blog owner to create a blog post."),
        ],
    )
    def post(self, request, request_data, blog):
        try:
            blog_post = create_blog_post(
                create_blog_post_form=request_data.create_blog_post_form,
                blog=blog,
            )
        except BlogPostWithTitleAlreadyExistsError:
            raise ValidationError(code="BLOG_POST_TITLE_ALREADY_EXISTS")

        return Response(
            BlogPostSerializer(blog_post).data, status=status.HTTP_201_CREATED
        )
```

RULE: If the action raises an exception, convert it to a `ValidationError` with a string `code` (and optionally `detail`). Do not let action exceptions bubble up unhandled.

RULE: The `request_data` argument (injected by `extend_schema`) holds the deserialized POST body. Access nested form data via attribute access (e.g. `request_data.create_blog_post_form`).

## GET view pattern

### Basic GET view (without filtering)

```python
from blogs_be.blogs.shortcuts import get_blog_or_400
from blogs_be.blogs.serializers import BlogPostSerializer
from blogs_be.blogs.models import BlogPost
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blogs_be.api.utils.extend_schema import extend_schema


class GetBlogPostsApiView(APIView):
    @extend_schema(
        responses={200: BlogPostSerializer(many=True)},
        data=dict(blog=get_blog_or_400),
        permissions=[],
    )
    def get(self, request, blog):
        blog_posts = BlogPost.objects.filter(blog=blog)
        return Response(BlogPostSerializer(blog_posts, many=True).data, status=status.HTTP_200_OK)
```

### GET view with filtering

For GET views that accept query parameters to filter results, use `apply_filter_set_or_400` with a `FilterSet` class:

```python
from blogs_be.blogs.shortcuts import get_blog_or_400
from blogs_be.blogs.serializers import BlogPostSerializer
from blogs_be.blogs.models import BlogPost
from blogs_be.blogs.filters import BlogPostFilterSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.common.utils.apply_filter_set_or_400 import apply_filter_set_or_400


class GetBlogPostsApiView(APIView):
    filterset_class = BlogPostFilterSet
    queryset = BlogPost.objects.none()

    @extend_schema(
        responses={200: BlogPostSerializer(many=True)},
        data=dict(blog=get_blog_or_400),
        permissions=[],
    )
    def get(self, request, blog):
        blog_posts = apply_filter_set_or_400(
            BlogPost.objects.filter(blog=blog), BlogPostFilterSet, request.query_params
        )
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

RULE: When filtering is needed, set `filterset_class` and `queryset` as class attributes. The `queryset` should be `.none()` as a safe default.

## UPDATE view pattern (POST with existing resource)

Update views use POST (not PUT/PATCH) and resolve the resource to update via the data spec:

```python
from blogs_be.blogs.actions.update_blog_post import (
    BlogPostWithTitleAlreadyExistsError,
    update_blog_post,
)
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.serializers import BlogPostSerializer, UpdateBlogPostFormSerializer
from blogs_be.blogs.shortcuts import get_blog_post_or_400
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.common.form_serializer import FormSerializer


class UpdateBlogPostRequestSerializer(FormSerializer):
    update_blog_post_form = UpdateBlogPostFormSerializer()


class UpdateBlogPostApiView(APIView):
    @extend_schema(
        request=UpdateBlogPostRequestSerializer,
        responses={200: BlogPostSerializer},
        data=dict(
            blog_post=get_blog_post_or_400,
            blog=lambda blog_post: blog_post.blog,
        ),
        permissions=[
            (403, user_is_blog_owner, "You must be the blog owner to update the blog post."),
        ],
    )
    def post(self, request, request_data, blog_post):
        try:
            updated_blog_post = update_blog_post(
                update_blog_post_form=request_data.update_blog_post_form,
                blog_post=blog_post,
            )
        except BlogPostWithTitleAlreadyExistsError:
            raise ValidationError(code="BLOG_WITH_THIS_TITLE_ALREADY_EXISTS")

        return Response(
            BlogPostSerializer(updated_blog_post).data, status=status.HTTP_200_OK
        )
```

RULE: Use lambda functions in the data spec to derive values from previously resolved data. In the example above, `blog=lambda blog_post: blog_post.blog` extracts the blog from the resolved blog_post, making it available to the permission function.

## DELETE view pattern (POST for deletion)

Delete views use POST and typically return 204 NO_CONTENT:

```python
from blogs_be.blogs.permissions import user_is_blog_owner
from blogs_be.blogs.shortcuts import get_blog_or_400
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blogs_be.api.utils.extend_schema import extend_schema
from blogs_be.blogs.actions.delete_blog_posts import delete_blog_posts, BlogPostsNotFoundError
from blogs_be.blogs.serializers import DeleteBlogPostsFormSerializer
from blogs_be.common.form_serializer import FormSerializer


class DeleteBlogPostsRequestSerializer(FormSerializer):
    delete_blog_posts_form = DeleteBlogPostsFormSerializer()


class DeleteBlogPostsApiView(APIView):
    @extend_schema(
        request=DeleteBlogPostsRequestSerializer,
        responses={204: None},
        data=dict(
            blog=get_blog_or_400,
        ),
        permissions=[
            (403, user_is_blog_owner, "You must be the blog owner to delete blog posts."),
        ],
    )
    def post(self, request, request_data, blog):
        try:
            deleted_count = delete_blog_posts(
                request_data.delete_blog_posts_form, blog=blog
            )
        except BlogPostsNotFoundError as e:
            raise ValidationError(code="BLOG_POSTS_NOT_FOUND", detail=f"{e.missing_ids}")

        return Response(
            {"deleted_count": deleted_count}, status=status.HTTP_204_NO_CONTENT
        )
```

RULE: Delete endpoints use POST method with a request body specifying what to delete (not DELETE with URL params).

RULE: Return 204 NO_CONTENT for successful deletions. You may include metadata (like `deleted_count`) in the response body even with 204 status.

## Checklist

- [ ] One view class per file, in `<module>/views/`
- [ ] `@extend_schema` on the method, not the class
- [ ] `data=` dict maps variable names to resolver functions
- [ ] `permissions=` list is present (empty list `[]` for public endpoints)
- [ ] POST: action exceptions caught and re-raised as `ValidationError(code=...)`
- [ ] POST: `request_data` used to access deserialized form fields
- [ ] Response uses the appropriate `status.HTTP_*` constant
