# Skill: py-write-settings

Applies when adding or modifying application settings.

Primary reference: `bookie/settings.py`

---

## File location

```
<app_package>/settings.py   ← single file at the application package root
```

RULE: All settings are collected into a single `settings.py` at the application package root. Settings are not split per module.

## Structure

Each setting is typically derived from an environment variable. The application must not read environment variables outside of `settings.py`, so that all environment dependencies are visible in one place.

Example from `bookie/settings.py`:

```python
MAX_BAD_WORDS_PER_PARAGRAPH = 5
MAX_CHAPTERS_PER_BOOK = 10
```

In production scenarios the values would come from `os.environ`:

```python
import os

MAX_CHAPTERS_PER_BOOK = int(os.environ.get("MAX_CHAPTERS_PER_BOOK", 10))
```

## Mapping from specs

Each module's `Settings` section in the scenario spec (e.g. `c.Books.Settings.MAX_CHAPTERS_PER_BOOK`) describes module-level settings. Despite being declared per-module in the spec, all of them are consolidated into the single root `settings.py`.

## Checklist

- [ ] `settings.py` is at the application package root (not inside a module subdirectory)
- [ ] All environment variable reads are in `settings.py`
- [ ] No module reads `os.environ` directly
