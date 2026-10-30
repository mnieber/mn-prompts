# Skill: le-add-python-service-to-src

Applies when adding a new Python-based service to the stack's `src/services/` directory.

Primary reference: `../examples/blogs/src/services/blogs_be/`

---

## What this skill covers

This skill describes the **minimal structure and files** needed for a Python service in the stack:

- Service directory structure
- Dockerfile and Dockerfile.local for containerization
- Python packaging files (setup.py, pyproject.toml, README.md)
- Requirements files for dependency management
- Minimal Justfile commands for the service
- Environment file templates
- Setup configuration

## What this skill does NOT cover

The following topics are covered in separate skills/targets:

- **Django-specific patterns** (models, views, settings, etc.) → see the [django_app layer](../../django_app/index.md)
- **Adding the service to docker-compose.yml** → see `layers/local_env/skills/le-add-python-service-to-compose.md`
- **Creating base images** → see `layers/local_env/skills/le-add-base-image.md`
- **Stub libraries backed by external code** → see `layers/local_env/skills/le-python-lib-stub.md`
- **Test configuration** (conftest.py, pytest_plugins) → see target-specific documentation
- **Specification files** (extra/spec_src) → see the [app layer](../../app/index.md) for how spec files are written and used
- **Setting up the environment variables** → see `layers/local_env/skills/le-add-python-service-to-compose.md`

---

## Service directory structure

Create the service directory at:

```
<stack>/src/services/<service_name>/
```

Example for a service called `blogs_be`:

```
src/services/blogs_be/
├── Dockerfile                  # Production Docker image
├── Dockerfile.local            # Development Docker image (with src overlays)
├── setup.py                    # Setuptools entry point
├── pyproject.toml              # Python project metadata
├── setup.cfg                   # Tool configuration (isort, etc.)
├── README.md                   # Service description
├── requirements.in             # Direct dependencies
├── requirements.editable       # Editable local dependencies
├── requirements.txt            # Compiled dependencies (auto-generated)
├── requirements.dev.txt        # Development dependencies
├── jazzoo                      # Service-specific targets, run with jaz in the container
└── src/
    └── <service_name>/         # Python package
        └── __init__.py
```

---

## Dockerfile.local

The `Dockerfile.local` is used for **development** with src overlays, allowing you to edit code on your host machine and see changes immediately in the container without rebuilding.

**Key characteristics:**

- Starts from a base Python image (e.g., `<stack_name>_base_python`)
- Copies only minimal setup files for dependencies
- Installs both production and development dependencies
- Uses `/app/src` as WORKDIR
- Leverages uv's caching for fast rebuilds

```dockerfile
FROM blogs_base_python

# Run pre-install scripts (if needed)
COPY install_scripts/install-postgres-tools.sh /app/install_scripts/
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    bash /app/install_scripts/install-postgres-tools.sh

# Copy the requirements file(s) for each library
COPY libs/jazzoo/pyproject.toml libs/jazzoo/setup.py libs/jazzoo/README.md /app/libs/jazzoo/
COPY libs/woodstock/pyproject.toml libs/woodstock/setup.py libs/woodstock/README.md /app/libs/woodstock/

# Install the service
COPY services/blogs_be/pyproject.toml services/blogs_be/requirements.* services/blogs_be/setup.py services/blogs_be/README.md /app/src/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --break-system-packages -e /app/src -r /app/src/requirements.txt -r /app/src/requirements.dev.txt

WORKDIR /app/src
```

**RULE:** Only copy minimal files needed for `pip install` (setup files, requirements files). The actual source code is mounted via src overlays at runtime.

**RULE:** Use `--mount=type=cache` for apt and uv caches to speed up rebuilds.

**RULE:** Install the service in editable mode (`-e /app/src`) so code changes are immediately visible.

**RULE:** Include both `requirements.txt` and `requirements.dev.txt` for development tools.

### Install scripts section

