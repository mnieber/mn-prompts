# Instructions for mn-prompts

This directory contains the instructions for a spec-driven software development process, where specifications are
written first, then mapped to implementation. It combines the layers that the parts of this repository use.

## Overview

The development process has five phases (design, test plan, tests, code and scenarios), which are described in the
[development workflow](./app_layer/skills/app-apply-development-phases.md). Before you write code (or a plan for it),
find the part of the repository that you work on below, read the index files of its layers to identify the skills
that apply to the code units, and follow them closely.

## The parts of this repository

| Part                                                   | What it is                                    | Layers                       |
| ------------------------------------------------------ | --------------------------------------------- | ---------------------------- |
| `src/mn_prompts/`                                      | the mn-prompts library and its entrypoint     | app, python_lib              |
| `extra/prompts/examples/bookie/`                       | example Python application                    | app, python_lib              |
| `extra/prompts/examples/blogs/` (`jazzoo`, `env/local/`) | the local development environment of the blogs stack | local_env                    |
| `extra/prompts/examples/blogs/src/services/blogs_be/`  | the Django backend of the blogs stack         | app, django_app, python_lib  |
| `extra/prompts/examples/blogs/src/services/blogs_fe/`  | the React frontend of the blogs stack         | app, react_app               |

## The layers

Consult [app_layer/index.md](./app_layer/index.md) for:

- the development workflow
- writing specifications
- implementing specifications
- general code generation guidelines

Consult [python_lib_layer/index.md](./python_lib_layer/index.md) for the python_lib skills, such as py-write-action.

Consult [django_app_layer/index.md](./django_app_layer/index.md) for:

- Django-specific spec sections declared implicitly in scenarios: Django models, ApiViews, DomainEvents
- the django_app skills, such as dj-write-api-view

Consult [react_app_layer/index.md](./react_app_layer/index.md) for the react_app skills, such as fe-add-api-hooks.

Consult [local_env_layer/index.md](./local_env_layer/index.md) for a local development stack:

- the Docker Compose files, and the `jaz` targets that build, start, initialise and operate the stack
- adding Python and React services, PostgreSQL, base images and stub libraries to the stack
- the environment variables of the services

**Paths between layers.** The `*_layer` entries are symlinks into `extra/prompts/layers/`. A link in a skill file
that leaves its layer (e.g. `../../python_lib/skills/py-publish-to-pypi.md` in a local_env skill) is relative to the
real location of the file: resolve it inside `extra/prompts/layers/`, not inside this directory.

## Examples

The [examples/](./examples/) directory (`extra/prompts/examples/`) contains the reference applications:

- **[examples/bookie/](./examples/bookie/)** - Python package patterns (actions, rules, utils, settings, enums,
  entrypoints)
- **[examples/blogs/](./examples/blogs/)** - a complete stack, and the primary template for local_env patterns:
  - `src/services/blogs_be/` - Django patterns (models, API views, serializers, admin, urls, permissions,
    factories, tests)
  - `src/services/blogs_fe/` - React patterns (components, API hooks, state, workflow tests)

Each example application contains:

- Spec files: `extra/spec_src/scenarios/`
- Implementation: `src/`
- How specs map to actual code

## Key Principles

- **One file per code unit** - Each model, action, rule, or util gets its own file
- **Snake_case file names** - Convert PascalCase spec names to snake_case
- **Forms co-location** - Forms are defined in the action files that use them
- **Settings consolidation** - All module settings go to root settings.py
- **Follow the examples** - The blogs and bookie examples serve as reference templates
- **Explicit is better** - When in doubt, ask for spec clarification rather than guessing
