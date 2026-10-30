# Skill: le-add-python-stub-lib

Applies when adding a Python library stub to the stack that references external library code stored outside the stack directory.

Primary reference: `../examples/blogs/src/libs/woodstock/`

---

## What is a stub library?

A stub library is a minimal Python package structure in `<stack>/src/libs/` that acts as a placeholder for a real library whose source code lives elsewhere (e.g., in a separate repository or development directory).

**Why we need it:**

Sometimes a developer works on the stack and on an external library (e.g. `jazzoo`) at the same time. They want
changes to the library to show up in the stack's containers straight away, without first releasing the library and
rebuilding the images. To make that work:

- The image must contain an installed package whose code can be swapped at runtime. An editable install of a
  package at `/app/libs/<lib_name>` gives us that.
- The real library's source is not part of the stack's build context, so the build cannot copy it. The stub provides
  the package metadata (name, dependencies, console scripts) that the editable install needs.
- At runtime, `docker-compose.override.yml` mounts the developer's checkout of the real library over the stub. The
  editable install then points at the real code.

**Purpose:**

- Allows the library to be installed in Docker images during build
- Defines the library's dependencies in `pyproject.toml`
- The actual source code is overlaid at runtime via `docker-compose.override.yml`
- Enables local development of both the stack and the library simultaneously

**Who it is for:**

The stub is only useful to developers who have a checkout of the real library and overlay it. For everyone else, the
stub is broken: its placeholder code does nothing and its console scripts fail. Other developers should therefore
install the released package instead. See [Switching between stub and real package](#switching-between-stub-and-real-package).

**When to use:**

- Library is developed in a separate repository, and you want to develop it together with the stack

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

The stack also has a stub for `jazzoo` (`src/libs/jazzoo/`), which every service installs so that `jaz` runs
in its container. Its real code is mounted from the jazzoo checkout (e.g. `/home/maarten/projects/jazzoo/src`,
which has `pyproject.toml` and `src/jazzoo/`).

---

## Stub-specific files

### Minimal `__init__.py`

Create `src/<lib_name>/__init__.py` with just a placeholder:

```python
# Placeholder for the real library
```

This file will be overwritten when the real library code is overlaid at runtime.

**RULE:** Do NOT implement any functionality in the stub's `__init__.py`.

### Console scripts

**RULE:** The stub's `pyproject.toml` declares the same `[project.scripts]` as the real library. The editable
install creates the console scripts (e.g. `jaz`, `zoo`) from the stub's metadata; the code that they call
arrives with the overlay. Without the overlay, the scripts fail to import their entry points.

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

This section describes the case where the stub is installed.

### During Docker build:

1. Stub library metadata files are copied into the image
2. `pip install -e /app/libs/woodstock` installs the stub in editable mode
3. This installs the dependencies listed in the stub's `pyproject.toml`
4. The placeholder `__init__.py` is present but not used

### During container runtime:

1. If no overlay in `docker-compose.override.yml`: the stub's placeholder code is used, so the library does not work
2. If overlay configured: the real library code is mounted over `/app/libs/woodstock`, replacing the placeholder
3. The editable install means Python immediately sees the real library code
4. Dependencies are already installed from the stub's `pyproject.toml`

### Benefits:

- No rebuild needed when editing library code
- Library dependencies are baked into the image
- Multiple developers can have different library paths

---

## Switching between stub and real package

A service's `requirements.editable` decides which one is installed. To switch, edit the line directly:

```
# Stub (only for developers who overlay the real library code)
-e ${BLOGS_LIBS_DIR}/jazzoo

# Real package (for everyone else)
jazzoo==0.1.0
```

Then run `jaz python.pip-compile` and rebuild the images with `jaz compose.build local=true`.

**RULE:** The committed `requirements.editable` and `requirements.txt` use the real package. A developer who
switches to the stub must not commit that change.

**RULE:** Use the stub as the committed default only when there is no released version of the library yet.

Notes:

- Services without requirements files install the stub directly in `Dockerfile.local` (see
  [Services without uv or requirements files](#services-without-uv-or-requirements-files)). Switch these by
  editing the `pip install` line in the same way.
- The Dockerfiles keep copying the stub into `/app/libs/<lib_name>`, and the compose files keep mounting it. When
  the real package is installed, nothing imports from `/app/libs/<lib_name>`, so the copy and the mounts have no
  effect. A real-code overlay in `docker-compose.override.yml` also has no effect in that case. If edits to the
  library don't show up in the container, check that the stub is installed.
- The stub and the real package may have different dependencies, so switching can change other pins in
  `requirements.txt`. When switching back, check the whole diff. Pins that differ from the stub's version mean
  that the stub's `pyproject.toml` is out of sync with the real library.
- Before committing stack changes that depend on unreleased library changes, release the library and bump the
  version in `requirements.editable`.

---

## Keeping stub in sync with real library

When the real library changes dependencies or console scripts:

1. Update the stub's `pyproject.toml` to match
2. Run `jaz python.pip-compile`
3. Rebuild the service images: `jaz compose.build local=true`

**RULE:** The stub's `pyproject.toml` dependencies must match the real library's dependencies.

---

## Services without uv or requirements files

A service that is not a Python service (e.g. a Node service on an alpine image) installs the stub with pip,
after installing `python3` and `py3-pip`. See `layers/local_env/skills/le-add-react-service-to-compose.md`.

```dockerfile
# Dockerfile.local
COPY libs/jazzoo/pyproject.toml libs/jazzoo/setup.py libs/jazzoo/README.md /app/libs/jazzoo/
RUN pip install --break-system-packages -e /app/libs/jazzoo
```

---

## Checklist

### Core setup (following le-add-python-lib.md Steps 1-6)
- [ ] Stub directory created at `src/libs/<lib_name>/`
- [ ] `pyproject.toml` created with correct dependencies matching real library
- [ ] `setup.py` created with placeholder generation logic
- [ ] `README.md` created with library name only
- [ ] Placeholder `src/<lib_name>/__init__.py` created (just a comment, no implementation)
- [ ] Service's `requirements.editable` uses the real package (e.g. `jazzoo==0.1.0`) in the committed version, or the stub (`-e ${<STACK>_LIBS_DIR}/<lib_name>`) if there is no release yet

### Stub-specific configuration
- [ ] **No tests directory created** (tests live with real library)
- [ ] Service's `Dockerfile.local` copies stub metadata files only (pyproject.toml, setup.py, README.md)
- [ ] Service's `Dockerfile` copies full stub directory
- [ ] Stub overlaid in `docker-compose.src-overlays.yml`
- [ ] Real library code overlaid in `docker-compose.override.yml` (developer-specific)
- [ ] Real library uses same src-layout structure as stub expects
- [ ] Stub declares the same `[project.scripts]` as the real library
