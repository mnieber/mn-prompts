# Skill: le-add-python-service-to-compose

Applies when adding a Python service to the Docker Compose configuration for local development.

Primary reference: `../examples/blogs/env/local/docker/`

---

## What this skill covers

This skill describes how to add a Python service to the Docker Compose setup:

- Adding the service to `docker-compose.yml`
- Adding the service to `docker-compose.src-overlays.yml`
- Adding the service to `docker-compose.dockerfile-local.yml`
- Adding the service to `docker-compose.override.yml`
- Creating the service's environment file template

## What this skill does NOT cover

The following topics are covered in separate skills:

- **Creating the service directory structure** → see `layers/local_env/skills/le-add-python-service-to-src.md`
- **Compiling .env.in files to .env files** → see `layers/local_env/skills/le-use-compose-ops.md`
- **Service-specific environment variables** → see target-specific documentation (e.g., `targets/django_app`)

---

## Docker Compose file structure

The local environment uses multiple compose files that layer on top of each other:

```
env/local/docker/
├── docker-compose.yml                    # Base service definitions (production Dockerfile)
├── docker-compose.dockerfile-local.yml   # Override to use Dockerfile.local for development
├── docker-compose.src-overlays.yml       # Mount service source code for live editing
├── docker-compose.override.yml           # Developer-specific customizations (gitignored)
└── docker-compose.base-images.yml        # Base image definitions
```

**Layering:** Docker Compose automatically merges these files when you run `docker compose` commands. The order matters:

1. `docker-compose.yml` (base)
2. `docker-compose.dockerfile-local.yml` (when building with Dockerfile.local)
3. `docker-compose.src-overlays.yml` (for development)
4. `docker-compose.override.yml` (always applied, developer-specific)

---

## Adding to docker-compose.yml

Add your service definition to the base compose file at `env/local/docker/docker-compose.yml`:

```yaml
services:
  blogs_be:
    container_name: blogs_be
    build:
      context: ${ROOT_DIR}/src
      dockerfile: services/blogs_be/Dockerfile
    command: sleep infinity
    depends_on:
      - postgres
    env_file:
      - ./env_files/blogs_be.env
    image: blogs_be
    ports:
      - 8000:8000 # Django
```

### Service definition fields

**container_name:** Use the service name without any suffix

```yaml
container_name: blogs_be
```

**build context:** Always use `${ROOT_DIR}/src` as the context

```yaml
build:
  context: ${ROOT_DIR}/src
  dockerfile: services/blogs_be/Dockerfile
```

**dockerfile:** Path relative to the build context

```yaml
dockerfile: services/blogs_be/Dockerfile
```

**command:** Use `sleep infinity` to keep the container running

```yaml
command: sleep infinity
```

This allows you to exec into the container and run commands manually or via `jaz`.

**depends_on:** List services this service needs

```yaml
depends_on:
  - postgres
  - localstack
```

**env_file:** Reference the compiled .env file

```yaml
env_file:
  - ./env_files/blogs_be.env
```

Note: Use `.env` (not `.env.in`) - the compiled file.

**image:** Use the service name as the image name

```yaml
image: blogs_be
```

**ports:** Expose ports for accessing the service from the host

```yaml
ports:
  - 8000:8000 # Django
```

Include a comment describing what the port is for.

**RULE:** The production Dockerfile is referenced in `docker-compose.yml`, not `Dockerfile.local`.

**RULE:** All paths in the compose file should use environment variables like `${ROOT_DIR}` for portability.

---

## Adding to docker-compose.dockerfile-local.yml

Override the build configuration to use `Dockerfile.local` for development:

```yaml
services:
  blogs_be:
    build:
      context: ${ROOT_DIR}/src
      dockerfile: services/blogs_be/Dockerfile.local
    image: blogs_be_local
```

**RULE:** Change the `dockerfile` to point to `Dockerfile.local`.

**RULE:** Change the `image` name to include `_local` suffix (e.g., `blogs_be_local`).

**RULE:** Keep the same `context` as in the base compose file.