If the service needs system packages (e.g., PostgreSQL client tools), add an install scripts section:

```dockerfile
# Run pre-install scripts
COPY install_scripts/install-postgres-tools.sh /app/install_scripts/
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    bash /app/install_scripts/install-postgres-tools.sh
```

Create the install script at `<stack>/src/install_scripts/<script_name>.sh`:

```bash
apt-get update && apt-get install -y \
    postgresql \
    postgresql-client \
```

**RULE:** Only include the install scripts section if the service requires additional system packages beyond what's in the base image.

---

## Dockerfile

The `Dockerfile` is used for **production** builds where the entire source code is copied into the image.

**Key differences from Dockerfile.local:**

- Copies the full library code (not just setup files)
- Copies the full service code
- Only installs production dependencies (no requirements.dev.txt)

```dockerfile
FROM blogs_base_python

# Run pre-install scripts
COPY install_scripts/install-postgres-tools.sh /app/install_scripts/
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    bash /app/install_scripts/install-postgres-tools.sh

# Copy each library
COPY libs/jazzoo /app/libs/jazzoo
COPY libs/woodstock /app/libs/woodstock

# Install the service
COPY services/blogs_be /app/src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --break-system-packages -e /app/src -r /app/src/requirements.txt

WORKDIR /app/src
```

**RULE:** Copy full directories for production builds, not just setup files.

**RULE:** Only install production requirements (`requirements.txt`), not development requirements.

---

## Python packaging files

### setup.py

Create a minimal `setup.py` that creates a placeholder package directory:

```python
from pathlib import Path

from setuptools import setup


def create_placeholder():
    this_directory = Path(__file__).parent
    pkg_directory = this_directory / "src" / "blogs_be"

    if not pkg_directory.exists():
        pkg_directory.mkdir(parents=True)
        with open(pkg_directory / "__init__.py", "w") as f:
            f.write("# Placeholder for package")


if __name__ == "__main__":
    create_placeholder()
    setup()
```

**RULE:** Replace `blogs_be` with your actual service name.

### pyproject.toml

Minimal example:

```toml
[project]
name = "blogs_be"
description = "Blogs Backend Application"
version = "0.1.0"
readme = "README.md"
dependencies = []

[tool.setuptools]
package-dir = { "" = "src" }

[tool.setuptools.packages.find]
where = ["src"]

[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"
```

**RULE:** A service only uses requirements files for dependencies. Therefore, we must set `dependencies = []`.

### README.md

Create a _very_ minimal README with a one-line summary of the project.

```markdown
# blogs_be

Blogs Backend Application
```

### setup.cfg

Configure code formatting tools (isort, etc.):

```ini
[isort]
multi_line_output=3
include_trailing_comma=True
force_grid_wrap=0
use_parentheses=True
line_length=88
known_first_party=blogs_be
```

**RULE:** Update `known_first_party` to match your service name.

---

## Requirements files

### requirements.in

List your **direct dependencies** (not transitive dependencies):

```
deepdiff
Django
django-cors-headers
djangorestframework==3.14.0
psycopg2-binary
```

**RULE:** Pin versions only when necessary for compatibility. Let uv resolve the rest.

### requirements.editable

List **local editable dependencies** using environment variables:

```
-e ${BLOGS_LIBS_DIR}/jazzoo
-e ${BLOGS_LIBS_DIR}/woodstock
```

The requirements.editable file is used during `jaz python.pip-compile` to generate `requirements.txt`.

**RULE:** Every service lists the jazzoo stub library (see `layers/local_env/skills/le-add-python-stub-lib.md`), so that `jaz` runs in its container.

**RULE:** Use the <XXX>\_LIBS_DIR environment variable for paths so the same file works in different contexts. On the host, `jaz python.pip-compile` sets it (see `layers/local_env/skills/le-use-compose-ops.md`); in the images, the base image sets it.

### requirements.txt

