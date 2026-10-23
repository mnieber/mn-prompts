# Local Development Stack Setup

This directory contains instructions for setting up and managing a stack containing multiple services and applications, focussing on the local development environment for working with this stack.

## Overview

Setting up a local development stack follows these main phases:

1. **Initial Setup** - Configure justfile structure, Docker Compose files, and base images
2. **Add Services** - Add backend/frontend services and infrastructure (databases, etc.)
3. **Configure Development Environment** - Set up overlays, environment variables, and developer tooling

## Quick Start

Consult [local_env/index.md](./local_env_layer/index.md) for instructions on:

- Setting up Docker Compose configuration
- Creating justfile commands for stack operations
- Adding Python/React services to the stack
- Configuring base images and stub libraries
- Managing environment variables

## Reference app

**[examples/blogs/](./examples/blogs/)** — complete reference stack; primary template for all patterns

The blogs stack contains:

- Django backend (`blogs_be`) with PostgreSQL
- React frontend (`blogs_fe`)
- Docker Compose orchestration
- Just commands for common operations

## Key Principles

- **Layered Compose Files** - Base (`docker-compose.yml`) + local dev overrides (`dockerfile-local.yml`, `src-overlays.yml`, `override.yml`)
- **Src Overlays** - Mount service source code for live editing without rebuilds
- **Base Images** - Shared images (`<stack>_base_python`) reduce build times
- **Environment Templates** - Use `.env.in` templates compiled to `.env` files
- **Just Commands** - Consistent interface (`just build`, `just up`, `just shell <service>`)
- **Developer Customization** - Personal preferences in `.local.env` and `docker-compose.override.yml`
