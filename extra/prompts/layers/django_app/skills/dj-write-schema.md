# Skill: dj-write-schema

Applies when writing a schema file that describes the internal structure of a JSON blob stored in a model field or passed between components.

---

## File location

```
<module>/schemas/<schema_name>.py
```

or, if there is only one schema for the module:

```
<module>/schema.py
```

## What is a schema?

A schema is a Pydantic model class that validates and documents the shape of a JSON blob. Unlike a Django REST framework serializer (which handles HTTP request/response), a schema is used internally — for example, to describe the content of a `JSONField` on a Django model.

## Pattern

```python
from pydantic import BaseModel
from typing import Optional


class BlogPostMetadata(BaseModel):
    reading_time_minutes: int
    tags: list[str]
    featured_image_url: Optional[str] = None
```

RULE: Use Pydantic `BaseModel`, not Django REST framework serializers, for internal JSON structure.

RULE: All fields should have explicit types. Optional fields use `Optional[T] = None`.

RULE: Schema classes are plain data containers — no business logic, no database access.

## Checklist

- [ ] Schema inherits from `pydantic.BaseModel`
- [ ] All fields have explicit type annotations
- [ ] Optional fields have a default of `None`
- [ ] No business logic inside the schema class