**Auto-generated** by `jaz python.pip-compile`. Contains fully resolved dependencies with exact versions.

**RULE:** Never edit this file manually. Always regenerate with `jaz python.pip-compile`.

### requirements.dev.txt

Development-only dependencies:

```
factory-boy
faker
pytest
pytest-django
pytest-html
pytest_pudb
pytest-socket
```

**RULE:** Include testing frameworks, debugging tools, and development utilities.

---

## The service's jazzoo file

The service's targets live in `src/services/<service_name>/jazzoo`. `jaz` loads the `jazzoo` file of the
current directory, and the WORKDIR of the container is `/app/src`, so in the container `jaz run-server`
runs the service's target (e.g. `jaz docker.exec blogs_be cmd="jaz run-server"` from the host).

Every service must provide the `run-server` target:

```
[interactive]
run-server():
    python manage.py runserver 0.0.0.0:8000
```

It must also provide `init-dev`, which prepares the service for development (e.g. creates the database and runs
the migrations), and `check`, which succeeds when the server responds. `jaz compose.init` runs them (see
[le-use-compose-ops](./le-use-compose-ops.md)): `init-dev` and `run-server` as the command of the container, and
`check` as its healthcheck.

```
init-dev(): create-db() migrate() collect-static() create-superuser()

check():
    python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/admin/login/', timeout=5)"
```

**RULE:** `init-dev` must be safe to run again (e.g. `create-db` and `create-superuser` ignore what exists).

**RULE:** `check` uses `127.0.0.1`, not `localhost`: the server binds to `0.0.0.0`, and in the container
`localhost` may resolve to `::1`.

**RULE:** `run-server` depends on the service type (Django uses `manage.py runserver`, Flask might use `flask run`, etc.).

**RULE:** Mark targets that run a server, a REPL or a prompt as `[interactive]`, so that their output reaches the terminal while they run.

**RULE:** Add the service to `/python/services` in `env/local/config/base.yaml`, so that `jaz python.pip-compile` compiles its requirements. The Python version that it compiles for (`--python-version=3.12`) should match the base image Python version.

## Optional targets

It can optionally also provide this target (which is run on the host)

```
create-opt-paths():
    sudo mkdir -p /opt/projects/blogs/blogs_be
    sudo echo     "- cmd: echo 'start of the fish history'" >> /opt/projects/blogs/blogs_be/fish_history
    sudo mkdir -p /opt/projects/blogs/blogs_be/ipython
    sudo mkdir -p /opt/projects/blogs/blogs_be/assets
    sudo touch    /opt/projects/blogs/blogs_be/pytest_report.html
    sudo mkdir -p /opt/projects/blogs/blogs_be/media  # when using django
    sudo mkdir -p /opt/projects/blogs/blogs_be/static  # when using django
    sudo chmod -R 777 /opt/projects/blogs
```

---

## Checklist

- [ ] Service directory created at `src/services/<service_name>/`
- [ ] `Dockerfile.local` created with minimal file copying and dev dependencies
- [ ] `Dockerfile` created with full file copying and production-only dependencies
- [ ] Both Dockerfiles use `/app/src` as WORKDIR
- [ ] Install scripts added if service needs system packages
- [ ] `setup.py` created with placeholder generation logic
- [ ] `pyproject.toml` created with src-layout configuration
- [ ] `setup.cfg` created with isort and tool configuration
- [ ] `README.md` created with service description
- [ ] `requirements.in` created with direct dependencies
- [ ] `requirements.editable` created with local library references
- [ ] `requirements.dev.txt` created with development dependencies
- [ ] `jazzoo` file created with the `run-server`, `init-dev` and `check` targets
- [ ] Service added to `docker-compose.init-stack.yml`
- [ ] Service added to `/python/services` in `env/local/config/base.yaml`
- [ ] `requirements.editable` lists the jazzoo stub library
- [ ] Python package created at `src/<service_name>/__init__.py`
