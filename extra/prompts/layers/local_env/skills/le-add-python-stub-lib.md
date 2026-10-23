# Skill: le-add-python-stub-lib

Applies when adding a Python library stub to the stack that references external library code stored outside the stack directory.

Primary reference: `../examples/blogs/src/libs/woodstock/`

---

## What is a stub library?

A stub library is a minimal Python package structure in `<stack>/src/libs/` that acts as a placeholder for a real library whose source code lives elsewhere (e.g., in a separate repository or development directory).

**Purpose:**

- Allows the library to be installed in Docker images during build
- Defines the library's dependencies in `pyproject.toml`
- The actual source code is overlaid at runtime via `docker-compose.override.yml`
- Enables local development of both the stack and the library simultaneously

**When to use:**

- Library is developed in a separate repository

**When NOT to use:**

- For libraries that are part of the stack → see `layers/local_env/skills/le-add-python-lib.md`

---

## Core library setup

For the basic library structure (creating pyproject.toml, setup.py, README.md, etc.), follow **Steps 1-6** in:

→ **`layers/local_env/skills/le-add-python-lib.md`**

The key difference for stub libraries:

- **No tests directory** - tests live with the real library
- **Minimal `__init__.py`** - just a placeholder comment
- **Minimal README** - just the library name

---

## File structure

A stub library contains only the minimal files needed for Python packaging:

```
<stack>/src/libs/<lib_name>/
├── pyproject.toml          # Package metadata and dependencies
├── setup.py                # Placeholder creation script
├── README.md               # Minimal library description
└── src/
    └── <lib_name>/
        └── __init__.py     # Placeholder module (not full implementation)
```

Example for `woodstock`:

```
src/libs/woodstock/
├── pyproject.toml
├── setup.py
├── README.md
└── src/
    └── woodstock/
        └── __init__.py
```

**IMPORTANT:** Do NOT create a `tests/` directory in the stub. Tests live with the real library.

---

## Stub-specific files

### Minimal `__init__.py`

Create `src/<lib_name>/__init__.py` with just a placeholder:

```python
# Placeholder for the real library
```

This file will be overwritten when the real library code is overlaid at runtime.

**RULE:** Do NOT implement any functionality in the stub's `__init__.py`.

### Minimal README.md

```markdown
# woodstock
```

Just the library name. The real documentation lives with the real library.

---

## Dockerfile configuration

Follow the same Dockerfile configuration as described in **Step 10** of `le-add-python-lib.md`:

### In Dockerfile.local:

```dockerfile
# Copy the requirements file(s) for each library
COPY libs/woodstock/pyproject.toml libs/woodstock/setup.py libs/woodstock/README.md /app/libs/woodstock/
```

Only copy the minimal files needed for installation, not the source code.

### In Dockerfile:

```dockerfile
# Copy each library
COPY libs/woodstock /app/libs/woodstock
```

Copy the full stub directory for production builds.

**RULE:** In Dockerfile.local, only copy metadata files (pyproject.toml, setup.py, README.md). The source code is overlaid at runtime.

**RULE:** In Dockerfile, copy the entire stub directory.

---

## Docker Compose configuration for stubs

### Step 1: Add to docker-compose.src-overlays.yml

Add the stub library overlay to `docker-compose.src-overlays.yml`:

```yaml
services:
  blogs_be:
    volumes:
      - ${ROOT_DIR}/src/services/blogs_be:/app/src
      - ${ROOT_DIR}/src/libs/woodstock:/app/libs/woodstock
```

This ensures the stub is available even when the real library isn't overlaid.

**RULE:** This overlay is for the stub itself, not the real library. The real library overlay goes in `docker-compose.override.yml`.

---

### Step 2: Overlay real library code in docker-compose.override.yml

To use the real library code during development, add a volume mount in `docker-compose.override.yml`:

```yaml
services:
  blogs_be:
    volumes:
      # Lib code overlays
      - /home/maarten/projects/woodstock/src/libs/woodstock:/app/libs/woodstock
```

**Path structure:** The real library should also use src-layout:

```
/home/maarten/projects/woodstock/
└── src/
    └── libs/
        └── woodstock/
            ├── __init__.py
            ├── server/
            └── ...
```

This mounts the real library's source code over the placeholder stub in the container.

**RULE:** Use absolute paths in `docker-compose.override.yml` since it's developer-specific.

**RULE:** The real library must have the same package structure as expected by the stub.

---

## How it works

### During Docker build:

1. Stub library metadata files are copied into the image
2. `pip install -e /app/libs/woodstock` installs the stub in editable mode
3. This installs the dependencies listed in the stub's `pyproject.toml`
4. The placeholder `__init__.py` is present but not used

### During container runtime:

1. If no overlay in `docker-compose.override.yml`: the stub's placeholder code is used (minimal functionality)
2. If overlay configured: the real library code is mounted over `/app/libs/woodstock`, replacing the placeholder
3. The editable install means Python immediately sees the real library code
4. Dependencies are already installed from the stub's `pyproject.toml`

### Benefits:

- No rebuild needed when editing library code
- Library dependencies are baked into the image
- Works whether or not the real library is available
- Multiple developers can have different library paths

---

## Keeping stub in sync with real library

When the real library changes dependencies:

1. Update the stub's `pyproject.toml` to match
2. Run `just pip-compile` in the service
3. Rebuild the service image: `just build use_dockerfile_local=true`

**RULE:** The stub's `pyproject.toml` dependencies must match the real library's dependencies.

---

## Checklist

### Core setup (following le-add-python-lib.md Steps 1-6)
- [ ] Stub directory created at `src/libs/<lib_name>/`
- [ ] `pyproject.toml` created with correct dependencies matching real library
- [ ] `setup.py` created with placeholder generation logic
- [ ] `README.md` created with library name only
- [ ] Placeholder `src/<lib_name>/__init__.py` created (just a comment, no implementation)
- [ ] Service's `requirements.editable` references stub with `${<STACK>_LIBS_DIR}`

### Stub-specific configuration
- [ ] **No tests directory created** (tests live with real library)
- [ ] Service's `Dockerfile.local` copies stub metadata files only (pyproject.toml, setup.py, README.md)
- [ ] Service's `Dockerfile` copies full stub directory
- [ ] Stub overlaid in `docker-compose.src-overlays.yml`
- [ ] Real library code overlaid in `docker-compose.override.yml` (developer-specific)
- [ ] Real library uses same src-layout structure as stub expects
