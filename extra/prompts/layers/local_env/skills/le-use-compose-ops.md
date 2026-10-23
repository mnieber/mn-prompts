# Skill: le-use-compose-ops

Applies when setting up Just commands to manage Docker Compose operations for the local development stack.

Primary reference: `../examples/blogs/env/local/just/compose/`

---

## What this skill covers

This skill describes how to set up and use Just commands for Docker Compose operations:

- Setting up the justfile structure for compose operations
- Configuring ROOT_DIR, COMPOSE_DIR, and COMPOSE_PROJECT_NAME
- Using the standard compose operation commands

## What this skill does NOT cover

- **Service-specific Just commands** → see target-specific documentation (e.g., `targets/django_app`)
- **Python-specific Just commands** → see `layers/local_env/skills/le-use-python-ops.md`

---

## Justfile structure

The stack uses a modular justfile structure:

```
<stack>/
├── justfile                           # Root justfile (delegates to env/local)
└── env/
    └── local/
        ├── justfile                   # Main local env justfile
        ├── .local.env                 # Developer-specific variables (gitignored)
        └── just/
            ├── compose/
            │   ├── index.just         # Compose operations coordinator
            │   ├── build.just         # Build commands
            │   ├── run.just           # Run commands (up, down, shell, run_cmd)
            │   ├── env-files.just     # Environment file compilation
            │   └── lib/               # Internal implementation helpers
            └── python/
                └── index.just         # Python operations
```

---

## Step 1: Create the root justfile

Create `<stack>/justfile` that delegates to the local environment:

```makefile
import 'env/local/justfile'
```

**RULE:** The root justfile should be minimal and just import the environment-specific justfile.

---

## Step 2: Set up env/local/justfile

Create `<stack>/env/local/justfile` with the core configuration:

```makefile
import './just/compose/index.just'

set dotenv-load := true
set dotenv-filename := 'env/local/.local.env'

# Determine root properties
export ROOT_DIR := canonicalize(source_directory() / "../..")

# Determine compose properties
export COMPOSE_DIR := source_directory() / "docker"
export COMPOSE_PROJECT_NAME := "blogs"
```

### Configuration variables

**ROOT_DIR:** Absolute path to the stack root directory

```makefile
export ROOT_DIR := canonicalize(source_directory() / "../..")
```

Uses `source_directory()` to get the justfile's location and goes up two levels to reach the stack root.

**COMPOSE_DIR:** Directory containing docker-compose files

```makefile
export COMPOSE_DIR := source_directory() / "docker"
```

Points to `env/local/docker/` where all compose files live.

**COMPOSE_PROJECT_NAME:** Docker Compose project name

```makefile
export COMPOSE_PROJECT_NAME := "blogs"
```

Replace `"blogs"` with your stack name. This determines the prefix for container names and networks.

**HOST_IP:** The host machine's IP address on the local network

```makefile
export HOST_IP := env_var_or_default("HOST_IP", `ip -4 addr show 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | grep -v 127.0.0.1 | head -1 || echo ""`)
```

Detected automatically from the host's network interfaces, excluding loopback. Useful when a container needs to reach a service running on the host machine (e.g. an external dependency not in Docker Compose). Falls back to an empty string if detection fails, in which case the developer can set it explicitly in `.local.env`.

**PYTHON:** Python executable path

```makefile
export PYTHON := `which python3 2>/dev/null || which python`
```

Used by Python-related commands.

**RULE:** Always use `canonicalize()` for ROOT_DIR to ensure absolute paths.

**RULE:** The COMPOSE_PROJECT_NAME should match your stack name and be lowercase.

---

## Step 3: Create .local.env for developer settings

Create `<stack>/env/local/.local.env` for developer-specific variables (gitignored):

```bash
BLOGS_SHELL_COMMAND=fish
BLOGS_USE_DOCKERFILE_LOCAL=true
BLOGS_OS_CUSTOM_PACKAGES="nano curl fish"
BLOGS_PIP_CUSTOM_PACKAGES=""
```

**Common variables:**

- `<STACK>_SHELL_COMMAND`: Shell to use when running `just shell` (e.g., `bash`, `fish`, `zsh`)
- `<STACK>_USE_DOCKERFILE_LOCAL`: Whether to use Dockerfile.local by default (`true`/`false`)
- `<STACK>_OS_CUSTOM_PACKAGES`: Additional OS packages to install in base images

**RULE:** Replace `BLOGS` prefix with your stack name in uppercase.

**RULE:** This file should be gitignored as it contains developer preferences.

---

## Step 4: Copy the docker operations justfiles

Copy the following structure from the blogs example to your stack:

```
env/local/just/compose/
├── index.just              # Copy and update
├── build.just              # Copy as-is
├── run.just                # Copy as-is
├── env-files.just          # Copy as-is
└── lib/                    # Copy entire directory as-is
```

### Update Just file to use the correct stack name in environment variables.

The following renamings can safely be done globally in the <xxx_stack>/env/local directory:

- Replace BLOGS_USE_DOCKERFILE_LOCAL with <XXX_STACK>\_USE_DOCKERFILE_LOCAL
- Replace BLOGS_SHELL_COMMAND with <XXX_STACK>\_SHELL_COMMAND
- Replace BLOGS_OS_CUSTOM_PACKAGES with <XXX_STACK>\_OS_CUSTOM_PACKAGES
- Replace BLOGS_PIP_CUSTOM_PACKAGES with <XXX_STACK>\_PIP_CUSTOM_PACKAGES
- Replace BLOGS_LIBS_DIR with <XXX_STACK>\_LIBS_DIR

---

## Available compose operation commands

Once the justfiles are set up, you can use these commands from the stack root:

### `just build [use_dockerfile_local=true/false] [use_no_cache=true/false]`

Builds all service images.

```bash
# Build using Dockerfile (production)
just build

# Build using Dockerfile.local (development)
just build use_dockerfile_local=true

# Build without cache
just build use_no_cache=true
```

**What it does:**

1. Compiles environment files (`.env.in` → `.env`)
   - In a service's `.env.in` file, reference secrets with `${VARIABLE_NAME}` where VARIABLE_NAME is defined in `secrets.env`.
   - Non-secrets are hard-coded directly in the .env.in file
2. Builds all services defined in docker-compose.yml
3. Uses Dockerfile.local if `use_dockerfile_local=true`

Note that the user is responsible for calling `pip install compile-env` in their local python env.

**When to use:** After changing Dockerfile, requirements, or dependencies.

### `just build-base-images [use_no_cache=true/false]`

Builds base images (e.g., `<stack>_base_python`).

```bash
just build-base-images
```

**What it does:**

1. Builds images defined in `docker-compose.base-images.yml`
2. These images are used as base for service images

**When to use:** After changing base image Dockerfiles or when setting up a new stack.

### `just up [use_dockerfile_local=true/false]`

Starts all services in detached mode.

```bash
# Start with Dockerfile.local images
just up use_dockerfile_local=true

# Start with production Dockerfiles
just up
```

**What it does:**

1. Touches docker-compose.override.yml (creates if missing)
2. Compiles environment files
3. Starts all services with docker-compose up
4. Includes src-overlays and override files (depending on use_dockerfile_local)

**When to use:** After building, to start the development environment.

### `just down`

Stops and removes all containers, networks.

```bash
just down
```

**What it does:**

1. Runs `docker compose down --remove-orphans`
2. Removes stopped containers and networks

**When to use:** To clean up the environment, before rebuilding, or when switching branches.

### `just restart [use_dockerfile_local=true/false] [use_no_cache=true/false]`

Full cycle: down → pip-compile → build → up.

```bash
# Restart with development images
just restart use_dockerfile_local=true

# Restart with fresh build
just restart use_dockerfile_local=true use_no_cache=true
```

**What it does:**

1. Stops all services (`down`)
2. Recompiles Python requirements (`pip-compile`)
3. Rebuilds images (`build`)
4. Starts services (`up`)

**When to use:** After major changes (dependencies, Dockerfile changes) or when troubleshooting.

### `just shell <service_name>`

Opens a shell in a running service container.

```bash
just shell blogs_be
```

**What it does:**

1. Compiles environment files
2. Execs into the running container
3. Uses the shell defined in `<STACK>_SHELL_COMMAND` (from `.local.env`)

**When to use:** Never. It's expected that you do not run this command. It's a convenience command for the user.

**RULE:** The container must be running (`just up`) before using `just shell`.

### `just run_cmd <service_name> <cmd> [use_dockerfile_local=true/false]`

Runs a one-off command in a new container instance.

```bash
# Run Django migrations
just run_cmd blogs_be "python manage.py migrate"

# Run tests
just run_cmd blogs_be "pytest"
```

**What it does:**

1. Compiles environment files
2. Runs `docker compose run` with the specified command
3. Creates a new container (doesn't use the running one)
4. Removes container after command completes (`--rm`)

**When to use:** To run commands when debugging or operating the stack in collaboration with the user.

### `just compile-env-files`

Compiles `.env.in` templates to `.env` files.

```bash
just compile-env-files
```

**What it does:**

1. Touches `secrets.env` if it doesn't exist
2. Runs the Python script to compile all `.env.in` files in `env/local/docker/env_files/`
3. Substitutes variables from `secrets.env`

**When to use:** After modifying `.env.in` files or `secrets.env`.

**Note:** This command is automatically called by other commands (build, up, down, etc.), so you rarely need to run it manually.

---

## Typical workflow

### Initial setup

```bash
just build-base-images
just build use_dockerfile_local=true
just up use_dockerfile_local=true
```

### After dependency changes

```bash
just restart use_dockerfile_local=true
```

---

## Checklist

- [ ] Root `justfile` created with import statement
- [ ] `env/local/justfile` created with ROOT_DIR, COMPOSE_DIR, COMPOSE_PROJECT_NAME
- [ ] `env/local/.local.env` created with developer preferences (gitignored)
- [ ] Compose operations justfiles copied to `env/local/just/compose/`
- [ ] Variable names updated in build.just and run.just to match stack name
- [ ] `env/local/.gitignore` excludes `docker/env_files/*.env` and `secrets.env`
- [ ] Non-secrets are hard-coded directly in the .env.in file
