# Skill: py-write-model

Applies when writing a model file: a dataclass that represents a domain entity.

Primary reference: `bookie/books/models/book.py`

---

## File location

```
<module>/models/<model_name>.py
```

RULE: Use a separate file for each model, even when this results in a very small file.

## Structure

RULE: A model is a class decorated with `@dataclass` from the `dataclassy` package (not the standard library).

Example from `book.py`:

```python
from dataclassy import dataclass
import typing as T

if T.TYPE_CHECKING:
    from bookie.chapters.models.chapter import Chapter


@dataclass
class Book:
    title: str
    chapters: T.List["Chapter"] = []
```

Key points:
- Use `T.TYPE_CHECKING` guards for imports that would cause circular imports at runtime.
- List fields can be initialized with `= []` thanks to `dataclassy`.
- No docstring or header comment on the class.

## Checklist

- [ ] One model per file under `<module>/models/`
- [ ] `@dataclass` from `dataclassy`, not `dataclasses`
- [ ] Circular imports avoided with `TYPE_CHECKING` guard
- [ ] No class docstring or header comment
