# Skill: py-write-enums

Applies when writing an enums file for a module.

Primary reference: `bookie/chapters/enums.py`

---

## File location

```
<module>/enums.py
```

Each module that has enums gets a single `enums.py` file. All enums for that module live together in this one file.

## Structure

Enums should inherit from both `str` and `Enum` so that values are directly usable as strings:

```python
from enum import Enum


class TitleStyles(str, Enum):
    NORMAL = "normal"
    EXCLAMATIONS = "exclamations"
```

## Mapping from specs

A module's `Enums` section in the scenario spec (e.g. `c.Chapters.Enums`) maps to `<module>/enums.py`.

## Checklist

- [ ] All enums for a module live in a single `<module>/enums.py`
- [ ] Enum classes inherit from `(str, Enum)` so values are usable as strings
