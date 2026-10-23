# Development of Python Libraries

When you are asked to generate code, or to plan for generating code, identify which of the below skills are needed and apply them.

## Skills

### General Python conventions

Comments, logging, and dataclassy usage — applies to every Python file.
→ [py-write-python-files](skills/py-write-python-files.md)

### Action

A function that changes application state. Covers forms co-location, exception handling, and helper function conventions.
→ [py-write-action](skills/py-write-action.md)

### Model

A dataclassy dataclass representing a domain entity.
→ [py-write-model](skills/py-write-model.md)

### Rule

A function that retrieves or computes information subject to business logic, without modifying state.
→ [py-write-rule](skills/py-write-rule.md)

### Util

A generic helper function free from business logic.
→ [py-write-util](skills/py-write-util.md)

### Policy

A replaceable class that hides an interaction with the outside world (e.g. an external service).
→ [py-write-policy](skills/py-write-policy.md)

### Workflow tests

Tests that a developer reads top to bottom, like a story, to understand how the tool is used.
→ [py-write-workflow-tests](skills/py-write-workflow-tests.md)

### Settings

Centralized `settings.py` at the application package root; environment variable handling.
→ [py-write-settings](skills/py-write-settings.md)

### Schema

Pydantic classes that describe the internal structure of a JSON blob.
→ [py-write-schema](skills/py-write-schema.md)

### Enums

A module-level `enums.py` file derived from the `Enums` section of the scenario spec.
→ [py-write-enums](skills/py-write-enums.md)

### Entrypoint

An application entrypoint file and its `pyproject.toml` registration.
→ [py-write-entrypoint](skills/py-write-entrypoint.md)

---

## Key Principles

- **One file per code unit** — each model, action, rule, or util gets its own file
- **Snake_case file names** — convert PascalCase spec names to snake_case
- **Forms co-location** — forms are defined in the action files that use them
- **Settings consolidation** — all module settings go to the root `settings.py`
- **Explicit is better** — when in doubt, ask for spec clarification rather than guessing
