# Skill: dj-write-serializer

Applies when writing a `serializers.py` file for a Django app module.

Primary reference: `blogs_be/src/blogs_be/blogs/serializers.py`

---

## File location

```
<module>/serializers.py
```

## Two types of serializers

### 1. Form serializers

Used to deserialize incoming POST request bodies. They are generated automatically from a dataclass form using `FormSerializer`:

```python
from blogs_be.common.form_serializer import FormSerializer
from blogs_be.blogs.actions.create_blog_post import CreateBlogPostForm


class CreateBlogPostFormSerializer(FormSerializer):
    class Meta:
        form_class = CreateBlogPostForm
```

RULE: The `Meta.form_class` must point to the dataclass defined in the action file. `FormSerializer` introspects the dataclass fields to produce the serializer fields automatically.

### 2. Read serializers

Used to serialize model instances in responses. They inherit from both `ReadSerializerMixin` and `BaseModelSerializer`:

```python
from blogs_be.common.serializers import BaseModelSerializer, ReadSerializerMixin
from blogs_be.blogs.models import BlogPost


class BlogPostSerializer(ReadSerializerMixin, BaseModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "blog_id", "content", "is_published", "level"]
```

RULE: Always list all fields explicitly in `Meta.fields`. Do not use `fields = "__all__"`.

RULE: ForeignKey IDs are exposed as `<field_name>_id` (e.g. `blog_id`, `owner_id`), not as nested objects, unless there is a specific requirement for nesting.

## Request body serializer (wrapping form serializers)

When a view needs to accept multiple nested form objects in its request body, define a wrapper serializer in the view file (not in `serializers.py`) using `FormSerializer` as the base:

```python
class CreateBlogPostRequestSerializer(FormSerializer):
    create_blog_post_form = CreateBlogPostFormSerializer()
```

## Checklist

- [ ] Form serializers use `FormSerializer` with `Meta.form_class`
- [ ] Read serializers inherit from `ReadSerializerMixin, BaseModelSerializer`
- [ ] `Meta.fields` is an explicit list, not `"__all__"`
- [ ] ForeignKey IDs are named `<field>_id`
