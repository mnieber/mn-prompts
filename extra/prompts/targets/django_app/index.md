# Spec-Driven Development for Django Apps

This directory contains instructions for a spec-driven software development process where specifications are written first, then mapped to a Django application.

## Overview

The development process has four phases (design, tests, code and scenarios), which are described in the
[development workflow](./app_layer/skills/app-apply-development-phases.md). Before you write code (or a plan for it), read
[django_app/index.md](./django_app_layer/index.md) and [python_lib/index.md](./python_lib_layer/index.md) to identify
the skills that apply to the code units, and follow them closely.

## Quick Start

Consult ./app_layer/index.md for instructions on:

- the development workflow
- writing specifications
- implementing specifications
- general code generation guidelines

Consult ./django_app_layer/index.md for instructions on:

- Django-specific spec sections declared implicitly in scenarios: Django models, ApiViews, DomainEvents
- Using specific django_app skills, such as dj-write-api-view.

Consult ./python_lib_layer/index.md for instructions on:

- Using specific python_lib skills, such as py-write-action.

## Examples

The [examples/](./examples/) directory contains two complete example applications:

- **[examples/blogs/src/services/blogs_be/](./examples/blogs/src/services/blogs_be/)** - A blogs backend showing Django-specific patterns (models, API views, serializers, admin, urls, permissions, factories, tests)
- **[examples/bookie/](./examples/bookie/)** - A bookie application showing Python package patterns (actions, rules, utils, settings, enums, entrypoints)

Each example application contains:

- Spec files: `extra/spec_src/scenarios/`
- Implementation: `src/<app_name>/`
- How specs map to actual code

## Key Principles

- **One file per code unit** - Each model, action, rule, or util gets its own file
- **Snake_case file names** - Convert PascalCase spec names to snake_case
- **Forms co-location** - Forms are defined in the action files that use them
- **Settings consolidation** - All module settings go to root settings.py
- **Follow the examples** - The blogs_be and bookie examples serve as reference templates
- **Explicit is better** - When in doubt, ask for spec clarification rather than guessing
