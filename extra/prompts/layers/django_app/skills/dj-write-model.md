# Skill: dj-write-model

Applies when writing a `models.py` file for a Django app module.

Primary reference: `blogs_be/src/blogs_be/blogs/models.py`

---

## File location

```
<module>/models.py
```

## Base class

RULE: All models inherit from `BaseModel` (from `common.models`), not Django's `models.Model` directly. `BaseModel` provides the `id` (UUID) and timestamp fields.

## Field types

RULE: Use `SingleLineTextField` (from `common.fields`) for short string fields such as names, titles, and slugs. It inherits from `TextField` but renders as a single-line input in Django admin.

Use `models.TextField` for long-form text (e.g. `description`, `content`) with `blank=True, null=True` when the field is optional.

## Enum fields

Use `models.TextField(choices=MyEnum.choices, default=MyEnum.DEFAULT)` for fields that hold one of a fixed set of values. The enum itself lives in `<module>/enums.py`.

## ForeignKey

Use `on_delete=models.CASCADE` unless there is a specific reason for a different strategy. Use `related_name` to allow reverse access (e.g. `related_name="blog_posts"`).

## `save()` override

Override `save()` only when derived fields (e.g. a `slug` auto-computed from `name`) need to be populated before the record is written. Always call `super().save(*args, **kwargs)`.

## `__str__`

RULE: Always define `__str__` and return the field that best identifies the instance to a human reader.

## Example

```python
from django.db import models

from blogs_be.blogs.enums import Audiences
from blogs_be.common.fields import SingleLineTextField
from blogs_be.common.models import BaseModel
from django.utils.text import slugify


class Blog(BaseModel):
    name = SingleLineTextField()
    slug = SingleLineTextField()
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="blogs"
    )
    audience = models.TextField(choices=Audiences.choices, default=Audiences.ANY)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "-":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
```

## Checklist

- [ ] Model inherits from `BaseModel`
- [ ] Short string fields use `SingleLineTextField`
- [ ] Long/optional text fields use `models.TextField(blank=True, null=True)`
- [ ] Enum fields use `models.TextField(choices=..., default=...)`
- [ ] ForeignKey has `on_delete` and `related_name`
- [ ] `save()` override calls `super().save(*args, **kwargs)`
- [ ] `__str__` defined
