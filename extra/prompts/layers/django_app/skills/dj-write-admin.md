# Skill: dj-write-admin

Applies when writing an `admin.py` file for a Django app module.

Primary reference: `blogs_be/src/blogs_be/blogs/admin.py`

---

## File location

```
<module>/admin.py
```

## Pattern

Register each model with `@admin.register`. Use `TabularInline` for related models that should be editable inline on the parent's admin page.

```python
from django.contrib import admin

from blogs_be.blogs import models


class BlogPostInline(admin.TabularInline):
    model = models.BlogPost
    extra = 3


@admin.register(models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = (BlogPostInline,)
```

RULE: Import models from the module's `models` module (e.g. `from blogs import models`), not by importing each class individually.

RULE: Register every model defined in the module's `models.py`, even if the admin class body is just `pass`.

## Inline classes

Use `admin.TabularInline` for child models (one-to-many relationships) when it's useful to view/edit children directly on the parent's change page. Set `extra` to the desired number of blank inline forms (typically 3).

## Checklist

- [ ] Every model from `models.py` is registered with `@admin.register`
- [ ] Models imported via `from <module> import models`
- [ ] Child models that warrant inline editing use `TabularInline`