This file is only included when building with the "use_dockerfile_local" flag (controlled via the stack's Justfile).

---

## Adding to docker-compose.src-overlays.yml

Mount the service's source code to enable live editing:

```yaml
services:
  blogs_be:
    volumes:
      - ${ROOT_DIR}/src/services/blogs_be:/app/src
      - ${ROOT_DIR}/src/libs/python_toolkit:/app/libs/python_toolkit
```

**RULE:** Mount the service directory to `/app/src` (matching the WORKDIR in the Dockerfile).

**RULE:** Overlay code from src/libs for dependency libs using `- ${ROOT_DIR}/src/libs/XXX_lib:/app/libs/XXX_lib` unless if `XXX_lib` is a stub (in that case, we overlay the source code in docker-compose.override.yml because the source code location is non-standard then).

**RULE:** Use `${ROOT_DIR}` to reference the stack root.

This allows you to edit code on your host machine and see changes immediately in the container without rebuilding.

---

## Adding to docker-compose.override.yml

The `docker-compose.override.yml` file contains **developer-specific customizations** and is gitignored. Setting this up is an **interactive process** with the developer.

### Common volume overlays

Ask the developer which of these they want to configure:

#### General development overlays

```yaml
services:
  blogs_be:
    volumes:
      # General overlays
      - $HOME/.config/pudb:/root/.config/pudb # Debugger config
      - /opt/projects/sunya/blogs_be/assets:/app/assets
      - /opt/projects/sunya/blogs_be/dumps:/app/dumps
      - /opt/projects/sunya/blogs_be/fish_history:/root/.local/share/fish/fish_history
      - /opt/projects/sunya/blogs_be/ipython:/root/.ipython
      - /opt/projects/sunya/blogs_be/log:/app/log
      - /opt/projects/sunya/blogs_be/pytest_report.html:/app/pytest_report.html
```

#### Django-specific overlays

```yaml
# Django-specific overlays
- /opt/projects/sunya/blogs_be/media:/app/media
- /opt/projects/sunya/blogs_be/static:/app/static
```

#### External library code overlays (for libraries that are stubbed)

```yaml
# Lib code overlays
- /home/maarten/projects/woodstock/src/libs/woodstock:/app/libs/woodstock
```

### Interactive setup process

When adding a service to `docker-compose.override.yml`, ask the developer:

1. **"Do you want to mount external library code for live development?"**
   - If yes: "Which libraries? What are their paths on your system?"
   - Add volume mounts mapping external library paths to `/app/libs/<lib_name>`

2. **"Do you want to persist development artifacts (logs, dumps, pytest reports)?"**
   - If yes, then ask for the /opt/projects/<project-name> directory that stores these artifacts.
   - Add volume mounts for `/app/log`, `/app/dumps`, `/app/pytest_report.html`, `fish_history`, `ipython`, and `pudb`.
   - Add mounts for `/app/media` and `/app/static` if it's a django service.

**RULE:** When in doubt about what should go in `docker-compose.override.yml`, ask the user for clarification.

**RULE:** Use absolute paths in `docker-compose.override.yml` (not `${ROOT_DIR}`) since this file is user-specific.

**RULE:** Group volume mounts with comments: `# General overlays`, `# Django-specific overlays`, `# Lib code overlays`, etc.

---

## Creating the environment file template

Create the environment file template at:

```
env/local/docker/env_files/<service_name>.env.in
```

Example for `blogs_be.env.in`:

```bash
DJANGO_DATABASE_NAME=blogs_be_local
DJANGO_DATABASE_PASSWORD=${BLOGS_BE_DJANGO_DATABASE_PASSWORD}
DJANGO_DATABASE_USER=blogs_be_local
DJANGO_SECRET_KEY=${BLOGS_BE_DJANGO_SECRET_KEY}
DJANGO_SETTINGS_MODULE=blogs_be.app.settings.local
DJANGO_SUPERUSER_EMAIL=admin@blogs.org
DJANGO_SUPERUSER_PASSWORD=${BLOGS_BE_DJANGO_SUPERUSER_PASSWORD}
DJANGO_SUPERUSER_USERNAME=admin

POSTGRES_HOST=postgres
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_PORT=5432

BLOGS_USER_EMAIL=blogs_be@blogs.org
BLOGS_USER_PASSWORD=${BLOGS_USER_PASSWORD}
```

### Environment variable patterns

**Service hostnames:** Use the Docker Compose service name (not `localhost`)

```bash
POSTGRES_HOST=postgres  # ✓ Correct
POSTGRES_HOST=localhost # ✗ Wrong
```

**Secrets:** Use placeholder variables that reference secrets from a central secrets file

```bash
DJANGO_SECRET_KEY=${BLOGS_BE_DJANGO_SECRET_KEY}
```

**Non-secret config:** Hard-code directly in the .env.in file

```bash
DJANGO_SETTINGS_MODULE=blogs_be.app.settings.local
POSTGRES_PORT=5432
```

**RULE:** The exact environment variables needed depend on the service type and are documented in target-specific documentation (e.g., `targets/django_app` for Django services).

**RULE:** Always use `.env.in` suffix for template files. The actual `.env` files are generated by `jaz compose.compile-env-files`.

---

## Checklist

- [ ] Service added to `docker-compose.yml` with all required fields
- [ ] Service uses `${ROOT_DIR}` for paths
- [ ] Service uses `command: sleep infinity`
- [ ] Service references the compiled `.env` file (not `.env.in`)
- [ ] Ports exposed with descriptive comments
- [ ] Service added to `docker-compose.dockerfile-local.yml` with `_local` suffix
- [ ] Service added to `docker-compose.src-overlays.yml` mounting to `/app/src`
- [ ] Developer consulted about `docker-compose.override.yml` customizations
- [ ] Volume overlays added to `docker-compose.override.yml` with grouping comments
- [ ] Environment file template created at `env_files/<service_name>.env.in`
- [ ] Environment variables use Docker Compose service names (not localhost)
- [ ] Secrets use placeholder variables
- [ ] Non-secret config is hard-coded
