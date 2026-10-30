# Skill: le-add-base-image

Applies when adding a base Docker image that will be used by multiple services in the stack.

Primary reference: `../examples/blogs/env/local/docker/base_images/`

---

## What is a base image?

A base image is a Docker image that provides common dependencies and configuration shared by multiple services. Instead of each service installing the same tools (Python, uv, etc.), they all inherit from a base image.

**Benefits:**
- Faster service builds (shared layers cached)
- Consistency across services
- Easier maintenance of common dependencies

---

## File structure

```
env/local/docker/
├── docker-compose.base-images.yml    # Base image definitions
└── base_images/
    ├── Dockerfile.base.python        # Python base image
    ├── Dockerfile.base.node          # Node base image (if needed)
    └── install_scripts/
        └── nop.sh                    # No-op script placeholder
```

---

## Step 1: Create docker-compose.base-images.yml

Create `env/local/docker/docker-compose.base-images.yml` to define your base images:

```yaml
services:
  base_python:
    build:
      context: ./base_images
      dockerfile: Dockerfile.base.python
    image: blogs_base_python
```

**Service naming:** Use `base_<language>` as the service name (e.g., `base_python`, `base_node`)

**Image naming:** Use `<stack_name>_base_<language>` as the image name (e.g., `blogs_base_python`)

**Build context:** Always use `./base_images` relative to the compose file location

**RULE:** Replace `blogs` with your actual stack name.

---

## Step 2: Create the base image Dockerfile

Create `env/local/docker/base_images/Dockerfile.base.python`:

```dockerfile
FROM python:3.12-slim

# Install standard OS packages.
RUN apt-get update && \
    apt-get install -y curl wget nano telnet && \
    rm -rf /var/lib/apt/lists/*

# Optionally install an LLM tool (e.g. INSTALL_LLM_SCRIPT=install-claude-code.sh).
ARG INSTALL_LLM_SCRIPT=nop.sh
COPY install_scripts/${INSTALL_LLM_SCRIPT} /app/install_scripts/
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    bash /app/install_scripts/${INSTALL_LLM_SCRIPT}

# Install uv
RUN curl -LsSf https://astral.sh/uv/0.8.22/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Upgrade pip
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --break-system-packages --upgrade pip

# Install non-geomodel Python packages.
# You can extend PIP_CUSTOM_PACKAGES with your favourite packages (e.g. pudb).
ARG PIP_CUSTOM_PACKAGES
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --break-system-packages \
    watchdog ${PIP_CUSTOM_PACKAGES}

# In a dev image, it's okay to update the package list without worrying about the
# extra space this takes.
RUN apt-get update

# Install custom OS packages.
# You can extend OS_CUSTOM_PACKAGES with your favourite packages.
ARG OS_CUSTOM_PACKAGES
RUN if [ -n "$OS_CUSTOM_PACKAGES" ]; then apt-get install -y $OS_CUSTOM_PACKAGES; else echo "No custom OS packages to install"; fi

ENV PYTHONUNBUFFERED 1

# Libraries will be copied to this directory.
ENV BLOGS_LIBS_DIR="/app/libs"

WORKDIR /app/src
```

### Key sections explained

**Base image:** Start from official language image
```dockerfile
FROM python:3.12-slim
```
Use slim variants to keep image size down.

**Standard OS packages:** Tools needed by most services
```dockerfile
RUN apt-get update && \
    apt-get install -y curl wget nano telnet && \
    rm -rf /var/lib/apt/lists/*
```

**LLM tool installation (optional):** Placeholder for AI coding assistants
```dockerfile
ARG INSTALL_LLM_SCRIPT=nop.sh
COPY install_scripts/${INSTALL_LLM_SCRIPT} /app/install_scripts/
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    bash /app/install_scripts/${INSTALL_LLM_SCRIPT}
```
Uses a no-op script by default. Replace with actual install script if needed.

**uv installation:** Fast Python package installer
```dockerfile
RUN curl -LsSf https://astral.sh/uv/0.8.22/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"
```

**Custom packages:** Build arguments for developer customization
```dockerfile
ARG PIP_CUSTOM_PACKAGES
ARG OS_CUSTOM_PACKAGES
```
These are populated from `/compose/os_custom_packages` and `/compose/pip_custom_packages` in the config during build.

**Libraries directory:** Environment variable for library location
```dockerfile
ENV BLOGS_LIBS_DIR="/app/libs"
```
Used by services to reference shared libraries. Replace `BLOGS` with your stack name.

**RULE:** Always set WORKDIR to `/app/src` to match service expectations.

**RULE:** Use `--mount=type=cache` for package manager caches to speed up rebuilds.

**RULE:** Don't install jazzoo in the base image. Each service installs it as a stub library (see
`layers/local_env/skills/le-add-python-stub-lib.md`), so that `jaz` runs the service's `jazzoo` file.

---

## Step 3: Create install scripts directory

Create `env/local/docker/base_images/install_scripts/nop.sh`:

```bash
echo
```

This is a no-op script that does nothing. It's the default value for `INSTALL_LLM_SCRIPT`.

**RULE:** Make the script executable: `chmod +x nop.sh`

If you want to add an LLM tool (like Claude Code), create a separate install script and reference it via build args.

---

## Step 4: Build the base image

The base image is built using the `jaz compose.build-base-images` target:

```bash
jaz compose.build-base-images
```

This target is described in `layers/local_env/skills/le-use-compose-ops.md`.

**When to build:**
- During initial stack setup
- After modifying the base image Dockerfile
- After changing the custom package lists in the config

---

## Using the base image in services

Once the base image is built, services reference it in their Dockerfiles:

```dockerfile
FROM blogs_base_python

# Service-specific setup continues...
```

The image name must match what's defined in `docker-compose.base-images.yml`.

---

## Customizing with build arguments

Developers can customize base images in their own config layer, `env/local/config/local.yaml`:

```yaml
compose:
  os_custom_packages: nano curl fish
  pip_custom_packages: pudb ipython
```

These are passed as build arguments when running `jaz compose.build-base-images`.

**RULE:** The build arguments are passed by `compose_tools.py`. No manual configuration needed.

---

## Adding additional base images

To add a base image for a different language (e.g., Node.js):

1. Add a service definition in `docker-compose.base-images.yml`:
```yaml
services:
  base_python:
    # ... existing python service

  base_node:
    build:
      context: ./base_images
      dockerfile: Dockerfile.base.node
    image: blogs_base_node
```

2. Create `base_images/Dockerfile.base.node` following similar patterns

3. Run `jaz compose.build-base-images` to build both images

**RULE:** Multiple base images can coexist. The compose file builds all services defined in it.

---

## Checklist

- [ ] `docker-compose.base-images.yml` created with service definitions
- [ ] Base image Dockerfile created in `base_images/` directory
- [ ] Standard tools installed (uv, curl, wget, etc.)
- [ ] Build arguments defined for custom packages
- [ ] WORKDIR set to `/app/src`
- [ ] Libraries directory environment variable set (e.g., `BLOGS_LIBS_DIR`)
- [ ] `install_scripts/nop.sh` created
- [ ] Base image builds successfully with `jaz compose.build-base-images`
- [ ] Services reference the base image in their Dockerfiles
- [ ] Custom packages configured in `env/local/config/local.yaml` (if needed)
