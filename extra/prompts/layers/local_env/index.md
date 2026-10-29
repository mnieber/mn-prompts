# Development of Local Environments

This layer describes how to set up and manage a **local development environment** for a stack containing multiple services.

A local_env stack runs all services in Docker containers via Docker Compose. Developers use Just commands to build, start, and operate the stack. Environment variables are managed through `.env.in` templates that are compiled into `.env` files before containers start.

When you are asked to generate code, or to plan for generating code, identify which of the below skills are needed and apply them. Each skill covers one concern and cross-references others where they overlap.

## Skills

### Compose ops

The justfile structure, ROOT_DIR/COMPOSE_DIR/COMPOSE_PROJECT_NAME, `.local.env`, `secrets.env`, and the compile-env-files workflow.
→ [le-use-compose-ops](./skills/le-use-compose-ops.md)

### Base image

A shared base Docker image used by multiple Python services.
→ [le-add-base-image](./skills/le-add-base-image.md)

### Python service — source

The source directory structure, Dockerfiles, requirements files, and justfile for a Python service.
→ [le-add-python-service-to-src](./skills/le-add-python-service-to-src.md)

### Python service — compose

Wiring a Python service into the Docker Compose files and creating its `.env.in` template.
→ [le-add-python-service-to-compose](./skills/le-add-python-service-to-compose.md)

### React service — compose

Wiring a React/Vite frontend service into the Docker Compose files and creating its `.env.in` template.
→ [le-add-react-service-to-compose](./skills/le-add-react-service-to-compose.md)

### PostgreSQL

A PostgreSQL service in Docker Compose.
→ [le-add-postgres-to-compose](./skills/le-add-postgres-to-compose.md)

### LocalStack

LocalStack for local AWS service emulation (S3, SQS, etc.).
→ [le-add-localstack](./skills/le-add-localstack.md)

### Python library

A Python library whose source code lives within the stack directory.
→ [le-add-python-lib](./skills/le-add-python-lib.md)

### Python stub library

A stub for a Python library whose source code lives in a separate repository.
→ [le-add-python-stub-lib](./skills/le-add-python-stub-lib.md)

### Dodo config files

The dodo_commands config files (`config.yaml`, `stack.root.yaml`, `stack.<service>.yaml`).
→ [le-write-dodo-config-files](./skills/le-write-dodo-config-files.md)

### Tmux menu

A `jaz tmux` target that opens a tmux session with a menu of commands, each picked command running in its own pane.
→ [le-add-tmux-menu](./skills/le-add-tmux-menu.md)

### Edit config

A `jaz edit-config` target that opens the stack's config files in an editor.
→ [le-add-edit-config](./skills/le-add-edit-config.md)

### Spec src

An `extra/spec_src/` directory for a service, wired into the root `sunya.config.yaml`.
→ [le-add-spec-src](./skills/le-add-spec-src.md)

---

## Typical setup order

When setting up a new stack from scratch, apply the skills in roughly this order:

1. `le-use-compose-ops` — justfile structure, `.local.env`, secrets
2. `le-add-base-image` — shared Python base image
3. `le-add-postgres-to-compose` — database service
4. `le-add-python-service-to-src` + `le-add-python-service-to-compose` — backend service(s)
5. `le-add-react-service-to-compose` — frontend service (if applicable)
6. `le-add-python-lib` + `le-add-python-stub-lib` — in-stack libraries and external library stubs (if applicable)
7. `le-write-dodo-config-files` — dodo_commands wiring
8. `le-add-spec-src` — spec source directories (if applicable)
9. `le-add-tmux-menu` — tmux session with a menu of commands (if applicable)
10. `le-add-edit-config` — a target that opens the config files in an editor (if applicable)
