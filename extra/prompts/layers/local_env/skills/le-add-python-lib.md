# Skill: le-add-python-lib

Applies when adding a Python library to the stack where the source code lives within the stack directory.

Primary reference: `../examples/blogs/src/libs/python_toolkit/`

---

## What this skill covers

This skill describes how to create a Python library in the stack with full source code:

- Creating the library directory structure
- Setting up `pyproject.toml` with dependencies
- Creating `setup.py` for package installation
- Setting up the source code structure
- Adding tests
- Configuring development tools (isort, etc.)

## What this skill does NOT cover

The following topics are covered in separate skills:

- **Creating a stub library that references external code** → see `layers/local_env/skills/le-add-python-stub-lib.md`
- **Adding the library to Docker Compose** → see `layers/local_env/skills/le-add-python-service-to-compose.md`
- **Referencing the library in services** → see target-specific documentation
- **How to write the Python files that live in the library** → see target-specific documentation

---

## File structure

A full Python library contains:

```
<stack>/src/libs/<lib_name>/
├── pyproject.toml          # Package metadata and dependencies
├── setup.py                # Placeholder creation script
├── setup.cfg               # Tool configuration (isort, etc.)
├── README.md               # Library description
├── src/
│   └── <lib_name>/
│       ├── __init__.py     # Package initialization
│       └── ...             # Library modules
└── tests/
    └── test_*.py           # Test files
```

Example for `python_toolkit`:

```
src/libs/python_toolkit/
├── pyproject.toml
├── setup.py
├── setup.cfg
├── README.md
├── src/
│   └── python_toolkit/
│       ├── __init__.py
│       └── logging.py
└── tests/
    └── test_logging.py
```

---

## Step 1: Create the directory structure

Create the library directory:

```bash
mkdir -p src/libs/python_toolkit/src/python_toolkit
mkdir -p src/libs/python_toolkit/tests
```

**RULE:** Use `src/<lib_name>/` layout (src-layout) inside the library, not flat layout.

**RULE:** Create a separate `tests/` directory at the library root for test files.

---

## Step 2: Create pyproject.toml

The `pyproject.toml` file defines the package metadata, dependencies, and build configuration:

```toml
[project]
name = "python_toolkit"
version = "0.1.0"
readme = "README.md"
dependencies = ["requests>=2.31.0"]

[project.optional-dependencies]
test = ["pytest>=7.0.0", "pytest-cov>=4.0.0"]

[tool.setuptools.package-dir]
"" = "src"

[tool.setuptools.packages.find]
where = ["src"]

[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"
```

### Key sections

**dependencies:** List all runtime dependencies the library needs

```toml
dependencies = ["requests>=2.31.0"]
```

**RULE:** Use version constraints to ensure compatibility (e.g., `>=2.31.0` instead of just `requests`).

**RULE:** Only list direct dependencies, not transitive dependencies.

**optional-dependencies:** Development and testing dependencies

```toml
[project.optional-dependencies]
test = ["pytest>=7.0.0", "pytest-cov>=4.0.0"]
```

These are installed separately (e.g., `pip install -e ".[test]"`).

**scripts:** Entry points if the library provides CLI commands

```toml
[project.scripts]
my_tool = "python_toolkit.cli:main"
```

Only include if the library has CLI entry points.

**package-dir:** Use src-layout

```toml
[tool.setuptools.package-dir]
"" = "src"
```

**RULE:** Always use src-layout for consistency across the codebase.

---

## Step 3: Create setup.py

Create a `setup.py` that generates a placeholder package:

```python
from pathlib import Path

from setuptools import setup


def create_placeholder():
    this_directory = Path(__file__).parent
    pkg_directory = this_directory / "src" / "python_toolkit"

    if not pkg_directory.exists():
        pkg_directory.mkdir(parents=True)
        with open(pkg_directory / "__init__.py", "w") as f:
            f.write("# Placeholder for package")


if __name__ == "__main__":
    create_placeholder()
    setup()
```

**What this does:**

1. Creates the package directory if it doesn't exist
2. Creates a placeholder `__init__.py` file
3. Calls `setup()` to install the package

**RULE:** Replace `python_toolkit` with your actual library name in the path.

---

## Step 4: Create setup.cfg

Configure development tools like isort:

```cfg
[isort]
multi_line_output=3
include_trailing_comma=True
force_grid_wrap=0
use_parentheses=True
line_length=88
```

**RULE:** Use consistent formatting configuration across all libraries.

---

## Step 5: Create README.md

Create a README with a brief description:

```markdown
# python_toolkit

A collection of Python utility functions for common development tasks.
```

**RULE:** Keep the README concise. Detailed documentation should live in docstrings or separate docs.

---

## Step 6: Create the package structure with a single `__init__.py` file

Create `src/<lib_name>/__init__.py`:

This skill does not cover how Python modules in the library are written.
The example code contains a `src/python_toolkit/logging.py` file for illustration purposes only (for the purpose of this skill, you can ignore it).

---

## Step 7: Create tests directory

Create a test files directory in `tests/`. This skill does not cover how tests are written.

---

## Step 8: Reference in service requirements.editable

Services that use the library must reference it in their `requirements.editable` file:

In `<stack>/src/services/<service_name>/requirements.editable`:

```
-e ${BLOGS_LIBS_DIR}/python_toolkit
```

**RULE:** Use the `<STACK>_LIBS_DIR` environment variable to reference the library location.

**RULE:** The `-e` flag installs in editable mode, allowing live code changes.

This file is used during `jaz python.pip-compile` to include the library in `requirements.txt`.

---

## Step 9: Copy library files in Dockerfile

Services must copy the library files in their Dockerfiles:

### In Dockerfile.local:

```dockerfile
# Copy the requirements file(s) for each library
COPY libs/python_toolkit/pyproject.toml libs/python_toolkit/setup.py libs/python_toolkit/README.md /app/libs/python_toolkit/
```

Only copy the minimal files needed for installation, not the source code (which gets overlaid).

### In Dockerfile:

```dockerfile
# Copy each library
COPY libs/python_toolkit /app/libs/python_toolkit
```

Copy the full library directory for production builds.

**RULE:** In Dockerfile.local, only copy metadata files (pyproject.toml, setup.py, README.md). The source code is overlaid at runtime.

**RULE:** In Dockerfile, copy the entire library directory.

---

## Step 10: Add to docker-compose.src-overlays.yml

Add the library overlay to `docker-compose.src-overlays.yml` for the services that are using the library:

```yaml
services:
  blogs_be:
    volumes:
      - ${ROOT_DIR}/src/services/blogs_be:/app/src
      - ${ROOT_DIR}/src/libs/python_toolkit:/app/libs/python_toolkit
```

This ensures the library source code is available for live editing during development.

**RULE:** Mount the library to `/app/libs/<lib_name>` to match the COPY path in the Dockerfile.

---

## Checklist

- [ ] Library directory created at `src/libs/<lib_name>/`
- [ ] `pyproject.toml` created with correct dependencies
- [ ] `setup.py` created with placeholder generation logic
- [ ] `setup.cfg` created with tool configuration
- [ ] `README.md` created with library description
- [ ] Package `src/<lib_name>/__init__.py` created
- [ ] Service's `requirements.editable` references library with `${<STACK>_LIBS_DIR}`
- [ ] Service's `Dockerfile.local` copies library metadata files only
- [ ] Service's `Dockerfile` copies full library directory
- [ ] Library overlaid in `docker-compose.src-overlays.yml`
