# Skill: dj-write-settings

Applies when writing settings files for a Django application.

Primary reference: `blogs_be/src/blogs_be/app/settings/` directory

---

## Directory structure

RULE: Django application settings live in `app/settings/`, not in a single `settings.py` at the package root. This overrides the general `py-write-settings` pattern.

```
app/settings/
├── __init__.py          # imports from the active environment
├── base/
│   ├── __init__.py      # imports all sections with *
│   └── sections/
│       ├── auth.py
│       ├── databases.py
│       ├── installed_apps.py
│       ├── middleware.py
│       ├── paths.py
│       ├── rest_framework.py
│       └── ...          # one file per logical group
└── dev/
    ├── __init__.py      # imports base + dev sections
    ├── inherit.py
    └── sections/
        ├── debug.py
        ├── secrets.py
        └── ...          # overrides for the dev environment
```

## Base settings

The `base/__init__.py` imports all sections using `*`:

```python
from .sections.auth import *  # noqa
from .sections.databases import *  # noqa
from .sections.installed_apps import *  # noqa
# ...
```

Each section file (e.g. `sections/databases.py`) defines a group of related settings variables and nothing else.

## Environment-specific settings

Environment directories (e.g. `dev/`) inherit from `base` and add or override specific sections. The `dev/__init__.py` re-exports the base settings and then imports the dev-specific sections on top.

## Adding a new setting

1. Identify the logical group the setting belongs to (e.g. authentication, middleware, REST framework).
2. Add it to the corresponding file in `base/sections/` or the appropriate environment `sections/` directory.
3. If the setting is environment-specific, add it only in the relevant environment section.

## Checklist

- [ ] Settings live in `app/settings/`, not `settings.py`
- [ ] New settings go in the correct `sections/` file under `base/` or the appropriate environment dir
- [ ] Each section file is imported with `*` in the environment `__init__.py`
- [ ] Secrets and environment-specific values are in the `dev/sections/` override, not in `base/`
