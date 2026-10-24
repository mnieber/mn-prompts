# Spec-Driven Development for React Apps

This directory contains instructions for a spec-driven software development process where specifications are written first, then mapped to a React/TypeScript frontend application.

## Overview

The development process has five phases (design, test plan, tests, code and scenarios), which are described in the
[development workflow](./app_layer/skills/app-apply-development-phases.md). Before you write code (or a plan for it), read
[react_app/index.md](./react_app_layer/index.md) to identify the skills that apply to the code units, and follow
them closely.

## Quick Start

Consult ./app_layer/index.md for instructions on:

- the development workflow
- writing specifications
- implementing specifications
- general code generation guidelines

Consult ./react_app_layer/index.md for instructions on:

- Using specific react_app skills, such as fe-add-api-hooks.

## Examples

The [examples/blogs/src/services/blogs_fe/](./examples/blogs/src/services/blogs_fe/) directory contains a complete
example application (the primary template for all patterns) showing:

- Spec files: `extra/spec_src/scenarios/`
- Implementation: `src/`
- Workflow tests: `tests/`
- How specs map to actual code

## Key Principles

- **One file per component** - Each component gets its own PascalCase file, named after the component (e.g. `BlogListView.tsx`)
- **Feature modules** - Code is grouped per feature (e.g. `blogs/`, `blogPosts/`), with its components, hooks and state
- **Types and schemas together** - A data model always has both an `XT.ts` type and an `XSchema.ts` Zod schema
- **camelCase in the app** - The frontend works in camelCase, and converts to the snake_case of the backend at the API boundary
- **Follow the example** - The blogs_fe example serves as the reference template
- **Explicit is better** - When in doubt, ask for spec clarification rather than guessing
