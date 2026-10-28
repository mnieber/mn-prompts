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

RULE: A model is a class decorated with the project's own `@dataclass` from `<package>/utils/dataclass.py` (see
the Dataclasses section of [py-write-python-files](py-write-python-files.md)), not the standard library decorator.

Example from `book.py`:

```python
import typing as T

from bookie.utils.dataclass import dataclass

if T.TYPE_CHECKING:
    from bookie.chapters.models.chapter import Chapter


@dataclass
class Book:
    title: str
    chapters: T.List["Chapter"] = []
```

Key points:
- Use `T.TYPE_CHECKING` guards for imports that would cause circular imports at runtime.
- List, dict and set fields can be initialized with `= []`, `= {}` and `= set()` thanks to our `dataclass`
  decorator: every instance gets its own copy of the default.
- No docstring or header comment on the class.

## Checklist

- [ ] One model per file under `<module>/models/`
- [ ] `@dataclass` from `<package>/utils/dataclass.py`, not from `dataclasses` or `dataclassy`
- [ ] Circular imports avoided with `TYPE_CHECKING` guard
- [ ] No class docstring or header comment
