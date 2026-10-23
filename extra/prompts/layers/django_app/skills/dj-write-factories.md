# Skill: dj-write-factories

Applies when writing factory classes for use in tests.

Primary reference: `blogs_be/src/blogs_be/blogs/tests/factories.py`

---

## File location

```
<module>/tests/factories.py
```

## Pattern

Each model gets one `DjangoModelFactory` subclass. Use `factory.Sequence` for fields that must be unique across test runs.

```python
import factory
from blogs_be.blogs.models import Blog, BlogPost
from factory.django import DjangoModelFactory


class BlogFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Blog{n}")
    description = "Some description"

    class Meta:
        model = Blog


class BlogPostFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: f"BlogPost{n}")
    content = "Some content"

    class Meta:
        model = BlogPost
```

RULE: Use `factory.Sequence` for fields that are unique in the database (e.g. names, titles, slugs). Use static strings for non-unique filler fields.

RULE: Do not set ForeignKey fields in the factory default unless every test that creates that model always needs the same parent. Instead let callers pass the related object as a keyword argument (e.g. `BlogPostFactory(blog=my_blog)`).

## Checklist

- [ ] One factory class per model
- [ ] Factory file lives at `<module>/tests/factories.py`
- [ ] Unique fields use `factory.Sequence`
- [ ] ForeignKey defaults are omitted; callers supply them explicitly
- [ ] `class Meta: model = ...` is set correctly
