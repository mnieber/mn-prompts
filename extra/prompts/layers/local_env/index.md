# Development of Local Environments

This layer describes how to set up and manage a **local development environment** for a stack containing multiple services.

A local_env stack runs all services in Docker containers via Docker Compose. Developers use `jaz` targets (jazzoo) to build, start, and operate the stack, and each service has a `jazzoo` file with its own targets, which runs in its container. Environment variables are managed through `.env.in` templates that are compiled into `.env` files before containers start.

When you are asked to generate code, or to plan for generating code, identify which of the below skills are needed and apply them. Each skill covers one concern and cross-references others where they overlap.

## Skills

### Compose ops

The `jaz compose.*` and `jaz python.*` targets (build, up, down, restart, run, init, compile-env-files, pip-compile), the `/compose` and `/python` config, the developer's own `local.yaml` config layer, and `secrets.env`.
→ [le-use-compose-ops](./skills/le-use-compose-ops.md)

### Base image

A shared base Docker image used by multiple Python services.
→ [le-add-base-image](./skills/le-add-base-image.md)

### Python service — source

The source directory structure, Dockerfiles, requirements files, and `jazzoo` file for a Python service.
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

### Tmux menu

A `jaz tmux` target that opens a tmux session with a menu of commands, each picked command running in its own pane.
→ [le-add-tmux-menu](./skills/le-add-tmux-menu.md)

### Jazzoo configs

A `config` layer of `jaz` targets (`jaz config.edit`, `config.print`) that open the stack's config files in an editor and print the merged config.
→ [le-manage-jazzoo-configs](./skills/le-manage-jazzoo-configs.md)

### Docker containers

A `docker` layer of `jaz` targets (`jaz docker.exec`, `docker.kill`, `docker.inspect`, `docker.commit`) for the stack's running containers, and a layer per service (e.g. `jaz be.run-server`, `jaz be.shell`).
→ [le-manage-docker-containers](./skills/le-manage-docker-containers.md)

### Dial

A `dial` layer of `zoo` targets, and fish key bindings that call them: F1–F12 insert a command, Shift+F and Ctrl+F `cd` to a directory of the stack.
→ [le-add-dial](./skills/le-add-dial.md)

### Spec src

An `extra/spec_src/` directory for a service, wired into the root `sunya.config.yaml`.
→ [le-add-spec-src](./skills/le-add-spec-src.md)

---

## Typical setup order

When setting up a new stack from scratch, apply the skills in roughly this order:

1. `le-use-compose-ops` — compose and python targets, config, secrets
2. `le-add-base-image` — shared Python base image
3. `le-add-postgres-to-compose` — database service
4. `le-add-python-service-to-src` + `le-add-python-service-to-compose` — backend service(s)
5. `le-add-react-service-to-compose` — frontend service (if applicable)
6. `le-add-python-lib` + `le-add-python-stub-lib` — in-stack libraries and external library stubs (the jazzoo stub is always needed)
7. `le-add-spec-src` — spec source directories (if applicable)
8. `le-add-tmux-menu` — tmux session with a menu of commands (if applicable)
9. `le-manage-jazzoo-configs` — targets that edit and print the config (if applicable)
10. `le-manage-docker-containers` — targets for the stack's running containers (if applicable)
